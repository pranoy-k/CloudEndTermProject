from __future__ import print_function
from collections import defaultdict

import time
import random
import threading

from Raft.messages.append_entries import AppendEntriesMessage
from Raft.messages.base import BaseMessage
from Raft.messages.response import ResponseMessage

class Leader(object):

    def __init__(self):
        self._nextIndexes = defaultdict(int)
        self._matchIndex = defaultdict(int)
        self._numofMessages = {}

    def set_server(self, server):
        self._server = server
        print("\nLeader", server._name, "got selected.\n")
        # self._send_heart_beat()
        for n in self._server._neighbors:
            self._nextIndexes[n._name] = self._server._lastLogIndex + 1
            self._matchIndex[n._name] = 0

    def on_response_received(self, message):
        # Was the last AppendEntries good?
        if (not message.data["response"]):
            # No, so lets back up the log for this node
            self._nextIndexes[message.sender] -= 1

            # Get the next log entry to send to the client.
            previousIndex = max(0, self._nextIndexes[message.sender] - 1)
            previous = self._server._log[previousIndex]
            current = self._server._log[self._nextIndexes[message.sender]]

            # Send the new log to the client and wait for it to respond.
            appendEntry = AppendEntriesMessage(
                self._server._name,
                message.sender,
                self._server._currentTerm,
                {
                    "leaderId": self._server._name,
                    "prevLogIndex": previousIndex,
                    "prevLogTerm": previous["term"],
                    "entries": [current],
                    "leaderCommit": self._server._commitIndex,
                })

            self._send_response_message(appendEntry)
        else:
            # The last append was good so increase their index.
            self._nextIndexes[message.sender] += 1

            # Are they caught up?
            if (self._nextIndexes[message.sender] > self._server._lastLogIndex):
                self._nextIndexes[message.sender] = self._server._lastLogIndex

        return self, None

    def _send_heart_beat(self):
        message = AppendEntriesMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "leaderId": self._server._name,
                "prevLogIndex": self._server._lastLogIndex,
                "prevLogTerm": self._server._lastLogTerm,
                "entries": [],
                "leaderCommit": self._server._commitIndex,
            })

        print("\nServer", self._server._name, "sending the Heartbeat")

        self._server.send_message(message)
    
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
        # elif (_type == BaseMessage.RequestVoteResponse):
        #     a = self.on_vote_received(message)
            # print("RequestVoteResponse", a._server._name)
            # return a
        if (_type == BaseMessage.Response):
            return self.on_response_received(message)

    # def _send_response_message(self, msg, yes=True):
    #     response = ResponseMessage(self._server._name, msg.sender, msg.term, {
    #         "response": yes,
    #         "currentTerm": self._server._currentTerm,
    #     })
    #     self._server.send_message_response(response)

    def _nextTimeout(self):
        self._currentTime = time.time()
        # print("NEXT TIMEOUT")
        return self._currentTime + random.randrange(self._timeout,
                                                    2 * self._timeout)
    
    def _send_response_message(self, msg, yes=True):
        response = ResponseMessage(self._server._name, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self._server._currentTerm,
        })
        self._server.send_message_response(response)
    
    def run_client_command(self, message):
        print ("running client command")
        term = self._server._currentTerm
        value = message._data["command"]
        log = {"term": term, "value": value}
        self._server._lastLogIndex = len(self._server._log) - 1
        self._server._lastLogTerm = term
        if self._server._lastLogIndex > -1:
            self._server._lastLogTerm = self._server._log[self._server._lastLogIndex]["term"]
        self._server._log.append(log)
        for n in self._server._neighbors:
            self._numofMessages[n._name] = 1

        message = Message(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "leaderId": self._server._name,
                "prevLogIndex": self._server._lastLogIndex,
                "prevLogTerm": self._server._lastLogTerm,
                "entries": [log],
                "leaderCommit": self._server._commitIndex,
            }, Message.AppendEntries)
        self._server.send_message(message)
        return self, None
