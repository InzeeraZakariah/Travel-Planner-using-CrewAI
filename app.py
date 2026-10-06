import streamlit as st
from crew import travel_crew


st.set_page_config(page_title = "AI Travel Planner",layout = "wide")

st.title("AI Travel Planner")
st.write("Create a personalized travel itinerary using CrewAI multi-agent")

with st.sidebar:
    st.header("Trip Details")
    destination = st.text_input("Destination", placeholder = "Example: Kerala")
    days = st.number_input("Number of days", min_value = 1, value = 3)
    budget = st.number_input("Maximum Budget (Rs.)", min_value = 1000)
    create_plan = st.button("Create Travel Plan", use_container_width = True)

if create_plan:
    if not destination.strip():
        st.error("Please enter a destination")
        st.stop()
    
    inputs = {
        "destination": destination,
        "days":days,
        "budget": budget
    }

    st.subheader(f"Planning your {days}- day trip to {destination}")
    
    with st.status("AI agents are working.......", expanded = True):
        st.write("Research Agent is searching on the web")
        try:
            result = travel_crew.kickoff(inputs=inputs)
        except Exception as e:
            st.error(e)
            st.stop()
        st.write("Web search completed !")
        st.write("Budget analysis completed !")
        st.write("Final Itinerary created !")
        
        st.subheader("Your Travel Plan")
        st.markdown(str(result))

        st.download_button(
            label = "Download Travel Plan",
            data = str(result),
            file_name = "travel_plan.txt",
            mime = "text/plain  "
        )