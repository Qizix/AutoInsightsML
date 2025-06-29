from os import write
import streamlit as st
import pandas as pd
from services import DataCleaner, DataLoader

# Load menu
file = None
st.title("Auto Insights")
if not file:
    file = st.file_uploader("Upload your CSV", type="csv")

# Frame with data
if "dl" not in st.session_state:
    dl = DataLoader(file)
    st.session_state["dl"] = dl

dataframe = st.session_state["dl"].dataframe()
st.write(st.session_state["dl"].check_nulls())
# st.write(dl.define_columns())
st.data_editor(dataframe)

# Action buttons
fill_missing_values_button, _, _ = st.columns(3)
if fill_missing_values_button.button("Fill missing values", use_container_width=True):
    dc = DataCleaner(st.session_state["dl"].dataframe(), st.session_state["dl"].define_columns())
    st.session_state["dl"].df = dc.handle_missing()
    st.experimental_rerun()

