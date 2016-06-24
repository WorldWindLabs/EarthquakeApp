import queue



station_map = {

                    'zGxbWe1R00I0XVQ5mo69F9e9qrr' : ['world_bridge_earthquake_precursor_signal_alaska_1',0],
                    'kB6EbMxAKXIY5g9wZbGQi3D6BQg' : ['world_bridge_earthquake_signal_precursors_alaska_2',1],
                    'EGMwq5m16RTG5K0QMj7KUVyP9YA' : ['world_bridge_earthquake_signal_precursors_alaska_3',2],
                    'ppkZO7k2gvu2RWqbjdj4u2re9m8' : ['wb_esp_alaska_4',3]
                }

buffer = [queue.LifoQueue(), queue.LifoQueue(), queue.LifoQueue(), queue.LifoQueue()]


key = 'zGxbWe1R00I0XVQ5mo69F9e9qrr'

buffer[0].qsize()

buffer[station_map[key][1]].put(1)