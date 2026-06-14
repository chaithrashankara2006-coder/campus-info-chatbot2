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

DEPT_FALLBACK_INFO = """
LIBRARY INFO:
- Timings: 8:00 AM to 8:00 PM, Monday to Saturday
- Location: Main Building, First Floor
- Facilities: Reading room, digital resources, book lending
- Borrowing: Students can borrow books using library card, max 3 books for 14 days
- Librarian: Sowjanya B L (Library Assistant)

CANTEEN INFO:
- Location: Near Main Gate, Ground Floor
- Timings: 7:00 AM to 9:00 PM
- Food: Veg and non-veg meals, snacks, beverages
- Prices: Affordable, student-friendly rates

HOSTEL INFO:
- Boys Hostel and Girls Hostel available within campus
- Facilities: Mess, Wi-Fi, study rooms, 24/7 security
- Timings: In-time by 9:30 PM (subject to warden rules)
- Fees: Contact college administration for current fee structure
- Warden contact: +91 9448282588

TRANSPORT INFO:
- KSRTC buses available from Bangalore, Mysore, Hassan to Mandya
- College is 100km from Bangalore via Bangalore-Mysore highway
- Nearest railway station: Mandya Railway Station (3km from college)
- Bus pass and route details: Contact transport office

PLACEMENT CELL INFO:
- Placement Officer: Dr. Vinay S
- Email: vinay@pesce.ac.in
- Phone: +91 9986515835
- Location: Administrative Block, Ground Floor
- Companies visiting: TCS, Infosys, Wipro, and other IT/core companies
- Activities: Pre-placement training, mock interviews, internships

COLLEGE RULES:
- Dress Code: Formal attire required (no casual wear like t-shirts, shorts, slippers)
- Attendance: Minimum 75% required to be eligible for exams
- Mobile Phones: Restricted use during class hours
- ID Cards: Must be carried at all times on campus
- Exam Rules: No malpractice tolerated, valid ID required for exams

SPORTS & FACILITIES:
- Sports Ground: Behind Main Building
- Facilities: Cricket, volleyball, basketball, indoor games
- Sports Events: Inter-department competitions held annually
- How to join: Contact Physical Education Department or sports committee
"""

def get_chatbot():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
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

ADDITIONAL CAMPUS INFO:
{CAMPUS_INFO}

DEPARTMENT FALLBACK INFO:
{DEPT_FALLBACK_INFO}

IMPORTANT RULES:
- Check DOCUMENT CONTEXT first
- If not found there, check DEPARTMENT FALLBACK INFO and ADDITIONAL CAMPUS INFO
- NEVER say "not available" if any of the above sections contain relevant info
- Extract and present information clearly
- Keep answer under 5 sentences
- If genuinely nowhere in any section, say exactly: "This information is not available. Please contact +91 9448282588 or visit pesce.ac.in"
"""),
        HumanMessage(content=f"Question: {question}\n\nCheck all provided information sections carefully and answer.")
    ]
    response = llm.invoke(messages)
    return response.content