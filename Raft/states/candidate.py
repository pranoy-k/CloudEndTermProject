from Raft.states.voter import Voter
from Raft.states.leader import Leader
from Raft.messages.request_vote import RequestVoteMessage


class Candidate(Voter):

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
                # self._server._state = Leader()
                leader.set_server(self._server)
                print(leader._server._name, "Leader got selected.")
                return leader, None
        return self, None

    def _start_election(self):
        self._server._currentTerm += 1
        print("Start Election!!!!")
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
