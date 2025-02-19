import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# FastAPI base URL
BASE_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.title("Energy Metrics Dashboard")

# User inputs
site_ids = st.multiselect("Select Site IDs", options=['site_1', 'site_2', 'site_3'])
start_time = st.date_input("Start Date", value=datetime(2025, 2, 17))
end_time = st.date_input("End Date", value=datetime(2025, 2, 18))

if st.button("Fetch Data"):
    all_records = []

    for site_id in site_ids:
        # Fetch records for each selected site
        response = requests.get(f"{BASE_URL}/records/", params={
            "site_id": site_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        })

        if response.status_code == 200:
            records = response.json()
            all_records.extend(records)  # Collect records from all sites
        else:
            st.write(f"Error fetching data for {site_id}.")

    if all_records:
        df = pd.DataFrame(all_records)
        st.write("### Records", df)

        # Energy generation vs. consumption per site
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='site_id', y='energy_generated_kwh', color='blue', label='Generated')
        sns.barplot(data=df, x='site_id', y='energy_consumed_kwh', color='red', label='Consumed', alpha=0.6)
        plt.title('Energy Generation vs. Consumption per Site')
        plt.xlabel('Site ID')
        plt.ylabel('Energy (kWh)')
        plt.legend()
        st.pyplot(plt)
        # ------------------------------------------------------------------------
        # Energy trends over time
        energy_trend_plot_columns = ['timestamp', 'energy_generated_kwh', 'energy_consumed_kwh']
        energy_trend_plot_df = df[energy_trend_plot_columns]

        energy_trend_plot_df['timestamp'] = pd.to_datetime(energy_trend_plot_df['timestamp'])

        # day-to-day changes
        energy_trend_df = energy_trend_plot_df.set_index('timestamp').resample('D').mean()

        plt.figure(figsize=(12, 6))
        energy_trend_df['energy_generated_kwh'].plot(label='Generated', color='blue')
        energy_trend_df['energy_consumed_kwh'].plot(label='Consumed', color='red')
        plt.title('Energy Trends Over Time')
        plt.xlabel('Time')
        plt.ylabel('Energy (kWh)')
        plt.legend()
        st.pyplot(plt)

        # ------------------------------------------------------------------------
        # Weather condition vs Energy Generation
        plt.figure(figsize=(12, 6))
        sns.pointplot(data=df, x='weather_condition', y='energy_generated_kwh',
                      ci=95, capsize=0.1)
        plt.title('Energy Generation by Weather Condition')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Weather condition vs Energy Consumption
        plt.figure(figsize=(12, 6))
        sns.pointplot(data=df, x='weather_condition', y='energy_consumed_kwh',
                      ci=95, capsize=0.1)
        plt.title('Energy Consumed by Weather Condition')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # ------------------------------------------------------------------------
        # Energy metrics by site
        plt.figure(figsize=(15, 6))
        df_site_avg = df.groupby('site_id').agg({
            'energy_generated_kwh': 'mean',
            'energy_consumed_kwh': 'mean',
            'temperature_c': 'mean',
            'humidity_percent': 'mean'
        }).reset_index()

        df_site_avg.plot(x='site_id', kind='bar', rot=0)
        plt.title('Average Metrics by Site')
        st.pyplot(plt)

    else:
        st.write("No records found for the selected criteria.")
