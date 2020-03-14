import json
import os
class StorageInterface:
    filename = ".pastqueries"
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

    def save_query(self, query):
        firstItemFlag = False
        if os.stat(self.filename).st_size == 0:
            firstItemFlag = True
            with open(self.filename, mode='w', encoding='utf-8') as f:
                f.truncate(0)
                json.dump([], f)

        if self.data != None:
            for item in self.data: ## check that query is not already saved
                if item['id'] == query.queryResult['id']:
                    print("Query already saved...")
                    return None

        entry = dict()
        entry['id'] = query.queryResult['id']
        entry['name'] = query.queryResult['name']
        entry['timestamp'] = query.queryResult['timestamp']
        entry['command'] = query.queryResult['command']

        with open(self.filename, mode='a', encoding='utf-8') as f:
            f.seek(f.tell()-1, os.SEEK_SET)
            f.truncate()
            if not firstItemFlag:
                f.write(', ')
            f.write(json.dumps(entry, indent=4))
            f.write(']')

    def get_query(self, id):
        """returns query by ID"""
        try:
            return self.data[id]

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