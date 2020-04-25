import psycopg2

class GlobalDatabaseAccess:
    def __init__(self):
        try:
            # add global database credentials here
            self.connection = psycopg2.connect(user="", password="", host="localhost", port="5432", database="")
            self.cursor = self.connection.cursor()

            # Print PostgreSQL Connection properties
            print(self.connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record,"\n")
        except (Exception, psycopg2.Error) as error :
            print("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
            #if(self.connection):
                #self.cursor.close()
                #self.connection.close()
                print("finally")

    def executeQuery(self, query):
        print("executing: " + query)
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        print(record)
        return record

    def close(self):
        # closing database connection.
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
