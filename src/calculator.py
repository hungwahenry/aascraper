# -*- coding: utf-8 -*-
"""CPP (Cents Per Point) calculator"""
import re

def parse_price(price_str: str):
    """Parse price string to extract dollar amount"""
    match = re.search(r'\$?([\d,]+\.?\d*)', price_str)
    if match:
        return float(match.group(1).replace(',', ''))
    return 0.0

def parse_award_price(price_str: str):
    """Parse award price string to extract points and taxes"""
    # Extract points (handles "35k" or "35,000")
    points_match = re.search(r'([\d,]+)k?', price_str)
    if not points_match:
        return None, None

    points_str = points_match.group(1).replace(',', '')
    # If it has 'k', multiply by 1000
    if 'k' in price_str.lower():
        points = float(points_str) * 1000
    else:
        points = float(points_str)

    # Extract taxes/fees
    taxes_match = re.search(r'\$\s*([\d,]+\.?\d*)', price_str)
    taxes = float(taxes_match.group(1).replace(',', '')) if taxes_match else 0.0

    return int(points), taxes

def calculate_cpp(cash_price: float, points: int, taxes: float):
    """Calculate Cents Per Point (CPP)

    Formula: (cash_price - taxes_fees) / points_required * 100
    """
    if points == 0:
        return 0.0

    cpp = ((cash_price - taxes) / points) * 100
    return round(cpp, 2)

def match_and_calculate(cash_flights: list, award_flights: list):
    """Match cash and award flights, calculate CPP, return final output format"""
    from src.config import ORIGIN, DESTINATION, DEPARTURE_DATE, PASSENGERS

    flights = []

    for i, (cash, award) in enumerate(zip(cash_flights, award_flights)):
        cash_price = parse_price(cash.get('price', ''))
        points, taxes = parse_award_price(award.get('price', ''))

        if points and cash_price:
            cpp = calculate_cpp(cash_price, points, taxes)

            # Format flight number (remove AA prefix if exists, then add it)
            flight_num = cash.get('flight_number', 'N/A').replace('AA', '').strip()

            flights.append({
                "is_nonstop": cash.get('is_nonstop', True),
                "segments": [
                    {
                        "flight_number": f"AA{flight_num}" if flight_num != 'N/A' else f"AA{i + 1}",
                        "departure_time": cash.get('departure_time'),
                        "arrival_time": cash.get('arrival_time')
                    }
                ],
                "total_duration": cash.get('duration'),
                "points_required": points,
                "cash_price_usd": cash_price,
                "taxes_fees_usd": taxes,
                "cpp": cpp
            })

    # Convert date format from MM/DD/YYYY to YYYY-MM-DD
    date_parts = DEPARTURE_DATE.split('/')
    formatted_date = f"{date_parts[2]}-{date_parts[0].zfill(2)}-{date_parts[1].zfill(2)}"

    return {
        "search_metadata": {
            "origin": ORIGIN,
            "destination": DESTINATION,
            "date": formatted_date,
            "passengers": PASSENGERS,
            "cabin_class": "economy"
        },
        "flights": flights,
        "total_results": len(flights)
    }
