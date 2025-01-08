import streamlit as st
import streamlit_star_rating as st_star
from blocks.side_bar import render_side_bar

st.set_page_config(
    page_title="Báo cáo lỗi | UTC Virtual Assistant",
    page_icon="res\icon.png",
)

render_side_bar() # Query channels list from firebase - TODO

st.title("🤖 Báo cáo lỗi")

with st.form(border=True, clear_on_submit=False, key="report-form"):
    st.markdown(
"""
Mô tả lỗi bạn gặp phải:

**⚠ Chú ý**: Hãy đi kèm với nội dung câu hỏi bạn đã hỏi
"""
    )
    st.text_area("Mô tả lỗi bạn gặp", height=200, label_visibility="collapsed")
    st.write("Đính kèm file mô tả (nếu có):")
    st.file_uploader(".", accept_multiple_files=True, key="report-attached-files", label_visibility="collapsed")
    submitted = st.form_submit_button("Gửi")

