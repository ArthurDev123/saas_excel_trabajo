import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from supabase import create_client, Client
from datetime import datetime
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jobhunter-secret-key-2024')

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY', supabase_key)

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    supabase = None
    print("ADVERTENCIA: Supabase no configurado. Configure las variables de entorno.")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user():
    return session.get('user')

@app.before_request
def before_request():
    g.user = get_user()

def get_ofertas(user_id):
    if not supabase:
        return []
    response = supabase.table('ofertas').select('*').eq('user_id', user_id).order('fecha_aplicacion', desc=True).execute()
    return response.data

def agregar_oferta_db(empresa, titulo, fecha_aplicacion, tipo, user_id, salario=None, observaciones=None):
    if not supabase:
        return False
    data = {
        'empresa': empresa,
        'titulo': titulo,
        'fecha_aplicacion': fecha_aplicacion,
        'tipo': tipo,
        'salario': salario,
        'observaciones': observaciones,
        'estado': 'en_espera',
        'user_id': user_id
    }
    supabase.table('ofertas').insert(data).execute()
    return True

def actualizar_estado_db(id, estado, user_id):
    if not supabase:
        return False
    supabase.table('ofertas').update({'estado': estado}).eq('id', id).eq('user_id', user_id).execute()
    return True

def eliminar_oferta_db(id, user_id):
    if not supabase:
        return False
    supabase.table('ofertas').delete().eq('id', id).eq('user_id', user_id).execute()
    return True

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('ofertas_aplicadas'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            session['user'] = {
                'id': response.user.id,
                'email': response.user.email
            }
            session['access_token'] = response.session.access_token
            return redirect(url_for('ofertas_aplicadas'))
        except Exception as e:
            flash('Email o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            flash('Cuenta creada. Por favor verifica tu email para iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error al crear cuenta. Intenta de nuevo.', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/ofertas-aplicadas')
@login_required
def ofertas_aplicadas():
    user = get_user()
    ofertas = get_ofertas(user['id'])
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('ofertas.html', ofertas=ofertas, today=today)

@app.route('/buscar-trabajo')
@login_required
def buscar_trabajo():
    portales = [
        {'nombre': 'LinkedIn', 'url': 'https://www.linkedin.com/jobs'},
        {'nombre': 'Indeed', 'url': 'https://www.indeed.com'},
        {'nombre': 'InfoJobs', 'url': 'https://www.infojobs.net'},
        {'nombre': 'Glassdoor', 'url': 'https://www.glassdoor.com'},
        {'nombre': 'Computrabajo', 'url': 'https://www.computrabajo.com'},
        {'nombre': 'Jobrapido', 'url': 'https://www.jobrapido.com'},
    ]
    return render_template('buscar.html', portales=portales)

@app.route('/agregar-oferta', methods=['POST'])
@login_required
def agregar_oferta_route():
    user = get_user()
    empresa = request.form.get('empresa')
    titulo = request.form.get('titulo')
    fecha_aplicacion = request.form.get('fecha_aplicacion')
    tipo = request.form.get('tipo')
    salario = request.form.get('salario')
    observaciones = request.form.get('observaciones')
    
    if agregar_oferta_db(empresa, titulo, fecha_aplicacion, tipo, user['id'], salario, observaciones):
        flash('Oferta agregada correctamente', 'success')
    else:
        flash('Error al agregar oferta. Configure Supabase.', 'danger')
    
    return redirect(url_for('ofertas_aplicadas'))

@app.route('/actualizar-estado/<int:id>', methods=['POST'])
@login_required
def actualizar_estado_route(id):
    user = get_user()
    nuevo_estado = request.form.get('estado')
    if actualizar_estado_db(id, nuevo_estado, user['id']):
        flash('Estado actualizado', 'success')
    return redirect(url_for('ofertas_aplicadas'))

@app.route('/eliminar-oferta/<int:id>', methods=['POST'])
@login_required
def eliminar_oferta_route(id):
    user = get_user()
    if eliminar_oferta_db(id, user['id']):
        flash('Oferta eliminada', 'success')
    return redirect(url_for('ofertas_aplicadas'))

if __name__ == '__main__':
    app.run(debug=True)
