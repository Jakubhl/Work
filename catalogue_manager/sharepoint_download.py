import requests
import msal

class database:
    def __init__(self,filename):
        self.file_name = filename
        self.finished = False
        self.output = ""
        self.start_download()

    def start_download(self):
        print(self.file_name)
        client_id = "83536c55-0b9e-4f34-a5ae-e8c03424a57b"
        tenant_id = "be9cc48a-55c9-47c4-a1bc-b2b95a1c09e4"
        cert_thumbprint = "556D88AE0FA5A77BF27594291EE81AEE98FD8AD9"
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        # key_path = "C:/Users/jakub.hlavacek.local/Desktop/kamerove_vybaveni/key.pem"
        # with open(key_path, 'r') as key_file:
        #      private_key = key_file.read()

        private_key ="""REDACTED_PEM"""
        cert = {
            "private_key": private_key.encode(),
            "thumbprint": cert_thumbprint,
        }

        msal_app = msal.ConfidentialClientApplication(
            client_id = client_id,
            authority = authority,
            client_credential = cert,
        )
        try:
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
                # self.file_name = "Book.xlsx"
                # self.file_name = "Sharepoint_databaze.xlsx"
                # self.file_name = "testovani_Kuba.xlsx"
                file_url = f"{sharepoint_site_url}/_api/web/GetFolderByServerRelativeUrl('{document_library_name}')/Files('{self.file_name}')/$value"

                response = requests.get(url=file_url, headers=headers)
                print(response.status_code)
                # print(json.dumps(response.json(),indent = 4))
                if response.status_code == 200:
                    with open(self.file_name, "wb") as local_file:
                        local_file.write(response.content)
                    self.output = f"Databáze komponentů byla úspěšně synchronizována s jhvengcz.sharepoint.com"
                    print(f"Databáze komponentů byla úspěšně synchronizována s jhvengcz.sharepoint.com")
                else:
                    self.output = f"Databázi komponentů se nepodařilo synchronizovat: {response.status_code} - {response.text}"
                    print(f"Databázi komponentů se nepodařilo synchronizovat: {response.status_code} - {response.text}")
            else:
                self.output = "Chyba ověření aplikace na sharepoint"
                print("Chyba ověření aplikace na sharepoint")
        except Exception as e:
            self.output = str(e)

        self.finished = True
