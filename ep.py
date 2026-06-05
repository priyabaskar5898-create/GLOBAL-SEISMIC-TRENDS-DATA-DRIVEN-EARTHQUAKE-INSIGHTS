import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:priya@localhost:3306/eq_database')


st.subheader("Welcome to the Global Seismic Trends dashboard!")
st.title("Global Seismic Trends: Data-Driven Earthquake Insights🌏")
st.subheader("Explore Earthquake Data with SQL Queries ✨")
st.divider()
st.write("***Select any problem statement (1 - 30) and get the corresponding SQL queries to analyze earthquake data.***")

sql_queries = {

"1.Top 10 strongest earthquakes (mag)." : """
    SELECT id, date, country, mag 
    FROM eq_database.earthquake_table 
    ORDER BY mag DESC LIMIT 10""",

"2. Top 10 deepest earthquakes (depth_km)." : """ 
    SELECT id, date, country, depth_km 
    FROM eq_database.earthquake_table
    ORDER BY depth_km DESC LIMIT 10""",

"3. Shallow earthquakes < 50 km and mag > 7.5." :"""
    SELECT id, time, country, mag, depth_km 
    FROM eq_database.earthquake_table 
    WHERE depth_km < 50 and mag > 7.5 
    ORDER BY depth_km""",

"5. Average magnitude per magnitude type (magType)." : """ 
    SELECT magType, avg(mag) as avg_mag 
    FROM eq_database.earthquake_table
    GROUP BY magType
    ORDER BY avg(mag) DESC""",

"6. Year with most earthquakes." : """
    SELECT year, count(year) as earthquake_count 
    FROM eq_database.earthquake_table 
    GROUP BY year 
    ORDER BY earthquake_count DESC 
    LIMIT 1""",

"7. Month with highest number of earthquakes." : """
    SELECT month,month_name, count(month) as earthquake_count
    FROM eq_database.earthquake_table 
    GROUP BY month, month_name
    ORDER BY earthquake_count DESC 
    LIMIT 1""",

"8. Day of week with most earthquakes." : """
    SELECT day_of_week, day_name, count(day_of_week) as earthquake_count 
    FROM eq_database.earthquake_table 
    GROUP BY day_of_week, day_name
    ORDER BY earthquake_count DESC
    LIMIT 1""",

"9. Count of earthquakes per hour of day.": """
    SELECT hour,count(hour) as earthquake_count 
    FROM eq_database.earthquake_table 
    GROUP BY hour 
    ORDER BY hour ASC""",

"10.Most active reporting network (net).": """
    SELECT net, count(net) as active_net_count 
    FROM eq_database.earthquake_table 
    GROUP BY net 
    ORDER BY active_net_count DESC 
    LIMIT 1""",

"11.Top 5 places with highest casualties." : """
    SELECT place, max(felt) as highest_casualities 
    FROM eq_database.earthquake_table 
    GROUP BY place 
    ORDER BY highest_casualities DESC
    LIMIT 5""",

"13.Average economic loss by alert level.": """
    SELECT alert, avg(cdi) as avg_eco_loss 
    FROM eq_database.earthquake_table 
    GROUP BY alert 
    ORDER BY avg_eco_loss DESC""",

"14.Count of reviewed vs automatic earthquakes (status)." : """
    SELECT status, count(status) as earthquake_count
    FROM eq_database.earthquake_table 
    GROUP BY status 
    ORDER BY earthquake_count DESC""",

"15.Count by earthquake type (type)." : """
    SELECT type, count(type) as earthquake_type 
    FROM eq_database.earthquake_table 
    GROUP BY type 
    ORDER BY earthquake_type DESC""",

"16.Number of earthquakes by data type (types)." : """
    SELECT types, count(types) AS eq_count 
    FROM eq_database.earthquake_table 
    GROUP BY types
    ORDER BY eq_count DESC""",

"18.Events with high station coverage (nst > threshold)." : """
    SELECT id,date, place, nst 
    FROM eq_database.earthquake_table 
    WHERE nst > 50
    ORDER BY nst DESC""",

"19.Number of tsunamis triggered per year." : """
    SELECT year, COUNT(year) AS tsunami_count 
    FROM eq_database.earthquake_table 
    WHERE tsunami = 1 
    GROUP BY year 
    ORDER BY year ASC""",

"20.Count earthquakes by alert levels (red, orange, etc.)." : """
    SELECT alert, COUNT(alert) AS earthquake_count 
    FROM eq_database.earthquake_table
    GROUP BY alert 
    ORDER BY earthquake_count DESC""",

"21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years." : """
    SELECT country, avg(mag) as average_magnitude 
    FROM eq_database.earthquake_table 
    GROUP BY country 
    ORDER BY average_magnitude DESC 
    limit 5""",

"22.Find countries that have experienced both shallow and deep earthquakes within the same month." : """
    SELECT country, year, month
    FROM eq_database.earthquake_table 
    GROUP BY country, year, month 
    HAVING SUM(depth_km <= 70) > 0 
    AND SUM(depth_km > 300) > 0""",

"23.Compute the year-over-year growth rate in the total number of earthquakes globally." : """
    SELECT year, current_year_count, previous_year_count,
    ROUND(((current_year_count - previous_year_count) / previous_year_count) * 100, 2) AS year_over_year_change
    FROM (SELECT year, COUNT(*) AS current_year_count, LAG(COUNT(*)) OVER (ORDER BY year) AS previous_year_count 
    FROM eq_database.earthquake_table 
    GROUP BY year) AS yearly_data 
    ORDER BY year DESC""",

"24.List the 3 most seismically active regions by combining both frequency and average magnitude." : """
    SELECT country,COUNT(country) AS earthquake_count, AVG(mag) AS avg_magnitude
    FROM eq_database.earthquake_table 
    GROUP BY country 
    ORDER BY COUNT(country) DESC LIMIT 3""",

"25.For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator." : """
    SELECT country,AVG(depth_km) AS avg_depth 
    FROM eq_database.earthquake_table
    WHERE latitude BETWEEN -5 AND 5 
    GROUP BY country 
    ORDER BY avg_depth DESC""",

"26.Identify countries having the highest ratio of shallow to deep earthquakes." : """
    SELECT country, SUM(depth_km < 70) AS shallow_eq,
    SUM(depth_km > 300) AS deep_eq,
    ROUND(SUM(CASE WHEN depth_km <= 70 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END), 0), 2) 
    AS shallow_to_deep_ratio 
    FROM eq_database.earthquake_table 
    GROUP BY country 
    ORDER BY shallow_to_deep_ratio DESC LIMIT 20""",

"27. Find the average magnitude difference between earthquakes with tsunami alerts and those without." : """
    SELECT 
    (SELECT AVG(mag) FROM eq_database.earthquake_table WHERE tsunami = 1) AS tsunami_avg,
    (SELECT AVG(mag) FROM eq_database.earthquake_table WHERE tsunami = 0) AS no_tsunami_avg,
    (SELECT AVG(mag) FROM eq_database.earthquake_table WHERE tsunami = 1) - (SELECT AVG(mag) FROM eq_database.earthquake_table WHERE tsunami = 0) 
    AS diff""",

"28.Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)." : """
    SELECT id,date, place, gap, rms 
    FROM eq_database.earthquake_table 
    ORDER BY gap DESC, rms ASC
    LIMIT 25""",

"30.Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)." : """
    SELECT country, count(country) as deep_earthquake_count, max(depth_km) AS deep_focus_earthquake
    FROM eq_database.earthquake_table
    WHERE depth_km > 300 
    GROUP BY country 
    ORDER BY deep_earthquake_count DESC""",
}
question_option = list(sql_queries.keys())

selected_question = st.selectbox("select a question to analyse:", question_option)


query = sql_queries[selected_question]

if st.button("Get SQL Query", type="primary"):
        result = st.code(sql_queries[selected_question], language="sql")
        st.divider()
        df = pd.read_sql(query,engine)
        st.dataframe(df, use_container_width=True)

st.sidebar.subheader("About this Dashboard")

st.sidebar.markdown("""This dashboard provides insights into global seismic trends using earthquake data.
Explore various SQL queries to analyze earthquake patterns, magnitudes, depths, and more.""")

st.sidebar.subheader("Data Source")

st.sidebar.markdown("""The earthquake data is sourced from the USGS Earthquake Catalog, 
which provides comprehensive information on seismic events worldwide.""")   