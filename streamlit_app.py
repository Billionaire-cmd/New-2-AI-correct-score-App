import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import poisson

# Helper function to predict match outcome using Poisson distribution
def poisson_predict(home_goals_lambda, away_goals_lambda):
    home_goals = poisson.pmf(np.arange(0, 5), home_goals_lambda)
    away_goals = poisson.pmf(np.arange(0, 5), away_goals_lambda)
    
    score_matrix = np.outer(home_goals, away_goals)
    return score_matrix

# Helper function for machine learning model prediction
def ml_predict(team_stats, model):
    prediction = model.predict(team_stats)
    return prediction

# Streamlit input form
st.title("Sports Betting Prediction App")
st.write("Enter team data to predict the correct score for both HT/FT")

# Team data input
team_a_goals = st.number_input("Team A Average Goals", min_value=0.0, value=1.5)
team_b_goals = st.number_input("Team B Average Goals", min_value=0.0, value=1.2)

# Poisson model predictions
team_a_lambda = team_a_goals
team_b_lambda = team_b_goals

score_matrix = poisson_predict(team_a_lambda, team_b_lambda)

st.subheader("Predicted Correct Score Matrix (Poisson)")
st.write(score_matrix)

# Machine learning model (RandomForest in this case)
# Sample input: recent matches data, player stats, etc.
team_stats = np.array([[team_a_goals, team_b_goals]])  # Example, extend with more features

# Load pre-trained model (assuming the model is saved as a .joblib file)
model = RandomForestClassifier()
model.load("trained_model.joblib")

ml_prediction = ml_predict(team_stats, model)
st.subheader("ML Model Prediction")
st.write(ml_prediction)

# Insights on betting markets (e.g., odds comparison)
# For simplicity, this is just a placeholder example
st.subheader("Betting Market Insights")
st.write("Recommended betting odds for high payout: Match Outcome A win, Draw")

# Display results for correct score predictions
st.subheader("Predicted Correct Scores (HT/FT)")
st.write("Full-Time Predictions: 2-1, 1-0, 1-1")
st.write("Half-Time Predictions: 1-0, 0-0")
