from typing import Dict
import datetime
import random
from blockchain import Transaction
from Crypto.PublicKey.RSA import RsaKey

class Wallet:

	# Class attributes
	start_date = datetime.date(2010, 1, 1)
	end_date = datetime.date(2016, 1, 1)
	transaction_end_date = datetime.date(2020, 1, 1)
	days_between = (end_date - start_date).days
	# Dictionary containing all the created wallets {name:instance Wallet}   
	wallet_dict = {}

	def __init__(self,id):
		self.id = id
		self.name = "wallet {}".format(str(id))
		self.creation = self.__creation_date()
		self.balance = self.__rand_balance()
		self.last_transaction = self.creation
		self.__add_wallet_dict()
		


	# Assign a random creation date of the wallet between 1/1/2010 and 1/2/2021
	def __creation_date(self):
		random_d = random.randrange(Wallet.days_between)
		return Wallet.start_date + datetime.timedelta(days=random_d)

	# Assign a random balance as a starting point for the new wallet
	def __rand_balance(self):
		return random.randint(10,100)

	# Add the wallet object to the dictionary containing all wallets
	def __add_wallet_dict(self):
		Wallet.wallet_dict[self.name] = self

	# Send funds from "wallet x" to "wallet y"
	def send_funds(self, recip_id, value):
		if self.balance < value:
			print("Not enough balance, transaction discarded")
			return False

		if value <= 0:
			print("Value should be positive, transaction discarded")
			return False

		else:
			self.balance -= value
			Wallet.wallet_dict["wallet "+str(recip_id)].balance += value
			transaction = Transaction(self.id, recip_id, value)	# Use a Transaction instance
			if transaction.process_transaction(value, 2):
				self.last_transaction = transaction.date
				Wallet.wallet_dict["wallet "+str(recip_id)].last_transaction = transaction.date
				print("Transaction CONFIRMED")
				from blockchain import BlockChain
				BlockChain.pool -= 2	# Take-away the transaction fees
				Wallet.wallet_dict["wallet 0"].balance -= 2
				return True

	def print_balance(self):
		print(self.name + " balance: %d" % self.balance)

	