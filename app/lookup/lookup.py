import csv
from app.common.exceptions import LookupTableParsingException
from app.common.const import LOOKUP_FILE, PORT_PROTOCOL_DELIMITER

class LookupTableMgr(object):
    def __init__(self):
        self.lookup_map = {}
        self.file = LOOKUP_FILE

    def loadLookupTable(self):
        with open(self.file) as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                try:
                    if i == 0:
                        if str(line[0]).lower() == "dstport":
                            continue
                    if len(line) < 2:
                        raise LookupTableParsingException("Error in parsing lookup table line {} with data {}".format(i, line))
                    tag = line[2]
                    if " " in tag: #If there is a space then take the first part as TAG
                        tag = tag.split(" ")[0]

                    key = str(line[0]) + PORT_PROTOCOL_DELIMITER + str(line[1]).lower()
                    self.lookup_map[key] = str(tag).lower()
                except Exception as e:
                    print(e)