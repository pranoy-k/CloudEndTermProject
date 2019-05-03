# Raft

This is a implementation of a RAFT distributed consensus algorithm 


## What does it contain?
It consists of three directories
- Raft
- UnitTests
- BehavioralTests

## Dependencies

This implementation tries to stay as pure Python as possible to ensure that as few dependencies are required to run this outside of the code in this repo.
I am also striving to have it run on Python 3.7+ as well to make it as flexible as possible. 

The system is designed in two parts. There are a system of state classes that define the functionality required for the specific states that a node can
go through during the running of Raft, these include:

* Follower
* Candidate
* Leader

Each one has their roles defined in their class files. Along with these state classes there are defined messages that will be used to keep the 
message format well defined and abstracted from the wire format as much as possible. 

The final part is the communication layer. The current communication layer will use Gossiping using randomized subgroups at the moment, but it will
be written in such a way so as to be easy to implement and plug in a different communicationl layer at a later time.

References:
==========
* [In Search of an Understandable Consensus Algorithm](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [Raft Lecture](http://www.youtube.com/watch?v=YbZ3zDzDnrw)
* [Safty and Liveness](https://container-solutions.com/raft-explained-part-33-safety-liveness-guarantees-conclusion/)
* [Raft Simulation Cartoon](https://www.youtube.com/watch?v=xieqo3Tb5LQ)
* [Raft Consensus Algorithm](https://medium.com/@amangoeliitb/raft-consensus-algorithm-d93e7ee22b12)
* [Paxos and Raft](https://blockonomi.com/paxos-raft-consensus-protocols/)
* [Paxos & Raft Video](https://www.youtube.com/watch?v=Hm5LAxKxrD8)
* [Leader Election and Log Replication](https://www.youtube.com/watch?v=Bxm4FG4Nvs0)

