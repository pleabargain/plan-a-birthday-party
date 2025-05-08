"""
JSON Handler for Birthday Party Planner

This module provides functions for handling JSON data in the Birthday Party Planner app.
"""

import json
import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd

def get_default_data() -> Dict[str, Any]:
    """
    Returns the default data structure for the birthday party planner.
    
    Returns:
        Dict[str, Any]: The default data structure
    """
    return {
        "basic_info": {
            "name": "",
            "age": "",
            "interests": "",
            "favorite_colors": "",
            "favorite_themes": ""
        },
        "party_details": {
            "date": "",
            "start_time": "",
            "end_time": "",
            "venue": "",
            "theme": "",
            "guests_expected": 0
        },
        "guest_list": [
            {"name": "", "contact": "", "rsvp_status": "", "notes": ""}
            for _ in range(5)  # Default 5 empty rows
        ],
        "budget": {
            "categories": [
                {"name": "Venue", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Food", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Cake", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Drinks", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Decorations", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Entertainment", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Party Favors", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Invitations", "estimated_cost": 0, "actual_cost": 0, "notes": ""},
                {"name": "Other", "estimated_cost": 0, "actual_cost": 0, "notes": ""}
            ],
            "total_estimated": 0,
            "total_actual": 0
        },
        "menu_plan": {
            "main_dishes": ["", "", ""],
            "side_dishes": ["", "", ""],
            "snacks": ["", "", ""],
            "desserts": ["", "", ""],
            "drinks": ["", "", ""],
            "cake_details": {
                "flavor": "",
                "design": "",
                "bakery_homemade": "",
                "order_date": "",
                "pickup_delivery_date": ""
            }
        },
        "activities": {
            "planned_activities": ["", "", "", "", ""],
            "entertainment": {
                "type": "",
                "contact": "",
                "cost": 0,
                "time_scheduled": ""
            }
        },
        "decorations": {
            "color_scheme": "",
            "key_elements": ["", "", "", ""],
            "shopping_list": ["", "", "", "", ""]
        },
        "party_favors": {
            "items": ["", "", "", ""],
            "packaging": "",
            "cost_per_favor": 0
        },
        "timeline": {
            "3_4_weeks_before": [
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False}
            ],
            "1_2_weeks_before": [
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False}
            ],
            "few_days_before": [
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False}
            ],
            "day_before": [
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False}
            ],
            "day_of_party": [
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False},
                {"task": "", "person_responsible": "", "completed": False}
            ]
        },
        "special_notes": ["", "", "", ""],
        "post_party_checklist": {
            "clean_up_venue": False,
            "return_rentals": False,
            "send_thank_you_notes": False,
            "share_photos": False,
            "note_what_worked": False
        }
    }

def load_data_from_json(uploaded_file) -> Dict[str, Any]:
    """
    Loads data from an uploaded JSON file.
    
    Args:
        uploaded_file: The uploaded file object from st.file_uploader
        
    Returns:
        Dict[str, Any]: The loaded data
    """
    try:
        content = uploaded_file.read()
        data = json.loads(content)
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return get_default_data()

def download_json_data(data: Dict[str, Any]) -> str:
    """
    Converts the data to a JSON string for download.
    
    Args:
        data (Dict[str, Any]): The data to convert
        
    Returns:
        str: The JSON string
    """
    return json.dumps(data, indent=2)

def calculate_budget_totals(budget_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates the total estimated and actual costs from the budget data.
    
    Args:
        budget_data (Dict[str, Any]): The budget data
        
    Returns:
        Dict[str, Any]: The updated budget data with totals
    """
    total_estimated = sum(category["estimated_cost"] for category in budget_data["categories"])
    total_actual = sum(category["actual_cost"] for category in budget_data["categories"])
    
    budget_data["total_estimated"] = total_estimated
    budget_data["total_actual"] = total_actual
    
    return budget_data

def get_budget_dataframe(budget_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts the budget data to a pandas DataFrame for visualization.
    
    Args:
        budget_data (Dict[str, Any]): The budget data
        
    Returns:
        pd.DataFrame: The budget data as a DataFrame
    """
    df = pd.DataFrame(budget_data["categories"])
    return df
