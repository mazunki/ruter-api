#!/usr/bin/env python

AUTHOR = "mazunki_dev"
_APP_NAME = "transport_widget"
APP_NAME = f"{AUTHOR}-${_APP_NAME}"

API_ENDPOINT = "https://api.entur.io/journey-planner/v3/graphql"
GEOCODER_ENDPOINT = "https://api.entur.io/geocoder/v1/autocomplete"

def get_cache_dir():
    import os
    return os.path.join(
        os.environ.get("XDG_CACHE_HOME") or
        os.path.join(os.environ["HOME"], ".cache"),
        _APP_NAME
    )


HEADERS = {
    "Content-Type": "application/json",
    "ET-Client-Name": "mazunki_ruter_api-waybar",
}

CACHE_EXPIRATION = 10*60
CACHE_DIR = get_cache_dir()



