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

# Correct Score Odds
st.sidebar.subheader("Correct Score Odds (HT and FT)")
correct_score_odds = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds[score] = st.sidebar.number_input(f"Odds for {score}", value=10.0, step=0.01)

# "Other" scores
correct_score_odds["Other"] = st.sidebar.number_input("Odds for scores exceeding 4:4", value=50.0, step=0.01)

# Halftime Correct Score Odds
st.sidebar.subheader("Halftime Correct Score Odds")
ht_correct_score_odds = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        ht_correct_score_odds[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)

# "Other" halftime scores
ht_correct_score_odds["Other"] = st.sidebar.number_input("HT Odds for scores exceeding 2:2", value=50.0, step=0.01)

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals=4):
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Predict Probabilities and Correct Scores
if st.button("Predict Probabilities and Insights"):
    try:
        # Poisson probabilities
        home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(home_probs, away_probs)

        # Halftime Poisson probabilities (assuming halftime goals are ~50% of full-time goals)
        ht_home_probs = calculate_poisson_prob(avg_goals_home / 2, max_goals=2)
        ht_away_probs = calculate_poisson_prob(avg_goals_away / 2, max_goals=2)
        ht_score_matrix = np.outer(ht_home_probs, ht_away_probs)

        # Calculate full-time score probabilities
        score_probs = {f"{i}:{j}": score_matrix[i, j] for i in range(5) for j in range(5)}
        other_prob = 1 - sum(score_probs.values())  # Probability of scores exceeding 4:4
        score_probs["Other"] = other_prob

        # Calculate halftime score probabilities
        ht_score_probs = {f"{i}:{j}": ht_score_matrix[i, j] for i in range(3) for j in range(3)}
        ht_other_prob = 1 - sum(ht_score_probs.values())  # Probability of scores exceeding 2:2
        ht_score_probs["Other"] = ht_other_prob

        # Sort scores by probabilities
        sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)
        sorted_ht_scores = sorted(ht_score_probs.items(), key=lambda x: x[1], reverse=True)

        # Insights
        st.header("Predictions and Insights")

        # Halftime Correct Score
        st.subheader("Halftime Correct Score Predictions")
        st.write("### Top 5 Likely Halftime Scores:")
        for ht_score, prob in sorted_ht_scores[:5]:
            st.write(f"**{ht_score}:** {prob * 100:.2f}%")

        # Fulltime Correct Score
        st.subheader("Fulltime Correct Score Predictions")
        st.write("### Top 5 Likely Fulltime Scores:")
        for score, prob in sorted_scores[:5]:
            st.write(f"**{score}:** {prob * 100:.2f}%")

        # Other Insights
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

        # Match Outcome Probabilities
        home_win_prob = sum(score_matrix[i][j] for i in range(5) for j in range(i)) * 100
        draw_prob = sum(score_matrix[i][i] for i in range(5)) * 100
        away_win_prob = 100 - home_win_prob - draw_prob
        st.subheader("Match Outcome Probabilities")
        st.write(f"**Home Win:** {home_win_prob:.2f}%")
        st.write(f"**Draw:** {draw_prob:.2f}%")
        st.write(f"**Away Win:** {away_win_prob:.2f}%")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
