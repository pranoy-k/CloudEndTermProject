import unittest

from Raft.messages.append_entries import AppendEntriesMessage
from Raft.messages.request_vote import RequestVoteMessage
from Raft.servers.server import Server
from Raft.states.follower import Follower


class TestFollowerServer(unittest.TestCase):
    ### Doing the initial setup for tests ##########
    def setUp(self):
        state = Follower()
        self.oserver = Server(0, state, [], [])

        state = Follower()
        self.server = Server(1, state, [], [self.oserver])

    ## Unit test to send heartbeart message to neighbours ################
    def test_follower_server_on_message(self):
        input_message = AppendEntriesMessage(0, 1, 10, {})
        self.server.on_message(input_message)
        self.assertEquals(10, self.server._currentTerm)

    ## Unit test to reject message with lesser term ###########
    def test_follower_server_on_receive_message_with_lesser_term(self):
        input_message = AppendEntriesMessage(0, 1, -1, {})
        self.server.on_message(input_message)
        self.assertEquals(False, self.oserver.get_message().data["response"])

    #### Unit test to append log to an initial empty log##################
    def test_follower_server_on_receiving_message_to_empty_logs(self):
        msg = AppendEntriesMessage(0, 1, 2, {
            "prevLogIndex": 0,
            "prevLogTerm": 100,
            "leaderCommit": 1,
            "entries": [{"term": 1, "value": 100}]})

        self.server.on_message(msg)
        self.assertEquals({"term": 1, "value": 100}, self.server._log[0])

    ## Unit test to test if follower is receiving message from candidate ######
    def test_follower_server_on_receive_request_for_voting(self):
        msg = RequestVoteMessage(0, 1, 2, {"lastLogIndex": 0, "lastLogTerm": 0, "entries": []})
        self.server.on_message(msg)
        self.assertEquals(0, self.server._state._last_vote)
        self.assertEquals(True, self.oserver.get_message().data["response"])

if __name__ == '__main__':
    unittest.main()