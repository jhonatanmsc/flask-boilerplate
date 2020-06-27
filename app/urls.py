from app import app
from app.controllers import default

app.add_url_rule('/', view_func=default.index)
app.add_url_rule('/register', view_func=default.register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=default.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=default.logout)
