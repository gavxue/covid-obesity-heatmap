# COVID-19 and Obesity Rate Visualization

This project visualizes COVID-19 cases and obesity rates across US states using interactive choropleth maps. The application is built with Streamlit and Plotly, and it processes data from CSV files to generate insights on the correlation between COVID-19 case growth and obesity rates.

## Features

- **COVID-19 Map**: Displays the growth of COVID-19 cases by state.
- **Obesity Map**: Shows obesity rates by state.
- **Combined Map**: Provides a dual-layer choropleth map to compare COVID-19 case growth and obesity rates.

## Requirements

- streamlit
- pandas
- plotly

## Usage

1. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

3. Open the provided URL in your browser to interact with the visualizations.

## Data Sources

- `covid_confirmed_usafacts.csv`: Contains COVID-19 case data.
- `obesity-2022.csv`: Contains obesity rate data for the year 2022.
- `2023-Obesity-by-demographic.csv`: Contains obesity rate data by demographic for the year 2023.