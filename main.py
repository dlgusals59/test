import streamlit as st

import mapp
import py_Dash
import py_table

def main():
    # site-packages / streamlit / static / static / js /로 이동하여 'main ... chunk.js'파일을 찾아서 엽니다.
    # 검색하여 다음 document.title="".concat(t," \xb7 Streamlit")으로 바꿉니다.document.title="".concat(t,"")
    # Streamlit 앱을 다시 시작하면 제목에서 "· Streamlit"이 사라집니다.
    st.set_page_config(layout="wide",page_title='Demo')
    # hide_menu_style = """
    #             <style>
    #                 #MainMenu {visibility: hidden;}
    #                 footer {visibility: hidden;}
    #             </style>
    #             """
    # st.markdown(hide_menu_style, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: blue; margin:0 0;'>Python Web Dashboard Demo</h1>", unsafe_allow_html=True)

    PAGES = {
        "대시보드": py_Dash,
        "상세 테이블": py_table,
        "지도":mapp
    }
    #st.sidebar.image(obj, width=100)
    st.sidebar.title('Navigation')
    selection = st.sidebar.selectbox("GO", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


if __name__ == '__main__':
    main()
