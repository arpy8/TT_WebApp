import streamlit as st
from updateTT import insert_user
from displayTT import display_tt
from st_on_hover_tabs import on_hover_tabs

st.set_page_config(page_title="TT WebApp", page_icon="📅", layout="wide")
st.markdown('<style>' + open('./assets/style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['View My TT', 'Join/Create TT', 'Heyp Me', 'About Me'], 
                         iconName=['home', 'add_circle', 'help', 'info'], default_choice=0)

if tabs =='View My TT':
    display_tt()

elif tabs == 'Join/Create TT':
    insert_user()

elif tabs == 'Heyp Me':
    st.write(open('./assets/heyp.html', 'r', encoding='cp1252').read(), unsafe_allow_html=True)

elif tabs == 'About Me':
    st.title("I am arpy8")