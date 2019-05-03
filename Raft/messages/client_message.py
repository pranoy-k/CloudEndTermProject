from Raft.messages.base import BaseMessage


class ClientMessage(BaseMessage):
    _type = BaseMessage.Client

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)