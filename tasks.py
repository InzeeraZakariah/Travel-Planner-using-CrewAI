from crewai import Task

from agents import research_agent, budget_agent, planner_agent


# RESEARCH TASK
research_task = Task(
    description="""
    Research current travel information for {destination}.
    The user wants to travel for {days} days.
    Use the web search tool to find current information.

    Search for:
        1. Best tourist attractions in {destination}
        2. Popular activities
        3. Local experiences
        4. Popular food
        5. Approximate entry fees where available
        6. Opening hours where available
        7. Recommended areas for accommodation
        8. Local transportation information
        9. Important travel tips
        10. Any important current travel information

    Prefer reliable and recent sources.

    Do not invent prices, opening hours or other current
    information.

    If exact information cannot be verified, clearly state
    that it needs to be checked before travelling.

    The user has a maximum budget of ₹{budget}.
    Therefore, prioritize affordable options.
    """,

    expected_output="""
    A structured travel research report containing:
    DESTINATION OVERVIEW

    TOURIST ATTRACTIONS
    - Name
    - Description
    - Approximate entry fee if available
    - Opening hours if available

    ACTIVITIES
    - Activity
    - Approximate cost if available

    FOOD
    - Popular local foods
    - Recommended food experiences

    ACCOMMODATION
    - Recommended areas
    - Approximate price range if available

    TRANSPORTATION
    - Local transportation options
    - Approximate costs if available

    TRAVEL TIPS

    SOURCES
    - Include the URLs or source names used during research.
    """,

    agent=research_agent
)


# BUDGET TASK
budget_task = Task(
    description="""
    Create a realistic budget for a {days}-day trip
    to {destination}.

    The user's maximum budget is ₹{budget}.

    Use the research provided by the Research Agent.

    Divide the budget into:

    - Accommodation
    - Food
    - Local transportation
    - Tourist attractions
    - Activities
    - Miscellaneous expenses

    Make the plan affordable.

    The total estimated cost must not exceed
    ₹{budget}.

    If exact prices are unavailable, clearly label
    the values as estimates.
    """,

    expected_output="""
    A clear budget breakdown containing:

    Accommodation: ₹...
    Food: ₹...
    Transportation: ₹...
    Attractions: ₹...
    Activities: ₹...
    Miscellaneous: ₹...

    Total Estimated Cost: ₹...

    Also mention whether the trip fits within
    the user's maximum budget.
    """,

    agent=budget_agent,
    context=[research_task]
)


# TRAVEL PLANNING TASK
planning_task = Task(
    description="""
    Create a complete {days}-day travel itinerary
    for {destination}.

    Maximum budget: ₹{budget}.

    Use the research from the Research Agent and
    budget from the Budget Agent.

    Create a practical day-by-day plan.

    For each day include:

    - Morning activities
    - Afternoon activities
    - Evening activities
    - Places to visit
    - Food suggestions
    - Approximate daily expense

    Also include:

    - Total estimated budget
    - Important opening-hour considerations
    - Important travel tips
    - Sources used for current information

    Do not exceed the user's budget.

    Do not present uncertain information as confirmed fact.
    """,

    expected_output="""
    A complete travel itinerary in this format:

    ==================================================
    TRIP OVERVIEW
    ==================================================

    Destination:
    Duration:
    Maximum Budget:

    ==================================================
    DAY 1
    ==================================================

    Morning:
    Afternoon:
    Evening:

    Places:
    Food:
    Estimated Cost:

    ==================================================
    DAY 2
    ==================================================

    Morning:
    Afternoon:
    Evening:

    Places:
    Food:
    Estimated Cost:

    Continue for all days.

    ==================================================
    BUDGET SUMMARY
    ==================================================

    Accommodation:
    Food:
    Transportation:
    Activities:
    Miscellaneous:

    Total Estimated Cost:

    ==================================================
    TRAVEL TIPS
    ==================================================

    - Tip 1
    - Tip 2
    - Tip 3

    ==================================================
    SOURCES
    ==================================================
    """,
    
    agent=planner_agent,
    context=[research_task, budget_task]
)