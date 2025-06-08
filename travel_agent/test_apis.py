#!/usr/bin/env python3
"""
Test script to verify API integrations work correctly.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from utils import get_weather_data, search_flights_api, search_hotels_api

async def test_weather_api():
    """Test the weather API integration."""
    print("🌤️  Testing Weather API...")
    
    test_cities = ["Tokyo", "Paris", "New York", "Sydney", "InvalidCity123"]
    
    for city in test_cities:
        print(f"\n📍 Testing weather for: {city}")
        try:
            weather_data = await get_weather_data(city)
            if 'error' in weather_data:
                print(f"   ❌ Error: {weather_data['error']}")
            else:
                print(f"   ✅ Temperature: {weather_data.get('temperature', 'N/A')}°C")
                print(f"   ✅ Description: {weather_data.get('description', 'N/A')}")
                print(f"   ✅ Country: {weather_data.get('country', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

async def test_flight_api():
    """Test the flight API integration."""
    print("\n✈️  Testing Flight API...")
    
    test_routes = [
        ("JFK", "NRT", "2024-06-15"),  # New York to Tokyo
        ("LAX", "CDG", "2024-07-01"),  # Los Angeles to Paris
        ("XXX", "YYY", "2024-01-01"),  # Invalid route
    ]
    
    for origin, destination, date in test_routes:
        print(f"\n📍 Testing flight: {origin} → {destination} on {date}")
        try:
            flight_data = await search_flights_api(origin, destination, date)
            if flight_data and len(flight_data) > 0:
                if 'error' in flight_data[0]:
                    print(f"   ❌ Error: {flight_data[0]['error']}")
                else:
                    print(f"   ✅ Found {len(flight_data)} flights")
                    for i, flight in enumerate(flight_data[:2]):  # Show first 2
                        print(f"   ✅ Flight {i+1}: {flight.get('airline', 'N/A')} - {flight.get('flight_number', 'N/A')}")
            else:
                print("   ❌ No flight data returned")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

async def test_hotel_api():
    """Test the hotel API integration."""
    print("\n🏨 Testing Hotel API...")
    
    test_searches = [
        ("Tokyo", "2024-06-15", "2024-06-22"),
        ("Paris", "2024-07-01", "2024-07-08"),
        ("InvalidCity123", "2024-01-01", "2024-01-02"),
    ]
    
    for city, check_in, check_out in test_searches:
        print(f"\n📍 Testing hotels in: {city} ({check_in} to {check_out})")
        try:
            hotel_data = await search_hotels_api(city, check_in, check_out)
            if hotel_data and len(hotel_data) > 0:
                if 'error' in hotel_data[0]:
                    print(f"   ❌ Error: {hotel_data[0]['error']}")
                else:
                    print(f"   ✅ Found {len(hotel_data)} hotels")
                    for i, hotel in enumerate(hotel_data[:2]):  # Show first 2
                        print(f"   ✅ Hotel {i+1}: {hotel.get('name', 'N/A')} - ${hotel.get('price_per_night', 'N/A')}/night")
            else:
                print("   ❌ No hotel data returned")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

async def main():
    """Run all API tests."""
    print("🧪 Starting API Integration Tests...")
    print("=" * 50)
    
    # Check if API keys are configured
    weather_key = os.getenv('WEATHER_API_KEY')
    flight_key = os.getenv('FLIGHT_API_KEY')
    hotel_key = os.getenv('HOTEL_API_KEY')
    
    print(f"🔑 Weather API Key: {'✅ Configured' if weather_key else '❌ Missing'}")
    print(f"🔑 Flight API Key: {'✅ Configured' if flight_key else '❌ Missing'}")
    print(f"🔑 Hotel API Key: {'✅ Configured' if hotel_key else '❌ Missing'}")
    print()
    
    # Run tests
    await test_weather_api()
    await test_flight_api()
    await test_hotel_api()
    
    print("\n" + "=" * 50)
    print("🏁 API Integration Tests Complete!")
    print("\n💡 Note: If APIs return errors, the system will fall back to mock data.")
    print("💡 This ensures your travel agent works even without API access!")

if __name__ == "__main__":
    asyncio.run(main())
