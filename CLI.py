import cmd
from Periscope import *

class CLI(cmd.Cmd):
    def do_quit(self, line):
        print("exiting...")
        exit(0)

    def do_getlgnodes(self, line):
        args = {}
        rawArgs = self.parseline(line)[2]

        for item in rawArgs.split(" "): ## Parses line arguments
            if rawArgs == "" or rawArgs == "all":
                query = PeriscopeQuery()
                query.get_lg_nodes(verbose=True)
                return

            try:
                arg, value = item.split("=")
                args[arg] = value

                query = PeriscopeQuery()
                query.get_lg_nodes(verbose=True)

            except:
                print("invalid syntax")


    def do_EOF(self, line):
        return True

    def postloop(self):
        print()

if __name__ == '__main__':
    HelloWorld().cmdloop()
