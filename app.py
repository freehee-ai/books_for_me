import streamlit as st
from search import run_app
from app_local_lib import app_local_lib

def main() :
    st.title('AI 책 추천')

    menu = ['Home', '책추천', 'AI책추천', '도서관찾기']
    choice = st.sidebar.selectbox('메뉴', menu)
    if choice == menu[0] :
            ()
    elif choice == menu[1] :
        run_app()
    elif choice == menu[2] :
            ()
    elif choice == menu[3] :
        app_local_lib()






if __name__ == '__main__' :
        main()