import streamlit as st
import numpy as np
from scipy.stats import poisson

# Title and Intro
st.title("Advanced Sports Betting Predictor")
st.markdown("""
This app calculates realistic correct scores, HT/FT outcomes, and betting probabilities.
It also provides AI recommendations for the most profitable bets with detailed calculations for maximum margin and ROI.
""")

# Input Section
st.header("Input Betting Odds and Parameters")
col1, col2 = st.columns(2)

# Halftime Odds
with col1:
    st.subheader("Halftime Odds")
    ht_home = st.number_input("Halftime Home Odds", min_value=1.0, step=0.1)
    ht_draw = st.number_input("Halftime Draw Odds", min_value=1.0, step=0.1)
    ht_away = st.number_input("Halftime Away Odds", min_value=1.0, step=0.1)

# Full-time Odds
with col2:
    st.subheader("Full-time Odds")
    ft_home = st.number_input("Fulltime Home Odds", min_value=1.0, step=0.1)
    ft_draw = st.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1)
    ft_away = st.number_input("Fulltime Away Odds", min_value=1.0, step=0.1)

# Correct Score Odds (HT and FT)
st.sidebar.write("Correct Score Odds (Max 4:4)")

correct_score_odds = {
    "0:0": st.sidebar.number_input("Odds for 0:0", value=9.10, step=0.01),
    "0:1": st.sidebar.number_input("Odds for 0:1", value=14.50, step=0.01),
    "0:2": st.sidebar.number_input("Odds for 0:2", value=44.00, step=0.01),
    "0:3": st.sidebar.number_input("Odds for 0:3", value=210.00, step=0.01),
    "0:4": st.sidebar.number_input("Odds for 0:4", value=250.00, step=0.01),
    "1:0": st.sidebar.number_input("Odds for 1:0", value=5.30, step=0.01),
    "1:1": st.sidebar.number_input("Odds for 1:1", value=7.80, step=0.01),
    "1:2": st.sidebar.number_input("Odds for 1:2", value=25.00, step=0.01),
    "1:3": st.sidebar.number_input("Odds for 1:3", value=115.00, step=0.01),
    "1:4": st.sidebar.number_input("Odds for 1:4", value=250.00, step=0.01),
    "2:0": st.sidebar.number_input("Odds for 2:0", value=5.80, step=0.01),
    "2:1": st.sidebar.number_input("Odds for 2:1", value=8.90, step=0.01),
    "2:2": st.sidebar.number_input("Odds for 2:2", value=26.00, step=0.01),
    "2:3": st.sidebar.number_input("Odds for 2:3", value=125.00, step=0.01),
    "2:4": st.sidebar.number_input("Odds for 2:4", value=250.00, step=0.01),
    "3:0": st.sidebar.number_input("Odds for 3:0", value=9.50, step=0.01),
    "3:1": st.sidebar.number_input("Odds for 3:1", value=14.50, step=0.01),
    "3:2": st.sidebar.number_input("Odds for 3:2", value=45.00, step=0.01),
    "3:3": st.sidebar.number_input("Odds for 3:3", value=200.00, step=0.01),
    "3:4": st.sidebar.number_input("Odds for 3:4", value=250.00, step=0.01),
    "4:0": st.sidebar.number_input("Odds for 4:0", value=21.00, step=0.01),
    "4:1": st.sidebar.number_input("Odds for 4:1", value=32.00, step=0.01),
    "4:2": st.sidebar.number_input("Odds for 4:2", value=8.90, step=0.01),
    "4:3": st.sidebar.number_input("Odds for 4:3", value=250.00, step=0.01),
    "4:4": st.sidebar.number_input("Odds for 4:4", value=250.00, step=0.01)
}

# Halftime Correct Score Odds
st.subheader("Correct Score Odds (HT)")
score_1_0_odds = st.number_input("Odds for 1-0 (HT)", min_value=0.0, value=3.10)
score_0_0_odds = st.number_input("Odds for 0-0 (HT)", min_value=0.0, value=2.50)
score_0_1_odds = st.number_input("Odds for 0-1 (HT)", min_value=0.0, value=8.30)
score_2_0_odds = st.number_input("Odds for 2-0 (HT)", min_value=0.0, value=7.50)
score_1_1_odds = st.number_input("Odds for 1-1 (HT)", min_value=0.0, value=10.50)
score_0_2_odds = st.number_input("Odds for 0-2 (HT)", min_value=0.0, value=58.00)
score_2_1_odds = st.number_input("Odds for 2-1 (HT)", min_value=0.0, value=26.00)
score_2_2_odds = st.number_input("Odds for 2-2 (HT)", min_value=0.0, value=185.00)
score_1_2_odds = st.number_input("Odds for 1-2 (HT)", min_value=0.0, value=74.00)

# BTTS and Over/Under Odds
st.subheader("BTTS and Over/Under Odds")
btts_gg = st.number_input("BTTS GG Odds", min_value=1.0, step=0.1)
btts_ng = st.number_input("BTTS NG Odds", min_value=1.0, step=0.1)
over_25 = st.number_input("Over 2.5 Odds", min_value=1.0, step=0.1)
under_25 = st.number_input("Under 2.5 Odds", min_value=1.0, step=0.1)

# HT Over/Under 1.5 Goals
st.subheader("HT Over/Under 1.5 Goals Odds")
ht_over_15 = st.number_input("HT Over 1.5 Goals Odds", min_value=1.0, step=0.1)
ht_under_15 = st.number_input("HT Under 1.5 Goals Odds", min_value=1.0, step=0.1)

# Process Input
if st.button("Calculate Probabilities"):
    try:
        # Define helper function for probabilities
        def calculate_poisson_prob(goal_avg, max_goals=4):
            return [poisson.pmf(i, goal_avg) for i in range(max_goals + 1)]
        
        # Calculate average goal probabilities
        ht_goal_avg = (ht_home + ht_away) / 2
        ft_goal_avg = (ft_home + ft_away) / 2

        # Calculate probabilities for halftime and full-time
        ht_probs = calculate_poisson_prob(ht_goal_avg, max_goals=2)
        ft_probs = calculate_poisson_prob(ft_goal_avg, max_goals=4)

        # Calculate HT Over/Under 1.5 goals probabilities
        ht_over_15_prob = 1 - sum(ht_probs[:2])  # Goals 2 or more
        ht_under_15_prob = sum(ht_probs[:2])  # Goals 0 or 1

        # Combine HT/FT probabilities
        combined_probs = np.outer(ht_probs, ft_probs)

        # Calculate BTTS and Over/Under probabilities
        btts_prob = 1 / btts_gg
        under_25_prob = 1 / under_25
        over_25_prob = 1 / over_25

        # Display probabilities
        st.subheader("Calculated Probabilities")
        st.write("Halftime Probabilities (0-0 to 2-2):", ht_probs)
        st.write("Fulltime Probabilities (0-0 to 4-4):", ft_probs)
        st.write("BTTS GG Probability:", f"{btts_prob * 100:.2f}%")
        st.write("Under 2.5 Probability:", f"{under_25_prob * 100:.2f}%")
        st.write("Over 2.5 Probability:", f"{over_25_prob * 100:.2f}%")
        st.write("HT Over 1.5 Goals Probability:", f"{ht_over_15_prob * 100:.2f}%")
        st.write("HT Under 1.5 Goals Probability:", f"{ht_under_15_prob * 100:.2f}%")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
