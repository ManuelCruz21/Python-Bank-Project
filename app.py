import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import SessionLocal, ContaDB, MovimentoDB
from decimal import Decimal
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "ultra-secure-banking-session-2026")

def verificar_autenticacao():
    return 'conta_logada' in session

# Main Route (dashboard)
@app.route('/')
def index():
    if not verificar_autenticacao():
        return redirect(url_for('login_page'))
    
    # Manager Role
    if session.get('role') == 'gerente':
        db = SessionLocal()
        todas_contas = db.query(ContaDB).filter(ContaDB.role != 'gerente').order_by(ContaDB.numero).all()
        total_banco = db.query(ContaDB).sum(ContaDB.saldo) or 0
        todos_movimentos = db.query(MovimentoDB).order_by(MovimentoDB.data.desc()).limit(50).all()
        db.close()
        return render_template('dashboard.html', accounts_admin=todas_contas, total_banco=total_banco, movimentos_admin=todos_movimentos, conta=None)
    
    # Client Role
    numero_conta = session['conta_logada']
    db = SessionLocal()
    conta = db.query(ContaDB).filter(ContaDB.numero == numero_conta).first()
    movimentos = db.query(MovimentoDB).filter(MovimentoDB.conta_numero == numero_conta).order_by(MovimentoDB.data.desc()).all()
    db.close()
    
    if not conta:
        session.clear()
        return redirect(url_for('login_page'))
        
    return render_template('dashboard.html', conta=conta, movimentos=movimentos)

# Login Page
@app.route('/login-portal')
def login_page():
    if verificar_autenticacao():
        return redirect(url_for('index'))
    return render_template('login.html')

# Login Process
@app.route('/login', methods=['POST'])
def login():
    numero = request.form.get('numero')
    pin = request.form.get('pin')
    
    db = SessionLocal()
    conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
    db.close()
    
    if conta and conta.pin == pin:
        session['conta_logada'] = conta.numero
        session['titular_logado'] = conta.titular
        session['role'] = conta.role
        flash(f"Welcome back, {conta.titular}!", "success")
        return redirect(url_for('index'))
    else:
        flash("Error: Invalid account number or PIN.", "error")
        return redirect(url_for('login_page'))

#  Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Session securely closed.", "success")
    return redirect(url_for('login_page'))

# Register Account (Client Only)
@app.route('/criar-conta', methods=['POST'])
def criar_conta():
    numero = request.form.get('numero')
    titular = request.form.get('titular')
    pin = request.form.get('pin')
    
    if numero == "0000":
        flash("Error: This account number is reserved for system administration.", "error")
        return redirect(url_for('login_page'))

    if len(str(pin)) != 4 or not str(pin).isdigit():
        flash("Error: PIN must contain exactly 4 digits.", "error")
        return redirect(url_for('login_page'))

    db = SessionLocal()
    try:
        conta_existente = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if conta_existente:
            flash("Error: This account number is already registered.", "error")
            return redirect(url_for('login_page'))
            
        nova_conta = ContaDB(numero=numero, titular=titular, saldo=Decimal('0.00'), pin=pin, role='cliente')
        db.add(nova_conta)
        db.commit()
        flash("Account created successfully! Please log in below.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database Error: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('login_page'))

# Financial Operations 
@app.route('/operacao', methods=['POST'])
def operacao():
    if not verificar_autenticacao() or session.get('role') == 'gerente':
        return redirect(url_for('login_page'))
        
    numero = session['conta_logada']
    tipo = request.form.get('tipo') 
    try:
        valor = Decimal(request.form.get('valor'))
    except Exception:
        flash("Error: Invalid amount value.", "error")
        return redirect(url_for('index'))

    if valor <= 0:
        flash("Error: Amount must be greater than 0 €.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if tipo == "Deposit":
            conta.saldo += valor
            flash(f"Deposit of {valor:.2f}€ successfully processed!", "success")
        elif tipo == "Withdrawal":
            if valor > conta.saldo:
                flash("Error: Insufficient balance.", "error")
                return redirect(url_for('index'))
            conta.saldo -= valor
            flash(f"Withdrawal of {valor:.2f}€ successfully processed!", "success")

        novo_movimento = MovimentoDB(
            conta_numero=numero, tipo=tipo, valor=valor if tipo == "Deposit" else -valor,
            data=datetime.now(), descricao=f"{tipo} via Online ATM"
        )
        db.add(novo_movimento)
        db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Transaction Error: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('index'))

# Transfers
@app.route('/transferir', methods=['POST'])
def transferir():
    if not verificar_autenticacao() or session.get('role') == 'gerente':
        return redirect(url_for('login_page'))

    origem = session['conta_logada']
    destino = request.form.get('destino')
    try:
        valor = Decimal(request.form.get('valor'))
    except Exception:
        flash("Error: Invalid amount value.", "error")
        return redirect(url_for('index'))

    if valor <= 0 or origem == destino:
        flash("Error: Invalid transfer request.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta_origem = db.query(ContaDB).filter(ContaDB.numero == origem).first()
        conta_destino = db.query(ContaDB).filter(ContaDB.numero == destino).first()

        if not conta_destino:
            flash(f"Error: Destination account #{destino} does not exist.", "error")
            return redirect(url_for('index'))
        if valor > conta_origem.saldo:
            flash("Error: Insufficient funds for this transfer.", "error")
            return redirect(url_for('index'))

        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        mov_origem = MovimentoDB(conta_numero=origem, tipo="Transfer (Sent)", valor=-valor, data=datetime.now(), descricao=f"Sent to account #{destino}", conta_destino=destino)
        mov_destino = MovimentoDB(conta_numero=destino, tipo="Transfer (Received)", valor=valor, data=datetime.now(), descricao=f"Received from account #{origem}", conta_destino=origem)

        db.add(mov_origem)
        db.add(mov_destino)
        db.commit()
        flash(f"Transfer of {valor:.2f}€ successfully completed!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Transfer Error: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('index'))

# Admin Actions: manager revokes account
@app.route('/admin/eliminar-conta/<numero>', methods=['POST'])
def admin_eliminar_conta(numero):
    if not verificar_autenticacao() or session.get('role') != 'gerente':
        flash("Access Denied: Insufficient privileges.", "error")
        return redirect(url_for('login_page'))
        
    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if conta:
            db.delete(conta)
            db.commit()
            flash(f"Account #{numero} has been permanently terminated for security auditing purposes.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", "error")
    finally:
        db.close()
    return redirect(url_for('index'))

# Client Self-termination
@app.route('/eliminar-minha-conta', methods=['POST'])
def eliminar_conta():
    if not verificar_autenticacao() or session.get('role') == 'gerente':
        return redirect(url_for('login_page'))
        
    numero = session['conta_logada']
    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        db.delete(conta)
        db.commit()
        session.clear()
        flash("Your account has been permanently deleted from our servers.", "success")
        return redirect(url_for('login_page'))
    except Exception as e:
        db.rollback()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('index'))
    finally:
        db.close()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)