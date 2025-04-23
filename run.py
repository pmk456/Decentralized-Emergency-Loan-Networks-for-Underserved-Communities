from app import create_app
import os
app = create_app()
app.config['SECRET_KEY'] = os.urandom(32)

print("Please Run Create Database if database not exists!")

if __name__ == '__main__':
    app.run("0.0.0.0", port=2001, debug=True)
