import zmq
import threading
from Raft.states.leader import Leader
from Raft.states.follower import Follower
from Raft.messages.client_message import ClientMessage


class Server(object):

    def __init__(self, name, state, log, neighbors):
        self._name = name
        self._state = state
        self._log = log
        # self._messageBoard = messageBoard
        self._neighbors = neighbors
        self._total_nodes = 0
        self._board = []
        self._commitIndex = 0
        self._currentTerm = 0

        self._lastApplied = 0

        self._lastLogIndex = 0
        self._lastLogTerm = None

        self._state.set_server(self)
    def post_message(self, message):
        self._board.append(message)

        self._board = sorted(self._board,
                                key=lambda a: a.timestamp, reverse=True)

    def get_message(self):
        if (len(self._board) > 0):
            return self._board.pop()
        else:
            return None
    def send_message(self, message):
        # print("Sending Messages!!!")
        for n in self._neighbors:
            message._receiver = n._name
            n.post_message(message)

    def send_message_response(self, message):
        n = [n for n in self._neighbors if n._name == message.receiver]
        if (len(n) > 0):
            n[0].post_message(message)

   

    def on_message(self, message):
        state, response = self._state.on_message(message)

        self._state = state
    
    def send_data(self, message_data):
        """This is called when there is a client request."""
        leader = None
        leaderTerm = None
        for n in self._neighbors:
            if type(n._state) == Leader:
                leader = n._name
                leaderTerm = n._currentTerm
        message = ClientMessage(self._name, leader, leaderTerm, {"command": message_data})
        if leader != None:
            self.send_message_response(message)
        else:
            self._state.run_client_command(message)


