"""
Test script to load the sample JSON file directly into the Streamlit app.
"""

import json
import streamlit as st
import sys
import os
from utils.json_handler import get_default_data

def main():
    # Load the sample JSON file
    sample_file_path = 'sample_birthday_party_plan.json'
    
    try:
        with open(sample_file_path, 'r') as f:
            sample_data = json.load(f)
            print(f"Successfully loaded sample data from {sample_file_path}")
            
            # Print some key information from the loaded data
            print(f"Birthday Person: {sample_data['basic_info']['name']}")
            print(f"Party Theme: {sample_data['party_details']['theme']}")
            print(f"Number of Guests: {sample_data['party_details']['guests_expected']}")
            print(f"Total Budget (Estimated): ${sample_data['budget']['total_estimated']}")
            print(f"Total Budget (Actual): ${sample_data['budget']['total_actual']}")
            
            # Set the data in the session state
            # Note: This will only work when run within the Streamlit app context
            if 'data' in st.session_state:
                st.session_state.data = sample_data
                print("Data loaded into session state")
            else:
                print("Warning: Not running in Streamlit context, can't set session state")
                
    except Exception as e:
        print(f"Error loading sample data: {e}")
        return

if __name__ == "__main__":
    main()
