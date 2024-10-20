import bcrypt  # pip install bcrypt


class Hash():

    """
    - **bcrypt**: Mã hóa mật khẩu người dùng
    - **verify**: Kiểm tra mật khẩu được cung cấp có trùng với mật khẩu đã mã hóa hay không
    """
    # Hash a password using bcrypt
    def bcrypt(password):
        """
        Mã hóa mật khẩu  
        Chuyển đổi dạng str sang byte để xử lý
        """
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    # Check if the provided password matches the stored password (hashed)
    def verify(plain_password, hashed_password):
        """
        Kiểm tra mật khẩu có trùng với mật khẩu đã mã hóa hay không  
        Chuyển đổi dạng str sang byte để xử lý
        """
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password_bytes)