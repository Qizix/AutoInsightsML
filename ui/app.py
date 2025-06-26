import streamlit as st
import requests

st.title("Auto Insights")

file = st.file_uploader("Upload your CSV", type="csv")
if file:
    response = requests.post("http://backend:8000/analyze", files={"file": file})
    st.json(response.json())
