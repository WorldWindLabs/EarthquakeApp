import psycopg2

conn = None
cur = None

def send_to_db(table,record):

    global conn, cur
    #table = 'gefs.' + table
    table = 'gefs.lo_res_test_1'

    if conn is None:
        conn = psycopg2.connect(host="10.193.20.17",port="5432",user="postgres",password="refOSSwi")

    if cur is None:
        cur = conn.cursor()


    cur.execute("INSERT INTO " + table + " VALUES (%s, %s, %s, %s)", (record[0], record[1], record[2], record[3]))
    conn.commit()


record = [1,2,3,4]
send_to_db('a',record)