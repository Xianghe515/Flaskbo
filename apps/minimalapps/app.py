import logging
import os

from email_validator import EmailNotValidError, validate_email
# Flask 클래스를 import
from flask import (Flask, current_app, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# Flask 클래스를 인스턴스화
app = Flask(__name__)
# __name__ 변수의 값 출력
print(__name__)

'''
import random
import string

# 소스 생성
string_pool = string.ascii_letters+string.digits

# 비밀 키 생성
result=""
for i in range(20):
    result += random.choice(string_pool)
print(result)           dVmWZSOfLUdq4Hs0n1E1
'''
# 비밀 키 추가 - 세션을 위해 필요
app.config['SECRET_KEY'] = 'dVmWZSOfLUdq4Hs0n1E1'

# 로그 레벨 설정
app.logger.setLevel(logging.DEBUG)

# 로그 출력을 위해 다음과 같이 지정
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

# 리다이렉트를 중단하지 않도록 함
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtension에 애플리케이션을 설정(debugtoolbar 연동 처리)
toolbar = DebugToolbarExtension(app)

# Mail 클래스의 config 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록
mail = Mail(app)

# 맵핑 - @app.route()
@app.route("/", endpoint="root")
def hello_world():
    return "<h1>Hello, Flask!</h1>"


# 허가할 HTTP 메소드 지정(@app.route() 데코레이터의 method 옵션)
@app.route("/hello/<name>/<int:out>", methods=["GET", "POST", "PUT"], endpoint="hello")
def hello(name, out):
    # return f"Hello, {name}"
    # 템플릿 엔진 적용
    dic = {"name": name, "age": 20, "out": bool(out)}
    # for문을 사용하기 위한 값 생성
    dataList = []   # user.url, user.username
    for i in range(10):
        user = {}
        user['url'] = f"http://localhost{i}"
        user['name'] = f"testUser{i}"
        dataList.append(user)
        user = {}
    print(dataList)
    return render_template("index.html", data=dic, datas=dataList)


# app.get(), app.post()         *Flask 2.0 이후 생긴 데코레이터
@app.get("/test", endpoint="getTest")
def testGet():
    return "<h3>testGet</h3>"


@app.post("/test", endpoint="postTest")
def testPost():
    return "<h3>testPost</h3>"


@app.put("/test", endpoint="putTest")
def testPut():
    return "<h3>putTest</h3>"


# (연습) uri 주소가 /info인 경로에 이름과 나이를 입력 받아서 그 결과를 출력하는 플라스크 맵핑 함수 작성
# (method, endpoint는 자유)
@app.route("/info/<string:name>/<int:age>", endpoint="info")
def info(name, age):
    print(type(name), type(age))
    result = f"""<div>
    <h3>info</h3>
    <table border="1">
        <tr><th style="width:100px">이름</th>
        <tr><th style="width:100px">나이</th></tr>
        <tr><td>{name}</td><td>{age}살</td></tr>
    </table>
    </div>"""
    return result


# test_request_context()
with app.test_request_context():
    # /
    print('주소 url_for("root") : ', url_for("root"))     # 주소를 알아오는 함수
    # /test
    print('주소 url_for("putTest") : ', url_for("putTest"))
    # /hello/<name>/<int:out>
    print("hello : ", url_for("hello", name="test", out=1))
    # /hello/test/1?page=1&age=10
    print("hello : ", url_for("hello", name="test", out=1, page=1, age=10))
    # /info/홍길동/19
    print(url_for("info", name="testname", page=1, age=19))
    '''
    http://127.0.0.1:5000/hello/test/1?page=1&age=10
    http:// : 프로토콜
    127.0.0.1 : 서버 주소(도메인 정보)
    5000 : 서버의 포트 주소
    /hello/test/1 : 어플리케이션(앱, 프로그램)
    ?page=1&age=10 : 어플리케이션에 전달할 인자값
        └? - 어플리케이션과 인자값 구분     page=1, age=10
        └& - 전달한 값들을 구분
    '''

# 애플리케이션 컨텍스트
# 여기서 호출하면 오류 생김 -> 직접 참조는 불가함
# print(current_app)    *RuntimeError: Working outside of application context.

# 애플리케이션 Context를 취득하여 stack 영역에 push
ctx = app.app_context()     # 현재 동작 중인 app의 context를 ctx라는 변수에 저장
ctx.push()                  # stack에 저장
print(current_app.name)     # └위 과정을 거친 이후 접근 가능

# 전역 임시 영역에 값 설정 : g(g를 사용하기 위해서는 current_app이 로드되어 있어야 함)
g.connection = "connection" # connection 정보를 사용하는 내용은 db접근 정보
print(g.connection)

# 요청 컨텍스트
print('요청 컨텍스트 테스트')
with app.test_request_context("/users?updated=true&test=test입니다."):
    # 테스트 결과 출력
    print(request.args.get("updated"))
    print(request.args.get("test"))
    print(request.args)
    
    
@app.route("/contact")
def contact():
    # 응답 객체를 취득
    response = make_response(render_template("contact.html", username=session["username"]))
    
    # 쿠키 설정
    response.set_cookie("flaskbook key", "flaskbook value")
    
    # 세션 설정
    session["username"] = "xianghe"
    
    # 응답 오브젝트 반환
    return response
#    return render_template("contact.html")      # templates 내 contact.html을 렌더링하여 보내겠음

@app.route("/contact_complete", methods=['GET', 'POST'])
def contact_complete():
    if request.method == "POST":
        # request를 통해 전달된 값 처리 : form 태그로부터 전달받은 값
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']
#        print("username : ", username)
#        print("email : ", email)
#        print("description : ", description)
        
        # 입력값 확인(값이 있는지, 이메일 형식이 맞는지 등)
        is_valid = True
        if not username:
            flash("사용자 명은 필수입니다.")
            is_valid = False
        if not email:
            flash("메일 주소는 필수입니다.")
            is_valid = False
        
        # 주소 형식 검증
        try:
            validate_email(email)
        except:
            flash("메일 주소 형식으로 입력해주세요.")
            is_valid = False
        
        if not description:
            flash("문의 내용은 필수입니다.")
            is_valid = False
        
        # 검증 실패 시 (is_valid = False) ➜ 문의 폼으로 되돌림
        if not is_valid:
            app.logger.warning("입력값 검증에 실패입니다.")
            return redirect("contact")
        
        # 이메일을 발송하기 위한 작업 진행
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description
        )
        
        
        # contact 엔드 포인트로 리다이렉트 처리
        flash("문희해주셔서 나문희")
        app.logger.info("정상적으로 문의 메일을 발송했습니다.")
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

# 메일 발송과 관련된 함수
def send_email(to, subject, template, **kwargs):
    '''메일을 송신하는 함수'''
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
