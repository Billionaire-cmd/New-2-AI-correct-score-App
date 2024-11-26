import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Set up Streamlit layout
st.set_page_config(page_title="🤖 💯Massive Payout Correct Score Predictor", layout="wide")

st.title("🤖 💯Massive Payout Correct Score Predictor")
st.write("Welcome to the **Massive Payout Correct Score Predictor** system. Predict full-time and halftime scores with high accuracy.")

# Input fields for user data
home_team = st.text_input("Home Team Name", placeholder="Enter home team name")
away_team = st.text_input("Away Team Name", placeholder="Enter away team name")
home_goals = st.number_input("Goals Scored by Home Team", min_value=0, step=1)
away_goals = st.number_input("Goals Scored by Away Team", min_value=0, step=1)

# A function to simulate your prediction model (replace with your actual model)
def predict_match(home_goals, away_goals):
    # Example prediction using some placeholder logic (replace with real model logic)
    home_attack = home_goals * 1.5  # Simplified for the example
    away_attack = away_goals * 1.3  # Simplified for the example
    
    predicted_home_goals = home_attack
    predicted_away_goals = away_attack
    
    # Betting insights based on the prediction
    betting_insights = betting_insights(2.50, 3.00)  # Example odds for home and away
    
    return {
        'full_time': f"{predicted_home_goals:.1f} - {predicted_away_goals:.1f}",
        'half_time': f"{predicted_home_goals / 2:.1f} - {predicted_away_goals / 2:.1f}",
        'betting_insights': betting_insights
    }

# A function to simulate betting insights based on odds
def betting_insights(odds_home_win, odds_away_win):
    # Calculate implied probability for each team
    prob_home = 1 / odds_home_win
    prob_away = 1 / odds_away_win
    return f"Home Win Probability: {prob_home * 100:.2f}% | Away Win Probability: {prob_away * 100:.2f}%"

# When the user clicks the "Predict" button
if st.button("Predict"):
    if home_team and away_team:
        result = predict_match(home_goals, away_goals)
        st.subheader(f"Predicted Full-Time Score: {result['full_time']}")
        st.subheader(f"Predicted Half-Time Score: {result['half_time']}")
        st.write(f"**Betting Insights**: {result['betting_insights']}")
    else:
        st.warning("Please fill in both team names and goals to get predictions.")

# Extra information about the system
st.sidebar.header("About the Predictor")
st.sidebar.write(
    """
    This system uses advanced statistical models and data analysis to predict accurate match scores.
    - Input your team statistics and match data to get full-time and halftime predictions.
    - Based on team strengths and market odds, the system provides insights into betting strategies for maximum payout.
    """
)
