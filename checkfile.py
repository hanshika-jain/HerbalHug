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
    # Remove code block formatting if present
    cleaned_response = response.replace('```sql', '').replace('```', '').strip()
    return cleaned_response

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return clean_query(response.text)  # Clean the query

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

# Function to execute SQL insert queries
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
    print("\nItem identified: ", plant_name)
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
if "plant_name" not in st.session_state:
    st.session_state.plant_name = None
if "locations" not in st.session_state:
    st.session_state.locations = None

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Search")
    question = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")
    if submit:
        sql_query = get_gemini_response(question, prompt)
        response = read_sql_query(sql_query, mydb)
        st.subheader("Output")
        if response:
            for row in response:
                st.write(row)
        else:
            st.write("No results found or an error occurred.")

    # Additional search box for plant name
    search_plant = st.text_input("Search for a plant:", "")
    if st.button("Search"):
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
    st.subheader('Welcome to Herbal Hug! Navigate the World of Herbal Health')

    uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'png'])
    process_image = st.button("Process Image")

    if process_image and uploaded_file is not None:
        try:
            image_bytes = uploaded_file.read()
            st.session_state.plant_name = get_gemini_response_from_image(image_bytes).strip()  # Store in session state
            if st.session_state.plant_name:
                st.success(f'Plant identified: {st.session_state.plant_name}')
                sql_query = f"SELECT Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses FROM plantsf WHERE Scientific_Name='{st.session_state.plant_name}'"
                plant_info = read_sql_query(sql_query, mydb)
                if plant_info:
                    st.subheader('Plant Information')
                    for info in plant_info:
                        st.write(f"Plant_Name: {info[0]}, Scientific_Name: {info[1]}, Common_Name: {info[2]}, Family_Name: {info[3]}, Uses: {info[4]}")
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
        # Add checkbox to confirm if the plant is present at the captured location
        plant_present = st.checkbox("Is the plant present at this location?")

        # Convert checkbox value to 1 or 0
        presence_value = 1 if plant_present else 0

        if st.button("Save Location"):
            insert_query = f"INSERT INTO user_loc (Scientific_Name, latitude, longitude, presence, Date_found, Last_Confirmed) VALUES ('{st.session_state.plant_name}', {latitude}, {longitude}, {presence_value}, CURRENT_DATE, CURRENT_DATE)"
            try:
                execute_sql_query(insert_query, mydb)
                st.success(f'Location and plant presence saved: Latitude - {latitude}, Longitude - {longitude}')
            except Exception as e:
                st.error(f'Failed to save location and plant presence: {e}')
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
        df = pd.DataFrame(st.session_state.locations, columns=["Scientific_Name", "latitude", "longitude"])
        st.map(df)
    elif st.session_state.plant_name:
        locations_query = f"SELECT Scientific_Name, latitude, longitude FROM user_loc WHERE Scientific_Name = '{st.session_state.plant_name}'"
        locations = read_sql_query(locations_query, mydb)

        if locations:
            df = pd.DataFrame(locations, columns=["Scientific_Name", "latitude", "longitude"])
            st.map(df)
        else:
            st.write(f"No locations available for {st.session_state.plant_name}.")
    else:
        st.write("Please process an image or search for a plant to see its locations.")
except Exception as e:
    st.error(f"An error occurred while fetching locations: {e}")
