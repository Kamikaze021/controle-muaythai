from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def carregar_dados():
    try:
        with open('alunos.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_dados(alunos):
    with open('alunos.json', 'w') as f:
        json.dump(alunos, f, indent=4)

@app.route('/')
def index():
    alunos = carregar_dados()
    hoje = datetime.today().date()

    for aluno in alunos:
        vencimento = datetime.strptime(aluno['proximo_vencimento'], '%Y-%m-%d').date()

        if hoje >= vencimento:
            aluno['pago'] = False
        # Se ainda não venceu, mantemos como pago

    salvar_dados(alunos)
    return render_template('index.html', alunos=alunos)


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    data_pagamento = datetime.today().strftime('%Y-%m-%d')
    proximo_vencimento = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')

    novo_aluno = {
        'nome': nome,
        'pago': False,
        'ultimo_pagamento': data_pagamento,
        'proximo_vencimento': proximo_vencimento
    }
    alunos = carregar_dados()
    alunos.append(novo_aluno)
    salvar_dados(alunos)
    return redirect(url_for('index'))

@app.route('/pagar/<int:indice>')
def pagar(indice):
    alunos = carregar_dados()
    alunos[indice]['pago'] = True
    alunos[indice]['ultimo_pagamento'] = datetime.today().strftime('%Y-%m-%d')
    alunos[indice]['proximo_vencimento'] = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    salvar_dados(alunos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Iniciando servidor...")
    app.run(debug=True)

