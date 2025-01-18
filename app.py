from flask import Flask, render_template, request, redirect, url_for, Response, abort
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料庫模型
class RSSItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  # 新增圖片 URL 欄位


# 初始化資料庫
def init_db():
    with app.app_context():
        db.create_all()


# 隨機下載圖片
def get_random_image():
    try:
        # 使用 Lorem Picsum API 來獲取隨機圖片
        response = requests.get("https://picsum.photos/1600/900", allow_redirects=True)
        if response.status_code == 200:
            return response.url  # 返回圖片的最終 URL
    except Exception as e:
        print(f"下載圖片失敗: {e}")
    return None  # 如果獲取失敗，返回 None


# 主頁：新增 RSS 項目
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            abort(400, "標題或內容不能為空")

        # 隨機獲取圖片
        image_url = get_random_image()

        # 創建新 RSS 項目
        new_item = RSSItem(title=title, content=content, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('index'))

    items = RSSItem.query.order_by(RSSItem.id.desc()).all()
    return render_template('index.html', items=items)


# RSS Feed 輸出
@app.route('/rss')
def rss_feed():
    items = RSSItem.query.order_by(RSSItem.id.desc()).all()

    try:
        # 創建 RSS XML
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        
        ET.SubElement(channel, 'title').text = "香港創科參考資訊分享"
        ET.SubElement(channel, 'link').text = url_for('rss_feed', _external=True)
        ET.SubElement(channel, 'description').text = "香港科研資訊匯聚的RSS"

        for item in items:
            rss_item = ET.SubElement(channel, 'item')
            ET.SubElement(rss_item, 'title').text = item.title
            ET.SubElement(rss_item, 'link').text = url_for('rss_feed', _external=True) + f"/{item.id}"
            ET.SubElement(rss_item, 'description').text = item.content

            # 如果有圖片，添加到 RSS 項目中
            if item.image_url:
                enclosure = ET.SubElement(rss_item, 'enclosure', attrib={
                    'url': item.image_url,
                    'type': 'image/jpeg'
                })

        rss_xml = ET.tostring(rss, encoding='utf-8', xml_declaration=True)
        return Response(rss_xml, mimetype='application/rss+xml')
    except Exception as e:
        abort(500, f"生成 RSS 時出錯：{str(e)}")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)