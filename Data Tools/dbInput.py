import psycopg2,sys,os
from subprocess import call


table = 'gefs.wb_esp_alaska_1_hires'



if len(sys.argv) == 2:


    rootdir = sys.argv[1]

    for subdir, dirs, files in os.walk(rootdir):
#    for files in os.walk(rootdir):
        for file in files:
            fname = os.path.join(subdir, file)
            print (fname)
            if fname[-2:] == "gz":


                call(["gzip", "-d", "-k", fname])
                call(["mv", fname[:-3],"/tmp/tmpdbimport"])

                f = open('/tmp/tmpdbimport')
                conn = psycopg2.connect(host="10.193.20.17",port="5432",user="postgres",password="refOSSwi")
                cur = conn.cursor()
                try:
                     cur.copy_from(f,table,sep=',')
                except:
                     print (Exception)
                     pass

                conn.commit()
            #cur.execute("SELECT * FROM gefs.wb_esp_alaska_1_hires;")
            #print(cur.fetchone())
                cur.close()
                conn.close()

                f.close()
                call(["rm", "/tmp/tmpdbimport"])
                call(["mv",fname,rootdir+"/imported/"])


    #f = open(sys.argv[1])

#for line in f:
    #print (line)
#    (ts,sr,n,data) = line.split(',')
#    data = data[:-1]

#    cur.execute("INSERT INTO gefs.wb_esp_alaska_1_hires VALUES (%s, %s, %s, %s)",(ts,sr,n,data))

#cur.copy_from(sys.stdout, "gefs.wb_esp_alaska_1_hires", sep=",")

else:

    print("Specify a path to import")
