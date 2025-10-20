from classifier import classify_csv
import pandas as pd
import streamlit as st
import os

def col_name_processing(df):
    df.columns = [col.lower() for col in df.columns]
    map = {
        'src': 'source',
        'source': 'source',
        'sources': 'source',
        'message': 'log_message',
        'messages': 'log_message',
        'log': 'log_message',
        'logs': 'log_message'
    }
    df.columns = [map.get(col, col) for col in df.columns]


st.title("Log Message Classifier")

st.write("Upload a CSV file with `source` and `log_message` columns to classify the logs.")

# --- Upload a csv file if not choose the sample file using the Use sample csv file button
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
use_sample = st.button("Use Sample CSV File")

# --- Handle sample selection ---
if "df" not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.success("✅ File uploaded successfully!")

elif use_sample:
    sample_path = os.path.join(os.path.dirname(__file__), "test.csv")
    try:
        df = pd.read_csv(sample_path)
        st.session_state.df = df
        st.success("✅ Loaded sample.csv successfully!")
    except FileNotFoundError:
        st.error("❌ sample.csv not found in the project directory.")
        st.stop()

# --- If df exists in session_state then only the below code runs
if st.session_state.df is not None:
    df = st.session_state.df
    col_name_processing(df)

    if st.button("Run Log Classification"):
        with st.spinner("Classifying... Please wait..."):
            output_path = classify_csv(df)

        st.success("🎉 Classification complete!")

        # Display the classified output
        df_result = pd.read_csv(output_path)
        st.subheader("🧾 Classified Results:")
        if df_result.shape[0] < 20:
            st.dataframe(df_result, use_container_width=True)
        else:
            st.dataframe(df_result.head(20))

        # Download button
        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Classified CSV",
                data=f,
                file_name="classified_output.csv",
                mime="text/csv"
            )

