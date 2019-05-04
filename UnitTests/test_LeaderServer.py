import unittest

from Raft.states.leader import Leader
from Raft.states.follower import Follower
from Raft.servers.server import Server
from Raft.messages.append_entries import AppendEntriesMessage

class TestLeaderServer(unittest.TestCase):
    ### Doing the initial setup for tests ##########

    def setUp(self):
        followers = []
        for i in range(1, 4):
            state = Follower()
            followers.append(Server(i, state, [], []))

        state = Leader()

        self.leader = Server(0, state, [], followers)

        for i in followers:
            i._neighbors.append(self.leader)

    ##### Unit test to send heart beat to all the neighbours ##############
    def test_leader_server_sends_heartbeat_to_all_neighbors(self):

        self._perform_hearbeat()
        self.assertEquals({1: 0, 2: 0, 3: 0}, self.leader._state._nextIndexes)

    ##### Unit test to ensure logs are getting committed to the neighbours ###### 
    def test_leader_server_sends_messages_to_append_neighbours_logs(self):

        self._perform_hearbeat()

        msg = AppendEntriesMessage(0, None, 1, {
            "prevLogIndex": 0,
            "prevLogTerm": 0,
            "leaderCommit": 1,
            "entries": [{"term": 1, "value": 800}]})

        self.leader.send_message(msg)

        for i in self.leader._neighbors:
            i.on_message(i.get_message())

        for i in self.leader._neighbors:
            self.assertEquals([{"term": 1, "value": 800}], i._log)



    ####### Function to simulate performing heartbeat for the unit test ############    
    def _perform_hearbeat(self):
        self.leader._state._send_heart_beat()
        for i in self.leader._neighbors:
            i.on_message(i.get_message())

        for i in self.leader._board:
            self.leader.on_message(i)

if __name__ == '__main__':
    unittest.main()
