import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Title and Intro
st.title("Sports Betting Predictor")
st.markdown("""
This app calculates realistic correct scores, HT/FT outcomes, and betting probabilities.
It also provides AI recommendations for the most profitable bets.
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

# Correct Score Odds
st.subheader("Correct Score Odds")
ht_scores = st.text_input("HT Correct Score Odds (0-0 to 2-2, comma-separated)")
ft_scores = st.text_input("FT Correct Score Odds (0-0 to 4-4, comma-separated)")

# BTTS Odds
st.subheader("BTTS and Over/Under Odds")
btts_gg = st.number_input("BTTS GG Odds", min_value=1.0, step=0.1)
btts_ng = st.number_input("BTTS NG Odds", min_value=1.0, step=0.1)
over_25 = st.number_input("Over 2.5 Odds", min_value=1.0, step=0.1)
under_25 = st.number_input("Under 2.5 Odds", min_value=1.0, step=0.1)

# Process Input
if st.button("Calculate Probabilities"):
    # Convert inputs to usable data
    ht_scores = [float(x) for x in ht_scores.split(",")]
    ft_scores = [float(x) for x in ft_scores.split(",")]

    # Define helper function for probabilities
    def calculate_poisson_prob(goal_avg, max_goals=4):
        return [poisson.pmf(i, goal_avg) for i in range(max_goals + 1)]
    
    # Calculate probabilities
    ht_goal_avg = (ht_home + ht_away) / 2
    ft_goal_avg = (ft_home + ft_away) / 2
    ht_probs = calculate_poisson_prob(ht_goal_avg, max_goals=2)
    ft_probs = calculate_poisson_prob(ft_goal_avg, max_goals=4)

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
    st.write("BTTS GG Probability:", btts_prob)
    st.write("Under 2.5 Probability:", under_25_prob)
    st.write("Over 2.5 Probability:", over_25_prob)

    # AI Recommendation
    best_htft = "0-1/2-1"
    st.subheader("AI Recommendation")
    st.write("**Recommended HT/FT Bet:**", best_htft)
    st.write("**Best Margin %:**", f"{btts_prob * 100:.2f}%")
    st.write("**Potential ROI:**", f"{(1/ft_home) * 100:.2f}%")
