from flask import Flask, render_template, request, redirect, session, flash
from weather_util import get_weather, get_weather_by_coord
from holiday_util import holiday
import crawl_util as cu
import map_util as mu
import image_util as iu
import os, random, json
from datetime import datetime
from user_module.user import user_bp

app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'

app.register_blueprint(user_bp, url_prefix='/user')

# flask 2.3 에서는 이 코드만 사용 가능
""" with app.app_context():
    global quote, quotes           # quote, quotes 변수를 전역 변수로 만들어 줌
    global addr
    filename = os.path.join(app.static_folder, 'data/QuoteEnVer.txt')
    with open(filename, encoding='utf-8') as f:
        quotes = f.readlines()
    addr = '수원시 장안구' """

@app.before_first_request
def before_first_request():
    global quote, quotes           # quote, quotes 변수를 전역 변수로 만들어 줌
    global addr
    global ymd, hh, now
    filename = os.path.join(app.static_folder, 'data/QuoteEnVer.txt')
    with open(filename, encoding='utf-8') as f:
        quotes = f.readlines()
    quote = random.sample(quotes, 1)[0]
    session['quote'] = quote
    addr = '수원시 장안구'
    session['addr'] = addr
    now = datetime.now()
    ymd = now.strftime('%Y-%m-%d')
    hh = now.strftime('%H')

@app.route('/change_quote')
def change_quote():
    global quote
    quote = random.sample(quotes, 1)[0]
    session['quote'] = quote
    return quote

@app.route('/change_addr')
def change_addr():
    global addr
    addr = request.args.get('addr')
    session['addr'] = addr
    return addr

@app.route('/weather')
def weather():
    addr = request.values['addr']
    lat, lng = mu.get_coord(addr + '청')
    html = get_weather_by_coord(app, lat, lng)
    return html

@app.route('/change_profile', methods=['POST'])
def change_profile():
    file_image = request.files['image']
    filename = os.path.join(app.static_folder, f'upload/{file_image.filename}')
    print(filename)
    file_image.save(filename)
    mtime = iu.change_profile(app, filename)
    return str(mtime)

@app.route('/')
def home():
    menu = {'ho':1, 'us':0, 'api':0, 'cr':0, 'ai':0, 'sc':0}
    return render_template('home.html', menu=menu, weather=get_weather(app),
                           quote=quote, addr=addr)

@app.route('/user')
def user():
    try:
        _ = session['uid']
    except:
        flash('사용자 정보를 확인하기 위해 먼저 로그인 하세요')
        return redirect('/user/login')
    
    menu = {'ho':0, 'us':1, 'api':0, 'cr':0, 'ai':0, 'sc':0}
    return render_template('user/user.html', menu=menu, weather=get_weather(app),
                           quote=quote, addr=addr)

@app.route('/interpark')
def interpark():
    menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
    book_list = cu.interpark()
    return render_template('interpark.html', menu=menu, weather=get_weather(app),
                           book_list=book_list, quote=quote, addr=addr, ymd=ymd, hh=hh)

@app.route('/genie')
def genie():
    menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
    music_list = cu.genie()
    return render_template('genie.html', menu=menu, weather=get_weather(app),
                           music_list=music_list, quote=quote, addr=addr, ymd=ymd, hh=hh)

@app.route('/genie_jquery')
def genie_jquery():
    menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
    music_list = cu.genie()
    return render_template('genie_jquery.html', menu=menu, weather=get_weather(app),
                           music_list=music_list, quote=quote, addr=addr, ymd=ymd, hh=hh)

@app.route('/siksin', methods=['GET', 'POST'])
def siksin():
    if request.method == 'GET':
        menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
        return render_template('siksin.html', menu=menu, weather=get_weather(app),
                               quote=quote, addr=addr)
    else:
        place = request.form['place']
        menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
        food_list = cu.siksin(place)
        return render_template('siksin.html', menu=menu, weather=get_weather(app),
                               food_list=food_list, quote=quote, addr=addr)

@app.route('/hotplaces', methods=['GET', 'POST'])
def hotplaces():
    if request.method == 'GET':
        menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
        return render_template('hotplaces.html', menu=menu, weather=get_weather(app),
                                quote=quote, addr=addr)
    else:
        place1 = request.form['place1']
        place2 = request.form['place2']
        place3 = request.form['place3']
        places = [place1, place2, place3]

        mu.hot_places(places, app)

        menu = {'ho':0, 'us':0, 'api':0, 'cr':1, 'ai':0, 'sc':0}
        return render_template('hotplaces.html', menu=menu, weather=get_weather(app),
                                quote=quote, addr=addr)

@app.route('/schedule')
def schedule():
    try:
        _ = session['uid']
    except:
        flash('스케쥴을 확인하기 위해 먼저 로그인 하세요')
        return redirect('/user/login')
    
    menu = {'ho':0, 'us':0, 'api':0, 'cr':0, 'ai':0, 'sc':1}
    return render_template('schedule.html', menu=menu, weather=get_weather(app),
                           quote=quote, addr=addr, ymd=ymd)

@app.route('/schedule_js')
def schedule_js():
    try:
        _ = session['uid']
    except:
        flash('스케쥴을 확인하기 위해 먼저 로그인 하세요')
        return redirect('/user/login')
    
    holidays = holiday()
    menu = {'ho':0, 'us':0, 'api':0, 'cr':0, 'ai':0, 'sc':1}
    return render_template('schedule_js.html', menu=menu, weather=get_weather(app),
                           quote=quote, addr=addr, ymd=ymd, holidays=holidays)

if __name__ == '__main__':
    app.run(debug=True)