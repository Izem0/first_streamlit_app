import requests
import pandas
import streamlit
import snowflake.connector
import random


streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import fruits list
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list.set_index('Fruit', inplace=True)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# ========= Fruityvice api response ============= #
streamlit.header('Fruityvice Fruit Advice!')

# user input
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# get fruityvice data
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# show fruityvice data
streamlit.dataframe(fruityvice_normalized)

# ========= snowflake connector ============= #
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_added = streamlit.text_input('What fruit would you like to add?', random.choice(my_data_rows[0].values))
streamlit.write(f'The user entered {fruit_added}')

