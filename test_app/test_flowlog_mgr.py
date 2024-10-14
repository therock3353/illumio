import unittest
from app.flowlog.flow_log_mgr import FlowLogProcessorMgr

class FlowLogProcessorMgrTestCase(unittest.TestCase):
    def test_handleUnknown(self):
        mgr = FlowLogProcessorMgr()
        mgr.lookup_table = {
            '80+http': 'tag_1'
        }
        desired_result = {'Unknown': 1}
        mgr.handleUnknown()
        self.assertDictEqual(mgr.tag_count, desired_result)

    def test_handlePortProtocol01(self):
        mgr = FlowLogProcessorMgr()
        mgr.lookup_table = {
            '80+http': 'tag_1',
            '25+tcp': 'tag_2'
        }
        mgr.handlePortProtocol(port='25', protocol='tcp')
        self.assertDictEqual(mgr.tag_count, {'tag_2': 1})
        self.assertDictEqual(mgr.uniq_port_proto_count, {'25+tcp': 1})

    def test_handlePortProtocol02(self):
        mgr = FlowLogProcessorMgr()
        mgr.lookup_table = {
            '80+http': 'tag_1',
            '25+tcp': 'tag_2'
        }
        mgr.handlePortProtocol(port='443', protocol='tcp')
        self.assertDictEqual(mgr.tag_count, {'Unknown': 1})
        self.assertDictEqual(mgr.uniq_port_proto_count, {'443+tcp': 1})

    def test_handleICMP01(self):
        mgr = FlowLogProcessorMgr()
        mgr.lookup_table = {
            '0+icmp': 'tag_1',
            '25+tcp': 'tag_2'
        }
        mgr.handlePortProtocol(port='0', protocol='icmp')
        self.assertDictEqual(mgr.tag_count, {'tag_1': 1})
        self.assertDictEqual(mgr.uniq_port_proto_count, {'0+icmp': 1})

    def test_handleICMP02(self):
        mgr = FlowLogProcessorMgr()
        mgr.lookup_table = {
            '80+http': 'tag_1',
            '25+tcp': 'tag_2'
        }
        mgr.handlePortProtocol(port='0', protocol='icmp')
        self.assertDictEqual(mgr.tag_count, {'Unknown': 1})
        self.assertDictEqual(mgr.uniq_port_proto_count, {'0+icmp': 1})

if __name__ == '__main__':
    unittest.main()