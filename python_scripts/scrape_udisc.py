import websocket
import json
import threading

convert_dict = lambda msg: json.dumps(json.dumps(msg))
read_dict = lambda msg: json.loads(msg[3:-2].replace("\\", ""))

connectMsg = convert_dict({"msg":"connect","version":"1","support":["1","pre2","pre1"]})

SCORE_CARD_IDs = ["WGjy4shru6", "CL37y8RYow"] 
SCORE_CARD_ENTRY_IDs = []

lock = threading.Lock()

def on_message(ws, message):
    #print(f"Received message:")
    if message[0] == 'a':
        msg = read_dict(message)
        if msg['msg'] == 'connected':
            connection_id = msg['session']
            playerReqMsg = {"msg":"sub",
                            "id":f"{connection_id}",
                            "name":"scorecardForId",
                            "params":[SCORE_CARD_IDs.pop(0)]
                            }
            playerReqMsg = convert_dict(playerReqMsg)
            ws.send(playerReqMsg)
            #print(f"sending playerReqMsg")
        elif msg['msg'] == 'added' and msg['collection'] == 'Scorecard':
            players = [entry['objectId'] for entry in msg['fields']['entries']]
            with lock:
                SCORE_CARD_ENTRY_IDs.append(players)
            print(SCORE_CARD_ENTRY_IDs)
            scorecardReqMsg = {"msg":"sub",
                               "id":"25rN8BkxE7jBDq9Df",
                               "name":"cardcastEntries",
                               "params":[players]
                               }
            scorecardReqMsg = convert_dict(scorecardReqMsg)
            ws.send(scorecardReqMsg)
            #print(f"sending scorecardReqMsg")
        elif msg['msg'] == 'added' and msg['collection'] == 'ScorecardEntry':

            try:
                user = msg['fields']['users'][0]['objectId']
            except:
                user = msg['fields']['players'][0]['objectId']
            scores = [data['strokes'] for data in msg['fields']['holeScores']]
            roundrating = msg['fields']['roundRating']
            date = msg['fields']['startDate']['$date']
            course = msg['fields']['layoutId']
            print(f"player: {user}, scores: {scores}, roundrating: {roundrating}, date: {date}, course: {course}")
            id = msg['id']
            print(id)
            for group in SCORE_CARD_ENTRY_IDs:
                if id in group:
                    with lock:
                        group.remove(id)
                    if len(group) == 0:
                        ws.close()

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, a, b):
    print("### Closed ###")

def on_open(ws):
    print("### Opened ###")
    ws.send(connectMsg)

def websocket_thread():
        ws = websocket.WebSocketApp("wss://sync.udisc.com/sockjs/657/tgmb0xdy/websocket",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

if __name__ == "__main__":

    num_threads = len(SCORE_CARD_IDs)
    threads = [threading.Thread(target=websocket_thread) for _ in range(num_threads)]
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
