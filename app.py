import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Transactions Visualizer", layout="wide")

st.title("📈 Stock Transactions Visualizer")

uploaded_file = st.file_uploader("Upload your stock transaction CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File successfully uploaded and read!")
    st.dataframe(df)

    df["Date"] = pd.to_datetime(df["Date"])
    summary = df.groupby(["Date", "Type"]).agg({"Quantity": "sum"}).reset_index()

    st.subheader("📊 Daily Buy vs Sell Quantity")

    fig, ax = plt.subplots()
    for action in summary["Type"].unique():
        sub_df = summary[summary["Type"] == action]
        ax.bar(sub_df["Date"], sub_df["Quantity"], label=action)
    ax.set_ylabel("Quantity")
    ax.set_title("Buy vs Sell Over Time")
    ax.legend()
    st.pyplot(fig)

    st.subheader("🥧 Buy vs Sell Overall Distribution")
    type_summary = df.groupby("Type")["Quantity"].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(type_summary, labels=type_summary.index, autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

else:
    st.warning("Please upload a CSV file to visualize.")
