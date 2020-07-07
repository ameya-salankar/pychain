import json
import requests
import sys
import time
import numpy as np

from client_method import Client
from pprint import pprint

SPLIT_SIZE = 10

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"


def weights_update(all_weights):
        models = []
        for model in all_weights:
            z = []
            for j in model:
                z.append(np.array(j))
            models.append(z)
        all_weights = models
        m = all_weights[0]
        for num in range(1, len(all_weights)):
            a = all_weights[num]
            m = np.add(m, a)
        m /= len(all_weights)
        return m

time1 = time.time()

# Initialize the client
client = Client()
model = (client.model_build()).get_weights()
models = np.array([0, 0])

f = open("output.txt", "a")


time2 = time.time()
for i in range(10):
    # Get the recent most block from the chain, which contains the avg weights
    response = requests.get("{}/recent_block".format(CONNECTED_NODE_ADDRESS))
    
    # The first iteration won't have any avg weights from server
    if i != 0:
        if response.status_code == 200:
            model = []
            content = json.loads(response.content)
            modeld = json.loads(content["block"][0]["content"])
            for j in modeld:
                model.append(np.array(j))
            

            # print(model, file=f)
            # print("\n\n WEIGHTS", weights_update(models), file=f)

            resp = requests.get("{}/last_self_added_block".format(CONNECTED_NODE_ADDRESS))
            cont = json.loads(resp.content)

            submitted_modeld = json.loads(cont["block"][0]["content"])            
            submitted_model = [np.array(j) for j in submitted_modeld]

            avg_model = weights_update(submitted_model)
            is_update_valid = True

            for k in range(len(model)):
                if not np.array_equal(model[k], avg_model[k]):
                    is_update_valid = False
                    print(model[k].shape, avg_model[k].shape)
                    # sys.exit(0)
            
            if is_update_valid:
                print("Server OK. Proceeding")
            else:
                print("Server's update doesn't match. Careful!")
        else:
            print("Invalid response from the server:", response.content, "\nSkipping this iteration")
            continue

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

current_time = time.time()
print(f"Total time: {current_time-time1}, {current_time-time2}")