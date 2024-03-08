import streamlit as st
from constants import TT_SLOTS, EMOJIS, DAYS, SELECTED
from utils import authenticate_tt_id, update_time_table, add_time_table, map_slot

# st.set_page_config(layout="wide")


def insert_user():
    # """-------------------------------------------- HEADER ------------------------------------------------------"""
    st.write("<center><h1>Join/Create TT</h1></center><br>", unsafe_allow_html=True)
    

    # """-------------------------------------------- NAME &  EMOJI ------------------------------------------------------"""
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.text_input("Name:", key="name")
    with col2: 
        st.text_input("Unique Time Table ID:", key="tt_id", help="Enter your unique id here to join your friend's time table.\nLeave this field empty if you wish to create a new time table.")
    with col3: 
        st.selectbox("Emoji:", options=EMOJIS, key="emoji", help="This will be used to represent you in the time table.")

    # """-------------------------------------------- TIME TABLE ------------------------------------------------------"""
    st.write("<center><h3 style='padding:15px 0 20px 0; font-size:25px; color:#9c9d9f;'>Select your slots</h3></center>", unsafe_allow_html=True)

    st_columns = st.columns([2,4,4,4,1,4,4,4,4])
    
    if "user_time_table" not in st.session_state:
        st.session_state["user_time_table"]=set()
    if "user_time_table_copy" not in st.session_state:
        st.session_state["user_time_table_copy"]=set()

    for i in range(0, len(st_columns)):
        for j in range(6):
            with st_columns[i]:
                string = f"C{i}R{j}"
                if i==0:
                    st.write(f"<center><h6 style='font-size:15px; color: #9c9d9f;'>{DAYS[j][:3].upper()}</h6></center>", unsafe_allow_html=True)
                    st.write(f"<br>", unsafe_allow_html=True)
                    continue
                if i==4:
                    st.write(f"<center><b style='color: #9c9d9f;'>{' LUNCH'[j]}</b><br></center>", unsafe_allow_html=True)
                    st.write(f"<br>", unsafe_allow_html=True)
                    continue
                elif j==0:
                    st.write(f"<center><b><h5 style='color: #9c9d9f;'>{TT_SLOTS[string]}</h5></b></center>", unsafe_allow_html=True)
                    continue
                else:
                    
                    if string not in st.session_state:
                        st.session_state[string] = -1
                    
                    button_text = TT_SLOTS[string]+SELECTED if st.session_state[string]%2 == 0 else TT_SLOTS[string].replace(SELECTED, "")
                    
                    if st.button(button_text, use_container_width=True, key=f"button_{string}", help=f"Double click to select {TT_SLOTS[string]}"):
                        st.session_state[string]+=1
                    
                    if SELECTED in button_text and button_text not in st.session_state["user_time_table"]:
                        st.session_state["user_time_table"].add(string)
                        st.session_state["user_time_table_copy"].add(TT_SLOTS[string])
                        
                    elif SELECTED not in st.session_state["user_time_table"] and button_text in st.session_state["user_time_table"]:
                        st.session_state["user_time_table"].remove(string)
                        st.session_state["user_time_table_copy"].remove(TT_SLOTS[string])

    st.write(f"<center style='color:#9c9d9f;font-size:15px;'>{'' if len(st.session_state['user_time_table_copy'])==0 else st.session_state['user_time_table_copy']}</center><br>", unsafe_allow_html=True)

    # """-------------------------------------------- SUBMIT ------------------------------------------------------"""
    if st.button("Submit", use_container_width=True):
        tt_id = st.session_state["tt_id"]
        name = st.session_state["name"]
        emoji = st.session_state["emoji"]
        tt_slots = list(st.session_state["user_time_table"])
        
        if name == "":
            st.toast("Please enter your name.")
        elif len(tt_slots) == 0:
            st.toast("Please select at least 1 time slot.")
        elif len(name)>25:
            st.toast("Name should be less than 15 characters.")
        elif len(tt_id)==0:
            unique_id = add_time_table(name, emoji, tt_slots)
            st.write(f"Your Time Table id is : {unique_id}, please note it down.")
            st.toast("Time Table created successfully, please note down your unique id.")
        elif len(tt_id)!=6:
            st.toast("Invalid Time Table ID.")
        elif not authenticate_tt_id(tt_id):
            st.toast("This Time Table ID does not exist.")
        else:
            response = update_time_table(tt_id, name, emoji, tt_slots)
            st.toast(response)
            
if __name__ == "__main__":
    st.set_page_config(page_title="Insert User", page_icon="📅", layout="wide")
    insert_user()