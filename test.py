from blockchain import Block, BlockChain, Wallet, Transaction
import random
import json

if __name__ == "__main__":
	difficulty = 2
	minimum_transaction = 1

	blockchain = BlockChain(difficulty)

	# Create coinbase wallet (mining pool) and assign 21M noobcoins as a balance
	wallet_coinbase = Wallet(0)
	wallet_coinbase.balance = BlockChain.pool

	# Genesis transaction: send 2 noobcoins from and to the wallet coinbase
	wallet_coinbase.send_funds(0,2)
	genesis_transaction = Transaction.transaction_dict["transaction 1"]

	# Create the genesis block (block 0)
	print("Creating and mining genesis block")
	genesis_block = Block(0, "0")

	# Add the genesis transaction to the genesis block and mine it
	genesis_block.add_transaction(genesis_transaction,minimum_transaction)

	# Add the genesis block to the blockchain
	blockchain.append_block(genesis_block)
	print("Genesis Block")
	genesis_block.print()

	# Choose a number of wallets to simulate
	n = input("Enter a number of Wallets you want to simulate:\t\t")
	while n=="":
		n = input("Enter a number of Wallets you want to simulate:\t\t")
	n = int(n)

	# generate n wallets through a loop
	for i in range(1,n+1):
		wallet_tmp = Wallet(i)
		print(wallet_tmp.__dict__)

	# Generate distributed balances (https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html)
	d = int(n*51/100)
	for i in range(1,d):
		Wallet.wallet_dict['wallet '+str(i)].balance = random.randint(4,15)
	
	for i in range(d,d+int(n*25/100)):
		Wallet.wallet_dict['wallet '+str(i)].balance = random.randint(15,100)

	d += int(n*25/100)
	for i in range(d, d+int(n*15/100)):
		Wallet.wallet_dict['wallet '+str(i)].balance = random.randint(100,1000)

	d += int(n*15/100)
	for i in range(d, d+int(n*6/100)):
		Wallet.wallet_dict['wallet '+str(i)].balance = random.randint(1000,10000)

	d += int(6/100)
	for i in range(d, d+int(n*1.7/100)):
		Wallet.wallet_dict['wallet '+str(i)].balance = random.randint(10000,100000)



	#print("is chain valid?", blockchain.check_valid(genesis_transaction))
	
	# generate as many transactions as we want
	n_transactions = int(input("Enter a number of Transactions you want to simulate:\t\t"))

	block_id = 1		# for the block id
	tr_id = 2		# for the transaction id
	block_tmp = Block(1, genesis_block.hash)
	for i in range(1,n_transactions+1):
		# Choose randomly the sender and recipient ids
		from_id = random.randint(1,n)
		to_id = random.randint(1,n)
		rand_value = random.randint(2,25)

		# Make sure the sender is not the recipient as well
		while from_id == to_id:
			to_id = random.randint(2,n)

		from_wallet = Wallet.wallet_dict["wallet "+str(from_id)]
		to_wallet = Wallet.wallet_dict["wallet "+str(to_id)]
		# Make sure that the funds are sufficient
		#while (from_wallet.balance <= rand_value):
		#	rand_value = random.randint(2,rand_value+1)

		while not(from_wallet.send_funds(to_id, rand_value)):
			from_id = random.randint(1,n)
			from_wallet = Wallet.wallet_dict["wallet "+str(from_id)]
			rand_value = random.randint(2,25)
		print()
		print("\t#### TRANSACTION N° "+str(tr_id)+" #####")
		print("Wallet SENDER N°:\t" + str(from_id))
		print("Wallet RECIPIENT N°:\t" + str(to_id))
		print("The amount of transaction is:\t" + str(rand_value))

		# Add the transaction to the current block
		block_tmp.add_transaction(Transaction.transaction_dict["transaction "+str(tr_id)], minimum_transaction)

		# print balances of the involved wallets
		from_wallet.print_balance()
		to_wallet.print_balance()

		# Create, mine blocks and append them to the blockchain (Each block contains 5 transactions)
		
		if tr_id%5==0 and tr_id!=0:
			print("\nBlock " + str(block_id))
			blockchain.append_block(block_tmp)
			block_tmp.print()
			#print("is chain valid?", blockchain.check_valid(genesis_transaction))
			block_id += 1
			block_tmp = Block(block_id, block_tmp.hash)
	
		tr_id += 1


	if tr_id%5!=1:
		print("\nBlock " + str((tr_id // 5)+1))
		blockchain.append_block(block_tmp)
		block_tmp.print()
	#print("is chain valid?", blockchain.check_valid(genesis_transaction))
	
	# Export data to json files
	data_wallet = {}
	for key in Wallet.wallet_dict.keys():
		data_wallet[key] = Wallet.wallet_dict[key].__dict__
		data_wallet[key]["creation"] = str(data_wallet[key]["creation"])
		data_wallet[key]["last_transaction"] = str(data_wallet[key]["last_transaction"])
	data_wallet = json.dumps(data_wallet)
	with open("wallet.json", 'w') as f_wallet:
		f_wallet.write(data_wallet)
		f_wallet.close()

	
	data_transaction = {}
	for key in Transaction.transaction_dict.keys():
		data_transaction[key] = Transaction.transaction_dict[key].__dict__
		data_transaction[key]["date"] = str(data_transaction[key]["date"])
	with open("transaction.json", "w") as f_transaction:
		json.dump(data_transaction, f_transaction)


	data_block = {}
	for key in Block.block_dict.keys():
		data_block[key] = Block.block_dict[key].__dict__
		data_block[key]["timestamp"] = str(data_block[key]["timestamp"])
		del data_block[key]["transactions"]
	with open("block.json", "w") as f_block:
		json.dump(data_block, f_block)
	
	



	