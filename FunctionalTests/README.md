

## What does this folder contain?
The folder contains 2 files:
- leader_election.py 
  - This file contains the code for implementing leader election
- log_replication.py
  - This file contains the code for implementing log replication


## Leader Election
In order to maintain authority as a Leader of the cluster, the Leader node sends heartbeat to express dominion to other Follower nodes. A leader election takes place when a Follower node times out while waiting for a heartbeat from the Leader node. At this point of time, the timed out node changes it state to Candidate state, votes for itself and issues RequestVotes RPC to establish majority and attempt to become the Leader. 

## Log Replication
Client makes write requests. Each request made by the client is stored in the Logs of the Leader. This log is then replicated to other nodes(Followers).The Leader node fires AppendEntries RPCs to all other servers(Followers) to sync/match up their logs with the current Leader.The Leader keeps sending the RPCs until all the Followers safely replicate the new entry in their logs.

