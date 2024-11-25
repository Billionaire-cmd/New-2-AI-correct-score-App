import streamlit as st
import numpy as np
from scipy.stats import poisson

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, correct score odds, and more, 
to predict realistic halftime and full-time correct scores.  
It is designed to enhance your betting strategies by providing precise calculations for maximum ROI.
""")

# Input Section: Betting Odds
st.header("Input Betting Odds and Parameters")
col1, col2 = st.columns(2)

# Halftime Odds
with col1:
    st.subheader("Halftime Odds")
    ht_home = st.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
    ht_draw = st.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
    ht_away = st.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

# Full-time Odds
with col2:
    st.subheader("Full-time Odds")
    ft_home = st.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
    ft_draw = st.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
    ft_away = st.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# Correct Score Odds (HT and FT)
st.sidebar.header("Correct Score Odds (Max 4:4)")
correct_score_odds = {}
for score in ["0:0", "0:1", "0:2", "1:0", "1:1", "1:2", "2:0", "2:1", "2:2", "3:0", "3:1", "3:2", "3:3", "4:0", "4:1", "4:2", "4:3", "4:4"]:
    correct_score_odds[score] = st.sidebar.number_input(f"Odds for {score}", value=10.0, step=0.01)

# Additional Odds Inputs
st.subheader("BTTS and Over/Under Odds")
col3, col4 = st.columns(2)

with col3:
    btts_gg = st.number_input("BTTS GG Odds", min_value=1.0, step=0.1, value=1.8)
    over_25 = st.number_input("Over 2.5 Odds", min_value=1.0, step=0.1, value=2.0)

with col4:
    btts_ng = st.number_input("BTTS NG Odds", min_value=1.0, step=0.1, value=2.1)
    under_25 = st.number_input("Under 2.5 Odds", min_value=1.0, step=0.1, value=1.9)

# Process Input: Calculate Probabilities
if st.button("Calculate Probabilities"):
    try:
        def calculate_poisson_prob(goal_avg, max_goals):
            """Calculate Poisson probabilities for goals."""
            return [poisson.pmf(i, goal_avg) for i in range(max_goals + 1)]

        # Halftime and Fulltime Goal Averages
        ht_goal_avg = (ht_home + ht_away) / 2
        ft_goal_avg = (ft_home + ft_away) / 2

        # Halftime and Fulltime Goal Probabilities
        ht_probs = calculate_poisson_prob(ht_goal_avg, max_goals=2)
        ft_probs = calculate_poisson_prob(ft_goal_avg, max_goals=4)

        # Halftime Over/Under 1.5 Goals Probabilities
        ht_over_15_prob = 1 - sum(ht_probs[:2])  # Goals 2 or more
        ht_under_15_prob = sum(ht_probs[:2])  # Goals 0 or 1

        # Combine HT/FT probabilities using outer product
        combined_probs = np.outer(ht_probs, ft_probs)

        # BTTS and Over/Under Probabilities
        btts_prob = 1 / btts_gg
        under_25_prob = 1 / under_25
        over_25_prob = 1 / over_25

        # Display Results
        st.header("Calculated Probabilities and Recommendations")
        st.write("**Halftime Probabilities (0-0 to 2-2):**", ht_probs)
        st.write("**Fulltime Probabilities (0-0 to 4-4):**", ft_probs)
        st.write(f"**Halftime Over 1.5 Goals Probability:** {ht_over_15_prob * 100:.2f}%")
        st.write(f"**Halftime Under 1.5 Goals Probability:** {ht_under_15_prob * 100:.2f}%")
        st.write(f"**Over 2.5 Goals Probability:** {over_25_prob * 100:.2f}%")
        st.write(f"**Under 2.5 Goals Probability:** {under_25_prob * 100:.2f}%")
        st.write(f"**BTTS (GG) Probability:** {btts_prob * 100:.2f}%")

        # Recommendations
        most_likely_ht_score = max(zip(ht_probs, ["0:0", "1:0", "0:1", "1:1", "2:0", "2:1", "2:2"]))
        most_likely_ft_score = max(zip(ft_probs, ["0:0", "1:0", "0:1", "1:1", "2:0", "2:1", "2:2", "3:0", "3:1", "3:2", "3:3", "4:0", "4:1", "4:2", "4:3", "4:4"]))
        st.subheader("Recommended Results")
        st.write(f"**Halftime Recommended Correct Score:** {most_likely_ht_score[1]} with probability {most_likely_ht_score[0] * 100:.2f}%")
        st.write(f"**Fulltime Recommended Correct Score:** {most_likely_ft_score[1]} with probability {most_likely_ft_score[0] * 100:.2f}%")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
