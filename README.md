# Code snippets for Mono Corp API
API doc: https://api.monobank.ua/docs/corporate.html

To request Mono API corp access:
1. Generate a key:  
`openssl ecparam -genkey -name secp256k1 -rand /dev/urandom -out priv.key`
2. Execute `request_corp` function (provide all the necessary information for it).
