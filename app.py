import streamlit as st

from services import DataCleaner, DataLoader

st.title("Auto Insights")

# load data, data loaded in object DataLoader
if "dl" not in st.session_state:
    file = st.file_uploader("Upload your CSV", type="csv")
    if file:
        dl = DataLoader(file)
        st.session_state["dl"] = dl
        st.session_state["file_name"] = file.name
        st.rerun()
else:
    # show missing data count for each column
    st.write(st.session_state['file_name'])
    st.dataframe(st.session_state["dl"].check_nulls().to_frame().T)
    st.data_editor(st.session_state["dl"].dataframe())
    st.write("DataFrame shape:", st.session_state["dl"].df.shape)

    with st.expander("Missing data and duplicates handling"):
        fill_missing_values, drop_missing_values, drop_duplicates = st.columns(3)
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
                    ["text", "mode"],
                    default="text",
                    disabled=is_missing,
                )
                text_value = st.text_input(
                    "Categorical filling text", value="Unknown", disabled=is_missing
                )

            if fill_missing_values_button:
                dc = DataCleaner(
                    st.session_state["dl"].dataframe(),
                    st.session_state["dl"].define_columns(),
                )
                if col_strat == "text":
                    col_strat = text_value
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
                    "How much % missing data needed to drop:",
                    options=range(101),
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

        with drop_duplicates:
            if st.button("Drop duplicates", use_container_width=True):
                dc = DataCleaner(
                    st.session_state["dl"].dataframe(),
                    st.session_state["dl"].define_columns(),
                )
                st.session_state["dl"].df = dc.drop_duplicates()
                st.rerun()

    with st.expander("Categorical data encoding"):
        (
            data_encode_type_column,
            data_encode_columns_column,
            data_encode_button_column,
        ) = st.columns(3)

        with data_encode_type_column:
            encode_method = st.selectbox(
                "Select control type", ["one-hot", "label"]
            )

        with data_encode_columns_column:
            data_encode_columns = st.multiselect(
                    "Select columns for encoding",
                    st.session_state["dl"].define_columns()['categorical']
                    )
        with data_encode_button_column:
            data_encode_button = st.button("Encode data", use_container_width=True)

        if data_encode_button:
            dc = DataCleaner(
                st.session_state["dl"].dataframe(),
                st.session_state["dl"].define_columns(),
            )
            st.session_state["dl"].df = dc.encode_categorical(
                data_encode_columns, method=encode_method
            )
            st.rerun()

    st.download_button(
        "Save table in csv format",
        use_container_width=True,
        data=st.session_state["dl"].save_csv(),
        file_name=st.session_state['file_name'],
        mime="text/csv",
    )
