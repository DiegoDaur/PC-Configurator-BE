from flask import Flask
from flask_cors import CORS

from controller.auth_controller import auth_bp
from controller.component_controller import component_bp
from controller.compatibility_controller import compatibility_bp
from controller.build_controller import build_bp
from controller.user_controller import user_bp

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.register_blueprint(auth_bp)
app.register_blueprint(component_bp)
app.register_blueprint(compatibility_bp)
app.register_blueprint(build_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run(debug=True)
