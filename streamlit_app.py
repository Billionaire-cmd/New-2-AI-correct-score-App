import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals=4):
    """Calculate Poisson probabilities up to max_goals."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Function to Calculate Bookmaker's Margin
def calculate_margin(odds_list):
    """Calculate bookmaker's margin given a list of odds."""
    return (sum(1 / odds for odds in odds_list) - 1) * 100

# Function to Calculate Expected Value
def calculate_expected_value(prob, odds):
    """Calculate expected value."""
    return (prob * odds) - 1
# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals=5):
    """Calculate Poisson probabilities up to max_goals."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, betting odds, and team statistics, 
to predict realistic halftime and full-time correct scores for football matches.  
It is designed to enhance your betting strategies by providing precise calculations for maximum ROI.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Average Points
avg_points_home = st.sidebar.number_input("Average Points for Home Team", min_value=0.0, step=0.1, value=1.8)
avg_points_away = st.sidebar.number_input("Average Points for Away Team", min_value=0.0, step=0.1, value=1.5)

# Betting Odds for HT and FT
st.sidebar.subheader("Halftime Odds")
ht_home = st.sidebar.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
ht_draw = st.sidebar.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
ht_away = st.sidebar.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

st.sidebar.subheader("Fulltime Odds")
ft_home = st.sidebar.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
ft_draw = st.sidebar.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
ft_away = st.sidebar.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# Correct Score Odds for HT and FT
def get_correct_score_odds(prefix, max_goals, half_time=True):
    """Generate correct score odds inputs for HT or FT."""
    score_odds = {}
    for i in range(max_goals):
        for j in range(max_goals):
            score = f"{i}:{j}"
            score_odds[score] = st.sidebar.number_input(f"{prefix} Odds for {score}", value=10.0, step=0.01)
    score_odds["Other"] = st.sidebar.number_input(f"{prefix} Odds for scores exceeding {max_goals-1}:{max_goals-1}", value=50.0, step=0.01)
    return score_odds

correct_score_odds_halftime = get_correct_score_odds("HT", 3)
correct_score_odds_fulltime = get_correct_score_odds("FT", 5, half_time=False)

# Calculate Probabilities for HT/FT based on odds
def calculate_probabilities(odds_list):
    """Calculate probabilities based on odds."""
    return [1 / odds for odds in odds_list]

ht_probs = calculate_probabilities([ht_home, ht_draw, ht_away])
ft_probs = calculate_probabilities([ft_home, ft_draw, ft_away])

# Calculate Margins for HT and FT
ht_margin = calculate_margin([ht_home, ht_draw, ht_away])
ft_margin = calculate_margin([ft_home, ft_draw, ft_away])

# Display HT/FT probabilities and margins
st.write(f"Halftime Probabilities: {np.round(ht_probs, 3)}")
st.write(f"Fulltime Probabilities: {np.round(ft_probs, 3)}")
st.write(f"Halftime Bookmaker Margin: {ht_margin:.2f}%")
st.write(f"Fulltime Bookmaker Margin: {ft_margin:.2f}%")

# Halftime/Fulltime Correct Score Recommendation
# HT Score Information
st.subheader("Most Likely HT Score (90% Probability)")
ht_recommendation = list(correct_score_odds_halftime.keys())[np.argmax(ht_probs)]
ht_probability = max(ht_probs) * 100
st.write(f"Recommended HT Score: {ht_recommendation}")
st.write(f"Probability: {ht_probability:.2f}%")
# Example probabilities for Home Win, Draw, and Away Win
outcomes = {
    "Home Win": 0.23,  # 23% probability
    "Draw": 0.18,      # 18% probability
    "Away Win": 0.22   # 22% probability
}

# Define the probability range
lower_bound = 0.20  # 20%
upper_bound = 0.25  # 25%

# Find outcomes within the range
def find_outcomes_in_range(outcomes, lower_bound, upper_bound):
    results_in_range = {outcome: prob for outcome, prob in outcomes.items() 
                        if lower_bound <= prob <= upper_bound}
    return results_in_range

# Get the outcomes within the range
results_in_range = find_outcomes_in_range(outcomes, lower_bound, upper_bound)

# Display results
if results_in_range:
    print("Outcomes within 20% to 25% probability range:")
    for outcome, prob in results_in_range.items():
        print(f"- {outcome}: {prob * 100:.2f}%")
else:
    print("No outcomes found within the 20% to 25% probability range.")

# FT Score Information
st.subheader("Most Likely FT Score")
ft_recommendation = list(correct_score_odds_fulltime.keys())[np.argmax(ft_probs)]
ft_probability = max(ft_probs) * 100
st.write(f"Recommended FT Score: {ft_recommendation}")
st.write(f"Probability: {ft_probability:.2f}%")

# FT Probability Range
ft_probability_range = "20% to 25% (combined)"
st.subheader("Fulltime Probability Range")
st.write(f"Combined FT Probability Range: {ft_probability_range}")

# Exact Goals Odds Calculation (Optional)
st.sidebar.subheader("Exact Goals Odds (0 to 6+ Goals)")
exact_goals_odds = {
    "0 Goals": st.sidebar.number_input("Odds for 0 Goals", min_value=1.0, step=0.1, value=6.0),
    "1 Goal": st.sidebar.number_input("Odds for 1 Goal", min_value=1.0, step=0.1, value=5.5),
    "2 Goals": st.sidebar.number_input("Odds for 2 Goals", min_value=1.0, step=0.1, value=4.0),
    "3 Goals": st.sidebar.number_input("Odds for 3 Goals", min_value=1.0, step=0.1, value=3.0),
    "4 Goals": st.sidebar.number_input("Odds for 4 Goals", min_value=1.0, step=0.1, value=2.5),
    "5 Goals": st.sidebar.number_input("Odds for 5 Goals", min_value=1.0, step=0.1, value=15.0),
    "6+ Goals": st.sidebar.number_input("Odds for 6+ Goals", min_value=1.0, step=0.1, value=30.0)
}

# Calculate Exact Goal Probabilities
exact_goal_probs = {}
total_odds = sum(1 / value for value in exact_goals_odds.values())
for goal, odds in exact_goals_odds.items():
    prob = 1 / odds
    exact_goal_probs[goal] = prob / total_odds * 100
    
# Display Exact Goal Probabilities
st.write(f"Exact Goal Probabilities: {exact_goal_probs}")

# Button to predict probabilities and insights
if st.button("Predict Probabilities and Insights"):
    try:
        # Calculate Poisson Probabilities for Fulltime
        fulltime_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)

        # Calculate Poisson Probabilities for Halftime (assuming halftime goals are ~50% of fulltime goals)
        halftime_home_avg = avg_goals_home / 2
        halftime_away_avg = avg_goals_away / 2
        halftime_home_probs = calculate_poisson_prob(halftime_home_avg, max_goals=2)
        halftime_away_probs = calculate_poisson_prob(halftime_away_avg, max_goals=2)
        halftime_score_matrix = np.outer(halftime_home_probs, halftime_away_probs)

        # Calculate Fulltime Score Probabilities
        fulltime_score_probs = {f"{i}:{j}": score_matrix[i, j] for i in range(5) for j in range(5)}
        fulltime_other_prob = 1 - sum(fulltime_score_probs.values())
        fulltime_score_probs["Other"] = fulltime_other_prob

        # Calculate Halftime Score Probabilities
        halftime_score_probs = {f"{i}:{j}": halftime_score_matrix[i, j] for i in range(3) for j in range(3)}
        halftime_other_prob = 1 - sum(halftime_score_probs.values())
        halftime_score_probs["Other"] = halftime_other_prob

                # Determine Most Likely Match Result
        most_likely_result = max(
            [("Home Win", home_win_prob), ("Draw", draw_prob), ("Away Win", away_win_prob)],
            key=lambda x: x[1]
        )

        # Determine Most Likely Correct Score
        most_likely_score = max(fulltime_score_probs.items(), key=lambda x: x[1])

        # Display Results
        st.subheader("Match Outcome Predictions")
        st.write(f"Most Probable Match Result: {most_likely_result[0]} ({most_likely_result[1] * 100:.2f}%)")
        st.write(f"Recommended Correct Score: {most_likely_score[0]} ({most_likely_score[1] * 100:.2f}%)")

        # Display Fulltime Score Probabilities
        st.subheader("Top Fulltime Score Predictions")
        top_fulltime_scores = sorted(fulltime_score_probs.items(), key=lambda x: x[1], reverse=True)[:5]
        for score, prob in top_fulltime_scores:
            st.write(f"{score}: {prob * 100:.2f}%")

    except Exception as e:
        st.error(f"Error: {str(e)}")
