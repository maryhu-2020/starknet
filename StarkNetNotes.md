## StarkNet Notes

https://starknet.io/


1. L2 Node

 - Flow chart: https://cdn.discordapp.com/attachments/853954510515208192/947905885202681936/image.png

 - Provers
   	HD: >> L1 full node

 - Executor
	HD: > L1 full node (Solana type)

 above 2 cores consists of Starknet sequencer node	

 - L2 full node (for querying the current StarkNet state)
	HD: ~ L1 full node
 		
 - L2 Light Client
	HD: ~ L1 light node 

2. starknet command:
 - starknet -h
 - starknet deploy_account
 - starknet-compile
 - starknet deploy
 - starknet invoke
 - starknet call
 - starknet tx_status
 - starknet get_transaction
 - starknet get_transaction_receipt
 - starknet get_code
 - starknet get_block  
 - starknet get_storage_at

Note that while **deploy** and **invoke** affect StarkNet’s state, all other functions are read-only 

3. Possible transaction states:
	- **NOT_RECEIVED**: The transaction has not been received yet (i.e., not written to storage).
	- **RECEIVED**: The transaction was received by the sequencer.
	- **PENDING**: The transaction passed the validation and entered the pending block.
	- **REJECTED**: The transaction failed in validation and execution on L2 (thus was skipped) or rejected on L1.
	- **ACCEPTED_ON_L2**: The transaction passed the validation and entered an actual created block.
	- **ACCEPTED_ON_L1**: The transaction was accepted on-chain.

	During the construction of the block, as it is accumulating new transactions, the block’s status is PENDING. While PENDING, new transactions are dynamically added to the block. Once the sequencer decides to “close” the block, it becomes ACCEPTED_ON_L2 and its hash is computed.

	Pending block:  in every CLI command that takes block_number as an argument (contract_call/get_block/get_code/get_storage_at), we can query the StarkNet with respect to the pending block by specifying block_number=pending.

4. Fee schema:
 - estimated fee = estimated gas * estimated gas price
	- off-chain computational complexity of a transaction
		- execution traces: TraceCells[tx]/L
			- Number of Cairo steps
			- Number of applications of each Cairo builtin (e.g., five range checks and two Pedersens)
			- a pre-defined weights factor
				- Cairo step: 0.05 gas/step
				- ECDSA: 25.6 gas/application
				- range check: 0.4 gas/application
				- bitwise: 12.8 gas/application
				- Pedersen: 0.4 gas/application
	- costs occurring from L2→L1 messages
	- data availability