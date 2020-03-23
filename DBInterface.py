import mysql.connector as plug
import config as cfg

class DBInterface:
    connection = None
    user = cfg.dbuser
    password = cfg.dbpassword
    host = cfg.dbhost
    database = cfg.database

    def __init__(self):
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
            status = query.check_status()
            data = (status['id'],
                    status['name'],
                    status['timestamp'],
                    status['argument'],
                    status['command'],
                    status['queries'],
                    status['status']['completed'],
                    status['status']['failed'],
                    status['status']['pending']
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

    def sql(self, sqlSyntax):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlSyntax)

            result = cursor.fetchall()
            cursor.close()

            return result

        except plug.Error as err:
            if err.errno == plug.errorcode.ER_PARSE_ERROR:
                print("SQL syntax is incorrect...")
                return None
