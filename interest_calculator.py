import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Load and clean the data
file_path = 'Prompt Payment State Survey_3_22_2023.xlsx'
excel_data = pd.ExcelFile(file_path)
data_sheet1 = excel_data.parse('Sheet1', header=1)
interest_data = data_sheet1[['STATE', 'INTEREST RATE', 'WHEN IT APPLIES']]

def parse_interest_rate(rate_str):
    if 'per month' in rate_str:
        rate = float(re.search(r'[\d.]+', rate_str).group()) / 100
        rate_type = 'monthly'
    elif 'per year' in rate_str or 'per annum' in rate_str:
        rate = float(re.search(r'[\d.]+', rate_str).group()) / 100
        rate_type = 'yearly'
    else:
        rate = float(rate_str)
        rate_type = 'yearly'
    return rate, rate_type

def calculate_interest(principal, state, start_date, end_date):
    state_row = interest_data[interest_data['STATE'].str.contains(state, case=False, na=False)].iloc[0]
    interest_rate_str = state_row['INTEREST RATE']
    rate, rate_type = parse_interest_rate(interest_rate_str)
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end_date - start_date).days
    
    if rate_type == 'monthly':
        interest = principal * rate * (days / 30)
    else:
        interest = principal * rate * (days / 365)
    
    return interest

# Streamlit interface
st.title("Interest Calculator 🧮")
st.write("Calculate the amount of interest owed for a given payment based on the state and dates provided.")

principal = st.number_input("Principal Amount", min_value=0.0, value=1000.0)
state = st.selectbox("State", interest_data['STATE'].unique())
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Calculate
