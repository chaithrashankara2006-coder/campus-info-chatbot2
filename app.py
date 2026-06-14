import os
import streamlit as st
from src.chatbot import get_chatbot, ask_question
from src.web_scraper import scrape_website
from src.document_processor import process_pdf
from src.vector_store import create_vector_store, search_context

st.set_page_config(
    page_title="Campus Info Chatbot",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Campus Info Chatbot")
st.caption("PES College of Engineering — AI Campus Assistant")

# Department wise PDF paths and URLs
dept_info = {
    "Computer Science & Engineering": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CSE.pdf"),
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "AI & Machine Learning": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CSE.pdf"),
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Data Science": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CSE.pdf"),
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Computer Science & Business Systems": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CSE.pdf"),
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Electronics & Communication": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "ECE.pdf"),
        "url": "https://pesce.ac.in/department-ece.php"
    },
    "Mechanical Engineering": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "MECH.pdf"),
        "url": "https://pesce.ac.in/department-mechanical.php"
    },
    "Civil Engineering": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CIVIL.pdf"),
        "url": "https://pesce.ac.in/department-civil.php"
    },
    "Electrical Engineering": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "EEE.pdf"),
        "url": "https://pesce.ac.in/department-eee.php"
    },
    "Information Science": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "ISE.pdf"),
        "url": "https://pesce.ac.in/department-ise.php"
    },
    "Library": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "LIBRARY.pdf"),
        "url": "https://pesce.ac.in"
    },
    "Canteen": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CANTEEN.pdf"),
        "url": "https://pesce.ac.in"
    },
    "Placement Cell": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "PLACEMENT.pdf"),
        "url": "https://pesce.ac.in/placements.php"
    },
    "Hostel": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "HOSTEL.pdf"),
        "url": "https://pesce.ac.in/hostel.php"
    },
    "Transport": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CollegeRules.pdf"),
        "url": "https://pesce.ac.in/transport.php"
    },
    "College Rules": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "CollegeRules.pdf"),
        "url": "https://pesce.ac.in/about.php"
    },
    "Sports & Facilities": {
        "pdf": os.path.join(os.path.dirname(__file__), "data", "pdfs", "SPORTS.pdf"),
        "url": "https://pesce.ac.in/facilities.php"
    },
}

dept_questions = {
    "Library": [
        ("📚 Library Timings", "What are the library timings?"),
        ("📖 Books Available", "What books and resources are available in library?"),
        ("🔖 How to Borrow", "How to borrow books from library?"),
        ("💻 Digital Resources", "What digital resources are available in library?"),
        ("📋 Library Rules", "What are the library rules?"),
        ("🪑 Reading Room", "Is there a reading room in library?"),
    ],
    "Canteen": [
        ("🍽️ Menu", "What food is available in canteen?"),
        ("⏰ Timings", "What are the canteen timings?"),
        ("💰 Price", "What are the canteen food prices?"),
        ("🥗 Veg Options", "What vegetarian food is available?"),
        ("🏪 Facilities", "What are the canteen facilities?"),
        ("📍 Location", "Where is the canteen located?"),
    ],
    "Hostel": [
        ("🏠 Facilities", "What are the hostel facilities?"),
        ("📋 Rules", "What are the hostel rules?"),
        ("⏰ Timings", "What are hostel in and out timings?"),
        ("💰 Fees", "What is the hostel fee?"),
        ("🍽️ Mess Info", "What are the mess timings and menu?"),
        ("📞 Warden Contact", "Who is the hostel warden and contact?"),
    ],
    "Transport": [
        ("🚌 Bus Routes", "What are the bus routes available?"),
        ("⏰ Bus Timings", "What are the bus timings?"),
        ("💰 Bus Fees", "What is the transport fee?"),
        ("📍 Bus Stops", "What are the bus stop locations?"),
        ("📞 Transport Contact", "Who to contact for transport info?"),
        ("🔄 Route Changes", "How to apply for route change?"),
    ],
    "Placement Cell": [
        ("🏢 Companies", "Which companies visit for placements?"),
        ("📊 Placement Stats", "What are the placement statistics?"),
        ("📝 How to Register", "How to register for placements?"),
        ("💼 Internships", "How to get internships through college?"),
        ("📞 Contact", "What are placement cell contact details?"),
        ("📅 Schedule", "What is the placement schedule?"),
    ],
    "College Rules": [
        ("👗 Dress Code", "What is the dress code at PESCE?"),
        ("📱 Mobile Policy", "What is the mobile phone policy?"),
        ("⏰ Attendance", "What is the attendance requirement?"),
        ("🚫 Prohibited", "What is prohibited on campus?"),
        ("📋 General Rules", "What are the general college rules?"),
        ("🎓 Exam Rules", "What are the examination rules?"),
    ],
    "Sports & Facilities": [
        ("⚽ Sports Available", "What sports facilities are available?"),
        ("⏰ Ground Timings", "What are the sports ground timings?"),
        ("🏆 Achievements", "What are sports achievements of PESCE?"),
        ("📝 How to Join", "How to join sports teams?"),
        ("🏊 Other Facilities", "What other facilities are available on campus?"),
        ("👕 Sports Events", "What sports events are conducted?"),
    ],
    "default": [
        ("👨‍🏫 Who is HOD?", "Who is the HOD?"),
        ("🏢 Placement Info", "What are the placement details?"),
        ("📚 Courses Offered", "What courses are offered?"),
        ("🔬 Research Info", "What are the research activities?"),
        ("🏛️ About Department", "Tell me about this department?"),
        ("📞 Contact Info", "What are the contact details?"),
        ("🎭 Clubs & Events", "What are the clubs and events?"),
        ("🏆 Achievements", "What are the achievements?"),
        ("👨‍🎓 Faculty List", "Who are the faculty members?"),
    ],
}

# Initialize session state
if "llm" not in st.session_state:
    st.session_state.llm = get_chatbot()

if "vector_stores" not in st.session_state:
    st.session_state.vector_stores = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_dept" not in st.session_state:
    st.session_state.selected_dept = "Computer Science & Engineering"

# Functions
def load_dept_data(dept):
    if dept not in st.session_state.vector_stores:
        info = dept_info.get(dept, {})
        pdf_path = info.get("pdf", "")
        url = info.get("url", "")
        combined_text = ""

        if pdf_path:
            if os.path.exists(pdf_path):
                pdf_text = process_pdf(pdf_path)
                if pdf_text:
                    combined_text += pdf_text
                    st.sidebar.write(f"PDF loaded: {len(pdf_text)} chars")
                else:
                    st.sidebar.write(f"PDF empty: {pdf_path}")
            else:
                st.sidebar.write(f"PDF not found: {pdf_path}")

        if url:
            scraped = scrape_website(url)
            if scraped and "Error" not in scraped and len(scraped.strip()) > 0:
                combined_text += "\n" + scraped
                st.sidebar.write(f"Website scraped: {len(scraped)} chars")
            else:
                st.sidebar.write(f"Web scrape failed: {scraped[:100]}")

        if not combined_text.strip():
            combined_text = f"Information about {dept} at PES College of Engineering, Mandya, Karnataka."
            st.sidebar.write(f"Using fallback text")

        st.session_state.vector_stores[dept] = (
            create_vector_store(combined_text)
        )
    return True


def get_response(prompt):
    current_store = st.session_state.vector_stores.get(
        st.session_state.selected_dept
    )
    if current_store:
        context = search_context(current_store, prompt)
    else:
        context = "No information loaded yet."
    return ask_question(st.session_state.llm, context, prompt)

# Sidebar
with st.sidebar:
    st.header("🏛️ Select Department")
    dept = st.selectbox(
        "Department",
        list(dept_info.keys())
    )

    if dept != st.session_state.selected_dept:
        st.session_state.selected_dept = dept
        st.session_state.messages = []

    st.divider()

    if st.button("🔄 Load Department Data"):
        with st.spinner(f"Loading {dept} data..."):
            load_dept_data(dept)
            st.success(f"{dept} loaded! ✅")

    st.divider()

    st.write("📤 Upload PDF manually:")
    uploaded_file = st.file_uploader(
        f"Upload {dept} PDF",
        type="pdf"
    )
    if uploaded_file:
        pdf_path = f"data/pdfs/{dept.replace(' ', '_')}.pdf"
        os.makedirs("data/pdfs", exist_ok=True)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        with st.spinner(f"Processing {dept} PDF..."):
            pdf_text = process_pdf(pdf_path)
            st.session_state.vector_stores[dept] = (
                create_vector_store(pdf_text)
            )
            st.success(f"{dept} PDF loaded! ✅")

    st.divider()

    st.header("📊 Loaded Departments")
    for d in dept_info.keys():
        if d in st.session_state.vector_stores:
            st.write(f"✅ {d}")
        else:
            st.write(f"⬜ {d}")

    st.divider()
    st.header("📞 Quick Contacts")
    st.write("**HOD CSE:** Dr. Anitha M L")
    st.write("📧 anithaml@pesce.ac.in")
    st.write("📞 +91 9945576186")
    st.divider()
    st.write("**Placement:** Dr. Vinay S")
    st.write("📧 vinay@pesce.ac.in")
    st.write("📞 +91 9986515835")
    st.divider()
    st.write("**College:** +91 9448282588")
    st.write("📧 admissions@pesce.ac.in")
    st.write("🌐 pesce.ac.in")
    st.divider()
    st.header("📍 Location")
    st.write("**PESCE, Mandya, Karnataka**")
    st.markdown("[📌 Open in Google Maps](https://maps.google.com/?q=PES+College+of+Engineering+Mandya)")
    st.write("📞 Emergency: 112")
    st.write("🏥 Medical: +91 9448282588")

# Auto load on startup
if dept not in st.session_state.vector_stores:
    with st.spinner(f"Loading {dept} data..."):
        load_dept_data(dept)

# Status
if dept in st.session_state.vector_stores:
    st.success(f"✅ {dept} data loaded — Ready to answer!")
else:
    st.warning(f"⚠️ No data for {dept}. Click 'Load Department Data'.")

# Dynamic quick questions
st.subheader(f"💡 Quick Questions — {dept}")
questions = dept_questions.get(dept, dept_questions["default"])

cols = st.columns(3)
for i, (label, question) in enumerate(questions):
    with cols[i % 3]:
        if st.button(label, key=f"q_{i}"):
            st.session_state.quick_q = question

st.divider()

st.caption("📍 General Campus Info")
location_questions = [
    ("📍 Location & Map", "Where is PESCE located? How to reach the college?"),
    ("🚌 Transport Info", "What are the bus routes and transport facilities?"),
    ("🏠 Hostel Info", "What are the hostel facilities and rules at PESCE?"),
]
loc_cols = st.columns(3)
for i, (label, question) in enumerate(location_questions):
    with loc_cols[i]:
        if st.button(label, key=f"loc_{i}"):
            st.session_state.quick_q = question

st.divider()

# Chat interface

st.subheader("💬 Chat")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle quick questions
if "quick_q" in st.session_state:
    prompt = st.session_state.quick_q
    del st.session_state.quick_q
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt)
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

# User input
if prompt := st.chat_input(f"Ask about {dept}..."):
    if len(prompt.strip()) < 3:
        st.warning("Please enter a valid question!")
        st.stop()
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt)
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )