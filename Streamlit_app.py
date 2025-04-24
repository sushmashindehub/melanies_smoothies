# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits that you want in your custom smoothie!
  """
)

title = st.text_input("Name on your smoothie:")
st.write("The name on your smoothie will be:", title)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop()
#Convert snowpark dataframe to pandas so that we can use LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()



ingredients_list = st.multiselect("Choose upto 5 ingredients:",my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
       
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')

        st.subheader(each_fruit + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
    st.write(ingredients_string)        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER )
            values ('""" + ingredients_string + """','""" + title +"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + title + '!' ,  icon="✅")



