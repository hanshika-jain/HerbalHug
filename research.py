import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import mysql.connector
from streamlit_geolocation import streamlit_geolocation
from PIL import Image
import io
import pandas as pd
import datetime

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

# Function to clean and extract SQL from model's response
def clean_query(response):
    return response.replace('sql', '').strip()

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

# Define chatbot prompt for SQL generation
chat_prompt = """
You are a SQL expert working with a MySQL database called 'herbalhug' containing medicinal plants data.
The correct table name is 'plantsf' and it contains the following columns: Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses, location.
When asked about a plant, generate a SQL query that checks for the plant in all three columns: 'Plant_Name', 'Scientific_Name', and 'Common_Name'.
The query should look for a match in any of these columns. Do not include any explanation, just the SQL query as output.
"""

# Function to generate SQL query from chatbot response
def generate_sql_query(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([chat_prompt, question])
    return clean_query(response.text).strip()

# Function to handle chatbot interaction
def handle_chat(question):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Generate and clean the SQL query
    sql_query = generate_sql_query(question)
    cleaned_query = sql_query.replace("```", "").strip()

    # Get result from the database
    result = read_sql_query(cleaned_query, mydb)

    # Process the result
    if result:
        plant_name = result[0][1] if len(result[0]) > 1 else "the plant"
        
        # Check for 'uses' related question
        if any(keyword in question.lower() for keyword in ["use", "uses"]):
            uses = result[0][5] if len(result[0]) > 5 and result[0][5] else "Unknown"
            answer = f"The medicinal uses of {plant_name} 🌿 are: {uses}."
        
        # Check for 'location' related question
        elif any(keyword in question.lower() for keyword in ["where", "location", "found"]):
            location = result[0][-1]  # Assuming location is the last column
            answer = f"📍 {plant_name} is commonly found in {location}."
        
        # Check for scientific name related question
        elif "scientific name" in question.lower():
            answer = f"The scientific name of {plant_name} is 🌱 {result[0][2]}."
        
        # Check for family name related question
        elif "family name" in question.lower():
            answer = f"The family name of {plant_name} is *{result[0][4]}*."
        
        # Default response with plant information
        else:
            answer = f"Here's what I found about {plant_name}:\n {result[0]}"
        
        # Store question and answer in history
        st.session_state.chat_history.append(("You", question))
        st.session_state.chat_history.append(("Bot", answer))
        return answer
    else:
        return "🤖 I couldn't find the information you're looking for. Could you try a different query?"

# Function to handle image-based plant identification using Gemini
def get_gemini_response_from_image(image_bytes):
    model = genai.GenerativeModel('gemini-1.5-flash')
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    response = model.generate_content([    
        'The image shows a medicinal/ayurvedic plant/tree leaf. Identify the leaf. '
        'Give only the scientific name and nothing else. It should be only a two-word answer.', image
    ])
    return response.text.strip()

# Chat UI setup
def chat_ui():
    st.markdown("<h2 style='text-align: center;'>🌿 Herbal Hug Chatbot 🌿</h2>", unsafe_allow_html=True)

    question = st.text_input("Ask me anything about medicinal plants:", key="chat_input")
    
    if st.button("💬 Send"):
        if question:  # Only handle chat if there is input
            # Generate response
            with st.spinner("Bot is typing..."):
                answer = handle_chat(question)

    # Display chat history in a scrollable container
    with st.container():
        st.write("### 🗨 Chat History")

        # Create a div container with scrolling enabled
        chat_history_container = """
        <div style='max-height: 400px; overflow-y: auto; padding-right: 10px;'>
        """
        for speaker, message in st.session_state.chat_history:
            if speaker == "You":
                chat_history_container += f"<div style='text-align: right; background-color: #f1f1f1; padding: 8px; border-radius: 10px; margin-bottom: 5px;'>{speaker}:** {message}</div>"
            else:
                chat_history_container += f"<div style='text-align: left; background-color: #e0ffe0; padding: 8px; border-radius: 10px; margin-bottom: 5px;'>{speaker}:** {message}</div>"

        chat_history_container += "</div>"

        # Display the chat history in a markdown component
        st.markdown(chat_history_container, unsafe_allow_html=True)

    # Add some additional styling
    st.markdown(
        """
        <style>
        .stTextInput, .stButton {
            margin-top: 20px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )


# Streamlit App setup
st.set_page_config(page_title="Herbal Hug", layout="wide")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if "plant_name" not in st.session_state:
    st.session_state.plant_name = None
if "locations" not in st.session_state:
    st.session_state.locations = None

# Layout with two columns
col1, col2 = st.columns([1, 3])

with col1:
    st.image("herbal_hug_logo.png", width=270, caption="Where tech meets nature!")

    search_plant = st.text_input("Search for a plant:", "")
    if st.button("🔍 Search"):
        if search_plant:
            locations_query = f"SELECT Scientific_Name, latitude, longitude FROM user_loc WHERE Scientific_Name = '{search_plant}'"
            st.session_state.locations = read_sql_query(locations_query, mydb)
            if st.session_state.locations:
                st.success(f"Locations found for {search_plant}.")
            else:
                st.warning(f"No locations found for {search_plant}.")
        else:
            st.warning("Please enter a plant name to search.")

with col2:
    st.title('Herbal Hug')
    st.subheader('🌍 Welcome to Herbal Hug! Explore Herbal Health')

    uploaded_file = st.file_uploader('🌱 Upload an image of a plant leaf:', type=['jpg', 'png'])
    if st.button("🖼 Process Image") and uploaded_file is not None:
        try:
            image_bytes = uploaded_file.read()
            st.session_state.plant_name = get_gemini_response_from_image(image_bytes).strip()
            if st.session_state.plant_name:
                st.success(f'🌿 Plant identified: {st.session_state.plant_name}')
                sql_query = f"SELECT Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses FROM plantsf WHERE Scientific_Name='{st.session_state.plant_name}'"
                plant_info = read_sql_query(sql_query, mydb)
                if plant_info:
                    st.subheader('🌱 Plant Information')
                    for info in plant_info:
                       st.write(f"**Plant Name**: {info[0]}, **Scientific Name**: {info[1]}, **Common Name**: {info[2]}, **Family Name**: {info[3]}, **Uses**: {info[4]}")
                else:
                    st.warning('No information found for the identified plant in the database.')
            else:
                st.error('Could not identify the plant. Please try another image.')
        except Exception as e:
            st.error(f'An error occurred: {e}')

st.write("---")  # Add a separator line

st.header("🌍 Capture Location")
st.write("Click on the location icon to capture your current location.")

location = streamlit_geolocation()

if location is not None:
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    st.success(f'Location captured: Latitude - {latitude}, Longitude - {longitude}')

    if st.session_state.plant_name:
        # Add selectbox to confirm if the plant is present at the captured location
        plant_present = st.selectbox("Is the plant present at this location?", ("Yes", "No"))
        remark = st.text_input("Add any remarks (optional):")
        print(remark)

        # Convert Yes/No to 1 or 0
        presence_value = 1 if plant_present == "Yes" else 0

        if st.button("Save Location"):
            # Check if the latitude, longitude, and scientific key (Scientific_Name) exist
            check_query = f"""
            SELECT COUNT(*) FROM user_loc 
            WHERE Scientific_Name = '{st.session_state.plant_name}' 
            AND latitude = {latitude} 
            AND longitude = {longitude}
            """
            record_exists = read_sql_query(check_query, mydb)

            # If the record exists, perform an update
            if record_exists and record_exists[0][0] > 0:
                update_query = f"""
                UPDATE user_loc 
                SET presence = {presence_value}, remarks='{remark}', Last_Confirmed = CURRENT_DATE, Date_found = CURRENT_DATE
                WHERE Scientific_Name = '{st.session_state.plant_name}' 
                AND latitude = {latitude} 
                AND longitude = {longitude}
                """
               
                print(update_query)  # For debugging

                try:
                    execute_sql_query(update_query, mydb)
                    st.success(f'Location and plant presence updated: Latitude - {latitude}, Longitude - {longitude}')
                except Exception as e:
                    st.error(f'Failed to update location and plant presence: {e}')
            # If the record does not exist, perform an insert
            else:
                insert_query = f"""
                INSERT INTO user_loc (Scientific_Name, latitude, longitude, presence, Date_found, Last_Confirmed, remarks) 
                VALUES ('{st.session_state.plant_name}', {latitude}, {longitude}, {presence_value}, CURRENT_DATE, CURRENT_DATE,'{remark}')
                """
                print(insert_query)  # For debugging
                try:
                    execute_sql_query(insert_query, mydb)
                    st.success(f'New location and plant presence saved: Latitude - {latitude}, Longitude - {longitude}')
                except Exception as e:
                    st.error(f'Failed to save new location and plant presence: {e}')
    else:
        st.warning('Please identify a plant by processing an image first.')
else:
    st.warning('Failed to capture location. Please try again.')

# Map Display
st.write("---")
st.header("🗺 Map of Plant Locations")

# Show map based on search results or uploaded image
try:
    if st.session_state.locations:
        print(st.session_state.locations) 
        df = pd.DataFrame(st.session_state.locations, columns=["Scientific_Name", "latitude", "longitude"])
        st.map(df)
    elif st.session_state.plant_name:
        locations_query = f"SELECT Scientific_Name, latitude, longitude FROM user_loc WHERE Scientific_Name = '{st.session_state.plant_name}'"
        locations = read_sql_query(locations_query, mydb)
        print(locations)

        if locations:
            df = pd.DataFrame(locations, columns=["Scientific_Name", "latitude", "longitude"])
            st.map(df)
        else:
            st.write(f"No locations available for {st.session_state.plant_name}.")
    else:
        st.write("Please process an image or search for a plant to see its locations.")
except Exception as e:
    st.error(f"An error occurred while fetching locations: {e}")




# Run the chat UI
chat_ui()