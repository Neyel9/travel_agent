# 🚀 Quick Start Guide - AI Travel Agent

Get your worldwide travel agent running in 5 minutes!

## ⚡ Super Quick Setup

```bash
# 1. Run the setup script
python setup_travel_agent.py

# 2. Start the travel agent
cd travel_agent
streamlit run streamlit_ui.py

# 3. Open your browser to http://localhost:8501
```

That's it! 🎉

---

## 🔧 Manual Setup (if needed)

### 1. Install Dependencies
```bash
cd travel_agent
pip install -r requirements.txt
pip install aiohttp
```

### 2. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys (optional)
nano .env
```

### 3. Test Everything
```bash
# Test API integration
python test_apis.py

# Start the web interface
streamlit run streamlit_ui.py
```

---

## 🌍 Try These Examples

Once running, try these in the chat:

```
🗾 "I want to go to Tokyo from New York, June 15-22, hotel budget $200/night"

🗼 "Plan a trip to Paris from LA, July 1-8, luxury hotels preferred"

🏝️ "Family vacation to Bali from Chicago, August 10-20, need pool"

🏔️ "Adventure trip to Iceland from Miami, September 5-12"

🕌 "Business trip to Dubai from London, October 1-5, 5-star hotels"
```

---

## 🔑 API Keys (Optional)

For real worldwide data, get these free API keys:

| Service | Link | Free Tier |
|---------|------|-----------|
| OpenWeatherMap | [Get Key](https://openweathermap.org/api) | 1,000 calls/day |
| AviationStack | [Get Key](https://aviationstack.com/) | 1,000 calls/month |
| RapidAPI Hotels | [Get Key](https://rapidapi.com/apidojo/api/hotels4/) | Free tier available |

Add them to `travel_agent/.env`:
```env
WEATHER_API_KEY=your_key_here
FLIGHT_API_KEY=your_key_here  
HOTEL_API_KEY=your_key_here
```

---

## 🛠️ CLI Tools (Extras)

Test individual agents:

```bash
# Test flight agent
cd extras
python cli-sync.py

# Test with streaming
python flight-cli.py

# Test info gathering
python info_gathering_cli.py
```

---

## 🚨 Troubleshooting

### Dependencies Issues
```bash
# If requirements.txt fails
pip install pydantic-ai streamlit aiohttp python-dotenv

# If import errors
pip install --upgrade pydantic-ai langgraph
```

### Port Already in Use
```bash
# Use different port
streamlit run streamlit_ui.py --server.port 8502
```

### API Errors
- The system works without API keys using smart mock data
- Check `travel_agent/.env` for correct API key format
- Run `python test_apis.py` to verify API status

---

## 🎯 What's Next?

1. **Customize Preferences** → Use the sidebar to set airlines, amenities, budget
2. **Try Different Destinations** → The agent works for ANY location worldwide
3. **Explore CLI Tools** → Test individual agents in the `extras/` folder
4. **Add More APIs** → Extend with car rentals, restaurants, tours

---

**Happy travels! ✈️🌍**
