from crewai import Crew, Process
from agents import research_agent, budget_agent, planner_agent
from tasks import research_task, budget_task, planning_task
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# CREATE CREW
travel_crew = Crew(
    agents = [research_agent, budget_agent, planner_agent],
    tasks = [research_task, budget_task, planning_task],
    process = Process.sequential,
    verbose = True
)