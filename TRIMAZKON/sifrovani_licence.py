from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import datetime

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

def make_licence(hwid):
    """
    pro každého uživatele je možné nastavit jeho HW klíč, který se bude ověřovat
    - aby se to nešířilo na více zařízení
    """
    # Načtení soukromého klíče
    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Licence
    licence_data = hwid+"|EXPIRES:31.12.9999"

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
    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Načtení licence a podpisu
    with open("license.lic", "r") as f:
        lines = f.readlines()

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
        exp_date = datetime.datetime.strptime(licence_data.split(":")[1], "%Y-%m-%d")
        if exp_date >= datetime.datetime.today():
            print(f"Licence platná do: {exp_date.date()}")
        else:
            print("Licence EXPIRED!")

    except Exception as e:
        print("Chyba ověření licence!", e)

# generate_rsa_keys()
# make_licence("B841925X0SNLM7S") #kingspan když je tam zasunutej disk
# make_licence("0025_3848_41A1_B7DF") #kingspan
# make_licence("E823_8FA6_BF53_0001_001B_444A_4876_94E7") #asus ntb
# make_licence("E823_8FA6_BF53_0001_001B_444A_48F0_774B") #honza ntb
make_licence("ACE4_2E00_314A_D20C_2EE4_AC00_0000_0001") #zdenda bervid ntb

# make_licence("FSB5N690910705S61_00000001") #dell ntb pracovni
# check_licence()