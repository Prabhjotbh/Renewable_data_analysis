import streamlit as st
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt

plant1_gen = pd.read_csv('D:/sem5/de/mini_project/Plant_1_Generation_Data.csv')
plant2_gen = pd.read_csv('D:/sem5/de/mini_project/Plant_2_Generation_Data.csv')
plant1_sens = pd.read_csv('D:/sem5/de/mini_project/Plant_1_Weather_Sensor_Data.csv')
plant2_sens = pd.read_csv('D:/sem5/de/mini_project/Plant_2_Weather_Sensor_Data.csv')

plant1_gendaily = plant1_gen.groupby('DATE_TIME')[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']].agg('sum').reset_index()
plant2_gendaily = plant2_gen.groupby('DATE_TIME')[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']].agg('sum').reset_index()

plant1_gendaily['DATE_TIME'] = pd.to_datetime(plant1_gendaily['DATE_TIME'], format='%d-%m-%Y %H:%M')
plant1_gendaily['TIME'] = plant1_gendaily['DATE_TIME'].dt.time
plant1_gendaily['DATE'] = plant1_gendaily['DATE_TIME'].dt.date

plant2_gendaily['DATE_TIME'] = pd.to_datetime(plant2_gendaily['DATE_TIME'])
plant2_gendaily['TIME'] = plant2_gendaily['DATE_TIME'].dt.time
plant2_gendaily['DATE'] = plant2_gendaily['DATE_TIME'].dt.date

today = pd.to_datetime('today').normalize()  

plant1_gendaily['TIME'] = plant1_gendaily['TIME'].apply(lambda x: today + pd.Timedelta(hours=x.hour, minutes=x.minute, seconds=x.second))
plant2_gendaily['TIME'] = plant2_gendaily['TIME'].apply(lambda x: today + pd.Timedelta(hours=x.hour, minutes=x.minute, seconds=x.second))

st.title('Solar Plant Generation and Sensor Data Analysis')
st.sidebar.header('Select Visualization')

option = st.sidebar.selectbox('Select Data to Visualize:', ['Generation Data', 'Sensor Data'])

if option == 'Generation Data':
    st.header('Generation Data Analysis')

    plant_choice = st.radio('Choose Plant:', ['Plant 1', 'Plant 2'])

    gen_plot_type = st.selectbox('Select Graph Type:', ['Line Plot', 'Histogram', 'Scatter Plot', 'Correlation Matrix', 'Box Plot', 'Pair Plot'])
    
    if plant_choice == 'Plant 1':
        st.subheader('Plant 1 - Generation Data')
        
        if gen_plot_type == 'Scatter Plot':
            fig, ax = plt.subplots(2, 1, figsize=(10, 8))
            ax[0].plot(plant1_gendaily['TIME'], plant1_gendaily['DC_POWER'], '.', color='red')
            ax[0].set_title('DC Power for Plant 1')
            ax[0].set_xlabel('Time of Day')
            ax[0].set_ylabel('DC Power')
            
            ax[1].plot(plant1_gendaily['TIME'], plant1_gendaily['AC_POWER'], '.', color='blue')
            ax[1].set_title('AC Power for Plant 1')
            ax[1].set_xlabel('Time of Day')
            ax[1].set_ylabel('AC Power')
            st.pyplot(fig)

        elif gen_plot_type == 'Histogram':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(plant1_gendaily['DC_POWER'], bins=30, color='red', alpha=0.7, label='DC Power')
            ax.hist(plant1_gendaily['AC_POWER'], bins=30, color='blue', alpha=0.7, label='AC Power')
            ax.set_title('Histogram of Power Outputs for Plant 1')
            ax.set_xlabel('Power Output')
            ax.set_ylabel('Frequency')
            ax.legend()
            st.pyplot(fig)

        elif gen_plot_type == 'Line Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(plant1_gendaily['DC_POWER'], plant1_gendaily['AC_POWER'], color='purple', alpha=0.5)
            ax.set_title('Scatter Plot of DC vs AC Power for Plant 1')
            ax.set_xlabel('DC Power')
            ax.set_ylabel('AC Power')
            st.pyplot(fig)

        elif gen_plot_type == 'Correlation Matrix':
            corr = plant1_gendaily[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sbn.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            ax.set_title('Correlation Matrix for Plant 1')
            st.pyplot(fig)

        elif gen_plot_type == 'Box Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            sbn.boxplot(data=plant1_gendaily[['DC_POWER', 'AC_POWER']], ax=ax)
            ax.set_title('Box Plot of Power Outputs for Plant 1')
            ax.set_ylabel('Power Output')
            st.pyplot(fig)

        elif gen_plot_type == 'Pair Plot':
            fig = sbn.pairplot(plant1_gendaily[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']])
            st.pyplot(fig)

    elif plant_choice == 'Plant 2':
        st.subheader('Plant 2 - Generation Data')

        if gen_plot_type == 'Scatter Plot':
            fig, ax = plt.subplots(2, 1, figsize=(10, 8))
            ax[0].plot(plant2_gendaily['TIME'], plant2_gendaily['DC_POWER'], '.', color='red')
            ax[0].set_title('DC Power for Plant 2')
            ax[0].set_xlabel('Time of Day')
            ax[0].set_ylabel('DC Power')

            ax[1].plot(plant2_gendaily['TIME'], plant2_gendaily['AC_POWER'], '.', color='blue')
            ax[1].set_title('AC Power for Plant 2')
            ax[1].set_xlabel('Time of Day')
            ax[1].set_ylabel('AC Power')
            st.pyplot(fig)

        elif gen_plot_type == 'Histogram':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(plant2_gendaily['DC_POWER'], bins=30, color='red', alpha=0.7, label='DC Power')
            ax.hist(plant2_gendaily['AC_POWER'], bins=30, color='blue', alpha=0.7, label='AC Power')
            ax.set_title('Histogram of Power Outputs for Plant 2')
            ax.set_xlabel('Power Output')
            ax.set_ylabel('Frequency')
            ax.legend()
            st.pyplot(fig)

        elif gen_plot_type == 'Line Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(plant2_gendaily['DC_POWER'], plant2_gendaily['AC_POWER'], color='purple', alpha=0.5)
            ax.set_title('Scatter Plot of DC vs AC Power for Plant 2')
            ax.set_xlabel('DC Power')
            ax.set_ylabel('AC Power')
            st.pyplot(fig)

        elif gen_plot_type == 'Correlation Matrix':
            corr = plant2_gendaily[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sbn.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            ax.set_title('Correlation Matrix for Plant 2')
            st.pyplot(fig)

        elif gen_plot_type == 'Box Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            sbn.boxplot(data=plant2_gendaily[['DC_POWER', 'AC_POWER']], ax=ax)
            ax.set_title('Box Plot of Power Outputs for Plant 2')
            ax.set_ylabel('Power Output')
            st.pyplot(fig)

        elif gen_plot_type == 'Pair Plot':
            fig = sbn.pairplot(plant2_gendaily[['DC_POWER', 'AC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD']])
            st.pyplot(fig)

elif option == 'Sensor Data':
    st.header('Sensor Data Analysis')

    plant_choice = st.radio('Choose Plant:', ['Plant 1', 'Plant 2'])

    sens_plot_type = st.selectbox('Select Graph Type:', ['Line Plot', 'Histogram', 'Scatter Plot', 'Correlation Matrix', 'Box Plot', 'Pair Plot'])
    
    if plant_choice == 'Plant 1':
        st.subheader('Plant 1 - Sensor Data')

        if sens_plot_type == 'Line Plot':
            fig, ax = plt.subplots(3, 1, figsize=(10, 12))
            ax[0].plot(plant1_sens['DATE_TIME'], plant1_sens['IRRADIATION'], '.', color='green')
            ax[0].set_title('Irradiation for Plant 1')
            ax[0].set_xlabel('Time of Day')
            ax[0].set_ylabel('Irradiation')

            ax[1].plot(plant1_sens['DATE_TIME'], plant1_sens['MODULE_TEMPERATURE'], '.', color='orange')
            ax[1].set_title('Module Temperature for Plant 1')
            ax[1].set_xlabel('Time of Day')
            ax[1].set_ylabel('Module Temperature')

            ax[2].plot(plant1_sens['DATE_TIME'], plant1_sens['AMBIENT_TEMPERATURE'], '.', color='blue')
            ax[2].set_title('Ambient Temperature for Plant 1')
            ax[2].set_xlabel('Time of Day')
            ax[2].set_ylabel('Ambient Temperature')
            st.pyplot(fig)

        elif sens_plot_type == 'Histogram':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(plant1_sens['IRRADIATION'], bins=30, color='green', alpha=0.7, label='Irradiation')
            ax.hist(plant1_sens['MODULE_TEMPERATURE'], bins=30, color='orange', alpha=0.7, label='Module Temperature')
            ax.hist(plant1_sens['AMBIENT_TEMPERATURE'], bins=30, color='blue', alpha=0.7, label='Ambient Temperature')
            ax.set_title('Histogram of Sensor Readings for Plant 1')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()
            st.pyplot(fig)

        elif sens_plot_type == 'Scatter Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(plant1_sens['IRRADIATION'], plant1_sens['MODULE_TEMPERATURE'], color='purple', alpha=0.5)
            ax.set_title('Scatter Plot of Irradiation vs Module Temperature for Plant 1')
            ax.set_xlabel('Irradiation')
            ax.set_ylabel('Module Temperature')
            st.pyplot(fig)

        elif sens_plot_type == 'Correlation Matrix':
            corr = plant1_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sbn.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            ax.set_title('Correlation Matrix for Plant 1 Sensor Data')
            st.pyplot(fig)

        elif sens_plot_type == 'Box Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            sbn.boxplot(data=plant1_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']], ax=ax)
            ax.set_title('Box Plot of Sensor Readings for Plant 1')
            ax.set_ylabel('Value')
            st.pyplot(fig)

        elif sens_plot_type == 'Pair Plot':
            fig = sbn.pairplot(plant1_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']])
            st.pyplot(fig)

    elif plant_choice == 'Plant 2':
        st.subheader('Plant 2 - Sensor Data')

        if sens_plot_type == 'Line Plot':
            fig, ax = plt.subplots(3, 1, figsize=(10, 12))
            ax[0].plot(plant2_sens['DATE_TIME'], plant2_sens['IRRADIATION'], '.', color='green')
            ax[0].set_title('Irradiation for Plant 2')
            ax[0].set_xlabel('Time of Day')
            ax[0].set_ylabel('Irradiation')

            ax[1].plot(plant2_sens['DATE_TIME'], plant2_sens['MODULE_TEMPERATURE'], '.', color='orange')
            ax[1].set_title('Module Temperature for Plant 2')
            ax[1].set_xlabel('Time of Day')
            ax[1].set_ylabel('Module Temperature')

            ax[2].plot(plant2_sens['DATE_TIME'], plant2_sens['AMBIENT_TEMPERATURE'], '.', color='blue')
            ax[2].set_title('Ambient Temperature for Plant 2')
            ax[2].set_xlabel('Time of Day')
            ax[2].set_ylabel('Ambient Temperature')
            st.pyplot(fig)

        elif sens_plot_type == 'Histogram':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(plant2_sens['IRRADIATION'], bins=30, color='green', alpha=0.7, label='Irradiation')
            ax.hist(plant2_sens['MODULE_TEMPERATURE'], bins=30, color='orange', alpha=0.7, label='Module Temperature')
            ax.hist(plant2_sens['AMBIENT_TEMPERATURE'], bins=30, color='blue', alpha=0.7, label='Ambient Temperature')
            ax.set_title('Histogram of Sensor Readings for Plant 2')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()
            st.pyplot(fig)

        elif sens_plot_type == 'Scatter Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(plant2_sens['IRRADIATION'], plant2_sens['MODULE_TEMPERATURE'], color='purple', alpha=0.5)
            ax.set_title('Scatter Plot of Irradiation vs Module Temperature for Plant 2')
            ax.set_xlabel('Irradiation')
            ax.set_ylabel('Module Temperature')
            st.pyplot(fig)

        elif sens_plot_type == 'Correlation Matrix':
            corr = plant2_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sbn.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            ax.set_title('Correlation Matrix for Plant 2 Sensor Data')
            st.pyplot(fig)

        elif sens_plot_type == 'Box Plot':
            fig, ax = plt.subplots(figsize=(10, 6))
            sbn.boxplot(data=plant2_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']], ax=ax)
            ax.set_title('Box Plot of Sensor Readings for Plant 2')
            ax.set_ylabel('Value')
            st.pyplot(fig)

        elif sens_plot_type == 'Pair Plot':
            fig = sbn.pairplot(plant2_sens[['IRRADIATION', 'MODULE_TEMPERATURE', 'AMBIENT_TEMPERATURE']])
            st.pyplot(fig)
