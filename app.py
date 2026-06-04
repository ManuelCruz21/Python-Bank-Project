import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models.database import SessionLocal, ContaDB

app = Flask(__name__)
# Vai buscar a secret key definida no teu .env, ou usa uma padrão de segurança
app.secret_key = os.getenv("SECRET_KEY", "chave-secreta-padrao")

# 🏠 Rota Principal: Carrega a página e mostra as contas gravadas no Supabase
@app.route('/')
def index():
    db = SessionLocal()
    # Faz uma consulta (Query) ao Supabase para trazer todas as contas
    contas = db.query(ContaDB).all()
    db.close()
    return render_template('dashboard.html', contas=contas)

# ➕ Rota para Criar Conta: Processa o formulário enviado pelo HTML
@app.route('/criar-conta', methods=['POST'])
def criar_conta():
    numero = request.form.get('numero')
    titular = request.form.get('titular')
    
    db = SessionLocal()
    try:
        # Cibersegurança & Regra de Negócio: Garante que não há números duplicados
        conta_existente = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if conta_existente:
            flash("Erro: Uma conta com esse número já existe!", "error")
            return redirect(url_for('index'))
            
        # Adiciona a nova conta na nuvem (Supabase) com saldo inicial a 0
        nova_conta = ContaDB(numero=numero, titular=titular, saldo=0.00)
        db.add(nova_conta)
        db.commit()
        flash("Conta criada com sucesso e guardada no Supabase!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro ao ligar ao servidor: {str(e)}", "error")
    finally:
        db.close()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)