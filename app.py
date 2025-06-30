import streamlit as st

from services import DataCleaner, DataLoader

st.title("Auto Insights")

# load data, data loaded in object DataLoader
if "dl" not in st.session_state:
    file = st.file_uploader("Upload your CSV", type="csv")
    dl = DataLoader(file)
    st.session_state["dl"] = dl
    st.rerun()

# showing table
st.write(
    st.session_state["dl"].check_nulls()
)  # need to show as additional columns under the table
st.dataframe(st.session_state["dl"].check_nulls().to_frame().T)

st.data_editor(st.session_state["dl"].dataframe())

# Action buttons
fill_missing_values, qfill_missing_values_button, wfill_missing_values_button = (
    st.columns(3)
)
# Fill missing data, using DataCleaner
with fill_missing_values:
    fill_missing_values_button = fill_missing_values.button(
        "Fill missing values", use_container_width=True
    )

    fill_missing_values_selectors_container = st.container(border=True)
    with fill_missing_values_selectors_container:
        num_strat = st.segmented_control(
            "Numerical filling strategy", ["mean", "median"], default="mean"
        )
        col_strat = st.segmented_control(
            "Categorical filling strategy", ["Unknown", "mode"], default="Unknown"
        )

    if fill_missing_values_button:
        dc = DataCleaner(
            st.session_state["dl"].dataframe(), st.session_state["dl"].define_columns()
        )
        st.session_state["dl"].df = dc.handle_missing(num_strat, col_strat)
        st.rerun()


with qfill_missing_values_button:
    if qfill_missing_values_button.button("pass1", use_container_width=True):
        dc = DataCleaner(
            st.session_state["dl"].dataframe(), st.session_state["dl"].define_columns()
        )
        st.session_state["dl"].df = dc.handle_missing()
        st.rerun()
    st.segmented_control("pass1", ["meanasdf", "mediasdfn"])

with wfill_missing_values_button:
    if wfill_missing_values_button.button("pass2", use_container_width=True):
        dc = DataCleaner(
            st.session_state["dl"].dataframe(), st.session_state["dl"].define_columns()
        )
        st.session_state["dl"].df = dc.handle_missing()
        st.rerun()
    st.segmented_control("pass2", ["123mean", "234median"])
