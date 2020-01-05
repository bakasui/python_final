## Python技术文档
### 姓名：陈舒雨 学号：181013001 
#### 协作成员：18网新刘心如 17网新李煜华
- **[项目仓库](https://github.com/bakasui/python_final)**  
- **[Pythonanywhere网址](http://teoko.pythonanywhere.com/)**
### 项目介绍
为帮助有穷游意向的用户更快捷地选择东南亚的旅行目的地，我们选择了数据提取较为容易且拥有一定用户量的穷游网作为数据来源。该项目爬取了东南亚各国旅游景点的多项数据，使用柱状图、热力图等图表直观地为用户展示东南亚各国热度最高的地区及景点，并通过分析这些数据对每个东南亚国家的游客提出了参考性建议，且此项目网站设置了可供用户选择的交互控件，以让用户更方便地获取景点信息。

### 数据传递描述
将[all_position.csv](https://github.com/bakasui/python_final/blob/master/all_destination.csv)和[qiongyou_position.csv](https://github.com/bakasui/python_final/blob/master/qiongyou_position.csv)导入pycharm项目，使用pd.read读取两个csv文件，将其转化为列表的形式，再以“国家”作为索引词提取相关数据。通过函数将提取出的数据制成柱状图，并获取了百度地图API权限，生成了散点图和热力图。使用jiaja2来完成base页面与.py文件之间变量的传递，让html能够以设置好的css样式展现。

### HTML档描述
***base.html***
利用<style>标签设置了每一个页面的字体大小、表格宽度等基础样式，并包含了网页背景的渐变及星空效果和位于网页最上方的十一个按钮样式的代码。最上方的十一个按钮均为交互控件，点击之后即可跳转至相关url。即本项目网站包含初始页面url及用户选择跳转的另外10个url，总计能生成11种不同结果的url。

***sea_all.html***

就是东南亚每个国家所要展示的条形图，饼图和地图的源码。

***try.html***


### PYTHON档描述
***app.py***

此python档使用import引入了pandas、pyecharts等模块，利用函数实现前端与后端的传值。

***minding.py***


### WEB APP动作描述
用户根据自己的需求，点击右上角的按钮选择目的地，页面会由展示了东南亚旅游概况的初始界面跳转至被选择的地点的旅游概况。同时，用户能够左右拖动柱状图的滚动条以查看每个地区的参观人数及景点数量。

