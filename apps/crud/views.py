from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user  # type: ignore

from apps.app import db
from apps.crud.forms import UserForm
from apps.crud.models import User

crud = Blueprint(
      "crud",
      __name__,
      static_folder="static",
      template_folder="templates",
)

@crud.route("/")
@login_required
def index():
      return render_template("crud/index.html")

# 사용자 신규 등록을 위한 엔드포인트 작성
@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserForm 클래스를 인스턴스화
    form = UserForm()
    if form.validate_on_submit():  # submit 클릭시 검증에 문제가 없는 경우.
        # 사용자 정보 생성
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # DB작업으로 사용자를 추가하고 커밋
        db.session.add(user)
        db.session.commit()

        # 사용자 일람 화면으로 리다이렉트
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

# 사용자 편집을 위한 엔드포인트 작업
@crud.route("/users/<user_id>", methods=["GET","POST"])
@login_required
def edit_user(user_id):
    form = UserForm()
    
    # User 모델을 이용하여 사용자를 취득
    user = User.query.filter_by(id=user_id).first()
    
    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트
    if form.validate_on_submit():   # post 메서드로 수정 정보가 들어온 경우
        # 수정 내용을 적용
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        # DB에 적용
        db.session.add(user)  # primary_key의 값이 있는 경우 수정, 없으면 생성
        db.session.commit()
        return redirect(url_for('crud.users'))   # 수정 완료. 일람으로 이동
    
    # GET으로 접근한 경우 HTML을 반환
    return render_template("crud/edit.html", user=user, form=form)

# 사용자 일람을 위한 엔드포인트 작업
@crud.route("/users")
@login_required
def users():
    """사용자 일람을 얻는 함수"""
    # users = db.session.query(User).all()
    users = User.query.all()
    return render_template("crud/index.html", users=users)

# 사용자 삭제를 위한 엔드포인트 작업
@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
      user=User.query.filter_by(id=user_id).first()
      db.session.delete(user)
      db.session.commit()
      return redirect(url_for("crud.users"))

# SQL 테스트를 위한 endpoint 작성!
@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return "콘솔에서 확인해 주세요."