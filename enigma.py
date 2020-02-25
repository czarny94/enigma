import json
from os import urandom, getenv

from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf.csrf import CSRFProtect

from flask_socketio import SocketIO, emit, join_room
from forms import forms
from sql import enigma_cockroachdb

RECAPTCHA_PUBLIC_KEY = getenv('RECAPTCHA_PUBLIC_KEY')  # "6LcS8MwUAAAAAHx02QRjhBWh76MGRY6E2KKS9NEM"
RECAPTCHA_PRIVATE_KEY = getenv('RECAPTCHA_PRIVATE_KEY')  # "6LcS8MwUAAAAADE4kFsBXIh3zcEa52i_jmXMwhQC"
COCKROACH_DB_URL = getenv('COCKROACH_DB_URL')  # 'localhost:26257'
COCKROACH_DB_USER = 'enigma'
COCKROACH_DB_DATABASE = 'enigma'

app = Flask(__name__)
# utworzenie losowego klucza prywatnego dla ochrony przed CSRF
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
app.testing = False


# CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)

# socketIO implementujący WebSockety
# https://socket.io/
# manage_session na false, ponieważ sesjami zarządza moduł flask-login
socketio = SocketIO(app, manage_session=True)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# połączenie z bazą danych
cockroach = enigma_cockroachdb.Cockroach(COCKROACH_DB_USER, COCKROACH_DB_URL, COCKROACH_DB_DATABASE)


@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html', mainpage_active=True)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        account = enigma_cockroachdb.Account(cockroach)
        user_data = account.check_password(form.username.data, form.password.data)
        if user_data:
            account.id = user_data[0]
            account.username = user_data[1]
            account.email = user_data[2]
            login_user(account)
            flash('Zalogowano się pomyślnie')
            # next = request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            return redirect(url_for('profil'))
        flash('niepoprawny login lub hasło')
        return redirect(url_for('login'))
    return render_template('login.html', login_active=True, form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = forms.RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            account = enigma_cockroachdb.Account(cockroach)
            is_created = account.create_account(username=form.username.data, password=form.password.data,
                                                email=form.email.data)
            if is_created:
                flash('Konto utworzone, teraz czas na wygenerowanie kluczy')
                login_user(account)
                return redirect(url_for('generate_keys'))
            else:
                flash('Konto nie zostało utworzone, prawdopodobnie taki użytkownik już istnieje')
                return redirect(url_for('register'))
        else:
            flash('prosze poprawnie uzupełnić formularz')
            return redirect(url_for('register'))
    return render_template('register.html', register_active=True, form=form)


@app.route('/profil')
def profil():
    if current_user.is_authenticated:
        key_timestamp = cockroach.session.query(enigma_cockroachdb.Keys.timestamp).filter_by(
            id=current_user.id).first()
        if key_timestamp:
            key_timestamp = key_timestamp.timestamp
        else:
            key_timestamp = "brak klucza PGP"
        return render_template('profil.html', profil_active=True, key_timestamp=key_timestamp)
    else:
        flash('zabroniony dostęp dla niezalogowanych użytkowników - najpierw się zaloguj')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('zostaleś wylogowany')
    return redirect(url_for('mainpage'))


@login_manager.user_loader
def load_user(id):
    try:
        if id is not None:
            return cockroach.session.query(enigma_cockroachdb.Account).get(id)
    except:
        cockroach.session.rollback()
    return None


@app.route('/generate_keys', methods=["POST", "GET"])
@login_required
def generate_keys():
    return render_template('generate_keys.html')


@app.route('/get_keys', methods=["POST"])
@csrf.exempt
def get_keys():
    if request.method == "POST":
        try:
            data = json.loads(request.get_data().decode())
            id = data['key']['key']['users'][0]['userId']['name']
            email = data['key']['key']['users'][0]['userId']['email']
            privateKeyArmored = data['key']['privateKeyArmored']
            publicKeyArmored = data['key']['publicKeyArmored']
            revocationCertificate = data['key']['revocationCertificate']
            timestamp = data['key']['key']['keyPacket']['created']
        except KeyError or TypeError:
            return ""
        key = enigma_cockroachdb.Keys(cockroach)
        key.add_key(id=id, email=email, private_key=privateKeyArmored,
                    public_key=publicKeyArmored, revocation_key=revocationCertificate, timestamp=timestamp)
    # zwracam pusty string, w przeciwnym razie flask zgłasza wyjątki
    return ""


@app.route('/komunikator', methods=["POST", "GET"])
def komunikator():
    if current_user.is_authenticated:
        return render_template('komunikator.html', komunikator_active=True, )
    else:
        flash('zabroniony dostęp dla niezalogowanych użytkowników - najpierw się zaloguj')
        return redirect(url_for('login'))



@socketio.on('connect', namespace='/enigma_komunikator')
def broadcast_on_connection():
    try:
        user_name = enigma_cockroachdb.Account(cockroach).get_user_name(session['_user_id'])
        username = user_name.username
        join_room(username)
        session['_user_name'] = username
        emit('server_response', {'data': '{} połączył się'.format(username)}, broadcast=True)
    except KeyError:
        pass


@socketio.on('disconnect', namespace='/enigma_komunikator')
def broadcast_on_disconnect():
    emit('server_response', {'data': session['_user_name'] + " rozłączył się"}, broadcast=True)


@socketio.on('komunikator_response', namespace='/enigma_komunikator')
def komunikator_response(message):
    if message['data'] is not "":
        emit('server_response', {'data': session['_user_name'] + ': ' + message['data']}, broadcast=True)


@socketio.on('response_to_user', namespace='/enigma_komunikator')
def response_to_user(message):
    emit('server_response',
         {'data': '{}: {}'.format(session['_user_name'], message['data'])},
         room=message['room'])


@socketio.on('response_to_user_encrypted', namespace='/enigma_komunikator')
def response_to_user_encrypted(message):
    id = enigma_cockroachdb.Account(cockroach).get_user_id(message['room'])
    privkey = enigma_cockroachdb.Keys(cockroach).get_privkey(id)
    emit('server_response_encrypted',
         {'data': '{}: '.format(session['_user_name']),
          'privkey': privkey,
          'encrypted_message': message['data']},

         room=message['room'])


@socketio.on('get_public_key', namespace='/enigma_komunikator')
def get_public_key(message):
    id = enigma_cockroachdb.Account(cockroach).get_user_id(message['data'])
    pubkey = enigma_cockroachdb.Keys(cockroach).get_pubkey(id)
    emit('public_key',
         {'data': pubkey},
         room=session['_user_name'])


def main():
    socketio.run(app, debug=True, host="0.0.0.0", port="5000")


if __name__ == '__main__':
    main()
