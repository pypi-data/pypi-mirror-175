import json
import subprocess
from dotenv import load_dotenv

from defi_marketplace_py.constants import Commands
from defi_marketplace_py.utils import create_command


class CliWapper:

    def __init__(self, network: str) -> None:
        self.network = network
        load_dotenv()

    def __execute_command__(self, command_array):
        result = subprocess.run(
            command_array,
            stdout=subprocess.PIPE,
            shell=False
        )

        subprocess_return = result.stdout

        return subprocess_return

    def list_assets(self, search_term: str) -> None:

        page = 0
        total_pages = 1
        files_to_download = []

        while (total_pages > page):
            page += 1

            result = self.__execute_command__(
                create_command(
                    Commands.LIST_ASSETS,
                    {
                        'search_term': search_term,
                        'network': self.network,
                        'page': page
                    }
                )
            )

            result_json = json.loads(result)
            results = json.loads(result_json['data'][0]['results'])
            total_pages = results['totalPages']
            page += 1
            content = results['results']
            files_to_download = [*files_to_download, *content]

        files = []

        for file in files_to_download:
            try:
                start_index = file['serviceEndpoint'].find('did')
                files.append({
                    'fileName': file['attributes']['additionalInformation']['file_name'],
                    'did': file['serviceEndpoint'][start_index:]
                })

            except:
                print('File name does not exit')

        return files

    def download_did(self, did: str, destination: str, account_index: int):
        result = self.__execute_command__(
            create_command(
                Commands.DOWNLOAD_DID,
                {
                    'did': did,
                    'network': self.network,
                    'destination': destination,
                    'accountIndex': account_index
                }
            )
        )


    def publish_dataset(self, dataset_name: str, author: str, subscriptionAddress: str, url: str):
        result = self.__execute_command__(
            create_command(
                command=Commands.PUBLISH_ASSET,
                args={
                    'network': self.network,
                    'name': dataset_name,
                    'author': author,
                    'nftSubscriptionAddress': subscriptionAddress,
                    'price': '0',
                    'urls': url,
                    'contentType': 'text/csv'
                }
            )
        )

        print(result)

    def upload_to_filecoin(self, file_path: str):
        result = self.__execute_command__(
            create_command(
                command=Commands.UPLOAD_TO_FILECOIN,
                args={
                    'file_path': file_path
                }
            )
        )

        json_return = json.loads(result)
        cid = json.loads(json_return['data'][0]['results'])['url']

        return cid
