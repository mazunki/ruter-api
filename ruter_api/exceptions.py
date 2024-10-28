#!/usr/bin/env python

class RuterAPIError(Exception):
    """Base exception for Ruter API errors"""
    pass

class StopNotFoundError(RuterAPIError):
    """Raised when no stops are found near a location"""
    pass

