# Declare this file as a StarkNet contract.
%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math import assert_nn
from starkware.starknet.common.syscalls import get_caller_address

# Define a storage variable.
# A map from user (represented by account contract address)
# to their balance.
@storage_var
func balance(user : felt) -> (res : felt):
end

# An event emitted whenever increase_balance() is called.
# current_balance is the balance before it was increased.
@event
func increase_balance_called(
        current_balance : felt, amount : felt, user:felt):
end


# Increases the balance by the given amount.
@external
func increase_balance{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*,
        range_check_ptr}(amount : felt):

    # Verify that the amount is positive.
    with_attr error_message("Amount must be positive."):
        assert_nn(amount)
    end

    # Obtain the address of the account contract.
    let (user) = get_caller_address()

    let (res) = balance.read(user=user)
    balance.write(user, res + amount)


    # Emit the event.
    increase_balance_called.emit(current_balance=res, amount=amount, user=user)
    return ()
end

# Returns the current balance.
@view
func get_balance{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*,
        range_check_ptr}(user : felt) -> (res : felt):

    let (res) = balance.read(user=user)
    return (res)
end