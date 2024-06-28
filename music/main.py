import requests
import streamlit as st

def get_music(id):
    # 文件的 URL
    file_url = f'http://music.163.com/song/media/outer/url?id={id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }
    # 本地文件存储路径
    local_file_path = f"{id}.wav"

    # 发送 GET 请求
    response = requests.get(file_url, stream=True,headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开本地文件进行写入
        with open(local_file_path, 'wb') as file:
            # 分块写入文件，避免占用过多内存
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        st.subheader(f"文件下载成功，并保存至 {'python_system_design/UI_Streamlit'}{local_file_path}")
    else:
        st.subheader(f"文件下载失败. HTTP Status Code: {response.status_code}")

    # #创建WebDrive实例,打开浏览器
    # driver = Chrome()
    # driver.get('http://music.163.com/song/media/outer/url?id=2003700105')


