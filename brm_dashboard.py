from flask import Flask, request
from flask_restful import Resource, Api
import cx_Oracle


host='0.0.0.0'
port=8001

app = Flask(__name__)

api = Api(app)

items = []

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class Accounts(Resource):
    def get(self):
        connection = cx_Oracle.connect("pin", "pin", "172.17.0.3:1521/pindb")

        cursor = connection.cursor()
        query = "SELECT * FROM config_t"
        cursor.execute(query)
        accounts = dictfetchall(cursor)
        connection.close()
        return {'configs': accounts }

api.add_resource(Accounts, '/configs')        


app.run(host, port, debug=True)