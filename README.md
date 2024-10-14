# illumio
Explanation:
====================
We are given 2 files. One file contains flow logs, another file contains a mapping of dstport, protocol, tag.
We need to calculate:
    1. Count of matches for each tag.
    2. Count of matches for each port/protocol.

Here is the general approach we will take.
1. read lookup file line by line and create a HashMap/dict
    with key being port+lower_case(protocol) (Since matches should be case insensitive)
    There are only 10k such entries so no need to worry about data not fitting in memory.
2. read flow-log file line by line.
    for each_line in flow-log
        here we need to parse the log based on version.
        for version 2 there will be different parser as compared to version 3 (for simplicity, I have
        only implemented version-2 parser)
        port = parsePortFromLog(each_log)
        protocol = parseProtocolFromLog(each_log)
        here we have 3 cases:
            1. both port+protocol is present:
                if port+protocol combo present in reference lookup table, update count
                else update unknown/untagged count
            2.


Assumptions:
================
    - The lookup table contains DestPort & Protocol combination hence assuming that we want to look for the same DestPort & Protocol
      in flow-log. Flow log also has Source Port attribute but it is ignored for this exercise.
    - The lookup file has all unique dstport, protocol combinations. i.e no two rows with same dstPort, Protocol combinations.
      If they are the first one is only taken into effect.
    - Flow-log version 2 is only supported. later versions (3,5 etc)are not supported, as log formats hence parsing
      logic changes based on version
    - IANA has well published list of protocols to protocol number mappings (https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers)
        For programming purpose, taking only the most common once
        1- icmp
        6- tcp
        17- udp
    - It is possible that the security logs will be in format destport 0 protocol tcp (Allow|Reject) all TCP/UDP connections.
      For simplicity, ignoring this use-case.
    - It was not clear if the 'Count of matches for each port/protocol combination' was required for all
      port protocol combinations in flow.log or for only the combinations present in the lookup file.
      Here printing output for all the port+protocol combinations in flow.log file.


How to run program & check output (./app/data/output.csv)
============================================================
Tested with Python 3.9 env.
No external module required (only default csv parser used)
to run the program, just type:
    python main.py

note: Tested with python3.9, on local-machine the python binary
should be part of PATH env variable.

The data files are in ./app/data/ directory and output file 'output.csv' is also
generated in ./app/data/ directory.



Future Improvements:
====================
- improved CLI utility with ability to provide more CLI options
- support for v3, v5 and other version of logs
