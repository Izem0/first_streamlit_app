import requests
import pandas
import streamlit
import snowflake.connector
from urllib.error import URLError


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
def get_fruity_vice_data(fruit_name):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    # get fruityvice data
    fruit_data = get_fruity_vice_data(fruit_choice)
    # show data
    streamlit.dataframe(fruit_data)
    # small msg
    streamlit.write('The user entered ', fruit_choice)
    
except URLError as e:
  streamlit.error()
 

# ========= snowflake connector ============= #
# streamlit.stop()
# init connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  
streamlit.header("View our fruit list - Add your favorites!")

def get_fruit_loat_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    my_cnx.close()
    return my_cur.fetchall()


if streamlit.button('Get fruit list'):
  my_data_rows = get_fruit_loat_list()
  streamlit.dataframe(my_data_rows)

# add fruit to list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    my_cnx.close()
    return f"{new_fruit} was successfully added!"

new_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  resp = insert_row_snowflake(new_fruit)
  streamlit.text(resp)
  
# my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
