import requests
import msal
import json

client_id = "83536c55-0b9e-4f34-a5ae-e8c03424a57b"
tenant_id = "be9cc48a-55c9-47c4-a1bc-b2b95a1c09e4"
cert_thumbprint = "556D88AE0FA5A77BF27594291EE81AEE98FD8AD9"
authority = f"https://login.microsoftonline.com/{tenant_id}"
key_path = "C:/Users/jakub.hlavacek.local/Desktop/kamerove_vybaveni/key.pem"
with open(key_path, 'r') as key_file:
     private_key = key_file.read()
cert = {
	"private_key": private_key,
	"thumbprint": cert_thumbprint,
}
msal_app = msal.ConfidentialClientApplication(
    client_id = client_id,
	authority = authority,
	client_credential = cert,
)
result = msal_app.acquire_token_for_client(["https://jhvengcz.sharepoint.com/.default"])
if "access_token" in result:
    access_token = result.get("access_token")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json",
    }
    # sharepoint_site_url = "https://jhvengcz.sharepoint.com/sites/TestikMB"
    sharepoint_site_url = "https://jhvengcz.sharepoint.com/sites/JHV-software"
    # document_library_name = "Sdilene dokumenty"
    document_library_name = "Storage/05_technologie/04_kamery/TEMPLATE FOLDERS"
    # file_name = "Book.xlsx"
    file_name = "KAM_PrehledKomponentu.xlsx"
    # file_name = "testovani_Kuba.xlsx"
    file_url = f"{sharepoint_site_url}/_api/web/GetFolderByServerRelativeUrl('{document_library_name}')/Files('{file_name}')/$value"

    response = requests.get(url=file_url, headers=headers)
    print(response.status_code)
    # print(json.dumps(response.json(),indent = 4))
    if response.status_code == 200:
        with open(file_name, "wb") as local_file:
            local_file.write(response.content)
        print(f"File downloaded successfully")
    else:
        print(f"Failed to download file: {response.status_code} - {response.text}")
else:
    print("Authentication failed")

