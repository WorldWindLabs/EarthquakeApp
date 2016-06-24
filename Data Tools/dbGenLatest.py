# dbGenLatest - 3-31-2016 - Generates a latest.json file for vector creation


import psycopg2,sys,os
from subprocess import call


table = 'gefs.wb_esp_alaska_3_hires'



#if len(sys.argv) == 2:

 #   table = sys.argv[1]
if True:

    conn = psycopg2.connect(host="10.193.20.17",port="5432",user="postgres",password="refOSSwi")
    cur = conn.cursor()
    conn.commit()
    cur.execute("SELECT * FROM " + table + " ORDER BY time_stamp DESC LIMIT 1" )
    (time_stamp, sr, n, data) = cur.fetchone()

    print(time_stamp,sr,n,data)
    d = bytearray(data)
    print(d[-12:])
    cur.close()
    conn.close()

#else:

#    print("Specify a table")
