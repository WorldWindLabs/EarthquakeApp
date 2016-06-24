import psycopg2,sys,os,tempfile,gzip
from subprocess import call
import traceback

file_list = './datafilelist'
i = 0

with open(file_list,'r') as fl:


    for fname in fl:

        i = i + 1
        fname = fname.rstrip()

        if (i % 10000) == 0:
            print ("At file: ", i)

        if fname[-2:] == "gz":


            try:

                with gzip.open(fname, 'r') as f:
                    #file_contents = f.read()
                    file = fname[fname.find('wb'):]
#                    print ("HERE: ", file)

                    collection = file.split('-')[0] + file.split('-')[1] + file.split('-')[2] + file.split('-')[3]
                    collection = collection.split("T")[0]    # Split off the HH:MM
                    collection = os.path.join("./combined-files2", collection)

                    with open(collection,'ab') as c:
                        buf = f.readlines()
                        #print (buf)

                        c.writelines(buf)
                        #exit(0)
                    c.close()

            except Exception:

                print("Problem processing file: ", fname)
                print(traceback.format_exc())



        elif fname[-3:] == "csv":

            try:

                with open(fname, 'r') as f:

                    file = fname[fname.find('wb'):]

                    #file_contents = f.read()
                    collection = file.split('-')[0] + file.split('-')[1] + file.split('-')[2] + file.split('-')[3]
                    collection = collection.split("T")[0]    # Split off the HH:MM
                    collection = os.path.join("./combined-files2", collection)

                    with open(collection,'ab') as c:
                        buf = f.readlines()
                        #print (buf)

                        c.writelines(buf)
                        #exit(0)
                    c.close()

            except Exception:

                print("Problem processing file: ", fname)
                print(traceback.format_exc())