from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql, close_connection


def update_danhmuc(danhmuc_id, ten_moi, mo_ta_moi):
    """
    Hàm cập nhật tên và mô tả của danh mục theo ID.
    """
    connection = connect_mysql()
    if connection is None:
        print("⚠️ Không thể kết nối database để cập nhật danh mục.")
        return False

    try:
        cursor = connection.cursor()
        sql = "UPDATE danhmuc SET ten_danh_muc = %s, mo_ta = %s WHERE id = %s"
        data = (ten_moi, mo_ta_moi, danhmuc_id)
        cursor.execute(sql, data)
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Cập nhật danh mục ID = {danhmuc_id} thành công!")
            return True
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {danhmuc_id}")
            return False

    except Error as e:
        print("❌ Lỗi khi cập nhật danh mục:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            close_connection(connection)


# Test nhanh khi chạy trực tiếp file này
if __name__ == "__main__":
    id = input("Nhập ID danh mục cần sửa: ")
    ten = input("Nhập tên danh mục mới: ")
    mo_ta = input("Nhập mô tả mới: ")
    update_danhmuc(id, ten, mo_ta)
