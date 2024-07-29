from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
users = {}


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
        username = request.form.get('email')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            session['user_id'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            return render_template('signup.html', error='Usuário já cadastrado')

        # Armazena o novo usuário com a senha criptografada
        hashed_password = generate_password_hash(password)
        users[email] = hashed_password

        # Salva o usuário e a senha criptografada no arquivo
        with open('users.txt', 'a') as f:
            f.write(f"{name},{email},{hashed_password}\n")

        return redirect(url_for('login'))

    return render_template('signup.html')


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
