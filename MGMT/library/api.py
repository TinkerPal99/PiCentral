import flask
import json
from os import listdir
import mariadb
from flask import request
import xml.etree.ElementTree as etree

app = flask.Flask("MGMT:PiCentral")

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
@app.route("/duty", methods=['Get'])
def expose_dutylist_json():
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
            "SELECT * FROM active_vehicles"
        )

        vehiclelist = []
        for vehicle in cur:
            vehiclelist.append(vehicle)
        conn.close()
        if not vehiclelist:
            return flask.make_response("No vehicles on active duty", 204)
        else:
            return flask.make_response(json.dumps(vehiclelist), 200)


@app.route("/avail", methods=['Get'])
def expose_avail_json():
    avail = listdir(path="xml/")

    if not avail:
        return flask.make_response("No vehicles available", 204)
    else:
        available = []
        for item in avail:
            item = item.split(".")
            data = {"vehicle": item[0],
                    "ib-type": item[1]}

            available.append(data)
        return flask.make_response(json.dumps(available), 200)


@app.route("/ib/add/", methods=['Post'])
def new_ib():
    """
    GH#4
    :return: flaskresponse
    """
    try:
        assert "json" in request.headers.get("Content-Type")
    except AssertionError:
        flask.make_response("Format not supported", 415)

    ib = request.data
    ib = json.loads(ib)
    created = []
    try:
        for base in ib:
            f = open("xml/" + base + ".json", "x")
            try:
                f.write(json.dumps(ib.get(base)))
            finally:
                f.close()
            created.append(base)
    except FileExistsError:
        return flask.make_response("File exists", 409)
    else:
        return flask.make_response(json.dumps(created), 201)


# ----------------------vehicle SST--------------------
@app.route("/ib/<modell>", methods=['Get'])
def expose_installedbase(modell):
    f = None
    try:
        f = open("xml/{file}.xml".format(file=modell)).read()
    except FileNotFoundError:
        pass
    try:
        f = open("xml/{file}.json".format(file=modell)).read()
    except FileNotFoundError:
        pass

    if f is None:
        return flask.make_response(404)

    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print("MAJOR ERROR: " + e)
    else:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO {table}(name) VALUES ('{values}')".format(table="active_vehicles", values=modell)
        )
        conn.commit()

    return flask.make_response(str(f), 200)


@app.route("/ib/<modell>", methods=['Delete'])
def deactivate_vehicle(modell):
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
            "DELETE FROM {tables} WHERE name = '{value}';".format(tables="active_vehicles", value=modell)
        )
        conn.commit()
        conn.close()
    return flask.make_response(f"Modell {modell} isn't on active duty anymore".format(modell=modell), 201)
