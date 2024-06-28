#其他.py
#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12
import streamlit as st
@st.cache_data
def show_images():
    st.image('./images/hello3.jpg', caption='')
#其他功能    
def show_ohters():
    st.title("其他功能尚未完成")  
    show_images()
    
if __name__ =='__main__':
    show_ohters()