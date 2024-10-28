#!/usr/bin/env python
from ruter_api.api import DepartureQuery



def main(): 
    departures = DepartureQuery(station)
    # print(departures)

    for departure in departures:
        print(departure)


if __name__ == "__main__":
    import sys
    station = sys.argv[1] if len(sys.argv) >= 2 else "NSR:StopPlace:59706"
    main()



