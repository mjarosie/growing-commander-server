from growing_commander_server import app
import growing_commander_server.views.app

if __name__ == "__main__":
    if 'CERT_PATH' in app.config and 'KEY_PATH' in app.config:
        app.run(host='0.0.0.0', ssl_context=(app.config['CERT_PATH'], app.config['KEY_PATH']))
    else:
        app.run(host='0.0.0.0')
