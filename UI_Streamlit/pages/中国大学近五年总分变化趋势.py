#中国大学近五年总分变化趋势.py
#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12

import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def read_file(file_path):
    data = pd.read_csv(file_path, encoding='utf-8')
    return data

def university_rankings_trend():
    st.title('查看某大学近五年总分的变化趋势')
    
    # 用于设置文件路径
    file_base_path = '../university_rankings/'
    file_format = '_cn_university_rankings.csv'
    
    # 读取2024年的数据以获取大学列表
    file_path_2024 = file_base_path + '2024' + file_format
    data_2024 = read_file(file_path_2024)
    
    # 提取大学列表
    university_list = data_2024[' 学校名称'].unique()
    
    # 侧边栏选择多个大学
    selected_universities = st.sidebar.multiselect('选择大学', university_list)
    
    if selected_universities:
        trend_data = pd.DataFrame()  # 初始化一个空的 DataFrame 来存储趋势数据
        
        # 逐年读取数据
        for year in ['2020', '2021', '2022', '2023', '2024']:
            file_path = file_base_path + year + file_format
            data = read_file(file_path)
            
            # 筛选选择的大学数据
            selected_data = data[data[' 学校名称'].isin(selected_universities)]
            
            # 如果有数据，则添加到趋势数据中
            if not selected_data.empty:
                selected_data['年份'] = year  # 添加年份列
                trend_data = pd.concat([trend_data, selected_data], ignore_index=True)
        
        if not trend_data.empty:
            st.table(trend_data)
            
            # 使用Plotly绘制交互式折线图
            fig = px.line(trend_data, x='年份', y='总分', color=' 学校名称', title='大学总分变化趋势')
            st.plotly_chart(fig)
        else:
            st.write('未找到选择大学的数据。')

if __name__ == '__main__':
    university_rankings_trend()
