import os, base64, sqlite3, hashlib

from flask import render_template, request, redirect
from app import app
from detector import *

api_path = ""
if os.environ.get("FLASK_DEBUG") == '1':
    api_path = "api/"

db_file = "pesquisas.db"
try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS pesquisas (
        id INTEGER PRIMARY KEY,
        dir_name TEXT NULL,
        name TEXT NULL,
        age TEXT NULL,
        email TEXT NULL,
        sex TEXT NULL,
        photo_1 TEXT NULL,
        empresa TEXT NULL,
        q1_01 TEXT NULL,
        q1_02 TEXT NULL,
        q1_03 TEXT NULL,
        q1_04 TEXT NULL,
        q1_05 TEXT NULL,
        q2_01 TEXT NULL,
        q2_02 TEXT NULL,
        q2_03 TEXT NULL,
        q2_04 TEXT NULL,
        q2_05 TEXT NULL
    )
    """
    cursor.execute(create_table_query)
except sqlite3.Error as e:
    print(f"Error: {e}")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/resposta_inicio', methods=['GET'])
def resposta_inicio():
    return render_template('resposta_inicio.html', title='Home')

@app.route('/leitura', methods=['GET'])
def leitura():
    return render_template('leitura.html', title='Leitura Facial')

@app.route('/qrcode', methods=['GET'])
def qrcode():
    usuarios = buscar_pessoas()
    return render_template('qrcode.html', title='Leitura Facial', usuarios=usuarios)

@app.route('/resposta_inicio', methods=['POST'])
def salva_resposta_inicio():
    if request.method == 'POST':

        file_name = request.form['nome'].lower().replace(' ', '')
        dir_user = api_path + 'training/' + file_name
        if not os.path.exists(dir_user) :
            os.mkdir(dir_user)

        f1_titulo = file_name + '_01.jpg'
        with open(dir_user + '/' + f1_titulo, "wb") as fh:
            fh.write(threatPhoto(request))
        f2_titulo = file_name + '_02.jpg'
        with open(dir_user + '/' + f2_titulo, "wb") as fh:
            fh.write(threatPhoto(request))

        adicionar_pesquisa(file_name, f1_titulo, request)
        adicionar_pessoa(file_name)
        return {
            'success': True,
            'message': 'salva_resposta_inicio cadastradas'
        }

@app.route('/resposta_fim', methods=['GET'])
def resposta_fim():
    user = request.args.get('user', default = 'null')
    usuario = busca_pesquisa(user)

    if (not usuario):
        return redirect("/", code=302)

    return render_template('resposta_fim.html', title='Resposta final', u=usuario)

@app.route('/resposta_fim', methods=['POST'])
def salva_resposta_fim():
    if request.method == 'POST':
        atualizar_pesquisa(request)
        return {
            'success': True,
            'message': 'salva_resposta_inicio cadastradas'
        }


@app.route('/leitura_facial', methods=['POST'])
def leitura_facial():
    id_imagem = request.form['user_photo']
    file_name = hashlib.md5(id_imagem.encode()).hexdigest()
    dir_user = api_path + 'match/' 

    f1_titulo = file_name + '.jpg'
    with open(dir_user + '/' + f1_titulo, "wb") as fh:
        fh.write(threatPhoto(request))

    nome = recognize_face(file_name, model="hog")
    if (nome):
        return {"usuario": nome}
    
    return False

@app.route('/graficos', methods=['GET'])
def graficos():
    refresh = request.args.get('refresh', default = '1')

    return render_template('x_graficos.html', title='Resposta final', r=busca_grafico(), refresh=refresh)

def adicionar_pessoa(file_name):
    return{
        encode_new_face(file_name, model="hog")
    }

def threatPhoto(request):
    userPhoto = request.form['user_photo'].replace('data:image/png;base64,', '');
    return base64.b64decode(userPhoto)

def busca_pesquisa(pesquisa):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql = "SELECT * FROM pesquisas WHERE dir_name = '"+pesquisa+"'"
        cursor.execute(sql)

        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error: {e}")

def busca_grafico():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql = """SELECT 
                    SUM(case when (q1_01 = 'S') THEN 1 else 0 end) as q1_01_s,
                    SUM(case when (q1_02 = 'S') THEN 1 else 0 end) as q1_02_s,
                    SUM(case when (q1_03 = 'S') THEN 1 else 0 end) as q1_03_s,
                    SUM(case when (q1_04 = 'S') THEN 1 else 0 end) as q1_04_s,
                    SUM(case when (q1_05 = 'S') THEN 1 else 0 end) as q1_05_s,
                    SUM(case when (q1_01 = 'N') THEN 1 else 0 end) as q1_01_n,
                    SUM(case when (q1_02 = 'N') THEN 1 else 0 end) as q1_02_n,
                    SUM(case when (q1_03 = 'N') THEN 1 else 0 end) as q1_03_n,
                    SUM(case when (q1_04 = 'N') THEN 1 else 0 end) as q1_04_n,
                    SUM(case when (q1_05 = 'N') THEN 1 else 0 end) as q1_05_n,
                    SUM(case when (q2_01 = 'S') THEN 1 else 0 end) as q2_01_s,
                    SUM(case when (q2_02 = 'S') THEN 1 else 0 end) as q2_02_s,
                    SUM(case when (q2_03 = 'S') THEN 1 else 0 end) as q2_03_s,
                    SUM(case when (q2_04 = 'S') THEN 1 else 0 end) as q2_04_s,
                    SUM(case when (q2_05 = 'S') THEN 1 else 0 end) as q2_05_s,
                    SUM(case when (q2_01 = 'N') THEN 1 else 0 end) as q2_01_n,
                    SUM(case when (q2_02 = 'N') THEN 1 else 0 end) as q2_02_n,
                    SUM(case when (q2_03 = 'N') THEN 1 else 0 end) as q2_03_n,
                    SUM(case when (q2_04 = 'N') THEN 1 else 0 end) as q2_04_n,
                    SUM(case when (q2_05 = 'N') THEN 1 else 0 end) as q2_05_n,
                    COUNT(*) AS total
                FROM pesquisas p"""
        cursor.execute(sql)

        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error: {e}")


def buscar_pessoas():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql = """SELECT dir_name, name FROM pesquisas  where q2_01=' ' order by name"""
        cursor.execute(sql)

        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error: {e}")


def adicionar_pesquisa(file_name, f1_titulo, request):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql = ''' INSERT INTO pesquisas(
                dir_name, name, age, email, sex, photo_1, empresa,
                q1_01, q1_02, q1_03, q1_04, q1_05,
                q2_01, q2_02, q2_03, q2_04, q2_05
            )
            VALUES(
                ?,?,?,?,?,?,?,
                ?,?,?,?,?,
                ?,?,?,?,?
            ) '''
        pesquisa_data = (
            file_name, request.form['nome'], request.form['idade'], request.form['email'], request.form['sexo'], f1_titulo, request.form['empresa'],
            request.form['q1_01'], request.form['q1_02'], request.form['q1_03'], request.form['q1_04'], request.form['q1_05'], 
            ' ', ' ', ' ', ' ', ' '
        )

        cursor.execute(sql, pesquisa_data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")

def atualizar_pesquisa(request):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql = ''' UPDATE pesquisas SET q2_01 = ?, q2_02 = ?, q2_03 = ?, q2_04 = ?, q2_05 = ? WHERE id = ? '''
        pesquisa_data = (
            request.form['q2_01'], request.form['q2_02'], request.form['q2_03'], request.form['q2_04'], request.form['q2_05'], request.form['id']
        )

        cursor.execute(sql, pesquisa_data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
