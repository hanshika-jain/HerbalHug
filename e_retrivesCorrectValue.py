import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("API_KEY"))

# DB Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="herbalhug"
)

def clean_query(response):
    return response.replace('sql', '').strip()

def read_sql_query(sql, db):
    cur = db.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Define chatbot prompt for SQL generation
chat_prompt = """
You are a SQL expert working with a MySQL database called 'herbalhug' containing medicinal plants data.
The correct table name is 'plantsf' and it contains the following columns: Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses, location.
When asked about a plant, generate a SQL query that checks for the plant in all three columns: 'Plant_Name', 'Scientific_Name', and 'Common_Name'.
The query should look for a match in any of these columns.
Do not include any explanation, just the SQL query as output.
"""

# Function to generate SQL query from chatbot response
def generate_sql_query(question, plant_name=None):
    model = genai.GenerativeModel('gemini-pro')
    if plant_name:
        question = f"The user is asking about the plant '{plant_name}'. {question}"
    
    response = model.generate_content([chat_prompt, question])
    return clean_query(response.text).strip()

# Function to remember the plant in context
def update_context(question):
    # Check for any plant names mentioned in the question
    for word in question.split():
        sql_query = f"SELECT Plant_Name FROM plantsf WHERE Common_Name LIKE '%{word}%' OR Scientific_Name LIKE '%{word}%' OR Plant_Name LIKE '%{word}%'"
        plant_check = read_sql_query(sql_query, mydb)
        if plant_check:
            return plant_check[0][0]  # Return the first matching plant name
    return st.session_state.plant_context  # Return the existing context if no new plant is found

def handle_chat(question):
    if "plant_context" not in st.session_state:
        st.session_state.plant_context = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    new_context = update_context(question)

    if new_context and new_context != st.session_state.plant_context:
        st.session_state.plant_context = new_context

    sql_query = generate_sql_query(question, st.session_state.plant_context)
    cleaned_query = sql_query.replace("```", "").strip()
    print(cleaned_query)

    result = read_sql_query(cleaned_query, mydb)

    

    plant_name = st.session_state.plant_context if st.session_state.plant_context else "the plant"

    if result:
        if any(keyword in question.lower() for keyword in ["where", "location"]):
            location = result[0][-1]  # Assuming location is the last column
            return f"{plant_name} is found in {location}."
        elif any(keyword in question.lower() for keyword in ["use", "uses"]):
            if len(result[0]) > 5:  # Ensure that the uses column is present
                uses = result[0][5]  # Assuming uses are at index 5
                return f"The medicinal uses of {plant_name} include {uses}."
            else:
                return f"I couldn't find the uses of {plant_name}."
        elif "scientific name" in question.lower():
            return f"The scientific name of {plant_name} is {result[0][2]}."  # Assuming scientific name is at index 2
        elif "family name" in question.lower():
            return f"The family name of {plant_name} is {result[0][4]}."  # Assuming family name is at index 3
        else:
            return f"Here's what I found about {plant_name}: {result[0]}"
    else:
        return "I couldn't find the information you're looking for."















# Chat UI setup
def chat_ui():
    st.markdown("### Herbal Chatbot")
    
    question = st.text_input("Ask me anything about medicinal plants:", key="chat_input")
    if st.button("Send"):
        answer = handle_chat(question)
        
        st.session_state.chat_history.append(("You", question))
        st.session_state.chat_history.append(("Bot", answer))
    
    st.write("### Chat History")
    for speaker, message in st.session_state.chat_history:
        st.write(f"**{speaker}:** {message}")

# Streamlit layout
st.set_page_config(page_title="Herbal Hug", layout="wide")

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'plant_context' not in st.session_state:
    st.session_state.plant_context = None
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

col1, col2 = st.columns([2, 3])

with col1:
    st.header("Search")
    # Other search and image processing sections can go here

with col2:
    st.title("Herbal Hug Chatbot")
    st.subheader("Welcome to Herbal Hug!")
    
    if st.button("Open Chat"):
        st.session_state.show_chat = True
    
    if st.session_state.show_chat:
        chat_ui()

# Scrollbar for the chat
st.markdown("""<style>div[data-testid="stVerticalBlock"] { max-height: 400px; overflow-y: scroll; }</style>""", unsafe_allow_html=True)
