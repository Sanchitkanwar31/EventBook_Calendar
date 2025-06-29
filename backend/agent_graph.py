from typing import TypedDict, List, Any
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from datetime import timedelta
import dateparser
from dateparser.search import search_dates
from backend.calendar_utils import get_calendar_service, get_availability, create_event
from backend.calendar_utils import get_upcoming_events

# State schema
class AgentState(TypedDict):
    messages: List[dict]
    credentials: Any





def handle_booking(state: AgentState) -> AgentState:
    messages = state['messages']
    credentials = state['credentials']
    user_msg = messages[-1]['content']

    # Use search_dates to extract datetime from natural language
    found = search_dates(user_msg, settings={"PREFER_DATES_FROM": "future"})

    if not found:
        return {
            "messages": messages + [{"role": "assistant", "content": " I couldn't understand the time. Can you rephrase?"}],
            "credentials": credentials
        }

    dt = found[0][1]  # First matched datetime

    service = get_calendar_service(credentials)
    busy = get_availability(service, dt, dt + timedelta(hours=1))

    if busy:
        return {
            "messages": messages + [{"role": "assistant", "content": " You're busy at that time. Try another slot?"}],
            "credentials": credentials
        }

    event = create_event(service, dt, dt + timedelta(hours=1), summary="Booked via AI")
    return {
        "messages": messages + [{"role": "assistant", "content": f" Booked: {event['summary']} at {dt.strftime('%A %I:%M %p')}"}],
        "credentials": credentials
    }

def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("handle_booking", RunnableLambda(handle_booking))
    builder.set_entry_point("handle_booking")
    builder.set_finish_point("handle_booking")  # CORRECTED
    return builder.compile()

#QUERY GENEARATOR
# def route_intent(state: AgentState) -> str:
#     user_msg = state["messages"][-1]["content"].lower()
#     if any(kw in user_msg for kw in ["show", "list", "what", "upcoming", "meetings", "events"]):
#         return "handle_query"
#     return "handle_booking"


# def build_graph():
#     builder = StateGraph(AgentState)

#     builder.add_node("route_intent", RunnableLambda(route_intent))
#     builder.add_node("handle_booking", RunnableLambda(handle_booking))
#     builder.add_node("handle_query", RunnableLambda(handle_query))

#     builder.set_entry_point("route_intent")

#     builder.add_edge("route_intent", "handle_booking")
#     builder.add_edge("route_intent", "handle_query")

#     builder.set_finish_point("handle_booking")
#     builder.set_finish_point("handle_query")

#     return builder.compile()


def handle_query(state: AgentState) -> AgentState:
    messages = state["messages"]
    credentials = state["credentials"]
    user_msg = messages[-1]["content"]

    service = get_calendar_service(credentials)
    events = get_upcoming_events(service)

    if not events:
        reply = "You're free! No upcoming meetings."
    else:
        reply = "📅 Upcoming events:\n"
        for event in events:
            time = event["start"].get("dateTime", event["start"].get("date"))
            reply += f"- {event['summary']} at {time}\n"

    return {
        "messages": messages + [{"role": "assistant", "content": reply}],
        "credentials": credentials
    }
