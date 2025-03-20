import streamlit as st
import pickle
import pandas as pd

teams = sorted(['Royal Challengers Bangalore', 'Punjab Kings', 'Delhi Capitals',
       'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Sunrisers Hyderabad', 'Chennai Super Kings'])

cities = sorted(['Dubai', 'Chennai', 'Abu Dhabi', 'Mumbai', 'Indore', 'Bangalore',
       'Jaipur', 'Port Elizabeth', 'Cuttack', 'Delhi', 'Navi Mumbai',
       'Kolkata', 'Dharamsala', 'Ranchi', 'Bengaluru', 'Hyderabad',
       'Durban', 'Ahmedabad', 'Chandigarh', 'Nagpur', 'Kimberley', 'Pune',
       'Centurion', 'Mohali', 'Sharjah', 'Cape Town', 'East London',
       'Visakhapatnam', 'Johannesburg', 'Bloemfontein', 'Raipur',
       'Guwahati'])

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', teams)
with col2:
    bowling_team = st.selectbox('Select the bowling team', teams)

city = st.selectbox('Select host city', cities)

target = st.number_input('Target', step=1)

col3, col4= st.columns(2)

with col3:
    runs = st.number_input('Runs', step=1)
    overs = st.number_input('Overs', step=1)
with col4:
    wickets = st.number_input('Wickets', step=1)
    balls = st.number_input('Balls', step=1)    

st.text('Eg: To choose 9.4 overs, select Overs = 9 and Balls = 4')

if st.button('Predict Probability'):
    runs_left = target - runs
    balls_left = 120 - overs*6 - balls
    wickets_left = 10 - wickets
    crr = runs/(overs + balls/6)
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'crr': [crr],
        'rrr': [rrr]
    }
    )

    result = pipe.predict_proba(input_df)
    # st.text(result)
    col5, col6 = st.columns(2)
    with col5:
        st.subheader(batting_team +': ')
        st.subheader(str(round(result[0][1]*10000)/100) + '%')
    with col6:
        st.subheader(bowling_team +': ')
        st.subheader(str(round(result[0][0]*10000)/100) + '%')
    
    

