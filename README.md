# Backend

### Running Locally

```sh
python3 app.py run
```

- http://localhost:5000


### Running on MainRoute

... under construction


## Routes
#### Consulta
##### Request: 
/check_transaction

*apenas chamar a aplicação, sem necessidade de parametros. Rotina irá buscar os transactions "em andamento" para envio a acesso condo

##### Response:
Success: {
     "payload": [
             {"deliveryTransactionID" : 20201215001,
                 "deliverymanName" : "Renato Oliveira",
                 "dwellerName" : "Felipe Pinheiro",
                 "condominiumName" : "Morada dos Bosques",
                 "condominiumUnit" : "106B",
                 "storeName" : "Nostro Molino",
                 "vehicleTypeName" : "Motocicleta",
                 "vehicleManufacturer" : "Honda",
                 "vehicleColorName" : "Azul",
                 "vehicleLicensePlate" : "ZXD123A456",
                 "orderInfo" : "Pizza"

             }

     ]

 }

Error: {"mensagem": "Nenhuma entrega para autorizar!"}
