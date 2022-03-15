import asyncio
import os
from pathlib import Path
from starknet_py.contract import Contract
from starknet_py.net.client import Client
from starknet_py.net.models import StarknetChainId
from starknet_py.net.account.account_client import AccountClient,KeyPair
from starkware.starknet.public.abi import get_selector_from_name
from starkware.python.utils import from_bytes
# Use devnet for playing with Starknet

# >source .env
#
# >nile setup SIGNER_SECRET -->create an account
#    
# >nile deploy amm -->deploy the contract
SIGNER_SECRET=12345
SIGNER_ADDRESS='0x3d62f79be5f588c30125098d2dd39bab4757da655ea484ba6e302c4db24ac43'
AMM_CONTRACT_ADDRESS='0x02d938999364bab78663bc321c17bf28096e2319499c377129a16d396074b5eb'
network = "http://localhost:5000"
chain_id = StarknetChainId.TESTNET

#devnet_client = Client("http://localhost:5000", chain=StarknetChainId.TESTNET)
#testnet_client = Client("https://alpha4.starknet.io", chain=StarknetChainId.TESTNET)
#mainnet_client = Client("https://alpha-mainnet.starknet.io",chain=StarknetChainId.MAINNET)

#directory = os.path.dirname(__file__)
#contracts_source_base_path = Path(directory, "../contracts")
#amm_source_code = Path(os.path.join(contracts_source_base_path, "amm.cairo")).read_text("utf-8")

#
# create an client account instance for given signer_address and signer_secret
#
async def create_account_instance() -> AccountClient:
    #account_client = await AccountClient.create_account(net="http://localhost:5000", chain=StarknetChainId.TESTNET)
    #print('account address: %s' % hex(account_client.address))

    account_client = AccountClient(
        address=SIGNER_ADDRESS,
        key_pair=KeyPair.from_private_key(SIGNER_SECRET),
        net=network,
        chain=chain_id,
    )    
    
    return account_client

#
# create an contract instance that is connected to given account_client.
# This allows proxying transactions through the account to the target contract.
#
async def create_contract_instance(_client: AccountClient) -> Contract:
    contract = await Contract.from_address(
        address=AMM_CONTRACT_ADDRESS,
        client=_client,
    )
    return contract


async def test_init_pool(contract:Contract):    
    invocation = await contract.functions['init_pool'].invoke(6,20)    
    
    (t1_balance,) = await contract.functions['get_pool_token_balance'].call(1)    
    assert t1_balance == 6
    (t2_balance,) = await contract.functions['get_pool_token_balance'].call(2)
    assert t2_balance == 20
    print(t1_balance, t2_balance)


async def main():
    client_acct = await create_account_instance()
    contract = await create_contract_instance(client_acct)
    await test_init_pool(contract)


if __name__ == '__main__':   
    asyncio.run(main())