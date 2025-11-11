import mysql.connector
from mysql.connector import Error

def connect_mysql():
    """
    Hàm kết nối đến MySQL Database
    Trả về đối tượng connection nếu kết nối thành công, ngược lại trả về None.
    """
    try:
        # Thông tin kết nối CSDL
        connection = mysql.connector.connect(
            host='127.0.0.1',        # Địa chỉ server (thường là localhost)
            user='root',             # Tên đăng nhập MySQL
            password='',       # Mật khẩu MySQL
            database='qlthuocankhang11'    # Tên database muốn kết nối
        )

        # Kiểm tra trạng thái kết nối
        if connection.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return connection

    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None


def close_connection(connection):
    """
    Đóng kết nối MySQL an toàn
    """
    if connection and connection.is_connected():
        connection.close()
        print("🔒 Đã đóng kết nối MySQL.")
