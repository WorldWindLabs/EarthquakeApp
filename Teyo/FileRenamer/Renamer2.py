import os

path = "/Users/tdeguzman/Desktop/untitled folder"

dict = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'}

for root, dirs, files in os.walk(path, topdown=False):

    print(root, "\n", dirs, "\n", files)

    for name in files:
        fName = os.path.join(root, name)

        with open(fName, "r") as f:

             line_list = f.readlines()

                # line = line.encode()
                #line_list.append(line)

             src_name = name

             midpoint = int(len(line_list)/2)

             name = name.replace(" ","")
             name = name.replace("(", "")
             name = name.replace(")", "")

             for i in range(10):
                 name = name.replace(str(i),"")

             name = name.replace("-gefs_","")

             #print("File: ", fName, "Last line: ", line_list[midpoint])
             month = dict[line_list[midpoint][0:2]]
             year = line_list[midpoint][6:10]
             #fileName = name[6:18]+"_"+"intelecell"+"_"+month+line_list[-1][6:10]
             fileName = name[:-4] + "_" + "intelecell" + "_" + month + year + ".csv"
             print(fileName)
             os.rename(os.path.join(path,src_name), os.path.join(path,fileName))

             f.close()
