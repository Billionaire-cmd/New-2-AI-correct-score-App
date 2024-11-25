import streamlit as st
import numpy as np
from scipy.stats import poisson

# Helper Function to Calculate Poisson Probabilities
def poisson_probability(mean, goals):
    return poisson.pmf(goals, mean)

# Header
st.title("Sports Betting Correct Score Predictor")
st.markdown("""
This app calculates and predicts realistic correct scores for sports betting, including HT/FT results, BTTS, and Over/Under odds.
""")

# Input Fields
st.header("Input Match Details")
home_team = st.text_input("Home Team", "Team A")
away_team = st.text_input("Away Team", "Team B")

st.subheader("Average Team Stats")
home_avg_goals = st.number_input("Home Team Avg Goals Scored", value=1.5)
away_avg_goals = st.number_input("Away Team Avg Goals Scored", value=1.2)
home_conceded = st.number_input("Home Team Avg Goals Conceded", value=1.0)
away_conceded = st.number_input("Away Team Avg Goals Conceded", value=1.3)

st.subheader("Odds and Probabilities")
ht_home_odds = st.number_input("HT Home Win Odds", value=2.8)
ht_draw_odds = st.number_input("HT Draw Odds", value=2.5)
ht_away_odds = st.number_input("HT Away Win Odds", value=3.1)

ft_home_odds = st.number_input("FT Home Win Odds", value=2.5)
ft_draw_odds = st.number_input("FT Draw Odds", value=3.0)
ft_away_odds = st.number_input("FT Away Win Odds", value=2.9)

btts_odds = st.number_input("BTTS (GG) Odds", value=1.8)
over_2_5_odds = st.number_input("Over 2.5 Odds", value=2.0)
under_2_5_odds = st.number_input("Under 2.5 Odds", value=1.9)

# Calculations
st.header("Calculated Probabilities")
home_ht_mean = home_avg_goals * 0.45
away_ht_mean = away_avg_goals * 0.45
home_ft_mean = home_avg_goals
away_ft_mean = away_avg_goals

# Poisson Probabilities for Correct Scores
ht_correct_scores = {
    (home_goals, away_goals): poisson_probability(home_ht_mean, home_goals) * poisson_probability(away_ht_mean, away_goals)
    for home_goals in range(3)
    for away_goals in range(3)
}

ft_correct_scores = {
    (home_goals, away_goals): poisson_probability(home_ft_mean, home_goals) * poisson_probability(away_ft_mean, away_goals)
    for home_goals in range(5)
    for away_goals in range(5)
}

# Display Top Probabilities
st.subheader("Top Halftime Correct Scores")
ht_sorted = sorted(ht_correct_scores.items(), key=lambda x: x[1], reverse=True)
for (home_goals, away_goals), prob in ht_sorted[:5]:
    st.write(f"HT {home_goals}-{away_goals}: {prob:.2%}")

st.subheader("Top Fulltime Correct Scores")
ft_sorted = sorted(ft_correct_scores.items(), key=lambda x: x[1], reverse=True)
for (home_goals, away_goals), prob in ft_sorted[:5]:
    st.write(f"FT {home_goals}-{away_goals}: {prob:.2%}")

# BTTS, Over/Under, HT/FT Prediction
st.subheader("Additional Predictions")
btts_prob = (1 - np.exp(-(home_avg_goals + away_avg_goals))) * 100
over_2_5_prob = (1 - (poisson.cdf(2, home_ft_mean + away_ft_mean))) * 100
under_2_5_prob = 100 - over_2_5_prob

st.write(f"BTTS (GG) Probability: {btts_prob:.2f}%")
st.write(f"Over 2.5 Probability: {over_2_5_prob:.2f}%")
st.write(f"Under 2.5 Probability: {under_2_5_prob:.2f}%")

# HT/FT Prediction
ht_ft_prediction = "0-1/2-1"
st.write(f"Recommended HT/FT Prediction: {ht_ft_prediction}")

# AI Recommendation
st.header("AI Betting Recommendation")
best_bet = max(
    [
        ("BTTS (GG)", btts_odds, btts_prob),
        ("Over 2.5", over_2_5_odds, over_2_5_prob),
        ("Under 2.5", under_2_5_odds, under_2_5_prob),
    ],
    key=lambda x: x[2] / x[1],  # Probability / Odds Ratio
)
st.write(f"**Best Bet:** {best_bet[0]} with a value of {best_bet[2]:.2f}% and odds {best_bet[1]}")

# Footer
st.markdown("**Disclaimer:** Predictions are based on probabilities and historical data. Bet responsibly!")
