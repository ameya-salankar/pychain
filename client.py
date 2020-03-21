import json
import requests
import numpy as np

from client_method import Client
from pprint import pprint


CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

client = Client()
model = (client.model_build()).get_weights()
models = np.array([0, 0])
print(len(model))


for i in range(10):

    response = requests.get("{}/recent_block".format(CONNECTED_NODE_ADDRESS))
    # content = []
    if i != 0 and response.status_code == 200:
        model = []
        content = json.loads(response.content)
        modeld = json.loads(content["block"][0]["content"])
        for i in modeld:
            model.append(np.array(i))
        # print(content, "\n", model)

    # pprint(model)
    # pprint(content, "\n", model)

    model_list = []
    # model = np.array(model)
    models = client.Federated_model(i, model)
    for model in models:
        z = []
        for j in model:
            z.append(j.tolist())
        model_list.append(z)

    post_object = {
        "author": "client",
        "content": json.dumps(model_list),
    }

    # pprint(post_object, "\n", models)
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(
        new_tx_address, json=post_object, headers={"Content-type": "application/json"},
    )

    requests.get("{}/mine".format(CONNECTED_NODE_ADDRESS))
