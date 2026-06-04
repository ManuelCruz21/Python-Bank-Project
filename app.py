import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models.database import SessionLocal, ContaDB, MovimentoDB
from datetime import datetime

app = Flask(__name__)
# Vai buscar a secret key definida no teu .env para segurança das sessões
app.secret_key = os.getenv("SECRET_KEY", "chave-secreta-padrao")

# 🏠 1. ROTA PRINCIPAL: Listar Contas no Dashboard
@app.route('/')
def index():
    db = SessionLocal()
    # Vai buscar as contas gravadas no Supabase para listar na tabela
    contas = db.query(ContaDB).all()
    db.close()
    return render_template('dashboard.html', contas=contas)

# ✨ 2. ROTA: Criar Nova Conta
@app.route('/criar-conta', methods=['POST'])
def criar_conta():
    numero = request.form.get('numero')
    titular = request.form.get('titular')
    
    db = SessionLocal()
    try:
        # Cibersegurança & Regra de Negócio: Verificar duplicação
        conta_existente = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if conta_existente:
            flash("Erro: Uma conta com esse número já existe!", "error")
            return redirect(url_for('index'))
            
        nova_conta = ContaDB(numero=numero, titular=titular, saldo=0.00)
        db.add(nova_conta)
        db.commit()
        flash(f"Conta #{numero} ativada com sucesso no Supabase!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro ao criar conta: {str(e)}", "error")
    finally:
        db.close()
        
    return redirect(url_for('index'))

# 💵 3. ROTA: Depositar ou Levantar Dinheiro
@app.route('/operacao', methods=['POST'])
def operacao():
    numero = request.form.get('numero')
    tipo = request.form.get('tipo') # 'Depósito' ou 'Levantamento'
    try:
        valor = float(request.form.get('valor'))
    except ValueError:
        flash("Erro: Valor inválido introduzido.", "error")
        return redirect(url_for('index'))

    if valor <= 0:
        flash("Erro: O valor deve ser superior a 0 €.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta = db.query(ContaDB).filter(ContaDB.numero == numero).first()
        if not conta:
            flash("Erro: Conta não encontrada no sistema.", "error")
            return redirect(url_for('index'))

        if tipo == "Depósito":
            conta.saldo += valor
            flash(f"Depósito de {valor:.2f}€ realizado com sucesso na conta #{numero}!", "success")
        
        elif tipo == "Levantamento":
            if valor > conta.saldo:
                flash(f"Erro: Saldo insuficiente. Saldo atual: {conta.saldo:.2f}€", "error")
                return redirect(url_for('index'))
            conta.saldo -= valor
            flash(f"Levantamento de {valor:.2f}€ realizado com sucesso na conta #{numero}!", "success")

        # Registar a transação no histórico de movimentos
        novo_movimento = MovimentoDB(
            conta_numero=numero,
            tipo=tipo,
            valor=valor if tipo == "Depósito" else -valor,
            data=datetime.now(),
            descricao=f"{tipo} via Web interface"
        )
        db.add(novo_movimento)
        db.commit()

    except Exception as e:
        db.rollback()
        flash(f"Erro na operação: {str(e)}", "error")
    finally:
        db.close()

    return redirect(url_for('index'))

# 🔄 4. ROTA: Transferência Bancária entre Contas
@app.route('/transferir', methods=['POST'])
def transferir():
    origem = request.form.get('origem')
    destino = request.form.get('destino')
    try:
        valor = float(request.form.get('valor'))
    except ValueError:
        flash("Erro: Valor de transferência inválido.", "error")
        return redirect(url_for('index'))

    if valor <= 0:
        flash("Erro: O valor de transferência deve ser maior que 0 €.", "error")
        return redirect(url_for('index'))

    if origem == destino:
        flash("Erro: Não pode transferir dinheiro para a mesma conta.", "error")
        return redirect(url_for('index'))

    db = SessionLocal()
    try:
        conta_origem = db.query(ContaDB).filter(ContaDB.numero == origem).first()
        conta_destino = db.query(ContaDB).filter(ContaDB.numero == destino).first()

        if not conta_origem:
            flash(f"Erro: Conta de Origem #{origem} não existe.", "error")
            return redirect(url_for('index'))
        if not conta_destino:
            flash(f"Erro: Conta de Destino #{destino} não existe.", "error")
            return redirect(url_for('index'))

        # Validar segurança de fundos
        if valor > conta_origem.saldo:
            flash(f"Erro: Saldo insuficiente na conta de origem. Saldo atual: {conta_origem.saldo:.2f}€", "error")
            return redirect(url_for('index'))

        # Executar a transferência matemática
        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        # Registar movimento na conta de origem (Saída de dinheiro)
        mov_origem = MovimentoDB(
            conta_numero=origem,
            tipo="Transferência (Enviada)",
            valor=-valor,
            data=datetime.now(),
            descricao=f"Transferido para conta #{destino}",
            conta_destino=destino
        )
        
        # Registar movimento na conta de destino (Entrada de dinheiro)
        mov_destino = MovimentoDB(
            conta_numero=destino,
            tipo="Transferência (Recebida)",
            valor=valor,
            data=datetime.now(),
            descricao=f"Recebido da conta #{origem}",
            conta_destino=origem
        )

        db.add(mov_origem)
        db.add(mov_destino)
        db.commit()
        
        flash(f"Transferência de {valor:.2f}€ enviada com sucesso para a conta #{destino}!", "success")

    except Exception as e:
        db.rollback()
        flash(f"Erro ao processar transferência: {str(e)}", "error")
    finally:
        db.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)