from mysql import connector as mysql
import config
from datetime import datetime

# {
#     "payload": [
#             {"deliveryTransactionID" : 20201215001,       #table -> DeliveryTransaction
#              "deliverymanName" : "Renato Oliveira",       #table -> Deliveryman by deliverymanID in DeliveryTransaction
#              "dwellerName" : "Felipe Pinheiro",           #table -> Dweller by dwellerID in DeliveryTransaction
#              "condominiumName" : "Morada dos Bosques",    #table -> Condominium by CondominiumID in DeliveryTransaction ****** return acesso condo
#              "condominiumUnit" : "106B",                  #table -> Condominium by CondominiumID in DeliveryTransaction ****** return acesso condo
#              "storeName" : "Nostro Molino",               #table -> Store by storeID in DeliveryTransaction
#              "vehicleTypeName" : "Motocicleta",           #table -> VehicleType by vehicleID in Vehicle                                           ****
#              "vehicleManufacturer" : "Honda",             #table -> Vehicle by vehicleID in DeliveryTransaction
#              "vehicleColorName" : "Azul",                 #table -> Vehicle by vehicleID in DeliveryTransaction
#              "vehicleLicensePlate" : "ZXD123A456",        #table -> Vehicle by vehicleID in DeliveryTransaction
#              "orderInfo" : "Pizza"                        #table -> orderInfo in DeliveryTransaction
#              }]
# }

def conectBD():
    connection = None
    try:
        connection = mysql.connect(host=config.HOST,
                           port=config.PORT,
                           database=config.DATABASE,
                           user=config.USER,
                           password=config.PASSWORD
                           )
        return connection

    except Exception as e:
        handle_exception(e)
        return connection


# def verify(qr_code):
#     try:
#
#         # with mysql.connect(host=config.HOST,
#         #                    port=config.PORT,
#         #                    database=config.DATABASE,
#         #                    user=config.USER,
#         #                    password=config.PASSWORD
#         #                    ) as connection:
#
#             with conectBD().cursor() as cursor:
#                 query = 'SELECT * FROM DeliveryTransaction as p WHERE p.deliverytransactionQRCode = ' + qr_code + ' AND p.deliverytransactionStatus = "Aprovado"'
#                 cursor.execute(query)
#
#                 query_result = cursor.fetchone()
#                 if query_result is None:
#                     return False
#                 else:
#                     return True
#
#     except Exception as e:
#         handle_exception(e)


def verifyTransactionsID_inprogress(idtransaction):
    try:
        connect = None
        connect = conectBD()

        c = connect.cursor()
        q = 'SELECT * FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(idtransaction) +';'
        r = c.execute(q)


        query_result = c.fetchone()

        c.close()
        connect.close()

        if query_result is None:
            return False
        else:
            return True

    except Exception as e:
        handle_exception(e)

def Get_transactions(idtransaction):
    """
    Função usada para capturar os dados que estão disponíveis para mostrar ao porteiro
    """
    payload = list()
    deliveryTransaction_dict = dict()
    try:
        bd = conectBD()
        getIDsCursor = bd.cursor()
        query = 'SELECT deliveryTransactionID FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(idtransaction)
        getIDsCursor.execute(query)
        getIds = getIDsCursor.fetchall()
        deliveryTransaction_dict = {"deliveryTransactionID" : "",
                    "deliverymanName" : "",
                    "deliverymanCPF": "",
                    "deliverymanProfilePicture": "",
                    "dwellerName" : "",
                    "residenceUnit": "",
                    "storeName" : "",
                    "storeAddress": "",
                    "authorizedBy": "",
                    "authorizedTimestamp": "",
                    "orderInfo" : ""}
        getIDsCursor.close()
        for id in getIds:
            with bd.cursor() as cursorQuery:
                SQuery = """SELECT p.deliveryTransactionID,
                                 dlv.deliverymanName, 
                                 dlv.deliverymanCPF, 
                                 dlv.deliverymanProfilePicture, 
                                 p.dwellerName, 
                                 res.residenceUnit, 
                                 st.storeName, 
                                 st.storeAddress, 
                                 p.authorizedBy, 
                                 p.authorizedTimestamp, 
                                 p.orderInfo FROM DeliveryTransaction as p
                            LEFT JOIN Deliveryman as dlv ON dlv.deliverymanID = p.deliverymanID
                            LEFT JOIN Residence as res ON res.residenceID = p.residenceID
                            LEFT JOIN Store as st ON st.storeID = p.storeID
                            WHERE p.deliveryTransactionID = """ + str(id[0])
                cursorQuery.execute(SQuery)

                # cursorQuery.execute("""SELECT p.deliveryTransactionID,
                #                                             p.vehicleID,
                #                                             p.dwellerID,
                #                                             p.storeID,
                #                                             p.deliverymanID,
                #                                             p.condominiumID,
                #                                             dlv.deliverymanName,
                #                                             dlv.deliverymanCPF,
                #                                             dlv.deliverymanProfilePicture,
                #                                             p.dwellerName,
                #                                             cdm.condominiumName,
                #                                             cdm.condominiumAddress,
                #                                             st.storeName,
                #                                             st.storeAddress,
                #                                             p.authorizationBy,
                #                                             vT.vehicleTypeName,
                #                                             vM.vehicleManufacturer,
                #                                             vC.vehicleColorName,
                #                                             v.vehicleLicensePlate,
                #                                             p.orderInfo FROM DeliveryTransaction as p
                #                                       LEFT JOIN Vehicle as v ON v.vehicleID = p.vehicleID
                #
                #                                       LEFT JOIN VehicleType as vT ON vT.vehicleTypeID = v.vehicleID
                #                                       LEFT JOIN VehicleManufacturer as vM ON vM.VehicleManufacturerID = v.vehicleID
                #                                       LEFT JOIN VehicleColor as vC ON vC.VehicleColorID = v.vehicleID
                #
                #                                       LEFT JOIN Dweller as cdm ON cdm.dwellerID = p.dwellerID
                #                                       LEFT JOIN Store as st ON st.storeID = p.storeID
                #                                       LEFT JOIN Deliveryman as dlv ON dlv.deliverymanID = p.deliverymanID
                #                                       LEFT JOIN Condominium as cond ON cond.condominiumID = p.condominiumID
                #
                #                                       LEFT JOIN Authorization as aut ON aut.deliveryTransactionID = p.deliveryTransactionID
                #                                       LEFT JOIN AuthorizationPartner as autPrt ON autPrt.authorizationPartnerID = aut.authorizationPartnerID
                #
                #                                       WHERE p.deliveryTransactionID = %s;""",
                #                     (id,))

                line = cursorQuery.fetchall()
                i = 0
                for key in deliveryTransaction_dict.keys():
                    deliveryTransaction_dict[key] = line[0][i]
                    i += 1

                payload.append(deliveryTransaction_dict)

        bd.close()
        return payload
    except Exception as e:
        handle_exception(e)

def ExpirationTest(id):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = 'SELECT authorizedTimestamp FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)

        cursor.execute(query)

        # get query result
        query_result = cursor.fetchone()

        # get timedate now
        now = datetime.now()
        authorizedtime= query_result[0]

        expiratehours = 3 #inteiro para controlar em quantos horas expira o qr code, mudar conforme necessidade

        dif = now - authorizedtime

        if int(dif.total_seconds() / 60**2) > expiratehours:
            return "Expirado"
        else:
            return "Válido"


    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def GetStatus(id):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = 'SELECT deliveryTransactionStatus FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)

        cursor.execute(query)

        # get query result
        query_result = cursor.fetchone()

        # get status id transaction
        return query_result[0]


    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()


def update_book(id, upText):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET deliveryTransactionStatus = "+'"'+upText+'"'+" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def update_datetime_At_entrance(id, entrance):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET atEntranceTimestamp = "+'"'+entrance+'"'+" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def update_datetime_RejectAt_entrance(id, entrance):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET rejectedAtEntranceTimestamp = "+'"'+entrance+'"'+" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def update_datetime_entrance(id, entrance):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET enteredTimestamp = "+'"'+entrance+'"'+" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def GetCont(id):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = 'SELECT cont_usedQRCode FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)

        cursor.execute(query)

        # get query result
        query_result = cursor.fetchone()

        # get cont_usedQR Code id transaction
        if query_result is None:
            return 0
        else:
            return int(query_result[0])


    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def contCheckin(id, cont):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()


        cont = GetCont(id) + cont

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET cont_usedQRCode = "+ cont +" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def update_datetime_exit(id, exitedTimestamp):

    try:
        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = "UPDATE DeliveryTransaction SET exitedTimestamp = "+'"'+exitedTimestamp+'"'+" WHERE deliveryTransactionID = "+id

        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def TestTimeinCondominium(id):

    try:

        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()
        cursor2 = conn.cursor()

        # prepare query and data
        query_getEntrance = 'SELECT enteredTimestamp FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)
        cursor.execute(query_getEntrance)

        # get query result
        query_resultEntrance = cursor.fetchone()

        # get timedate entrance
        timeentrance= query_resultEntrance[0]

        # prepare query and data
        query_getExit = 'SELECT exitedTimestamp FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)
        cursor2.execute(query_getExit)

        # get query result
        query_resultExit = cursor2.fetchone()

        # get timedate exit
        timeexit = query_resultExit[0]

        dif = timeexit - timeentrance
        dif = int(dif.total_seconds() / 60)

        return dif

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def GetTimeinCondominium(id):

    try:

        now = str(datetime.now())
        update_datetime_exit(id, now)

        # read database
        conn = conectBD()

        # update book title
        cursor = conn.cursor()

        # prepare query and data
        query = 'SELECT enteredTimestamp FROM DeliveryTransaction as p WHERE p.deliveryTransactionID = ' + str(id)

        cursor.execute(query)

        # get query result
        query_result = cursor.fetchone()

        # get timedate entrance
        timeentrance= query_result[0]

        limitmin = 45 #inteiro para controlar em quantos horas expira o qr code, mudar conforme necessidade

        dif = now - timeentrance

        if int(dif.total_seconds() / 60) > limitmin:
            return "Limite excedido"
        else:
            return "Ok"

    except Exception as e:
        handle_exception(e)

    finally:
        cursor.close()
        conn.close()

def handle_exception(e):
    print(e)
