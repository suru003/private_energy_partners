# Energy Metrics Dashboard

## Overview
A Streamlit-based interactive dashboard for visualizing and analyzing renewable energy data fetched from a FastAPI backend.

## Features Explained
#### 1. Multi-site Data Selection
Allows users to choose and compare energy metrics from multiple renewable energy sites simultaneously, enabling comprehensive cross-site analysis.

#### 2. Date Range Filtering
Provides flexible time-based data exploration, letting users zoom into specific periods to analyze energy generation and consumption patterns over custom timeframes.

### 3. Energy Generation vs. Consumption Visualization
Displays a comparative bar chart showing energy generated and consumed across different sites, helping identify production and consumption imbalances.

### Plots
#### 4. Energy Trends Over Time
Presents a line graph tracking daily energy generation and consumption trends, revealing seasonal patterns, efficiency changes, and long-term performance.

#### 5. Weather Condition Impact on Energy Metrics
Illustrates how different weather conditions (sunny, cloudy, rainy) affect energy generation and consumption, supporting predictive maintenance and planning.

#### 6. Site-level Energy Performance
Aggregates and compares key metrics like average energy generation, consumption, temperature, and humidity across different sites, facilitating performance benchmarking.

---

## Prerequisites
- Python 3.8+
- Required Libraries:
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `seaborn`

## Installation
```bash
pip install streamlit pandas requests matplotlib seaborn
```

## Running the Dashboard
```bash
streamlit run dashboard.py
```

## Visualizations
1. Bar chart: Energy generation and consumption per site
2. Line graph: Energy trends over time
3. Point plots: Weather condition impact on energy metrics
4. Bar graph: Average site-level metrics

## Configuration
- Modify `BASE_URL` to match your FastAPI server endpoint
- Customize site IDs and date ranges as needed

## Usage
1. Select site(s)
2. Choose start and end dates
3. Click "Fetch Data"
4. Explore interactive visualizations

## Notes
- Requires active FastAPI backend
- Assumes data availability in specified date range

## Recommended Browser
- Chrome
- Firefox
- Edge (Chromium-based)