import mysql.connector as plug
import config as cfg
from Periscope import PeriscopeQuery

class DBInterface:
    def __init__(self):
        self.connection = None
        self.user = cfg.dbuser
        self.password = cfg.dbpassword
        self.host = cfg.dbhost
        self.database = cfg.database
        self.connect()

    def connect(self):
        try:
            self.connection = plug.connect(user=self.user,
                               password=self.password,
                               host=self.host,
                               database=self.database)

        except plug.Error as err:
            if err.errno == plug.errorcode.ER_ACCESS_DENIED_ERROR:
                print("MySQL username/password is not correct...")

            elif err.errno == plug.errorcode.ER_BAD_DB_ERROR:
                print("Database", self.database, "does not exist...")

            else:
                print(err)

    def add_query(self, query):
        preamble = ("INSERT INTO caida_queries "
                    "(id, name, timestamp, argument, command, queries, completed, failed, pending) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )

        try:
            data = (query.queryStatus['id'],
                    query.queryStatus['name'],
                    query.queryStatus['timestamp'],
                    query.queryStatus['argument'],
                    query.queryStatus['command'],
                    query.queryStatus['queries'],
                    query.queryStatus['status']['completed'],
                    query.queryStatus['status']['failed'],
                    query.queryStatus['status']['pending']
                    )

            cursor = self.connection.cursor()
            cursor.execute(preamble, data)

            self.connection.commit()
            cursor.close()

        except plug.Error as err:
            if err.errno == plug.errorcode.ER_DUP_ENTRY:
                print("Query already saved...")

            else:
                print("Unknown error...")

            return False

    def add_routers(self, query):
        for host in query.iter_hosts():
            sqlSyntax = "SELECT * FROM router_info WHERE asn=%s " \
                        "AND router='%s' AND city='%s' AND country='%s'" \
                        % (host['asn'], host['router'], host['city'], host['country'])

            result = self.sql(sqlSyntax)

            if result == []:
                sqlSyntax = "INSERT INTO router_info (asn, router, city, country) " \
                            "VALUES ('%s', '%s', '%s', '%s')" \
                            % (host['asn'], host['router'], host['city'], host['country'])
                self.sql(sqlSyntax, commit=True)

    def get_router_id(self, trace):
        if trace.city != None:
            trace.city = trace.city.replace("'","")

        sqlSyntax = "SELECT * FROM router_info WHERE asn=%s " \
                    "AND router='%s' AND city='%s' AND country='%s'" \
                    % (trace.asn, trace.router, trace.city, trace.country)

        result = self.sql(sqlSyntax)

        if result == []:
            return None
        else:
            return result[0][0]


    def add_result(self, query):
        for trace in query.traces():
            router_id = self.get_router_id(trace)


            sqlSyntax = "INSERT INTO results (id, router_id, success, starttime, endtime) " \
                        "VALUES (%s, %s, %s, '%s', '%s')" \
                        % (query.queryID, router_id, trace.completed, trace.starttime, trace.endtime)

            self.sql(sqlSyntax, commit=True)

    def sql(self, sqlSyntax, commit=False):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlSyntax)

            if commit:
                self.connection.commit()
                cursor.close()

            else:
                result = cursor.fetchall()
                cursor.close()
                return result

        except plug.Error as err:
            if err.errno == plug.errorcode.ER_PARSE_ERROR:
                print("SQL syntax is incorrect...")
                print(sqlSyntax)
                return None

    def where(self, sqlSyntax=None):
        if sqlSyntax == None:
            result = self.sql("SELECT * From caida_queries")

        else:
            preamble = "SELECT * FROM caida_queries WHERE "
            result = self.sql(preamble + sqlSyntax)

        for item in result:
            query = PeriscopeQuery(item[0])
            query.update_result()
            yield query