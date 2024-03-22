import streamlit as st
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os
from PIL import Image
import io

load_dotenv()

mongo_url = os.getenv("MONGO_URL")

# MongoDB connection
client = MongoClient(f"mongodb+srv://shieldinnovsense:{mongo_url}")
db = client["CampusGuard"]
collection = db["RecordedIncidents1"]  # Change collection name accordingly

data = {
    'Time Stamp': [],
    'Reported_type': [],
    'Name': [],
    'Roll No': [],
    'Department': [],
    'Vehicle No': [],
    'Class': [],
    'Location': [],
    'Bounding Img': [],
    'Collage Img': []
}

# Main display logic
st.title("CampusGuard - Incident Reports")

reports = collection.find({})  # Fetch all records from the collection

show_content = st.checkbox("Show Content")

for report in reports:
    if show_content:
        st.subheader(f"Class: {report['Class']}")
        if report['Reported_type']:
            st.write(f"Reported Type: {report['Reported_type']}")
        if report['timestamp']:
            st.write(f"Timestamp: {report['timestamp']}")
        if report['Name']:
            st.write(f"Name: {report['Name']}")
        if report['Roll No']:
            st.write(f"Roll No: {report['Roll No']}")
        if report['Department']:
            st.write(f"Department: {report['Department']}")
        if report['Vehicle No']:
            st.write(f"Vehicle No: {report['Vehicle No']}")
        if report['location']:
            st.write(f"Location: {report['location']}")

        # Display bounding image
        if report['Bounding Img']:
            bounding_img = Image.open(io.BytesIO(report['Bounding Img']))
            st.image(bounding_img, caption='Bounding Image', use_column_width=True)

        # Display collage image
        if report['Collage Img']:
            collage_img = Image.open(io.BytesIO(report['Collage Img']))
            st.image(collage_img, caption='Collage Image', use_column_width=True)

        st.write("-" * 20)

    # Append data to dictionary for DataFrame
    data['Time Stamp'].append(report['timestamp'])
    data['Reported_type'].append(report['Reported_type'])
    data['Name'].append(report['Name'])
    data['Roll No'].append(report['Roll No'])
    data['Department'].append(report['Department'])
    data['Vehicle No'].append(report['Vehicle No'])
    data['Class'].append(report['Class'])
    data['Location'].append(report['location'])
    data['Bounding Img'].append(report['Bounding Img'])
    data['Collage Img'].append(report['Collage Img'])

# Create DataFrame from fetched data
df = pd.DataFrame(data)

# Display DataFrame
st.write(df)
