This is our final year project about the recovery of lost Bitcoins

These are the main features of our project:

- Simulate real world bitcoin blockchain using Python by generating wallets and transactions (random balances,creation and transaction dates)

- Respect the bitcoin wallet distribution when generating the wallets (Check out this website: https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html) 

- Propose a probabilistic model to decide whether a bitcoin is lost or not, and then recover it using two
parameters: how old is the wallet(i.e. last time it was part of a transaction) and the balance of this wallet.

- This proposed model is not practical on Bitcoin, but it can be easily considered for similar
new future cryptocurrencies!


### Install
`pip install -r requirements.txt`

### Run
For setting the environment and having json files as an output for analysis
`python test.py`

For applying the probabalistic model and plotting the results
`python proba.py`

### Credits
- Mohamed Amine AJINOU
- Karim HABOUCH

Mentors: Meryem AYACHE, Amjad GAWANMEH 

INPT Rabat School | Major: Cybersecurity & Digital Trust Engineering

©PFA July 2021
