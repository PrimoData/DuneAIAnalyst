import streamlit as st
import os
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import requests
import json
import re

# Configure Streamlit Page
page_icon = "https://dune.com/assets/DuneLogoCircle.svg"
st.set_page_config(page_title="Dune AI Analyst", page_icon=page_icon, layout="wide")

# Read Custom CSS
with open("assets/css/style.css", "r") as f:
    css_text = f.read()
custom_css = f"<style>{css_text}</style>"
st.markdown(custom_css, unsafe_allow_html=True)

# OpenAI "powered by" component
powered_by = """
<div style="display: flex; align-items: center; margin-bottom:20px">
    <span style="font-size: 14px; margin-right: 4px; font-style: italic;">Powered by:</span>
    <img src="https://www.freelogovectors.net/wp-content/uploads/2023/01/openai-logo-freelogovectors.net_.png" alt="OpenAI logo" height="24">
</div>
"""

# Get API Keys
openai_api_key = os.environ["OPENAI_KEY"]
dune_api_key = os.environ["DUNE_KEY"]

# Heading
st.write(
    f'<h1><img src="https://dune.com/assets/DuneLogoCircle.svg" alt="OpenAI logo" height="36" style="margin-bottom:6px">  Dune AI Analyst</h1>',
    unsafe_allow_html=True,
)
st.subheader("Analyze any Dune dataset using natural language")
st.markdown(powered_by, unsafe_allow_html=True)


# Query Dune Analytics using API
def query_dune(q):
    url = f"https://api.dune.com/api/v1/query/{q}/results?api_key={dune_api_key}"
    response = requests.get(url)
    results_json = json.loads(response.text)["result"]["rows"]
    results_df = pd.DataFrame.from_dict(results_json)
    return results_df


# Initialize Session State
if "df" not in st.session_state:
    st.session_state["df"] = ""

col1, col2 = st.columns(2)

# Query Dune
with col1:
    query = st.text_input("(1) Enter a Dune Query Id.")
    submit_query = st.button("Query Data")
    if submit_query:
        st.session_state.df = query_dune(query)
        st.table(st.session_state.df.head())
    elif isinstance(st.session_state.df, pd.DataFrame):
        st.table(st.session_state.df.head())

# Ask Question
with col2:
    # Setup Pandas AI
    llm = OpenAI(openai_api_key)
    pandas_ai = PandasAI(llm, save_charts=True)

    # Analyze Data
    question = st.text_input("(2) Ask a question or plot results.")
    submit_question = st.button("Analyze Data")

    if submit_question:
        answer = pandas_ai(st.session_state.df, prompt=question)
        try:
            # Display image if generated
            pattern = r"Charts saved to: (.*)"
            file_path = re.search(pattern, answer).group(1)
            st.image(f"{file_path}/chart.png")
        except:
            # Otherwise display text
            st.write("Answer:", answer)
