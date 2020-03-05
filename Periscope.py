# python character encoding: utf-8
from PeriscopeKey import PeriscopeKey
import requests
import random
import json

class PeriscopeQuery():
    credentials = PeriscopeKey()
    api_url = "https://periscope.caida.org/api/v2"
    measurement = dict()
    queryID = None
    queryStatus = None
    queryResult = None

    def __init__(self, id):
        self.queryID = id
        self.check_status()

    def gen_headers(self, data):
        headers = {
            'Content-type': 'application/json; charset=utf-8',
            'X-Public': self.credentials.public_key,
            'X-Hash': self.credentials.gen_signature(data)
        }
        return headers

    def get_available_lg_nodes(self, number=None):
        hosts = list()
        response = requests.get(self.api_url + "/host/list?command=traceroute")
        available_hosts = response.json()

        if number is None:
            for host in available_hosts:
                hosts.append({"asn": host["asn"], "router": host["router"]})

            return hosts

        else:
            selected_hosts = random.sample(available_hosts, number)
            for host in selected_hosts:
                hosts.append({"asn": host["asn"], "router": host["router"]})

            return hosts

    def traceroute(self, destination, hosts, verbose=False):
        """submits traceroute query from each host to destination"""

        self.measurement["argument"] = destination
        self.measurement["command"] = "traceroute"
        self.measurement["name"] = "test"
        self.measurement["hosts"] = hosts

        data = json.dumps(self.measurement)
        headers = self.gen_headers(data)

        response = requests.post(self.api_url + "/measurement", data=data, headers=headers)
        decoded_response = response.json()

        if verbose:
            print("HTTP response status: " + str(response.status_code))
            print("HTTP response text:  " + str(response.text))
            print("Measurement ID: " + str(decoded_response["id"]))

        if response.status_code == 201:  ## HTTP 201 = POST request has been successfully created on server
            decoded_response = response.json()
            self.queryID = decoded_response["id"]
            self.check_status()
            return decoded_response["id"]

        else:
            print("Response status code error: ", response.status_code)
            return None

    def check_status(self, verbose=False):
        """Checks status of Periscope query"""

        if self.queryID == None:
            if verbose:
                print("No query was run...")
            return None

        elif self.queryStatus != None and self.queryStatus['pending'] == 0:
            if verbose:
                print(self.queryStatus)

            if self.queryResult == None:
                self.get_result()

            return self.queryStatus

        else:
            requestURL = self.api_url + "/measurement/" + str(self.queryID)
            response = requests.get(requestURL)

            decoded_response = response.json()

            if 'errors' in decoded_response.keys():
                print("Invalid ID...")
                return None

            self.queryStatus = response.json()['status']

            if verbose:
                print(self.queryStatus)

            return self.queryStatus

    def get_result(self):
        """pulls result from Periscope"""

        if self.queryStatus == None or self.queryStatus['pending'] != 0:
            print("Query is not complete...")
            return None

        requestURL = self.api_url + "/measurement/" + str(self.queryID) + "/result?format=raw"
        response = requests.get(requestURL)
        self.queryResult = response.json()

        return self.queryResult

    def parse_result(self, result):
        """returns nested dictionary of results"""

        out = dict()
        for index, item in enumerate(result):
            if item['status'] == 'completed':
                lines = item['result'].splitlines()

                trace = dict()
                for line in lines:
                    words = line.split()

                    if len(words) != 0:
                        hop = words.pop(0)
                        if hop.isdigit():
                            trace[hop] = dict()

                            if words[0] == '*':
                                trace[hop]['ip'] = '*'
                                trace[hop]['name'] = '*'
                                trace[hop]['time'] = ['*', '*', '*']

                            else:
                                trace[hop]['ip'] = words[1].strip('()')
                                trace[hop]['name'] = words[0]
                                trace[hop]['time'] = [words[2], words[4], words[6]]

                out[index] = trace

        return out