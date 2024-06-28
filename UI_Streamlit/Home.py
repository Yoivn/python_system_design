#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12
import streamlit as st

#展示主页
def show_home():
    st.title("Python课程-期末系统设计")
    st.sidebar.header('贵州大学')
    st.sidebar.subheader('徐宝')
    st.image('./images/hello2.jpg',width=500)
    st.header("完成内容：")
    st.markdown("##### (1)对2020~2024年的中国大学排名进行了爬取，并在此页面上进行展示")
    st.markdown("##### (2)尝试通过给出的网易云某首歌的id信息，在不登陆的情况下爬取音乐并下载")
    

if __name__ == "__main__":
    
    show_home()
