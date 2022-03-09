import streamlit as st
import pandas as pd
import apriori

st.set_page_config(layout='wide')
#For Excel File
df = pd.read_excel("Dataset.xlsx")
st.title("Customer Grocery Transactions:")
st.sidebar.title("Apriori Algorithm:")
st.write(df)
list = apriori.get_freq_item("Dataset.xlsx")
result = pd.DataFrame(list)
st.write(result)