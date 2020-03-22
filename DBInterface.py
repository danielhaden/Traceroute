import mysql.connector as plug
import config as cfg

class DBInterface:
    user = cfg.dbuser
    password = cfg.dbpassword
    host = cfg.dbhost
    database = cfg.database

    def connect(self):
        try:
            cnx = plug.connect(user=self.user,
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