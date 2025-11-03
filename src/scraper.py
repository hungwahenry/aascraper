# -*- coding: utf-8 -*-
"""AA.com flight scraper with Selenium"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.browser import wait_for_element, wait_for_clickable
from src.config import (
    AA_HOME_URL, ORIGIN, DESTINATION, DEPARTURE_DATE,
    random_delay, DELAY_ACTION, DELAY_TYPING, DELAY_AFTER_SEARCH
)

def human_type(element, text):
    """Type text with human-like delays"""
    for char in text:
        element.send_keys(char)
        time.sleep(random_delay(DELAY_TYPING))

def fill_search_form(driver, redeem_miles=False):
    """Fill out AA.com search form

    Args:
        driver: Selenium WebDriver
        redeem_miles: If True, check the "Redeem miles" box for award pricing
    """
    print(f"[FORM] Filling search form (redeem_miles={redeem_miles})...")

    # Click "One way" radio button - click the label instead of hidden input
    one_way_label = wait_for_clickable(driver, 'label[for="flightSearchForm.tripType.oneWay"]')
    if one_way_label:
        one_way_label.click()
        time.sleep(random_delay(DELAY_ACTION))

    # Check "Redeem miles" if award pricing - click the label
    if redeem_miles:
        redeem_label = wait_for_clickable(driver, 'label[for="flightSearchForm.tripType.redeemMiles"]')
        if redeem_label:
            redeem_label.click()
            time.sleep(random_delay(DELAY_ACTION))

    # Select 1 passenger (should be default, but let's be explicit)
    from selenium.webdriver.support.ui import Select
    try:
        passenger_select = Select(driver.find_element(By.ID, 'flightSearchForm.adultOrSeniorPassengerCount'))
        passenger_select.select_by_value('1')
        time.sleep(0.5)
    except:
        pass  # Already selected

    # Fill origin
    origin_input = wait_for_element(driver, '#reservationFlightSearchForm\\.originAirport')
    if origin_input:
        origin_input.click()
        time.sleep(0.5)
        origin_input.clear()
        origin_input.send_keys(ORIGIN)
        time.sleep(1)  # Wait for autocomplete
        origin_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.3)
        origin_input.send_keys(Keys.ENTER)
        time.sleep(random_delay(DELAY_ACTION))

    # Fill destination
    dest_input = wait_for_element(driver, '#reservationFlightSearchForm\\.destinationAirport')
    if dest_input:
        dest_input.click()
        time.sleep(0.5)
        dest_input.clear()
        dest_input.send_keys(DESTINATION)
        time.sleep(1)  # Wait for autocomplete
        dest_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.3)
        dest_input.send_keys(Keys.ENTER)
        time.sleep(random_delay(DELAY_ACTION))

    # Fill date
    date_input = wait_for_element(driver, '#aa-leavingOn')
    if date_input:
        date_input.click()
        time.sleep(0.3)
        date_input.clear()
        date_input.send_keys(DEPARTURE_DATE)
        time.sleep(random_delay(DELAY_ACTION))

    # Click search
    print("[SEARCH] Clicking search button...")
    search_button = wait_for_clickable(driver, '#flightSearchForm\\.button\\.reSubmit')
    if search_button:
        search_button.click()

    # Wait for navigation to results
    time.sleep(random_delay(DELAY_AFTER_SEARCH))

def extract_flight_data(driver, is_award=False):
    """Extract flight data from results page

    Args:
        driver: Selenium WebDriver
        is_award: True if scraping award pricing, False for cash pricing
    """
    print("[EXTRACT] Extracting flight data...")

    # Wait for flights to load
    flight_buttons = wait_for_element(driver, 'button.btn-flight', timeout=15)
    if not flight_buttons:
        print("[WARN] No flights found or page didn't load")
        return []

    # Different selectors for cash vs award pricing
    if is_award:
        # Award pricing: grid-x grid-padding-x
        flight_rows = driver.find_elements(By.CSS_SELECTOR, 'div.grid-x.grid-padding-x')
    else:
        # Cash pricing: app-slice-details
        flight_rows = driver.find_elements(By.CSS_SELECTOR, 'app-slice-details')

    print(f"[DEBUG] Found {len(flight_rows)} flight rows")
    flights = []

    for i, row in enumerate(flight_rows):
        try:
            if is_award:
                # Award pricing selectors
                dep_time = row.find_element(By.CSS_SELECTOR, '.origin .flt-times').text.strip()
                arr_time = row.find_element(By.CSS_SELECTOR, '.destination .flt-times').text.strip()
                duration = row.find_element(By.CSS_SELECTOR, '.duration').text.strip()

                # Get Main cabin award price (product0)
                main_button = row.find_element(By.CSS_SELECTOR, 'button.btn-flight[id*="product0"]')
                price_amount = main_button.find_element(By.CSS_SELECTOR, '.per-pax-amount').text

                try:
                    price_addon = main_button.find_element(By.CSS_SELECTOR, '.per-pax-addon').text
                except:
                    price_addon = ""

                price_text = f"{price_amount} {price_addon}".strip()
            else:
                # Cash pricing selectors
                time_elem = row.find_element(By.CSS_SELECTOR, '.origin .time').text.strip()
                meridiem = row.find_element(By.CSS_SELECTOR, '.origin .meridiem').text.strip()
                dep_time = f"{time_elem} {meridiem}"

                time_elem = row.find_element(By.CSS_SELECTOR, '.destination .time').text.strip()
                meridiem = row.find_element(By.CSS_SELECTOR, '.destination .meridiem').text.strip()
                arr_time = f"{time_elem} {meridiem}"

                duration = row.find_element(By.CSS_SELECTOR, '.duration').text.strip()

                # Get Main cabin cash price
                main_button = row.find_element(By.CSS_SELECTOR, 'button.btn-flight.MAIN')
                price_text = main_button.find_element(By.CSS_SELECTOR, '.per-pax-amount').text.strip()

            flights.append({
                "departure_time": dep_time,
                "arrival_time": arr_time,
                "duration": duration,
                "price": price_text
            })

            print(f"[FLIGHT {i+1}] {dep_time} -> {arr_time} | {duration} | {price_text}")
        except Exception as e:
            print(f"[WARN] Error extracting flight {i}: {e}")
            continue

    print(f"[SUCCESS] Extracted {len(flights)} flights")
    return flights

def scrape_flights(driver, redeem_miles=False):
    """Main scraping function

    Args:
        driver: Selenium WebDriver
        redeem_miles: If True, scrape award prices; if False, scrape cash prices
    """
    mode = "award" if redeem_miles else "cash"
    print(f"\n{'='*60}")
    print(f"[START] Starting {mode.upper()} price scrape")
    print(f"{'='*60}")

    # Navigate to homepage
    print(f"[NAV] Navigating to {AA_HOME_URL}...")
    driver.get(AA_HOME_URL)

    # Wait for page to load
    time.sleep(random_delay(DELAY_AFTER_SEARCH))

    # Fill and submit search form
    fill_search_form(driver, redeem_miles=redeem_miles)

    # Extract flight data from results
    flights = extract_flight_data(driver, is_award=redeem_miles)

    print(f"[COMPLETE] {mode.upper()} scrape complete")
    return flights

def scrape_both_prices(driver):
    """Scrape both cash and award prices"""
    # Scrape cash prices
    cash_flights = scrape_flights(driver, redeem_miles=False)

    # Scrape award prices
    award_flights = scrape_flights(driver, redeem_miles=True)

    return {
        "cash": cash_flights,
        "award": award_flights
    }
