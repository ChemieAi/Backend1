import socket

class User(object):
    def __init__(self, name: str, id: str, conn: socket.socket):
        self.name = name
        self.id = id
        self.conn = conn
    
    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

class Bid(object):
    def __init__(self, auction_id: str, bidder: User, amount: float):
        self.auction_id = auction_id
        self.bidder = bidder
        self.amount = amount

class Auction(object):
    def __init__(self, auction_id: str,
                 owner: User,
                 item_name: str,
                 starting_price: float,
                 bids: list[Bid],
                 deadline: None | float,
                 open: bool,
                 buyer: None | User):
        self.auction_id = auction_id
        self.owner = owner
        self.item_name = item_name
        self.starting_price = starting_price
        self.bids = bids
        self.deadline = deadline
        self.open = open
        self.buyer = buyer
