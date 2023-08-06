# dw1656_hw1
A small demo library created for Data Engineering homework, to obfuscate the Polygon API key from the main method.

### Installation
```
pip install dw1656-hw1
```

### Get started
How to retrieve the required Polygon API key with this lib:

```Python
from dw1656_hw1 import PolygonAPIKey

# Retrieve the API key
api_key = PolygonAPIKey.get_polygon_api_key()
```