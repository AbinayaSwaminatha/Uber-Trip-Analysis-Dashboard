import pandas as pd
import plotly.express as px
import streamlit as st
# Load Data
df = pd.read_csv(r"C:\Users\Abinaya\Downloads\ride_bookings.csv")
df.columns = df.columns.str.strip().str.replace(' ', '_')
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df.dropna(subset=['Datetime'], inplace=True)
# Feature Engineering
df['Hour'] = df['Datetime'].dt.hour
df['Day'] = df['Datetime'].dt.day_name()
df['Month'] = df['Datetime'].dt.month_name()
def classify_status(status):
    if status == 'Completed':
        return 'Completed'
    elif 'Cancel' in str(status) or 'No Driver' in str(status):
        return 'Cancelled'
    else:
        return 'Incomplete'

df['Trip_Status'] = df['Booking_Status'].apply(classify_status)
#Sidebar Filters
st.sidebar.header("Filter Trips")
status_filter = st.sidebar.multiselect("Trip Status", df['Trip_Status'].unique(), default=df['Trip_Status'].unique())
vehicle_filter = st.sidebar.multiselect("Vehicle Type", df['Vehicle_Type'].dropna().unique(), default=df['Vehicle_Type'].dropna().unique())
filtered_df = df[(df['Trip_Status'].isin(status_filter)) & (df['Vehicle_Type'].isin(vehicle_filter))]
#Dashboard Title
st.title("🚖 Uber Trip Analysis Dashboard")
#Trip Status Distribution
st.subheader("Trip Status Overview")
status_fig = px.histogram(filtered_df, x='Trip_Status', color='Trip_Status', title='Trip Status Count')
st.plotly_chart(status_fig)
#Top Pickup Locations
st.subheader("Top Pickup Locations")
top_pickups = filtered_df['Pickup_Location'].value_counts().nlargest(10).reset_index()
top_pickups.columns = ['Pickup Location', 'Count']
pickup_fig = px.bar(top_pickups, x='Count', y='Pickup Location', orientation='h', title='Top 10 Pickup Locations')
st.plotly_chart(pickup_fig)
#Payment Method Breakdown
st.subheader("Payment Method Distribution")
payment_fig = px.pie(filtered_df, names='Payment_Method', title='Payment Methods')
st.plotly_chart(payment_fig)
#Ride Distance Distribution
st.subheader("Ride Distance Distribution")
distance_fig = px.histogram(filtered_df, x='Ride_Distance', nbins=30, title='Ride Distance Histogram')
st.plotly_chart(distance_fig)
#Ratings
st.subheader("Driver Ratings Distribution")
rating_fig = px.histogram(filtered_df, x='Driver_Ratings', nbins=10, title='Driver Ratings')
st.plotly_chart(rating_fig)