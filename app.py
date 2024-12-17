import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

def load_and_process_data(start_date=None, end_date=None):
    """
    Load and process COVID and obesity datasets with date range selection
    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
    """
    try:
        # Load COVID data
        covid_df = pd.read_csv('covid_confirmed_usafacts.csv')
        
        # Get all date columns (excluding metadata columns)
        date_columns = covid_df.columns[4:]  # Skip countyFIPS, County Name, State, StateFIPS
        available_dates = list(date_columns)
        
        # Print available date range
        print(f"\nAvailable date range: {available_dates[0]} to {available_dates[-1]}")
        
        # Validate and set dates
        if start_date is None or start_date not in available_dates:
            start_date = available_dates[0]
            print(f"Using default start date: {start_date}")
            
        if end_date is None or end_date not in available_dates:
            end_date = available_dates[-1]
            print(f"Using default end date: {end_date}")
            
        # Ensure start date comes before end date
        if available_dates.index(start_date) > available_dates.index(end_date):
            raise ValueError("Start date must be before end date")
            
        print(f"Analyzing COVID data from {start_date} to {end_date}")
        
        # Calculate state totals for selected date range
        covid_state_totals = covid_df.groupby('State').agg({
            start_date: 'sum',
            end_date: 'sum'
        }).reset_index()
        
        # Rename columns and calculate growth
        covid_state_totals.columns = ['State', 'InitialCases', 'FinalCases']
        covid_state_totals['CaseGrowth'] = covid_state_totals['FinalCases'] - covid_state_totals['InitialCases']
        
        # Add case rate per 100k calculation
        # state_populations = covid_df.groupby('State')[start_date].count()  # Using county count as a proxy for population
        # covid_state_totals['CasesPer100k'] = (covid_state_totals['CaseGrowth'] / 
        #                                      state_populations * 100000)
        
        # Print summary statistics
        print("\nCOVID Data Summary:")
        print(f"Total cases at start: {covid_state_totals['InitialCases'].sum():,}")
        print(f"Total cases at end: {covid_state_totals['FinalCases'].sum():,}")
        print(f"Total growth: {covid_state_totals['CaseGrowth'].sum():,}")
        
        # Load and process obesity data
        obesity_df = pd.read_csv('obesity-2022.csv')
        obesity_df.rename(columns={"Prevalence": "ObesityRate"}, inplace='true')
        
        # Define region mapping
        # region_mapping = {
        #     'Northeast': ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA'],
        #     'Midwest': ['OH', 'IN', 'IL', 'MI', 'WI', 'MN', 'IA', 'MO', 'ND', 'SD', 'NE', 'KS'],
        #     'South': ['DE', 'MD', 'DC', 'VA', 'WV', 'NC', 'SC', 'GA', 'FL', 'KY', 'TN', 'AL', 'MS', 'AR', 'LA', 'OK', 'TX'],
        #     'West': ['MT', 'ID', 'WY', 'CO', 'NM', 'AZ', 'UT', 'NV', 'WA', 'OR', 'CA', 'AK', 'HI']
        # }
        
        # Define regional obesity rates
        # region_rates = {
        #     'Northeast': 28.6,
        #     'Midwest': 36.0,
        #     'South': 34.7,
        #     'West': 29.1
        # }
        
        # Create state-level obesity dataset
        # states_obesity = []
        # for region, states in region_mapping.items():
        #     for state in states:
        #         states_obesity.append({
        #             'State': state,
        #             'ObesityRate': float(region_rates[region])
        #         })
        
        # obesity_state = pd.DataFrame(states_obesity)
        
        # Merge datasets
        # merged_data = covid_state_totals.merge(obesity_state, on='State', how='outer')
        merged_data = covid_state_totals.merge(obesity_df, on='State', how='outer')
        
        # Normalize the data
        merged_data['CovidGrowthNormalized'] = merged_data['CaseGrowth'] / merged_data['CaseGrowth'].max()
        merged_data['ObesityNormalized'] = merged_data['ObesityRate'] / 100
        
        print("\nMerged Data Sample:")
        print(merged_data.head())
        print(f"\nTotal states processed: {len(merged_data)}")
        
        return merged_data
        
    except Exception as e:
        print(f"Error in load_and_process_data: {str(e)}")
        raise e

def create_obesity_choropleth():
    """
    Create a choropleth map showing only obesity rates
    """
    # Load the processed data
    state_data = load_and_process_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add choropleth layer for obesity
    fig.add_choropleth(
        locations=state_data['State'],
        z=state_data['ObesityRate'],
        locationmode='USA-states',
        colorscale='Blues',
        showscale=True,
        name='Obesity Rate',
        colorbar=dict(
            title="Obesity Rate (%)",
            x=1.0,
            xanchor='left'
        ),
        zmin=20,
        zmax=40
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='Obesity Rates by State',
            x=0.5,
            y=0.95
        ),
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        width=800,
        height=500,
        margin=dict(r=80, l=40, t=60, b=20)
    )
    
    return fig

def create_covid_choropleth():
    """
    Create a choropleth map showing only COVID-19 cases
    """
    # Load the processed data
    state_data = load_and_process_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add choropleth layer for COVID cases
    fig.add_choropleth(
        locations=state_data['State'],
        z=state_data['FinalCases'],
        locationmode='USA-states',
        colorscale='Reds',
        showscale=True,
        name='COVID-19 Cases',
        colorbar=dict(
            title="COVID-19 Cases<br>(Normalized)",
            x=1.0,
            xanchor='left'
        ),
        zmin=0,
        zmax=11300486
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='COVID-19 Cases by State',
            x=0.5,
            y=0.95
        ),
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        width=800,
        height=500,
        margin=dict(r=80, l=40, t=60, b=20)
    )
    
    return fig

def create_dual_choropleth():
    """
    Create a dual-layer choropleth map using Plotly
    """
    # Load the processed data
    state_data = load_and_process_data()
    
    # Create the base figure
    fig = go.Figure()
    
    # Add first choropleth layer for COVID cases
    fig.add_choropleth(
        locations=state_data['State'],
        z=state_data['CovidGrowthNormalized'],
        locationmode='USA-states',
        colorscale='Reds',
        showscale=True,
        name='COVID-19 Cases',
        colorbar=dict(
            title="COVID-19 Cases<br>(Normalized)",
            x=1.0,
            xanchor='left'
        ),
        zmin=0,
        zmax=1
    )
    
    # Add second choropleth layer for obesity
    fig.add_choropleth(
        locations=state_data['State'],
        z=state_data['ObesityNormalized'],
        locationmode='USA-states',
        colorscale='Blues',
        showscale=True,
        name='Obesity Rate',
        colorbar=dict(
            title="Obesity Rate",
            x=1.2,
            xanchor='left'
        ),
        zmin=0,
        zmax=1,
        marker=dict(opacity=0.6)
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='COVID-19 Cases and Obesity Rates by State',
            x=0.5,
            y=0.95
        ),
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        width=1000,  # Increased width to accommodate both colorbars
        height=600,
        margin=dict(r=100, l=40, t=60, b=20)  # Adjusted margins
    )
    
    return fig

def main():
    st.title('COVID-19 and Obesity Rate Visualization')
    
    st.write("""
    These visualizations show COVID-19 cases and obesity rates across US states. 
    Select different tabs to view each metric separately.
    """)
    
    try:
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["COVID-19 Map", "Obesity Map", "Combined Map"])
        
        with tab1:
            st.subheader("COVID-19 Cases by State")
            fig_covid = create_covid_choropleth()
            st.plotly_chart(fig_covid)
            
        with tab2:
            st.subheader("Obesity Rates by State")
            fig_obesity = create_obesity_choropleth()
            st.plotly_chart(fig_obesity)
            
        with tab3:
            st.subheader("Combined COVID-19 and Obesity Rates")
            fig_combined = create_dual_choropleth()
            st.plotly_chart(fig_combined)
        
        # Show data table
        st.subheader('Raw Data')
        merged_data = load_and_process_data()
        st.dataframe(merged_data)
        
    except Exception as e:
        st.error("""
            Error loading data. Please ensure you have both required CSV files:
            - covid_confirmed_usafacts.csv
            - obesity_data.csv
        """)
        st.exception(e)

if __name__ == "__main__":
    main()
