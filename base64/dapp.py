from os import environ
import logging
import requests
import base64
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

#0x70ac08179605AF2D9e75782b8DEcDD3c22aA4D0C

def read_base64_file(file):
    base64_data = file
    return f"data:image/png;base64,{base64_data}"

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    data['payload'] = bytes.fromhex(data['payload'][2:]).decode('utf-8')
    image = read_base64_file(data['payload'])

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
