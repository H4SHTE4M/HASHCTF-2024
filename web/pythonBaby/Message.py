import os
import pickle
import time
from hashlib import md5
from flask import jsonify
import base64

import app


def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except Exception:
        return False


class Message:

    def __init__(self, _message, _status):
        self.message = _message
        self.status = _status


class MessageManager:

    def __init__(self):
        # store the hash value of file
        self.MessageList = []
        self.MsgPath = os.path.join(os.getcwd(), "message")

    def update(self):
        # update the MsgManager's MessageList var
        temp = []
        for root, dirs, files in os.walk(self.MsgPath):
            for file in files:
                temp.append(file)
        self.MessageList = temp

    def Store(self, message: Message):
        try:
            # store the (message, status) value from the edit value
            messageBytes = pickle.dumps(message, protocol=4)

            file = md5(str(time.time()).encode()).hexdigest().__str__()

            filePath = os.path.join(os.getcwd(), "message", file)

            if not os.path.exists(self.MsgPath):
                os.makedirs(self.MsgPath)

            with open(filePath, 'wb+') as f:
                f.write(messageBytes)

        except Exception:
            return jsonify(''), 500

    def Show(self):
        global filepath
        try:
            self.update()

            # read /message/* to result dict
            result = {}
            index = 1
            for filename in self.MessageList:
                filepath = os.path.join(os.getcwd(), "message", filename)
                with open(filepath, "rb") as f:
                    content = f.read()
                    m: Message = pickle.loads(content)
                    result[str(index)] = {
                        "message": pickle.loads(base64.b64decode(m.message)) if is_base64(m.message) else m.message,
                        "status": m.status
                    }
                index += 1
            return result
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify(''), 500
