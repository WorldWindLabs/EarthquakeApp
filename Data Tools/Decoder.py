from __future__ import print_function
from struct import *
import json
import time,datetime
import traceback
import sys


csv_output = True
json_output = False

#test_line = '2016-06-19T07:59:14Z,123,123,1C4200F301C81C4100F501C81C4100F501C91C4100F501C91C4100F501C81C4100F501C91C4100F501C91C4100F301C91C4100F301C81C4100F301C81C4100F301C81C4100F501C91C4100F301C91C4100F301C81C4100F301C81C4100F301C81C4100F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C81C4200F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301CA1C4200F301CA1C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4100F301C91C4100F301C91C4100F301C81C4100F501C81C4100F501C81C4100F501C81C4100F501C81C4100F301C91C4100F301C91C4100F301C81C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301C91C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F501C81C4100F301C81C4100F301C91C4100F301C91C4100F501C81C4100F301C81C4100F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4300F301CA1C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C81C4100F301C81C4100F501C81C4100F501C81C4100F501C81C4100F501C81C4100F301C81C4100F301C81C4100F301C91C4100F501C91C4100F301C8'

#filename = '/Users/GEFS/Desktop/ESP_Sensor/wb_esp_alaska_1_hires20160619'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) != 2:
    eprint("converter.py <file>")
    exit(-1)

filename = sys.argv[1]

try:

    with open(filename,"r") as f:

        for line in f.readlines():

            fields = line.rstrip("\n").split(",")

            ts = datetime.datetime.strptime(fields[0],"%Y-%m-%dT%H:%M:%SZ")

            sr = int(fields[1])
            n = int(fields[2])


            #print ("Sample Starts @ ", fields[0])
            #print ("Sample Rate: \t", sr, "Hz")
            #print ("N = \t\t\t", n)

            sub_sample = 0



            if len(fields[3]) != n*12:
                eprint("Data mismatch - dropping row: ", line)

                break


            for i in range(0, len(fields[3]),12):

                value = fields[3][i:i+12]

                value = bytearray.fromhex(value)
                #print(value)

                (x, y, z) = unpack('>hhh', value)

                nT = 100000

                x = (x / 15000) * nT
                y = (y / 15000) * nT
                z = (z / 15000) * nT

                x = round(x, 2)
                y = round(y, 2)
                z = round(z, 2)

                # 2016-02-27 23:16:39.173


                ts = ts.replace(microsecond=int((sub_sample/123)*1000000))

                #print(ts.strftime("%Y-%m-%d %H:%M:%S.%f"))


                if csv_output is True:

                    print(ts.strftime("%Y-%m-%d %H:%M:%S.%f") + "," + str(x) + "," + str(y) + "," + str(z))

                elif json_output is True:

                    json_data = json.dumps({'timestamp': fields[0], 'x': x, 'y': y, 'z': z}, sort_keys=True, indent=None,
                                           separators=(',', ':'))
                    print(json_data)

                sub_sample = sub_sample + 1

except Exception:

    print(traceback.print_exc())

finally:

    f.close()

