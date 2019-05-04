import unittest

from Raft.servers.server import Server
from Raft.states.follower import Follower
from Raft.states.candidate import Candidate
from Raft.states.leader import Leader

class TestCandidateServer(unittest.TestCase):
    ### Doing the initial setup for tests ##########

    def setUp(self):
        state = Follower()
        self.oserver = Server(0, state, [], [])

        state = Candidate()
        self.server = Server(1, state, [], [self.oserver])

        self.oserver._neighbors.append(self.server)

# unit test to check if communication between candidate and follower
    def test_candidate_can_communicate_with_the_follower(self):

        self.assertEquals(1, len(self.oserver._board))

        self.oserver.on_message(self.oserver.get_message())

        self.assertEquals(1, len(self.server._board))
        self.assertEquals(True, self.server.get_message().data["response"])


### Candidate starting the election and gets vote from majority ##############
    def test_candidate_server_wins_election(self):
        state = Follower()
        server0 = Server(0, state, [], [])

        state = Follower()
        server3 = Server(3, state, [], [])

        state = Follower()
        oserver = Server(1, state, [],  [])

        state = Candidate()
        server = Server(2, state, [], [oserver, server0, server3])

        server0._neighbors.append(server)
        oserver._neighbors.append(server)
        server3._neighbors.append(server)

        oserver.on_message(oserver.get_message())
        server0.on_message(server0.get_message())
        server3.on_message(server3.get_message())

        server._total_nodes = 4

        server.on_message(server.get_message())
        server.on_message(server.get_message())

        self.assertEquals(type(server._state), Leader)

    
if __name__ == '__main__':
    unittest.main()
