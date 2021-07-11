from blockchain import Block, Transaction

class BlockChain:

	# Define a mining pool (21M noobcoins), the transaction fees will be retrieved from here (2 noobcoins for each transaction) 
	pool = 21000000

	def __init__(self, difficulty):
		self.blocks = []
		self.difficulty = difficulty

	# Add a block to the blockchain list of blocks
	def append_block(self, block: Block, mine_block=True):
		if mine_block:
			block.mine(self.difficulty)
			print("Block mined: " + block.hash)

		self.blocks.append(block)

	# Check the validity of the whole blockchain
	def check_valid(self, genesis_transaction: Transaction):
		hash_prefix = "0" * self.difficulty
		prev_hash = self.blocks[0].hash
		for block_ind in range(1, len(self.blocks)):
			print("Checking block %d" % block_ind)

			block = self.blocks[block_ind]

			# compare registered hash and calculated hash
			"""if block.calculate_hash() != block.hash:
				print("Invalid hash")
				return False
			"""
			# check registered previous hash with its real previous hash
			if block.previous_hash != prev_hash:
				print("Invalid previous hash")
				return False

			prev_hash = block.hash

			# check if hash is solved
			if not block.hash.startswith(hash_prefix):
				print("Hash is not solved")
				return False

		return True

	# Last registered block hash
	def last_block_hash(self):
		if self.blocks:
			return self.blocks[-1].hash
		else:
			return "0"

	# Add a new block to the blockchain
	def append_new_block(self, mine=True):

		block = Block(self.last_block_hash())

		if mine:
			block.mine(self.difficulty)
			print("Block mined: " + block.hash)

		self.append_block(block)

		return block

	# Print the important details about the blockchain
	def print(self):
		index = 0

		for block in self.blocks:
			print("Block %d" % index)
			block.print()
			index += 1