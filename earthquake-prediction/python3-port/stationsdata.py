import loadearthquake as earthquake
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

def get_relevant_dates(min_mag = 4):

	stations = [['ESP-Kenny-Lake-1', '2016-01-01', '2016-03-01'],
	            ['ESP-Kenny-Lake-1', '2016-01-06', '2016-02-06'],
	            ['ESP-Kenny-Lake-1', '2016-04-01', '2016-04-19'],
	            ['ESP-Kenny-Lake-1', '2016-04-01', '2016-06-21'],
	            ['ESP-Kenny-Lake-1', '2016-04-19', '2016-05-05'],
	            ['ESP-Kenny-Lake-1', '2016-04-28', '2016-05-02'],
	            ['ESP-Kenny-Lake-1', '2016-05-05', '2016-05-24'],
	            ['ESP-Kenny-Lake-1', '2016-05-19', '2016-05-22'],
	            ['ESP-Kenny-Lake-1', '2016-05-24', '2016-06-16'],
	            ['ESP-Kenny-Lake-1', '2016-06-16', '2016-06-21'],
	            ['ESP-Kodiak-2', '2016-06-05', '2016-06-21'],
	            ['ESP-Kodiak-3', '2016-04-07', '2016-04-30'],
	            ['ESP-Kodiak-3', '2016-04-10', '2016-04-13'],
	            ['ESP-Kodiak-3', '2016-04-10', '2016-04-17'],
	            ['ESP-Kodiak-3', '2016-04-10', '2016-05-10'],
	            ['ESP-Kodiak-3', '2016-04-28', '2016-05-02'],
	            ['ESP-Kodiak-3', '2016-05-19', '2016-05-22'],
	            ['ESP-Kodiak-3', '2016-06-03', '2016-06-10'],
	            ['ESP-Kodiak-4', '2016-06-04', '2016-06-21']]

	relevant_data = []
	for item in stations:
	    name, begin, end = item
	    stationcoord = get(name)
	    earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=min_mag)

	    if len(earthquake.index) >= 1:
	        relevant_data.append(item)

	return relevant_data