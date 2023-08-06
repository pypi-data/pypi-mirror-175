# MainFuncLib
This library is created for the first homework of MG 8411 Data Engineering. The goal is protecting information in a "script language" like Python - more specifically, we want to protect the key (password) to access Polygon data. The main function gets moved to a library, so the key is no longer exposed

### Installation
```
pip install MainFuncLib==0.1.1
```

### Get started
How to use this library in Max's code:

```Python
from MainFuncLib import mainFunc


# Example with 2 currency pairs
currency_pairs = [["AUD", "USD", [], Portfolio.Portfolio("AUD", "USD")],
                  ["GBP", "EUR", [], Portfolio.Portfolio("GBP", "EUR")]]

mainFunc(currency_pairs)
```