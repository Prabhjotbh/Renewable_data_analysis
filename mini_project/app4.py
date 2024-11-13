import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

energy_req_df = pd.read_csv('EnergyReq.csv')
hydro_inflow_gen_df = pd.read_csv('HydroInflowandGen.csv')
interstate_transfer_df = pd.read_csv('InterstateEnergyTransfer.csv')

st.title('Energy Data Engineering Dashboard')

st.header('Energy Requirement vs Availability for Selected States')
states_to_plot = st.multiselect('Select States:', energy_req_df['State'].unique(), default=['Andhra Pradesh', 'Assam'])
fig, ax = plt.subplots()
for state in states_to_plot:
    state_data = energy_req_df[energy_req_df['State'] == state]
    ax.plot(state_data['Year'], state_data['Requirement (MU)'], label=f'{state} Requirement')
    ax.plot(state_data['Year'], state_data['Availability (MU)'], linestyle='--', label=f'{state} Availability')

ax.set_xlabel('Year')
ax.set_ylabel('Energy (MU)')
ax.legend()
st.pyplot(fig)

st.header('Hydro Inflows vs Generation')
fig, ax = plt.subplots()
ax.scatter(hydro_inflow_gen_df['INFLOWS (MCM)'], hydro_inflow_gen_df['GENERATION (GWH)'], color='g', alpha=0.6)
ax.set_xlabel('Inflows (MCM)')
ax.set_ylabel('Generation (GWH)')
st.pyplot(fig)


st.header('Interstate Energy Transfer Over Time')
year_selected = st.slider('Select Year Range', int(interstate_transfer_df['Year'].min()), int(interstate_transfer_df['Year'].max()), (2000, 2010))
filtered_transfer_df = interstate_transfer_df[(interstate_transfer_df['Year'] >= year_selected[0]) & (interstate_transfer_df['Year'] <= year_selected[1])]
fig, ax = plt.subplots()
ax.plot(filtered_transfer_df['Year'], filtered_transfer_df['ENERGRY TRANSFERED (GWH)'], color='b')
ax.set_xlabel('Year')
ax.set_ylabel('Energy Transferred (GWH)')
st.pyplot(fig)

# Total Energy Requirement vs Availability (Bar Plot)
st.header('Total Energy Requirement vs Availability (All States)')
total_energy_by_year = energy_req_df.groupby('Year')[['Requirement (MU)', 'Availability (MU)']].sum()
st.bar_chart(total_energy_by_year)

# Pie Chart - Energy requirement by state for a specific year
st.header('Energy Requirement Proportion by State for Selected Year')
year_for_pie = st.selectbox('Select Year:', energy_req_df['Year'].unique())
energy_by_state_in_year = energy_req_df[energy_req_df['Year'] == year_for_pie]
fig, ax = plt.subplots()
ax.pie(energy_by_state_in_year['Requirement (MU)'], labels=energy_by_state_in_year['State'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Heatmap of Inflow vs Generation
st.header('Correlation Heatmap: Inflow and Generation Data')
corr = hydro_inflow_gen_df[['INFLOWS (MCM)', 'GENERATION (GWH)']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Energy Prediction for Future Years (Line Plot)
st.header('Energy Requirement Predictions for 2025-2030')
predictions = {2025: 30353, 2026: 30885, 2027: 31416, 2028: 31947, 2029: 32478, 2030: 33009}
fig, ax = plt.subplots()
ax.plot(list(predictions.keys()), list(predictions.values()), marker='o', linestyle='-', color='r')
ax.set_xlabel('Year')
ax.set_ylabel('Predicted Energy Requirement (MU)')
ax.set_title('Energy Requirement Predictions (2025-2030)')
st.pyplot(fig)

st.write('Predicted Energy Requirements (MU):')
st.write(predictions)
