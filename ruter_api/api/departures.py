#!/usr/bin/env python
import os
import json
import time
import datetime
import requests
from typing import Set
from .routes import Route
from ..config import *

class Departure:
    def __init__(self, arrival_time: datetime.datetime, departure_time: datetime.datetime, destination: str, route: Route):
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.destination = destination
        self.route = route

    @classmethod
    def from_dict(cls, data: dict):
        arrival_time = datetime.datetime.fromisoformat(data["expectedArrivalTime"].replace("Z", "+00:00"))
        departure_time = datetime.datetime.fromisoformat(data["expectedDepartureTime"].replace("Z", "+00:00"))
        destination = data["destinationDisplay"]["frontText"]
        route = Route.from_dict(data["serviceJourney"]["journeyPattern"]["line"])
        return cls(arrival_time, departure_time, destination, route)

    def __repr__(self):
        return f"Departure(arrival_time={self.arrival_time}, departure_time={self.departure_time}, destination={self.destination}, route={self.route})"

    def __format__(self, fmt):
        placeholders = {
                "{icon}": f"{self.route.transport_icon}",
                "{time}": f"{self.departure_time:%H:%M}",
                "{countdown}": f"{self.countdown.strip()}",
                "{line_no}": f"{self.route.line_number}",
                "{destination}": f"{self.destination}",
                "\\t": "\t",
                "\\n": "\n",
        }

        for key in placeholders:
            fmt = fmt.replace(key, placeholders[key])

        return fmt


    def __str__(self):
        return f"{self.route.transport_icon}\t{self.departure_time:%H:%M} ({self.countdown.strip():>8}) {self.route.line_number:>5} {self.destination}"

    @property
    def countdown(self):
        now = datetime.datetime.now(self.departure_time.tzinfo)  # Use the same timezone as departure_time
        time_left = self.departure_time - now

        if time_left <= datetime.timedelta(0):
            return "too late"
        elif time_left < datetime.timedelta(minutes=1):
            return f"{time_left.seconds:>5} sec"
        elif time_left < datetime.timedelta(minutes=5):
            minutes, seconds = divmod(time_left.seconds, 60)
            return f"{minutes:>2}m {seconds:>2}s"
        elif time_left < datetime.timedelta(hours=1):
            minutes, seconds = divmod(time_left.seconds, 60)
            return f"{minutes:>2} min"
        elif time_left < datetime.timedelta(hours=3):
            hours, seconds = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            return f"{hours:>2}h {minutes:>2}min"
        else:
            hours, seconds = divmod(time_left.seconds, 3600)
            return f"{hours:>2}hr"

class DepartureQuery:
    data: dict
    departures: Set

    def __init__(self, station_id: str, number_of_departures: int = 5, time_range: int = 7200):
        if not station_id.startswith("NSR:StopPlace"):
            from .stations import GeocodeQuery
            station_id = GeocodeQuery(station_id)[0].station_id

        self.station_id = station_id
        self.number_of_departures = number_of_departures
        self.time_range = time_range
        self.cache_file = os.path.join(CACHE_DIR, f"departures_{station_id}.json")

    @property
    def graphql_query(self) -> str:
        return f"""
        {{
          stopPlace(id: "{self.station_id}") {{
            id
            name
            estimatedCalls(timeRange: {self.time_range}, numberOfDepartures: {self.number_of_departures}) {{
              expectedArrivalTime
              expectedDepartureTime
              destinationDisplay {{
                frontText
              }}
              serviceJourney {{
                journeyPattern {{
                  line {{
                    id
                    name
                    transportMode
                  }}
                }}
              }}
            }}
          }}
        }}
        """

    def is_cache_valid(self) -> bool:
        if not os.path.exists(self.cache_file):
            return False
        last_modified = os.path.getmtime(self.cache_file)
        return (time.time() - last_modified) < CACHE_EXPIRATION

    def load_from_cache(self):
        with open(self.cache_file, 'r') as f:
            self.data = json.load(f)

    def save_to_cache(self):
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        with open(self.cache_file, 'w') as f:
            json.dump(self.data, f)

    def get_data(self):
        if self.is_cache_valid():
            self.load_from_cache()
        else:
            headers = {
                "Content-Type": "application/json",
                "ET-Client-Name": APP_NAME
            }
            response = requests.post(API_ENDPOINT, json={"query": self.graphql_query}, headers=headers)
            response.raise_for_status()
            self.data = response.json()
            self.save_to_cache()

    def __iter__(self):
        if not hasattr(self, "data"):
            self.get_data()

        station_data = self.data["data"]["stopPlace"]
        departures_data = station_data.get("estimatedCalls", [])

        for departure_data in departures_data:
            yield Departure.from_dict(departure_data)

    def __repr__(self):
        return f"DepartureQuery(station_id={self.station_id}, number_of_departures={self.number_of_departures}, time_range={self.time_range})"

