import json
import os
from Periscope import *


class StorageInterface:
    filename = ".store.json"
    data = {}

    def __init__(self):
        f = open(self.filename)
        jsonStr = f.read()

        if os.stat(self.filename).st_size != 0:
            try:
                self.data = json.loads(jsonStr)
            except:
                print("Could not load json storage file...")
        else:
            self.data = None

    def exists(self, id):
        """returns true if query is already saved, false otherwise"""
        for key in self.data.keys():
            if key == id:
                return True

        return False

    def _update_to_file(self):
        """Overwrites JSON file with contents of object data dictionary"""
        with open(self.filename, 'w') as f:
            data = json.dump(self. data, f, indent=4)

    def save_query(self, query):
        """Saves query to JSON file"""
        if self.exists(query.queryID):
            print("Query already saved...")
            return False

        else:
            entry = {}
            if query.get_result() is None: ## query has not completed
                entry['id'] = query.queryID
                entry['name'] = None
                entry['timestamp'] = None
                entry['command'] = None
                self.data[query.queryID] = entry
                self._update_to_file()
                return False

            else:
                entry['id'] = query.queryResult['id']
                entry['name'] = query.queryResult['name']
                entry['timestamp'] = query.queryResult['timestamp']
                entry['command'] = query.queryResult['command']
                self.data[query.queryID] = entry
                self._update_to_file()
                return True

    def delete_query(self, query):
        """Removes query from JSON file"""
        if not self.exists(query.queryID):
            print("No query:%s" % query.queryID, "in storage...")
            return False

        else:
            self.data.pop(query.queryID, None)
            self._update_to_file()
            return True

    def get_query(self, id):
        """returns query by ID"""
        try:
            return PeriscopeQuery(id)

        except KeyError as err:
            print(err.args[0], "is invalid ID...")
            return None

    def get_all_saved_queries(self):
        for key, value in self.data.items():
            print(key, value)

    def clear_file(self):
        with open(self.filename, mode='w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump([], f)