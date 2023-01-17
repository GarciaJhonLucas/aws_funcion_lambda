import json
import os
import mercadopago


def lambda_handler(event, context):

    sdk = mercadopago.SDK(os.environ["TEST_TOKEN"])
    bodyGet = json.loads(event["body"])

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
    
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    if payment.get("status_detail") is None:
        rpta = payment
    else:
        rpta = {
            "id": payment["id"],
            "status": payment["status"],
            "detail": payment["status_detail"],
        }

    return {"statusCode": 200, "body": json.dumps(rpta)}