import streamlit as st
import pandas as pd
import chardet
from modules.calculations import compute_tam, compute_sam, compute_som

# --- Page Setup ---
st.set_page_config(page_title="Finvij TAM/SAM/SOM Estimator", layout="wide")
st.title("📊 Finvij TAM / SAM / SOM Dashboard")

# --- Load Data ---
with open("data/Banks_NewList.csv", 'rb') as f:
    result = chardet.detect(f.read(50000))
banks_encoding = result['encoding']

banks = pd.read_csv("data/Banks_NewList.csv", encoding=banks_encoding, on_bad_lines='skip')
nbfcs = pd.read_csv("data/NBFC_NewList.csv", encoding='cp1252', on_bad_lines='skip')

st.sidebar.header("Operational Inputs")

# --- Sidebar Inputs ---
ticket_size = st.sidebar.number_input("Average Deal Size (₹ Lakhs)", 10, 1000, 50)
arr_per_person = st.sidebar.number_input("ARR per Person (₹ Lakhs)", 1, 100, 25)
team_size = st.sidebar.slider("Team Size", 1, 50, 5)

# --- Filters ---
st.sidebar.subheader("Market Filters")
regions = st.sidebar.multiselect("Select Region(s)", banks['region'].dropna().unique())
aum_min = st.sidebar.number_input("Min AUM (₹ Cr)", 0)
aum_max = st.sidebar.number_input("Max AUM (₹ Cr)", 100000)

filters = {"region": regions, "aum_min": aum_min, "aum_max": aum_max}

# --- Tabs for Banks & NBFCs ---
tab1, tab2 = st.tabs(["🏦 Banks", "💰 NBFCs"])

with tab1:
    st.subheader("Bank Market")
    tam_banks = compute_tam(banks, ticket_size)
    sam_banks = compute_sam(banks, filters)
    som_banks = compute_som(sam_banks, arr_per_person, team_size)

    st.metric("TAM (Banks)", tam_banks)
    st.metric("SAM (Banks Count)", len(sam_banks))
    st.metric("SOM (Reachable Market)", som_banks)
    st.dataframe(sam_banks.head(10))

with tab2:
    st.subheader("NBFC Market")
    tam_nbfc = compute_tam(nbfcs, ticket_size)
    sam_nbfc = compute_sam(nbfcs, filters)
    som_nbfc = compute_som(sam_nbfc, arr_per_person, team_size)

    st.metric("TAM (NBFCs)", tam_nbfc)
    st.metric("SAM (NBFC Count)", len(sam_nbfc))
    st.metric("SOM (Reachable Market)", som_nbfc)
    st.dataframe(sam_nbfc.head(10))

st.caption("💡 Tip: Adjust filters in the sidebar to see live changes in TAM/SAM/SOM.")
