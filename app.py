from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__, static_folder='assets', template_folder='templates')
app.secret_key = 'supersecretkey'  # Chave secreta para gerenciar sessões

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Usuário fictício para autenticação
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Dicionário de usuários para autenticação
users = {
    'user@user.com': 'password123'  # Usuário e senha fictícios
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            session['user_id'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')
@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html')

@app.route('/financas')
@login_required
def financas():
    return render_template('financas.html')

@app.route('/reservas')
@login_required
def reservas():
    return render_template('reservas.html')

@app.route('/comunicados')
@login_required
def comunicados():
    return render_template('comunicados.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
