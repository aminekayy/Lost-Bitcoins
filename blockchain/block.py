from datetime import datetime
from crypto.utils import sha256
from crypto.utils import merkle_root


class Block:

	# Dictionary containing all blocks
	block_dict = {}

	def __init__(self, block_id, previous_hash):
		self.previous_hash = previous_hash
		self.nonce = 0
		self.timestamp = None
		self.transactions = []
		self.hash = self.calculate_hash()
		self.name = "block {}".format(str(block_id))

	# Add a transaction to the block
	def add_transaction(self, transaction, minimum_transaction) -> bool:
		if transaction is None:
			return False

		# process transaction and check if valid, unless block is genesis block then ignore.
		if self.previous_hash != "0":
			if not transaction.process_transaction_mine(transaction.value, minimum_transaction):
				print("Transaction failed to process")
				return False

		self.transactions.append(transaction)
		self.timestamp = transaction.date
		return True

	# Concatenate the previous hash, nonce, timestamp and the merke root hash as one string to hash it later with calculate_hash() function
	def get_message(self):
		return self.previous_hash + str(self.nonce) + str(self.timestamp) + self.get_merkle_root()

	# calculate the merkle root hash
	def get_merkle_root(self) -> str:
		transaction_ids = [transaction.transaction_id for transaction in self.transactions]
		return merkle_root(transaction_ids)

	# calculate the block hash
	def calculate_hash(self):
		message = self.get_message()
		return sha256(message)

	# Block mining
	def mine(self, difficulty=2):
		hash_prefix = "0" * difficulty
		while not self.hash.startswith(hash_prefix):
			self.nonce += 1
			self.hash = self.calculate_hash()
			Block.block_dict[self.name] = self

	def __str__(self):
		return self.hash

	# Print the important details of the block
	def print(self):
		print("hash:", self.hash)
		print("transactions_count", len(self.transactions))
		print("merkle_root:", self.get_merkle_root())
		print("timestamp:", self.timestamp)
		print("nounce:", self.nonce)
		print("prev_hash:", self.previous_hash)
		print()

    