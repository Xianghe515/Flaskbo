from flask import Blueprint, render_template

from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage

# template_folder를 지정한다(static은 지정하지 않는다)
dt = Blueprint(
      "detector",
      __name__, 
      template_folder="templates"
      )

# dt 애플리케이션을 사용하여 엔드포인트를 작성한다
@dt.route("/")
def index():
      user_images = (
            db.session.query(User, UserImage)
            .join(UserImage)
            .filter(User.id == UserImage.user_id)
            .all()
      )

      return render_template("detector/index.html", user_images=user_images)