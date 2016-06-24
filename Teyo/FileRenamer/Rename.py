import sys, time

print "Test"

a = 1
# a = "String"
class precise_time:

    variable = 1

    def msleep(self,ms):
        time.sleep(ms / 1000)

    def usleep(self,us):
        self.variable = 5
        time.sleep(us / 1000000)


pt = precise_time()


while True:


    a = 3

    if a == 1:
        print ("A is 1")

    elif a == 2:
        print("A is 2")

    else:
        print("A is something else")

    pt.msleep(1000)
    pt.usleep(1000000)