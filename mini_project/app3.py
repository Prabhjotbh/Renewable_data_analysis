import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Solar Plant Analysis", layout="wide")

st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stPlotly {
            background-color: #ffffff;
            border-radius: 5px;
            padding: 1rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("☀️ Solar Plant Performance Analytics")
st.markdown("Interactive dashboard for solar plant performance analysis and prediction")

with st.sidebar:
    st.header("Data Controls")
    uploaded_generation = st.file_uploader("Upload Generation Data", type=['csv'])
    uploaded_weather = st.file_uploader("Upload Weather Data", type=['csv'])
    
    if uploaded_generation and uploaded_weather:
        generation_data = pd.read_csv(uploaded_generation)
        weather_data = pd.read_csv(uploaded_weather)

        generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
        weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])
        
        data = pd.merge(generation_data, weather_data, 
                       on=['DATE_TIME', 'PLANT_ID'],
                       how='inner')

        data['hour'] = data['DATE_TIME'].dt.hour
        data['month'] = data['DATE_TIME'].dt.month
        data['day_of_week'] = data['DATE_TIME'].dt.dayofweek

        data['DC_POWER'] = pd.to_numeric(data['DC_POWER'], errors='coerce')
        data.fillna(0, inplace=True)

        features = ['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION',
                   'hour', 'month', 'day_of_week']
        X = data[features]
        y = data['DC_POWER']
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        data['predicted_power'] = model.predict(X)
        data['power_ratio'] = data['DC_POWER'] / (data['predicted_power'] + 1e-6)
        
        if 'SOURCE_KEY_x' in data.columns:
            group_key = 'SOURCE_KEY_x'
        elif 'SOURCE_KEY_y' in data.columns:
            group_key = 'SOURCE_KEY_y'
        else:
            group_key = 'PLANT_ID'
    
        data['power_ratio'] = pd.to_numeric(data['power_ratio'], errors='coerce')
        data['power_ratio_ma'] = data.groupby(group_key)['power_ratio'].transform(
            lambda x: x.rolling(window=48, min_periods=1).mean()
        )
        
        st.success("✅ Data loaded and model trained successfully!")
        
        st.header("Analysis Controls")
        cleaning_threshold = st.slider("Cleaning Threshold", 0.5, 1.0, 0.85)
        std_dev_threshold = st.slider("Fault Detection Threshold (std dev)", 1.0, 5.0, 3.0)
        sample_size = st.slider("Sample Size for Plots", 1000, 10000, 5000)

if 'data' in locals():
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Power Generation", "🧹 Maintenance Needs", 
                                     "⚠️ Fault Detection", "📊 Performance Metrics"])
    
    with tab1:
        st.header("Power Generation Analysis")

        daily_pattern = data.groupby('hour')['DC_POWER'].mean().reset_index()
        fig_daily = px.line(daily_pattern, x='hour', y='DC_POWER', 
                           title='Average Daily Power Generation Pattern')
        fig_daily.update_layout(height=400)
        st.plotly_chart(fig_daily, use_container_width=True)

        sampled_data = data.sample(n=sample_size, random_state=42)
        fig_pred = px.scatter(sampled_data, 
                            x='DC_POWER', 
                            y='predicted_power',
                            title='Actual vs Predicted Power Generation')

        max_power = max(sampled_data['DC_POWER'].max(), sampled_data['predicted_power'].max())
        fig_pred.add_trace(go.Scatter(x=[0, max_power], 
                                    y=[0, max_power],
                                    mode='lines', 
                                    name='Perfect Prediction',
                                    line=dict(color='red', dash='dash')))
        
        fig_pred.update_layout(
            xaxis_title="Actual Power (DC)",
            yaxis_title="Predicted Power (DC)",
            height=500
        )
        st.plotly_chart(fig_pred, use_container_width=True)

        importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=True)
        
        fig_imp = px.bar(importance, x='importance', y='feature', orientation='h',
                        title='Feature Importance')
        st.plotly_chart(fig_imp, use_container_width=True)
    
    with tab2:
        st.header("Maintenance Needs Analysis")

        cleaning_needs = data[data['power_ratio_ma'] < cleaning_threshold][
            ['DATE_TIME', group_key, 'power_ratio_ma']
        ].drop_duplicates()

        pivot_data = data.pivot_table(values='power_ratio_ma', 
                                    index=pd.Grouper(key='DATE_TIME', freq='D'),
                                    columns=group_key,
                                    aggfunc='mean')

        pivot_data = pivot_data.apply(pd.to_numeric, errors='coerce')
        
        fig_heatmap = px.imshow(pivot_data,
                               title='Panel Performance Heatmap',
                               color_continuous_scale='RdYlBu')
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.subheader("Panels Needing Maintenance")
        st.dataframe(cleaning_needs)
    
    with tab3:
        st.header("Fault Detection")
        
        panel_stats = data.groupby(group_key).agg({
            'DC_POWER': ['mean', 'std'],
            'power_ratio': ['mean', 'std']
        }).reset_index()
        
        panel_stats.columns = [group_key, 'power_mean', 'power_std', 
                             'ratio_mean', 'ratio_std']
        
        power_mean_std = panel_stats['power_mean'].std()
        ratio_mean_std = panel_stats['ratio_mean'].std()
        
        faulty_panels = panel_stats[
            (abs(panel_stats['power_mean'] - panel_stats['power_mean'].mean()) > 
             std_dev_threshold * power_mean_std) |
            (abs(panel_stats['ratio_mean'] - panel_stats['ratio_mean'].mean()) > 
             std_dev_threshold * ratio_mean_std)
        ]

        sampled_data_dist = data.sample(n=min(len(data), sample_size))
        fig_dist = px.box(sampled_data_dist, x=group_key, y='power_ratio',
                         title='Panel Performance Distribution')
        st.plotly_chart(fig_dist, use_container_width=True)
        
        st.subheader("Potentially Faulty Panels")
        st.dataframe(faulty_panels)
    
    with tab4:
        st.header("Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Daily Generation", 
                     f"{data['DC_POWER'].mean():.2f} kW")
        
        with col2:
            st.metric("Peak Generation", 
                     f"{data['DC_POWER'].max():.2f} kW")
        
        with col3:
            st.metric("Generation Efficiency", 
                     f"{data['power_ratio'].mean()*100:.1f}%")
        
        daily_data = data.resample('D', on='DATE_TIME').mean()
        fig_ts = px.line(daily_data, 
                        y='DC_POWER',
                        title='Daily Power Generation Trend')
        st.plotly_chart(fig_ts, use_container_width=True)
        
        results = pd.DataFrame({
            'DATE_TIME': data['DATE_TIME'],
            'PLANT_ID': data['PLANT_ID'],
            'DC_POWER': data['DC_POWER'],
            'predicted_power': data['predicted_power'],
            'power_ratio': data['power_ratio']
        })
        
        st.download_button("Download Results", results.to_csv(), "results.csv")

else:
    st.info("Upload both generation and weather data to start the analysis.")
