import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import SessionLocal, ContaDB, MovimentoDB
from decimal import Decimal
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sessao-bancaria-ultra-segura-2026")

# 🔒 DECORATOR / FUNÇÃO DE CONTROLO DE ACESSO (CIBERSEGURANÇA)
def verificar_autenticacao():
    if 'conta_logada' not in session:
        return False
    return True

# 🏠 1. ROTA PRINCIPAL: Redireciona e carrega dados com base na Role (Cibersegurança RBAC)
@app.route('/')
def index():
    if not verificar_autenticacao():
        return redirect(url_for('login_page'))
    
    # 👑 CASO 1: Se o utilizador logado for GERENTE
    if session.get('role') == 'gerente':
        db = SessionLocal()
        # Busca todas as contas (exceto os gerentes) para listagem administrativa
        todas_contas = db.query(ContaDB).filter(ContaDB.role != 'gerente').order_by(ContaDB.numero).all()
        # Calcula a soma de dinheiro guardado em todo o banco
        total_banco = db.query(ContaDB).sum(ContaDB.saldo) or 0
        # Carrega as últimas 50 transações globais do banco para auditoria preventiva
        todos_movimentos = db.query(MovimentoDB).order_by(MovimentoDB.data.desc()).limit(50).all()
        db.close()
        
        # Enviamos as variáveis do administrador, e fixamos conta=None para evitar conflitos no HTML
        return render_template('dashboard.html', accounts_admin=todas_contas, total_banco=total_banco, movimentos_admin=todos_movimentos, conta=None)
    
    # 💵 CASO 2: Se o utilizador logado for um CLIENTE comum
    numero_conta = session['conta_logada']
    db = SessionLocal()
    
    # Busca estritamente os dados da conta que fez login (Isolamento de Dados)
    conta = db.query(ContaDB).filter(ContaDB.numero == numero_conta).first()
    # Busca apenas o histórico de movimentos desta conta específica para o Extrato Pessoal
    movimentos = db.query(MovimentoDB).filter(MovimentoDB.conta_numero == numero_conta).order_by(MovimentoDB.data.desc()).all()
    
    db.close()
    
    if not conta:
        session.clear()
        return redirect(url_for('login_page'))
        
    return render_template('dashboard.html', conta=conta, movimentos=movimentos)

# 🔑 2. ROTA: ECRÃ DE LOGIN
@app.route('/login-portal')
def login_page():
    if 'conta_logada' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

# 🔐 3. ROTA: PROCESSAR AUTENTICAÇÃO
@app.route('/login', methods=['POST'])
def login():
    numero = request.form.get('numero')
    pin = request.form.get('pin')
    
    db = SessionLocal()
    conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
    db.close()
    
    # Validação segura (No mundo real usar-se-ia hashing como bcrypt, mas para o trabalho o PIN direto já valida a lógica)
    if conta and conta.pin == pin:
        session['conta_logada'] = conta.numero
        session['titular_logado'] = conta.titular
        flash(f"Bem-vindo de volta, {conta.titular}!", "success")
        return redirect(url_for('index'))
    else:
        flash("Erro: Número de conta ou PIN incorretos.", "error")
        return redirect(url_for('login_page'))

# 🚪 4. ROTA: LOGOUT SEGURO
@app.route('/logout')
def logout():
    session.clear() # Destrói os tokens e cookies de sessão
    flash("Sessão encerrada com segurança.", "success")
    return redirect(url_for('login_page'))

# ✨ 5. ROTA: REGISTAR / CRIAR CONTA COM PIN
@app.route('/criar-conta', methods=['POST'])
def criar_conta():
    numero = request.form.get('numero')
    titular = request.form.get('titular')
    pin = request.form.get('pin')
    
    if len(str(pin)) != 4 or not str(pin).isdigit():
        flash("Erro: O PIN deve conter exatamente 4 números.", "error")
        return redirect(url_for('login_page'))

    db = SessionLocal()
    try:
        conta_existente = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if conta_existente:
            flash("Erro: Esse número de conta já se encontra registado.", "error")
            return redirect(url_for('login_page'))
            
        nova_conta = ContaDB(numero=numero, titular=titular, saldo=Decimal('0.00'), pin=pin)
        db.add(nova_conta)
        db.commit()
        flash("Conta registada com sucesso! Introduza as credenciais para aceder.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro no registo: {str(e)}", "error")
    finally:
        db.close()
        
    return redirect(url_for('login_page'))

# 💵 6. ROTA: OPERAÇÕES (DEPOSITAR / LEVANTAR NA PRÓPRIA CONTA)
@app.route('/operacao', methods=['POST'])
def operacao():
    if not verificar_autenticacao():
        return redirect(url_for('login_page'))
        
    numero = session['conta_logada'] # Segurança: Força o uso da conta da sessão, impedindo IDOR attacks
    tipo = request.form.get('tipo')
    try:
        valor = Decimal(request.form.get('valor'))
    except Exception:
        flash("Erro: Valor inválido.", "error")
        return redirect(url_for('index'))

    if valor <= 0:
        flash("Erro: O valor deve ser superior a 0 €.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if tipo == "Depósito":
            conta.saldo += valor
            flash(f"Depósito de {valor:.2f}€ efetuado!", "success")
        elif tipo == "Levantamento":
            if valor > conta.saldo:
                flash("Erro: Saldo insuficiente.", "error")
                return redirect(url_for('index'))
            conta.saldo -= valor
            flash(f"Levantamento de {valor:.2f}€ efetuado!", "success")

        novo_movimento = MovimentoDB(
            conta_numero=numero, tipo=tipo,
            valor=valor if tipo == "Depósito" else -valor,
            data=datetime.now(), descricao=f"{tipo} no ATM Online"
        )
        db.add(novo_movimento)
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Erro: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('index'))

# 🔄 7. ROTA: TRANSFERÊNCIA
@app.route('/transferir', methods=['POST'])
def transferir():
    if not verificar_autenticacao():
        return redirect(url_for('login_page'))

    origem = session['conta_logada'] # Segurança redobrada
    destino = request.form.get('destino')
    try:
        valor = Decimal(request.form.get('valor'))
    except Exception:
        flash("Erro: Valor inválido.", "error")
        return redirect(url_for('index'))

    if valor <= 0 or origem == destino:
        flash("Erro: Operação inválida.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta_origem = db.query(ContaDB).filter(ContaDB.numero ==  origem).first()
        conta_destino = db.query(ContaDB).filter(ContaDB.numero == destino).first()

        if not conta_destino:
            flash(f"Erro: A conta destinatária #{destino} não existe.", "error")
            return redirect(url_for('index'))
        if valor > conta_origem.saldo:
            flash("Erro: Saldo insuficiente para transferência.", "error")
            return redirect(url_for('index'))

        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        mov_origem = MovimentoDB(conta_numero=origem, tipo="Transferência (Enviada)", valor=-valor, data=datetime.now(), descricao=f"Enviado para conta #{destino}", conta_destino=destino)
        mov_destino = MovimentoDB(conta_numero=destino, tipo="Transferência (Recebida)", valor=valor, data=datetime.now(), descricao=f"Recebido de conta #{origem}", conta_destino=origem)

        db.add(mov_origem)
        db.add(mov_destino)
        db.commit()
        flash(f"Transferência de {valor:.2f}€ concluída!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('index'))

# 🗑️ 8. ROTA: ELIMINAR A PRÓPRIA CONTA
@app.route('/eliminar-minha-conta', methods=['POST'])
def eliminar_conta():
    if not verificar_autenticacao():
        return redirect(url_for('login_page'))
        
    numero = session['conta_logada']
    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        db.delete(conta)
        db.commit()
        session.clear()
        flash("A tua conta foi permanentemente apagada do servidor.", "success")
        return redirect(url_for('login_page'))
    except Exception as e:
        db.rollback()
        flash(f"Erro: {str(e)}", "error")
        return redirect(url_for('index'))
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)