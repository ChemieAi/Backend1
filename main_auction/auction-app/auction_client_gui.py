import sys
from typing import Optional, Tuple
from auction_client import Client
from PyQt5.QtWidgets import QTextEdit, QDialog, QDialogButtonBox, QLineEdit, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QLabel
from PyQt5 import QtGui

class UsernameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Username")
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_username(self) -> str:
        return self.username_input.text()

class AuctionCreationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Auction")
        self.item_name_label = QLabel("Item Name:")
        self.item_name_input = QLineEdit()
        self.starting_price_label = QLabel("Starting Price:")
        self.starting_price_input = QLineEdit()
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.item_name_label)
        layout.addWidget(self.item_name_input)
        layout.addWidget(self.starting_price_label)
        layout.addWidget(self.starting_price_input)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_new_auction_info(self) -> Tuple[str, str]:
        return self.item_name_input.text(), self.starting_price_input.text()

class AuctionWindow(QWidget):
    def __init__(self, client, auction_id, owner, item_name, starting_price, bids, deadline, open, buyer, is_owner):
        super().__init__()
        self.setWindowTitle("Auction")
        self.client = client
        self.auction_id = auction_id
        self.owner = owner
        self.item_name = item_name
        self.starting_price = starting_price
        self.bids = bids
        self.deadline = deadline
        self.open = open
        self.buyer = buyer
        self.is_owner = is_owner
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.item_label = QLabel("Item Name: " + self.item_name)
        layout.addWidget(self.item_label)

        self.start_price_label = QLabel("Starting Price: " + str(self.starting_price))
        layout.addWidget(self.start_price_label)

        if self.deadline:
            self.deadline = QLabel("Deadline: " + self.deadline)
            layout.addWidget(self.deadline)

        bids_str = ""
        for bid in self.bids:
            bids_str = bids_str + bid["bidder"] + ": " + str(bid["amount"]) + "<br/>"
        self.bid_history_textedit = QTextEdit(bids_str)
        self.bid_history_textedit.setReadOnly(True)
        layout.addWidget(self.bid_history_textedit)
        
        if self.open:
            if not self.is_owner:
                self.bid_amount_input = QLineEdit()
                layout.addWidget(self.bid_amount_input)

                self.send_bid_button = QPushButton("Send Bid")
                self.send_bid_button.clicked.connect(self.send_bid)
                layout.addWidget(self.send_bid_button)
            else:
                self.close_auction_button = QPushButton("Close Bid")
                self.close_auction_button.clicked.connect(self.close_auction)
                layout.addWidget(self.close_auction_button)

        else:
            self.closed_label = QLabel("Auction closed. Buyer: " + self.buyer)
            layout.addWidget(self.closed_label)

        self.setLayout(layout)


    # To-do: Not implemented
    def send_bid(self):
        bid_amount = self.bid_amount_input.text()
        if bid_amount:
            try:
                bid_amount = float(bid_amount)
                self.client.send_bid(bid_amount)
                self.bid_amount_input.clear()  # Clear the bid amount input after sending the bid
            except:
                QMessageBox.warning(self, "Error", "Please enter a number.")
                self.bid_amount_input.clear()  # Clear the bid amount
        else:
            QMessageBox.warning(self, "Error", "Please enter a bid amount.")

    def close_auction(self):
        self.client.close_auction()

    def closeEvent(self, a0: Optional[QtGui.QCloseEvent]) -> None:
        self.client.leave_auction()


class MainMenuWindow(QWidget):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client
        self.setWindowTitle("Main Menu")
        self.auctions = {}
        self.init_ui()
        self.auction_window = None
        name = self.get_username()
        if not name:
            sys.exit()
        self.client.name = name
        self.client.auction_signal.connect(self.set_auction)
        self.client.auction_list_signal.connect(self.update_auction_list)

    def init_ui(self):
        layout = QVBoxLayout()

        self.auction_list = QListWidget()
        layout.addWidget(self.auction_list)

        start_auction_button = QPushButton("Start Auction")
        start_auction_button.clicked.connect(self.create_new_auction)
        layout.addWidget(start_auction_button)

        join_auction_button = QPushButton("Join Auction")
        join_auction_button.clicked.connect(self.join_auction)
        layout.addWidget(join_auction_button)

        self.setLayout(layout)

    def get_username(self):
        dialog = UsernameDialog()
        if dialog.exec_():
            return dialog.get_username()

    def create_new_auction(self):
        while True:
            dialog = AuctionCreationDialog()
            if dialog.exec_():
                item_name, starting_price = dialog.get_new_auction_info()
                try:
                    starting_price = float(starting_price)
                except:
                    QMessageBox.warning(self, "Error", "Please enter a valid starting price.")
                    continue
                if starting_price < 0 or not item_name:
                    QMessageBox.warning(self, "Error", "Please enter valid values.")
                    continue
                break
            else:
                return 
        self.client.create_new_auction(item_name, starting_price)



    def update_auction_list(self, data):
        self.auctions = data
        self.auction_list.clear()
        for auction in self.auctions:
            self.auction_list.addItem(auction)

    def join_auction(self):
        selected_item = self.auction_list.currentItem()
        if selected_item:
            auction_name = selected_item.text()
            auction_id = self.auctions.get(auction_name)
            if auction_id:
                self.client.join_auction(auction_id)
        else:
            QMessageBox.warning(self, "Error", "No auction selected. Please select an auction to join.")

    def set_auction(self, data):
        pos = self.auction_window.pos() if self.auction_window else self.pos()
        self.auction_window = AuctionWindow(self.client, **data)
        self.auction_window.show()
        self.auction_window.move(pos)

    def closeEvent(self, a0: Optional[QtGui.QCloseEvent]) -> None:
        self.client.close()
        sys.exit()
