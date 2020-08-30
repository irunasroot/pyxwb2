# Python Xwing Builder for X-wing v2.0

An Xwing builder written in python

master branch:  
![Unittest - master](https://github.com/minsis/pyxwb2/workflows/Python%20package/badge.svg?branch=master)

beta branch:  
![Unittest - beta](https://github.com/minsis/pyxwb2/workflows/Python%20package/badge.svg?branch=beta)


## Installation
Install from pypi
```bash
pip install pyxwb2
```

Install locally
```bash
git clone https://github.com/minsis/pyxwb2.git
cd pyxwb2
pip install .
```

## Usage
There are two separate libraries to use here: one fro loading XWS import data 
and one for loading the entire xwing-data pack for usage in an app or web app, etc

### XWS Data Load
To load and validate an XWB json file you can load it in. With a basic XWS load you get
a full manifest of data for the pilots included.

```python
from pyxwb2 import XwingSquadron

squadron = XwingSquadron()
squadron.import_squad("xws-squad.json")
```

As per the XWS standard point costs are ignored on import and loaded from the manifest.
If the source is trusted then the json schema is ignored.

To load trusted data
```python
from pyxwb2 import XwingSquadron

squadron = XwingSquadron(trust_source=True)
squadron.import_squad("xws-squad.json")
```

### X-wing Data Pack
This loads the entire manifest data from xwing-data. Gives you access to the entire data
strcutre that it has to offer.

```python
from pyxwb2 import XwingDataPack

data = XwingDataPack()
```

## Citing

### xwing-data2
The dataset included is provided by guidokessels/xwing-data2 under the MIT license

* Author: guidokessels
* Title: xwing-data2
* Version: 1.21.0
* Availability: [xwing-data2](https://github.com/guidokessels/xwing-data2)

### xws 
The ruleset spec used is provided by elistevens/xws-spec

* Author: elistevens
* Title: xws-spec
* Version: 2.0.0
* Availability: [xws-spec](https://github.com/elistevens/xws-spec)
