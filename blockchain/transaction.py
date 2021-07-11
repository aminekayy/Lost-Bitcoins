from crypto.utils import sha256
import datetime
import random
from typing import List, Dict


class Transaction:

	sequence = 0  # id of the new transaction
	# Dictionary that stores all the transactions
	transaction_dict = {}

	def __init__(self, from_id, to_id, value):
		self.sender = from_id
		self.recipient = to_id
		self.value = value
		self.date = None
		self.transaction_id = None

	# Calculate the transaction hash
	def __calculate_hash(self):
		# increase the sequence to avoid 2 identical transactions having the same hash
		Transaction.sequence += 1
		message = str(self.sender) + str(self.recipient) + str(self.value) + str(Transaction.sequence)
		return sha256(message)

	# A function that returns True if the transaction can be created
	def process_transaction(self, value, minimum):
		if value < minimum:
			print("Transaction inputs too small: " + str(value))
			return False

		self.transaction_id = self.__calculate_hash()
		self.__set_transaction_date()
		Transaction.transaction_dict["transaction "+str(Transaction.sequence)] = self
		return True


	# Set random date for the transaction between the last creation date of the two wallets and 1/2/2021
	def __set_transaction_date(self):
		from blockchain import Wallet
		from_id_date = Wallet.wallet_dict["wallet "+str(self.sender)].last_transaction
		to_id_date = Wallet.wallet_dict["wallet "+str(self.recipient)].last_transaction
		days_between = (from_id_date - to_id_date).days
		last_date = to_id_date
		if days_between > 0:
			last_date = from_id_date

		self.date = last_date + datetime.timedelta(days=random.randrange((Wallet.transaction_end_date - last_date).days))

	def process_transaction_mine(self, value, minimum):
		if value < minimum:
			print("Transaction inputs too small: " + str(value))
			return False

		message = str(self.sender) + str(self.recipient) + str(self.value) + str(Transaction.sequence)
		self.transaction_id = sha256(message)
		self.__set_transaction_date()
		Transaction.transaction_dict["transaction "+str(Transaction.sequence)] = self
		return True
