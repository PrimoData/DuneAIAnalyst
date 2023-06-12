import streamlit as st
import os
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import requests
import json

# Configure Streamlit Page
page_icon = "https://dune.com/assets/DuneLogoCircle.svg"
st.set_page_config(page_title="DuneAI", page_icon=page_icon, layout="wide")

# Read Custom CSS
with open("assets/css/style.css", "r") as f:
    css_text = f.read()
custom_css = f"<style>{css_text}</style>"
st.markdown(custom_css, unsafe_allow_html=True)

# OpenAI "powered by" component
powered_by = """
<div style="display: flex; align-items: center;">
    <span style="font-size: 14px; margin-right: 4px; font-style: italic;">Powered by:</span>
    <img src="https://www.freelogovectors.net/wp-content/uploads/2023/01/openai-logo-freelogovectors.net_.png" alt="OpenAI logo" height="24">
</div>
"""

# Get API Keys
openai_api_key = os.environ["OPENAI_KEY"]
dune_api_key = os.environ["DUNE_KEY"]

# Setup Pandas AI
llm = OpenAI(openai_api_key)
pandas_ai = PandasAI(llm, save_charts=True)


# Query Dune Analytics using API
def query_dune(q):
    url = f"https://api.dune.com/api/v1/query/2296642/results?api_key={dune_api_key}"
    response = requests.get(url)
    results_json = json.loads(response.text)["result"]["rows"]
    results_df = pd.DataFrame.from_dict(results_json)
    return results_df


# Load data
@st.cache_data(show_spinner="Pulling Dune data...")
def load_data():
    # https://dune.com/queries/2296642
    q = "2296642"
    df = query_dune(q)
    return df


# Fetch data
df = load_data()

# Sidebar
st.image(
    "https://cdn.sanity.io/images/22xmfoma/production/e8ff6d4fe83614b4b7ed6ea9e864cf526c4c0e3c-2134x293.png",
    width=150,
)
st.markdown(powered_by, unsafe_allow_html=True)
st.header("Dune AI")
st.info("This is an experimental AI tool to analyze data using natural language.")

# Body
queryid = st.text_input("Enter a Dune query id:", help="")
submit_queryid = st.button("Pull Query Data")
st.table(df.head())

question = st.text_input("Ask me a question or tell me to plot something.", help="")
submit_question = st.button("Submit")

# Display the text when the button is clicked
"""
if submit_question:
    st.write("Question:", question)
    st.write("Thinking...")
    answer = pandas_ai(df, prompt=question)

    try:
        # Display image if generated
        pattern = r"Charts saved to: (.*)"
        file_path = re.search(pattern, answer).group(1)
        st.image(f"{file_path}/chart.png")
    except:
        # Otherwise display text
        st.write("Answer:", answer)
"""
