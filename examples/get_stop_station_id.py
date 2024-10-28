#!/usr/bin/env python
from ruter_api.api import GeocodeQuery

import json

query = GeocodeQuery("Kringsjå")

# print(query)

for station in query:
     print(json.dumps(station, indent=2))


