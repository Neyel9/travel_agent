from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import Optional
import logfire
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_model

logfire.configure(send_to_logfire='if-token-present')

model = get_model()

class TravelDetails(BaseModel):
    """Details for the current trip."""
    response: str = Field(default="", description='The response to give back to the user if they did not give all the necessary details for their trip')
    destination: Optional[str] = Field(default=None, description='Destination city or country')
    origin: Optional[str] = Field(default=None, description='Origin city or country')
    max_hotel_price: Optional[int] = Field(default=None, description='Maximum hotel price per night')
    date_leaving: Optional[str] = Field(default=None, description='Date in format MM-DD')
    date_returning: Optional[str] = Field(default=None, description='Date in format MM-DD')
    all_details_given: bool = Field(default=False, description='True if the user has given all the necessary details, otherwise false')

system_prompt = """
You are a travel planning assistant who helps users plan their trips worldwide.

Your goal is to gather all the necessary details from the user for their trip.

REQUIRED FIELDS (all must have values):
1. destination - where they are going
2. origin - where they are flying from
3. date_leaving - departure date in MM-DD format
4. date_returning - return date in MM-DD format
5. max_hotel_price - maximum hotel price per night (number)

DECISION LOGIC - Follow this exactly:

IF all 5 fields have values (not None, not null, not empty):
- SET all_details_given = True
- SET response = ""
- DO NOT ask for more information

IF any field is missing/None/null/empty:
- SET all_details_given = False
- SET response = ask for missing information

EXAMPLES:

Example 1 - COMPLETE (all_details_given = True):
destination: "Sydney"
origin: "Miami"
date_leaving: "03-05"
date_returning: "03-12"
max_hotel_price: 250
→ all_details_given = True, response = ""

Example 2 - INCOMPLETE (all_details_given = False):
destination: "Paris"
origin: None
date_leaving: "06-15"
date_returning: "06-22"
max_hotel_price: 200
→ all_details_given = False, response = "I need to know where you're flying from."

You can help with travel to ANY location worldwide. Accept any valid city or country name.
"""

info_gathering_agent = Agent(
    model,
    result_type=TravelDetails,
    system_prompt=system_prompt,
    retries=2
)