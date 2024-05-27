import os 
from flask import render_template, request
from app import app
from detector import * # Isso precisa mudar, não está importando do local correto

import csv


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

@app.route('/resposta_inicio', methods=['POST'])
def salva_resposta_inicio():
    if request.method == 'POST':
        filename, fields = config_data()

        dir_name = request.form['nome'].lower().replace(' ', '')
        dir_user = 'api/training/' + dir_name
        '''os.mkdir(dir_user)
        f1 = request.files['foto1']
        f1_titulo = dir_name + '_01.' + f1.rsplit('.', 1)[1].lower()
        f1.save(dir_user, f1_titulo)
        f2 = request.files['foto2']
        f2_titulo = dir_name + '_02.' + f2.rsplit('.', 1)[1].lower()
        f2.save(dir_user, f2_titulo)
        '''
        rows = [
            [
                dir_name,
                request.form['nome'],
                request.form['idade'],
                request.form['email'],
                request.form['sexo'],
                'f1_titulo',
                'f2_titulo',
                request.form['q1_01'],
                request.form['q1_02'],
                request.form['q1_03'],
                request.form['q1_04'],
                request.form['q1_05'],
                request.form['q1_06'],
                request.form['q1_07'],
                '',
                '',
                '',
                '',
                ''
            ]
        ]

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

        adicionar_pessoa(request)
        return {
            'success': True,
            'message': 'salva_resposta_inicio cadastradas'
        }

@app.route('/resposta_fim', methods=['GET'])
def resposta_fim():
    user = request.args.get('user', default = '1')
    filename, fields = config_data()

    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["dir_name"] == user:
                fields = row
            line_count += 1

    return render_template('resposta_fim.html', title='Resposta final', u=fields)

@app.route('/resposta_fim', methods=['POST'])
def salva_resposta_fim():
    if request.method == 'POST':
        filename, fields = config_data()

        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if row["dir_name"] == request.form['dir_name']:
                    fields = row
                line_count += 1
                
        rows = [
            [
                fields['dir_name'],
                fields['name'],
                fields['age'],
                fields['email'],
                fields['sex'],
                'f1_titulo',
                'f2_titulo',
                fields['q1_01'],
                fields['q1_02'],
                fields['q1_03'],
                fields['q1_04'],
                fields['q1_05'],
                fields['q1_06'],
                fields['q1_07'],
                request.form['q2_02'],
                request.form['q2_03'],
                request.form['q2_04'],
                request.form['q2_05'],
                request.form['q2_07']
            ]
        ]

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

        return {
            'success': True,
            'message': 'salva_resposta_inicio cadastradas'
        }

@app.route('/user', methods=['GET'])
def get_user():
    return {
        'usuario': 'Nome do Usuário'
    }


def config_data():
    filename = "pesquisas.csv"
    fields = ['dir_name', 'name', 'age', 'email', 'sex', 'photo_1', 'photo_2', 'q1_01', 'q1_02', 'q1_03', 'q1_04', 'q1_05', 'q1_06', 'q1_07', 'q2_02', 'q2_03', 'q2_04', 'q2_05', 'q2_07']

    return filename, fields

@app.route('/leitura_facial', methods=['POST'])
def leitura_facial():
    id_imagem = request.form['id_imagem']
    return{
        recognize_face(id_imagem, model="hog")
    }


def adicionar_pessoa(request):
    nome = request.form['nome']
    return{
        encode_new_face(nome, model="hog")
    }