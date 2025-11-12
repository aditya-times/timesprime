
import streamlit as st
import json

# Load offers data
with open("offers.json", "r") as f:
    offers = json.load(f)

st.set_page_config(page_title="AI Bundling Prototype", layout="centered")
st.title("🎁 Personalized Subscription Bundler")
st.write("Answer a few quick questions and we’ll design a personalized Times Prime–style bundle for you!")

# --- Questionnaire ---
with st.form("bundle_form"):
    st.subheader("Tell us about yourself:")
    entertainment = st.selectbox("What kind of entertainment do you enjoy most?", 
                                 ["Movies & Shows", "Sports", "Music", "News"])
    food_freq = st.selectbox("How often do you order food online?", 
                             ["Rarely", "Occasionally", "Frequently"])
    fitness_interest = st.radio("Are you into fitness or wellness?", ["Yes", "No"])
    travel_freq = st.selectbox("How often do you travel?", 
                               ["Rarely", "Occasionally", "Frequently"])
    budget = st.slider("Your monthly budget for subscriptions (₹)", 500, 5000, 2000, step=500)
    submitted = st.form_submit_button("Generate My Bundle")

# --- Simple rule-based recommendation ---
if submitted:
    st.subheader("Your Recommended Bundle")

    selected_offers = []

    # Entertainment logic
    if entertainment in ["Movies & Shows", "Sports"]:
        selected_offers += [o for o in offers if o["category"] == "Entertainment"]
    elif entertainment == "Music":
        selected_offers += [o for o in offers if o["name"] == "MUBI Subscription"]
    elif entertainment == "News":
        selected_offers += [o for o in offers if o["category"] == "Reading"]

    # Food preference
    if food_freq in ["Occasionally", "Frequently"]:
        selected_offers += [o for o in offers if o["category"] == "Food"]

    # Fitness
    if fitness_interest == "Yes":
        selected_offers += [o for o in offers if o["category"] in ["Fitness", "Wellness"]]

    # Travel
    if travel_freq in ["Occasionally", "Frequently"]:
        selected_offers += [o for o in offers if o["category"] == "Travel"]

    # Remove duplicates
    unique_offers = {o["id"]: o for o in selected_offers}.values()

    # Calculate totals
    total_value = sum(o["value"] for o in unique_offers)
    suggested_price = int(total_value * 0.6)

    # Show bundle results
    for o in unique_offers:
        st.markdown(f"**{o['name']}** — ₹{o['value']}  \n*{o['description']}*")

    st.write("---")
    st.metric("Total Value", f"₹{total_value}")
    st.metric("Suggested Bundle Price", f"₹{suggested_price}")

    if suggested_price > budget:
        st.warning("⚠️ This bundle may exceed your preferred budget.")
    else:
        st.success("✅ Perfect! This bundle fits within your budget.")

    st.write("*(Mock data only — this is a prototype demo)*")
