# -*- coding: utf-8 -*-
import time

HTML_TEMPLATE = '''
<!DOCTYPE html>
<head>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
  <style>
body{
  background-color: #dedede;
}
.gallery{
  display: flex;
  width: 900px;
  margin: auto;
  justify-content: space-between;
  flex-wrap: wrap;
}
figure{
  width: 200px;
  margin: 8px 0;
  border: 1px solid #777;
  padding: 8px;
  box-sizing: border-box;
  background-color: #fff;
}
figure img{
  width: 100%;
}
figure figcaption{
  text-align: center;
  padding: 8px 4px;
}
.center {
    text-align: center;
}
  </style>
</head>
<body>
%BODY%
</body>
</html>
'''

ITEM_TEMPLATE = '''
<div class="gallery">
<h1>%TITLE%</h1>
%GALLERY%
</div>
<div class="center">
%DETAIL%
<a href="%URL%">網址：%URL%</a>
<div>
'''

GALLERY_TEMPLATE = '''
<figure><img src="%IMG%"/></figure>
'''

DETAIL_TEMPLATE = '''
<p>%TEXT%</p>
'''

WEB_URL_FORMAT_STR = "https://rent.591.com.tw/rent-detail-{}.html"


def render(houses, output='temp.html'):
    items = ''
    for house in houses:
        gallery = ''
        title = "名稱：{}-{}-{}".format(
                house['region_name'],
                house['section_name'],
                house['fulladdress'],
            )
        
        for url in house['img_url']:
            gallery += GALLERY_TEMPLATE.replace('%IMG%', url)
            
        detail = ''
        detail += DETAIL_TEMPLATE.replace('%TEXT%', "租金：{} {}".format(house['price'], house['unit']))
        detail += DETAIL_TEMPLATE.replace('%TEXT%', "坪數：{} 坪".format(house['area']))
        detail += DETAIL_TEMPLATE.replace('%TEXT%', "格局：{}".format(house['layout']))
        detail += DETAIL_TEMPLATE.replace('%TEXT%', "更新時間：{}".format(time.ctime(house['refreshtime'])))
        
        items += ITEM_TEMPLATE.replace('%TITLE%', title).replace('%GALLERY%', gallery).replace('%DETAIL%', detail)\
            .replace('%URL%', WEB_URL_FORMAT_STR.format(house['post_id']))
    
    
    with open(output, 'w') as f:
        f.write(HTML_TEMPLATE.replace('%BODY%', items))
    
if __name__ == '__main__':
    import pickle
    houses = pickle.load( open( "save.p", "rb" ) )
    render(houses)
    