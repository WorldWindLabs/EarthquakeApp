import psycopg2,sys,os,tempfile,gzip
from subprocess import call


def make_temp_file():

    f = tempfile.NamedTemporaryFile(delete=False,mode="w+t")

    try:
        print('temp:', f)
        print('temp.name:', f.name)

        f.writelines(["TEST\n", "TEST2\n"])
        f.seek(0)

        for line in f:
            print(line.rstrip())

        f.flush()
        os.fsync(f.fileno())
        f.close()
        os.replace(f.name,"/tmp/TEST")


    finally:
        # Automatically cleans up the file
        f.close()
    print('Exists after close:', os.path.exists(f.name))


table = 'gefs.wb_esp_alaska_1_hires'

#if len(sys.argv) == 2:

#data_root = "../uploads.201606200003"
data_dict = {}



if True:

    data_root = sys.argv[1]

    for subdir, dirs, files in os.walk(data_root):
        for file in files:
            fname = os.path.join(subdir, file)
            #print (fname)
            if fname[-2:] == "gz":

                with gzip.open(fname, 'r') as f:
                    #file_contents = f.read()
                    collection = file.split('-')[0] + file.split('-')[1] + file.split('-')[2] + file.split('-')[3]
                    collection = collection.split("T")[0]    # Split off the HH:MM
                    collection = os.path.join("..", collection)

                    with open(collection,'ab') as c:
                        buf = f.readlines()
                        #print (buf)

                        c.writelines(buf)
                        #exit(0)
                    c.close()





                    #lines = f.readlines()
                    #print (lines)
                    #exit(0)

                #print(lines)
                #exit(0)
                #for l in lines:
                #    print(str(l[]).split(","))





                #call(["gzip", "-d", "-k", fname])
                #call(["mv", fname[:-3],"/tmp/tmpdbimport"])

                #f = open('/tmp/tmpdbimport')
                #conn = psycopg2.connect(host="10.193.20.17",port="5432",user="postgres",password="refOSSwi")
                #cur = conn.cursor()

                #cur.copy_from(f,table,sep=',')
                #conn.commit()

                #cur.execute("SELECT * FROM gefs.wb_esp_alaska_1_hires;")
                #print(cur.fetchone())

                #cur.close()
                #conn.close()

                f.close()
                #call(["rm", "/tmp/tmpdbimport"])


    #print(data_dict['../uploads.201606200003/wb_esp_alaska_4_hires-2016-06-20T075900Z-c32eb5bdc6bc91cf81c16c61e5cdd0b430020b490cf1774d321c491c9fed6da61381526d64ff2098d55ab498a0d869712325ef26f0cbbcfbbdae035537fd3646-done.csv.gz'])

    #f = open(sys.argv[1])

#for line in f:
    #print (line)
#    (ts,sr,n,data) = line.split(',')
#    data = data[:-1]

#    cur.execute("INSERT INTO gefs.wb_esp_alaska_1_hires VALUES (%s, %s, %s, %s)",(ts,sr,n,data))

#cur.copy_from(sys.stdout, "gefs.wb_esp_alaska_1_hires", sep=",")

else:

    print("Specify a path to import")
