#中国大学的地图分布.py
#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12

import folium
import pandas as pd
import geopandas as gpd
import streamlit as st
import numpy as np
import random
from folium import Marker
from streamlit_folium import folium_static#用于绘制地图
from shapely.geometry import MultiPolygon#用于计算地图轮廓的不规则几何体

@st.cache_data
def read_file(file_path):
    data = pd.read_csv(file_path)
    university_list = data[' 学校名称']
    province_list=data['省市']
    return province_list,university_list, data

def get_shape_data():
    shape_data = gpd.read_file('./China/China.shp', encoding='utf-8')
    return shape_data
@st.cache_data
def show_image():
    st.image('./images/hello.jpg', caption='', width=100)

def generate_points_within_province(province_shape, num_points):
    """生成指定数量的点，确保所有点都位于指定省份的轮廓内"""
    bounds = province_shape.total_bounds  # 获取省份边界框作为潜在点生成的范围
    
    # 在省份边界内生成大量潜在点
    potential_points = gpd.GeoSeries(
        gpd.points_from_xy(
            np.random.uniform(bounds[0], bounds[2], size=num_points * 20),
            np.random.uniform(bounds[1], bounds[3], size=num_points * 20)
        )
    )
    
    # 检查并收集所有落在省份内的点
    selected_points = []
    for idx, geom in enumerate(province_shape.geometry):
        # 对于多部件几何体，遍历每一个子几何体
        if isinstance(geom, MultiPolygon):
            for sub_geom in geom.geoms:
                mask = potential_points.intersects(sub_geom)
                selected_points.extend(potential_points[mask].centroid.apply(lambda x: (x.y, x.x)).tolist())
        else:  # 如果是单一的Polygon
            mask = potential_points.intersects(geom)
            selected_points.extend(potential_points[mask].centroid.apply(lambda x: (x.y, x.x)).tolist())
    
    # 随机选择或直接返回num_points个点
    if len(selected_points) >= num_points:
        return random.sample(selected_points, num_points)
    else:
        print(f"实际找到的点数 {len(selected_points)} 少于所需点数 {num_points}")
        return selected_points
def show_university_position():
    st.sidebar.markdown("#### 在地图上显示大学所在省的轮廓及散点分布图 (2024年数据)")

    show_image()

    shape_data = get_shape_data()
    
    str1 = '../university_rankings/'
    year = '2024'
    file_path = str1 + year + '_cn_university_rankings.csv'
    province_list,university_list, data = read_file(file_path)

    show_filter = st.sidebar.checkbox('需要筛选请点击此处')
    if show_filter:
        university_name_filter = st.sidebar.checkbox('大学')
        if university_name_filter:
            university_name = st.sidebar.selectbox('选择大学', university_list, index=None)
            if university_name:
                university_data = data[data[' 学校名称'].str.contains(university_name.strip(), case=False)]
                if not university_data.empty:
                    province = university_data.iloc[0]['省市'].strip()

                    # 读取 shapefile 文件，指定编码为 'utf-8'
                    # 过滤出省市的地理轮廓数据
                    province_shape = shape_data[
                        (shape_data['name'] == province+'省') |
                        (shape_data['name'] == province+'市') |
                        (shape_data['name'] == province+'自治区') |
                        (shape_data['name'] == province+'特别行政区')
                    ]
                    if province=='广西':
                        province_shape = shape_data[shape_data['name'] == province+'壮族自治区']
                    elif province=='宁夏':
                        province_shape = shape_data[shape_data['name'] == province+'回族自治区']
                    elif province=='新疆':
                        province_shape = shape_data[shape_data['name'] == province+'维吾尔自治区']
                    if not province_shape.empty:
                        # 创建地图 m，并显示省份轮廓
                        m = folium.Map(location=[province_shape.geometry.centroid.y.values[0], province_shape.geometry.centroid.x.values[0]], zoom_start=6)
                        folium.GeoJson(province_shape).add_to(m)
                        
                        # 添加省份中心点的标注
                        center_lat = province_shape.geometry.centroid.y.values[0]
                        center_lon = province_shape.geometry.centroid.x.values[0]
                        
                        Marker([center_lat, center_lon], popup=f'{province}省份{university_name}').add_to(m)

                        
                        folium_static(m, width=800, height=700)
                    else:
                        st.write(f'未找到 "{province}" 省份的地理轮廓。')
            else:
                st.write(f'未找到 "{university_name}" 大学的数据。')
        province_filter = st.sidebar.checkbox('省市')
        if province_filter:
            province_name = st.sidebar.selectbox('选择省市', province_list.unique(), index=None)
            if province_name:
                province_data = data[data['省市'].str.contains(province_name.strip(), case=False)]
                if not province_data.empty:
                    province = province_data.iloc[0]['省市'].strip()

                    # 读取 shapefile 文件，指定编码为 'utf-8'
                    # 过滤出省市的地理轮廓数据
                    province_shape = shape_data[
                        (shape_data['name'] == province+'省') |
                        (shape_data['name'] == province+'市') |
                        (shape_data['name'] == province+'自治区') |
                        (shape_data['name'] == province+'特别行政区')
                    ]
                    if province=='广西':
                        province_shape = shape_data[shape_data['name'] == province+'壮族自治区']
                    elif province=='宁夏':
                        province_shape = shape_data[shape_data['name'] == province+'回族自治区']
                    elif province=='新疆':
                        province_shape = shape_data[shape_data['name'] == province+'维吾尔自治区']
                    if not province_shape.empty:
                        # 创建地图 m，并显示省份轮廓
                        m = folium.Map(location=[province_shape.geometry.centroid.y.values[0], province_shape.geometry.centroid.x.values[0]], zoom_start=6)
                        folium.GeoJson(province_shape).add_to(m)
                        num_points = province_data.shape[0]
                        
                        st.subheader(f'{province}有{num_points}所大学')
                        
                        #原算法
                        # selected_random_points=[]
                        # bounds = province_shape.total_bounds
                        # random_lat = np.random.uniform(bounds[1], bounds[3])# bounds[1]是最小纬度，bounds[3]是最大纬度
                        # random_lon = np.random.uniform(bounds[0], bounds[2])# bounds[0]是最小经度，bounds[2]是最大经度
                        # selected_random_points.append([random_lat,random_lon])
                        
                        #改进后算法
                        #控制随机点的分布在轮廓范围内
                        selected_random_points = generate_points_within_province(province_shape, num_points)

                        for point in selected_random_points:
                            folium.Marker(point, popup=f'{province}').add_to(m)
                        folium_static(m, width=800, height=400)
                    else:
                        st.write(f'未找到 "{province}" 省份的地理轮廓。')
            else:
                st.write(f'未找到数据。')
    else:
        # 默认显示中国地图的轮廓和各个大学随机散点分布
        m = folium.Map(location=[35.8617, 104.1954], zoom_start=4)  # 设定中国的中心经纬度及缩放级别
        
        for university_name in university_list:
            if university_name:
                university_data = data[data[' 学校名称'].str.contains(university_name.strip(), case=False)]
                if not university_data.empty:
                    province = university_data.iloc[0]['省市'].strip()
                    
                    # 读取 shapefile 文件，指定编码为 'utf-8'
                    # 过滤出省市的地理轮廓数据
                    province_shape = shape_data[
                        (shape_data['name'] == province+'省') |
                        (shape_data['name'] == province+'市') |
                        (shape_data['name'] == province+'自治区') |
                        (shape_data['name'] == province+'特别行政区')
                    ]
                    if province=='广西':
                        province_shape = shape_data[shape_data['name'] == province+'壮族自治区']
                    elif province=='宁夏':
                        province_shape = shape_data[shape_data['name'] == province+'回族自治区']
                    elif province=='新疆':
                        province_shape = shape_data[shape_data['name'] == province+'维吾尔自治区']
                    if not province_shape.empty:
                        #显示轮廓，但会叠加
                        #folium.GeoJson(province_shape).add_to(m)
                        
                        #原算法
                        # selected_random_points=[]
                        # bounds = province_shape.total_bounds
                        # random_lat = np.random.uniform(bounds[1], bounds[3])# bounds[1]是最小纬度，bounds[3]是最大纬度
                        # random_lon = np.random.uniform(bounds[0], bounds[2])# bounds[0]是最小经度，bounds[2]是最大经度
                        # selected_random_points.append([random_lat,random_lon])
                        
                        #改进后算法
                        #控制随机点的分布在轮廓范围内
                        selected_random_points = generate_points_within_province(province_shape, 1)
                        
                        for point in selected_random_points:
                            folium.Circle(
                            location=point,
                            #radius=1000,  # 半径，单位是米
                            color='red',  # 边界颜色
                            fill=True,
                            fill_color='red'
                        ).add_to(m)    
                    else:
                        st.write(f'未找到 "{province}" 省份的地理轮廓。')
            else:
                st.write(f'未找到 "{university_name}" 大学的数据。')
        folium_static(m, width=800, height=500)
                
            

if __name__ == '__main__':
    show_university_position()
