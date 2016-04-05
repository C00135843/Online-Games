from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import mysql.connector

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '3.5.1',
                     'last_build':  date.today().isoformat() }
        self.write(response)
 
class SignIn(tornado.web.RequestHandler):
    def get(self):
        print("get")

        # get config data
        configDict = self.get_config()
        config = configDict["config"]
        connection = configDict["connection"]
        cursor = configDict["cursor"]

        # Define our MySQL query
        query = ("SELECT name, password from signInTable")
        cursor.execute(query)

        nameList = []
        passwordList = []

        # Get the selected values from the cursor
        # Values are 'tuples' so we convert to string
        for u in cursor:
            nameList.append(str(u[0]))
            passwordList.append(str(u[1]))

        count = 0
        for u in nameList:
            self.write("[ " + u + ": " + passwordList[count] + " ]  ")
            count+=1

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        print(name)
        print(password)

        # Get our configuration data from the helper function
        # so we can use the MySQL-Python connector
        configDict = self.get_config()
        config = configDict["config"]
        connection = configDict["connection"]
        cursor = configDict["cursor"]

        query = ("INSERT INTO signInTable"
                "(name, password)"
                "VALUES (%(name)s, %(password)s)")

        data_user = {
        'name': name,
        'password': password
        }

        cursor.execute(query, data_user)

        connection.commit()

    def get_config(self):
        """ get_config helper function
        Sorts configuration for the MySQL database
        """
        config = {
        'user': 'root',
        'password': 'soccermatch8',
        'host': '127.0.0.1',
        'database': 'signInDB'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        configDict = dict()
        configDict["config"] = config
        configDict["connection"] = connection
        configDict["cursor"] = cursor

        return configDict
 
 
 
 
 
application = tornado.web.Application([
    (r"/signin", SignIn),
    (r"/version", VersionHandler)
])
 
if __name__ == "__main__":
	application.listen(443)
	tornado.ioloop.IOLoop.instance().start()