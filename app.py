import streamlit as st  
  
st.title("🎓 Campus Info Chatbot")  
st.write("Hello! I am your campus assistant!")  
  
name = st.text_input("What is your name?")  
if name:  
    st.write(f"Welcome {name}! 👋")

