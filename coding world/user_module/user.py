from flask import Blueprint, request, render_template, session, redirect, flash
import hashlib, base64, json

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])        # localhost:5000/user/login 이 처리되는 곳
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        with open('static/data/password.txt') as f:
            s = f.read()
        passwords = json.loads(s)
        try:
            db_pwd = passwords[uid]
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            if hashed_pwd == db_pwd:
                flash(f'{uid} 님 환영합니다.')      # 초기 화면으로 보내줌
                session['uid'] = uid                # 세션값을 설정함으로써 사용자가 로그인하였음을 알게 해줌
                return redirect('/')
            else:
                flash('비밀번호를 다시 입력해주세요.')      # 로그인 화면을 다시 보내줌
                return redirect('/user/login')
        except:
            flash('사용자 ID를 다시 입력해주세요.')         # 회원 가입 페이지로 안내
            return redirect('/user/register')

@user_bp.route('/logout')
def logout():
    session.pop('uid', None)        # 설정한 세션값을 삭제
    return redirect('/')

@user_bp.route('/register')
def register():
    return render_template('user/register.html')

@user_bp.route('/mypage')
def mypage():
    menu = {'ho':0, 'us':0, 'api':0, 'cr':0, 'ai':0, 'sc':0}
    return render_template('user/mypage.html', menu=menu)