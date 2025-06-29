from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse
from backend.calendar_utils import get_auth_url, get_user_credentials
from backend.agent_graph import build_graph

app = FastAPI()

user_tokens = {}

@app.get("/auth")
def authorize():
    auth_url, state = get_auth_url()
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def auth_callback(code: str = Query(...)):
    creds = get_user_credentials(code)
    user_tokens['user'] = creds
    return {"message": "✅ Auth successful! You can now book appointments."}

from datetime import datetime, timedelta
from backend.calendar_utils import get_calendar_service, get_availability, create_event

@app.get("/book_demo")
def book_demo():
    creds = user_tokens.get("user")
    if not creds:
        return {"error": "User not authenticated. Visit /auth first."}

    service = get_calendar_service(creds)
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=1)

    busy = get_availability(service, start, end)
    if busy:
        return {"message": "You're busy at that time!"}
    else:
        event = create_event(service, start, end, summary="Demo Booking")
        return {"message": f"✅ Event created at {start.strftime('%A %I:%M %p')}"}

graph = build_graph()
user_tokens = {}  # already exists

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    credentials = user_tokens.get("user")

    if not credentials:
        return {"messages": messages + [{"role": "assistant", "content": "🔒 Please log in at /auth to connect your calendar."}]}

    result = graph.invoke({
        "messages": messages,
        "credentials": credentials
    })
    return {"messages": result["messages"]}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Calendar Assistant API! Visit /auth to start."}