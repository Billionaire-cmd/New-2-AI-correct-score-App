import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to adjust probabilities based on Over 2.5 goals odds
def adjust_for_over_2_5_goals(over_2_5_odds, poisson_prob):
    over_2_5_prob = implied_prob(over_2_5_odds)
    return poisson_prob * (over_2_5_prob / 100)

# Function to generate all possible scorelines up to max_goals
def generate_scorelines(max_goals=5):
    return [(home, away) for home in range(max_goals + 1) for away in range(max_goals + 1)]

# Function to calculate the distribution of goals
def calculate_goal_distributions(home_rate, away_rate, max_goals):
    home_dist = [poisson_prob(home_rate, k) for k in range(max_goals + 1)]
    away_dist = [poisson_prob(away_rate, k) for k in range(max_goals + 1)]
    return home_dist, away_dist

# Main function to calculate predictions
def calculate_predictions():
    # User inputs for team statistics
    st.title("Advanced Football Prediction Tool")

    st.header("Team Statistics")
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=1.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=0.96)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.50)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=2.00)

    # Sidebar inputs for odds
    st.sidebar.header("Odds and Parameters")
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=1.0, value=2.50)
    ht_home_odds = st.sidebar.number_input("HT Home Odds", min_value=1.0, value=3.50)
    ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=1.0, value=3.70)
    ht_away_odds = st.sidebar.number_input("HT Away Odds", min_value=1.0, value=2.80)
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=1.0, value=2.20)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=1.0, value=3.20)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=1.0, value=2.70)

    # Compute expected goals
    st.sidebar.header("Expected Goals")
    home_expected_goals = (team_a_home_goals + team_b_away_conceded) / 2
    away_expected_goals = (team_b_away_goals + team_a_home_conceded) / 2

    st.sidebar.write(f"Home Expected Goals: {home_expected_goals:.2f}")
    st.sidebar.write(f"Away Expected Goals: {away_expected_goals:.2f}")

    # Generate scorelines and probabilities
    max_goals = 5
    scorelines = generate_scorelines(max_goals)
    home_dist, away_dist = calculate_goal_distributions(home_expected_goals, away_expected_goals, max_goals)

    correct_score_probs = {}
    for home_goals, away_goals in scorelines:
        prob = home_dist[home_goals] * away_dist[away_goals]
        correct_score_probs[f"{home_goals}-{away_goals}"] = prob

    # Most likely scoreline
    most_likely_scoreline = max(correct_score_probs, key=correct_score_probs.get)
    most_likely_scoreline_prob = correct_score_probs[most_likely_scoreline] * 100

    # Calculate probabilities for outcomes
    home_win_prob = sum(
        home_dist[i] * sum(away_dist[j] for j in range(i))
        for i in range(max_goals + 1)
    ) * 100
    draw_prob = sum(home_dist[i] * away_dist[i] for i in range(max_goals + 1)) * 100
    away_win_prob = sum(
        away_dist[i] * sum(home_dist[j] for j in range(i))
        for i in range(max_goals + 1)
    ) * 100

    over_2_5_prob = sum(
        home_dist[i] * away_dist[j]
        for i in range(max_goals + 1)
        for j in range(max_goals + 1) if i + j > 2
    ) * 100
    under_2_5_prob = 100 - over_2_5_prob

    # Display results
    st.subheader("Predicted Probabilities")
    st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
    st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
    st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
    st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")

    st.subheader("Most Likely Outcome")
    st.write(f"**Most likely scoreline:** {most_likely_scoreline} with a probability of {most_likely_scoreline_prob:.2f}%.")

    st.subheader("Top Correct Score Probabilities")
    for score, prob in sorted(correct_score_probs.items(), key=lambda x: x[1], reverse=True)[:10]:
        st.write(f"{score}: {prob * 100:.2f}%")

# Run the application
if __name__ == "__main__":
    calculate_predictions()
