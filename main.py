import sys
from Periscope import *
from Topology import *
from StorageInterface import *
from CLI import *
from DBInterface import *

d = DBInterface()
s = PeriscopeQuery(1250502)

d.add_router_result(s)


# item = d.sql("SELECT * FROM router_info WHERE caida_id=5533437")
# for thing in item:
#     print(thing)

exit(0)


query = PeriscopeQuery() ## create query object
hosts = query.get_lg_nodes() # add all nodes

query.traceroute(destination="162.151.38.197", ## perform traceroute from each host to 162.151.38.197
                 hosts=hosts,
                 verbose=True)

query.check_status(verbose=True) ## check status of request with Periscope API

s = StorageInterface() ## save query
s.save_query(query)



exit(0)









###################### CLI ########################
CLI().cmdloop()
exit(0)

