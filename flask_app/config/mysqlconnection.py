import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        # Change the user and password as needed
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        # Establish the connection to the database
        self.connection = connection

    # The method to query the database
    def query_db(self, query:str, data:tuple=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data) if data else query
                print("Running Query:", query)
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    return cursor.fetchall()
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # If the query fails the method will return FALSE
                print("Something went wrong", e)
                return False

    # Close the connection method
    def close_connection(self):
        self.connection.close()

# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
