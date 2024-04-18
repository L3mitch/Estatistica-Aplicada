from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/resposta_inicio', methods=['GET'])
def resposta_inicio():
    return render_template('resposta_inicio.html', title='Resposta início')

@app.route('/resposta_inicio', methods=['POST'])
def salva_resposta_inicio():
    return {
        'success': True,
        'message': 'salva_resposta_inicio cadastradas'
    }

@app.route('/resposta_fim', methods=['GET'])
def resposta_fim():
    return render_template('resposta_fim.html', title='Resposta final')

@app.route('/resposta_fim', methods=['POST'])
def salva_resposta_fim():
    return {
        'success': True,
        'message': 'salva_resposta_fim cadastradas'
    }

@app.route('/user', methods=['GET'])
def get_user():
    return {
        'usuario': 'Nome do Usuário'
    }