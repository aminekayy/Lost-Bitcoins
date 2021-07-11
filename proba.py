import pandas as pd
import datetime
from math import *
import matplotlib.pyplot as plt
import time
import statistics
from decimal import *

# Current date
now = datetime.date.today()

# Loading the wallet.json file
data_wallet = pd.read_json (r'wallet1.json').T
print(data_wallet.head())

# Adding a column representing the timestamp between the current date and last transaction date ==> output in days
timestamp = [(now - datetime.date.fromisoformat(item)).days for item in data_wallet['last_transaction']]

data_wallet['timestamp']= timestamp
data_wallet['timestamp'].apply(lambda x: float(x))
data_wallet['balance'].apply(lambda x: float(x))

# Calculate the median of last transaction dates for all the wallets
T = statistics.median(data_wallet['timestamp'][1:])

# Calculate the median of all wallets' balances
N = statistics.median(data_wallet['balance'][1:])

# The first probabilistic function, the input is the last transaction date
def P(t):
    return 1/(1+exp(-(t-T)/2))

# The second probabilistic function, the input is the wallet balance
def F(x):
    return 1-((2/pi)*atan(N*x))

Lp = [(P(item)) for item in data_wallet['timestamp']]
Lf = [(F(item)) for item in data_wallet['balance']]

# List of combined probabilties calculated for all wallets
y = [i*j for i,j in zip(Lp,Lf)]

# Add the probabilities as a column in the wallet pandas dataframe
data_wallet['proba'] = y

# Display the wallets that are likely to be considered lost, change the "border" parameter as the border value
border = 0.7
result = data_wallet[data_wallet['proba']>border][['proba', 'name']].sort_values(by='proba', ascending = False)
ctr = 0
for index, row in result.iterrows():
    ctr += 1
    print("The Wallet that is most likely to be lost N° "+str(ctr)+":\t"+row['name']+"\tProbability ==>\t"+str(row['proba']))

# Plotting the output
plt.plot(data_wallet.id[1:], y[1:])
plt.show()