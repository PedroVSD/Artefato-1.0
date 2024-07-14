from flask import Flask, g, jsonify, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
from pytz import timezone
from functions import Sala, get_next_weekday, ler_planilha_excel, get_Bloco, get_Bloco_dia, reset_file

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'qualquercoisa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

oauth = OAuth(app)
db = SQLAlchemy(app)
google = oauth.register(
    name='google',
    client_id='Enter id',
    client_secret='Enter secret id',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

class Solititacao(db.Model):
    numero_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    Bloco = db.Column(db.String(150), nullable=False)
    Sala = db.Column(db.String(150), nullable=False)
    Hora = db.Column(db.String(25), nullable=False)
    Dia = db.Column(db.String(45), nullable=False)
    couteudo = db.Column(db.String(150), nullable=False)
    aprovado = db.Column(db.Integer, nullable=False)

    def __init__(self, id, email, Bloco, Sala, hora, dia, couteudo, aprovado=0):
        self.id = id
        self.email = email
        self.Bloco = Bloco
        self.Sala = Sala
        self.Hora = hora
        self.Dia = dia
        self.couteudo = couteudo
        self.aprovado = 0

class Admins(db.Model):
    email = db.Column(db.String(150), nullable=False, primary_key=True)
    dia = db.Column(db.String(10), nullable=False)
    responsavel = db.Column(db.String(150), nullable=False)


    def __init__(self,email, dia, responsavel):
        self.email = email
        self.dia = dia
        self.responsavel = responsavel


#GOOGLE LOGIN
@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    if google is not None:
        return google.authorize_redirect(redirect_uri, prompt='consent')
    return ''

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    if google is not None:
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
        user_info = resp.json()
        user = google.userinfo()  # uses openid endpoint to fetch user info

        domain = user_info['email'].split('@')[1]
        if domain != 'ufrrj.br':    
            return  '<script> alert("Acesso negado: você deve usar um email @ufrrj.br.");window.location.href = "/";</script>'
    
    
    if Admins.query.filter_by(email=user_info['email']).first() is not None:
        session['confirm'] = user_info
        return render_template('Confirm.html')

    session['profile'] = user_info
    return redirect('/Profile')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('profile', None)
    session.pop('admin', None)
    return redirect('/')
#FIM GOOGLE LOGIN





#Pagina Principal
@app.route("/")
def Index():
    return render_template("Index.html")

#Parte do ADMIN
@app.route("/Confirm", methods=['POST', 'GET'])
def Confirm():
    if 'confirm' in session:
        confirmation = request.form.get('confirmation')
        if confirmation == 'yes':
            session['admin'] = session['confirm']
            session.pop('confirm', None)
            return redirect('/Admin')
        
        session['profile'] = session['confirm']
        session.pop('confirm', None)
        return redirect('/Profile')
    return '<script> alert("Acesso negado");window.location.href = "/logout";</script>'

#Pagina Admin
@app.route("/Admin")
def Admin():
    if 'admin' in session:
        nome = session['admin']['given_name']
        nome = nome.capitalize()
        return render_template("Admin.html", nome = nome)
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Mostra as solicitações
@app.route("/Solicitacoes")
def Solicitacoes():
    if 'admin' in session:
        solititacoes = Solititacao.query.all()
        nome = session['admin']['given_name']
        nome = nome.capitalize()
        return render_template("Consulta_Admin.html", users=solititacoes, nome=nome)
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Aprova as solicitações
@app.route("/Aprovar", methods=['POST', 'GET'])
def Aprovar():
    if 'admin' in session:
        if request.method == 'POST':
            numero_pedido = request.form.get('id')
            solicitacao = Solititacao.query.filter_by(numero_pedido=numero_pedido).first()

            if solicitacao:
                # Set all requests with the same day as not approved
                Solititacao.query.filter_by(Dia=solicitacao.Dia, Bloco=solicitacao.Bloco, Sala=solicitacao.Sala, Hora=solicitacao.Hora).update({"aprovado": 2})
                solicitacao.aprovado = 1
                db.session.commit()
            return redirect('/Solicitacoes')
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Rejeita as solicitações
@app.route("/Rejeitar", methods=['POST', 'GET'])
def Rejeitar():
    if 'admin' in session:
        if request.method == 'POST':
            numero_pedido = request.form.get('id')
            solicitacao = Solititacao.query.filter_by(numero_pedido=numero_pedido).first()

            if solicitacao:
                solicitacao.aprovado = 2
                db.session.commit()
            return redirect('/Solicitacoes')
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Fim Parte do ADMIN


#Pagina Profile
@app.route("/Profile")
def Profile():
    if 'profile' in session:
        nome = session['profile']['given_name']
        nome = nome.capitalize()
        return render_template("Profile.html", nome=nome)
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Pagina Agendar
@app.route("/Agendar")
def Agendar():
    if 'profile' in session:
        #db.session.query(Solititacao).delete()
        #db.session.commit()
        return render_template("Agendar.html") 
    return redirect('/')

#Leva os dados para Agendar
@app.route('/get_salas', methods=['POST'])
def get_salas():
    if 'profile' in session:
        bloco = None
        if request.json is not None:
            bloco = request.json.get('bloco')
        dado = ler_planilha_excel(bloco, False, True)
        return jsonify(dado)
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Salva os dados do Agendamento
@app.route("/Confirmar", methods=['POST', 'GET'])
def Confirmar():
    if 'profile' in session:        
        if request.method == 'POST':
            email = session['profile']['email']
            bloco = request.form.get('bloco')
            objetivo = request.form.get('observacoes')
            pedido = request.form.get('sala')
            if pedido is not None:
                sala, hora = pedido.split(' ')
                print(sala, hora)
            dia = request.form.get('dia_semana')
            dia = get_next_weekday(dia)
            id = Solititacao.query.filter_by(email=email).count()+1
            solicitacao = Solititacao(id=id, email=email, Bloco=bloco, Sala=sala, hora=hora, dia=dia, couteudo=objetivo, aprovado=0)
            db.session.add(solicitacao)
            db.session.commit()

            return '<script> alert("solicitação enviado com sucesso!");window.location.href = "/Agendar";</script>'
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

#Pagina de Consulta
@app.route("/Consulta")
def Consulta():
    if 'profile' in session:
        solititacoes = Solititacao.query.filter_by(email=session['profile']['email']).all()
        nome = session['profile']['given_name']
        nome = nome.capitalize()
        return render_template("Consulta.html", users=solititacoes, nome=nome)
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'

# Pagina dos blocos
@app.route("/Blocos/", methods=['POST', 'GET'])
def Blocos():
    if 'profile' in session:

        dia_atual = datetime.today().weekday()
        hora_atual = datetime.now(timezone('America/Sao_Paulo')).strftime("%H")
        hora_atual = int(hora_atual)

        dia = request.args.get('dia')
        bloco = request.args.get('bloco')

        if(bloco):
            bloco = bloco.upper()
            if(bloco not in ['A', 'B', 'M', 'I']):
                redirect('/Blocos')

            if(dia is None or int(dia) < 0 or int(dia) > 4):  
                dados, dia = get_Bloco(bloco)
            else:
                dia = int(dia)
                dados = get_Bloco_dia(bloco, dia)

        else:
            dados, dia = get_Bloco('A')

        return render_template('Blocos.html', dados=dados, hora = 8, dia = dia, atual = dia_atual)
        
    return '<script> alert("Acesso negado: você deve estar logado para acessar esta página.");window.location.href = "/logout";</script>'








@app.before_request
def create_tables():
    # EstaA linha remove a marcação que indica que a função create_tables seja chamada
    # a cada request, fazendo com que ela seja chamada apenas no primeiro request
    app.before_request_funcs[None].remove(create_tables)

    # Cria a base de dados
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
