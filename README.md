# Birthday Party Planner

A Streamlit application for planning birthday parties with comprehensive features for managing all aspects of party planning.

## Overview

This application provides an interactive interface for planning a birthday party, with all data stored in JSON format. The app is based on a comprehensive Birthday Party Planning Worksheet and includes features for managing all aspects of party planning.

## Features

- **Tabbed Interface**: Organized sections for each aspect of party planning
- **JSON Data Storage**: Save and load your party plans as JSON files
- **Budget Visualization**: Visual charts for budget allocation and spending
- **Guest List Management**: Track RSVPs and guest information
- **Timeline Management**: Organize tasks with assignments and completion tracking
- **Comprehensive Planning**: Covers all aspects from basic information to post-party checklist

## Project Structure

```
birthday_planner/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── sample_birthday_party_plan.json  # Sample data file
├── README.md              # This file
├── README_STREAMLIT.md    # Detailed documentation for the Streamlit app
└── utils/
    ├── __init__.py
    └── json_handler.py    # Functions for JSON operations
```

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the App

To run the app, navigate to the project directory and execute:

```bash
python -m streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser. The app will automatically load the sample data file if it exists.

## Sample Data

The repository includes a sample JSON file (`sample_birthday_party_plan.json`) that demonstrates all the features of the app. This file is automatically loaded when you start the app, providing a comprehensive example of a birthday party plan.

## Testing

You can test the app with the sample data by running:

```bash
python -m streamlit run app.py
```

The app will automatically load the sample data file and display it in the interface.

## Usage

See the [README_STREAMLIT.md](README_STREAMLIT.md) file for detailed usage instructions.

## License

This project is open source and available for personal and commercial use.
