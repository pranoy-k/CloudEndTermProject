from __future__ import print_function
from Raft.states.leader import Leader
from Raft.messages.request_vote import RequestVoteMessage
import time
import random
import locker
from Raft.messages.request_vote import RequestVoteResponseMessage
from Raft.messages.base import BaseMessage
from Raft.messages.response import ResponseMessage
from threading import Thread
# global lock
class Candidate(object):
    
    def __init__(self,timeout = 5):  # time is in sec NOT millisec. 500 origin
        self._last_vote = None
        self._timeout = timeout

    def set_server(self, server):
        self._server = server
        self._votes = {}
        self._start_election()

    def on_vote_request(self, message):
        return self, None

    def on_vote_received(self, message):
        # print("on vote received")
        if message.sender not in self._votes:
            self._votes[message.sender] = message
            # print("message_sender: ", message.sender)
            if (len(self._votes.keys()) > (self._server._total_nodes - 1) / 2):
                leader = Leader()
                leader.set_server(self._server)
                print("Leader", leader._server._name, "got selected.")
                self._server._state = leader

                return leader, None
        return self, None

    def _start_election(self):
        # global lock
        self._server._currentTerm += 1
        locker.lock.acquire
        print("Server", self._server._name, " times out and then becomes a candidate!!")
        print("It starts the Election with term ", self._server._currentTerm,"!!! \n")
        locker.lock.release
        election = RequestVoteMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "lastLogIndex": self._server._lastLogIndex,
                "lastLogTerm": self._server._lastLogTerm,
            })

        self._server.send_message(election)
        self._last_vote = self._server._name
    def on_message(self, message):
            """This method is called when a message is received,
            and calls one of the other corrosponding methods
            that this state reacts to.

            """
            _type = message.type

            if (message.term > self._server._currentTerm):
                self._server._currentTerm = message.term
            # Is the messages.term < ours? If so we need to tell
            #   them this so they don't get left behind.
            # elif (message.term < self._server._currentTerm):
            #     self._send_response_message(message, yes=False)
            #     return self, None

            # if (_type == BaseMessage.AppendEntries):
            #     return self.on_append_entries(message)
            # elif (_type == BaseMessage.RequestVote):
            #     a = self.on_vote_request(message)
            #     return a
            if (_type == BaseMessage.RequestVoteResponse):
                a = self.on_vote_received(message)
                # print("RequestVoteResponse", a._server._name)
                return a
            # elif (_type == BaseMessage.Response):
            #     return self.on_response_received(message)

    def _nextTimeout(self):
        self._currentTime = time.time()
        # print("NEXT TIMEOUT")
        return self._currentTime + random.randrange(self._timeout,
                                                    2 * self._timeout)
