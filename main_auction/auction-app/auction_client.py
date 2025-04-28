import socket
import threading
import json
import sys
from uuid import uuid4
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import auction_client_gui

HOST = "127.0.0.1"
PORT = 8888

class Client(QObject):
    auction_signal = pyqtSignal(dict)
    auction_list_signal = pyqtSignal(dict)

    def __init__(self):
        super(Client, self).__init__()
        self.connected = False
        self.id = str(uuid4())
        self.name: str | None = None
        self.current_auction = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.connected = True
        self.gui = auction_client_gui.MainMenuWindow(self)
        self.gui.show()

    def join_auction(self, auction_id: str):
        if not self.connected:
            return
#        if self.current_auction:
#            self.leave_auction()
        msg = { 
               "sender": "client",
               "msg_type": "connect_user_to_auction",
               "content": {
                   "user": {
                       "name": self.name,
                       "id": self.id,
                       },
                   "auction_id": auction_id
                   }
               },
        self.socket.sendall(json.dumps(msg).encode("utf-8"))
    
    def leave_auction(self):
        msg = { 
               "sender": "client",
               "msg_type": "disconnect_user_from_auction",
               "content": {
                   "user": {
                       "name": self.name,
                       "id": self.id,
                       },
                   "auction_id": self.current_auction
                   }
               },
        self.socket.sendall(json.dumps(msg).encode("utf-8"))

    def send_bid(self, amount):
        msg = { 
               "sender": "client",
               "msg_type": "send_bid",
               "content": {
                   "auction_id": self.current_auction,
                   "bidder": {
                       "name": self.name,
                       "id": self.id,
                       },
                   "amount": amount
                   }
               }
        self.socket.sendall(json.dumps(msg).encode("utf-8"))

    def close_auction(self):
        msg = { 
               "sender": "client",
               "msg_type": "close_auction",
               "content": {
                   "owner_id": self.id,
                   "auction_id": self.current_auction
                   }
               }
        self.socket.sendall(json.dumps(msg).encode("utf-8"))

    def create_new_auction(self, item_name: str, starting_price: float):
        msg = { 
               "sender": "client",
               "msg_type": "create_auction",
               "content": {
                   "owner": {
                       "name": self.name,
                       "id": self.id,
                       },
                   "item_name": item_name,
                   "starting_price": starting_price,
                   "deadline": 1,
                   }
               }
        self.socket.sendall(json.dumps(msg).encode("utf-8"))

    def listen_to_server(self):
        while True:
            print("Waiting to recieve...")
            try:
                msg_bytes = self.socket.recv(2048)
            except:
                break
            if not msg_bytes:
                break
            print(msg_bytes.decode("utf-8"))
            msg = json.loads(msg_bytes.decode("utf-8"))
            if msg["sender"] != "server":
                return
            content = msg["content"]

            if msg["msg_type"] == "auction_info":
                self.auction_signal.emit(content)
                self.current_auction = content["auction_id"]
            if msg["msg_type"] == "update_auction_list":
                self.auction_list_signal.emit(content)

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.run()
    threading.Thread(target=client.listen_to_server).start()
    sys.exit(app.exec_())



