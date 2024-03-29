import streamlit as st
from updateTT import insert_user
from displayTT import display_tt
from st_on_hover_tabs import on_hover_tabs


st.set_page_config(page_title="TT WebApp", page_icon="./assets/logo.png", layout="wide")
st.markdown('<style>' + open('./assets/style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    st.image('./assets/logo.png')
    st.write("")
    tabs = on_hover_tabs(tabName=['View My TT', 'Join/Create TT', 'Heyp Me', 'About Me'], 
                         iconName=['home', 'add_circle', 'help', 'info'], default_choice=0)
    st.write("")
    st.write(f"<center><h6 style='font-size:15px; color: #9c9d9f; padding: 20px 0 0 0'>By arpy8</h6></center>", unsafe_allow_html=True)
    
    
if tabs =='View My TT':
    display_tt()

elif tabs == 'Join/Create TT':
    insert_user()

elif tabs == 'Heyp Me':
    st.write(open('./assets/heyp.html', 'r', encoding='cp1252').read(), unsafe_allow_html=True)

elif tabs == 'About Me':
    st.title("Hi, I am arpy8")