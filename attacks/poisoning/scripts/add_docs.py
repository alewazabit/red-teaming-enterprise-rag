import requests

# Update settings
#USER_NAME = "test_user"   
#USER_PASSWORD = "YOUR_PASSWORD"
localhost = "YOUR_HOST_IP"
PORT = 8000
kb_name = "kb_name_redacted"

file_paths = [
    'data/test_poisoned/documento_client_beta.txt'
]


# 1 - Login to get the token
#login_url = f'http://{localhost}:{PORT}/token'
#login_data = {
#    'grant_type': 'password',
#    'username': USER_NAME,
#    'password': USER_PASSWORD,
#    'scope': '',
#    'client_id': 'string',
 #   'client_secret': 'string'
#}

#login_headers = {
#    'accept': 'application/json',
#    'Content-Type': 'application/x-www-form-urlencoded'
#}

#response = requests.post(url=login_url, data = login_data, headers=login_headers)
#response.raise_for_status()
output_token = "YOUR_TOKEN_HERE"


# 2 - Run and injest
upload_url = f"http://localhost:{PORT}/kb/upload_and_ingest?kb_name={kb_name}"


upload_headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {output_token}',
}


for file_path in file_paths:
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path.split('/')[-1], file, 'text/plain')
        }
        response = requests.post(upload_url, headers=upload_headers, files=files)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"File {file_path} uploaded and ingested successfully.")

