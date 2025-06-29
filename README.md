# Appointment Booking AI Agent with Google Calendar

This project is a conversational AI agent built with FastAPI, LangGraph, and Streamlit that allows users to **book appointments** and **query their upcoming events** using natural language.

---

## Live Demo

[Click here to try the deployed app](https://eventbookcalendargit.streamlit.app/)

---

## Tech Stack

* Backend: FastAPI (Python)
* Agent Framework: LangGraph + LangChain
* Frontend: Streamlit chat UI
* Calendar Integration: Google Calendar API
* OAuth2: User-specific login & booking

---

## Features

* Accepts **natural language** like:

  * "Book a meeting tomorrow at 3 PM"
  * "Do I have any events next week?"
* Automatically **understands intent** (book vs view)
* Books directly into the user's **Google Calendar**
* Shows **upcoming meetings** on demand

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/appointment-bot.git
cd appointment-bot
```

---

### 2. Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# OR
source venv/bin/activate   # On macOS/Linux
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add Your `.env` File

Create a `.env` file in the root:

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
REDIRECT_URI=http://localhost:8000/oauth2callback
```

> Do **not** commit `.env` or `credentials.json`. They are in `.gitignore`.

---

### 5. Place Your Google OAuth Credentials

Save your `credentials.json` (from Google Cloud Console) into the `backend/` folder.

---

### 6. Run FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

---

### 7. Run Streamlit Frontend

In a new terminal:

```bash
streamlit run frontend/app.py
```

Opens in browser at: [http://localhost:8501](http://localhost:8501)

---

## Example User Prompts

| Prompt                               | What It Does                     |
| ------------------------------------ | -------------------------------- |
| "Book an event tomorrow at 4 PM"     | Books an event for 4 PM tomorrow |
| "What meetings do I have this week?" | Lists upcoming events            |
| "Schedule a call Friday at 2 PM"     | Books an event on Friday         |

---

## Project Structure

```
Appointment_Bot/
├── backend/
│   ├── main.py
│   ├── agent_graph.py
│   ├── calendar_utils.py
│   └── credentials.json (NOT tracked)
├── frontend/
│   └── app.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## Security Notes

* `.env`, `credentials.json`, and service account files are ignored via `.gitignore`.
* Store secrets securely in deployment using environment variables or GitHub Secrets.

---

## Future Enhancements

* Add location and attendee support
* Rescheduling & canceling events
* Time zone detection
* Switch to multi-turn LLM with memory

---

## License

MIT License — free to use and modify for educational and commercial projects.

---

## Author

Made by **Sanchit Kanwar**
Try the live version: [https://eventbookcalendargit.streamlit.app](https://eventbookcalendargit.streamlit.app)
