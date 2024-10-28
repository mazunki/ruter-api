#!/usr/bin/env python
from typing import List, Optional

from .departures import Departure
from ..config import GEOCODER_ENDPOINT, API_ENDPOINT, APP_NAME

import requests

class Station:
    def __init__(self, station_id: str, name: str, departures: Optional[List[Departure]]=None):
        self.station_id = station_id
        self.name = name
        self.departures = departures

    @classmethod
    def from_dict(cls, data: dict):
        station_id = data["id"]
        name = data["name"]
        departures = [Departure.from_dict(call) for call in data.get("estimatedCalls", [])]
        return cls(station_id, name, departures)

    def __repr__(self):
        return f"Station(id={self.station_id}, name={self.name}, departures={self.departures})"


class GeocodeQuery:
    data: dict
    stations: List[Station]

    def __init__(self, query_text: str, lang: str = "en", layers: str = "venue"):
        self.query_text = query_text
        self.lang = lang
        self.layers = layers

    def get_data(self):
        """Fetch stop places that match the query text."""
        params = {
            "text": self.query_text,
            "lang": self.lang,
            "layers": self.layers,
        }
        headers = {
            "Content-Type": "application/json",
            "ET-Client-Name": APP_NAME
        }

        response = requests.get(GEOCODER_ENDPOINT, params=params, headers=headers)
        response.raise_for_status()
        self.data = response.json()

    def parse_data(self) -> None:
        if not hasattr(self, "data"):
            self.get_data()
        self.stations = []

        for feature in self.data["features"]:
            try:
                stop_id: str = feature["properties"]["id"]
                stop_label: str = feature["properties"]["label"]
            except KeyError as e:
                print(f"Couldn't find key: {e}")
                continue

            if stop_id.startswith("NSR:StopPlace"):
                self.stations.append(Station(stop_id, stop_label))

    def __getitem__(self, i) -> Station:
        if not hasattr(self, "stations"):
            self.parse_data()

        return self.stations[i]


    def __iter__(self):
        if not hasattr(self, "stations"):
            self.parse_data()

        return iter(self.stations)


    def __repr__(self):
        return f"GeocodeQuery(query_text={self.query_text})"

    def __str__(self):
        if not hasattr(self, "data"):
            self.get_data()

        return str(list(iter(self)))


