import streamlit as st
from const import TT_SLOTS, DAYS
from utils import fetch_tt_data, remove_duplicates, authenticate_tt_id

st.session_state["isloggedin"] = False


def display_tt():
    # """----------------------------------------------- HEADER ----------------------------------------------------------"""
    st.write("<center><h1>TT WebApp</h1></center>", unsafe_allow_html=True)
    temp = st.empty()
    temp.write("<center><h3>View Your Time Table</h3></center><br><br>", unsafe_allow_html=True)

    # """-------------------------------------------- NAME &  EMOJI ------------------------------------------------------"""
    column = st.empty()
    _, mid_col, _ = column.columns(3)
    
    if "isloggedin" not in st.session_state:
        st.session_state["isloggedin"] = False
    if "tt_id" not in st.session_state:
        st.session_state["tt_id"] = ""
    
    with mid_col:
        with st.form(key="login"):
            tt_id = st.text_input("Unique Time Table ID:", help="To join a time table, ask the creator for the unique time table id and enter it below. If you are the creator, then enter the unique time table id and select the 'Create' button.")
            if st.form_submit_button("Submit", use_container_width=True) and authenticate_tt_id(str(tt_id.upper().replace(" ", "")).strip()):
                st.session_state["isloggedin"] = True
                _id = st.session_state["tt_id"] = str(tt_id.upper().replace(" ", "")).strip()
                st.toast("Logged in successfully!", icon="🎉")
                
            st.caption("Go to Join/Create TT section to create a new time table or join an existing one.")
                
    if st.session_state["isloggedin"]:
        column.empty()
        temp.write("<br><br>", unsafe_allow_html=True)
        
        tt_slots_copy = TT_SLOTS.copy()

        for key in tt_slots_copy:
            tt_slots_copy[key] = ""
        
        try:
            data = fetch_tt_data(_id)
            names_list = data[0][_id].keys()
            
            for slot in tt_slots_copy:
                for name in names_list:
                    emoji = data[0][_id][name]["emoji"]
                    user_tt_slots = data[0][_id][name]["tt_slots"]
                    
                    if slot in user_tt_slots:
                        tt_slots_copy[slot] = remove_duplicates(f"{str(tt_slots_copy[slot])+str(emoji)}")
                
            st_columns = st.columns([2,4,4,4,1,4,4,4,4])

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
                        elif tt_slots_copy[string] != "":
                            st.button(tt_slots_copy[string], use_container_width=True, key=f"button_{string}_{0}", help=f"This is slot {TT_SLOTS[string]}")
                            continue
                        else:
                            if string not in st.session_state:
                                st.session_state[string] = -1
                            
                            st.button(TT_SLOTS[string], use_container_width=True, key=f"button_{string}_{0}", help=f"This is slot {TT_SLOTS[string]}")
    
            for name in names_list:
                emoji = data[0][_id][name]["emoji"]
                st.write(f"{emoji}: {name}")
                
        except UnboundLocalError:
            st.write("<center><h1>Oops, looks like you've encoutered a bug. Please reload the page, I'm sure it'll work then. If it doesn't, then please contact me, I've a lot of free time.</h1></center>", unsafe_allow_html=True)
            
        
if __name__ == "__main__":
    st.set_page_config(page_title="Time Table", page_icons="📅", layout="wide")
    display_tt()