[Network] Half Awake - UTCTF 2026
1. Challenge Overview

    Category: Network Forensics

    Points: 100

    Description: "SOC captured suspicious traffic from a lab VM. Some packets are 'pretending to be something they are not'."

    Artifact: challenge.pcap

2. Analysis & Observation

Dựa trên file tải về, mình nhận thấy lượng gói tin khá ít nên đã tiến hành kiểm tra lần lượt các luồng dữ liệu.

Tại TCP Stream 4, mình phát hiện các chuỗi ký tự nghi ngờ là định dạng của file nén (Magic bytes PK). Ban đầu, mình thử export dữ liệu dưới dạng RAW với đuôi .zip nhưng file thu được không đúng cấu trúc chuẩn (do bị lẫn các byte rác của giao thức giả mạo).

Tiếp tục phân tích kỹ hơn nội dung bên trong, mình tìm thấy file nhị phân stage2.bin. Mình quyết định export riêng file này ra để tiến hành giải mã.
3. Exploitation (Solving Script)

Nhận thấy dữ liệu trong stage2.bin có dấu hiệu bị mã hóa XOR đơn giản, mình sử dụng script Python sau để khôi phục nội dung gốc với key tìm được là [0x00, 0xB7]:
Python

from pathlib import Path

# Đọc dữ liệu từ file đã trích xuất
data = Path("stage2.bin").read_bytes()
key = bytes([0x00, 0xB7])

# Giải mã bằng phép toán XOR tuần hoàn
out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

# Lưu kết quả và in Flag
Path("decoded.txt").write_bytes(out)
print("Decoded content:")
print(out.decode(errors='ignore').strip())

4. Result

Sau khi thực thi script, mình đã thu được Flag hoàn chỉnh:

Flag: utflag{h4lf_aw4k3_s33_th3_pr0t0c0l_tr1ck}
