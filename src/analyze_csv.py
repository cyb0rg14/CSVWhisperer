import pandas
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components

def analyzeCSV(csv_file):
    # load csv
    df = pandas.read_csv(csv_file)

    # Use PygWalker to display data and visualization
    pyg_html = pyg.walk(df, return_html=True)
    components.html(pyg_html, height=1000, scrolling=True)