# Get the most beautiful Payoff Chart using a single simple function


## Installation

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install payoffgraph-juttu
  ```

## Usage

## Import get_payoff

```python
from payoffgraph_juttu import get_payoff
```

# The only function you need to get the payoff graph

```python
get_payoff(positions_list,x1,x2)
```
This is the only function you need to plot the graph

# Parameters - positions_list, x1, x2

# positions_list

```python
position1=[strike,option_type,transaction_type,option_premium,quantity]

position2=[strike,option_type,transaction_type,option_premium,quantity]

position3=[strike,option_type,transaction_type,option_premium,quantity]

positions_list=[position1,position2,position3]

```
position_list is the list of all positions


```python
strike : int, float
Option Strike 

option_type : in the form {"CE","PE"}

transaction_type : in the form {"B","S"}
B: Buy 
S: Sell

option_premium : int, float
Option price

quantity : int
Quantity
Eg: (Nifty : 1Lot = 50 quantity, BankNifty: 1Lot = 25 quantity )

```


