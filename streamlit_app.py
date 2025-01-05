import streamlit as st

# Title of the app
st.title("🤖🤖🤖Rabiotic Correct Score Probability℅ Of Scorelines Analyzer")
st.markdown("## Final 💯 Correct Score Calculator")
st.markdown("### Powered by Rabiotic Rules")

# Sidebar for user input
st.sidebar.title("Input 12 Top Most Likely Scorelines")
st.sidebar.markdown("Enter the **Scorelines and Probability%** in descending order.")

# Input fields for scorelines and probabilities
scorelines = []
probabilities = []

for i in range(1, 13):
    scoreline = st.sidebar.text_input(f"Scoreline {i}", key=f"scoreline_{i}")
    probability = st.sidebar.number_input(f"Probability℅ for Scoreline {i}", min_value=0.0, max_value=100.0, step=0.01, key=f"probability_{i}")
    if scoreline and probability:
        scorelines.append(scoreline)
        probabilities.append(probability)

# Function to apply Rabiotic rules
def calculate_final_score(scorelines, probabilities):
    sorted_data = sorted(zip(probabilities, scorelines), reverse=True)  # Sort by descending probabilities
    probabilities, scorelines = zip(*sorted_data)
    
    highest_probability = probabilities[0]
    highest_middle_probabilities = probabilities[4:6]  # 5th and 6th probabilities
    
    # Apply the rules
    if 6.8 <= probabilities[4] <= 6.02:
        final_score = scorelines[4]
    elif 5.71 <= probabilities[4] <= 5.2:
        final_score = scorelines[4]
    elif 6.50 <= probabilities[4] <= 6.19:
        final_score = scorelines[4]
    elif probabilities[0] == 12.26 and 6.38 <= probabilities[4] <= 6.07:
        final_score = scorelines[4]
    elif 6.85 <= probabilities[4] <= 6.39:
        final_score = scorelines[4]
    elif probabilities[0] == 20.39 and len(probabilities) == 6:
        final_score = scorelines[5]
    elif probabilities[0] == 11.92 and 6.08 in highest_middle_probabilities:
        final_score = scorelines[5]
    elif probabilities[0] == 9.25:
        final_score = scorelines[2]
    elif probabilities[0] == 12.26 and 6.67 in probabilities:
        final_score = scorelines[1]
    elif probabilities[0] == 11.54 and probabilities[5] > probabilities[4]:
        final_score = scorelines[5]
    else:
        final_score = scorelines[4]  # Default to the 5th scoreline
    
    return final_score

# Predict Button
if st.sidebar.button("Predict Final Correct Score"):
    if len(scorelines) == 12 and len(probabilities) == 12:
        final_score = calculate_final_score(scorelines, probabilities)
        st.success(f"🎯 The Final Correct Score is: **{final_score}**")
    else:
        st.error("Please input all 12 Scorelines and their Probabilities℅.")

# Footer
st.markdown("---")
st.markdown("**Designed by Rabiotic Analyzer**")
