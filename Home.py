import streamlit as st
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder
from prophet import Prophet
import numpy as np

faker = Faker()

def generate_data(start_date, end_date):
    data = []
    for _ in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=_)
        data.append({
            "score": np.random.randint(0, 101),  # New field: score ranging from 0 to 100
            "date": date,
            "user_id": faker.unique.random_int(min=1, max=1000),
            "name": faker.name(),
            "email": faker.email(),
            "gender": faker.random_element(elements=('Male', 'Female')),
            "birthday": faker.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=70),
            "location": faker.address(),
            "page_id": faker.unique.random_int(min=1, max=100),
            "page_name": faker.company(),
            "about": faker.text(max_nb_chars=200),
            "category": faker.random_element(elements=('Entertainment', 'Business', 'Community')),
            "fan_count": faker.random_int(min=100, max=10000),
            "posts": faker.random_int(min=0, max=5),
            "friends_count": faker.random_int(min=50, max=500),
            "usage_time": faker.random_int(min=10, max=300),  # in minutes
            "posting_time": faker.random_int(min=0, max=60),  # in minutes
            "posting_count": faker.random_int(min=0, max=10),
            "engagement_time": faker.random_int(min=0, max=60),  # in minutes
            "reaction_pattern": faker.random_element(elements=('Positive', 'Negative', 'Neutral')),
            "reaction_count": faker.random_int(min=0, max=100),
            "sharing_count": faker.random_int(min=0, max=20),
            "event_time": faker.random_int(min=0, max=60),  # in minutes
            "reaction_event_pattern": faker.random_element(elements=('Will Go', 'Interested', 'Not Interested')),
            "reaction_event_count": faker.random_int(min=0, max=100),
            "physical_step_count": faker.random_int(min=0, max=10000),
            "physical_training": faker.random_element(elements=('Yes', 'No')),
            "messenger_chats_count": faker.random_int(min=0, max=50),
            "messenger_time_screen": faker.random_int(min=0, max=300),  # in minutes
            "whatsapp_chats_count": faker.random_int(min=0, max=50),
            "whatsapp_time_screen": faker.random_int(min=0, max=300),  # in minutes
            "instagram_friends_count": faker.random_int(min=50, max=500),
            "instagram_time": faker.random_int(min=0, max=300),  # in minutes
            "instagram_uploaded_photos": faker.random_int(min=0, max=20),
            "spotify_playlists_count": faker.random_int(min=0, max=50),
            "spotify_liked_tracks": faker.random_int(min=0, max=200),
            "youtube_playlists_count": faker.random_int(min=0, max=50),
            "youtube_liked_tracks": faker.random_int(min=0, max=200),
            "call_frequency": faker.random_int(min=0, max=30),
            "call_length": faker.random_int(min=0, max=120),  # in minutes
            "calendar_entries": faker.random_int(min=0, max=10),
            "tasks_per_day": faker.random_int(min=0, max=10),
            "browser_time": faker.random_int(min=0, max=300),  # in minutes
            "app_usage_time": faker.random_int(min=0, max=300),  # in minutes
            "conversation_length": faker.random_int(min=0, max=500)  # number of words
        })
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])  # Ensure the 'date' column is datetime type
    return df

st.title("Mentastic Score")

st.markdown("""
## What is Mentastic Score?

The Mentastic Score is a comprehensive well-being metric that combines multiple data sources to evaluate and predict a user's mental health state. The score ranges from 0-100, where:
- 0-30: Indicates potential concerns requiring immediate attention
- 31-60: Moderate well-being with room for improvement
- 61-100: Good to excellent mental health state

### Data Sources
The score incorporates data from:
1. **Social Media Activity**: Engagement patterns, posting frequency, and sentiment
2. **Physical Activity**: Step counts and exercise routines
3. **Communication Patterns**: Messaging frequency and call durations
4. **Digital Wellness**: Screen time and app usage
5. **Daily Routines**: Calendar entries and task completion

### Model Purpose
The predictive model serves to:
- Identify early warning signs of mental health challenges
- Provide personalized recommendations
- Track intervention effectiveness
- Enable proactive mental health support

### Technical Implementation
We use Facebook Prophet for time series forecasting due to its ability to handle:
- Multiple seasonality patterns
- Missing data
- Outliers
- Holiday effects
""")

st.markdown("""
## Data Science Interview Questions

### 1. Feature Engineering & Selection
- How would you handle the cyclical nature of social media usage patterns?
- Which techniques would you use to identify the most important features?
- How would you incorporate temporal features like time of day or day of week?

### 2. Model Evaluation & Selection
- What metrics would be most appropriate for evaluating the model's performance?
- How would you handle class imbalance in mental health scoring?
- What alternative models would you consider besides Prophet?

### 3. Time Series Specific
- How would you detect and handle seasonality at different scales (daily, weekly, monthly)?
- What methods would you use to detect anomalies in the score?
- How would you incorporate external factors like holidays or global events?

### 4. Feature Importance Analysis
- How would you measure the contribution of each data source to the final score?
- What techniques would you use to ensure feature interpretability?
- How would you handle feature interactions?

### 5. Model Deployment & Monitoring
- How would you ensure the model remains accurate over time?
- What drift detection methods would you implement?
- How would you handle real-time updates to the score?
""")

st.sidebar.header("Data Generation Settings")
start_date = st.sidebar.date_input("Start date", datetime(2024, 7, 1))
end_date = st.sidebar.date_input("End date", datetime(2024, 7, 31))

if st.sidebar.button("Generate Data"):
    st.session_state['df'] = generate_data(start_date, end_date)

    # Encode categorical variables
    st.session_state['df']['gender_encoded'] = LabelEncoder().fit_transform(st.session_state['df']['gender'])
    st.session_state['df']['category_encoded'] = LabelEncoder().fit_transform(st.session_state['df']['category'])
    st.session_state['df']['reaction_pattern_encoded'] = LabelEncoder().fit_transform(st.session_state['df']['reaction_pattern'])
    st.session_state['df']['reaction_event_pattern_encoded'] = LabelEncoder().fit_transform(st.session_state['df']['reaction_event_pattern'])
    st.session_state['df']['physical_training_encoded'] = LabelEncoder().fit_transform(st.session_state['df']['physical_training'])

if 'df' in st.session_state:
    st.write("Generated Data:", st.session_state['df'].head())

    st.markdown("""
    ### Model Analysis
    Select features to include in the prediction model. Consider:
    - Feature correlation with the target score
    - Temporal relevance
    - Data availability and reliability
    """)

    # Select regressors
    available_regressors = ['gender_encoded', 'category_encoded', 'fan_count', 'friends_count', 'usage_time', 'posting_time', 
                            'posting_count', 'engagement_time', 'reaction_pattern_encoded', 'reaction_count', 'sharing_count', 
                            'event_time', 'reaction_event_pattern_encoded', 'reaction_event_count', 'physical_step_count', 
                            'physical_training_encoded', 'messenger_chats_count', 'messenger_time_screen', 'whatsapp_chats_count', 
                            'whatsapp_time_screen', 'instagram_friends_count', 'instagram_time', 'instagram_uploaded_photos', 
                            'spotify_playlists_count', 'spotify_liked_tracks', 'youtube_playlists_count', 'youtube_liked_tracks', 
                            'call_frequency', 'call_length', 'calendar_entries', 'tasks_per_day', 'browser_time', 'app_usage_time', 
                            'conversation_length', 'posts']
    selected_regressors = st.multiselect("Select Regressors:", available_regressors, default=available_regressors[:5])

    if st.button("Rerun with Selected Regressors"):
        prophet_df = st.session_state['df'][['date', 'score'] + selected_regressors].rename(columns={'date': 'ds', 'score': 'y'})
        prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])  # Ensure 'ds' is datetime type

        model = Prophet(daily_seasonality=True)
        for regressor in selected_regressors:
            model.add_regressor(regressor)

        model.fit(prophet_df)

        future = model.make_future_dataframe(periods=30)
        future['ds'] = pd.to_datetime(future['ds'])  # Ensure 'ds' is datetime type
        future = future.merge(prophet_df.drop('y', axis=1), on='ds', how='left').fillna(method='ffill')

        forecast = model.predict(future)

        st.subheader("Mentastic Score Forecast")
        fig1 = model.plot(forecast)
        # Customizing the plot
        ax = fig1.gca()  # Get the current Axes instance on the current figure
        ax.set_ylabel('Mentastic Score')  # Set the y-axis label

        st.pyplot(fig1)  # Display the customized plot in Streamlit

        st.subheader("Forecast Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

    if st.button("Analyze Feature Importance"):
        if len(selected_regressors) > 0:
            importance_df = pd.DataFrame({
                'Feature': selected_regressors,
                'Importance': np.random.uniform(0, 1, len(selected_regressors))  # Placeholder for actual importance
            })
            importance_df = importance_df.sort_values('Importance', ascending=False)
            
            st.subheader("Feature Importance Analysis")
            st.bar_chart(importance_df.set_index('Feature'))
            
            st.markdown("""
            ### Interpretation Guidelines
            - Consider both statistical significance and practical importance
            - Look for seasonal patterns in important features
            - Evaluate feature stability over time
            """)