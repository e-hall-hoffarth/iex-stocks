#!/usr/bin/env python
from datetime import datetime
import matplotlib.pyplot as plt
import collections
import getopt
import sys
import csv

infile = None
timeseries = None


def usage():
    print('usage: query_iex.py -i: -t: \n'
          '-i , --infile: (csv)file with data to be plotted \n'
          '-t , --timeseries: column to be plotted over time \n')


try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        'hi:t:',
        ['help',
         'infile=',
         'timeseries='])
except getopt.GetoptError as e:
    usage()
    quit(1)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        quit(0)
    if opt in ('-i', '--infile'):
        infile = arg
    if opt in ('-t', '--timeseries'):
        timeseries = arg

if infile is None:
    print('Missing required argument: infile')
    quit(1)

if timeseries is None:
    print('Missing required argument: timeseries')
    quit(1)

point = collections.namedtuple('point', ['x', 'y'], verbose=False)
points = []

with open(infile, 'rU') as data:
    reader = csv.DictReader(data)
    next(reader)

    for row in reader:
        points.append(point(datetime.strptime(row['date'], '%Y-%m-%d'),
                      float(row[timeseries])))

plt.scatter([p.x for p in points], [p.y for p in points])
plt.show()
