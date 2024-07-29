import streamlit as st
import requests
import json

# List of tags
tags = [
    "AIXI", "Coherent Extrapolated Volition", "Complexity of Value", "Corrigibility",
    "deceptive-alignment", "Decision Theory", "Embedded Agency", "Fixed Point Theorems",
    "Goodhart's Law", "Goal-Directedness", "Gradient Hacking", "Infra-Bayesianism",
    "Inner Alignment", "Instrumental Convergence", "Intelligence Explosion",
    "Logical Induction", "Logical Uncertainty", "Mesa-Optimization", "Multipolar Scenarios",
    "Myopia", "Newcomb's Problem", "Optimization", "Orthogonality Thesis", "Outer Alignment",
    "Paperclip Maximizer", "Power Seeking (AI)", "Recursive Self-Improvement",
    "simulator-theory", "Sharp Left Turn", "Solomonoff Induction", "Superintelligence",
    "Symbol Grounding", "Transformative AI", "Treacherous Turn", "Utility Functions",
    "Whole Brain Emulation"
]

st.title("AI Safety collaborator finder")

# Dropdown for selecting a tag
selected_tag = st.selectbox("Select a tag:", tags)

# Text area for user profile
user_profile = st.text_area("Enter your profile:", height=200)

# Button to submit
if st.button("Find Friends"):
    if user_profile:
        # Prepare the data to send to the API
        data = {
            "tag": selected_tag,
            "user_profile": user_profile
        }

        # Make a POST request to your API
        try:
            response = requests.post("http://localhost:8000/recommend_friends", json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the JSON response
            result = response.json()

            # Display the recommended friends
            st.subheader("Potential collaborators:")
            st.write(result["recommended_friends"])
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your profile before submitting.")
