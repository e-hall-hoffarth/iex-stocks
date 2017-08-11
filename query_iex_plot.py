import sys
import collections
from datetime import datetime
import csv
import json
import requests as rq
import matplotlib.pyplot as plt
import matplotlib

response = rq.get('https://api.iextrading.com/1.0/stock/aapl/chart/5y')

response_json = response.json()

point = collections.namedtuple('point', ['x','y'], verbose=False)
points = []

for i in range(0, len(response_json)):
    points.append(point(datetime.strptime(response_json[i]['date'],'%Y-%m-%d'), response_json[i]['high']))

plt.scatter([p.x for p in points],[p.y for p in points])
plt.show()
