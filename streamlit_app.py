import numpy as np
from scipy.stats import poisson
import pandas as pd

# Example Team Data (for demonstration purposes)
team_data = {
    'Team A': {'attack': 1.5, 'defense': 1.2},  # goals per match
    'Team B': {'attack': 1.2, 'defense': 1.0}   # goals per match
}

# Bookmaker Odds (for HT/FT)
bookmaker_odds = {
    'HT Home': 2.5, 'HT Draw': 3.0, 'HT Away': 3.5,
    'FT Home': 2.8, 'FT Draw': 3.2, 'FT Away': 3.0
}

# Poisson Distribution Function for Goal Prediction
def poisson_prob(lmbda, max_goals=4):
    return [poisson.pmf(i, lmbda) for i in range(max_goals + 1)]

# Calculate Expected Goals (HT and FT)
ht_home_goals = team_data['Team A']['attack'] * 0.6 + team_data['Team B']['defense'] * 0.4
ht_away_goals = team_data['Team B']['attack'] * 0.6 + team_data['Team A']['defense'] * 0.4
ft_home_goals = team_data['Team A']['attack'] * 0.6 + team_data['Team B']['defense'] * 0.4
ft_away_goals = team_data['Team B']['attack'] * 0.6 + team_data['Team A']['defense'] * 0.4

# HT and FT Poisson Probabilities
ht_home_probs = poisson_prob(ht_home_goals)
ht_away_probs = poisson_prob(ht_away_goals)
ft_home_probs = poisson_prob(ft_home_goals)
ft_away_probs = poisson_prob(ft_away_goals)

# Predict the HT/FT score combinations (e.g., 1-0, 2-1)
def predict_ht_ft(ht_home_probs, ht_away_probs, ft_home_probs, ft_away_probs):
    predictions = []
    for ht_home in range(4):
        for ht_away in range(4):
            for ft_home in range(5):
                for ft_away in range(5):
                    prob_ht = ht_home_probs[ht_home] * ht_away_probs[ht_away]
                    prob_ft = ft_home_probs[ft_home] * ft_away_probs[ft_away]
                    predictions.append(((ht_home, ht_away), (ft_home, ft_away), prob_ht * prob_ft))
    return predictions

# Get Predictions
predictions = predict_ht_ft(ht_home_probs, ht_away_probs, ft_home_probs, ft_away_probs)

# Sort Predictions by Probability
predictions.sort(key=lambda x: x[2], reverse=True)

# Output Top 5 HT/FT Predictions
top_predictions = predictions[:5]
for prediction in top_predictions:
    st.write(f"HT: {prediction[0]} -> FT: {prediction[1]} with Probability: {prediction[2]:.2f}")

