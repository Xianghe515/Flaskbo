# from pathlib import Path
from flask import Flask
from flask_login import LoginManager  # type:ignore
from flask_migrate import Migrate  # type:ignore
from flask_sqlalchemy import SQLAlchemy
# flask-wtf 모듈의 CSRFProtect import
from flask_wtf.csrf import CSRFProtect  # type:ignore

from apps.config import config

# 인스턴스화
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message =""

def create_app(config_key):
      app = Flask(__name__)
      app.config.from_object(config[config_key])
      # app.config.from_mapping(
      #       SECRET_KEY="dVmWZSOfLUdq4Hs0n1E1",
      #       SQLALCHEMY_DATABASE_URI=
      #             f"sqlite:///{Path(__file__).parent / 'local.sqlite'}",
      #       SQLALCHEMY_TRACK_MODIFICATIONS=False,
      #       # SQL 콘솔 로그에 출력
      #       SQLALCHEMY_ECHO=True,
      #       WTF_CSRF_SECRET_KEY="El1oD921KMdGKONsydDa"
      # )
      
      csrf.init_app(app)
      
      db.init_app(app)
      
      Migrate(app, db)
      
      # login_manager를 애플리케이션과 연계
      login_manager.init_app(app)
      from apps.crud import views as crud_views
      
      app.register_blueprint(crud_views.crud, url_prefix="/crud")
      
      # AUTH 패키지로부터 views 모듈을 import
      from apps.auth import views as auth_views

      # register_blueprint()로 blueprint 등록
      app.register_blueprint(auth_views.auth, url_prefix="/auth")
      
      # 이제부터 작성하는 detector 패키지로부터 views를 import
      from apps.detector import views as dt_views

      # register_blueprint를 사용해 views의 dt를 앱에 등록
      app.register_blueprint(dt_views.dt)
            
      return app

