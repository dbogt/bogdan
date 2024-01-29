import streamlit as st

st.sidebar.markdown("# Main page 🎈")

text = """
### Hi there 👋

![](https://komarev.com/ghpvc/?username=your-github-username&color=blue)

- :computer: Connect with me on **[LinkedIn](https://www.linkedin.com/in/tudosebogdan/)**
- :newspaper: Read some of my Python articles on **[Medium](https://medium.com/@bogdan-tudose)**
- :office: I'm currently Co-Head of Data Science and instructor for **[The Marque Group](https://marqueegroup.ca/)** and **[Training The Street](https://trainingthestreet.com/bogdan-tudose/)**
- :school: Check out some of the programming courses I teach:
  - [Python 1: Core Data Analysis](https://marqueegroup.ca/course/python-1-core-data-analysis/)  
  - [Python 2: Visualization and Analysis](https://marqueegroup.ca/course/python-2-visualization-and-analysis/)
  - [Python 3: Web Scraping and Machine Learning](https://marqueegroup.ca/course/python-3-web-scraping-and-machine-learning/)
  - [VBA for Finance Professionals](https://marqueegroup.ca/course/vba-for-finance-professionals/)
- Python Resources: https://github.com/dbogt/pythonResources

Some Python projects to try out:

- :computer:[Financial Dashboards with Python and ChatGPT](https://chatgpt-python-dashboard.streamlit.app/): Dashboard to showcase power of ChatGPT and Streamlit. Used ChatGPT to create the starting code for the streamlit dashboard
- :fuelpump:[Gas Stations Locator](https://bit.ly/locationsDemo): Dashboard created with Streamlit and Python to plot gas station locations of Couche-Tard and Shell Canada. Pick a gas station and km radius and the app will locate all the Couche-Tard and Shell stations within that distance. App is a demo of how Python could be used in an M&A deal to help with cost synergy analysis. [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](hhttps://dbogt-locationsdemo-app-avfon4.streamlitapp.com/) 
- :chart_with_upwards_trend:[Stock Beta Calculator](https://bogdan.streamlit.app/Stock_Beta_Calculator): Dashboard created with Streamlit and Python to calculate a stock's beta. Pick a ticker and a stock index to run the regression and calculate the beta. [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bogdan.streamlit.app/Stock_Beta_Calculator) 
- :chart_with_upwards_trend:[Options Calculator](https://bogdan.streamlit.app/Stock_Beta_Calculator): Dashboard created with Streamlit and Python to calculate a call/put option value with Black Scholes. App also allows to scrape options chains from Yahoo Finance for a particular ticker and visualizes strike prices vs. implied vols and bid/ask/last price of option. [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bogdan.streamlit.app/Stock_Beta_Calculator) 
- :moneybag:[Ontario Sunshine List](https://bit.ly/ONSunshineList): Dashboard that explores 20+ years of public sector salary disclosures from Ontario (https://www.ontario.ca/page/public-sector-salary-disclosure). [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dbogt/on_sunshine/main) 
- :movie_camera::trophy:[Oscars Stats](https://oscars.streamlit.app/): Make predictions for the top categories and compare your answers with other people around the world. Also try out the Best Picture Emoji quiz while you're at it! [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://oscars.streamlit.app/)
- :game_die:[Board Game Collection](https://bitly.com/BGGApp): Check out your board game collection by connecting with your BoardGameGeek account. [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dbogt/bggcollection/main/app.py) 
"""

st.markdown(text)

st.sidebar.image("https://avatars.githubusercontent.com/u/59750436?v=4")
st.sidebar.write("Bogdan delivers a variety of courses at The Marquee Group and Training The Street that focus on financial modeling, data sciences, and programming.")
st.sidebar.write("Github: https://github.com/dbogt")
