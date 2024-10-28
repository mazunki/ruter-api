#!/usr/bin/env python
from ruter_api.api import DepartureQuery



def main(station, format=None): 
    departures = DepartureQuery(station)
    # print(departures)

    for departure in departures:
        if not format:
            print(departure)
        else:
            print(f"{departure:{format}}")


if __name__ == "__main__":
    import sys
    station = sys.argv[1] if len(sys.argv) >= 2 else "NSR:StopPlace:59706"
    format = sys.argv[2] if len(sys.argv) >= 3 else None

    main(station, format)



