from crewai import Agent, LLM
from crewai_tools import SerperDevTool # Google Search tool
from dotenv import load_dotenv
import os
import time
from litellm import RateLimitError

load_dotenv()


def safe_llm_call(llm, **kwargs):
    while True:
        try:
            return llm(**kwargs)
        except RateLimitError as e:
            wait_time = 6
            import re
            match = re.search(r"try again in ([\d\.]+)s", str(e))
            if match:
                wait_time = float(match.group(1))
            print(f"Rate limit hit, retrying in {wait_time} seconds...")
            time.sleep(wait_time)

# Example: wrap your LLM instance
llm = LLM(
    model="groq/gemini/gemini-2.5-flash",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0
)

# Defining the search tool
search_tool = SerperDevTool()

# RESEARCH AGENT
research_agent = Agent(
    role = "Travel Researcher",
    goal = (
        """
        Research the destination using current web information 
        and identify useful tourist attractions, activities, 
        food experiences, travel information, prices and 
        opening hours.
        """
    ),
    backstory = (
        """ 
        You are an experienced travel researcher.
        You use web search to find current and reliable 
        travel information. You carefully compare search 
        results and avoid presenting unsupported information as fact.
        """
    ),
    tools = [search_tool],
    llm = llm,
    verbose = True,
 #  allow_delegation = False, -> whether the ai agent assign the task to other agents
    max_iter = 3,
    max_rpm=2,
)

# BUDGET AGENT
budget_agent = Agent(
    role = "Travel Budget Planner",
    goal = (""" 
        Create a realistic travel budget based on the 
        destination, number of days and user's maximum budget.
        """),
    backstory = (
        """ 
        You are a professional travel budget planner. 
        You specialize in creating affordable and practical
        travel budgets. You use the researcher's information
        to estimate realistic expenses.
        """
    ),
    llm = llm,
    verbose = True,
    max_iter = 3,
    max_rpm=2
)

# TRAVEL PLANNER AGENT
planner_agent = Agent(
    role = "Travel Itinerary Planner",
    goal = ("""
        Create a complete day-by-day itinerary using the 
        latest travel research and the calculated budget.
        """
    ),
    backstory = (""" 
        You are an expert travel planner. You combine 
        current travel information, tourist attractions, 
        activities and budget information into a practical 
        and enjoyable itinerary."""
    ),
    llm = llm,
    verbose = True,
    max_iter = 3,
    max_rpm=2,
)

