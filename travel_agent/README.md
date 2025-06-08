# 🌍 Global Travel Planning Agent System

A comprehensive multi-agent travel planning system that helps users plan trips to **anywhere in the world** using real APIs for flights, hotels, and weather data. Built with Pydantic AI and LangGraph, featuring an interactive Streamlit UI with worldwide location support.

![Travel Agent Graph](extras/TravelAgentGraph.png)

## 🌟 Key Features

### 🌍 **Worldwide Location Support**
- **Any destination on Earth**: From Tokyo to Timbuktu, Paris to Patagonia
- **Smart location recognition**: Accepts cities, countries, or "City, Country" format
- **Popular destination suggestions**: Quick-select from 50+ countries and hundreds of cities
- **Real-time location validation**: Ensures your destination exists and is accessible

### 🔗 **Real API Integration**
- **Live weather data**: OpenWeatherMap API for current conditions worldwide
- **Real flight search**: AviationStack API for actual flight availability and pricing
- **Hotel booking data**: RapidAPI Hotels for real accommodation options
- **Graceful fallbacks**: Mock data ensures the system works even without API access

### 🤖 **Intelligent Multi-Agent System**
This project implements a sophisticated travel planning system that uses multiple specialized AI agents working in parallel to create comprehensive travel plans. The system collects user preferences and travel details through a conversational interface, then simultaneously processes flight, hotel, and activity recommendations before combining them into a final travel plan.

All tool calls for the agents are mocked, so this isn't using real data! This is simply built as an example, focusing on the agent architecture instead of the tooling.

## Features

- **Interactive Streamlit UI** with real-time streaming responses
- **Multi-agent architecture** with specialized agents for different aspects of travel planning
- **Parallel processing** of recommendations for improved efficiency
- **User preference management** for airlines, hotel amenities, and budget levels
- **Conversational interface** for gathering travel details
- **Comprehensive travel plans** with flights, accommodations, and activities

## Architecture

The system consists of five specialized agents:

1. **Info Gathering Agent**: Collects necessary travel details (destination, origin, dates, budget)
2. **Flight Agent**: Recommends flights based on travel details and user preferences
3. **Hotel Agent**: Suggests accommodations based on destination, dates, budget, and amenity preferences
4. **Activity Agent**: Recommends activities based on destination, dates, and weather forecasts
5. **Final Planner Agent**: Aggregates all recommendations into a comprehensive travel plan

These agents are orchestrated through a LangGraph workflow that enables parallel execution and dynamic routing based on the completeness of gathered information.

## Technical Stack

- **Pydantic AI**: For structured agent definitions and type validation
- **LangGraph**: For orchestrating the agent workflow and parallel execution
- **Streamlit**: For building the interactive user interface

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- OpenAI or OpenRouter API key (can use Ollama too)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/travel-planning-agent.git
   cd travel-planning-agent
   ```

2. Set up a virtual environment:

   **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```env
   # LLM Configuration
   PROVIDER=OpenRouter
   BASE_URL=https://openrouter.ai/api/v1
   LLM_API_KEY=your_openrouter_api_key
   MODEL_CHOICE=qwen/qwen3-14b:free

   # Real API Keys for Worldwide Travel Data
   WEATHER_API_KEY=your_openweathermap_api_key
   FLIGHT_API_KEY=your_aviationstack_api_key
   HOTEL_API_KEY=your_rapidapi_key
   ```

### 🔑 Getting API Keys (Optional but Recommended)

To enable real worldwide data, get these free API keys:

1. **Weather Data** - [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for free account
   - Get API key from dashboard
   - 1,000 calls/day free tier

2. **Flight Data** - [AviationStack](https://aviationstack.com/)
   - Free tier: 1,000 requests/month
   - Real-time flight information worldwide

3. **Hotel Data** - [RapidAPI Hotels](https://rapidapi.com/apidojo/api/hotels4/)
   - Sign up for RapidAPI account
   - Subscribe to Hotels4 API (free tier available)
   - Global hotel search and pricing

**Note**: The system works without API keys using intelligent mock data, but real APIs provide live, accurate information for any location worldwide.

### Running the Application

1. Start the Streamlit UI:
   ```bash
   streamlit run streamlit_ui.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

### 🧪 Testing API Integration

To verify your API keys are working correctly:

```bash
python test_apis.py
```

This will test:
- ✅ Weather data for multiple cities worldwide
- ✅ Flight search functionality
- ✅ Hotel search capabilities
- ✅ Error handling and fallback systems

The test script shows which APIs are working and provides helpful debugging information.

## 🚀 Usage

### 🌍 **Worldwide Travel Planning**

1. **Choose Your Destination**:
   - Use the sidebar's location selector for popular destinations
   - Or type any city/country in the world in the chat
   - Examples: "Tokyo", "Paris, France", "Bali, Indonesia", "Reykjavik, Iceland"

2. **Set Your Preferences**: Use the sidebar to configure:
   - Preferred airlines
   - Must-have hotel amenities
   - Budget level (budget/mid-range/luxury)

3. **Start Planning**: Type your travel request in natural language:

**Example Destinations Worldwide:**
```
🗾 I want to go to Tokyo, Japan from New York. June 15-22. Hotel budget $200/night.

🗼 Planning a trip to Paris from Los Angeles. July 1-8. Max $300/night for hotels.

🏝️ I want to visit Bali, Indonesia from Chicago. August 10-20. Budget hotels under $150.

🏔️ Trip to Reykjavik, Iceland from Miami. September 5-12. Mid-range accommodations.

🕌 I want to explore Marrakech, Morocco from London. October 1-10. Luxury hotels preferred.

🏛️ Planning to visit Athens, Greece from Toronto. May 15-25. Hotel budget $180/night.
```

3. **Interact with the Agent**: The system will ask follow-up questions if any details are missing.

4. **Review Your Plan**: Once all details are collected, the system will generate a comprehensive travel plan with flight, hotel, and activity recommendations.

Note that with this demonstration, once the final plan is given to you, the conversation is over. This can of course be extended to allow for editing the trip, asking more questions, etc.

## Project Structure

```
travel-planning-agent/
├── agents/                      # Individual agent definitions
│   ├── activity_agent.py        # Agent for recommending activities
│   ├── final_planner_agent.py   # Agent for creating the final travel plan
│   ├── flight_agent.py          # Agent for flight recommendations
│   ├── hotel_agent.py           # Agent for hotel recommendations
│   └── info_gathering_agent.py  # Agent for collecting travel details
├── agent_graph.py               # LangGraph workflow definition
├── streamlit_ui.py              # Streamlit user interface
├── utils.py                     # Utility functions
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## How It Works

1. The system starts by gathering all necessary information from the user through the Info Gathering Agent.
2. Once all required details are collected, the system simultaneously calls the Flight, Hotel, and Activity agents to get recommendations.
3. Each specialized agent uses its tools to search for and recommend options based on the user's preferences.
4. After all recommendations are collected, the Final Planner Agent creates a comprehensive travel plan.
5. The entire process is streamed in real-time to the user through the Streamlit UI.

## Inspired by Anthropic's Agent Architecture

This project is a demonstration of the parallelization workflow showcased in [Anthropic's Agent Architecture blog](https://www.anthropic.com/engineering/building-effective-agents). The implementation follows a similar pattern where multiple specialized agents work in parallel to solve different aspects of a complex task.

![Anthropic Parallelization Workflow](extras/AnthropicParallelizationWorkflow.png)

The key architectural pattern demonstrated here is the ability to:
1. Gather initial information
2. Fan out to multiple specialized agents working in parallel
3. Aggregate results into a final, comprehensive response

This approach significantly improves efficiency compared to sequential processing, especially for complex tasks with independent subtasks.

## Customization

You can customize the system by:

- Modifying agent prompts in the respective agent files
- Adding new specialized agents for additional travel aspects
- Enhancing the tools with real API integrations for flights, hotels, and activities
- Extending the user preference system with additional options

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- Powered by [LangGraph](https://github.com/langchain-ai/langgraph)
- UI created with [Streamlit](https://streamlit.io/)
