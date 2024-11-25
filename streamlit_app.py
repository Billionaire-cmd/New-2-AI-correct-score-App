import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Title and Description
st.title("Sports Betting Correct Score Predictor")
st.write("""
This app predicts realistic correct scores for sports matches, aligns them with HT/FT outcomes, 
and provides AI-based recommendations for bets with the best potential profits.
""")

# User Inputs
st.sidebar.header("Match Details")
team_a = st.sidebar.text_input("Team A", "Team A")
team_b = st.sidebar.text_input("Team B", "Team B")
team_a_goals = st.sidebar.number_input("Avg Goals Scored by Team A", 1.5)
team_b_goals = st.sidebar.number_input("Avg Goals Scored by Team B", 1.2)
odds_a = st.sidebar.number_input("Odds for Team A Win", 2.5)
odds_b = st.sidebar.number_input("Odds for Team B Win", 2.8)
odds_draw = st.sidebar.number_input("Odds for Draw", 3.2)

# Generate Probabilities using Poisson Distribution
def poisson_prob(lam, goal):
    return poisson.pmf(goal, lam)

max_goals = 5  # Limit for practical purposes
st.header("Correct Score Probabilities")
score_matrix = np.zeros((max_goals + 1, max_goals + 1))
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        score_matrix[i, j] = poisson_prob(team_a_goals, i) * poisson_prob(team_b_goals, j)

# Display Probability Table
df_scores = pd.DataFrame(score_matrix, index=[f"A {i}" for i in range(max_goals + 1)], 
                         columns=[f"B {i}" for i in range(max_goals + 1)])
st.write("Probability of each scoreline:")
st.dataframe(df_scores)

# HT/FT Prediction
st.header("HT/FT Prediction")
ht_prob = poisson_prob(team_a_goals / 2, np.arange(max_goals + 1)) * \
          poisson_prob(team_b_goals / 2, np.arange(max_goals + 1))
ft_prob = poisson_prob(team_a_goals, np.arange(max_goals + 1)) * \
          poisson_prob(team_b_goals, np.arange(max_goals + 1))

ht_result = np.argmax(ht_prob)
ft_result = np.argmax(ft_prob)
st.write(f"Predicted HT/FT Outcome: {ht_result}-0/{ft_result}-1 (Example: 0-1/2-1)")

# BTTS (Both Teams to Score)
st.header("Both Teams to Score (BTTS)")
btts_yes = 1 - poisson_prob(team_a_goals, 0) * poisson_prob(team_b_goals, 0)
btts_no = poisson_prob(team_a_goals, 0) * poisson_prob(team_b_goals, 0)
st.write(f"BTTS Yes (GG) Probability: {btts_yes:.2%}")
st.write(f"BTTS No (NG) Probability: {btts_no:.2%}")

# AI Betting Recommendations
st.header("AI Betting Recommendations")
ev_a_win = (1 / odds_a) * team_a_goals
ev_b_win = (1 / odds_b) * team_b_goals
ev_draw = (1 / odds_draw) * (1 - (team_a_goals + team_b_goals))

if ev_a_win > ev_b_win and ev_a_win > ev_draw:
    recommendation = f"Bet on Team A to Win. Expected Value: {ev_a_win:.2f}"
elif ev_b_win > ev_a_win and ev_b_win > ev_draw:
    recommendation = f"Bet on Team B to Win. Expected Value: {ev_b_win:.2f}"
else:
    recommendation = f"Bet on Draw. Expected Value: {ev_draw:.2f}"

st.write("Recommended Bet:", recommendation)

# Additional Notes
st.write("""
**Disclaimer**: This app uses statistical methods and AI algorithms to suggest bets. 
It does not guarantee winning outcomes and should be used responsibly.
""")
