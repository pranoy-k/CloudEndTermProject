from __future__ import print_function

"""
Evaluation for measuring the time for leader election
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
leader_doesnot_exist = True
election_time = 0


def checkMesages():
    i = 0
    while (True):
        if leader_doesnot_exist:
            time.sleep(0.0001)
            if i % 10000 == 0 and i <= 80000:
                lock.acquire()
                print('.')
                lock.release()
            for name in range(len(followers)):
                while (True):
                    message = followers[name].get_message()

                    if message == None:
                        break
                    else:
                        followers[name]._state.on_message(message)
            i += 1
        else:
            break


## Function associated with each server
def serverFunction(name):
    global leader_doesnot_exist
    global followers
    global election_time

    timestart = 0
    timeend = 0
    server = followers[name]
    # timeoutTime = time.time()+1

    while leader_doesnot_exist:
        ## For time out of follower to become candidate
        if type(server._state) == Follower:
            # if leader_doesnot_exist == True:
            #     break
            if time.time() >= server._state._timeoutTime:
                server._state = Candidate()
                server._state.set_server(server)
                timestart = time.time()
        ## Leader Sending Heartbeat
        if type(server._state) == Leader:
            leader_doesnot_exist = False
            timeend = time.time()
            election_time = timeend - timestart
            time.sleep(1)
            print("The time for leader to get elected is", str(election_time*1000)[:7], "seconds")
            break
            # if time.time()-timeoutTime >0.5:
            #     server._state._send_heart_beat()
            #     timeoutTime = time.time()+0.5

    # print(name,"has been killed")



## Running experiment with different number of servers each time
for exp_num in range(2, 6):
    print('.'*100)
    print("\nRunning experiment with", exp_num, "servers\n.\n.\n.\n")
    followers = []
    thread = []
    leader_doesnot_exist = True
    for name in range(exp_num):

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
        thread.append(Thread(target=serverFunction, args=(name,)))
        thread[name].start()
        print ("Started server with name:", name)
    print("\nWait until first timer timesout")

    thread.append(Thread(target=checkMesages, args=()))
    thread[name + 1].start()
    for i in range(0, name + 2):
        thread[i].join()