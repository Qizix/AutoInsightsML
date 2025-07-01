import streamlit as st

from services import DataCleaner, DataLoader

st.title("Auto Insights")

# load data, data loaded in object DataLoader
if "dl" not in st.session_state:
    file = st.file_uploader("Upload your CSV", type="csv")
    if file:
        dl = DataLoader(file)
        st.session_state["dl"] = dl
        st.rerun()
else:
    # show missing data count for each column
    st.dataframe(st.session_state["dl"].check_nulls().to_frame().T)
    st.data_editor(st.session_state["dl"].dataframe())

    fill_missing_values, drop_missing_values, save_csv = st.columns(3)
    # Fill missing data, using DataCleaner
    with fill_missing_values:
        is_missing = bool(st.session_state["dl"].check_nulls().sum() == 0)
        fill_missing_values_button = fill_missing_values.button(
            "Fill missing values", use_container_width=True, disabled=is_missing
        )

        fill_missing_values_selectors_container = st.container(border=True)
        with fill_missing_values_selectors_container:
            num_strat = st.segmented_control(
                "Numerical filling strategy",
                ["mean", "median"],
                default="mean",
                disabled=is_missing,
            )
            col_strat = st.segmented_control(
                "Categorical filling strategy",
                ["Unknown", "mode"],
                default="Unknown",
                disabled=is_missing,
            )

        if fill_missing_values_button:
            dc = DataCleaner(
                st.session_state["dl"].dataframe(),
                st.session_state["dl"].define_columns(),
            )
            st.session_state["dl"].df = dc.handle_missing(num_strat, col_strat)
            st.rerun()

    with drop_missing_values:
        drop_missing_values_button = st.button(
            "Drop missing values", use_container_width=True, disabled=is_missing
        )
        drop_missing_values_selectors_container = st.container(border=True)
        with drop_missing_values_selectors_container:
            option_map = {0: "Rows", 1: "Cols"}
            drop_type = st.segmented_control(
                "Select drop type",
                option_map.keys(),
                disabled=is_missing,
                format_func=lambda option: option_map[option],
                default=0,
            )
            drop_rate = st.select_slider(
                "How much % missing data needed to drop:", options=range(101),
                disabled=is_missing,
            )
            if drop_missing_values_button:
                dc = DataCleaner(
                    st.session_state["dl"].dataframe(),
                    st.session_state["dl"].define_columns(),
                )
                st.session_state["dl"].df = dc.drop_with_missing_data(
                    drop_rate / 100,
                    drop_type,
                )
                st.rerun()

    with save_csv:
        st.download_button(
            "Save table in csv format",
            use_container_width=True,
            data=st.session_state["dl"].save_csv(),
            file_name="table.csv",  # need fix to loaded name
            mime="text/csv",
        )
