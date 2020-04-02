# FL with Blockchain

Blockchain implementation from [github.com/satwikkansal](https://github.com/satwikkansal/python_blockchain_app).

## Instructions to run

Install the dependencies,

```sh
pip install -r requirements.txt
```

Start the FL server

```sh
# Windows users can follow this: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
python3 node_server.py
```

Start the FL client

```sh
python3 node_client.py
```

The server now runs on port `8000` and the client at `8001`.
<!-- <br> -->
Register the client with the server using

```sh
curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

The above step is very important for the blockchain setup. Now the server and the client are the nodes of the blockchain network.

In a separate terminal, run `python3 client.py`. This will start the training of the model.

The chain and the peers of the nodes can be inspected by invoking `/chain` and `/peers` endpoints respectively, using cURL.

```sh
curl -X GET http://localhost:8000/chain
curl -X GET http://localhost:8001/chain
```
