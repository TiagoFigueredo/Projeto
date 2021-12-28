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


    if numero == 99:
        return redirect(url_for("entraSupervisor"))

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

@APP.route('/supervisor/')
def entraSupervisor():
    return render_template('SupervisorPage.html')

@APP.route('/supervisor/ConsultarTransacao/<int:NumTransacao>/')
def ConsultarTransacaoIndividual(NumTransacao):
    transacao = db.execute(
            '''
           SELECT *,c.Preco*b.Quantidade AS TOTAL FROM TRANSACAO a
NATURAL JOIN ADICIONA_ARTIGO b
NATURAL JOIN ARTIGO c
WHERE NumTransacao=%s;
            ''',NumTransacao).fetchall()
    if transacao is None:
        abort(404, 'TRANSAÇÃO NÃO EXISTE'.format(NumTransacao))

    operador = db.execute(
            '''
            SELECT * FROM TURNO  NATURAL JOIN OPERADOR WHERE NumTransacao = %s;
            ''',NumTransacao).fetchone()    
    cliente = db.execute(
            '''
            SELECT * FROM FATURA NATURAL JOIN CLIENTE WHERE NumTransacao = %s;
            ''',NumTransacao).fetchone()        
    return render_template("TransacaoIndividual.html",transacao=transacao,operador=operador,cliente=cliente)

@APP.route('/supervisor/ConsultarTransacao')
def ConsultarTransacao():
    transacao = "";
    if request.method == "GET":
        if request.args.get("NumTransacao") == "OK":
            transacao = db.execute(
            '''
            SELECT NumTransacao,Hora 
            FROM TRANSACAO
            ORDER BY NumTransacao
            ''').fetchall()
        if request.args.get("DataRecente") == "OK":
            transacao = db.execute(
            '''
            SELECT NumTransacao,Hora 
            FROM TRANSACAO
            ORDER BY Hora DESC
            ''').fetchall()
        if request.args.get("DataAntiga") == "OK":
            transacao = db.execute(
            '''
            SELECT NumTransacao,Hora 
            FROM TRANSACAO
            ORDER BY Hora 
            ''').fetchall()
        if request.args.get("back") == "OK":
            return redirect(url_for("entraSupervisor"))
        if request.args.get("OK") == "OK":
            NumOP=request.args.get("NumOP")
            transacao = db.execute(
            '''
            SELECT NumTransacao,Hora 
            FROM TRANSACAO
            NATURAL JOIN TURNO
            WHERE NumOP = %s
            ''',NumOP).fetchall()

    return render_template('ConsultarTransacao.html',transacao=transacao)




@APP.route('/supervisor/ConsultarOperador')
def ConsultarOperador():
    return render_template('ConsultarOperador.html')
@APP.route('/supervisor/ConsultarTurno')
def ConsultarTurno():
    return render_template('ConsultarTurno.html')




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
    if request.method == "GET" and request.args.get("finaliza") == "finaliza":
        transacao = db.execute(
            '''
                INSERT INTO TRANSACAO()
                VALUES()
            '''
        )
        a = db.execute(
            '''
                INSERT INTO TURNO(NTurno,NumTransacao,NumOP,Inicio)
                                
                    SELECT a.NTurno,b.NumTransacao,%s,a.Inicio 
                    FROM TURNO a
                    INNER JOIN TRANSACAO b 
                    ORDER BY b.NumTransacao DESC , Inicio DESC 
                    LIMIT 1;
            '''
        ,numero).fetchone()
        db.commit()
        #ESSA FUNCIONALIDADE NÃO FUNCIONARÁ POIS:
        #PRECISARIA SAIR DO APP.PY E ENTRAR NOVAMENTE PARA VALIDAR POIS
        #O DB.COMMIT SO REALIZA MUDANÇAS DEPOIS DE SAIR
        return redirect(url_for("entraOperador", numero=numero))
    return render_template('NovaTransacao.html', operador=operador, transacao=transacao)


@APP.route('/operador/<int:numero>/novaTransacao/addArtigo', methods=["GET", "POST"])
def adArtigo(numero):
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()
    CodBarra = 0
    if request.method == "GET":
        if request.args.get("OK") == "OK":
            CodBarra = request.args.get("CodBarra")
            a = db.execute(
                    '''
            SELECT *
            FROM ARTIGO 
            WHERE  CodBarra = %s
            ''', CodBarra).fetchone()
            if a is None:
                abort(404, 'ARTIGO NÃO EXISTE'.format(numero))
            a = db.execute(
                    '''
            SELECT *
            FROM ARTIGO
            NATURAL JOIN ESTOQUE 
            WHERE CodBarra = %s 
            AND
            Quantidade IS NOT NULL
            ''', CodBarra).fetchone()
            if a is None:
                abort(404, 'ARTIGO NÃO PRESENTE NO ESTOQUE'.format(numero))     
    elif(request.form["button"] == "CONFIRMAR"):
        CodBarra = request.args.get("CodBarra")
        transacao = db.execute(
            '''
                INSERT INTO ADICIONA_ARTIGO(CodBarra,NumTransacao)
                SELECT a.CodBarra,b.NumTransacao
                FROM ARTIGO a JOIN (SELECT * FROM TRANSACAO ORDER BY NumTransacao DESC LIMIT 1) b ON a.CodBarra = %s;
                ''', CodBarra).fetchone()
        aux =  db.execute(
            '''
                UPDATE ESTOQUE
                SET Quantidade = Quantidade - 1
                WHERE CodBarra = %s
                ''', CodBarra).fetchone()
    db.commit()
    artigo = db.execute(
        '''
          SELECT *
          FROM ARTIGO 
          WHERE  CodBarra = %s
          ''', CodBarra).fetchone()

    return render_template('addArtigo.html', operador=operador, artigo=artigo)


@APP.route('/operador/<int:numero>/novaTransacao/Fatura', methods=["GET", "POST"])
def Fatura(numero):
    operador = db.execute(
        '''
          SELECT NumOP, Nome, Salario
          FROM OPERADOR 
          WHERE  NumOP = %s
          ''', numero).fetchone()
    Nif = 0
    if request.method == "GET":
        if request.args.get("OK") == "OK":
            Nif = request.args.get("NIF")
            a = db.execute(
                    '''
            SELECT *
            FROM CLIENTE 
            WHERE  Nif = %s
            ''', Nif).fetchone()
            if a is None:
                abort(404, 'CLIENTE NÃO EXISTE'.format(numero))

    elif(request.form["button"] == "CONFIRMAR"):
        Nif = request.args.get("NIF")
        transacao = db.execute(
            '''
                INSERT INTO FATURA(Nif,NumTransacao)
                SELECT a.Nif,b.NumTransacao
                FROM CLIENTE a JOIN (SELECT * FROM TRANSACAO ORDER BY NumTransacao DESC LIMIT 1) b ON a.Nif = %s;
                ''', Nif).fetchone()
    cliente = db.execute(
        '''
          SELECT *
          FROM CLIENTE 
          WHERE  Nif = %s
          ''', Nif).fetchone()
    db.commit()

    return render_template('Fatura.html', operador=operador, cliente=cliente)


if __name__ == '__main__':
    app.debug = True
    app.run()
