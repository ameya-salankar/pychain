import json
import requests

from client_method import Client
from pprint import pprint


CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

client = Client()
model = (client.model_build()).get_weights()

for i in range(10):

    response = requests.get("{}/recent_block".format(CONNECTED_NODE_ADDRESS))
    # content = []
    if i != 0 and response.status_code == 200:
        content = json.loads(response.content)
        model = json.loads(content["block"][0]["content"])
        print(content, "\n", model)

    pprint(model)
    # pprint(content, "\n", model)

    models = client.Federated_model(i, model)

    post_object = {
        "author": "client",
        "content": models,
    }

    pprint(post_object, "\n", models)
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(
        new_tx_address,
        json=json.dumps(post_object),
        headers={"Content-type": "application/json"},
    )

    requests.get("{}/mine".format(CONNECTED_NODE_ADDRESS))

    requests.get("{}/average".format(CONNECTED_NODE_ADDRESS))
