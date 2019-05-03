# Raft

This is a implementation of a RAFT distributed consensus algorithm 


## What does it contain?
It consists of three directories
- Raft
  - messages
  - servers
  - states
- UnitTests
  - test_CandidateServer.py
  - test_LeaderServer.py
  - test_FollowerServer.py
- BehavioralTests
  - LeaderElection.py
  - LogReplication.py

## Dependencies

This implementation is completed in Python.

- nose==1.3.0 
  - nose extends the test loading and running features of unittest, making it easier to write, find and run tests.
- pyzmq==14.3.1 
  - This package contains Python bindings for ØMQ. ØMQ is a lightweight and fast messaging implementation.
- wsgiref==0.1.2 
  - A reference implementation of the WSGI specification that can be used to add WSGI support to a web server or framework.


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

