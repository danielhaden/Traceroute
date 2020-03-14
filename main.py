import sys
from Periscope import *
from Topology import *
from StorageInterface import *
from CLI import *

#### FOR TESTING ####
# s = StorageInterface()
# print(s.get_query("1250485"))
# exit(0)
######################


CLI().cmdloop()


exit(0)


query1 = PeriscopeQuery(1250485)
query1.check_status(verbose=True)


print(query1.queryResult['id'])
# query1.traceroute("96.120.12.153", query1.get_available_lg_nodes(3), verbose=True)

j = JSONStorage()
j.save_query(query1)
print(j.get_queries())


results = query1.parse_result()

topo = Topology()
topo.add_query(query1, verbose=False)

print(topo.G.order())
topo.write_to_file('C:/Users/hadend/Desktop/test.graphml')



exit(0)
