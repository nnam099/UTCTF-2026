[Forensics] Cold Workspace - UTCTF 2026
1. Challenge Overview

    Category: Forensics / Memory Analysis

    Description: A workstation crashed, and a critical desktop artifact disappeared. A memory snapshot was taken before the reboot.

    Goal: Recover the lost file.

    Artifact: cold-workspace.dmp (Windows Memory Dump)

2. Initial Reconnaissance

Đầu tiên, mình kiểm tra định dạng file bằng lệnh file để xác nhận đây là một file Crash Dump của Windows:
Bash

$ file cold-workspace.dmp
cold-workspace.dmp: MS Windows 64bit crash dump, version 0.0, MachineImageType 0x74656874...

Sử dụng strings kết hợp grep để tìm kiếm dấu vết của "flag", mình phát hiện một kịch bản PowerShell đáng ngờ đã được thực thi để mã hóa file ảnh trên desktop:
Bash

$ strings cold-workspace.dmp | grep flag

Phát hiện kịch bản:

    powershell.exe -File C:\Users\analyst\Desktop\encrypt_flag.ps1

    $bytes = [System.IO.File]::ReadAllBytes('C:\Users\analyst\Desktop\flag.jpg')

    Set-Content C:\Users\analyst\Desktop\flag.enc $env:ENCD

3. Deep Analysis & Data Extraction

Kịch bản PowerShell cho thấy dữ liệu mã hóa (Ciphertext), Khóa (Key) và IV được lưu trữ trong các biến môi trường ($env:ENCD, $env:ENCK). Mình tiến hành trích xuất logic cụ thể bằng cách xem ngữ cảnh xung quanh hàm ReadAllBytes:
Bash

$ strings cold-workspace.dmp | grep -A 5 "ReadAllBytes"

Output thu được:
PowerShell

$bytes = [System.IO.File]::ReadAllBytes('C:\Users\analyst\Desktop\flag.jpg')
$key = [byte[]](0..31)  # Tương ứng AES-256 (32 bytes)
$iv = [byte[]](0..15)   # Tương ứng Block size 16 bytes
# actual key/iv allocated at runtime, serialized to env vars
$env:ENCD = "..." 
$env:ENCK = "..."

Từ phân tích trên, mình xác định thuật toán sử dụng là AES-256-CBC. Tiếp tục truy vết, mình thu được các chuỗi Base64:

    Ciphertext (ENCD): S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIq

    Key (ENCK): Ddf4BCsshqFHJxXPr5X6MLPOGtITAmXK3drAqeZoFBU=

    IV (ENCV): xXpGwuoqihg/QHFTM2yMxA==

4. Exploitation (Decryption)

Mình viết một script Python sử dụng thư viện cryptography để giải mã dữ liệu và khôi phục file ảnh gốc:
Python

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# Dữ liệu trích xuất từ bộ nhớ
encd_b64 = "S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9woKXj5IzcU2C/Ft5u705bY3b6/Z/Q/N6MPLXV55pLzIDnO1nvtja123WWwH54O4mnyWNspt5"
enck_b64 = "Ddf4BCsshqFHJxXPr5X6MLPOGtITAmXK3drAqeZoFBU="
encv_b64 = "xXpGwuoqihg/QHFTM2yMxA=="

# Giải mã Base64
ciphertext = base64.b64decode(encd_b64)
key = base64.b64decode(enck_b64)
iv = base64.b64decode(encv_b64)

# Cấu hình AES-CBC Decryption
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Lưu kết quả
with open("flag_recovered.jpg", "wb") as f:
    f.write(plaintext)

print("[+] Decryption complete! Check flag_recovered.jpg")

5. Result & Flag

Mở file ảnh đã khôi phục hoặc dùng lệnh strings để kiểm tra:
Bash

$ strings flag_recovered.jpg | grep utflag

Flag: utflag{m3m0ry_r3t41ns_wh4t_d1sk_l053s}
