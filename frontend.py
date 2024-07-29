import streamlit as st
import requests
import json

# List of tags
tags = [
    "aixi", "coherent-extrapolated-volition", "complexity-of-value", "corrigibility",
    "deceptive-alignment", "decision-theory", "embedded-agency", "fixed-point-theorems",
    "goodhart's-law", "goal-directedness", "gradient-hacking", "infra-bayesianism",
    "inner-alignment", "instrumental-convergence", "intelligence-explosion",
    "logical-induction", "logical-uncertainty", "mesa-optimization", "multipolar-scenarios",
    "myopia", "newcomb's-problem", "optimization", "orthogonality-thesis", "outer-alignment",
    "paperclip-maximizer", "power-seeking-(ai)", "recursive-self-improvement",
    "simulator-theory", "sharp-left-turn", "solomonoff-induction", "superintelligence",
    "symbol-grounding", "transformative-ai", "treacherous-turn", "utility-functions",
    "whole-brain-emulation"
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
