import configparser
import zmq
import time
import json

config = configparser.ConfigParser()
config.read("config.ini")

def connect():
    global context
    context = zmq.Context()
    global socket
    socket = context.socket(zmq.PUB)
    connection_string = "tcp://" + config['TRACKING']['address'] + ":" + config['TRACKING']['port']
    print("Attempting to connect to tracking socket", connection_string)
    socket.connect(connection_string)
    print("connected to tracking socket")

def disconnect():
    socket.close()

def send_message(caseId, stepName, status):
    unified_case_id = caseId

    if len(caseId.split(".")) > 1:
        unified_case_id = caseId.split(".")[1]
    else:
        input_dir_name_length = len(caseId)
        if input_dir_name_length < 32: 
            unified_case_id = caseId
        elif input_dir_name_length > 32:
            extra_chars_length = input_dir_name_length - 32
            unified_case_id = caseId[extra_chars_length:]
        else:
            unified_case_id = caseId

    currentTimeSeconds = int(time.time())
    messageObject = {'caseId': unified_case_id, 'stepName': stepName, 'status': status, 'timestamp': currentTimeSeconds}
    socket.send_string("%s" % (json.dumps(messageObject)))
    print("sent message")

if __name__ == "__main__":
    global context
    context = zmq.Context()
    global socket
    socket = context.socket(zmq.PUB)
    connection_string = "tcp://10.1.0.205:4000"
    print("Attempting to connect", connection_string)
    socket.connect(connection_string)
    time.sleep(2)
    print("connected to socket")
    socket.send_string("hello doredzzzz")
    # send_message("service_alert", "test 2")
    disconnect()