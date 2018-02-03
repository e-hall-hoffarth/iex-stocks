#!/usr/bin/env python
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import pandas
import sys
import getopt

infile = None


def usage():
    print('usage: iex_ plot.py -i: \n'
          '-i , --infile: (csv)file with data to be plotted')


try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        'hi:',
        ['help',
         'infile='])
except getopt.GetoptError as e:
    usage()
    quit(1)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        quit(0)
    if opt in ('-i', '--infile'):
        infile = arg

if infile is None:
    print('Missing required argument: infile')
    quit(1)

with open(infile) as f:
    data = pandas.read_csv(f, quotechar='"', sep=',')
    scatter_matrix(data)
    plt.show()
