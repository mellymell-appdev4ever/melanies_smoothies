# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My Parents New Healthy Diner")
st.write(
    """Breakfast menu
    """
)
st.write("Omega 3 & Blueberry Oatmeal")
st.write("Kale, Spinach and Rocket Smoothie")
st.write("Hard-Boiled Free-Range Egg")


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your order will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name_on_order + "', '" + ingredients_string + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button ('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered')

