import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

st.title("📈 Stock Transaction Visualizer with P&L and XIRR")

uploaded_file = st.file_uploader("Upload your stock CSV file", type="csv")

def calculate_xirr(transactions):
    def xnpv(rate, txns):
        return sum([
            txn['Amount'] / (1 + rate)**((txn['Date'] - txns[0]['Date']).days / 365)
            for txn in txns
        ])

    def xirr(txns):
        try:
            return round(np.irr([txn['Amount'] for txn in txns]) * 100, 2)
        except:
            return None

    return xirr(transactions)

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    df.sort_values("Date", inplace=True)
    
    df["Amount"] = df["Quantity"] * df["Price"]
    df["Signed_Amount"] = df.apply(lambda x: -x["Amount"] if x["Type"].lower() == "buy" else x["Amount"], axis=1)
    
    st.subheader("📄 Transaction Data")
    st.dataframe(df)

    # Cumulative profit/loss
    df["Cumulative_PnL"] = df["Signed_Amount"].cumsum()

    st.subheader("📈 Cumulative Profit / Loss")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Cumulative_PnL"], marker="o")
    ax.set_ylabel("P&L (₹)")
    ax.set_xlabel("Date")
    st.pyplot(fig)

    # Pie chart - buy vs sell
    st.subheader("🥧 Buy vs Sell Volume")
    buy_total = df[df["Type"].str.lower() == "buy"]["Amount"].sum()
    sell_total = df[df["Type"].str.lower() == "sell"]["Amount"].sum()
    pie_labels = ["Buy", "Sell"]
    pie_values = [buy_total, sell_total]
    fig2, ax2 = plt.subplots()
    ax2.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

    # XIRR calculation
    st.subheader("📊 XIRR (Annualized Return)")
    txn_list = [
        {"Date": row["Date"], "Amount": row["Signed_Amount"]}
        for _, row in df.iterrows()
    ]
    xirr_result = calculate_xirr(txn_list)
    st.write(f"📌 **XIRR**: {xirr_result if xirr_result is not None else 'Could not calculate'} %")
