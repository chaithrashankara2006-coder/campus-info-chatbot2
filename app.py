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
        "pdf": "data/CSE.pdf",
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "AI & Machine Learning": {
        "pdf": "data/CSE.pdf",
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Data Science": {
        "pdf": "data/CSE.pdf",
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Computer Science & Business Systems": {
        "pdf": "data/pdfs/CSE.pdf",
        "url": "https://pesce.ac.in/department-computer-science.php"
    },
    "Electronics & Communication": {
        "pdf": "data/pdfs/ECE.pdf",
        "url": "https://pesce.ac.in/department-ece.php"
    },
    "Mechanical Engineering": {
        "pdf": "data/pdfs/MECH.pdf",
        "url": "https://pesce.ac.in/department-mechanical.php"
    },
    "Civil Engineering": {
        "pdf": "data/pdfs/CIVIL.pdf",
        "url": "https://pesce.ac.in/department-civil.php"
    },
    "Electrical Engineering": {
        "pdf": "data/pdfs/EEE.pdf",
        "url": "https://pesce.ac.in/department-eee.php"
    },
    "Information Science": {
        "pdf": "data/pdfs/ISE.pdf",
        "url": "https://pesce.ac.in/department-ise.php"
    },
    "Library": {
        "pdf": "data/pdfs/LIBRARY.pdf",
        "url": "https://pesce.ac.in"
    },
    "Canteen": {
        "pdf": "data/pdfs/CANTEEN.pdf",
        "url": "https://pesce.ac.in"
    },
    "Placement Cell": {
        "pdf": "",
        "url": "https://pesce.ac.in/placements.php"
    },
    "Hostel": {
        "pdf": "",
        "url": "https://pesce.ac.in/hostel.php"
    },
    "Transport": {
        "pdf": "",
        "url": "https://pesce.ac.in/transport.php"
    },
    "College Rules": {
        "pdf": "",
        "url": "https://pesce.ac.in/about.php"
    },
    "Sports & Facilities": {
        "pdf": "",
        "url": "https://pesce.ac.in/facilities.php"
    },

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


def load_dept_data(dept):
    if dept not in st.session_state.vector_stores:
        info = dept_info.get(dept, {})
        pdf_path = info.get("pdf", "")
        url = info.get("url", "")
        combined_text = ""

        # Load PDF only if path is given AND file exists
        if pdf_path and os.path.exists(pdf_path):
            combined_text += process_pdf(pdf_path)
        
        # Always try website scraping
        if url:
            scraped = scrape_website(url)
            if scraped and "Error" not in scraped:
                combined_text += "\n" + scraped

        # If nothing loaded, use basic info
        if not combined_text.strip():
            combined_text = f"Information about {dept} at PES College of Engineering, Mandya, Karnataka."

        st.session_state.vector_stores[dept] = (
            create_vector_store(combined_text)
        )
        return True
    return True





# Sidebar
with st.sidebar:
    st.header("🏛️ Select Department")
    dept = st.selectbox(
        "Department",
        list(dept_info.keys())
    )

    # Reset chat when department changes
    if dept != st.session_state.selected_dept:
        st.session_state.selected_dept = dept
        st.session_state.messages = []

    st.divider()

    # Auto load button
    if st.button("🔄 Load Department Data"):
        with st.spinner(f"Loading {dept} data..."):
            success = load_dept_data(dept)
            if success:
                st.success(f"{dept} loaded! ✅")
            else:
                st.warning(
                    f"No PDF found for {dept}. "
                    f"Please upload PDF below."
                )

    st.divider()

    # Manual PDF upload option
    st.write("📤 Upload PDF manually:")
    uploaded_file = st.file_uploader(
        f"Upload {dept} PDF",
        type="pdf"
    )
    if uploaded_file:
        # Save to dept specific path
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

    # Show loaded departments
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

# Auto load current department data on startup
if dept not in st.session_state.vector_stores:
    with st.spinner(f"Loading {dept} data..."):
        load_dept_data(dept)

# Quick question buttons
st.subheader(f"💡 Quick Questions — {dept}")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👨‍🏫 Who is HOD?"):
        st.session_state.quick_q = (
            f"Who is the HOD of {dept} department?"
        )
with col2:
    if st.button("🏢 Placement Info"):
        st.session_state.quick_q = (
            f"What are the placement details for {dept}?"
        )
with col3:
    if st.button("📚 Courses Offered"):
        st.session_state.quick_q = (
            f"What courses are offered in {dept}?"
        )

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("🔬 Research Info"):
        st.session_state.quick_q = (
            f"What are the research activities in {dept}?"
        )
with col5:
    if st.button("🏛️ About Department"):
        st.session_state.quick_q = (
            f"Tell me about {dept} department?"
        )
with col6:
    if st.button("📞 Contact Info"):
        st.session_state.quick_q = (
            f"What are the contact details of {dept}?"
        )

col7, col8, col9 = st.columns(3)
with col7:
    if st.button("🎭 Clubs & Events"):
        st.session_state.quick_q = (
            f"What are the clubs and events in {dept}?"
        )
with col8:
    if st.button("🏆 Achievements"):
        st.session_state.quick_q = (
            f"What are the achievements of {dept}?"
        )
with col9:
    if st.button("👨‍🎓 Faculty List"):
        st.session_state.quick_q = (
            f"Who are the faculty members in {dept}?"
        )
col10, col11, col12 = st.columns(3)
with col10:
    if st.button("📍 Location & Map"):
        st.session_state.quick_q = (
            "Where is PESCE located? How to reach the college?"
        )
with col11:
    if st.button("🚌 Transport Info"):
        st.session_state.quick_q = (
            "What are the bus routes and transport facilities?"
        )
with col12:
    if st.button("🏠 Hostel Info"):
        st.session_state.quick_q = (
            "What are the hostel facilities and rules at PESCE?"
        )

st.divider()

# Status message
if dept in st.session_state.vector_stores:
    st.success(f"✅ {dept} data loaded — Ready to answer!")
else:
    st.warning(
        f"⚠️ No data for {dept}. "
        f"Click 'Load Department Data' in sidebar."
    )

# Chat interface
st.subheader("💬 Chat")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def get_response(prompt):
    current_store = st.session_state.vector_stores.get(
        st.session_state.selected_dept
    )
    if current_store:
        context = search_context(current_store, prompt)
    else:
        context = f"No information loaded for {dept} yet."
    return ask_question(st.session_state.llm, context, prompt)

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