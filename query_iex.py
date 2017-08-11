#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sys
import csv
import getopt
import requests as rq


def usage():
    print('usage: query_iex.py -c: [-s] [-n] [-p]: [-l]: \n'
          '-c , --company: company to retrieve information about \n'
          '-s , --stocks: if present retrieve stock information of company \n'
          '-n , --news: if presnet retrieve news about company \n'
          '-p , --period:  time period for -s; must be one of: \n'
          '    1d \n'
          '    1m \n'
          '    3m \n'
          '    6m \n'
          '    1y \n'
          '    2y \n'
          '    5y \n'
          '-l , --last: last n news story to collect')


data_dir = 'data'
stocks = False
news = False
company = None
period = None
last = None

opts, args = getopt.getopt(
    sys.argv[1:],
    'hsnc:p:l:',
    ['help'
     'stocks'
     'news'
     'company',
     'period'
     'last']
)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        quit(0)
    if opt in ('-s', '--stocks'):
        stocks = True
    if opt in ('-n', '--news'):
        news = True
    if opt in ('-c', '--company'):
        company = arg
    if opt in ('-p' '--period'):
        period = arg
    if opt in ('-l', '--last'):
        last = arg

if company is None:
    print('Missing required argument: company')
    quit(1)

if not stocks and period or not news and last:
    print('Invalid options, see usage (-h)')
    quit(0)

if period is None:
    period = '1m'

if last is None:
    last = 1

if stocks:
    try:
        response = rq.get('https://api.iextrading.com/1.0/stock/{}/chart/{}'
                          .format(company, period))
    except Exception as e:
        print('IEX request for stocks failed: {}'.format(e))
        quit(1)
    if response.status_code != 200:
        print('IEX request for stocks failed')
        quit(1)

    response_json = response.json()
    f = open('{}/{}_{}_stock.csv'.format(data_dir, company, period), 'w+')
    writer = csv.writer(f, quoting=1)
    # Hardcoded to maintain order
    writer.writerow(['date', 'open', 'close', 'change',
                     'high', 'low', 'volume'])
    for row in response_json:
        writer.writerow([row['date'], row['open'], row['close'], row['change'],
                         row['high'], row['low'], row['volume']])

if news:
    try:
        response = rq.get('https://api.iextrading.com/1.0/stock/{}/news/last/{}'
                          .format(company, last))
    except Exception as e:
        print('IEX request for news failed: {}'.format(e))
        quit(1)
    if response.status_code != 200:
        print('IEX request for news failed')
        quit(1)

    response_json = response.json()
    f = open('{}/{}_{}_news.csv'.format(data_dir, company, period), 'w+')
    writer = csv.writer(f, quoting=1)
    # Hardcoded to maintain order
    writer.writerow(['datetime', 'url', 'headline', 'summary'])
    for row in response_json:
        writer.writerow([row['datetime'], row['url'],
                         row['headline'], row['summary']])
