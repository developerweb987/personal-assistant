# app.py
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# --- Helper functions ---

def generate_schedule_prompt(title, date, time, duration, attendees, location, details, tone):
    return f"""
You are a smart personal assistant.

Task: Create a professional scheduling message and a calendar entry description.

Title: {title}
Date: {date}
Time: {time}
Duration: {duration} minutes
Attendees: {attendees}
Location: {location}
Details: {details}
Tone: {tone}

Please return output in this format:

SUBJECT: ...
BODY: ...
CALENDAR: ...
AGENDA:
- point 1
- point 2
- point 3
    """


def generate_email_prompt(recipient_name, recipient_role, subject_hint, purpose, key_points, tone, length):
    return f"""
You are an expert email-writing assistant.

Draft a professional email using the details below.

Recipient name: {recipient_name}
Recipient role: {recipient_role}
Subject idea: {subject_hint}
Purpose: {purpose}
Key points: {key_points}
Tone: {tone}
Desired length: {length}

Please return output in this format:

SUBJECT: ...
BODY: ...
ALTERNATIVE SUBJECTS:
1. ...
2. ...
FOLLOW-UP SENTENCES:
1. ...
2. ...
    """

def get_gemini_response(prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---

st.set_page_config(page_title="AI Personal Assistant — Schedule & Email Drafts", layout="centered")

st.title("🤖 AI Personal Assistant — Schedule & Email Drafts")

option = st.radio("Select a feature", ["📅 Schedule Creator", "✉️ Email Draft Generator"])

if option == "📅 Schedule Creator":
    st.header("📅 Create a Meeting Invite")

    with st.form("schedule_form"):
        title = st.text_input("Meeting Title", "Project Sync Meeting")
        date = st.date_input("Date")
        time = st.text_input("Time (e.g. 3:00 PM)", "3:00 PM")
        duration = st.number_input("Duration (minutes)", 30)
        attendees = st.text_area("Attendees (comma-separated)", "john@example.com, jane@example.com")
        location = st.text_input("Location / Link", "Zoom: https://zoom.us/...")
        details = st.text_area("Additional Details", "Weekly catch-up on progress and blockers.")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Formal", "Casual"], index=0)
        submitted = st.form_submit_button("Generate Schedule")

    if submitted:
        with st.spinner("✨ Generating your meeting invite..."):
            prompt = generate_schedule_prompt(title, date, time, duration, attendees, location, details, tone)
            try:
                response_text = get_gemini_response(prompt)
                st.success("✅ Invite generated successfully!")
                st.text_area("Generated Invite", response_text, height=250)
            except Exception as e:
                st.error(f"Error: {e}")

elif option == "✉️ Email Draft Generator":
    st.header("✉️ Draft a Professional Email")

    with st.form("email_form"):
        recipient_name = st.text_input("Recipient Name", "Alex")
        recipient_role = st.text_input("Recipient Role / Company", "Marketing Manager at XYZ Co.")
        subject_hint = st.text_input("Subject Hint", "Inquiry about collaboration")
        purpose = st.text_area("Purpose of Email", "To discuss potential collaboration on upcoming campaign.")
        key_points = st.text_area("Key Points", "introduce myself, explain project, request a short call")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Persuasive", "Concise"], index=0)
        length = st.selectbox("Length", ["Short", "Medium", "Detailed"], index=1)
        submitted = st.form_submit_button("Generate Email")

    if submitted:
        with st.spinner("💡 Drafting your email..."):
            prompt = generate_email_prompt(recipient_name, recipient_role, subject_hint, purpose, key_points, tone, length)
            try:
                response_text = get_gemini_response(prompt)
                st.success("✅ Email generated successfully!")
                st.text_area("Generated Email", response_text, height=300)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini 2.5 Flash")
