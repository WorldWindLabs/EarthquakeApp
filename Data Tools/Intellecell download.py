# Proof of concept - Intelecell Download Script

import requests

data = {'fields[]':['cf5c71dabb0f8a9ffa20abc3b194b990','db7817085234d28451b2b999f5c1b2b6','8b269ebb06edcefa2d00305a034460c1'],
        'startdate': '2016-06-28',
        'enddate':'2016-06-28',
        'timezone':'gmt',
        'time_format':'rfc3339',
        'sort':'ASC',
        'format':'csv',
        'submit':'1'
        }
url = 'http://www.intelesense.net/data/intelecell/9999999900040000/view/download/'
data_url = 'https://www.intelesense.net/website-live/userdata/temp/-gefs_kodiak.csv'

r = requests.post(url, data = data)

#r.text.find('\"https://www.intelesense.net/website-live/userdata/temp/')

d = requests.get(data_url)
print (d.content)

#r = requests.Request('POST','http://www.intelesense.net/data/intelecell/9999999900040000/view/download/', data=data)

#prepared = r.prepare()
#print (r.content)
#s = requests.session()
#s.send(prepared)

#print (r.content)
#print (r.text)
