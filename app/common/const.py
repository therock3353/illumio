LOOKUP_FILE = "./app/data/lookup.csv"
FLOWLOG_FILE = "./app/data/flow.log"
OUTPUT_FILE = "./app/data/output.csv"
TAG_COUNTS_SECTION_TITLE = "TAG Count:"
TAG_COUNT_HEADERS = ["TAG", "Count"]
PORT_PROTO_SECTION_TITLE = "Port Protocol Uniq Count:"
PORT_PROTO_HEADERS = ["PORT", "PROTOCOL", "Count"]

PORT_PROTOCOL_DELIMITER = "+"
UNKNOWN_KEY = "Unknown"
#as per IANA, 1-ICMP, 17-UDP etc
PROTOCOL_NUM_TO_INT_MAP = {
    '1': 'icmp',
    '6': 'tcp',
    '17': 'udp'
}
