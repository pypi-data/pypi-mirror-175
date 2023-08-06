### Installation

> pip install polygon-homework-fall-2022

### Get started
How to use this package:

```
from get_data import *

# change to your currency pairs
currency_pairs = [["AUD","USD",[],portfolio("AUD","USD")],
                  ["GBP","EUR",[],portfolio("GBP","EUR")],
                   ["USD","CAD",[],portfolio("USD","CAD")]]

main(currency_pairs)
```