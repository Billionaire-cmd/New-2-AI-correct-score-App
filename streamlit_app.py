# Import necessary libraries
import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Streamlit App Title and Introduction
st.title("💯💯💯🤖 Rabiotic HT/FT Correct Score Predictor Pro")
st.markdown("""
Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- **Poisson distribution**
- **Betting odds**
- **Team statistics**

Enter the match statistics and odds below to get started!
""")

# Sidebar for Match Inputs
st.sidebar.header("Match Inputs")

# Team Statistics
st.sidebar.subheader("Team Statistics")
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50, step=0.01)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30, step=0.01)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", value=1.50, step=0.01)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", value=1.30, step=0.01)

# BTTS Inputs
st.sidebar.subheader("BTTS (Both Teams To Score)")
btts_yes_odds = st.sidebar.number_input("BTTS GG Odds", value=1.77, step=0.01)
btts_no_odds = st.sidebar.number_input("BTTS NG Odds", value=1.83, step=0.01)

# Over/Under 2.5 Goals Inputs
st.sidebar.subheader("Over/Under 2.5 Goals")
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87, step=0.01)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80, step=0.01)

# Odds for HT/FT
st.sidebar.subheader("Odds")
ht_home_win_odds = st.sidebar.number_input("HT Home Win Odds", value=2.40, step=0.01)
ht_draw_odds = st.sidebar.number_input("HT Draw Odds", value=2.10, step=0.01)
ht_away_win_odds = st.sidebar.number_input("HT Away Win Odds", value=4.50, step=0.01)

ft_home_win_odds = st.sidebar.number_input("FT Home Win Odds", value=1.80, step=0.01)
ft_draw_odds = st.sidebar.number_input("FT Draw Odds", value=3.50, step=0.01)
ft_away_win_odds = st.sidebar.number_input("FT Away Win Odds", value=3.90, step=0.01)

# HT and FT Correct Score Odds
st.sidebar.subheader("Correct Score Odds")
ht_correct_score_odds = st.sidebar.text_area("Enter HT Correct Score Odds (e.g., '0:0=2.58, 0:1=5.84')", 
                                             value="0:0=2.58, 0:1=5.84, 0:2=26.08, 1:0=3.63, 1:1=8.07, 1:2=36.39")
ft_correct_score_odds = st.sidebar.text_area("Enter FT Correct Score Odds (e.g., '0:0=10.41, 0:1=10.74')", 
                                             value="0:0=10.41, 0:1=10.74, 0:2=20.77, 1:0=7.03, 1:1=6.51, 1:2=13.21")

# Helper Function to Convert Score Odds Text to Dictionary
def parse_score_odds(input_text):
    odds_dict = {}
    for item in input_text.split(","):
        score, odds = item.strip().split("=")
        odds_dict[score.strip()] = float(odds.strip())
    return odds_dict

ht_odds_dict = parse_score_odds(ht_correct_score_odds)
ft_odds_dict = parse_score_odds(ft_correct_score_odds)

# Poisson Goal Prediction
st.header("🔢 Poisson Goal Prediction")
st.write("Based on the average goals scored and conceded, we use the Poisson distribution to predict the probability of each scoreline.")

# Calculate Probabilities for Scores
max_goals = 5  # Limit for the number of goals to predict
home_goals = np.arange(0, max_goals + 1)
away_goals = np.arange(0, max_goals + 1)

# Poisson Probability Calculation
home_lambda = avg_goals_home
away_lambda = avg_goals_away
home_prob = poisson.pmf(home_goals, home_lambda)
away_prob = poisson.pmf(away_goals, away_lambda)

# Create a Heatmap for Score Probabilities
score_matrix = np.outer(home_prob, away_prob)

# Plotting Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.matshow(score_matrix, cmap="coolwarm", alpha=0.8)
fig.colorbar(cax)
ax.set_xticks(range(len(away_goals)))
ax.set_yticks(range(len(home_goals)))
ax.set_xticklabels(away_goals)
ax.set_yticklabels(home_goals)
ax.set_xlabel("Away Goals")
ax.set_ylabel("Home Goals")
ax.set_title("Probability Heatmap of Scores")
st.pyplot(fig)

# HT/FT Correct Score Prediction
st.header("📊 HT/FT Correct Score Prediction")
st.write("Using the probabilities and odds, we calculate the most likely HT/FT correct scores:")

# Calculate Likelihood for Each HT/FT Score Combination
ht_scores = ht_odds_dict.keys()
ft_scores = ft_odds_dict.keys()
results = []

for ht_score in ht_scores:
    for ft_score in ft_scores:
        ht_home, ht_away = map(int, ht_score.split(":"))
        ft_home, ft_away = map(int, ft_score.split(":"))
        if ht_home <= ft_home and ht_away <= ft_away:  # Logical constraint
            prob = (poisson.pmf(ht_home, home_lambda) *
                    poisson.pmf(ht_away, away_lambda) *
                    poisson.pmf(ft_home - ht_home, home_lambda) *
                    poisson.pmf(ft_away - ht_away, away_lambda))
            combined_odds = ht_odds_dict[ht_score] * ft_odds_dict[ft_score]
            results.append((ht_score, ft_score, prob, combined_odds))

# Sort Results by Probability
results = sorted(results, key=lambda x: -x[2])

# Display Top 5 Results
st.subheader("Top 5 Predicted HT/FT Correct Scores")
for ht_score, ft_score, prob, odds in results[:5]:
    st.write(f"HT: {ht_score}, FT: {ft_score} - Probability: {prob:.4f}, Combined Odds: {odds:.2f}")
