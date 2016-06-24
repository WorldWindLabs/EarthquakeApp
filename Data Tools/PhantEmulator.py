from flask import Flask
from flask import request
from flask import jsonify
import datetime, time, queue
import psycopg2, os

csv_path = "."

station_map = {

                    'zGxbWe1R00I0XVQ5mo69F9e9qrr' : ['gefs.world_bridge_earthquake_precursor_signal_alaska_1',0],
                    'kB6EbMxAKXIY5g9wZbGQi3D6BQg' : ['gefs.world_bridge_earthquake_signal_precursors_alaska_2',1],
                    'EGMwq5m16RTG5K0QMj7KUVyP9YA' : ['gefs.world_bridge_earthquake_signal_precursors_alaska_3',2],
                    'ppkZO7k2gvu2RWqbjdj4u2re9m8' : ['gefs.wb_esp_alaska_4',3]
                }

buffer = [queue.LifoQueue(), queue.LifoQueue(), queue.LifoQueue(), queue.LifoQueue()]
latest = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]

conn = None
cur = None

def send_to_db(table,record):

    global conn, cur

    #table = 'gefs.lo_res_test_1'

    try:

        if conn is None:
            conn = psycopg2.connect(host="10.193.20.17",port="5432",user="postgres",password="refOSSwi")

        if cur is None:
            cur = conn.cursor()


        cur.execute("INSERT INTO " + table + " VALUES (%s, %s, %s, %s);", (record[0], record[1], record[2], record[3]))
        conn.commit()
        conn.close()
        conn = None
        cur = None

    except Exception:

        if(conn):
            conn.close()
        return(-1)

    return(0)

def append_to_csv(table,record):

    date_stamp = (datetime.datetime.utcfromtimestamp(time.time()).isoformat() + "Z")[0:10]

    try:

        with open(os.path.join(csv_path, date_stamp+table+".csv"),"a") as f:
            f.writelines(record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "\n")
            f.close()

    except:
        if (f):
            f.close()
        return(-1)

    return(0)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

"""
@app.route('/input/ppkZO7k2gvu2RWqbjdj4u2re9m8.txt', methods=['POST'])
def input():
    print(request.form['x'],request.form['y'],request.form['z'])
    return "OK"
"""

@app.route('/input/<key>.txt', methods=['POST'])
def input(key):

    try:
        table = station_map[key][0]
    except:
        return ("Invalid key", 500)

    time_stamp = time.time()
    time_stamp = datetime.datetime.utcfromtimestamp(time_stamp).isoformat()+"Z"

    record = [ time_stamp, request.form['x'], request.form['y'], request.form['z'] ]

    buf_index = station_map[key][1]

    buffer[buf_index].put(record)
    latest[buf_index] = record

    if send_to_db(table,record):
        return("Database problem", 500)

    if append_to_csv(table,record):
        return("Filesystem problem", 500)

    return("OK")

@app.route('/output/<key>/latest.json', methods=['GET'])
def output(key):

    try:
        table = station_map[key]
    except:
        return ("Invalid key", 500)

    buf_index = station_map[key][1]
    print(latest[buf_index])

    return jsonify(time_stamp=latest[buf_index][0],
                   x=latest[buf_index][1],
                   y=latest[buf_index][2],
                   z=latest[buf_index][3])



if __name__ == "__main__":
    app.run()