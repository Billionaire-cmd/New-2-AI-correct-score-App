import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(mean, goals):
    return poisson.pmf(goals, mean)

# Function to predict correct scores
def predict_scores(team_a_mean, team_b_mean):
    scores = []
    probs = []
    for a in range(6):  # Maximum of 5 goals considered
        for b in range(6):
            prob = poisson_prob(team_a_mean, a) * poisson_prob(team_b_mean, b)
            scores.append(f"{a}-{b}")
            probs.append(prob)
    df = pd.DataFrame({"Scoreline": scores, "Probability": probs})
    df = df.sort_values(by="Probability", ascending=False).reset_index(drop=True)
    return df

# Function for BTTS (GG/NG) probability
def btts_probability(team_a_mean, team_b_mean):
    btts = 1 - (poisson_prob(team_a_mean, 0) * poisson_prob(team_b_mean, 0))
    return btts

# Function for over/under 2.5 goals
def over_under_probability(team_a_mean, team_b_mean):
    total_prob = 0
    for a in range(6):
        for b in range(6):
            if a + b > 2.5:  # Over 2.5 goals
                total_prob += poisson_prob(team_a_mean, a) * poisson_prob(team_b_mean, b)
    return total_prob

# Function to recommend the best bet
def recommend_bet(predictions, btts, over):
    top_score = predictions.iloc[0]['Scoreline']
    if btts > 0.6 and over > 0.7:
        return f"Best Bet: Both Teams to Score (BTTS) and Over 2.5 Goals."
    else:
        return f"Best Bet: Correct Score Prediction: {top_score}"

# Streamlit App
st.title("Sports Betting Correct Score Predictor")

st.sidebar.header("Input Match Statistics")
team_a_mean = st.sidebar.slider("Team A Average Goals", 0.5, 3.0, 1.5, 0.1)
team_b_mean = st.sidebar.slider("Team B Average Goals", 0.5, 3.0, 1.2, 0.1)

st.sidebar.header("Odds")
team_a_odds = st.sidebar.number_input("Team A Win Odds", value=2.5)
team_b_odds = st.sidebar.number_input("Team B Win Odds", value=2.8)
draw_odds = st.sidebar.number_input("Draw Odds", value=3.0)

# Predict correct scores
st.subheader("Correct Score Prediction")
predictions = predict_scores(team_a_mean, team_b_mean)
st.table(predictions.head(5))

# Calculate BTTS probability
btts = btts_probability(team_a_mean, team_b_mean)
st.subheader("Both Teams to Score (BTTS)")
st.write(f"Probability: {btts:.2%} (GG if > 60%)")

# Calculate Over/Under 2.5 goals probability
over = over_under_probability(team_a_mean, team_b_mean)
st.subheader("Over/Under 2.5 Goals")
st.write(f"Probability of Over 2.5 Goals: {over:.2%}")

# Recommend best bet
st.subheader("AI Bet Recommendation")
recommendation = recommend_bet(predictions, btts, over)
st.write(recommendation)

st.write("**Example Outcome:** HT/FT = (0-1/2-1)")
st.write("This means Halftime result is 0-1, and Fulltime result is 2-1.")
