import json
import os
import mercadopago

def lambda_handler(event, context):

    # Obtener el token del archivo env
    sdk = mercadopago.SDK(os.environ["TEST_TOKEN"])
    bodyGet = json.loads(event["body"]) # Cargar los datos de la respuesta

    # Detallar los datos y sus tipos a usar en json
    payment_data = {
        "transaction_amount": float(bodyGet["transaction_amount"]),
        "token": bodyGet["token"],
        "installments": int(bodyGet["installments"]),
        "payment_method_id": bodyGet["payment_method_id"],
        "issuer_id": bodyGet["issuer_id"],
        "payer": {
            "email": bodyGet["payer"]["email"],
            "identification": {
                "type": bodyGet["payer"]["identification"]["type"],
                "number": bodyGet["payer"]["identification"]["number"],
            },
        },
    }
    
    # Cargar los datos de items.products
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    # Validamos la respuesta y ofrecemos una respuesta
    if payment.get("status_detail") is None:
        rpta = payment
    else:
        rpta = {
            "id": payment["id"],
            "status": payment["status"],
            "detail": payment["status_detail"],
        }

    # Todo ok
    return {
        "statusCode": 200, 
        "body": json.dumps(rpta)
    }