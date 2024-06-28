#大学排名爬取-拓展(爬取2020~2024年的排名数据)
#学号 2100170027 姓名 徐宝 贵州大学
#运行环境 vscode windows11 python3.12
#必要工具chrome,chromedrive
#必要条件chrome与chromedrive版本一致

import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome#驱动
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #定位
from selenium.webdriver.common.keys import Keys


def write_file(str,rankings):
    #文件路径
    file_path=str+'_'+'cn_university_rankings.csv'
    #write
    with open(file_path,'w',encoding='utf-8',newline='') as file:
        writer=csv.writer(file)
        #写入表头
        writer.writerow(['排名',' 学校名称','省市','类型','总分','办学层次'])
        #写入数据
        writer.writerows(rankings)
    print(f'{str}年的中国大学排名数据已经成功写入{file_path}')
def status_code_is_200(url):
    #确定是否能够访问url
    response=requests.get(url)
    status_code=response.status_code
    if  status_code==200:
        response.close()
        return True
    else:
        print(f"HTTP状态码: {status_code} - 请求失败")
        if 400 <= status_code < 500:
            print("客户端错误，请检查URL或请求参数。")
        elif 500 <= status_code < 600:
            print("服务器错误，请稍后再试。")
        else:
            print("请求出现问题，请检查网络连接或URL是否正确。")
        response.close()
        return False

def open_url_and_get_driver(url):
    #创建WebDrive实例,打开浏览器
    #如果在系统环境变量配置了chromedrive.exe的路径,则可如此使用
    #否则在Chrome()中以绝对路径作为参数传入,
    #例如Chrome('./')也可调用,但需保证chromedrive.exe在同目录下
    driver = Chrome()
    #使用get方法打开一个网页
    driver.get(url)
    return driver

    #获取网页内容
    #page_source=driver.page_source
    #打印
    #print(page_source)

def find_input_element(driver):  
    #找到键入信息能够操纵跳转页数的目的元素
    #等待页面加载完成，可以根据需要进行等待
    #使用CSS选择器定位
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ant-pagination-options-quick-jumper'))
    )
    # 在<div>内部找到<input>元素并返回
    return div_element.find_element(By.CSS_SELECTOR, 'input[type="text"]')

def page_redirect(i,input_element):
    #传入的参数为需要跳转的页数与
    #实现页面跳转功能
    input_element.send_keys(f'{i}')  #此处键入页数
    time.sleep(1)
    # 模拟按下Enter键
    input_element.send_keys(Keys.ENTER)
    
def get_university_rankings(content):
    #通过bs4从当前网页提取信息
    #然后转为列表进行存储
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    links = soup.find_all('tr')  #提取所有<tr>标签中的链接
    rankings=[]
    t=True
    # 提取<tr>标签中的<td>的文本内容
    for tr in links:   
        text = tr.get_text().strip() 
        if text:  # 如果文本内容不为空
            #去除第一行不需要的信息
            if t:
                t=False
                continue
            #将text按空格进行切分另命名为temp
            temp=text.split()
            #print(temp)测试用
            #因为切分后存储做temp的列表中存在不需要的元素(大学英文名),进行切分去除
            #且100之前的学校是有办学层次这一评比
            if int(temp[0])>int('100'):
                temp=temp[:2]+temp[-3:]
            else:
                temp=temp[:2]+temp[-4:]
            #list.append(temp)
            rankings.append(temp)
    #print(rankings)
    return rankings
    
def perform_tasks(str,url):
    #执行爬取当前url大学排名的方法
    #打开浏览器进入指定url
    driver=open_url_and_get_driver(url)
    
    #获取网页内容
    page_source=driver.page_source
    input_element=find_input_element(driver)
    rankings=[]
    #传入参数以控制页面跳转,同时爬取该页数据存入rankings列表
    for i in range(2,21):
        page_source=driver.page_source
        #print(page_source)
        time.sleep(1)
        rankings=rankings + get_university_rankings(page_source)
        page_redirect(i,input_element)
    #写入将数据写入本地文件
    write_file(str,rankings)
    #关闭浏览器
    driver.quit()

if __name__ == "__main__":
    str='202'
    url='https://www.shanghairanking.cn/rankings/bcur/'
    
    for i in range(5):
        if status_code_is_200(url+str+f'{i}'):
            perform_tasks(str+f'{i}',url+str+f'{i}')
            print('任务执行成功,退出程序')
        else:
            print('任务执行失败,退出程序')
    

    