"""
Birthday Party Planner Streamlit App

This application provides a user interface for planning a birthday party,
with all data stored in JSON format.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, time
import json
from utils.json_handler import (
    get_default_data,
    load_data_from_json,
    download_json_data,
    calculate_budget_totals,
    get_budget_dataframe
)

# Set page config
st.set_page_config(
    page_title="Birthday Party Planner",
    page_icon="🎂",
    layout="wide"
)

# Check if we should load sample data
import sys
import os
import json

# Initialize session state for data
if 'data' not in st.session_state:
    # Check if we have a sample file to load
    sample_file_path = 'sample_birthday_party_plan.json'
    if os.path.exists(sample_file_path):
        try:
            with open(sample_file_path, 'r') as f:
                sample_data = json.load(f)
                st.session_state.data = sample_data
                st.sidebar.success(f"Loaded sample data from {sample_file_path}")
        except Exception as e:
            st.sidebar.error(f"Error loading sample data: {e}")
            st.session_state.data = get_default_data()
    else:
        st.session_state.data = get_default_data()

# App title
st.title("Birthday Party Planner")

# File upload and download section
st.sidebar.header("Save/Load Your Plan")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload a saved plan", type=["json"])
if uploaded_file is not None:
    st.session_state.data = load_data_from_json(uploaded_file)
    st.sidebar.success("Plan loaded successfully!")

# File download
if st.sidebar.button("Save Current Plan"):
    json_data = download_json_data(st.session_state.data)
    current_date = datetime.now().strftime("%Y%m%d")
    st.sidebar.download_button(
        label="Download JSON",
        data=json_data,
        file_name=f"birthday_party_plan_{current_date}.json",
        mime="application/json"
    )

# Create tabs for each section
tab_basic, tab_details, tab_guests, tab_budget, tab_menu, tab_activities, tab_decorations, tab_favors, tab_timeline, tab_notes, tab_checklist = st.tabs([
    "Basic Info", "Party Details", "Guest List", "Budget", "Menu", 
    "Activities", "Decorations", "Party Favors", "Timeline", "Notes", "Checklist"
])

# Basic Information Tab
with tab_basic:
    st.header("Basic Information")
    
    # Get current values from session state
    basic_info = st.session_state.data["basic_info"]
    
    # Create form inputs
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Birthday Person's Name", value=basic_info["name"])
        age = st.text_input("Age Turning", value=basic_info["age"])
        interests = st.text_area("Interests/Hobbies", value=basic_info["interests"])
    
    with col2:
        favorite_colors = st.text_input("Favorite Colors", value=basic_info["favorite_colors"])
        favorite_themes = st.text_input("Favorite Characters/Themes", value=basic_info["favorite_themes"])
    
    # Update session state when values change
    st.session_state.data["basic_info"]["name"] = name
    st.session_state.data["basic_info"]["age"] = age
    st.session_state.data["basic_info"]["interests"] = interests
    st.session_state.data["basic_info"]["favorite_colors"] = favorite_colors
    st.session_state.data["basic_info"]["favorite_themes"] = favorite_themes

# Party Details Tab
with tab_details:
    st.header("Party Details")
    
    # Get current values from session state
    party_details = st.session_state.data["party_details"]
    
    # Create form inputs
    col1, col2 = st.columns(2)
    
    with col1:
        # Convert date string to datetime if it exists
        date_value = None
        if party_details["date"]:
            try:
                date_value = datetime.strptime(party_details["date"], "%Y-%m-%d").date()
            except:
                date_value = None
        
        date = st.date_input("Date", value=date_value)
        
        # Convert time strings to time objects if they exist
        start_time_value = None
        if party_details["start_time"]:
            try:
                start_time_value = datetime.strptime(party_details["start_time"], "%H:%M").time()
            except:
                start_time_value = None
        
        start_time = st.time_input("Start Time", value=start_time_value or time(12, 0))
        
        end_time_value = None
        if party_details["end_time"]:
            try:
                end_time_value = datetime.strptime(party_details["end_time"], "%H:%M").time()
            except:
                end_time_value = None
        
        end_time = st.time_input("End Time", value=end_time_value or time(15, 0))
    
    with col2:
        venue = st.text_input("Venue", value=party_details["venue"])
        theme = st.text_input("Theme", value=party_details["theme"])
        guests_expected = st.number_input("Number of Guests Expected", 
                                         min_value=0, 
                                         value=party_details["guests_expected"])
    
    # Update session state when values change
    st.session_state.data["party_details"]["date"] = date.strftime("%Y-%m-%d") if date else ""
    st.session_state.data["party_details"]["start_time"] = start_time.strftime("%H:%M") if start_time else ""
    st.session_state.data["party_details"]["end_time"] = end_time.strftime("%H:%M") if end_time else ""
    st.session_state.data["party_details"]["venue"] = venue
    st.session_state.data["party_details"]["theme"] = theme
    st.session_state.data["party_details"]["guests_expected"] = guests_expected

# Guest List Tab
with tab_guests:
    st.header("Guest List")
    
    # Get current values from session state
    guest_list = st.session_state.data["guest_list"]
    
    # Create a form for each guest
    st.write("Enter guest information:")
    
    # Ensure we have at least 5 guest entries
    while len(guest_list) < 5:
        guest_list.append({"name": "", "contact": "", "rsvp_status": "", "notes": ""})
    
    # Create columns for the table header
    cols = st.columns([3, 3, 2, 4])
    cols[0].write("**Name**")
    cols[1].write("**Contact Info**")
    cols[2].write("**RSVP Status**")
    cols[3].write("**Notes (Dietary Restrictions, etc.)**")
    
    # Create input fields for each guest
    for i, guest in enumerate(guest_list):
        cols = st.columns([3, 3, 2, 4])
        
        name = cols[0].text_input(f"Name {i+1}", value=guest["name"], key=f"guest_name_{i}", label_visibility="collapsed")
        contact = cols[1].text_input(f"Contact {i+1}", value=guest["contact"], key=f"guest_contact_{i}", label_visibility="collapsed")
        rsvp = cols[2].text_input(f"RSVP {i+1}", value=guest["rsvp_status"], key=f"guest_rsvp_{i}", label_visibility="collapsed")
        notes = cols[3].text_input(f"Notes {i+1}", value=guest["notes"], key=f"guest_notes_{i}", label_visibility="collapsed")
        
        # Update the guest information
        guest_list[i]["name"] = name
        guest_list[i]["contact"] = contact
        guest_list[i]["rsvp_status"] = rsvp
        guest_list[i]["notes"] = notes
    
    # Add button to add more guests
    if st.button("Add Another Guest"):
        guest_list.append({"name": "", "contact": "", "rsvp_status": "", "notes": ""})
    
    # Update session state
    st.session_state.data["guest_list"] = guest_list

# Budget Tab
with tab_budget:
    st.header("Budget Planner")
    
    # Get current values from session state
    budget_data = st.session_state.data["budget"]
    
    # Create input fields for each budget category
    st.write("Enter budget information:")
    
    # Create columns for the table header
    cols = st.columns([3, 2, 2, 5])
    cols[0].write("**Category**")
    cols[1].write("**Estimated Cost**")
    cols[2].write("**Actual Cost**")
    cols[3].write("**Notes**")
    
    # Create input fields for each budget category
    for i, category in enumerate(budget_data["categories"]):
        cols = st.columns([3, 2, 2, 5])
        
        # Category name (read-only)
        cols[0].text_input(f"Category {i+1}", value=category["name"], key=f"budget_category_{i}", disabled=True)
        
        # Estimated cost
        estimated_cost = cols[1].number_input(
            f"Estimated {i+1}", 
            min_value=0.0, 
            value=float(category["estimated_cost"]), 
            key=f"budget_estimated_{i}",
            label_visibility="collapsed"
        )
        
        # Actual cost
        actual_cost = cols[2].number_input(
            f"Actual {i+1}", 
            min_value=0.0, 
            value=float(category["actual_cost"]), 
            key=f"budget_actual_{i}",
            label_visibility="collapsed"
        )
        
        # Notes
        notes = cols[3].text_input(
            f"Notes {i+1}", 
            value=category["notes"], 
            key=f"budget_notes_{i}",
            label_visibility="collapsed"
        )
        
        # Update the category information
        budget_data["categories"][i]["estimated_cost"] = estimated_cost
        budget_data["categories"][i]["actual_cost"] = actual_cost
        budget_data["categories"][i]["notes"] = notes
    
    # Calculate totals
    budget_data = calculate_budget_totals(budget_data)
    
    # Display totals
    st.write("---")
    col1, col2 = st.columns(2)
    col1.metric("Total Estimated Cost", f"${budget_data['total_estimated']:.2f}")
    col2.metric("Total Actual Cost", f"${budget_data['total_actual']:.2f}")
    
    # Budget visualization
    st.subheader("Budget Visualization")
    
    # Create tabs for different visualizations
    viz_tab1, viz_tab2 = st.tabs(["Budget Allocation", "Estimated vs. Actual"])
    
    with viz_tab1:
        # Create a pie chart for budget allocation
        df = get_budget_dataframe(budget_data)
        
        # Filter out categories with zero estimated cost
        df_filtered = df[df["estimated_cost"] > 0]
        
        if not df_filtered.empty:
            fig = px.pie(
                df_filtered, 
                values="estimated_cost", 
                names="name", 
                title="Budget Allocation by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add estimated costs to see budget allocation visualization.")
    
    with viz_tab2:
        # Create a bar chart comparing estimated vs. actual costs
        df = get_budget_dataframe(budget_data)
        
        # Filter out categories with zero costs
        df_filtered = df[(df["estimated_cost"] > 0) | (df["actual_cost"] > 0)]
        
        if not df_filtered.empty:
            # Melt the dataframe to create a format suitable for grouped bar chart
            df_melted = pd.melt(
                df_filtered,
                id_vars=["name"],
                value_vars=["estimated_cost", "actual_cost"],
                var_name="Cost Type",
                value_name="Amount"
            )
            
            # Rename the cost types for better display
            df_melted["Cost Type"] = df_melted["Cost Type"].map({
                "estimated_cost": "Estimated",
                "actual_cost": "Actual"
            })
            
            fig = px.bar(
                df_melted,
                x="name",
                y="Amount",
                color="Cost Type",
                barmode="group",
                title="Estimated vs. Actual Costs by Category",
                labels={"name": "Category", "Amount": "Cost ($)"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add costs to see estimated vs. actual comparison.")
    
    # Update session state
    st.session_state.data["budget"] = budget_data

# Menu Plan Tab
with tab_menu:
    st.header("Menu Plan")
    
    # Get current values from session state
    menu_plan = st.session_state.data["menu_plan"]
    
    # Create form inputs for each section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Main Dishes")
        main_dishes = []
        for i, dish in enumerate(menu_plan["main_dishes"]):
            main_dish = st.text_input(f"Main Dish {i+1}", value=dish, key=f"main_dish_{i}")
            main_dishes.append(main_dish)
        
        st.subheader("Side Dishes")
        side_dishes = []
        for i, dish in enumerate(menu_plan["side_dishes"]):
            side_dish = st.text_input(f"Side Dish {i+1}", value=dish, key=f"side_dish_{i}")
            side_dishes.append(side_dish)
        
        st.subheader("Snacks")
        snacks = []
        for i, snack in enumerate(menu_plan["snacks"]):
            snack_item = st.text_input(f"Snack {i+1}", value=snack, key=f"snack_{i}")
            snacks.append(snack_item)
    
    with col2:
        st.subheader("Desserts")
        desserts = []
        for i, dessert in enumerate(menu_plan["desserts"]):
            dessert_item = st.text_input(f"Dessert {i+1}", value=dessert, key=f"dessert_{i}")
            desserts.append(dessert_item)
        
        st.subheader("Drinks")
        drinks = []
        for i, drink in enumerate(menu_plan["drinks"]):
            drink_item = st.text_input(f"Drink {i+1}", value=drink, key=f"drink_{i}")
            drinks.append(drink_item)
    
    st.subheader("Cake Details")
    cake_details = menu_plan["cake_details"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        flavor = st.text_input("Flavor", value=cake_details["flavor"])
        design = st.text_input("Design", value=cake_details["design"])
        bakery_homemade = st.text_input("Bakery/Homemade", value=cake_details["bakery_homemade"])
    
    with col2:
        order_date = st.text_input("Order Date (if applicable)", value=cake_details["order_date"])
        pickup_delivery_date = st.text_input("Pickup/Delivery Date", value=cake_details["pickup_delivery_date"])
    
    # Update session state
    st.session_state.data["menu_plan"]["main_dishes"] = main_dishes
    st.session_state.data["menu_plan"]["side_dishes"] = side_dishes
    st.session_state.data["menu_plan"]["snacks"] = snacks
    st.session_state.data["menu_plan"]["desserts"] = desserts
    st.session_state.data["menu_plan"]["drinks"] = drinks
    st.session_state.data["menu_plan"]["cake_details"]["flavor"] = flavor
    st.session_state.data["menu_plan"]["cake_details"]["design"] = design
    st.session_state.data["menu_plan"]["cake_details"]["bakery_homemade"] = bakery_homemade
    st.session_state.data["menu_plan"]["cake_details"]["order_date"] = order_date
    st.session_state.data["menu_plan"]["cake_details"]["pickup_delivery_date"] = pickup_delivery_date

# Activities Tab
with tab_activities:
    st.header("Activities & Entertainment")
    
    # Get current values from session state
    activities = st.session_state.data["activities"]
    
    # Planned Activities
    st.subheader("Planned Activities")
    planned_activities = []
    for i, activity in enumerate(activities["planned_activities"]):
        activity_item = st.text_input(f"Activity {i+1}", value=activity, key=f"activity_{i}")
        planned_activities.append(activity_item)
    
    # Entertainment
    st.subheader("Entertainment")
    entertainment = activities["entertainment"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        entertainment_type = st.text_input("Type", value=entertainment["type"])
        entertainment_contact = st.text_input("Contact", value=entertainment["contact"])
    
    with col2:
        entertainment_cost = st.number_input("Cost", min_value=0.0, value=float(entertainment["cost"]))
        entertainment_time = st.text_input("Time Scheduled", value=entertainment["time_scheduled"])
    
    # Update session state
    st.session_state.data["activities"]["planned_activities"] = planned_activities
    st.session_state.data["activities"]["entertainment"]["type"] = entertainment_type
    st.session_state.data["activities"]["entertainment"]["contact"] = entertainment_contact
    st.session_state.data["activities"]["entertainment"]["cost"] = entertainment_cost
    st.session_state.data["activities"]["entertainment"]["time_scheduled"] = entertainment_time

# Decorations Tab
with tab_decorations:
    st.header("Decoration Plan")
    
    # Get current values from session state
    decorations = st.session_state.data["decorations"]
    
    # Color Scheme
    color_scheme = st.text_input("Color Scheme", value=decorations["color_scheme"])
    
    # Key Decorative Elements
    st.subheader("Key Decorative Elements")
    key_elements = []
    for i, element in enumerate(decorations["key_elements"]):
        element_item = st.text_input(f"Element {i+1}", value=element, key=f"element_{i}")
        key_elements.append(element_item)
    
    # Shopping List
    st.subheader("Shopping List")
    shopping_list = []
    for i, item in enumerate(decorations["shopping_list"]):
        shopping_item = st.text_input(f"Item {i+1}", value=item, key=f"shopping_{i}")
        shopping_list.append(shopping_item)
    
    # Update session state
    st.session_state.data["decorations"]["color_scheme"] = color_scheme
    st.session_state.data["decorations"]["key_elements"] = key_elements
    st.session_state.data["decorations"]["shopping_list"] = shopping_list

# Party Favors Tab
with tab_favors:
    st.header("Party Favors")
    
    # Get current values from session state
    party_favors = st.session_state.data["party_favors"]
    
    # Items to Include
    st.subheader("Items to Include")
    items = []
    for i, item in enumerate(party_favors["items"]):
        favor_item = st.text_input(f"Item {i+1}", value=item, key=f"favor_{i}")
        items.append(favor_item)
    
    # Packaging and Cost
    col1, col2 = st.columns(2)
    
    with col1:
        packaging = st.text_input("Packaging", value=party_favors["packaging"])
    
    with col2:
        cost_per_favor = st.number_input("Estimated Cost Per Favor", 
                                        min_value=0.0, 
                                        value=float(party_favors["cost_per_favor"]))
    
    # Update session state
    st.session_state.data["party_favors"]["items"] = items
    st.session_state.data["party_favors"]["packaging"] = packaging
    st.session_state.data["party_favors"]["cost_per_favor"] = cost_per_favor

# Timeline Tab
with tab_timeline:
    st.header("Timeline & Task Assignment")
    
    # Get current values from session state
    timeline = st.session_state.data["timeline"]
    
    # Create a section for each timeline period
    timeline_periods = [
        ("3-4 Weeks Before", "3_4_weeks_before"),
        ("1-2 Weeks Before", "1_2_weeks_before"),
        ("Few Days Before", "few_days_before"),
        ("Day Before", "day_before"),
        ("Day of Party", "day_of_party")
    ]
    
    for display_name, period_key in timeline_periods:
        st.subheader(display_name)
        
        # Get tasks for this period
        tasks = timeline[period_key]
        
        # Create columns for the table header
        cols = st.columns([1, 8, 4, 2])
        cols[0].write("**Done**")
        cols[1].write("**Task**")
        cols[2].write("**Person Responsible**")
        
        # Create input fields for each task
        for i, task in enumerate(tasks):
            cols = st.columns([1, 8, 4, 2])
            
            # Checkbox for completion status
            completed = cols[0].checkbox(
                f"Completed {period_key}_{i}", 
                value=task["completed"],
                key=f"task_completed_{period_key}_{i}",
                label_visibility="collapsed"
            )
            
            # Task description
            task_desc = cols[1].text_input(
                f"Task {period_key}_{i}", 
                value=task["task"],
                key=f"task_desc_{period_key}_{i}",
                label_visibility="collapsed"
            )
            
            # Person responsible
            person = cols[2].text_input(
                f"Person {period_key}_{i}", 
                value=task["person_responsible"],
                key=f"task_person_{period_key}_{i}",
                label_visibility="collapsed"
            )
            
            # Add button
            if i == len(tasks) - 1 and cols[3].button("+", key=f"add_task_{period_key}"):
                tasks.append({"task": "", "person_responsible": "", "completed": False})
            
            # Update task information
            tasks[i]["completed"] = completed
            tasks[i]["task"] = task_desc
            tasks[i]["person_responsible"] = person
        
        # Update session state for this period
        st.session_state.data["timeline"][period_key] = tasks
        
        st.write("---")

# Special Notes Tab
with tab_notes:
    st.header("Special Notes & Reminders")
    
    # Get current values from session state
    special_notes = st.session_state.data["special_notes"]
    
    # Create text areas for each note
    notes = []
    for i, note in enumerate(special_notes):
        note_text = st.text_area(f"Note {i+1}", value=note, key=f"note_{i}", height=100)
        notes.append(note_text)
    
    # Add button to add more notes
    if st.button("Add Another Note"):
        notes.append("")
    
    # Update session state
    st.session_state.data["special_notes"] = notes

# Post-Party Checklist Tab
with tab_checklist:
    st.header("Post-Party Checklist")
    
    # Get current values from session state
    checklist = st.session_state.data["post_party_checklist"]
    
    # Create checkboxes for each item
    clean_up = st.checkbox("Clean up venue", value=checklist["clean_up_venue"])
    return_rentals = st.checkbox("Return any rentals", value=checklist["return_rentals"])
    thank_you = st.checkbox("Send thank you notes", value=checklist["send_thank_you_notes"])
    share_photos = st.checkbox("Share photos", value=checklist["share_photos"])
    note_worked = st.checkbox("Note what worked well for future reference", value=checklist["note_what_worked"])
    
    # Update session state
    st.session_state.data["post_party_checklist"]["clean_up_venue"] = clean_up
    st.session_state.data["post_party_checklist"]["return_rentals"] = return_rentals
    st.session_state.data["post_party_checklist"]["send_thank_you_notes"] = thank_you
    st.session_state.data["post_party_checklist"]["share_photos"] = share_photos
    st.session_state.data["post_party_checklist"]["note_what_worked"] = note_worked

# Footer
st.write("---")
st.write("Birthday Party Planner App - Plan your perfect celebration!")
