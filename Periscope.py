# python character encoding: utf-8
from PeriscopeKey import PeriscopeKey
import requests
import random
import json
from xml.etree import ElementTree as ET

class PeriscopeQuery():
    credentials = PeriscopeKey()
    api_url = "https://periscope.caida.org/api/v2"
    measurement = dict()
    queryID = None
    queryStatus = None
    queryResult = None

    def __init__(self, id=None):
        self.queryID = id

        if self.queryID != None:
            self.check_status()

    def gen_headers(self, data):
        headers = {
            'Content-type': 'application/json; charset=utf-8',
            'X-Public': self.credentials.public_key,
            'X-Hash': self.credentials.gen_signature(data)
        }
        return headers

    def get_lg_nodes(self, command="traceroute", asn=None, router=None, city=None, country=None, number=None, verbose=False):
        """lists available looking glass servers. Number arg sets number of randomly selected hosts"""
        hosts = []
        requestURL = self.api_url + "/host/list?command=" + command

        if asn != None:
            requestURL += "&asn=" + str(asn)

        if router != None:
            requestURL += "&router=" + router

        if city != None:
            requestURL += "&city=" + city.replace(" ","+")

        if country != None:
            requestURL += "&country=" + country

        response = requests.get(requestURL)
        available_hosts = response.json()

        try:
            if number is None:
                for host in available_hosts:
                    try:
                        hosts.append({"asn": host["asn"], "router": host["router"], "country": host["country"]})

                    except KeyError as err:
                        hosts.append({"asn": host["asn"], "router": host["router"], "country": None})

                if verbose:
                    for host in available_hosts:
                        print(host)

                return hosts

            else:
                selected_hosts = random.sample(available_hosts, number)
                for host in selected_hosts:
                    hosts.append({"asn": host["asn"], "router": host["router"], "country": host["country"]})

                if verbose:
                    for host in available_hosts:
                        print(host)

                return hosts

        except TypeError:
            if 'errors' in available_hosts.keys(): ## checks that query arg is valid
                print("Invalid ID...")
                return None

    def get_lg_countries(self, verbose=False):
        hosts = self.get_lg_nodes()
        countries = set()

        if verbose:
            tree = ET.parse("XML Country List")
            root = tree.getroot()

        for host in hosts:
            if host['country'] != None:
                countries.add(host['country'])

        if verbose:
            for country in countries:
                try:
                    e = root.findall("./country[@code='%s']" % country.lower())
                    print(country, ":", e[0].text)

                except IndexError as err:
                    pass

        return countries

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

    def get_result(self, verbose=False):
        """pulls result from Periscope"""

        if self.queryStatus == None or self.queryStatus['pending'] != 0:
            print("Query is not complete...")
            return None

        requestURL = self.api_url + "/measurement/" + str(self.queryID) + "/result?format=raw"
        response = requests.get(requestURL)
        self.queryResult = response.json()

        if verbose:
            for key, value in self.queryResult.items():
                print(key, ":", value)

        return self.queryResult

    def parse_result(self):
        """returns nested dictionary of results"""

        out = dict()
        for index, item in enumerate(self.queryResult['queries']):
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

    def get_trace_indices(self):
        result = self.parse_result()
        return list(result.keys())

    def print_trace(self):
        result = self.parse_result()
        for key, value in result.items():
            for step, data in value.items():
                print(step, "\t",data['ip'], "\t", data['name'], "\t", data['time'])

            print("\n")

    def items(self, tracenumber):
        result = self.parse_result()
        for hop, data in result[tracenumber].items():
            yield hop, data['ip'], data['name'], data['time']