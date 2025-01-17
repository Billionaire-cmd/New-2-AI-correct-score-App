import streamlit as st

# Function to calculate the final correct score based on the rules
def calculate_correct_score(probabilities):
    # Sort probabilities in descending order
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    
    # Extract key probabilities for rule application
    highest = sorted_probs[0]  # Highest correct score probability
    second_highest = sorted_probs[1]  # Second highest probability
    middle = sorted_probs[4:6]  # 5th and 6th probabilities for middle range
    lowest = sorted_probs[-1]  # Lowest probability
    
    # Rule-based logic
    # Rule 1
    if 6.8 >= middle[0][1] >= 6.02:
        return middle[0][0]
    
    # Rule 2
    if 5.71 >= middle[0][1] >= 5.2 and highest[1] == 12.9:
        return middle[0][0]
    
    # Rule 3
    if 6.5 >= middle[0][1] >= 6.19 and highest[1] == 11.38:
        return middle[0][0]
    
    # Rule 4
    if highest[1] == 12.26 and 6.38 >= middle[0][1] >= 6.07:
        corresponding = [x[0] for x in sorted_probs if x[1] == highest[1]]
        return corresponding[0]
    
    # Rule 5
    if 6.85 >= middle[0][1] >= 6.39 and highest[1] == 11.99:
        return middle[0][0]
    
    # Rule 6
    if highest[1] == 20.39 and len([x[1] for x in sorted_probs if x[1] == 6.77]) == 1:
        return sorted_probs[1][0]  # 10.15 corresponds to the second highest
    
    # Rule 7
    if highest[1] == 11.92 and 6.08 in [x[1] for x in middle]:
        return middle[1][0]
    
    # Rule 8
    if highest[1] == 9.25:
        return sorted_probs[2][0]  # Third descending scoreline
    
    # Rule 9
    if highest[1] == 12.26:
        competitive = [x for x in sorted_probs if x[1] in [6.67, 6.38, 6.07]]
        if competitive:
            return competitive[0][0]
    
    # Rule 10
    if highest[1] == 11.54:
        competitive = [x for x in sorted_probs if x[1] in [6.99, 6.63, 6.08]]
        if len(competitive) > 0:
            return sorted_probs[1][0]  # 10.03 is second highest after 11.54
    
    # Rule 11
    if highest[1] == 12.26 and len([x[1] for x in sorted_probs if x[1] in [6.74, 6.36]]) > 0:
        return sorted_probs[1][0]  # 11.14℅ corresponds to the second highest after 12.26℅

    # Rule 12
    if highest[1] == 12.45 and len([x[1] for x in sorted_probs if x[1] in [6.85, 6.54]]) > 0:
        return sorted_probs[1][0]  # 11.32℅ corresponds to the second highest after 12.45℅

    # Rule 13
    if highest[1] == 13.02 and len([x[1] for x in sorted_probs if x[1] in [6.83, 5.26]]) > 0:
        return sorted_probs[2][0]  # 0-3 corresponds to 3.18% for final score

    # Rule 14
    if highest[1] == 10.54 and len([x[1] for x in sorted_probs if x[1] in [6.85, 6.2, 6.17]]) > 0:
        return sorted_probs[-1][0]  # 6.17℅ is the final correct score for the game

    # Rule 15
    if highest[1] == 12.90 and second_highest[1] == 11.22:
        fifth_position = sorted_probs[4]  # 5th position in sorted probabilities
        if fifth_position[1] == 8.39:
            return fifth_position[0]  # Return the scoreline at 8.39%

    # Default fallback
    return highest[0]

# Streamlit UI
st.title("🤖🤖🤖🤑💯Rabiotic Correct Score Probability℅ Analyzer")
st.sidebar.header("Input the 12 Top Most Likely Scorelines")

# Input fields for scorelines and probabilities
probabilities = {}
for i in range(1, 13):
    scoreline = st.sidebar.text_input(f"Scoreline {i} (e.g., 2-1):", key=f"scoreline_{i}")
    probability = st.sidebar.number_input(f"Probability ℅ for {scoreline}:", min_value=0.0, max_value=100.0, key=f"prob_{i}")
    if scoreline:
        probabilities[scoreline] = probability

# Predict button
if st.sidebar.button("Predict"):
    if len(probabilities) == 12:
        final_score = calculate_correct_score(probabilities)
        st.success(f"The final correct score based on the rules is: {final_score}")
    else:
        st.error("Please input all 12 scorelines and their probabilities.")

# Additional features and UI enhancements
st.markdown("""
### How It Works:
1. Input the 12 most likely scorelines and their probabilities in the sidebar.
2. Click the 'Predict' button to calculate the final correct score based on the predefined rules.
3. The final correct score will be displayed below.

### Rules Applied:
- **Rule 1:** If the highest frequency of correct score probability ℅ ranges from 6.8℅ to 6.02℅, pick the corresponding scoreline.
- ...
- **Rule 15:** If the highest scoreline correct score probability ℅ is 12.90℅ and 11.22℅ is the second highest probability℅, pick 8.39℅ at the fifth position as the final correct score if 6.02℅ is not present in the probabilities.
""")
