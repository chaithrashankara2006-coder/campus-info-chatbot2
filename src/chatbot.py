
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
    limited_context = context[:6000] if context else ""
    
    messages = [
        SystemMessage(content=f"""You are a campus assistant for PES College of Engineering, Mandya.

DOCUMENT CONTEXT:
{limited_context}

IMPORTANT: The context above contains real information from department documents.
- For HOD questions: Look for "Head of Department" or "Professor & HOD" in context
- For contact questions: Look for email, phone numbers in context  
- For faculty questions: Look for faculty names and designations
- NEVER say "not available" if the context has relevant information
- Extract and present the information clearly
- If genuinely not in context, say: "Please contact +91 9448282588"
"""),
        HumanMessage(content=f"Question: {question}\n\nPlease check the document context carefully and answer.")
    ]
    response = llm.invoke(messages)
    return response.content