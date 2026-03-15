Writeup: UTCTF 2026 - Insanity Check: Hat Trick Denied

Phân loại: Misc

Tác giả: Caleb (@eden.caleb.a)

Mô tả thử thách

After a gap year, the sequel to "Insanity Check: Redux" and "Insanity Check: Reimagined" is finally here!

The flag is in CTFd, but, as always, you'll have to work for it.

(This challenge does not require any brute-force -- as per the rules of the competition, brute-force tools like dirbuster are not allowed, there is a clear solution path without it if you know where to look.)

By Caleb (@eden.caleb.a on discord)

Phân tích ban đầu và các bẫy tâm lý (Red Herrings)

Thử thách này được thiết kế như một "Hat Trick" với các bẫy tâm lý nhằm đánh lạc hướng người chơi:

    Bẫy ID 244: Trong mã nguồn HTML của trang Challenges có một đoạn script MutationObserver được thiết kế để xóa nút thử thách có ID 244. Điều này khiến nhiều người chơi tập trung tìm cách khôi phục hoặc gọi API đến ID này, nhưng kết quả chỉ nhận được 404 Not Found.

    Bẫy Unicode Steganography: Trong dữ liệu JSON của các thử thách, challenge ID 25 ("Hidden in Plain Sight") có chứa các ký tự Unicode Tags ẩn. Khi giải mã các ký tự này, ta nhận được một flag giả: utflag{1nv1s1bl3_un1c0d3}.

Quá trình giải quyết
1. Thu thập thông tin

Quay lại những kiến thức cơ bản về bảo mật web, tôi kiểm tra file robots.txt của nền tảng:
Plaintext

User-agent: *
Disallow: /admin
Disallow: /2065467898
Disallow: /3037802467

Hai đường dẫn số lạ bị cấm index gợi ý rằng chúng chứa dữ liệu thực sự của thử thách.
2. Thu thập dữ liệu

Bằng cách kiểm tra mã nguồn (View Source) của hai đường dẫn ẩn trên, tôi phát hiện hai dãy số nguyên được giấu trong các comment HTML:

    Đường dẫn /2065467898 (Ciphertext):
    2, 7, 9, 7, 8, 13, 17, 39, 85, 4, 57, 4, 93, 30, 104, 27, 44, 23, 89, 8, 30, 68, 107, 112, 54, 0, 30, 11, 2, 92, 66, 23, 31

    Đường dẫn /3037802467 (XOR Key):
    119, 115, 111, 107, 105, 106, 106, 110, 114, 105, 102, 106, 50, 106, 55, 122, 115, 101, 54, 106, 113, 48, 52, 57, 105, 112, 108, 100, 111, 53, 49, 114, 98

3. Khai thác (Exploitation)

Flag được khôi phục bằng cách thực hiện phép toán bitwise XOR giữa hai dãy số trên theo từng vị trí tương ứng.

Script giải mã (solve.py):
Python

cipher = [2, 7, 9, 7, 8, 13, 17, 39, 85, 4, 57, 4, 93, 30, 104, 27, 44, 23, 89, 8, 30, 68, 107, 112, 54, 0, 30, 11, 2, 92, 66, 23, 31]
key = [119, 115, 111, 107, 105, 106, 106, 110, 114, 105, 102, 106, 50, 106, 55, 122, 115, 101, 54, 106, 113, 48, 52, 57, 105, 112, 108, 100, 111, 53, 49, 114, 98]

flag = "".join([chr(c ^ k) for c, k in zip(cipher, key)])
print(f"Flag: {flag}")

Kết quả cuối cùng

Chạy script và thu được flag chính thức:
Bash

$ python3 solve.py
Flag: utflag{I'm_not_a_robot_I_promise}
