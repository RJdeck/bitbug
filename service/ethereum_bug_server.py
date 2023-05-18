import os
import requests
import dotenv
dotenv.load_dotenv()

BLOCKCHAIR_API_KEY = os.environ.get('BLOCKCHAIR_API_KEY')


def eth_crawl_blocks():
    # Blockchair API URL
    current_url = 'https://api.blockchair.com/ethereum/blocks?limit=100&key=' + BLOCKCHAIR_API_KEY # type: ignore

    # Get current block height from API
    response = requests.get(current_url)
    response.raise_for_status()
    block_info = response.json()
    block_dict = {'block_id': [], 'miner': []}
    current_block_height = int(block_info['data'][0]['id']) - 1

    # Create last crawled block height file if it does not exist
    if not os.path.exists('eth_last_crawled_block_height.txt'):
        with open('eth_last_crawled_block_height.txt', 'w') as f:
            f.write(str(current_block_height-3))

    # Load last crawled block height from file
    with open('eth_last_crawled_block_height.txt', 'r+') as f:
        last_block_height = int(f.read())
        # Clear file before writing new data
        f.seek(0)
        f.truncate()
        f.write(str(current_block_height))
        f.flush()
        os.fsync(f.fileno())

    for block_height in range(last_block_height + 1, current_block_height + 1):
        block_dict['block_id'].append(block_height)
        block_dict['miner'].append(
            block_info['data'][block_height - last_block_height - 1]['miner'])
    return block_dict


if __name__ == '__main__':
    res = eth_crawl_blocks()
    print(res)
