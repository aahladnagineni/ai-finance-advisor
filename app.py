import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# App title
st.title("💰 AI Personal Finance Advisor")
st.write("Enter your monthly finances and get personalized advice!")

# Input section
st.header("📊 Your Monthly Finances")

income = st.number_input("Monthly Income (₹)", min_value=0, value=0, step=500)

st.subheader("Monthly Expenses")
rent = st.number_input("Rent / Housing (₹)", min_value=0, value=0, step=500)
food = st.number_input("Food & Groceries (₹)", min_value=0, value=0, step=500)
transport = st.number_input("Transport (₹)", min_value=0, value=0, step=500)
entertainment = st.number_input("Entertainment (₹)", min_value=0, value=0, step=500)
other = st.number_input("Other Expenses (₹)", min_value=0, value=0, step=500)

# Calculate totals
total_expenses = rent + food + transport + entertainment + other
savings = income - total_expenses

# Show summary
st.header("📈 Your Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:,}")
col2.metric("Total Expenses", f"₹{total_expenses:,}")
col3.metric("Savings", f"₹{savings:,}", delta=f"₹{savings:,}")

# Get AI advice button
if st.button("💡 Get AI Financial Advice"):
    if income == 0:
        st.warning("Please enter your monthly income first!")
    else:
        with st.spinner("Analyzing your finances..."):
            prompt = f"""
            You are a helpful personal finance advisor. Analyze this person's monthly finances and give friendly, practical advice.

            Monthly Income: ₹{income}
            Expenses:
            - Rent/Housing: ₹{rent}
            - Food & Groceries: ₹{food}
            - Transport: ₹{transport}
            - Entertainment: ₹{entertainment}
            - Other: ₹{other}
            Total Expenses: ₹{total_expenses}
            Monthly Savings: ₹{savings}

            Please provide:
            1. A quick summary of their financial health
            2. Which areas they are overspending
            3. 3 practical tips to save more money
            4. A simple savings goal for next month

            Keep it friendly, encouraging and easy to understand.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.header("🤖 AI Advice")
            st.write(response.choices[0].message.content)

# Chat section
st.header("💬 Ask a Follow-up Question")
user_question = st.text_input("Ask anything about your finances...")

if st.button("Ask AI"):
    if user_question:
        with st.spinner("Thinking..."):
            chat_prompt = f"""
            A person has the following monthly finances:
            Income: ₹{income}, Expenses: ₹{total_expenses}, Savings: ₹{savings}
            
            They are asking: {user_question}
            
            Give a short, helpful, friendly answer.
            """
            chat_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": chat_prompt}]
            )
            st.write("🤖 " + chat_response.choices[0].message.content)
    else:
        st.warning("Please type a question first!")
