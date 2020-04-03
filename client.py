import json
import requests
import numpy as np

from client_method import Client
from pprint import pprint


CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

# Initialize the client
client = Client()
model = (client.model_build()).get_weights()
models = np.array([0, 0])


for i in range(10):
    # Get the recent most block from the chain, which contains the avg weights
    response = requests.get("{}/recent_block".format(CONNECTED_NODE_ADDRESS))
    
    # The first iteration won't have any avg weights from server
    if i != 0 and response.status_code == 200:
        model = []
        content = json.loads(response.content)
        modeld = json.loads(content["block"][0]["content"])
        for i in modeld:
            model.append(np.array(i))

    models = client.Federated_model(i, model)

    # Convert the model into list
    model_list = []
    for model in models:
        z = []
        for j in model:
            z.append(j.tolist())
        model_list.append(z)

    post_object = {
        "author": "client",
        "content": json.dumps(model_list),
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(
        new_tx_address, json=post_object, headers={"Content-type": "application/json"},
    )

    # Then immediately mine
    requests.get("{}/mine".format(CONNECTED_NODE_ADDRESS))
