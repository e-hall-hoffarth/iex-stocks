import requests as rq
import getopt
import sys
import csv
import time

infile = None
outdir = None
period = None
headers = ['date', 'open', 'close', 'change', 'high', 'low', 'volume']
stocks = []


def usage():
    print('usage: query_iex.py -i: -o: [-p]: \n'
          '-i , --infile: (csv)file that contains list of companies for which \n'
          'stock information is to be retrieved \n'
          '-o , --outdir: path where stock information is written \n'
          '-p , --period: (requires -s) time period for -s; must be one of: \n'
          '    1d \n'
          '    1m \n'
          '    3m \n'
          '    6m \n'
          '    1y \n'
          '    2y \n'
          '    5y \n')


try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        'hi:o:p:',
        ['help',
         'infile=',
         'outfile=',
         'period='])
except getopt.GetoptError as e:
    usage()
    quit(1)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        quit(0)
    if opt in ('-i', '--infile'):
        infile = arg
    if opt in ('-o', '--outdir'):
        outdir = arg.rstrip('/')
    if opt in ('-p', '--period'):
        period = arg

if infile is None:
    print('Missing required argument: infile')
    usage()
    quit(1)

if outdir is None:
    print('Missing required argument: outdir')
    usage()
    quit(1)

if period is None:
    period = '1m'

with open(infile) as data:
    reader = csv.reader(data)
    for row in reader:
        stocks.append(row[0])

print('Found {} stocks, starting queries.'.format(len(stocks)))

found = 0

for stock in stocks:
    try:
        resp = rq.get('https://api.iextrading.com/1.0/stock/{}/chart/{}'
                      .format(stock.lower(), period))
    except Exception as e:
        print('IEX request for stock {} failed: {}'.format(stock, e))
        continue
    if resp.status_code == 200 and resp.text != '""':
        print('Stock found: {}'.format(stock))
        found = found + 1
        outfile = '{}/{}_{}.csv'.format(outdir, stock.lower(), period)

        resp_json = resp.json()
        f = open(outfile, 'w+')
        writer = csv.writer(f, quoting=1)
        # Hardcoded to maintain order
        writer.writerow(headers)
        for row in resp_json:
            for col in headers:
                if col not in row:
                    row[col] = ''
            writer.writerow([row['date'], row['open'], row['close'],
                             row['change'], row['high'], row['low'],
                             row['volume']])
    else:
        print('Stock not found: {}'.format(stock))

    time.sleep(1)

print('Found {} of {} stocks'.format(found, len(stocks)))
