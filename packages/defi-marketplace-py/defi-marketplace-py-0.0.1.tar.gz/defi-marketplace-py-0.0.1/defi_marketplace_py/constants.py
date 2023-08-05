class Commands:
    INSTALL_CLI = 'npm install -g @nevermined-io/cli'
    LIST_ASSETS = 'ncli assets search {search_term} -n {network} --page {page} --json --onlyMetadata'
    DOWNLOAD_DID = 'ncli -n {network} -v nfts721 access {did} --destination {destination} --accountIndex {accountIndex} --json'
    PUBLISH_ASSET = """ncli -n {network} -v nfts721 create 
    {nftSubscriptionAddress} 
    --name {name} --author {author} --price {price} --urls {urls} 
    --contentType {contentType} --services nft-access --json"""
    UPLOAD_TO_FILECOIN = 'ncli utils upload {file_path} --json'


class AddressProvider:
    NFT_SUBSCRIPTION = {
        'local': '0xEBe77E16736359Bf0F9013F6017242a5971cAE76',
        'Mumbai': '0x3cAD3F3bF241757808790EA7A64A41949fCA8F6c'
    }
    GATEWAY_HOST = {
        'local': 'http://localhost:8030',
        'Mumbai': 'https://gateway.mumbai.public.nevermined.network'
    }

