import os

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PRIVATE_KEY_ENV_VAR = "SQUARE_PRIVATE_KEY_FILE"


def is_local_deployment():
    """Returns True if the deployment is local, False otherwise."""
    return os.path.exists(os.getenv(PRIVATE_KEY_ENV_VAR, ""))


def get_private_key_file():
    """Returns the path to the private key file for local deployment."""
    return os.getenv(PRIVATE_KEY_ENV_VAR, "private_key.pem")


def generate_and_dump_private_key():
    """Generates a private key and dumps it to the file in SQUARE_PRIVATE_KEY_FILE."""
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    private_key_file = get_private_key_file()

    with open(private_key_file, "wb") as f:
        f.write(pem)


def load_private_key():
    """Load the private key from the file in SQUARE_PRIVATE_KEY_FILE."""
    with open(get_private_key_file(), "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key


def generate_token_pubkey():
    """Generates a token and a public key for local deployment."""
    headers = {}
    payload = {
        "preferred_username": "LOCAL_SQUARE_USER",
        "iss": "/LOCAL_SQUARE_REALM",
        "exp": 9999999999,
    }
    private_key = load_private_key()
    token = jwt.encode(
        headers=headers, payload=payload, key=private_key, algorithm="RS256"
    )

    public_key = private_key.public_key()

    return token, public_key
