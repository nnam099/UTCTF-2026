from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# Extracted from your strings output
encd_b64 = "S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9woKXj5IzcU2C/Ft5u705bY3b6/Z/Q/N6MPLXV55pLzIDnO1nvtja123WWwH54O4mnyWNspt5"
enck_b64 = "Ddf4BCsshqFHJxXPr5X6MLPOGtITAmXK3drAqeZoFBU="
encv_b64 = "xXpGwuoqihg/QHFTM2yMxA=="

# Decode from Base64
ciphertext = base64.b64decode(encd_b64)
key = base64.b64decode(enck_b64)
iv = base64.b64decode(encv_b64)

# Setup AES-CBC Decryption
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Write the result to a file
with open("flag_recovered.jpg", "wb") as f:
    f.write(plaintext)

print("Decryption complete! Check flag_recovered.jpg")
