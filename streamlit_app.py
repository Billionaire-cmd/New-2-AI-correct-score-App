import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# App Title and Introduction
st.title("💯💯💯🤖 Rabiotic HT/FT Correct Score Predictor Pro")
st.markdown("""
Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- Poisson distribution
- Betting odds
- Team statistics
""")

# Sidebar Inputs
st.sidebar.header("Match Inputs")
st.sidebar.subheader("Team Statistics")
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", value=1.50)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", value=1.30)

st.sidebar.subheader("BTTS (Both Teams To Score) Inputs")
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds (Both Teams To Score)", value=1.77)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds (No Goal for One or Both)", value=1.83)

st.sidebar.subheader("Over/Under 2.5 Goals Inputs")
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80)

st.sidebar.subheader("Odds")
ht_home_win_odds = st.sidebar.number_input("HT Home Win Odds", value=2.40)
ht_draw_odds = st.sidebar.number_input("HT Draw Odds", value=2.10)
ht_away_win_odds = st.sidebar.number_input("HT Away Win Odds", value=4.50)
ft_home_win_odds = st.sidebar.number_input("FT Home Win Odds", value=1.80)
ft_draw_odds = st.sidebar.number_input("FT Draw Odds", value=3.50)
ft_away_win_odds = st.sidebar.number_input("FT Away Win Odds", value=3.90)

st.sidebar.subheader("HT Correct Score Odds")
ht_correct_scores = {
    "0:0": st.sidebar.number_input("HT Odds for 0:0", value=2.58),
    "0:1": st.sidebar.number_input("HT Odds for 0:1", value=5.84),
    "0:2": st.sidebar.number_input("HT Odds for 0:2", value=26.08),
    "1:0": st.sidebar.number_input("HT Odds for 1:0", value=3.63),
    "1:1": st.sidebar.number_input("HT Odds for 1:1", value=8.07),
    "1:2": st.sidebar.number_input("HT Odds for 1:2", value=36.39),
}

st.sidebar.subheader("FT Correct Score Odds")
ft_correct_scores = {
    "0:0": st.sidebar.number_input("FT Odds for 0:0", value=10.41),
    "1:2": st.sidebar.number_input("FT Odds for 1:2", value=13.21),
    "0:2": st.sidebar.number_input("FT Odds for 0:2", value=20.77),
}

# Helper Function: Poisson Probability
def poisson_probability(lam, x):
    return poisson.pmf(x, lam)

# Calculate Expected Goals
st.header("Expected Goals")
home_goal_rate = avg_goals_home * (avg_points_home / avg_points_away)
away_goal_rate = avg_goals_away * (avg_points_away / avg_points_home)

st.write(f"Expected Goals for Home Team: **{home_goal_rate:.2f}**")
st.write(f"Expected Goals for Away Team: **{away_goal_rate:.2f}**")

# Generate Probabilities for HT and FT Scores
st.header("Halftime and Full-Time Score Probabilities")

# Generate Score Ranges
score_range = range(0, 4)
home_probs = [poisson_probability(home_goal_rate / 2, x) for x in score_range]
away_probs = [poisson_probability(away_goal_rate / 2, x) for x in score_range]

# Display Probabilities in Table Format
st.subheader("Halftime Score Probabilities")
ht_probabilities = []
for h in score_range:
    row = []
    for a in score_range:
        prob = home_probs[h] * away_probs[a]
        row.append(prob)
    ht_probabilities.append(row)

st.write("Halftime Probabilities Matrix")
st.table(ht_probabilities)

# Calculate Full-Time Probabilities
home_probs_ft = [poisson_probability(home_goal_rate, x) for x in score_range]
away_probs_ft = [poisson_probability(away_goal_rate, x) for x in score_range]

st.subheader("Full-Time Score Probabilities")
ft_probabilities = []
for h in score_range:
    row = []
    for a in score_range:
        prob = home_probs_ft[h] * away_probs_ft[a]
        row.append(prob)
    ft_probabilities.append(row)

st.write("Full-Time Probabilities Matrix")
st.table(ft_probabilities)

# Plotting Score Distributions
st.header("Score Distributions")
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].bar(score_range, home_probs, color="blue", alpha=0.7, label="Home HT Goals")
ax[0].bar(score_range, away_probs, color="red", alpha=0.7, label="Away HT Goals")
ax[0].set_title("Halftime Goal Distribution")
ax[0].legend()

ax[1].bar(score_range, home_probs_ft, color="blue", alpha=0.7, label="Home FT Goals")
ax[1].bar(score_range, away_probs_ft, color="red", alpha=0.7, label="Away FT Goals")
ax[1].set_title("Full-Time Goal Distribution")
ax[1].legend()

st.pyplot(fig)

# HT/FT Outcome Prediction
st.header("HT/FT Outcome Prediction")
ht_away_away_prob = ht_probabilities[0][2] * ft_probabilities[1][2]  # Prob for HT 0-2, FT 1-2
st.write(f"Probability of HT/FT (Away/Away, 0-2/1-2): **{ht_away_away_prob:.5f}**")

st.markdown("**Thank you for using the Rabiotic HT/FT Correct Score Predictor Pro!**")
