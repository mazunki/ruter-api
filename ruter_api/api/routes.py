#!/usr/bin/env python

class Route:
    def __init__(self, line_id: str, name: str, transport_mode: str):
        self.line_id = line_id
        self.name = name
        self.transport_mode = transport_mode

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            line_id=data["id"],
            name=data["name"],
            transport_mode=data["transportMode"]
        )

    def __repr__(self):
        return f"Route(line_id={self.line_id}, name={self.name}, transport_mode={self.transport_mode})"

    @property
    def line_number(self):
        return self.line_id.rpartition(":")[-1]

    @property
    def transport_icon(self):
        if self.transport_mode == "metro":
            return "🚇"

        elif self.transport_mode == "bus":
            return "🚌"

        elif self.transport_mode == "tram":
            return "🚊"

        elif self.transport_mode == "water":
            return "⛴"

        else:
            return self.transport_mode

