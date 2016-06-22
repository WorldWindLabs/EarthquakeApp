
# TODO: update other coordinates
w, h = 3, 10
data = [[0 for x in range(w)] for y in range(h)]

data[0] = ['ESP-Kenny-Lake-1', '0', '0']
data[1] = ['ESP-Kodiak-2', '0', '0']
data[2] = ['ESP-Kodiak-3', '57.747225', '-152.496467']
data[9] = ['ESP-Kodiak-4', '57.793343', '-152.393180']
data[3] = ['InteleCell-Kodiak', '57.79348', '-152.3932']
data[4] = ['InteleCell-Old-Harbor', '0', '0']
data[5] = ['InteleCell-Copper-River', '0', '0']
data[6] = ['InteleCell-Craig-River', '0', '0']
data[7] = ['InteleCell-Craig', '0', '0']
data[8] = ['InteleCell-Ketchikan', '0', '0']

stations_data = {}

for station in data:
    stations_data[station[0]] = {'lati': station[1], 'long': station[2]}


def get(name):
    return stations_data[name]
