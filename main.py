from app.lookup.lookup import LookupTableMgr
from app.flowlog.flow_log_mgr import FlowLogProcessorMgr
from app.out.output_generator import OutputGenerator
from app.common.const import PORT_PROTO_HEADERS, TAG_COUNT_HEADERS, TAG_COUNTS_SECTION_TITLE, PORT_PROTO_SECTION_TITLE

class FlowLogOrchestrator(object):
    def __init__(self):
        self.lookupMgr = LookupTableMgr()
        self.flowLogMgr = FlowLogProcessorMgr()
        self.out = OutputGenerator()

    def initialize(self):
        self.lookupMgr.loadLookupTable()
        self.flowLogMgr.setLookupTable(self.lookupMgr.lookup_map)

    def generate_output(self):
        tag_counts = []
        for tag, count in self.flowLogMgr.tag_count.items():
            tag_count = []
            tag_count.append(tag)
            tag_count.append(count)
            tag_counts.append(tag_count)
        self.out.addSection(TAG_COUNTS_SECTION_TITLE, TAG_COUNT_HEADERS, tag_counts)
        port_protocols = []
        for port_proto, count in self.flowLogMgr.uniq_port_proto_count.items():
            port_protocol = []
            port_protocol.append(port_proto.split("+")[0])
            port_protocol.append(port_proto.split("+")[1])
            port_protocol.append(count)
            port_protocols.append(port_protocol)
        self.out.addSection(PORT_PROTO_SECTION_TITLE, PORT_PROTO_HEADERS, port_protocols)
        self.out.writeFile()

    def start(self):
        self.initialize()
        self.flowLogMgr.processLogFile()
        self.generate_output()

if __name__ == '__main__':
    flowLogParsingOrchestrator = FlowLogOrchestrator()
    flowLogParsingOrchestrator.start()