import unittest
import time

# from Raft.boards.memory_board import MemoryBoard
from Raft.messages.append_entries import AppendEntriesMessage
from Raft.messages.request_vote import RequestVoteMessage
from Raft.servers.server import Server
from Raft.states.follower import Follower
from Raft.states.candidate import Candidate
from Raft.states.leader import Leader


from threading import Thread

term = 0


def checkMesages():
    while(True):
        # print("x")
        time.sleep(0.0001)
        for name in range(len(followers)):
            while(True):
                message = followers[name].get_message()

                if message == None:
                    break
                else:
                    # print("Got message")
                    followers[name]._state.on_message(message)


def serverFunction(name):
    # print(name)
    global followers
    server = followers[name]
    timeoutTime = time.time()+1
    # if isinstance(server._state) == Follower:
    print("Started server with name ", name)
    # elif server._serverState == resumeState:
    #     print("Resumed server with name ", name)
    #     print(server._commitIndex)
    #     print(server._log)
    #     server._state = Follower()
    #     server._state.set_server(server)
    #     server._state.on_resume()
    #     server._serverState = followerState

    # count =0
    while(True):
        num = 0
        
        # print(name)
        if type(server._state) == Leader:
            # print("Server is now leader: ", server._name)
            if time.time()-timeoutTime >0.5:
                server._state._send_heart_beat()
                timeoutTime = time.time()+0.5

        # if type(server._state) == Candidate and time.time() >= server._state._timeoutTime:
        #     server._state = Follower()
        #     server._state.set_server(server)
        #     count += 1

        if type(server._state) == Follower:
            # print("time.time: ", time.time()/1000000)
            # print("server._state._timeoutTime: ",
            #       server._state._timeoutTime/1000000)
            if time.time() >= server._state._timeoutTime:
                # print("server._state._timeoutTime: ", server._state._timeoutTime/1000000)
                print(time.time(),server._state._timeoutTime)
                print("server ", server._name, "finds that the leader is dead")
                server._state = Candidate()
                server._state.set_server(server)
            # count += 1
        # if count == 50:
        #     break

        time.sleep(0.0001)
        # if server._serverState == deadState:
        #     print("Killed server with name", name)
        #     server._state = Follower()
        #     server._state.set_server(server)
        #     print(server._commitIndex)
        #     return
        #
        # if server._serverState == candidateState and type(server._state) != Candidate:
        #     timeout = randint(0.1e5, 5e5)
        #     timeout = 1.0*timeout/1e6
        #     time.sleep(timeout)
        #     if server._serverState == candidateState:
        #         server._state = Candidate()
        #         server._state.set_server(server)


# Create Servers
followers = []
for i in range(0, 2):
    # board = MemoryBoard()
    state = Follower()
    server = Server(i, state, [], [])

    for follower in followers:
        follower._neighbors.append(server)
        server._neighbors.append(follower)

    followers.append(server)
    thread = Thread(target=serverFunction, args=(i,))
    thread.start()

thread = Thread(target=checkMesages, args=())
thread.start()
