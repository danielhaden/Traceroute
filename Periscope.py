# python character encoding: utf-8
from PeriscopeKey import PeriscopeKey
import requests
import random
import json


class PeriscopeQuery():
    credentials = PeriscopeKey()
    api_url = "https://periscope.caida.org/api/v2"
    measurement = dict()

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

    def traceroute(self, destination, hosts):
        self.measurement["argument"] = destination
        self.measurement["command"] = "traceroute"
        self.measurement["name"] = "test"
        self.measurement["hosts"] = hosts

        data = json.dumps(self.measurement)
        headers = self.gen_headers(data)

        response = requests.post(self.api_url + "/measurement", data=data, headers=headers)

        print("HTTP response status: " + str(response.status_code))
        print("HTTP response headers: " + str(response.headers))
        print("HTTP response text:  " + str(response.text))

        decoded_response = response.json()
        print("Measurement ID: " + str(decoded_response["id"]))

        if response.status_code == 201:
            decoded_response = response.json()
            return decoded_response["id"]

        else:
            print("Response status code error: ", response.status_code)
            exit(1)

    def get_result(self, resultID):
        requestURL = self.api_url + "/measurement/" + str(resultID) + "/result?format=raw"
        print(requestURL)
        result = requests.post(requestURL, headers=self.gen_headers(resultID))
        print(result.json())

        return result