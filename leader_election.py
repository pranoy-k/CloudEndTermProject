from __future__ import print_function

## Importing all the required libraries
import unittest
import time
import threading

from threading import Thread

# from Raft.boards.memory_board import MemoryBoard
from Raft.messages.append_entries import AppendEntriesMessage
from Raft.messages.request_vote import RequestVoteMessage
from Raft.servers.server import Server
from Raft.states.follower import Follower
from Raft.states.candidate import Candidate
from Raft.states.leader import Leader

lock = threading.Lock()

def checkMesages():
    i = 0
    while(True):
        time.sleep(0.0001)
        if i % 10000 == 0:
            lock.acquire()
            print('.')
            lock.release()
        for name in range(len(followers)):
            while(True):
                message = followers[name].get_message()

                if message == None:
                    break
                else:
                    followers[name]._state.on_message(message)
        i += 1

## Function associated with each server
def serverFunction(name):
    global followers
    server = followers[name]
    timeoutTime = time.time()+1
    # if isinstance(server._state) == Follower:
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

        ## Leader Sending Heartbeat
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
            if time.time() >= server._state._timeoutTime:
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

print("\n\nCreating four servers with names ranging from 0-3")
# print("\nThe current term is 0")

# Create Servers
followers = []
for name in range(4):
    state = Follower()
    server = Server(name, state, [], [])

    for follower in followers:
        follower._neighbors.append(server)
        server._neighbors.append(follower)

    followers.append(server)
    thread = Thread(target=serverFunction, args=(name,))
    thread.start()
    print ("Started server with name ", name)
print("\nWait until first timer timesout")


thread = Thread(target=checkMesages, args=())
thread.start()
