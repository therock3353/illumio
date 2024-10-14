import csv
from app.common.const import OUTPUT_FILE

class OutputGenerator(object):
    def __init__(self):
        self.data = []

    def addSection(self, title, headers, data):
        self.data.append([title])
        self.data.append(headers)
        self.data.append(data)
        self.data.append([])

    def writeFile(self):
        with open(OUTPUT_FILE, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                for line in self.data:
                    if line and isinstance(line[0], list):
                        for row in line:
                            print(row)
                            writer.writerow(row)
                    else:
                        print(line)
                        writer.writerow(line)