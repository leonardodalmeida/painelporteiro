from flask import Flask, render_template, request
import sql
from datetime import datetime

app = Flask(__name__)
app._static_folder = "static"


#atEntrance = time de quando o entregador chegou na portaria
#rejectEntrance = time de quando rejeitado
#EnteredTime = time quando foi dada entrada
#ExitTime = time quando foi dado a saida

#to-do

#comprimir imagens - ok
#criar render para reuso - ok
#contador para reuso - ok
#criar tag para bd e reuso - ok
#mudar e registrar todos os timestamps conforme leganda acima - ok
#contar o tempo no condomínio - ok

@app.route('/onboarding/<idtransaction>', methods=["GET", "POST"])
def check_transactionID(idtransaction):
    if sql.verifyTransactionsID_inprogress(idtransaction) is True:
        if sql.GetStatus(idtransaction) == "Entregador entrou no condomínio":
            if sql.TestTimeinCondominium(idtransaction) == "Ok":
                sql.update_book(idtransaction, "Entregador saiu do condomínio")
            #else:
                #Este estado vai existir apenas com uma procedure que vai mudar o status para "Entrega sem check-out"
                #sql.update_book(idtransaction, "Entregador levou muito tempo no condomínio")

            #criar painel de saída - Este entregador permanceu por "x tempo" no condomínio
            timeincond = str(sql.GetTimeinCondominium(idtransaction))
            return '<h1>Este entregador permanceu por '+timeincond+' minutos no condomínio.</h1>'

        else:
            if sql.ExpirationTest(idtransaction) == "Válido" and sql.GetStatus(idtransaction) != "Entregador na portaria" or request.method == "POST":

                sql.update_book(idtransaction, "Entregador na portaria")
                sql.update_datetime_At_entrance(idtransaction, str(datetime.now()))

                # armazena todas as infos da entrega, por enquanto vamos pegar apenas a posicao zero, quando tivermos mais de uma entrega por motoboy precisa update
                var = sql.Get_transactions(idtransaction)[0]

                if request.method == "GET":
                    return render_painel(var)
                else:
                    result = submit()
                    if result == "aprovar":
                        sql.update_book(idtransaction, "Entregador entrou no condomínio")
                        # get timedate now
                        now = str(datetime.now())
                        sql.update_datetime_entrance(idtransaction, now)
                        return '<h1>O acesso foi Liberado!</h1>'
                    else:
                        sql.update_book(idtransaction, "Check-in rejeitado na portaria")
                        sql.update_datetime_RejectAt_entrance(idtransaction, str(datetime.now()))
                        return render_painel_reject(str(idtransaction))

            else:
                if sql.GetStatus(idtransaction) == "Entregador na portaria":
                    sql.update_book(idtransaction, "Check-in reutilzado")
                    sql.contCheckin(1)
                    return render_painel_used(str(idtransaction))
                else:
                    sql.update_book(idtransaction, "Check-in expirado")
                    return render_painel_expirate(str(idtransaction))

    else:
        return {
            "mensagem": "Nenhuma entrega para autorizar!"
        }

@app.route('/')
def submit():
    if request.form.get("resultButton_a"):
        return "aprovar"
    elif request.form.get("resultButton_b"):
        return "rejeitar"



@app.route('/')
def render_painel(var):
    try:
        render_page = render_template("painel.html",
                               deliveryTransactionID=var['deliveryTransactionID'],
                               deliverymanName=var['deliverymanName'],
                               deliverymanCPF=var['deliverymanCPF'],
                               #deliverymanProfilePicture="/static/" + var['deliverymanProfilePicture'],
                               deliverymanProfilePicture=var['deliverymanProfilePicture'],
                               dwellerName=var['dwellerName'],
                               residenceUnit=var['residenceUnit'],
                               storeName=var['storeName'],
                               storeAddress=var['storeAddress'],
                               authorizedBy="Autorizado por: " + var['authorizedBy'],
                               authorizedTimestamp="Quando? " + str(var['authorizedTimestamp']),
                               orderInfo=var['orderInfo']
                               )

        return render_page

    except Exception as e:
        handle_exception(e)

@app.route('/')
def render_painel_used(deliveryTransactionID):
    try:
        render_page = render_template("used.html",
                               deliveryTransactionID=deliveryTransactionID
                               )

        return render_page

    except Exception as e:
        handle_exception(e)

@app.route('/')
def render_painel_expirate(deliveryTransactionID):
    try:
        render_page = render_template("expirate.html",
                               deliveryTransactionID=deliveryTransactionID
                               )

        return render_page

    except Exception as e:
        handle_exception(e)
@app.route('/')
def render_painel_reject(deliveryTransactionID):
    try:
        render_page = render_template("reject.html",
                               deliveryTransactionID=deliveryTransactionID
                               )

        return render_page

    except Exception as e:
        handle_exception(e)

def handle_exception(e):
    print(e)
if __name__ == '__main__':
    app.run()
