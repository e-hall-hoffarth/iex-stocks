import sys
import csv
import getopt
import requests as rq

outfile = None
stocks = False
news = False
company = None
period = None
last = None

stock_headers = ['date', 'open', 'close', 'change', 'high', 'low', 'volume']
news_headers = ['datetime', 'url', 'headline', 'summary']


def usage():
    print('usage: query_iex.py -c: -o: [-s] [-n] [-p]: [-l]: \n'
          '-o , --outfile: file to which results are written'
          '-c , --company: company to retrieve information about \n'
          '-s , --stocks: if present retrieve stock information of company \n'
          '-n , --news: if presnet retrieve news about company \n'
          '-p , --period: (requires -s) time period for -s; must be one of: \n'
          '    1d \n'
          '    1m \n'
          '    3m \n'
          '    6m \n'
          '    1y \n'
          '    2y \n'
          '    5y \n'
          '-l , --last: (requires -n) last n news story to collect \n'
          'Note that because only one outfile is specified -s and -n are \n'
          'mutually exclusive.')


try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        'hsnc:o:p:l:',
        ['help',
         'stocks',
         'news',
         'company=',
         'outfile=',
         'period='
         'last='])
except getopt.GetoptError as e:
    usage()
    quit(1)

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
    if opt in ('-o', '--outfile'):
        outfile = arg
    if opt in ('-p', '--period'):
        period = arg
    if opt in ('-l', '--last'):
        last = arg

if outfile is None:
    print('Missing required argument: Outfile')
    quit(1)

if company is None:
    print('Missing required argument: Company')
    quit(1)

if not stocks and period or not news and last:
    usage()
    quit(0)

if stocks and news:
    print('Both stocks and news requested, providing only stocks.')

if period is None:
    period = '1m'

if last is None:
    last = 1

if stocks:
    try:
        resp = rq.get('https://api.iextrading.com/1.0/stock/{}/chart/{}'
                      .format(company, period))
    except Exception as e:
        print('IEX request for stocks failed: {}'.format(e))
        quit(1)
    if resp.status_code != 200 or resp.text == '""':
        print('IEX request for stocks failed')
        quit(1)

    resp_json = resp.json()
    f = open(outfile, 'w+')
    writer = csv.writer(f, quoting=1)
    # Hardcoded to maintain order
    writer.writerow(stock_headers)
    for row in resp_json:
        for col in stock_headers:
            if col not in row:
                row[col] = ''
        writer.writerow([row['date'], row['open'], row['close'], row['change'],
                         row['high'], row['low'], row['volume']])

if news:
    try:
        resp = rq.get('https://api.iextrading.com/1.0/stock/{}/news/last/{}'
                      .format(company, last))
    except Exception as e:
        print('IEX request for news failed: {}'.format(e))
        quit(1)
    if resp.status_code != 200 or resp.text == '""':
        print('IEX request for news failed')
        quit(1)

    resp_json = resp.json()
    f = open(outfile, 'w+')
    writer = csv.writer(f, quoting=1)
    # Hardcoded to maintain order
    writer.writerow(news_headers)
    for row in resp_json:
        for col in news_headers:
            if col not in row:
                row[col] = ''
        writer.writerow([row['datetime'], row['url'],
                         row['headline'], row['summary']])
