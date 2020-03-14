import cmd
from Periscope import *
from StorageInterface import *

class Env:
    queryObjects = {}

    def add_query(self, query):
        self.queryObjects[query.queryID] = query

class CLI(cmd.Cmd):
    env = Env()

    def do_quit(self, line):
        print("exiting...")
        exit(0)

    def do_getlgnodes(self, line):
        args = {"command": "traceroute",
                "asn": None,
                "city": None,
                "country": None,
                "number": None,
                "verbose": True}
        rawArgs = self.parseline(line)[2]

        for item in rawArgs.split(" "): ## Parses line arguments
            if rawArgs == "" or rawArgs == "all":
                query = PeriscopeQuery()
                query.get_lg_nodes(verbose=True)
                return

            try:
                arg, value = item.split("=")
                args[arg] ## throws KeyError if arg is not valid
                args[arg] = value

            except KeyError:
                print("invalid parameter...")

            except ValueError:
                print("invalid syntax...")

        query = PeriscopeQuery()
        query.get_lg_nodes(command=args["command"],
                           asn=args["asn"],
                           city=args["city"],
                           country=args["country"],
                           number=args["number"],
                           verbose=args["verbose"])

    def do_listcountries(self, line):
        query = PeriscopeQuery()
        query.get_lg_countries(verbose=True)
        return

    def do_listsavedqueries(self, line):
        s = StorageInterface()
        v = s.get_all_saved_queries()
        print(v)

    def numerical_input(self, line):
        try:
            arg = line.strip('()')

            if not arg.isdigit():
                raise ValueError

            return(arg)

        except ValueError:
            print("Invalid Query ID...")

    def do_loadquery(self, line):

        id = self.numerical_input(line)
        s = StorageInterface()
        result = s.get_query(id)

        query = PeriscopeQuery(id)
        self.env.add_query(query)
        print("query", id, "loaded...")

    def do_listloadedqueries(self, line):
        for item in self.env.queryObjects:
            print(item)

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()

if __name__ == '__main__':
    HelloWorld().cmdloop()
