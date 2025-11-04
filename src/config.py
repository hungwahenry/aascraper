"""Configuration for AA scraper"""
import random

# Search parameters
ORIGIN = "LAX"
DESTINATION = "JFK"
DEPARTURE_DATE = "12/15/2025"
PASSENGERS = 1

# URLs
AA_HOME_URL = "https://www.aa.com"

# Browser configuration
CHROME_VERSION = 141
WINDOW_SIZE = "1920,1080"

# Timeouts in seconds
TIMEOUT_ELEMENT = 10

# Human-like delays (seconds)
DELAY_TYPING = (0.05, 0.15)
DELAY_ACTION = (1, 2)
DELAY_AFTER_SEARCH = (3, 5)

def random_delay(delay_range):
    """Get random delay from range"""
    return random.uniform(*delay_range)
