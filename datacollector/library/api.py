import ast
from base64 import decode

import flask
import json
from druuid import Druuid
import mariadb
from flask import request

app = flask.Flask("datacollector:PiCentral")

user = "root"
password = "test"
host = "db"
port = 3306
database = "picentral"

'''
vehicle administrator
Admin sst is for user acess, 
    GET /duty lists all vehicles that are currently in use
    GET /avail lists al available IBs

Vehicle sst
    GET /ib/<modell> returns modell-ib and sets vehicle on active duty
    DELETE /ib/<modell> takes given modell from active duty
'''


# ---------------------Admin SST------------------
@app.route("/data", methods=['Get'])
def get_all_readings():
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(e)
    else:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM collected_data"
        )

        data = []
        for dset in cur:
            data.append(dset)
        conn.close()
        if not data:
            return flask.make_response("There is no data", 204)
        else:
            return flask.make_response(json.dumps(data), 200)


# ----------------------vehicle SST--------------------
@app.route("/up", methods=['POST'])
def upload_data():
    uuid = Druuid()

    data = request.data
    data = data.decode('UTF-8')
    data = ast.literal_eval(data)

    if "collector" and "reading" not in data:
        flask.make_response("Wrong input", 403)

    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(e)
    else:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO {table} VALUES {values}".format(table="collected_data",
                                                         values=(uuid.druuid, data["collector"], data["reading"]))
        )
        conn.commit()

    return flask.make_response(str(str(data) + "added"), 200)



