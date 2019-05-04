from __future__ import print_function
"""
Behavioral Test for Leader Election
"""

## Importing all the required libraries
import time
import threading

from threading import Thread

from Raft.servers.server import Server
from Raft.states.follower import Follower
from Raft.states.candidate import Candidate
from Raft.states.leader import Leader

lock = threading.Lock()

## Thread for constantly checking the messages for all servers
def checkMesages():
    i = 0
    while(True):
        time.sleep(0.0001)
        if i % 10000 == 0 and i <= 80000:
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

    while(True):

        ## Leader Sending Heartbeat
        if type(server._state) == Leader:
            if time.time()-timeoutTime >0.5:
                server._state._send_heart_beat()
                timeoutTime = time.time()+0.5

        ## For time out of follower to become candidate
        if type(server._state) == Follower:
            if time.time() >= server._state._timeoutTime:
                server._state = Candidate()
                server._state.set_server(server)


print("\n\nCreating four servers with names ranging from 0-3")

# Create Servers
followers = []
for name in range(4):

    ## Each server has a state out of (Candidate, Follower, Leader)
    ## Initially each candidate starts with follower state
    state = Follower()
    server = Server(name, state, [], [])

    ## Appending all neighbours to the current server
    for follower in followers:
        follower._neighbors.append(server)
        server._neighbors.append(follower)

    ## Attaching a thread to the server
    followers.append(server)
    thread = Thread(target=serverFunction, args=(name,))
    thread.start()
    print ("Started server with name ", name)
print("\nWait until first timer timesout")


thread = Thread(target=checkMesages, args=())
thread.start()
