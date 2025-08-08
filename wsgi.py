from app import rtm_app
from app.master.views import rtm_app_master_bp
from app.chats.views import rtm_app_chat_bp
from app.users.views import rtm_app_user_bp

rtm_app.register_blueprint(rtm_app_master_bp)
rtm_app.register_blueprint(rtm_app_chat_bp)
rtm_app.register_blueprint(rtm_app_user_bp)

if __name__ == '__main__':
    rtm_app.run(debug=True, host="0.0.0.0", port=5000)
