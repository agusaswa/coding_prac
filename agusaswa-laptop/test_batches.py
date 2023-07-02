import batch_func
import pytest
from datetime import date

def make_batch_and_order(line_sku: str, ava_qty: int, ordered_qty: int) -> tuple:
    '''This is a helper function to create batch and order for testing purpose.'''

    batch_sku="SMALL-TABLE"
    return (batch_func.Batch("test batch", batch_sku, ava_qty, date.today()),
            batch_func.OrderLine("test order", line_sku, ordered_qty)
    )

def test_reduce_qty() -> bool:
    '''This is a test to assert whether the table qty is reduced when order line is allocated.'''

    batch_1, line_1 = make_batch_and_order("SMALL-TABLE", 10, 2)
    batch_1.allocate(line_1)
    exp_outp = 8
    assert batch_1.ava_qty == exp_outp

def test_can_allocate_if_ava() -> bool:
    '''
    This is a test to assert whether batch can be allocated for order if the available stock qty
    is more than the ordered qty.
    '''
    batch_2, line_2 = make_batch_and_order("SMALL-TABLE", 10, 9)
    assert batch_2.can_allocate(line_2)

def test_cannot_allocate_if_not_ava() -> bool:
    '''
    This is a test to assert whether batch cannot be allocated for order if the available stock qty
    is less than the ordered qty.
    '''
    batch_3, line_3 = make_batch_and_order("SMALL-TABLE", 1, 9)
    assert batch_3.can_allocate(line_3) is False

def test_cannot_allocate_if_not_same_sku() -> bool:
    '''
    This is a test to assert whether batch cannot be allocated for order if the order lne sku 
    is different than the ava. sku.
    '''
    batch_4, line_4 = make_batch_and_order("SMALL-CHAIR", 1, 9)
    assert batch_4.can_allocate(line_4) is False

if __name__ == "__main__":
    pytest.main(["-vv"])
