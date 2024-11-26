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
def recommend_correct_score(ht_probs, ft_probs, correct_score_odds_halftime, correct_score_odds_fulltime):
    """Recommend the most probable HT/FT correct score."""
    best_ht_score = max(ht_probs)
    best_ft_score = max(ft_probs)
    
    ht_recommendation = list(correct_score_odds_halftime.keys())[np.argmax(ht_probs)]
    ft_recommendation = list(correct_score_odds_fulltime.keys())[np.argmax(ft_probs)]
    
    st.subheader("Recommended Correct Score")
    st.write(f"Most likely HT score: {ht_recommendation} with a probability of {best_ht_score*100:.2f}%")
    st.write(f"Most likely FT score: {ft_recommendation} with a probability of {best_ft_score*100:.2f}%")

recommend_correct_score(ht_probs, ft_probs, correct_score_odds_halftime, correct_score_odds_fulltime)

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

        # Identify High and Moderate Realistic Outcomes for Fulltime
        fulltime_high = {score: prob for score, prob in fulltime_score_probs.items() if prob > 0.30}
        fulltime_moderate = {score: prob for score, prob in fulltime_score_probs.items() if 0.20 < prob <= 0.30}

        # Identify High and Moderate Realistic Outcomes for Halftime
        halftime_high = {score: prob for score, prob in halftime_score_probs.items() if prob > 0.30}
        halftime_moderate = {score: prob for score, prob in halftime_score_probs.items() if 0.20 < prob <= 0.30}

        # Display Fulltime Score Probabilities as text
        st.write("### Fulltime Score Probabilities (Poisson):")
        fulltime_score_text = "\n".join([f"Score {score}: Probability {prob*100:.2f}%" for score, prob in fulltime_score_probs.items()])
        st.write(fulltime_score_text)

        # Display Halftime Score Probabilities as text
        st.write("### Halftime Score Probabilities (Poisson):")
        halftime_score_text = "\n".join([f"Score {score}: Probability {prob*100:.2f}%" for score, prob in halftime_score_probs.items()])
        st.write(halftime_score_text)

        # Display Recommendations
        st.write("### Recommended Moderate and High Realistic Outcomes:")

        st.write("#### High Realistic Fulltime Scores:")
        for score, prob in fulltime_high.items():
            st.write(f"{score}: Probability {prob*100:.2f}%")

        st.write("#### Moderate Fulltime Scores:")
        for score, prob in fulltime_moderate.items():
            st.write(f"{score}: Probability {prob*100:.2f}%")

        st.write("#### High Realistic Halftime Scores:")
        for score, prob in halftime_high.items():
            st.write(f"{score}: Probability {prob*100:.2f}%")

        st.write("#### Moderate Halftime Scores:")
        for score, prob in halftime_moderate.items():
            st.write(f"{score}: Probability {prob*100:.2f}%")

          # Fulltime Score Probabilities
        home_win_prob = sum([score_matrix[i, j] for i in range(5) for j in range(i+1, 5)])  # Home Win (Home > Away)
        away_win_prob = sum([score_matrix[i, j] for i in range(5) for j in range(i) ])    # Away Win (Away > Home)
        draw_prob = sum([score_matrix[i, i] for i in range(5)])  # Draw (Home == Away)

        # BTTS (Both Teams to Score) Probability (Yes: Both teams score)
        btts_yes_prob = sum([score_matrix[i, j] for i in range(1, 5) for j in range(1, 5)])  # Home and Away both score
        btts_no_prob = 1 - btts_yes_prob  # BTTS No: One team doesn't score

        # Over/Under Goals Probabilities (Total goals > or < x)
        over_1_5_prob = sum([score_matrix[i, j] for i in range(3, 5) for j in range(3, 5)])  # Over 1.5 Goals
        under_1_5_prob = 1 - over_1_5_prob  # Under 1.5 Goals
        over_2_5_prob = sum([score_matrix[i, j] for i in range(3, 5) for j in range(3, 5) if (i + j) > 2])  # Over 2.5 Goals
        under_2_5_prob = 1 - over_2_5_prob  # Under 2.5 Goals

        # Display Recommendations for Fulltime Outcomes
        st.write("### Recommended Match Result Outcomes:")

        st.write(f"#### Home Win Probability: {home_win_prob * 100:.2f}%")
        st.write(f"#### Draw Probability: {draw_prob * 100:.2f}%")
        st.write(f"#### Away Win Probability: {away_win_prob * 100:.2f}%")

        # Display BTTS Probability
        st.write(f"#### BTTS Yes Probability: {btts_yes_prob * 100:.2f}%")
        st.write(f"#### BTTS No Probability: {btts_no_prob * 100:.2f}%")

        # Display Over/Under Goals Probabilities
        st.write(f"#### Over 1.5 Goals Probability: {over_1_5_prob * 100:.2f}%")
        st.write(f"#### Under 1.5 Goals Probability: {under_1_5_prob * 100:.2f}%")
        st.write(f"#### Over 2.5 Goals Probability: {over_2_5_prob * 100:.2f}%")
        st.write(f"#### Under 2.5 Goals Probability: {under_2_5_prob * 100:.2f}%")
def poisson_probability(lam, k):
    """
    Calculate Poisson probability for a given lambda (mean goals) and k (number of goals).
    """
    return (lam**k * np.exp(-lam)) / math.factorial(k)

def calculate_full_time_correct_score(home_mean, away_mean):
    """
    Calculate and recommend Full-time Correct Score for a football match using Poisson distribution.
    """
    max_goals = 4  # We assume the maximum goals to be 4 for simplicity, this can be adjusted

    score_probabilities = {}
    
    # Calculate Poisson probabilities for each scoreline
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            home_prob = poisson_probability(home_mean, home_goals)
            away_prob = poisson_probability(away_mean, away_goals)
            score_probabilities[f"{home_goals}-{away_goals}"] = home_prob * away_prob

    # Sort the scorelines by probability in descending order
    sorted_scores = sorted(score_probabilities.items(), key=lambda x: x[1], reverse=True)
    
    # Display the top 5 most likely scorelines
    recommendations = []
    for score, prob in sorted_scores[:5]:
        recommendations.append(f"{score} - Probability: {prob*100:.2f}%")
    
    return recommendations

# Example input: average goals for home team and away team (mean values)
home_mean_goals = 1.5  # Example: Home Team average goals scored per match
away_mean_goals = 1.2  # Example: Away Team average goals scored per match

# Get Full-time Correct Score recommendations
correct_score_recommendations = calculate_full_time_correct_score(home_mean_goals, away_mean_goals)

# Display Recommendations for Full-time Correct Score
for recommendation in correct_score_recommendations:
    st.write(recommendation)
 
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
