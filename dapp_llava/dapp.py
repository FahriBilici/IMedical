from os import environ
import logging
import requests
import base64

from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

#rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]

rollup_server = "http://localhost:8080/host-runner"
logger.info(f"HTTP rollup_server url is {rollup_server}")

logging.info("Starting Llava DApp")
chat_handler = Llava15ChatHandler(clip_model_path="mmproj-model-f16.gguf",verbose=True)

llm = Llama(
  model_path="ggml-model-q4_k.gguf",
  chat_handler=chat_handler,
  n_ctx=2048, # n_ctx should be increased to accomodate the image embedding
  logits_all=True,# needed to make llava work
)
logging.info("Llava DApp started")

def read_base64_file(file):
    base64_data = file
    return f"data:image/png;base64,{base64_data}"




def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    data['payload'] = bytes.fromhex(data['payload'][2:]).decode('utf-8')
    print(data['payload'])
    image = read_base64_file(data['payload'])
    response=llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are an assistant who perfectly describes images."},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image}},
                {"type" : "text", "text": "Describe this image in detail please."}
            ]
        }
    ]
)
    
    ethereum_hex = "0x" + response['choices'][0]['message']['content'].encode("utf-8").hex()
    #ethereum_hex = "0x" + data['payload'].encode("utf-8").hex()
    logger.info("Adding notice")
    notice={'payload':ethereum_hex}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return "accept"


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
