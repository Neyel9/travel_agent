from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import requests
import json
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp

load_dotenv()

def get_model():
    provider_name = os.getenv('PROVIDER', 'OpenAI')
    llm = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
    base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
    api_key = os.getenv('LLM_API_KEY', 'no-api-key-provided')

    # Create AsyncOpenAI client based on provider
    if provider_name == 'OpenRouter':
        # OpenRouter configuration with required headers
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",  # Your site URL
                "X-Title": "Travel Agent App"  # Your app name
            }
        )
    elif provider_name == 'OpenAI':
        # Standard OpenAI configuration with rate limiting
        client = AsyncOpenAI(
            api_key=api_key,
            max_retries=3,
            timeout=60.0
        )
    else:
        # Generic configuration for other providers
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            max_retries=3,
            timeout=60.0
        )

    # Create the model using the async client
    return OpenAIModel(
        llm,
        openai_client=client
    )

# API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
FLIGHT_API_SECRET = os.getenv('FLIGHT_API_SECRET')
FLIGHT_API_PROVIDER = os.getenv('FLIGHT_API_PROVIDER', 'amadeus')
HOTEL_API_KEY = os.getenv('HOTEL_API_KEY')
HOTEL_API_PROVIDER = os.getenv('HOTEL_API_PROVIDER', 'rapidapi_booking')

# API Base URLs
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
AMADEUS_BASE_URL = "https://test.api.amadeus.com"
HOTEL_BASE_URL = "https://booking-com.p.rapidapi.com"

async def get_weather_data(city: str, country_code: str = None) -> Dict[str, Any]:
    """Get weather data for a city using OpenWeatherMap API."""
    if not WEATHER_API_KEY:
        return {"error": "Weather API key not configured"}

    try:
        location = f"{city},{country_code}" if country_code else city
        url = f"{WEATHER_BASE_URL}/weather"
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'country': data['sys']['country'],
                        'city': data['name']
                    }
                else:
                    return {"error": f"Weather API error: {response.status}"}
    except Exception as e:
        return {"error": f"Weather API request failed: {str(e)}"}

async def get_amadeus_token() -> str:
    """Get access token for Amadeus API."""
    if not FLIGHT_API_KEY or not FLIGHT_API_SECRET:
        return None

    try:
        url = f"{AMADEUS_BASE_URL}/v1/security/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': FLIGHT_API_KEY,
            'client_secret': FLIGHT_API_SECRET
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return token_data.get('access_token')
                else:
                    return None
    except Exception:
        return None

async def search_flights_api(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """Search for flights using Amadeus API."""
    if not FLIGHT_API_KEY or not FLIGHT_API_SECRET:
        return [{"error": "Flight API credentials not configured"}]

    try:
        # Get access token
        access_token = await get_amadeus_token()
        if not access_token:
            return [{"error": "Failed to authenticate with Amadeus API"}]

        # Search for flights
        url = f"{AMADEUS_BASE_URL}/v2/shopping/flight-offers"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Format date for Amadeus (YYYY-MM-DD)
        import datetime
        try:
            if len(date.split('-')) == 2:
                month, day = date.split('-')
                current_year = datetime.datetime.now().year
                formatted_date = f"{current_year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                formatted_date = date
        except:
            formatted_date = "2025-03-05"  # Default date

        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': formatted_date,
            'adults': 1,
            'max': 5
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data and data['data']:
                        flights = []
                        for offer in data['data'][:5]:
                            itinerary = offer['itineraries'][0]
                            segment = itinerary['segments'][0]
                            price = offer['price']

                            flights.append({
                                'airline': segment['carrierCode'],
                                'flight_number': f"{segment['carrierCode']}{segment['number']}",
                                'departure_time': segment['departure']['at'],
                                'arrival_time': segment['arrival']['at'],
                                'origin': segment['departure']['iataCode'],
                                'destination': segment['arrival']['iataCode'],
                                'price': f"{price['total']} {price['currency']}",
                                'direct': len(itinerary['segments']) == 1
                            })
                        return flights
                    else:
                        return [{"error": "No flight data available"}]
                else:
                    return [{"error": f"Flight API error: {response.status}"}]
    except Exception as e:
        return [{"error": f"Flight API request failed: {str(e)}"}]

async def search_hotels_api(city: str, check_in: str, check_out: str, adults: int = 2) -> List[Dict[str, Any]]:
    """Search for hotels using RapidAPI Booking.com API."""
    if not HOTEL_API_KEY:
        return [{"error": "Hotel API key not configured"}]

    try:
        # Use RapidAPI Booking.com API
        search_url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
        headers = {
            "X-RapidAPI-Key": HOTEL_API_KEY,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }

        # Format dates for Booking.com API (YYYY-MM-DD)
        import datetime
        try:
            # Convert MM-DD to YYYY-MM-DD (assuming current year)
            current_year = datetime.datetime.now().year
            if len(check_in.split('-')) == 2:
                month, day = check_in.split('-')
                check_in = f"{current_year}-{month.zfill(2)}-{day.zfill(2)}"
            if len(check_out.split('-')) == 2:
                month, day = check_out.split('-')
                check_out = f"{current_year}-{month.zfill(2)}-{day.zfill(2)}"
        except:
            # If date parsing fails, use default dates
            check_in = f"{current_year}-03-05"
            check_out = f"{current_year}-03-12"

        search_params = {
            "dest_type": "city",
            "dest_id": "-1456928",  # Default to Sydney (will be dynamic later)
            "search_type": "city",
            "arrival_date": check_in,
            "departure_date": check_out,
            "adults": adults,
            "room_qty": 1,
            "page_number": 1,
            "units": "metric",
            "temperature_unit": "c",
            "languagecode": "en-us",
            "currency_code": "USD"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=search_params) as response:
                if response.status == 200:
                    hotels_data = await response.json()
                    hotels = []

                    # Parse Booking.com API response
                    if 'result' in hotels_data:
                        properties = hotels_data['result'][:5]  # Get first 5 hotels
                        for prop in properties:
                            # Extract hotel information
                            hotel_info = {
                                'name': prop.get('hotel_name', 'Unknown Hotel'),
                                'price_per_night': prop.get('min_total_price', 'N/A'),
                                'currency': prop.get('currency_code', 'USD'),
                                'rating': prop.get('review_score', 'N/A'),
                                'location': prop.get('district', city),
                                'amenities': prop.get('hotel_facilities', [])[:4] if prop.get('hotel_facilities') else ['WiFi', 'Reception']
                            }
                            hotels.append(hotel_info)

                    return hotels if hotels else [{"error": "No hotels found"}]
                else:
                    return [{"error": f"Hotel search API error: {response.status}"}]
    except Exception as e:
        return [{"error": f"Hotel API request failed: {str(e)}"}]

def get_country_suggestions() -> List[str]:
    """Get a list of popular countries for travel."""
    return [
        "United States", "United Kingdom", "France", "Germany", "Italy", "Spain",
        "Japan", "Australia", "Canada", "Brazil", "India", "China", "Thailand",
        "Greece", "Turkey", "Egypt", "South Africa", "Mexico", "Argentina",
        "Netherlands", "Switzerland", "Austria", "Portugal", "Norway", "Sweden",
        "Denmark", "Belgium", "Ireland", "New Zealand", "Singapore", "Malaysia",
        "Indonesia", "Philippines", "Vietnam", "South Korea", "Russia", "Poland",
        "Czech Republic", "Hungary", "Croatia", "Morocco", "Israel", "UAE",
        "Qatar", "Chile", "Peru", "Colombia", "Costa Rica", "Iceland"
    ]

def get_popular_cities() -> Dict[str, List[str]]:
    """Get popular cities by country."""
    return {
        "United States": ["New York", "Los Angeles", "Chicago", "Miami", "Las Vegas", "San Francisco", "Boston", "Seattle"],
        "United Kingdom": ["London", "Edinburgh", "Manchester", "Liverpool", "Bath", "Oxford", "Cambridge"],
        "France": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Strasbourg", "Toulouse"],
        "Germany": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Dresden", "Heidelberg"],
        "Italy": ["Rome", "Milan", "Venice", "Florence", "Naples", "Turin", "Bologna"],
        "Spain": ["Madrid", "Barcelona", "Seville", "Valencia", "Bilbao", "Granada", "Toledo"],
        "Japan": ["Tokyo", "Osaka", "Kyoto", "Hiroshima", "Yokohama", "Kobe", "Nara"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Quebec City"],
        "Brazil": ["Rio de Janeiro", "São Paulo", "Salvador", "Brasília", "Recife", "Fortaleza"],
        "India": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"],
        "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou", "Xi'an"],
        "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Krabi", "Koh Samui"],
        "Greece": ["Athens", "Thessaloniki", "Mykonos", "Santorini", "Rhodes", "Crete"],
        "Turkey": ["Istanbul", "Ankara", "Antalya", "Izmir", "Cappadocia", "Bodrum"],
        "Egypt": ["Cairo", "Alexandria", "Luxor", "Aswan", "Hurghada", "Sharm El Sheikh"],
        "Mexico": ["Mexico City", "Cancun", "Guadalajara", "Puerto Vallarta", "Playa del Carmen", "Tulum"]
    }