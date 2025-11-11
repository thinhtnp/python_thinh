from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql, close_connection


def insert_danhmuc(ten_danh_muc, mo_ta):
    """
    Hàm thêm một danh mục mới vào bảng danhmuc.
    """
    connection = connect_mysql()
    if connection is None:
        print("⚠️ Không thể kết nối database để thêm danh mục.")
        return False

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO danhmuc (ten_danh_muc, mo_ta) VALUES (%s, %s)"
        data = (ten_danh_muc, mo_ta)
        cursor.execute(sql, data)
        connection.commit()
        print(f"✅ Đã thêm danh mục: {ten_danh_muc}")
        return True

    except Error as e:
        print("❌ Lỗi khi thêm danh mục:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            close_connection(connection)


# Nếu muốn test trực tiếp file này
if __name__ == "__main__":
    insert_danhmuc("Chăm sóc da", "Sản phẩm giúp chăm sóc và bảo vệ da")
    insert_danhmuc("Thuốc kháng sinh", "Các loại thuốc kháng sinh thông dụng")
