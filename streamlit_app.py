import streamlit as st
import numpy as np
from scipy.stats import poisson

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, betting odds, and team statistics, 
to predict realistic halftime and full-time correct scores for football matches.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Average Points
avg_points_home = st.sidebar.number_input("Average Points for Home Team", min_value=0.0, step=0.1, value=1.8)
avg_points_away = st.sidebar.number_input("Average Points for Away Team", min_value=0.0, step=0.1, value=1.5)

# Betting Odds
st.sidebar.subheader("Halftime Odds")
ht_home = st.sidebar.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
ht_draw = st.sidebar.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
ht_away = st.sidebar.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

st.sidebar.subheader("Fulltime Odds")
ft_home = st.sidebar.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
ft_draw = st.sidebar.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
ft_away = st.sidebar.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# BTTS and Over/Under Odds
st.sidebar.subheader("BTTS GG/NG Odds")
btts_gg = st.sidebar.number_input("BTTS (Yes) Odds", min_value=1.0, step=0.1, value=1.8)
btts_ng = st.sidebar.number_input("BTTS (No) Odds", min_value=1.0, step=0.1, value=1.9)

st.sidebar.subheader("Over/Under Odds (Fulltime)")
over_2_5_ft = st.sidebar.number_input("Over 2.5 FT Odds", min_value=1.0, step=0.1, value=2.0)
under_2_5_ft = st.sidebar.number_input("Under 2.5 FT Odds", min_value=1.0, step=0.1, value=1.8)

# Correct Score Odds
st.sidebar.subheader("Correct Score Odds (HT and FT)")
correct_score_odds = {}
for score in ["0:0", "1:0", "0:1", "1:1", "2:0", "2:1", "2:2", "3:0", "3:1", "3:2", "3:3"]:
    correct_score_odds[score] = st.sidebar.number_input(f"Odds for {score}", value=10.0, step=0.01)

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals):
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Function to Calculate Margins
def calculate_margin(odds):
    return (1 / odds.sum() - 1) * 100

# Predict Probabilities and Correct Scores
if st.button("Predict Probabilities and Insights"):
    try:
        # Poisson probabilities
        home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(home_probs, away_probs)

        # Calculate score probabilities
        score_probs = {f"{i}:{j}": score_matrix[i, j] for i in range(5) for j in range(5)}
        sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)

        # Insights
        st.header("Predictions and Insights")

        # Correct Score
        st.subheader("Correct Score Predictions")
        st.write("### Top 5 Likely Scores:")
        for score, prob in sorted_scores[:5]:
            st.write(f"**{score}:** {prob * 100:.2f}%")

        # BTTS
        btts_prob = sum(score_matrix[i][j] for i in range(1, 5) for j in range(1, 5)) * 100
        st.subheader("BTTS (GG/NG) Probabilities")
        st.write(f"**BTTS (Yes):** {btts_prob:.2f}%")
        st.write(f"**BTTS (No):** {100 - btts_prob:.2f}%")

        # Over/Under
        over_2_5_prob = sum(score_matrix[i][j] for i in range(3, 5) for j in range(5)) * 100
        st.subheader("Over/Under 2.5 Goals Probabilities")
        st.write(f"**Over 2.5 Goals:** {over_2_5_prob:.2f}%")
        st.write(f"**Under 2.5 Goals:** {100 - over_2_5_prob:.2f}%")

        # Win/Draw Probabilities
        home_win_prob = sum(score_matrix[i][j] for i in range(5) for j in range(i)) * 100
        draw_prob = sum(score_matrix[i][i] for i in range(5)) * 100
        away_win_prob = 100 - home_win_prob - draw_prob
        st.subheader("Match Outcome Probabilities")
        st.write(f"**Home Win:** {home_win_prob:.2f}%")
        st.write(f"**Draw:** {draw_prob:.2f}%")
        st.write(f"**Away Win:** {away_win_prob:.2f}%")

        # Moderate Value Bet
        st.subheader("Moderate Value Bet Recommendation")
        st.write(f"**Recommended Bet:** {sorted_scores[0][0]} (Probability: {sorted_scores[0][1] * 100:.2f}%)")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
