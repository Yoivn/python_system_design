#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12

import streamlit as st
import pandas as pd
import plotly.graph_objects as go 

# 读文件
@st.cache_data 
def read_file(file_path):
    
    data = pd.read_csv(file_path)
    province_list=data['省市']
    type_list=data['类型']
    return province_list,type_list,data

# 展示学校排名  
def show_university_rankings():
    st.sidebar.title("中国大学排名") 
    st.image('./images/hello.jpg', caption='', width=100)
    
    # 文件路径构建
    str1 = '../university_rankings/'
    str2 = '_cn_university_rankings.csv'
    
    # 年份选择框
    year_choice = st.sidebar.selectbox('请选择年份', ['2024', '2023', '2022', '2021', '2020'])
    file_path = str1 + year_choice + str2
    
    # 读取数据
    province_list,type_list,data = read_file(file_path)
    page_data = pd.DataFrame(data, columns=['排名', ' 学校名称', '省市', '类型', '总分', '办学层次'])
    
    # 显示数据统计信息
    length = len(page_data)
    st.subheader(f'{year_choice}年份共有{length}条大学排名数据')
    
    # 是否显示搜索框
    show_filter = st.sidebar.checkbox('需要筛选请点击此处')
    if show_filter:
        search_university_filter = st.sidebar.checkbox('直接搜索')
        if search_university_filter:
            search_university = st.sidebar.text_input("输入学校名称(支持模糊搜索)：")
            if search_university:
                university_name_filtered_data = page_data[page_data[' 学校名称'].str.contains(search_university.strip(), case=False)]
                page_data = university_name_filtered_data
        search_province_filter = st.sidebar.checkbox('省市')
        if search_province_filter:
            select_province=st.sidebar.selectbox('选择省市',province_list.unique())
            if select_province:
                province_filtered_data=page_data[page_data['省市'].str.contains(select_province.strip(), case=False)]
                page_data = province_filtered_data
        search_type_filter = st.sidebar.checkbox('类型')
        if search_type_filter:
            select_type=st.sidebar.selectbox('选择省市',type_list.unique(),index=None)
            if select_type:
                type_filtered_data=page_data[page_data['类型'].str.contains(select_type.strip(), case=False)]
                page_data = type_filtered_data
        
    
    # 使用Plotly创建交互式表格
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(page_data.columns),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[page_data['排名'], page_data[' 学校名称'], page_data['省市'],
                           page_data['类型'], page_data['总分'], page_data['办学层次']],
                   fill_color='lavender',
                   align='center'))
    ])
    
    st.plotly_chart(fig)

if __name__ == '__main__':
    show_university_rankings()
