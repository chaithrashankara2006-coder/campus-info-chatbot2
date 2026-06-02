import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# Hardcoded campus location info
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
- Parking: Near Main Gate
- Principal Office: Administrative Block, First Floor
- Exam Cell: Administrative Block, Ground Floor
"""

def get_chatbot():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        max_tokens=500
    )
    return llm

def ask_question(llm, context, question):
    # Limit context to avoid token limit error
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
CAMPUS_INFO = """
... existing info ...

Academic Calendar PESCE:
- Odd Semester: August to December
- Even Semester: January to May
- Internal Assessment: Every 6 weeks
- Semester End Exams: November/December and April/May
- Attendance Requirement: Minimum 75%
- Fee Payment: Before semester start

Student Procedures:
- Bonafide Certificate: Apply at admin office
- Transcript: Apply at exam cell
- Fee Payment: Online via college portal
- ID Card: Student affairs office
- Scholarship: SC/ST cell, OBC cell
"""