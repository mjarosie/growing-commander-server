from source import app, db
import source.views

if __name__ == "__main__":
    if 'CERT_PATH' in app.config and 'KEY_PATH' in app.config:
        app.run(ssl_context=(app.config['CERT_PATH'], app.config['KEY_PATH']))
    else:
        app.run()
