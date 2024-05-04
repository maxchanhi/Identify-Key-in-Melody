import streamlit as st
from notation import keyscale,easymode,intermediate,fun_emoji_list,hard
import random
from score_generation import lilypond_generation
from motif import generate_options,main_generation
from streamlit_extras.let_it_rain import rain
st.set_page_config(page_title="Identify Key in Melody")

st.title("Identify the Key in a Melody")

difficulty = st.selectbox("Select Difficulty", ["Easy Mode", 
                                                 "Intermediate Mode",
                                                 "Advanced Mode",
                                                 "Custom Mode"])

# Filter the keyscale dictionary based on the selected difficulty
filtered_keyscale = {}

if difficulty == "Easy Mode (2 sharps to 2 flats)":
    disable_select = True
    for key, scale in keyscale.items():
        if key in easymode:
            filtered_keyscale[key] = scale
elif difficulty == "Intermediate Mode (5 sharps to 5 flats)":
    disable_select = True  
    for key, scale in keyscale.items():
        if key in intermediate:
            filtered_keyscale[key] = scale
elif difficulty == "Advanced Mode (All sharps and flats)":
    disable_select = True 
    for key, scale in keyscale.items():
        if key in hard:
            filtered_keyscale[key] = scale
else:
    filtered_keyscale = keyscale
    disable_select = False

selected_keys = st.multiselect("Selected Keys", list(filtered_keyscale.keys()),filtered_keyscale,disabled=disable_select)
if len(selected_keys) <5:
    st.warning("Please select at least five keys to generate a question.")
    st.stop()
if 'user_answer' not in st.session_state:
    st.session_state['user_answer'] = ''
if 'ans_key' not in st.session_state:
    st.session_state['ans_key'] = ''
if 'options' not in st.session_state:
    st.session_state['options'] = ''

new_score = st.button("Generate Score")
if new_score and selected_keys:
    st.session_state['ans_key']  = random.choice(selected_keys)
    st.session_state['options'] = generate_options(st.session_state['ans_key'], selected_keys)
    melody = main_generation(st.session_state['ans_key'])
    lilypond_generation(melody,"testing",4,4)
    print("options", st.session_state['options'] )
if st.session_state['options']:
    st.write("What key is the score in?")
    option_list = st.session_state['options']
    st.image("static/cropped_score_testing.png", use_column_width=True)
    st.audio("static/testing.mp3", format="audio/mpeg")
    user_answer = st.radio("Select the key:", options= option_list,index=False )
    st.session_state['user_answer'] = user_answer

    ans_key = st.session_state['ans_key']
    user_answer = st.session_state['user_answer']
    check = st.button("Check Answer")

    print("user_answer", user_answer, "ans_key", ans_key)
    if check:
        if user_answer == ans_key and user_answer is not None:
            st.success("Correct!")
            fun_emoji = random.choice(fun_emoji_list)
            rain(emoji = fun_emoji,animation_length="1")
        elif user_answer != ans_key:
            st.warning(f"Incorrect. The correct answer is {st.session_state['ans_key']}.") 
