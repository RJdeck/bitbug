import os
from sre_constants import MIN_REPEAT
import requests
import dotenv
dotenv.load_dotenv()

BLOCKCHAIR_API_KEY = os.environ.get('BLOCKCHAIR_API_KEY')


def bit_crawl_blocks():
    # Blockchair API URL
    current_url = 'https://api.blockchair.com/bitcoin/stats&key=' + \
        BLOCKCHAIR_API_KEY  # type: ignore

    # Get current block height from API
    response = requests.get(current_url)
    response.raise_for_status()
    data = response.json()
    current_block_height = int(data['data']['blocks']) - 1

    # Create last crawled block height file if it does not exist
    if not os.path.exists('bit_last_crawled_block_height.txt'):
        with open('bit_last_crawled_block_height.txt', 'w') as f:
            f.write(str(current_block_height-20))

    # Load last crawled block height from file
    with open('bit_last_crawled_block_height.txt', 'r+') as f:
        last_block_height = int(f.read())
        # Clear file before writing new data
        f.seek(0)
        f.truncate()
        block_dict = {'block_id': [], 'miner': []}
        for block_height in range(last_block_height + 1, current_block_height + 1):
            interval_url = 'https://blockchain.info/block-height/' + \
                str(block_height) + '?format=json&key=' + \
                BLOCKCHAIR_API_KEY  # type: ignore
            try:
                # Get interval between last crawled block and current block
                response = requests.get(interval_url)
                response.raise_for_status()
                block_info = response.json()
                # try to get miner address from ["out"][0]
                for i in range(len(block_info["blocks"][0]["tx"][0]["out"])):
                    if "addr" in block_info["blocks"][0]["tx"][0]["out"][i]:
                        miner_address = block_info["blocks"][0]["tx"][0]["out"][i]["addr"]
                        # add info into dict
                        block_dict['block_id'].append(block_height)
                        block_dict['miner'].append(miner_address)

            except (requests.exceptions.RequestException, ValueError) as e:
                print(f'Error crawling data: {e}')
                block_dict['block_id'].append(block_height)
                block_dict['miner'].append('Error crawling data')
        # Write current block height to file for next crawl
        f.write(str(current_block_height))
        f.flush()
        os.fsync(f.fileno())
    return block_dict


if __name__ == '__main__':
    res = bit_crawl_blocks()
    print(res)