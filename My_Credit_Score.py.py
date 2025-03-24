import streamlit as st
import sqlite3

# Set page title and icon
st.set_page_config(
    page_title="VZ Credit Score App",  # Browser tab title
    page_icon="📊",  # Optional: Add an icon
)

# Database setup
def init_db():
    conn = sqlite3.connect("credit_scores.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS credit_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            credit_score REAL,
            risk_category TEXT,
            recommended_products TEXT
        )"""
    )
    conn.commit()
    conn.close()

# Save assessment to database
def save_to_db(customer_name, credit_score, risk_category, recommended_products):
    conn = sqlite3.connect("credit_scores.db")
    c = conn.cursor()
    c.execute(
        """INSERT INTO credit_assessments (customer_name, credit_score, risk_category, recommended_products)
        VALUES (?, ?, ?, ?)""",
        (customer_name, credit_score, risk_category, recommended_products),
    )
    conn.commit()
    conn.close()

# Get credit history score
def get_credit_history_score(is_new_customer):
    if is_new_customer:
        options = [
            "Regular inflows and outflows, consistent savings, and no loans.",
            "Regular inflows and outflows, no savings, and no loans.",
            "Regular inflows and outflows, no savings, with loans.",
            "Moderate transaction activity, consistent savings, and no loans.",
            "Moderate transaction activity, no savings, and no loans.",
            "Moderate transaction activity, no savings, with loans.",
            "Irregular transactions, consistent savings, and no loans.",
            "Irregular transactions, no savings, and no loans.",
            "Irregular transactions, no savings, with loans.",
            "No credit history data.",
        ]
        choice = st.selectbox("Select Credit History (New Customer):", options)
        return 10 - options.index(choice)  # Raw score is inversely proportional to choice
    else:
        options = [
            "100% Collections Rate",
            "90% Collections Rate",
            "80% Collections Rate",
            "70% Collections Rate",
            "60% Collections Rate",
            "50% Collections Rate",
            "40% Collections Rate",
            "30% Collections Rate",
            "20% Collections Rate",
            "10% Collections Rate",
        ]
        choice = st.selectbox("Select Credit History (Existing Customer):", options)
        return 10 - options.index(choice)  # Raw score is inversely proportional to choice

# Get income stability score
def get_income_stability_score():
    monthly_income = st.number_input("Enter Customer's Monthly Income (ZMW):", min_value=0.0)
    if monthly_income > 10000:
        return 10
    elif 7000 <= monthly_income <= 10000:
        return 9
    elif 5000 <= monthly_income <= 6999:
        return 8
    elif 3000 <= monthly_income <= 4999:
        return 7
    elif 2000 <= monthly_income <= 2999:
        return 6
    elif 1000 <= monthly_income <= 1999:
        return 5
    elif 500 <= monthly_income <= 999:
        return 4
    elif 300 <= monthly_income <= 499:
        return 3
    elif 100 <= monthly_income <= 299:
        return 2
    else:
        return 1

# Get location score
def get_location_score():
    distance = st.number_input("Enter Distance from Nearest Agent/Service Center (km):", min_value=0.0)
    if distance < 1:
        return 10
    elif 1 <= distance < 5:
        return 9
    elif 5 <= distance < 10:
        return 8
    elif 10 <= distance < 20:
        return 7
    elif 20 <= distance < 30:
        return 6
    elif 30 <= distance < 50:
        return 5
    elif 50 <= distance < 70:
        return 4
    elif 70 <= distance < 100:
        return 3
    elif 100 <= distance < 150:
        return 2
    else:
        return 1

# Get banking access score
def get_banking_access_score():
    options = [
        "Access to all financial services (traditional banking, mobile money, agent networks, SACCOs, etc.).",
        "Access to traditional banking services, mobile money platforms, and agent networks.",
        "Access to traditional banking services and mobile money platforms.",
        "Access to traditional banking services (e.g., bank account).",
        "Access to mobile money platforms, agent networks, and SACCOs.",
        "Access to mobile money platforms, agent networks, and informal savings groups.",
        "Access to mobile money platforms and agent banking networks.",
        "Access to mobile money platforms only (e.g., Airtel Money, MTN Mobile Money).",
        "Access to mobile money agents only.",
        "No access to any financial services.",
    ]
    choice = st.selectbox("Select Access to Banking/Financial Services:", options)
    return 10 - options.index(choice)  # Raw score is inversely proportional to choice

# Get referral score
def get_referral_score():
    options = [
        "Sales Agent/Staff (VITALITE)",
        "Existing Customer (good repayment history)",
        "Employer (formal employment)",
        "Commissioner of Oaths (legal authority)",
        "Community Leader (e.g., village head, pastor)",
        "Next of Kin (immediate family member)",
        "Local Business Owner (established business)",
        "Teacher/Educator (recognized professional)",
        "Neighbor (known to the customer)",
        "No Referral/Guarantor",
    ]
    choice = st.selectbox("Select Referral/Guarantor Type:", options)
    return 10 - options.index(choice)  # Raw score is inversely proportional to choice

# Calculate credit score
def calculate_credit_score(credit_history, income_stability, location, banking_access, referral):
    weighted_credit_history = credit_history * 0.30
    weighted_income_stability = income_stability * 0.25
    weighted_location = location * 0.15
    weighted_banking_access = banking_access * 0.20
    weighted_referral = referral * 0.10

    credit_score = (
        weighted_credit_history
        + weighted_income_stability
        + weighted_location
        + weighted_banking_access
        + weighted_referral
    )
    return credit_score

# Determine risk category
def get_risk_category(credit_score):
    if credit_score > 8:
        return "Low Risk"
    elif 5 <= credit_score <= 8:
        return "Medium Risk"
    elif 3 <= credit_score < 5:
        return "High Risk"
    else:
        return "Rejected"

# Get recommended products
def get_recommended_products(risk_category):
    if risk_category == "Low Risk":
        return "All Products"
    elif risk_category == "Medium Risk":
        return "Mid Value Products"
    elif risk_category == "High Risk":
        return "Low Value Products"
    else:
        return "Rejected (No Products Recommended)"

# Main function
def main():
    st.title("VZ Credit Score App")  # Updated app name
    st.write("This app helps sales agents assess a customer's creditworthiness.")

    # Initialize database
    init_db()

    # Input customer details
    customer_name = st.text_input("Enter Customer Name:")
    is_new_customer = st.radio("Is the customer new?", ("Yes", "No")) == "Yes"

    # Get raw scores for each risk factor
    credit_history = get_credit_history_score(is_new_customer)
    income_stability = get_income_stability_score()
    location = get_location_score()
    banking_access = get_banking_access_score()
    referral = get_referral_score()

    # Calculate credit score
    credit_score = calculate_credit_score(credit_history, income_stability, location, banking_access, referral)

    # Determine risk category and recommended products
    risk_category = get_risk_category(credit_score)
    recommended_products = get_recommended_products(risk_category)

    # Display results
    st.subheader("Credit Assessment Results")
    st.write(f"Customer Name: {customer_name}")
    st.write(f"Credit Score: {credit_score:.2f}")
    st.write(f"Risk Category: {risk_category}")
    st.write(f"Recommended Products: {recommended_products}")

    # Save results to database
    if st.button("Save Assessment"):
        save_to_db(customer_name, credit_score, risk_category, recommended_products)
        st.success("Assessment saved to database!")

    # Add a reset button
    if st.button("Reset/Restart App"):
        st.experimental_rerun()


if __name__ == "__main__":
    main()