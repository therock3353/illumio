import csv
from app.flowlog.flow_log_parser import FlowLogParserFactory
from app.common.const import FLOWLOG_FILE, PROTOCOL_NUM_TO_INT_MAP, PORT_PROTOCOL_DELIMITER, UNKNOWN_KEY

class FlowLogProcessorMgr(object):
    def __init__(self):
        self.file = FLOWLOG_FILE
        self.lookup_table = {}
        self.uniq_port_proto_count = {}
        self.tag_count = {}

    def setLookupTable(self, lookupTable):
        self.lookup_table = lookupTable

    def updateTagCount(self, key):
        tag = self.lookup_table.get(key, None)
        if tag:
            self.tag_count[tag] = 1 + self.tag_count.get(tag, 0)
        else:
            self.tag_count[UNKNOWN_KEY] = 1 + self.tag_count.get(UNKNOWN_KEY, 0)

    def updatePortProtoCount(self, key):
        self.uniq_port_proto_count[key] = 1 + self.uniq_port_proto_count.get(key, 0)

    def handleICMP(self, protocol):
        port = "0" #in case of icmp, the key will be '0+icmp'. We can have different key as well,
        #for uniformity keeping it as 0+icmp.
        key = str(port) + PORT_PROTOCOL_DELIMITER + str(protocol)
        self.updatePortProtoCount(key)
        self.updateTagCount(key)

    def handlePortProtocol(self, port, protocol):
        key = str(port) + PORT_PROTOCOL_DELIMITER + str(protocol)
        self.updatePortProtoCount(key)
        self.updateTagCount(key)

    def handleUnknown(self):
        key = UNKNOWN_KEY
        self.updateTagCount(key)

    '''
        handle different combinations of port + protocol combinations here
    '''
    def doComputation(self, port, protocol):
        protocol = PROTOCOL_NUM_TO_INT_MAP.get(str(protocol), None)  # convert number to string ie 1->ICMP, 6->TCP etc
        #tcp 25, http 80, udp 21 default use case where both port & protocol are present in the log
        if port and protocol:
            self.handlePortProtocol(port, protocol)
        #if ICMP then port = 0, handle this case.
        elif protocol:
            #It is possible that only protocol is present and the config applies to all ports, but that case
            #is not handled yet @TODO later
            self.handleICMP(protocol)
        else:
            self.handleUnknown()

    def processSigleLog(self, line):
        version = line[0]
        try:
            parser = FlowLogParserFactory.getParser(str(version))
            port, protocol = parser.parse(line)
            self.doComputation(port, protocol)
        except Exception as e:
            print(e)

    def processLogFile(self):
        with open(self.file) as f:
            reader = csv.reader(f, delimiter=' ')
            for i, line in enumerate(reader):
                self.processSigleLog(line)