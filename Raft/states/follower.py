from __future__ import print_function
import time
import random
import threading

from Raft.messages.request_vote import RequestVoteResponseMessage
from Raft.messages.base import BaseMessage
from Raft.messages.response import ResponseMessage



class Follower(object):

    def __init__(self,timeout = 8):  # time is in sec NOT millisec. 500 origin
        self._last_vote = None
        self._timeout = timeout
        # self._timeout = timeout
        self._timeoutTime = self._nextTimeout()
        
    def set_server(self, server):
        self._server = server

    def on_append_entries(self, message):
        self._timeoutTime = self._nextTimeout()

        if (message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if (message.data != {}):
            # print("##########################")
            log = self._server._log
            data = message.data

            # Check if the leader is too far ahead in the log.
            if (data["leaderCommit"] != self._server._commitIndex):
                # If the leader is too far ahead then we
                #   use the length of the log - 1
                self._server._commitIndex = min(data["leaderCommit"],
                                                len(log) - 1)

            # Can't possibly be up-to-date with the log
            # If the log is smaller than the preLogIndex
            if (len(log) < data["prevLogIndex"]):
                self._send_response_message(message, yes=False)
                return self, None

            # We need to hold the induction proof of the algorithm here.
            #   So, we make sure that the prevLogIndex term is always
            #   equal to the server.
            if (len(log) > 0 and
                    log[data["prevLogIndex"]]["term"] != data["prevLogTerm"]):

                # There is a conflict we need to resync so delete everything
                #   from this prevLogIndex and forward and send a failure
                #   to the server.
                log = log[:data["prevLogIndex"]]
                self._send_response_message(message, yes=False)
                self._server._log = log
                self._server._lastLogIndex = data["prevLogIndex"]
                self._server._lastLogTerm = data["prevLogTerm"]
                return self, None
            # The induction proof held so lets check if the commitIndex
            #   value is the same as the one on the leader
            else:
                # Make sure that leaderCommit is > 0 and that the
                #   data is different here
                if (len(log) > 0 and
                        data["leaderCommit"] > 0 and
                        log[data["leaderCommit"]]["term"] != message.term):
                    # Data was found to be different so we fix that
                    #   by taking the current log and slicing it to the
                    #   leaderCommit + 1 range then setting the last
                    #   value to the commitValue
                    log = log[:self._server._commitIndex]
                    for e in data["entries"]:
                        log.append(e)
                        self._server._commitIndex += 1

                    self._send_response_message(message)
                    self._server._lastLogIndex = len(log) - 1
                    self._server._lastLogTerm = log[-1]["term"]
                    self._commitIndex = len(log) - 1
                    self._server._log = log
                else:
                    # The commit index is not out of the range of the log
                    #   so we can just append it to the log now.
                    #   commitIndex = len(log)
                    #   Is this a heartbeat?
                    if (len(data["entries"]) > 0):
                        for e in data["entries"]:
                            log.append(e)
                            self._server._commitIndex += 1

                        self._server._lastLogIndex = len(log) - 1
                        self._server._lastLogTerm = log[-1]["term"]
                        self._commitIndex = len(log) - 1
                        self._server._log = log
                        self._send_response_message(message)

            self._send_response_message(message)
            return self, None
        else:
            return self, None

    def on_message(self, message):
        """This method is called when a message is received,
        and calls one of the other corrosponding methods
        that this state reacts to.

        """
        _type = message.type

        if _type == 0:
            print("Server", self._server._name,"received", "AppendEntries")
        elif _type == 1:
            print("Server", self._server._name,"received", "RequestVote")
        elif _type == 2:
            print("Server", self._server._name,"received", "RequestVoteResponse")
        elif _type == 3:
            print("Server", self._server._name,"received", "Response")

        if (message.term > self._server._currentTerm):
            self._server._currentTerm = message.term
        # Is the messages.term < ours? If so we need to tell
        #   them this so they don't get left behind.
        elif (message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if (_type == BaseMessage.AppendEntries):
            return self.on_append_entries(message)
        elif (_type == BaseMessage.RequestVote):
            a = self.on_vote_request(message)
            return a
        # elif (_type == BaseMessage.RequestVoteResponse):
        #     a = self.on_vote_received(message)
        #     # print("RequestVoteResponse", a._server._name)
        #     return a
        # elif (_type == BaseMessage.Response):
        #     return self.on_response_received(message)

    def _nextTimeout(self):
        self._currentTime = time.time()
        # print("NEXT TIMEOUT")
        return self._currentTime + random.randrange(self._timeout, 2 * self._timeout)

    def _send_response_message(self, msg, yes=True):
        response = ResponseMessage(self._server._name, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self._server._currentTerm,
        })
        self._server.send_message_response(response)

    def on_vote_request(self, message):
        self._timeoutTime = self._nextTimeout()
        # print("TIME OUT: ", self._timeoutTime/1000000)
        if (self._last_vote is None and
                message.data["lastLogIndex"] >= self._server._lastLogIndex):
            self._last_vote = message.sender
            self._send_vote_response_message(message)
        else:
            self._send_vote_response_message(message, yes=False)

        return self, None

    def _send_vote_response_message(self, msg, yes=True):
        voteResponse = RequestVoteResponseMessage(
            self._server._name,
            msg.sender,
            msg.term,
            {"response": yes})
        self._server.send_message_response(voteResponse)

