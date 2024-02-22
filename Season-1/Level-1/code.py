
'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal

MAX_TOTAL =   1_000_000
MAX_PAYMENT = 100_000
MAX_QUANTITY = 1000
MIN_QUANTITY = 1

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')


# Note that the test setup is such that you cannot raise an error for a bad amount
# or quantity, instead you just have to skip those orders/payments



def validorder(order: Order):
    payments = Decimal('0')
    expenses = Decimal('0')

    for item in order.items:

        if item.type == "payment":
            if abs(item.amount) > MAX_PAYMENT:
                #print(f"Payment amount of: {item.amount} is too high")
                continue
            
            payments += Decimal(str(item.amount))

        elif item.type == 'product':

            if abs(item.amount) > MAX_PAYMENT:
                #print(f"Payment amount of: {item.amount} is too high")
                continue

            if item.quantity > MAX_QUANTITY:
                #print(f"You have requested too much of the item: {item.description}.")
                continue

            if item.quantity < MIN_QUANTITY:
                #print(f"There was an attempt to order less than 1 of the item: {item.description}.")
                continue
            if item.quantity % 1 != 0: # whole number
                #print(f"Quantity of {item.description} is not equal to a whole number")
                continue
            
            expenses += Decimal(str(item.amount)) * item.quantity

        else:
            return f"Invalid item type: {item.type}"

    if abs(payments) > MAX_TOTAL or abs(expenses) > MAX_TOTAL:
        return "Total amount payable for an order exceeded"

    net = payments - expenses

    if net != 0:
        return f"Order ID: {order.id} - Payment imbalance: ${net:0.2f}" 

    return f"Order ID: {order.id} - Full payment received!"
    


