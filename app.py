from os import write
import streamlit as st
import pandas as pd
from services import DataCleaner, DataLoader

st.title("Auto Insights")

# load data, data loaded in object DataLoader
if "dl" not in st.session_state:
    file = st.file_uploader("Upload your CSV", type="csv")
    dl = DataLoader(file)
    st.session_state["dl"] = dl
    st.rerun()

# showing table
st.write(st.session_state["dl"].check_nulls()) # need to show as additional columns under the table
st.dataframe(st.session_state["dl"].check_nulls().to_frame().T)

st.data_editor(st.session_state["dl"].dataframe())

# Action buttons
fill_missing_values_button, _, _ = st.columns(3)
# Fill missing data, using DataCleaner
if fill_missing_values_button.button("Fill missing values", use_container_width=True):
    dc = DataCleaner(st.session_state["dl"].dataframe(), st.session_state["dl"].define_columns())
    st.session_state["dl"].df = dc.handle_missing()
    st.rerun()

