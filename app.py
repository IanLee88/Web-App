import streamlit as st
import pandas as pd
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('receipts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts 
                 (merchant TEXT, date TEXT, amount REAL, currency TEXT)''')
    conn.commit()
    return conn

# --- WEB APP INTERFACE ---
st.set_page_config(page_title="Receipt Processor", page_icon="🧾")

st.title("Receipt Review Form")
st.write("Review and edit the data extracted from **Receipt.jpg** below.")

# Pre-filled data from our extraction
initial_data = {
    "merchant": "Q-Q FOOD RETAIL SDN BHD",
    "date": "05/05/2026",
    "total_amount": 42.90,
    "currency": "RM"
}

# Create the Form
with st.form("receipt_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        merchant = st.text_input("Merchant Name", value=initial_data["merchant"])
        date = st.text_input("Date (DD/MM/YYYY)", value=initial_data["date"])
    
    with col2:
        amount = st.number_input("Total Amount", value=initial_data["total_amount"], format="%.2f")
        currency = st.text_input("Currency", value=initial_data["currency"])

    submit_button = st.form_submit_button("Save to Database")

# Handling the Submit
if submit_button:
    if not merchant or not date or not currency:
        st.error("⚠️ All fields must be filled before saving!")
    else:
        if amount <= 0:
            st.error("Invalid amount! The total amount must be greater than 0.")
        else:
            conn = init_db()
            c = conn.cursor()
            c.execute("INSERT INTO receipts VALUES (?, ?, ?, ?)", (merchant, date, amount, currency))
            conn.commit()
            conn.close()
            st.success(f"Successfully saved transaction for {merchant}!")

# --- VIEW SAVED DATA ---
if st.checkbox("Show saved receipts"):
    conn = sqlite3.connect('receipts.db')
    df = pd.read_sql_query("SELECT * FROM receipts", conn)
    df.index = df.index + 1
    st.dataframe(df.style.format({"amount": "{:.2f}"}))
    conn.close()

if st.sidebar.button("🗑️ Clear All Data"):
    conn = sqlite3.connect('receipts.db')
    c = conn.cursor()
    # DELETE FROM removes all rows but keeps the table structure
    c.execute("DELETE FROM receipts")
    conn.commit()
    conn.close()
    st.sidebar.success("All data cleared!")
    st.rerun() # Refresh the app to update the table display