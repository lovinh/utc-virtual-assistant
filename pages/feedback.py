import streamlit as st
import streamlit_star_rating as st_star
from blocks.side_bar import render_side_bar
from model.feedback import load_feedback_object

st.set_page_config(
    page_title="Feedback | UTC Virtual Assistant",
    page_icon="res\icon.png",
)

render_side_bar() # Query channels list from firebase - TODO

feedback_model = load_feedback_object()

st.title("🤖 Feedback")
if st.session_state.get("is_feedback_sent", None) != None:
    if st.session_state.get("is_feedback_sent", None):
        st.balloons()   
        st.success("Cảm ơn bạn đã gửi ý kiến!")    
        st.session_state["is_feedback_sent"] = None 
    else:
        st.error("Có lỗi xảy ra trong quá trình gửi. Vui lòng thử lại sau.")

with st.form(border=True, clear_on_submit=False, key="feedback_form"):
    feedback_content: str = st.text_area(
        "Để lại ý kiến đóng góp của bạn", height=200, key="txt_feedback")
    submitted: bool = st.form_submit_button("Gửi")
    if submitted:
        is_success : bool = False
        with st.spinner("Đang gửi ý kiến..."):
            is_success = feedback_model.send_feedback(feedback_content)  
        st.session_state["is_feedback_sent"] = is_success
        st.rerun()
