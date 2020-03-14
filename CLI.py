import cmd
from Periscope import *

class CLI(cmd.Cmd):
    def do_quit(self, line):
        print("exiting...")
        exit(0)

    def do_getlgnodes(self, line):
        args = {"command": "traceroute",
                "asn": None,
                "city": None,
                "country": None,
                "number": None}
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
                           verbose=True)


    def do_EOF(self, line):
        return True

    def postloop(self):
        print()

if __name__ == '__main__':
    HelloWorld().cmdloop()
