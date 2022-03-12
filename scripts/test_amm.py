import asyncio
from starknet_py.contract import Contract
from starknet_py.net.client import Client
from starknet_py.net.models import StarknetChainId
from starknet_py.net.account.account_client import AccountClient

# Use testnet for playing with Starknet
devnet_client = Client("http://localhost:5000", chain=StarknetChainId.TESTNET)
testnet_client = Client("https://alpha4.starknet.io", chain=StarknetChainId.TESTNET)
mainnet_client = Client("https://alpha-mainnet.starknet.io",chain=StarknetChainId.MAINNET)


async def test_account():
    pass


async def test_init_pool(contract:Contract):    
    await contract.functions['init_pool'].invoke(100,200)
    
    (t1_balance,) = await contract.functions['get_pool_token_balance'].call(1)    
    assert t1_balance == 100

    (t2_balance,) = await contract.functions['get_pool_token_balance'].call(2)
    assert t2_balance == 200


async def main():
    contract = await Contract.from_address('0x05f240753832f887f9294a3fd60cb15f9554aaaa3b4ef60f08fe13fab902e6f2', devnet_client)    
    await test_init_pool(contract)

    #acc_client = await AccountClient.create_account(net="testnet")
    #await test_account()




if __name__ == '__main__':   
    asyncio.run(main())