import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Sidebar section
st.sidebar.title("Rabiotic HT/FT Predictor Pro")
st.sidebar.markdown("### Match Inputs")

# Team statistics (user inputs)
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50, min_value=0.0)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30, min_value=0.0)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", value=1.50, min_value=0.0)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", value=1.30, min_value=0.0)

# Betting odds (user inputs)
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds", value=1.77, min_value=0.0)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds", value=1.83, min_value=0.0)
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87, min_value=0.0)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80, min_value=0.0)

# HT/FT Outcome prediction input
st.sidebar.subheader("HT/FT Prediction")
ht_ft_outcome = st.sidebar.selectbox("Select HT/FT Outcome", ["Home/Home", "Home/Draw", "Home/Away", 
                                                            "Draw/Home", "Draw/Draw", "Draw/Away", 
                                                            "Away/Home", "Away/Draw", "Away/Away"])

# HT/FT Correct Score Odds
ht_0_0_odds = 2.58
ht_0_1_odds = 5.84
ht_1_0_odds = 3.63
ht_1_1_odds = 8.07
ht_1_2_odds = 36.39
ft_0_0_odds = 10.41
ft_0_1_odds = 10.74
ft_1_0_odds = 7.03
ft_1_1_odds = 6.51

# Poisson distribution calculation for HT/FT outcomes
def poisson_prob(avg_goals, score):
    return poisson.pmf(score, avg_goals)

# Calculate probabilities for selected HT/FT outcome
def calculate_ht_ft_probabilities(avg_goals_home, avg_goals_away, ht_ft_outcome):
    home_prob = poisson_prob(avg_goals_home, 1)  # Example: probability for HT 1 goal (could be modified for other scorelines)
    away_prob = poisson_prob(avg_goals_away, 1)  # Example: probability for FT 1 goal
    margin = (home_prob * away_prob)
    
    if ht_ft_outcome == "Home/Home":
        probability = margin * ht_0_0_odds
    elif ht_ft_outcome == "Home/Draw":
        probability = margin * ht_1_0_odds
    elif ht_ft_outcome == "Away/Away":
        probability = margin * ft_0_1_odds
    else:
        probability = margin
    
    return probability, 100 - probability  # Return margin as well

# Calculate probabilities and margins based on selected HT/FT Outcome
probability, margin = calculate_ht_ft_probabilities(avg_goals_home, avg_goals_away, ht_ft_outcome)

# Display results
st.write(f"### HT/FT Outcome: {ht_ft_outcome}")
st.write(f"Prediction Probability: {probability:.2f}%")
st.write(f"Margin: {margin:.2f}%")

# Plot for better visualization
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(["Probability", "Margin"], [probability, margin], color=['blue', 'red'])
ax.set_ylabel("Percentage")
ax.set_title("HT/FT Outcome Prediction")
st.pyplot(fig)
