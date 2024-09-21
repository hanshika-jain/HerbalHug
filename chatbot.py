import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from dotenv import load_dotenv
import os
import mysql.connector
import google.generativeai as genai
from PIL import Image
import io
import pandas as pd

# Load environment variables
load_dotenv()

# Configure GenAI Key
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
print(f"Using Google Application Credentials from: {credentials_path}")

genai.configure(api_key=os.getenv("API_KEY"))

# DB Connection and configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="herbalhug"
)

# Function to clean and extract SQL from model's response
def clean_query(response):
    cleaned_response = response.replace('sql', '').replace('```', '').strip()
    return cleaned_response

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return clean_query(response.text)

# Function to retrieve query from the database
def read_sql_query(sql, db):
    cur = db.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to execute SQL insert/update queries
def execute_sql_query(sql, db):
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

# Function to load Gemini model and get responses from image
def get_gemini_response_from_image(image_bytes):
    model = genai.GenerativeModel('gemini-1.5-flash')
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')
    response = model.generate_content([
        'The image shows a medicinal/ayurvedic plant/tree leaf. Identify the leaf. '
        'Give only the scientific name and nothing else. It should be only a two-word answer.', image])
    plant_name = response.text.strip()
    return plant_name

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the table named plantsf and has the following columns - 
    ID, Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses
    """
]

# Streamlit App
st.set_page_config(page_title="Herbal Hug", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Layout
st.title('🌿 Herbal Hug')
st.subheader('Welcome to Herbal Hug! Navigate the World of Herbal Health')

# Chat input
user_input = st.text_input("Type your question or upload an image...")

if st.button("Send"):
    # Store user question in chat history
    st.session_state.chat_history.append({"user": user_input})

    if user_input.endswith(('.jpg', '.png')):
        # If input is an image upload (you may need to change this handling)
        uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'png'], key="image_upload")
        if uploaded_file:
            image_bytes = uploaded_file.read()
            plant_name = get_gemini_response_from_image(image_bytes).strip()
            st.session_state.chat_history.append({"bot": f"Plant identified: {plant_name}"})
    else:
        # Process the question
        sql_query = get_gemini_response(user_input, prompt)
        st.session_state.chat_history.append({"bot": f"Generated SQL Query: {sql_query}"})

        response = read_sql_query(sql_query, mydb)
        if response:
            st.session_state.chat_history.append({"bot": f"Output: {response}"})
        else:
            st.session_state.chat_history.append({"bot": "No results found or an error occurred."})

# Display chat history
for chat in st.session_state.chat_history:
    if "user" in chat:
        st.markdown(f"*You:* {chat['user']}")
    if "bot" in chat:
        st.markdown(f"*Bot:* {chat['bot']}")

# Capture Location
st.write("---")
st.header("🌍 Capture Location")
location = streamlit_geolocation()

if location is not None:
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    st.success(f'Location captured: Latitude - {latitude}, Longitude - {longitude}')
else:
    st.warning('Failed to capture location. Please try again.')

# Map Display
st.write("---")
st.header("🗺 Map of Plant Locations")

try:
    if st.session_state.chat_history:
        last_plant_query = st.session_state.chat_history[-1].get("bot", "")
        if "identified" in last_plant_query:
            plant_name = last_plant_query.split(":")[-1].strip()
            locations_query = f"SELECT Scientific_Name, latitude, longitude FROM user_loc WHERE Scientific_Name = '{plant_name}'"
            locations = read_sql_query(locations_query, mydb)

            if locations:
                df = pd.DataFrame(locations, columns=["Scientific_Name", "latitude", "longitude"])
                st.map(df)
            else:
                st.write(f"No locations available for {plant_name}.")
except Exception as e:
    st.error(f"An error occurred while fetching locations: {e}")