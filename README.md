# etherpadlite
A client library for etherpad

## Installation
Installing this library is as simple as running `pip install etherpadlite`. 

## Usage
Usage is meant to be as simple as possible.
```python
>>> from etherpadlite.client import EtherpadClient
>>> client = EtherpadClient(base_url='http://localhost:9001', api_key='<your_api_key>')
...
>>> groups = client.list_groups()
['g.12345', 'g.67890']
```
