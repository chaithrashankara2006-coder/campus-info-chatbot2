import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

def get_chatbot():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    return llm

def ask_question(llm, context, question):
    messages = [
        SystemMessage(content=f"""You are a helpful campus information 
        assistant. Answer based ONLY on this information:
        {context}
        Give direct and accurate answers."""),
        HumanMessage(content=question)
    ]
    response = llm.invoke(messages)
    return response.content