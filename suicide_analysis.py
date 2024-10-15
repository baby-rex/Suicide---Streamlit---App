import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_csv('master.csv')

# Set page configuration for full width
st.set_page_config(page_title="Suicide Data Analysis", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f5;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #333;
        font-size: 3em; /* Increased size for better visibility */
        text-align: center;
        font-family: 'Arial', sans-serif; /* Changed font */
    }
    h2 {
        color: #007bff;
        margin-top: 20px;
        font-family: 'Arial', sans-serif; /* Changed font */
    }
    .info-box {
        background-color: #ffffff;
        padding: 10px; /* Reduced padding for smaller boxes */
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px; /* Adjusted spacing between boxes */
        color: #333; /* Set text color to dark */
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for permanent information display
st.sidebar.header("Overview of the Application")
st.sidebar.markdown("""
- **Unique Countries**: List of countries analyzed.
- **Year Range**: Minimum and maximum years in the dataset.
- **Summary Statistics**: Overview of the dataset.
- **Missing Values**: Count of missing values in each column.
- **Shape Information**: Number of rows and columns in the dataset.
- **Top & Lowest Countries**: Countries with the most and least suicides.
- **Visualizations**: Various plots depicting data insights.
""")

# Streamlit App Title
st.title("Suicide Data Analysis")

# Sidebar for country selection
unique_countries = df['country'].unique()
selected_country = st.sidebar.selectbox("Choose a country:", unique_countries)

# Year range
min_year = df['year'].min()
max_year = df['year'].max()
st.subheader("Year Range")
st.markdown(f"<div class='info-box'>Min Year: {min_year}<br>Max Year: {max_year}<br></div>", unsafe_allow_html=True)

# Data info
st.subheader("Data Information")
data_info = df.info()  # Store info in a variable for display
st.markdown("<div class='info-box'>" + str(data_info) + "</div>", unsafe_allow_html=True)

# Clean Data
df_clean = df.dropna(subset=['HDI for year'])
summary_stats = df.describe()
st.subheader("Summary Statistics")
summary_stats_str = "<div class='info-box'>"
for stat_name, value in summary_stats.items():
    summary_stats_str += f"<strong>{stat_name:}: </strong>{value}<br>"
summary_stats_str += "</div>"
st.markdown(summary_stats_str, unsafe_allow_html=True)

# Missing values
missing_values = df.isnull().sum()
st.subheader("Missing Values in Each Column")
missing_values_str = "<div class='info-box '>"
for column, count in missing_values.items():
    missing_values_str += f"<strong>{column}: </strong>{count}<br>"
missing_values_str += "</div>"
st.markdown(missing_values_str, unsafe_allow_html=True)

# Shape info
shape_info = {
    'Number of Rows': len(df),
    'Number of Columns': len(df.columns),
    'Column Names': df.columns.tolist()
}

# Print shape information in a box format
st.subheader("Shape Information")
shape_info_str = "<div class='info-box'>"
for key, value in shape_info.items():
    shape_info_str += f"<strong>{key}: </strong>{value}<br>"
shape_info_str += "</div>"
st.markdown(shape_info_str, unsafe_allow_html=True)

# Top 5 countries with most suicides
top_countries = df_clean.groupby('country')['suicides_no'].sum().sort_values(ascending=False).head(5)
st.subheader("Top 5 Countries with Most Suicides")
top_countries_str = "<div class='info-box'>"
for country, count in top_countries.items():
    top_countries_str += f"{country}: {count}<br>"
top_countries_str += "</div>"
st.markdown(top_countries_str, unsafe_allow_html=True)

# Average suicides per 100k population
mean_suicides_per_100k = df_clean['suicides/100k pop'].mean()
st.markdown(f"<div class='info-box'>Average suicides per 100k population:{mean_suicides_per_100k:.2f}</div>", unsafe_allow_html=True)

# Lowest countries suicides
lowest_countries_suicides = df.groupby('country')['suicides_no'].sum().nsmallest(10)
st.subheader("Countries with Lowest Total Suicides")
lowest_countries_str = "<div class='info-box'>"
for country, count in lowest_countries_suicides.items():
    lowest_countries_str += f"{country}: {count}<br>"
lowest_countries_str += "</div>"
st.markdown(lowest_countries_str, unsafe_allow_html=True)

# Suicides by sex
suicides_by_sex = df.groupby('sex')['suicides_no'].sum().reset_index()

# Interactive donut plot
fig = px.pie(
    suicides_by_sex,
    names='sex',
    values='suicides_no',
    title='Distribution of Suicides by Sex',
    hole=0.4,
    color_discrete_sequence=['#FF69B4', '#000080']
)
st.plotly_chart(fig)

# Distribution of Suicides by Gender
g = sns.FacetGrid(df, col="sex", hue="sex", palette={'female': '#FF69B4', 'male': '#000080'}, height=6, aspect=1.5)
g.map(sns.histplot, "suicides_no", bins=30, kde=True, alpha=0.5)
g.set_titles(col_template="{col_name} Gender")
g.set_axis_labels("Number of Suicides", "Frequency")
plt.subplots_adjust(top=0.9)
g.fig.suptitle("Distribution of Suicide Rates by Gender", fontsize=20, fontweight='bold', color='darkblue')
st.pyplot(g.fig)

# Top countries with highest total suicides
top_countries_suicides = df.groupby('country')['suicides_no'].sum().nlargest(10).reset_index()
fig = px.bar(top_countries_suicides, x='country', y='suicides_no', title='Top Countries with Highest Total Suicidal Cases')
fig.update_traces(marker_color='red', marker_line_color='black', marker_line_width=1)
st.plotly_chart(fig)

# Lowest countries suicides
lowest_countries_suicides = df.groupby('country')['suicides_no'].sum().nsmallest(10).reset_index()
fig = px.bar(lowest_countries_suicides, x='country', y='suicides_no', title='Countries with Lowest Total Suicidal Cases')
fig.update_traces(marker_color='lightcoral', marker_line_color='black', marker_line_width=1)
st.plotly_chart(fig)

# Average suicide rate by country
avg_suicide_rate_by_country = df.groupby('country')['suicides/100k pop'].mean().reset_index()
fig = px.bar(avg_suicide_rate_by_country, x='country', y='suicides/100k pop', title='Average Suicide Rate by Country')
fig.update_traces(marker_color='red', marker_line_color='black', marker_line_width=1)
st.plotly_chart(fig)

# Suicides by age
suicides_by_age = df.groupby('age')['suicides_no'].sum().reset_index()
fig = px.bar(suicides_by_age, x='suicides_no', y='age', orientation='h', title='Distribution of Suicidal Cases by Age Group')
fig.update_traces(marker_color='skyblue', marker_line_color='navy', marker_line_width=2)
st.plotly_chart(fig)

# Area plot for suicides by age group
groupedby_age = df.groupby('age')['suicides_no'].sum()
fig, ax = plt.subplots(figsize=(8, 5))
groupedby_age.plot.area(ax=ax, color='#1d3557', alpha=0.7)
ax.set_xlabel('Age Group', fontsize=15, fontweight='bold')
ax.set_ylabel('Total Number of Suicidal Cases', fontsize=15, fontweight='bold')
ax.set_title('Suicide Rates by Age Group')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xticks(rotation=45, ha='right')
plt.style.use('ggplot')
st.pyplot(fig)

# Suicides by generation and gender
plt.figure(figsize=(10, 6))
sns.barplot(data=df_clean, x="generation", y="suicides_no", hue="sex", estimator=np.sum)
plt.title("Total Suicidal Cases by Generation and Gender")
plt.ylabel("Total Suicidal Cases")
plt.xlabel("Generation")
plt.xticks(rotation=45)
st.pyplot()

# Heatmap for suicides by generation and gender
heatmap_data = df_clean.pivot_table(values='suicides_no', index='generation', columns='sex', aggfunc=np.sum)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5, cbar_kws={'label': 'Total Suicidal Cases'})
plt.title("Heatmap of Total Suicidal Cases by Generation and Gender")
plt.ylabel("Generation")
plt.xlabel("Gender")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
st.pyplot()

# Time series for the selected country from sidebar
selected_country_data = df[df['country'] == selected_country]
if selected_country_data.empty:
    st.write(f"No data available for {selected_country}.")
else:
    country_data = selected_country_data.groupby(['year'])[['suicides_no']].sum().reset_index()
    fig = px.line(country_data, x='year', y='suicides_no',
                  title=f'Suicide Trends Over Time in {selected_country}', line_shape='linear')
    fig.update_traces(line=dict(color='red'))
    st.plotly_chart(fig)

# Correlation heatmap of numerical features
numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
correlation_matrix = df[numerical_columns].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, cbar_kws={"shrink": .8})
plt.title('Correlation Heatmap of Numerical Features')
st.pyplot()


