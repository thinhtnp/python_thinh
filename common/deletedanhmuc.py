from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql, close_connection


def delete_danhmuc(danhmuc_id):
    """
    Hàm xóa một danh mục khỏi bảng danhmuc theo ID.
    """
    connection = connect_mysql()
    if connection is None:
        print("⚠️ Không thể kết nối database để xóa danh mục.")
        return False

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM danhmuc WHERE id = %s"
        cursor.execute(sql, (danhmuc_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã xóa danh mục có ID = {danhmuc_id}")
            return True
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {danhmuc_id}")
            return False

    except Error as e:
        print("❌ Lỗi khi xóa danh mục:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            close_connection(connection)


# Test nhanh khi chạy file này trực tiếp
if __name__ == "__main__":
    danhmuc_id = input("Nhập ID danh mục muốn xóa: ")
    delete_danhmuc(danhmuc_id)
