
import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

CAMPUS_INFO = """
PESCE Campus Location Information:
- PES College of Engineering is located in Mandya, Karnataka, India
- Address: PES College of Engineering, Mandya - 571401, Karnataka
- Google Maps: https://maps.google.com/?q=PES+College+of+Engineering+Mandya
- How to reach: Mandya is 100km from Bangalore on Bangalore-Mysore highway
- Nearest railway station: Mandya Railway Station (3km from college)
- Bus: KSRTC buses available from Bangalore, Mysore, Hassan to Mandya

Campus Facility Locations:
- Placement Cell: Administrative Block, Ground Floor
- Library: Main Building, First Floor - Open 8AM to 8PM
- Canteen: Near Main Gate, Ground Floor - Open 7AM to 9PM
- Hostel: Boys hostel and Girls hostel within campus
- Medical Center: Near Administrative Block
- Sports Ground: Behind Main Building
- Principal Office: Administrative Block, First Floor
- Exam Cell: Administrative Block, Ground Floor

Academic Calendar PESCE:
- Odd Semester: August to December
- Even Semester: January to May
- Attendance Requirement: Minimum 75%
- Fee Payment: Before semester start
"""

def get_chatbot():
    # Try Streamlit secrets first, then .env
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        max_tokens=500
    )
    return llm

def ask_question(llm, context, question):
    limited_context = context[:3000] if context else ""
    
    messages = [
        SystemMessage(content=f"""You are a helpful campus information 
        assistant for PES College of Engineering, Mandya.
        
        Always use this campus info:
        {CAMPUS_INFO}
        
        Additional context:
        {limited_context}
        
        Give short, direct answers. Max 3-4 sentences."""),
        HumanMessage(content=question)
    ]
    response = llm.invoke(messages)
    return response.content