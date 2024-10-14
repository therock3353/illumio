import abc
from app.common.exceptions import ParserNotSupportedException
'''
    Abstract Base Class for the Parsers
'''
class FlowLogParser(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self, log):
        pass

'''
    Class implementing parsing of version 2 of logs
'''
class FlowLogV2Parser(FlowLogParser):
    def __init__(self):
        pass

    def parse(self, log):
        destPort = log[6]
        protocol = log[7]
        return destPort, protocol


class FlowLogV3Parser(FlowLogParser):
    def __init__(self):
        pass

    #Not implemented for the assignment
    def parse(self, log):
        pass

'''
    Factory method returns correct Parser based on log version
'''
class FlowLogParserFactory(object):
    parser_mappings = {
        '2': FlowLogV2Parser,
        '3': FlowLogV3Parser
    }

    @staticmethod
    def getParser(version):
        if version not in FlowLogParserFactory.parser_mappings.keys():
            raise ParserNotSupportedException("Parser with version {} not supported".format(version))
        klass = FlowLogParserFactory.parser_mappings.get(version)
        return klass() #return instance of the FlowLogParser class based on version