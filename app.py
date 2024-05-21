from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

import streamlit as st
import os
import mysql.connector

import google.generativeai as genai

## Configure GenAI Key
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
print(f"Using Google Application Credentials from: {credentials_path}")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))




#DB Connection and configuration
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "herbalhug"
)

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function To retrieve query from the database

def read_sql_query(sql,db):
    cur=db.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the table named plantsf and has the following columns - 
 ID,Plant_Name,Scientific_Name,Common_Name,Family_Name,Uses
\n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM plantsf ;
    \nExample 2 - Tell me all the plants which are from the Family_Name Sapindaceae, 
    the SQL command will be something like this SELECT * FROM plantsf
    where Family_Name="Sapindaceae"; 
    \nExample 3 - List the Common_Name and Uses of all Sapindaceae plants, 
    the SQL command will be something like this SELECT Common_Name, Uses FROM plantsf
    WHERE Family_Name = 'Sapindaceae';
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="SQL LLM")
st.header("Herbal Hug")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,mydb)
    st.subheader("Output")
    for row in response:
        print(row)
        st.header(row)