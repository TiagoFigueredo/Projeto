from flask import abort, render_template, Flask, request, redirect, url_for, app
import db
import logging
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

APP = Flask(__name__)

# PAGINA INICIAL


@APP.route('/')
def index():
    return render_template('index.html', message='I USE TO THINK DARLING')


@APP.route('/init/')
def init():
    return render_template('index.html', init=db.init())


@APP.route('/operador/<int:numero>/')
def entraOperador(numero):
    
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()

    if operador is None:
        abort(404, 'OPERADOR NÃO EXISTE'.format(numero))

    turno = db.execute(
        '''
        SELECT NTurno, NumOP, Inicio
        FROM TURNO 
        WHERE  NumOP = %s 
        ORDER BY NTurno DESC
        ''', numero).fetchone()

    return render_template('OperadorPage.html', operador=operador, turno=turno)


@APP.route('/operador/<int:numero>/logout')
def saiOperador(numero):
    adicionaTurno(numero)
    return index()


@APP.route('/operador/<int:numero>/')
def adicionaTurno(numero):
    turnoo = db.execute(
        '''
        INSERT INTO TURNO(NTurno,NumOP)
        SELECT (b.NTurno)+1,b.NumOP from TURNO b Where b.NumOP= %s ORDER BY b.NTurno DESC LIMIT 1;
        ''', numero).fetchone()
    db.commit()
    return "changed"


@APP.route('/operador/<int:numero>/novaTransacao')
def goTransacao(numero):
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()
    transacao = db.execute(
          '''
          SELECT * FROM TRANSACAO ORDER BY NumTransacao DESC LIMIT 1
          ''').fetchone()
    if request.method == "GET" and request.args.get("finaliza")=="finaliza":
        transacao = db.execute(
            '''
                INSERT INTO TRANSACAO()
                VALUES()
            '''
        )
        db.commit()
        return redirect(url_for("entraOperador",numero=numero))
    return render_template('transacao.html', operador=operador,transacao=transacao)


@APP.route('/operador/<int:numero>/novaTransacao/addArtigo', methods=["GET","POST"])
def adArtigo(numero):
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()
    CodBarra=0
    if request.method == "GET":
        if request.args.get("OK") == "OK":
            CodBarra = request.args.get("CodBarra")
    elif(request.form["button"]=="CONFIRMAR"):
            CodBarra = request.args.get("CodBarra")
            transacao = db.execute(
                '''
                INSERT INTO ADICIONA_ARTIGO(CodBarra,NumTransacao)
                SELECT a.CodBarra,b.NumTransacao
                FROM ARTIGO a JOIN (SELECT * FROM TRANSACAO ORDER BY NumTransacao DESC LIMIT 1) b ON a.CodBarra = %s;
                ''',CodBarra).fetchone()
    db.commit()
    artigo = db.execute(
        '''
          SELECT *
          FROM ARTIGO 
          WHERE  CodBarra = %s
          ''', CodBarra).fetchone()
    return render_template('addArtigo.html', operador=operador,artigo=artigo)



@APP.route('/operador/<int:numero>/novaTransacao/Fatura', methods=["GET","POST"])
def Fatura(numero):
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()
    Nif=0
    if request.method == "GET":
        if request.args.get("OK") == "OK":
            Nif = request.args.get("NIF")
    elif(request.form["button"]=="CONFIRMAR"):
            Nif = request.args.get("NIF")
            transacao = db.execute(
                '''
                INSERT INTO FATURA(Nif,NumTransacao)
                SELECT a.Nif,b.NumTransacao
                FROM CLIENTE a JOIN (SELECT * FROM TRANSACAO ORDER BY NumTransacao DESC LIMIT 1) b ON a.Nif = %s;
                ''',Nif).fetchone()
    db.commit()
    cliente = db.execute(
        '''
          SELECT *
          FROM CLIENTE 
          WHERE  Nif = %s
          ''', Nif).fetchone()
    return render_template('Fatura.html', operador=operador,cliente=cliente)


if __name__ == '__main__':
    app.debug = True
    app.run()
