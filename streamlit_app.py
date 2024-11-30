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
    return [(home, away) for home in range(max_goals + 1) for away in range(max_goals + 1)]

# Sidebar for inputs
def sidebar_inputs():
    st.sidebar.header("Input Parameters")
    st.sidebar.subheader("Team Strengths")
    home_attack = st.sidebar.number_input("Home Attack Strength", value=1.00, format="%.2f")
    home_defense = st.sidebar.number_input("Home Defense Strength", value=0.80, format="%.2f")
    away_attack = st.sidebar.number_input("Away Attack Strength", value=0.80, format="%.2f")
    away_defense = st.sidebar.number_input("Away Defense Strength", value=0.87, format="%.2f")

    st.sidebar.subheader("Odds")
    odds_home = st.sidebar.number_input("Odds: Home", value=2.20, format="%.2f")
    odds_draw = st.sidebar.number_input("Odds: Draw", value=3.20, format="%.2f")
    odds_away = st.sidebar.number_input("Odds: Away", value=2.70, format="%.2f")
    odds_over_2_5 = st.sidebar.number_input("Over 2.5 Odds", value=2.50, format="%.2f")
    odds_under_2_5 = st.sidebar.number_input("Under 2.5 Odds", value=1.40, format="%.2f")
    
    return home_attack, home_defense, away_attack, away_defense, odds_home, odds_draw, odds_away, odds_over_2_5, odds_under_2_5

# Main function to calculate predictions
def calculate_predictions(home_attack, home_defense, away_attack, away_defense, odds_home, odds_draw, odds_away, odds_over_2_5, odds_under_2_5):
    # Calculate expected goals
    home_goals = home_attack * away_defense
    away_goals = away_attack * home_defense

    # Poisson distributions
    home_goals_dist = poisson(home_goals)
    away_goals_dist = poisson(away_goals)

    # Correct Score Probabilities
    correct_score_probs = {}
    for i in range(6):  # Home goals (0-5)
        for j in range(6):  # Away goals (0-5)
            prob = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
            correct_score_probs[f"{i}-{j}"] = prob

    # Most Likely Scoreline
    most_likely_scoreline = max(correct_score_probs, key=correct_score_probs.get)
    most_likely_scoreline_prob = correct_score_probs[most_likely_scoreline] * 100

    # Outcome Probabilities
    home_win_prob = sum(
        home_goals_dist.pmf(i) * sum(away_goals_dist.pmf(j) for j in range(i))
        for i in range(6)
    ) * 100
    draw_prob = sum(home_goals_dist.pmf(i) * away_goals_dist.pmf(i) for i in range(6)) * 100
    away_win_prob = sum(
        away_goals_dist.pmf(i) * sum(home_goals_dist.pmf(j) for j in range(i))
        for i in range(6)
    ) * 100
    over_2_5_prob = sum(
        home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
        for i in range(6) for j in range(6) if i + j > 2
    ) * 100
    under_2_5_prob = 100 - over_2_5_prob

    # BTTS (Both Teams To Score)
    btts_prob = sum(
        home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
        for i in range(1, 6) for j in range(1, 6)
    ) * 100

    # Display Results
    st.subheader("Predicted Probabilities")
    st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
    st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
    st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
    st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")
    st.write(f"🔄 **BTTS Probability (Yes):** {btts_prob:.2f}%")

    st.subheader("Correct Score Probabilities")
    for score, prob in sorted(correct_score_probs.items(), key=lambda x: x[1], reverse=True)[:10]:
        st.write(f"{score}: {prob * 100:.2f}%")

    st.subheader("Most Likely Outcome")
    st.write(f"**The most likely scoreline is {most_likely_scoreline}** with a probability of {most_likely_scoreline_prob:.2f}%.")

# Streamlit app setup
def main():
    st.title("Advanced Football Prediction Model")
    st.write("Predict football match outcomes using Poisson distribution and implied probabilities.")

    # Sidebar inputs
    home_attack, home_defense, away_attack, away_defense, odds_home, odds_draw, odds_away, odds_over_2_5, odds_under_2_5 = sidebar_inputs()

    # Prediction calculations and display
    if st.sidebar.button("Submit Predictions"):
        calculate_predictions(home_attack, home_defense, away_attack, away_defense, odds_home, odds_draw, odds_away, odds_over_2_5, odds_under_2_5)

if __name__ == "__main__":
    main()
