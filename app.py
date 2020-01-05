from flask import Flask,render_template,request
import pandas as pd
import os
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from collections import Counter
import minding

mapbox_access_token = "pk.eyJ1IjoiY3VwYmVpIiwiYSI6ImNrNG1iMDJrZDI4NngzZXF3MHY1ZTB2aXUifQ.AlCV3ory0DrxiKwJqlFZiQ"
dir_path=os.path.dirname(os.path.abspath(__file__))

sea_ename=['philippines','cambodia','thailand','brunei','vitetnam','laos','malaysia','myanmar','east-timor','indonesia']
qyer_position=pd.read_csv(dir_path+'/qiongyou_position.csv',index_col=['country'],encoding='utf_8')
df=pd.read_csv(dir_path+'/all_destination.csv',index_col=['country'],encoding='utf_8')
qp=qyer_position

sea_text=minding.sea

def visited_sum():
    list1=[]
    for i in range(10):
        list1.append(str(qp.loc[sea_ename[i]]['visitedNumber'].sum()))
    return list1

def place_sum():
    list1=[]
    for i in range(10):
        list1.append(str(qp.loc[sea_ename[i]]['placeNumber'].sum()))
    return list1


visited_sum=visited_sum()
def bar_sea_visited() -> Bar:
    c = (
        Bar()
        .add_xaxis(sea_ename)
        .add_yaxis("东南亚",visited_sum, color=Faker.rand_color())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-东南亚各国参观（visited）数"),
            datazoom_opts=[opts.DataZoomOpts()],  
        )
        )
    return c.render_embed()
place_sum=place_sum()
def bar_sea_place() -> Bar:
    c = (
        Bar()
        .add_xaxis(sea_ename)
        .add_yaxis("东南亚",place_sum, color=Faker.rand_color())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-东南亚各国景观/目的地数"),
            datazoom_opts=[opts.DataZoomOpts()],  
        )
        )
    return c.render_embed()

    
html1=bar_sea_visited()
html2=bar_sea_place()

html='''{% extends 'base.html' %}
    {% block body %}
    '''+'''
    <div class='each_country'>
    {html1}
    </div>
    <div class='each_country'>
    {html2}
    </div>
    <div>
    {sea_text}
    </div>
    '''.format(html1=html1,html2=html2,sea_text=sea_text)+'''
    {% endblock %}
    '''

with open(dir_path+'/templates/sea_all.html','w',encoding='utf-8')as f:
    f.write(html)
       
app = Flask(__name__)

@app.route('/',methods=["GET"])  #生成东南亚参观数和景观数
def all_sea():
    return render_template('sea_all.html')

@app.route('/anyone',methods=("GET","POST"))
def map():
    def each_country_city_visited(country_name):
        list1=[str(i) for i in qp.loc[country_name]['visitedNumber']]
        return list1
        
    def each_country_city_place(country_name):
        list1=[str(i) for i in qp.loc[country_name]['placeNumber']]
        return list1

    def each_country_city_name(country_name):
        list1=[i for i in qp.loc[country_name]['city_cn']]
        return list1
    country=request.form['country']
    
    each_country_city_visited=each_country_city_visited(country)
    each_country_city_place=each_country_city_place(country)
    each_country_city_name=each_country_city_name(country)
    def bar_each_visited() -> Bar:
        c = (
            Bar()
            .add_xaxis(each_country_city_name)
            .add_yaxis(str(country),each_country_city_visited, color=Faker.rand_color())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-"+str(country)+"各地参观（visited）数"),
                datazoom_opts=[opts.DataZoomOpts()],  
            )
            
        )
        return c.render_embed()

    def bar_each_place() -> Bar:
        c = (
            Bar()
            .add_xaxis(each_country_city_name)
            .add_yaxis(str(country),each_country_city_place,color=Faker.rand_color())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-"+str(country)+"各地景观/目的地数"),
                datazoom_opts=[opts.DataZoomOpts()],  
            )
            
        )
        return c.render_embed()
    th=df.loc[country]
    
    
    def pie_each_country_lei() -> Pie:
        ss=Counter([i for i in th['catename'].fillna('未分类')])
        lei=[k for k,v in ss.items()]
        count=[v for k,v in ss.items()]
        c = (
            Pie()
            
            .add(
                "",
                [list(z) for z in zip(lei, count)],
                radius=["35%", "75%"],
                center=["50%", "50%"],
                rosetype="area",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-"+str(country)+"景观/目的地类别示例"))
        )
        return c.render_embed()
    px = th['position_x']
    py = th['position_y']
    pt = [i for i in th['en_destination']]
    pc = th['count']
    x=[i for i in px]
    y=[i for i in py]
    ptc=[i for i in th['cn_destination']]
    ptt=[str(ptc[i])+str(pt[i]) for i in range(len(ptc))]
    
  
    fig = go.Figure(go.Densitymapbox(
        name=str(country)+'热力图',
        lat=px,
        lon=py,
        z=pc,
        radius=25,
        text=ptt))

    fig.update_layout(
        title=str(country)+'热力图',
        paper_bgcolor='rgba(170,95,134,1)',
        plot_bgcolor='rgba(170,95,134,1)',
        mapbox=dict(
            style='outdoors',
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=float(x[0]),
                lon=float(y[0]),
            ),
            pitch=0,
            zoom=4
        ),
    )
    
    data = [
    go.Scattermapbox(
        name=str(country)+'散点图',
        lat=px,
        lon=py,
        mode='markers',
        marker=dict(
            size=9
        ),
        
        text=ptt,
    )]
 
    layout1 = go.Layout(
    title=str(country)+'散点图',
    autosize=True,
    hovermode='closest',
    paper_bgcolor='rgba(170,95,134,1)',
    plot_bgcolor='rgba(170,95,134,1)',
        mapbox=dict(
        style='outdoors',
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=float(x[0]),
            lon=float(y[0])
            ),
            pitch=0,
            zoom=4
        ),
    )
 
    fig1 = dict(data=data, layout=layout1)



    div1=plot(fig,output_type="div")
    div2=plot(fig1,output_type="div")
    html1=bar_each_visited()
    html2=bar_each_place()
    html3=pie_each_country_lei()
    each_sea_text=minding.each_sea[country]

    html='''{% extends 'base.html' %}
    {% block body %}
    '''+'''
    <div class='daxiao'>
    {div1}
    </div>
    <div class='daxiao'>
    {div2}
    </div>
    <div class='each_country'>
    {html1}
    </div>
    <div class='each_country'>
    {html2}
    </div>
    <div class='each_country'>
    {html3}
    </div>
    <div class='font'>
    {each_sea_text}
    </div>



    '''.format(div1=div1,div2=div2,html1=html1,html2=html2,html3=html3,each_sea_text=each_sea_text)+'''
    {% endblock %}
    '''
    with open(dir_path+'/templates/'+str(country)+'.html','w',encoding='utf-8') as f:
        f.write(html)
    
    return render_template(str(country)+'.html')



if __name__ == '__main__':
    app.run(debug=True)
    
