from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import datetime
import os

def generate_rsa_keys():
    """
    pouze jednou pro vygenerovani klicu
    """
    # Vygenerování RSA klíčů
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Uložení soukromého klíče
    with open("private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Uložení veřejného klíče
    with open("public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("RSA klíče byly vygenerovány.")

def make_licence(hwid, expiration_date="31.12.9999"):
    """
    pro každého uživatele je možné nastavit jeho HW klíč, který se bude ověřovat
    - aby se to nešířilo na více zařízení
    """
    # Načtení soukromého klíče
    try:
        with open("private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        print("Chyba načítání soukromého klíče:", e)
        return

    # Licence
    # licence_data = hwid+"|EXPIRES:31.12.9999"
    licence_data = hwid+"|EXPIRES:" + expiration_date

    # Podepsání licence soukromým klíčem
    signature = private_key.sign(
        licence_data.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    # Uložení licence a podpisu do souboru
    with open("license.lic", "w") as f:
        f.write(licence_data + "\n")
        f.write(signature.hex())

    # with open("license.txt", "w") as f:

    print("Licence byla podepsána a uložena.")

def check_licence():
    # Načtení veřejného klíče
    try:    
        with open("public.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
    except Exception as e:
        print("Chyba načítání veřejného klíče:", e)
        return False

    # Načtení licence a podpisu
    try:
        with open("license.lic", "r") as f:
            lines = f.readlines()
    except Exception as e:
        print("Chyba načítání licence:", e)
        return False

    # with open("license.sig", "rb") as f:
    #     signature = f.read()

    # Ověření podpisu
    licence_data = lines[0].strip()  # První řádek je expirace
    signature = bytes.fromhex(lines[1].strip())  # Druhý řádek je podpis

    # Ověření podpisu
    try:
        public_key.verify(
            signature,
            licence_data.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        
        # Ověření expirace
        # exp_date = datetime.datetime.strptime(licence_data.split(":")[1], "%Y-%m-%d")
        exp_date = datetime.datetime.strptime(licence_data.split(":")[1], "%d.%m.%Y")
        if exp_date >= datetime.datetime.today():
            print(f"Licence platná do: {exp_date.date()}")
        else:
            print("Licence EXPIRED!")
        return True

    except Exception as e:
        print("Chyba ověření licence!", e)
        return True

if __name__ == "__main__":
    hwid = input("Zadejte HWID pro vytvoření licence: ")
    format_ok = False;
    while format_ok == False:
        expiration = input("Zadejte datum expirace licence (dd.mm.yyyy): ")
        try:
            datetime.datetime.strptime(expiration, "%d.%m.%Y")
            format_ok = True
        except ValueError:
            print("Neplatný formát data. Zadejte datum ve formátu dd.mm.yyyy:")

    make_licence(hwid.replace(" ", "").upper(), expiration)

    if(check_licence()):
        os.startfile(os.getcwd())
        ok = input("Licence vytvořena...")
    else:
        ok = input("Vytvoření licence selhalo!")
