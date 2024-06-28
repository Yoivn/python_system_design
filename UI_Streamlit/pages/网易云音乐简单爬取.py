#网易云音乐简单爬取
#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12
import streamlit as st
import sys
# 添加music模块所在的路径
sys.path.append('../')
sys.path.append('../music')
from music.main import get_music

def show_images():
    st.image('./images/hello.jpg', caption='', width=100)

def main():
    show_images()
    id_list=[
        '',
        '1971144922',
        '2109171287',
        '2003700105',
        '1954381698',
        '37092571',
        '1809713120',
        '1809713123',
        '1809712330',
        '1809713146'
    ]
    id = st.sidebar.selectbox('音乐ID',id_list) 
    if id:
        get_music(id)
        st.audio(f'{id}.wav')

if __name__ == '__main__':
    main()
