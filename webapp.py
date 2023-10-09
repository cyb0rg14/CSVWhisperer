import streamlit as st
from constants import *
from streamlit_option_menu import option_menu
from src.chat_with_csv import chatWithCSV
from src.analyze_csv import analyzeCSV

# Set Basic Page Configuration
st.set_page_config(
    page_title="StatEase",
    page_icon="📈",
    layout="wide",
)

# Choose one of the following
selected_option = option_menu(
    menu_title=None ,  
    options=["Chat With Your CSV", "Analyze Your CSV"],
    icons=["chat-right-text", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)


# Sidebar Settings
with st.sidebar:
    st.image(f"{CURRENT_PATH}/assets/banner.png", width=270)
    # csv_file = st.selectbox(label="Choose one of following dataset:", options=datasets)
    csv_file = st.file_uploader("Choose a CSV file", type=["csv"])


# Main Content
if __name__ == "__main__":
    if selected_option == "Chat With Your CSV":
        if csv_file: chatWithCSV(csv_file)
    elif selected_option == "Analyze Your CSV":
        if csv_file: analyzeCSV(csv_file)