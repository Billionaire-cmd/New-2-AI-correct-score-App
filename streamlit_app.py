import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Generate all possible scorelines
def generate_scorelines(max_goals=5):
    return [(home_goals, away_goals) for home_goals in range(max_goals + 1) for away_goals in range(max_goals + 1)]

# Calculate probabilities for match outcomes
def calculate_match_probabilities(home_goals_dist, away_goals_dist, max_goals=5):
    correct_score_probs = {}
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            correct_score_probs[f"{i}-{j}"] = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
    return correct_score_probs

# Display predictions and probabilities
def display_results(home_win_prob, draw_prob, away_win_prob, over_2_5_prob, under_2_5_prob, btts_prob, ht_ft_probs, correct_score_probs):
    st.subheader("Predicted Probabilities")
    st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
    st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
    st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
    st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")
    st.write(f"🔄 **BTTS Probability (Yes):** {btts_prob:.2f}%")

    st.subheader("HT/FT Probabilities")
    for ht_ft, prob in ht_ft_probs.items():
        st.write(f"{ht_ft}: {prob:.2f}%")

    st.subheader("Correct Score Probabilities")
    for score, prob in sorted(correct_score_probs.items(), key=lambda x: x[1], reverse=True)[:10]:
        st.write(f"{score}: {prob * 100:.2f}%")

# Main function to calculate predictions
def calculate_predictions():
    # Team inputs
    st.sidebar.header("Team Statistics")
    team_a_home_goals = st.sidebar.number_input("Team A Average Goals Scored (Home)", value=1.30, format="%.2f")
    team_b_away_goals = st.sidebar.number_input("Team B Average Goals Scored (Away)", value=0.96, format="%.2f")
    team_a_home_conceded = st.sidebar.number_input("Team A Average Goals Conceded (Home)", value=1.50, format="%.2f")
    team_b_away_conceded = st.sidebar.number_input("Team B Average Goals Conceded (Away)", value=2.00, format="%.2f")

    # Odds inputs
    st.sidebar.header("Odds Inputs")
    odds_home = st.sidebar.number_input("FT Home Odds", value=2.20, format="%.2f")
    odds_draw = st.sidebar.number_input("FT Draw Odds", value=3.20, format="%.2f")
    odds_away = st.sidebar.number_input("FT Away Odds", value=2.70, format="%.2f")
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=2.50, format="%.2f")

    # Calculate expected goals
    home_expected_goals = team_a_home_goals * (team_b_away_conceded / team_b_away_goals)
    away_expected_goals = team_b_away_goals * (team_a_home_conceded / team_a_home_goals)

    # Poisson distributions for goal probabilities
    home_goals_dist = poisson(home_expected_goals)
    away_goals_dist = poisson(away_expected_goals)

    # Calculate outcome probabilities
    home_win_prob = sum(home_goals_dist.pmf(i) * sum(away_goals_dist.pmf(j) for j in range(i)) for i in range(6)) * 100
    draw_prob = sum(home_goals_dist.pmf(i) * away_goals_dist.pmf(i) for i in range(6)) * 100
    away_win_prob = sum(away_goals_dist.pmf(i) * sum(home_goals_dist.pmf(j) for j in range(i)) for i in range(6)) * 100

    # Over/Under 2.5 goals probabilities
    over_2_5_prob = sum(home_goals_dist.pmf(i) * away_goals_dist.pmf(j) for i in range(6) for j in range(6) if i + j > 2) * 100
    under_2_5_prob = 100 - over_2_5_prob

    # BTTS (Both Teams To Score) probability
    btts_prob = sum(home_goals_dist.pmf(i) * away_goals_dist.pmf(j) for i in range(1, 6) for j in range(1, 6)) * 100

    # HT/FT probabilities (simple example)
    ht_ft_probs = {
        "1/1": home_win_prob / 2, "1/X": draw_prob / 2, "1/2": away_win_prob / 2,
        "X/1": home_win_prob / 2, "X/X": draw_prob / 2, "X/2": away_win_prob / 2,
        "2/1": home_win_prob / 2, "2/X": draw_prob / 2, "2/2": away_win_prob / 2
    }

    # Correct score probabilities
    correct_score_probs = calculate_match_probabilities(home_goals_dist, away_goals_dist)

    # Display results
    display_results(home_win_prob, draw_prob, away_win_prob, over_2_5_prob, under_2_5_prob, btts_prob, ht_ft_probs, correct_score_probs)

# Streamlit App Layout
st.title("Advanced Football Match Prediction")
st.write("Analyze match outcomes using Poisson distribution and probability models.")

if st.button("Calculate Predictions"):
    calculate_predictions()
