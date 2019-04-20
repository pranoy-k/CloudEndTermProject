from Raft.states.state import State

from Raft.messages.request_vote import RequestVoteResponseMessage


class Voter(State):

    def __init__(self, timeout=5):
        self._last_vote = None
        self._timeout = timeout

    def on_vote_request(self, message):
        self._timeoutTime = self._nextTimeout()
        print("TIME OUT: ", self._timeoutTime/1000000)
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
