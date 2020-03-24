from PeriscopeKey import PeriscopeKey
import requests
import random
import json
from xml.etree import ElementTree as ET
from Trace import Trace


class PeriscopeQuery():
    def __init__(self, id=None):
        self.credentials = PeriscopeKey()
        self.api_url = "https://periscope.caida.org/api/v2"
        self.measurement = {}
        self.pending = None
        self.queryID = None
        self.queryStatus = None
        self.queryResult = None
        self.errorFlag = False
        self.hosts = None
        self.queryID = id

        if self.queryID != None:
            self.update_status()

            if self.queryStatus != None:
                self.update_result()

    def gen_headers(self, data):
        """Generates HTTP POST headers"""

        headers = {
            'Content-type': 'application/json; charset=utf-8',
            'X-Public': self.credentials.public_key,
            'X-Hash': self.credentials.gen_signature(data)
        }
        return headers

    def set_traceroute_hosts(self, command="traceroute", asn=None, router=None, city=None, country=None, number=None):
        """Sets specified servers as traceroute sources. Number arg sets number of randomly selected hosts"""
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
            fields = ["asn", "router", "city", "country"]
            if number is not None:
                available_hosts = random.sample(available_hosts, number)

            for host in available_hosts:
                entry = {}
                for field in fields:
                    try:
                        entry[field] = host[field]

                    except KeyError as err:
                        entry[err.args[0]] = ""

                hosts.append(entry)

            self.hosts = hosts

        except TypeError:
            if 'errors' in available_hosts.keys(): ## checks that query arg is valid
                print("Invalid ID...")
                self.hosts = None

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

    def traceroute(self, destination, name):
        """submits traceroute query from each host to destination"""

        self.measurement["argument"] = destination
        self.measurement["command"] = "traceroute"
        self.measurement["name"] = name
        self.measurement["hosts"] = self.hosts

        data = json.dumps(self.measurement)
        headers = self.gen_headers(data)

        response = requests.post(self.api_url + "/measurement", data=data, headers=headers)

        if response.status_code == 201:  ## HTTP 201 = POST request has been successfully created on server
            decoded_response = response.json()
            self.queryID = decoded_response["id"]
            self.update_status()

        else:
            self.errorFlag = True

    def update_status(self):
        """Gets query status from CAIDA server"""
        try:
            requestURL = self.api_url + "/measurement/" + str(self.queryID)
            response = requests.get(requestURL)
            self.queryStatus = response.json()
            self.pending = self.queryStatus['status']['pending']

        except KeyError:
            print("Invalid or missing query ID...")
            self.queryStatus = None

    def update_result(self):
        """pulls result from Periscope"""
        self.update_status()

        if self.queryStatus == None or self.pending !=0:
            self.queryResult = None

        else:
            requestURL = self.api_url + "/measurement/" \
                                      + str(self.queryID) \
                                      + "/result?format=raw"
            response = requests.get(requestURL)
            self.queryResult = response.json()

    def traces(self):
        "yields all traceroutes of query"
        if self.queryResult == None:
            return None

        for raw_trace in self.queryResult['queries']:
            yield Trace(raw_trace)

    def bad_traces(self):
        "yields failed traceroutes of query"
        if self.queryResult == None:
            return None

        for raw_trace in self.queryResult['queries']:
            trace = Trace(raw_trace)

            if not trace.completed:
                yield trace

    def good_traces(self):
        "yields completed traceroutes of query"
        if self.queryResult == None:
            return None

        for raw_trace in self.queryResult['queries']:
            trace = Trace(raw_trace)

            if trace.completed:
                yield trace

    def iter_hosts(self):
        "yields hosts"
        if self.hosts == None:
            return None

        for host in self.hosts:
            yield host