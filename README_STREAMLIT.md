# Birthday Party Planner Streamlit App

This Streamlit application provides an interactive interface for planning a birthday party, with all data stored in JSON format. The app is based on the Birthday Party Planning Worksheet and includes features for managing all aspects of party planning.

## Features

- **Tabbed Interface**: Organized sections for each aspect of party planning
- **JSON Data Storage**: Save and load your party plans as JSON files
- **Budget Visualization**: Visual charts for budget allocation and spending
- **Guest List Management**: Track RSVPs and guest information
- **Timeline Management**: Organize tasks with assignments and completion tracking
- **Comprehensive Planning**: Covers all aspects from basic information to post-party checklist

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the App

To run the app, navigate to the project directory and execute:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser.

## Usage

### Navigation

The app is organized into tabs, each representing a different section of the party planning process:

1. **Basic Info**: Enter details about the birthday person
2. **Party Details**: Set date, time, venue, and theme
3. **Guest List**: Manage invitees and their RSVP status
4. **Budget**: Track estimated and actual costs with visualizations
5. **Menu**: Plan food, drinks, and cake details
6. **Activities**: Organize entertainment and activities
7. **Decorations**: Plan decorative elements and shopping list
8. **Party Favors**: Manage party favor items and packaging
9. **Timeline**: Assign tasks with deadlines and track completion
10. **Notes**: Add special notes and reminders
11. **Checklist**: Track post-party tasks

### Saving and Loading Data

- Use the sidebar to upload a previously saved plan
- Click "Save Current Plan" to download your current plan as a JSON file
- The app automatically maintains your data between tabs using Streamlit's session state

### Budget Visualization

The Budget tab includes two visualization options:
- **Budget Allocation**: Pie chart showing the distribution of estimated costs
- **Estimated vs. Actual**: Bar chart comparing estimated and actual costs by category

## Data Structure

All data is stored in a structured JSON format that mirrors the organization of the planning worksheet. This makes it easy to save, load, and modify your party planning data.

## Customization

You can customize the app by modifying the following files:

- `app.py`: Main application logic and UI
- `utils/json_handler.py`: Functions for handling JSON data
- `requirements.txt`: Required packages

## Requirements

- Python 3.7+
- Streamlit 1.22.0+
- Pandas
- Matplotlib
- Plotly

## License

This project is open source and available for personal and commercial use.
