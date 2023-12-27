from db.model import app
from urlshort import router

app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug = True)