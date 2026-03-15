[Network] Half Awake - UTCTF 2026
1. Challenge Overview

    Category: Network Forensics

    Points: 100

    Description: SOC captured suspicious traffic from a lab VM. Some packets are "pretending to be something they are not."

    Artifact: challenge.pcap
2. Analysis
    Dựa trên file dowload về khi kiểm tra thì có khá ít gói tin nên mình lần lược kiểm tra.
    Tại TCP stream = 4 mình phát hiện có vào chuỗi nghi ngờ là file zip PK
   Mình thử export nó ra bằng RAW với đuôi .zip nhưng không chuẩn định dạng file
   Sau đó mình export ra file .bin và viết script solve:
   from pathlib import Path

   data = Path("stage2.bin").read_bytes()
  key = bytes([0x00, 0xB7])

  out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
  Path("decoded.txt").write_bytes(out)
  print(out.decode())   
3. Result
  Sau khi thực thi script thì ta có ngay flag : utflag{h4lf_aw4k3_s33_th3_pr0t0c0l_tr1ck}
