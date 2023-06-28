from urllib import response
import requests
from service import bitcoin_bug_server
import os
import time
import dotenv
dotenv.load_dotenv()

DATABASE_USER_URL = os.environ.get('DATABASE_USER_URL', 'http://localhost:5000/user')
DATABASE_TX_URL = os.environ.get('DATABASE_TX_URL', 'http://localhost:5000/user')

# get blocks from API
bit_miner_dict = bitcoin_bug_server.bit_crawl_blocks()

# Create json of block_ids and miners
# # sent to dabase one by one
for i in range(len(bit_miner_dict['block_id'])):
    time.sleep(5)
    json = {'minerUsername': bit_miner_dict['miner'][i]}
    print(json)
    response = requests.post(DATABASE_USER_URL, json=json)
    print(response.text)

for i in range(len(bit_miner_dict['block_id'])):
    time.sleep(5)
    json = {'minerUsername': bit_miner_dict['miner'][i]}
    print(json)
    response = requests.post(DATABASE_TX_URL, json=json)
    print(response.text)