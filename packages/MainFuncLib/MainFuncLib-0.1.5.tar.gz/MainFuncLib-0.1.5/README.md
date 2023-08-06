# MainFuncLib
This library is created for the first homework of MG 8411 Data Engineering. The goal is protecting information in a "script language" like Python - more specifically, we want to protect the key (password) to access Polygon data. The main function gets moved to a library, so the key is no longer exposed

### Installation
```
pip install MainFuncLib==0.1.5
```

### Get started
Make sure version==0.2.11 of Polygon-api-client is installed, code will not work with later versions. Example of how to use this library in Max's code, delete main() in Max's code and replace with the library:

```Python
from MainFuncLib import mainFunc

# Example with 2 currency pairs
currency_pairs = [["AUD", "USD", [], portfolio("AUD", "USD")],
                  ["GBP", "EUR", [], portfolio("GBP", "EUR")]]

mainFunc(currency_pairs)
```