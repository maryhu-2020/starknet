from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.compiler.compile import get_selector_from_name

balance_key = get_storage_var_address('balance')
print(f'Balance key: {balance_key}')

# compute the selector based on the L1 handler name
print(get_selector_from_name('deposit'))

