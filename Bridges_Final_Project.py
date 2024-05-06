'''
Created on May 4, 2024

@author: hwebb

Name: Hayden Webber
CS230: Section 2
Data: Streamlit, pandas, matplotlib.pyplot, seaborn, streamlit_folium
Description: 
An anaylysis of the Georgian Bridges using summary statistics, bar plots, scatterplots, and maps in order to determine the effect of age on condition, location, and types of bridges

'''
#C:\Users\hwebb\anaconda3\Scripts\streamlit.exe run Bridges_Final_Project.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

file_path = "Georgia_Bridges_10000_sample.csv"
data = load_data(file_path)

# Data Analysis Functions
def sort_data(data, columns, ascending=True):
    sorted_data = data.sort_values(by=columns, ascending=ascending)
    return sorted_data

def filter_data(data, condition):
    filtered_data = data[data[condition]]
    return filtered_data

def compute_summary_statistics(data):
    summary_stats = data.describe()
    return summary_stats

st.title("Georgia Bridges Data Analysis")

st.sidebar.title("Choose Column")
sort_columns = st.sidebar.multiselect("Select columns to sort by:", data.columns)
ascending = st.sidebar.checkbox("Sort in ascending order", True)

# Data Analysis
sorted_data = sort_data(data, sort_columns, ascending)
summary_stats = compute_summary_statistics(sorted_data)

# Show Summary Statistics
st.write("## Summary Statistics")
st.write(summary_stats)

# Visualizations
st.write("## Visualizations")

st.write("### Bar Chart of Bridge Types")
bridge_type_counts = sorted_data['43B - Main Span Design'].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=bridge_type_counts.index, y=bridge_type_counts.values, ax=ax)
ax.set_xlabel('Bridge Type')
ax.set_ylabel('Count')
ax.set_title('Bridge Types Distribution')
plt.xticks(rotation=45)
st.pyplot(fig)


st.write("### Scatter Plot of Bridge Age vs. Condition Rating")

# Create a figure and axes using plt.subplots()
fig, ax = plt.subplots(figsize=(10, 6))

# Use the axes for the scatterplot
sns.scatterplot(x='Bridge Age (yr)', y='CAT10 - Bridge Condition', data=sorted_data, ax=ax)

ax.set_xlabel('Bridge Age')
ax.set_ylabel('Condition Rating')
ax.set_title('Bridge Age vs. Condition Rating')

# Pass the figure to st.pyplot()
st.pyplot(fig)

median_longitude = data['17 - Longitude (decimal)'].median()
median_latitude = data['16 - Latitude (decimal)'].median()
                              
m = folium.Map(location=[median_latitude, median_longitude])

for idx, row in data[data['3 - County Name']=='Chatham County'].iterrows():
    folium.Marker([row['16 - Latitude (decimal)'], row['17 - Longitude (decimal)']]).add_to(m)


folium_static(m)