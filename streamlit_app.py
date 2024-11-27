import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Sidebar section
st.sidebar.title("Rabiotic HT/FT Predictor Pro")
st.sidebar.markdown("### Match Inputs")

# Team Statistics Inputs
st.sidebar.subheader("Team Statistics")
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", min_value=0.0, value=1.50, step=0.1)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", min_value=0.0, value=1.30, step=0.1)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", min_value=0.0, value=1.50, step=0.1)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", min_value=0.0, value=1.30, step=0.1)

# BTTS (Both Teams To Score) Inputs
st.sidebar.subheader("BTTS Inputs")
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds", min_value=0.0, value=1.77, step=0.01)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds", min_value=0.0, value=1.83, step=0.01)

# Over/Under 2.5 Goals Inputs
st.sidebar.subheader("Over/Under 2.5 Goals Inputs")
over_2_5_goals_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=0.0, value=1.87, step=0.01)
under_2_5_goals_odds = st.sidebar.number_input("Under 2.5 Goals Odds", min_value=0.0, value=1.80, step=0.01)

# Odds Inputs
st.sidebar.subheader("Odds")
ht_home_win_odds = st.sidebar.number_input("HT Home Win Odds", min_value=0.0, value=2.40, step=0.01)
ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=0.0, value=2.10, step=0.01)
ht_away_win_odds = st.sidebar.number_input("HT Away Win Odds", min_value=0.0, value=4.50, step=0.01)

ft_home_win_odds = st.sidebar.number_input("FT Home Win Odds", min_value=0.0, value=1.80, step=0.01)
ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=3.50, step=0.01)
ft_away_win_odds = st.sidebar.number_input("FT Away Win Odds", min_value=0.0, value=3.90, step=0.01)

# HT Correct Score Odds
st.sidebar.subheader("HT Correct Score Odds")
ht_odds_0_0 = st.sidebar.number_input("HT Odds for 0:0", min_value=0.0, value=2.58, step=0.01)
ht_odds_0_1 = st.sidebar.number_input("HT Odds for 0:1", min_value=0.0, value=5.84, step=0.01)
ht_odds_0_2 = st.sidebar.number_input("HT Odds for 0:2", min_value=0.0, value=26.08, step=0.01)

# FT Correct Score Odds
st.sidebar.subheader("FT Correct Score Odds")
ft_odds_0_0 = st.sidebar.number_input("FT Odds for 0:0", min_value=0.0, value=10.41, step=0.01)
ft_odds_0_1 = st.sidebar.number_input("FT Odds for 0:1", min_value=0.0, value=10.74, step=0.01)
ft_odds_0_2 = st.sidebar.number_input("FT Odds for 0:2", min_value=0.0, value=20.77, step=0.01)

# HT/FT Outcome and Correct Score Prediction
st.sidebar.subheader("HT/FT Prediction")
ht_ft_outcome = st.sidebar.selectbox("Select HT/FT Outcome", ["Home/Home", "Home/Draw", "Home/Away", "Draw/Home", "Draw/Draw", "Draw/Away", "Away/Home", "Away/Draw", "Away/Away"])

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Function to calculate expected score
def calculate_expected_goals(avg_goals_home, avg_goals_away):
    expected_home_goals = poisson.pmf(np.arange(0, 6), avg_goals_home)
    expected_away_goals = poisson.pmf(np.arange(0, 6), avg_goals_away)
    return expected_home_goals, expected_away_goals

# Expected Goals Prediction
expected_home_goals, expected_away_goals = calculate_expected_goals(avg_goals_home, avg_goals_away)

# Display Predicted Scores for HT/FT
st.title("💯💯💯🤖 Rabiotic HT/FT Correct Score Predictor Pro")

# Display Team Statistics
st.header("Team Statistics")
st.write(f"**Average Goals Scored (Home):** {avg_goals_home}")
st.write(f"**Average Goals Scored (Away):** {avg_goals_away}")
st.write(f"**Average Points (Home):** {avg_points_home}")
st.write(f"**Average Points (Away):** {avg_points_away}")

# BTTS and Over/Under 2.5 Goals
st.header("BTTS & Over/Under 2.5 Goals")
st.write(f"**BTTS GG Odds (Both Teams To Score):** {btts_gg_odds}")
st.write(f"**BTTS NG Odds (No Goal for One or Both):** {btts_ng_odds}")
st.write(f"**Over 2.5 Goals Odds:** {over_2_5_goals_odds}")
st.write(f"**Under 2.5 Goals Odds:** {under_2_5_goals_odds}")

# Display Predicted HT/FT Outcome
st.header("Predicted HT/FT Outcome")
st.write(f"**HT/FT Outcome:** {ht_ft_outcome}")

# Plot the expected goals distribution
st.header("Expected Goals Distribution")
fig, ax = plt.subplots(figsize=(10, 6))

# Plot for Home Team
ax.bar(np.arange(0, 6), expected_home_goals, label="Home Team Goals", color="blue", alpha=0.6)

# Plot for Away Team
ax.bar(np.arange(0, 6), expected_away_goals, label="Away Team Goals", color="red", alpha=0.6)

ax.set_xlabel("Goals")
ax.set_ylabel("Probability")
ax.set_title("Expected Goals Distribution (Poisson Distribution)")
ax.legend()

st.pyplot(fig)

# Final Prediction based on HT/FT Odds
st.header("Final Predictions")
if ht_ft_outcome == "Away/Away":
    st.write(f"**HT Odds for 0:2:** {ht_odds_0_2}, **FT Odds for 1:2:** {ft_odds_0_2}")
else:
    st.write(f"HT/FT Outcome: {ht_ft_outcome}")

