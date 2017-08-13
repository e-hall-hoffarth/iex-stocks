import sys
import pandas
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

infile = 'data/aapl_5y_data.csv'

data = pandas.read_csv(infile)

#scatter_matrix(data)
#plt.show()

#x = data.loc[:,['high']].values
#y = data.loc[:,['volume']].values

corrs = []

for i in range(0,len(data.columns) - 1):
    for j in range(0,len(data.columns) - 1):
        corrs.append(data[data.columns[i]].corr(data[data.columns[j]]))

print(corrs)
