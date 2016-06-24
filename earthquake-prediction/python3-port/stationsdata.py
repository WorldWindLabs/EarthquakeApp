
# TODO: update other coordinates
w, h = 3, 9
data = [[0 for x in range(w)] for y in range(h)]

data[0] = ['ESP-Kenny-Lake-1', '61.726441', '-145.007213']
data[1] = ['ESP-Kodiak-2', '57.821684', '-152.365319']
data[2] = ['ESP-Kodiak-3', '57.747225', '-152.496467']
data[7] = ['ESP-Kodiak-4', '57.793343', '-152.393180']
data[3] = ['InteleCell-Kodiak', '57.79348', '-152.3932']
data[4] = ['InteleCell-Old-Harbor', '57.20403', '-153.3052']
data[5] = ['InteleCell-Copper-River', '62.11304', '-145.5268']
data[6] = ['InteleCell-Craig', '55.47625', '-133.1375']
data[8] = ['InteleCell-Ketchikan', '55.35328', '-131.677']

stations_data = {}

for station in data:
    stations_data[station[0]] = {'lati': station[1], 'long': station[2]}

def get(name):
    return stations_data[name]
