import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from dotenv import load_dotenv
import os
import mysql.connector
import google.generativeai as genai
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure GenAI Key
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
print(f"Using Google Application Credentials from: {credentials_path}")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# DB Connection and configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="herbalhug"
)

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

# Function to execute SQL insert queries
def execute_sql_query(sql, db):
    cur = db.cursor()
    cur.execute(sql)
    db.commit()

# Function to load Gemini model and get responses from image
def get_gemini_response_from_image(image_bytes):
    model = genai.GenerativeModel('gemini-pro-vision')
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')
    response = model.generate_content(['The image shows a medicinal/ayurvedic plant/tree leaf. Identify the leaf. Give only the scientific name and nothing else. It should be only two word answer.', image])
    plant_name = response.text.strip()
    print("\nItem identified: ", plant_name)
    return plant_name

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the table named plantsf and has the following columns - 
    ID, Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses
    \n\nFor example,
    \nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM plantsf ;
    \nExample 2 - Tell me all the plants which are from the Family_Name Sapindaceae, 
    the SQL command will be something like this: SELECT * FROM plantsf
    where Family_Name="Sapindaceae"; 
    \nExample 3 - List the Common_Name and Uses of all Sapindaceae plants, 
    the SQL command will be something like this: SELECT Common_Name, Uses FROM plantsf
    WHERE Family_Name = 'Sapindaceae';
    The SQL code should not have ``` at the beginning or end and the sql word in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="Herbal Hug", layout="wide")

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Search")
    question = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")
    if submit:
        response = get_gemini_response(question, prompt)
        response = read_sql_query(response, mydb)
        st.subheader("Output")
        for row in response:
            st.write(row)

with col2:
    st.title('Herbal Hug')
    st.subheader('Welcome to Herbal Hug! Navigate the World of Herbal Health')
    image_question = "what is the thing in this image? Give one word answer only, never give more than 1 word answer. Make it a general answer. Do not give brand name. Do not answer human, person or animal, identify just the plant in the image. It is a medicinal plant."
    
    uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'png'])
    process_image = st.button("Process Image")
    
    plant_name = None
    
    if process_image and uploaded_file is not None:
        try:
            image_bytes = uploaded_file.read()
            plant_name = get_gemini_response_from_image(image_bytes).strip()
            if plant_name:
                st.success(f'Plant identified: {plant_name}')
                sql_query = f"SELECT Plant_Name, Scientific_Name, Common_Name, Family_Name, Uses FROM plantsf WHERE Scientific_Name='{plant_name}'"
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
    
    if plant_name:
        insert_query = f"INSERT INTO user_loc (Scientific_Name, Latitude, Longitude, Date_found, Last_Confirmed) VALUES ('{plant_name}', {latitude}, {longitude}, CURRENT_DATE, CURRENT_DATE)"
        try:
            execute_sql_query(insert_query, mydb)
            st.success(f'Location and plant name saved: Latitude - {latitude}, Longitude - {longitude}')
        except Exception as e:  
            st.error(f'Failed to save location and plant name: {e}')
    else:
        st.warning('Please identify a plant by processing an image first.')
else:
    st.warning('Failed to capture location. Please try again.')
