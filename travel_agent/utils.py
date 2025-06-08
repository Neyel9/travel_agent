from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
import os
import requests
import json
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp

load_dotenv()

def get_model():
    llm = os.getenv('MODEL_CHOICE', 'qwen/qwen3-14b:free')
    base_url = os.getenv('BASE_URL', 'https://openrouter.ai/api/v1')
    api_key = os.getenv('LLM_API_KEY', 'no-api-key-provided')

    return OpenAIModel(
        llm,
        base_url=base_url,
        api_key=api_key
    )

# API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
HOTEL_API_KEY = os.getenv('HOTEL_API_KEY')

# API Base URLs
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
FLIGHT_BASE_URL = "http://api.aviationstack.com/v1"
HOTEL_BASE_URL = "https://hotels4.p.rapidapi.com"

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

async def search_flights_api(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """Search for flights using AviationStack API."""
    if not FLIGHT_API_KEY:
        return [{"error": "Flight API key not configured"}]

    try:
        url = f"{FLIGHT_BASE_URL}/flights"
        params = {
            'access_key': FLIGHT_API_KEY,
            'dep_iata': origin,
            'arr_iata': destination,
            'flight_date': date,
            'limit': 10
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data:
                        flights = []
                        for flight in data['data'][:5]:  # Limit to 5 results
                            flights.append({
                                'airline': flight.get('airline', {}).get('name', 'Unknown'),
                                'flight_number': flight.get('flight', {}).get('number', 'N/A'),
                                'departure_time': flight.get('departure', {}).get('scheduled', 'N/A'),
                                'arrival_time': flight.get('arrival', {}).get('scheduled', 'N/A'),
                                'origin': flight.get('departure', {}).get('airport', 'N/A'),
                                'destination': flight.get('arrival', {}).get('airport', 'N/A'),
                                'status': flight.get('flight_status', 'N/A')
                            })
                        return flights
                    else:
                        return [{"error": "No flight data available"}]
                else:
                    return [{"error": f"Flight API error: {response.status}"}]
    except Exception as e:
        return [{"error": f"Flight API request failed: {str(e)}"}]

async def search_hotels_api(city: str, check_in: str, check_out: str, adults: int = 2) -> List[Dict[str, Any]]:
    """Search for hotels using RapidAPI Hotels API."""
    if not HOTEL_API_KEY:
        return [{"error": "Hotel API key not configured"}]

    try:
        # First, get destination ID
        search_url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        headers = {
            "X-RapidAPI-Key": HOTEL_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        search_params = {"q": city}

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=search_params) as response:
                if response.status == 200:
                    search_data = await response.json()
                    if 'sr' in search_data and len(search_data['sr']) > 0:
                        destination_id = search_data['sr'][0].get('gaiaId')

                        if destination_id:
                            # Now search for hotels
                            hotels_url = "https://hotels4.p.rapidapi.com/properties/v2/list"
                            hotels_params = {
                                "destination": {"regionId": destination_id},
                                "checkInDate": {"day": int(check_in.split('-')[2]), "month": int(check_in.split('-')[1]), "year": int(check_in.split('-')[0])},
                                "checkOutDate": {"day": int(check_out.split('-')[2]), "month": int(check_out.split('-')[1]), "year": int(check_out.split('-')[0])},
                                "rooms": [{"adults": adults}],
                                "resultsStartingIndex": 0,
                                "resultsSize": 5,
                                "sort": "PRICE_LOW_TO_HIGH"
                            }

                            async with session.post(hotels_url, headers=headers, json=hotels_params) as hotels_response:
                                if hotels_response.status == 200:
                                    hotels_data = await hotels_response.json()
                                    hotels = []
                                    if 'data' in hotels_data and 'propertySearch' in hotels_data['data']:
                                        properties = hotels_data['data']['propertySearch'].get('properties', [])
                                        for prop in properties[:5]:
                                            hotels.append({
                                                'name': prop.get('name', 'Unknown Hotel'),
                                                'price_per_night': prop.get('price', {}).get('lead', {}).get('amount', 'N/A'),
                                                'currency': prop.get('price', {}).get('lead', {}).get('currencyInfo', {}).get('code', 'USD'),
                                                'rating': prop.get('reviews', {}).get('score', 'N/A'),
                                                'location': prop.get('neighborhood', {}).get('name', city),
                                                'amenities': [amenity.get('text', '') for amenity in prop.get('amenities', {}).get('topAmenities', {}).get('items', [])][:4]
                                            })
                                    return hotels if hotels else [{"error": "No hotels found"}]
                                else:
                                    return [{"error": f"Hotels search API error: {hotels_response.status}"}]
                        else:
                            return [{"error": "Could not find destination"}]
                    else:
                        return [{"error": "Location not found"}]
                else:
                    return [{"error": f"Location search API error: {response.status}"}]
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