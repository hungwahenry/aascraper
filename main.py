"""AA Flight Scraper - Main entry point"""
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from src.browser import create_undetected_driver
from src.scraper import scrape_both_prices
from src.calculator import match_and_calculate

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("  AA FLIGHT SCRAPER - Cash vs Award Price Comparison")
    print("="*60 + "\n")

    driver = None

    try:
        print("Setting up browser...")
        driver = create_undetected_driver(headless=False)

        data = scrape_both_prices(driver)

        print("\nCalculating CPP values...")
        output = match_and_calculate(data['cash'], data['award'])

        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        for flight in output['flights']:
            print(f"\nFlight {flight['flight_number']}")
            print(f"   Departure: {flight['departure_time']}")
            print(f"   Arrival: {flight['arrival_time']}")
            print(f"   Cash Price: ${flight['cash_price_usd']:.2f}")
            print(f"   Award: {flight['points_required']:,} pts + ${flight['taxes_fees_usd']:.2f}")
            print(f"   CPP: {flight['cpp']:.2f}c")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"\nResults saved to: {output_file}")
        print(f"Total flights found: {output['total_results']}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
