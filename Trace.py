import re


class Trace:
    def __init__(self, dataDict):
        # self.caida_id = dataDict['id']
        self.city = dataDict['city']
        self.country = dataDict['country']
        self.starttime = dataDict['starttime']
        self.endtime = dataDict['endtime']
        self.router = dataDict['router']
        self.asn = dataDict['asn']

        if dataDict['status'] == 'completed':
            self.completed = True
            self.result = self.convert_raw_trace(dataDict['result'])
            self.error = None

        else:
            self.completed = False
            self.error = dataDict['error']
            self.result = None

    def convert_raw_trace(self, rawDict):
        """Converts trace as whitespace delimited string to Python dict"""
        lines = rawDict.splitlines()
        trace = {}

        for line in lines:
            words = line.split()

            if len(words) != 0:
                hop = words.pop(0)
                if hop.isdigit():
                    trace[hop] = {}

                    if words[0] == '*':
                        trace[hop]['ip'] = '*'
                        trace[hop]['name'] = '*'
                        trace[hop]['time'] = ['*', '*', '*']

                    else:
                        trace[hop]['ip'] = words[1].strip('()')
                        trace[hop]['name'] = words[0]

                        try:
                            trace[hop]['time'] = [words[2], words[4], words[6]]

                        except IndexError:
                            trace[hop]['time'] = None

                else:
                    pattern = re.compile("([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})")
                    ip = pattern.search(line)
                    if ip:
                        self.destination = ip.group(0)
                    else:
                        self.destination = None

        return trace

    def items(self):
        if self.completed:
            for key, item in self.result.items():
                yield key, item

        else:
            return None

    def pprint(self):

        print("### Traceroute from server", self.caida_id, "in", self.city, ",", self.country, ":")


        if self.completed:
            for key, item in self.result.items():
                print(key, "\t", item['ip'], "\t", item['name'], "\t", item['time'])

        else:
            print(self.error)