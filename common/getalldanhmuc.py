from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql, close_connection


def get_all_danhmuc():
    """
    Hàm lấy danh sách tất cả danh mục trong bảng danhmuc.
    Trả về danh sách tuple (id, ten_danh_muc, mo_ta, ngay_tao)
    """
    connection = connect_mysql()
    if connection is None:
        print("⚠️ Không thể kết nối database để lấy danh sách danh mục.")
        return []

    try:
        cursor = connection.cursor()
        sql = "SELECT id, ten_danh_muc, mo_ta, ngay_tao FROM danhmuc ORDER BY id ASC"
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            print("📋 Danh sách danh mục:")
            print("-" * 60)
            for row in results:
                print(f"ID: {row[0]} | Tên: {row[1]} | Mô tả: {row[2]} | Ngày tạo: {row[3]}")
            print("-" * 60)
        else:
            print("⚠️ Chưa có danh mục nào trong cơ sở dữ liệu.")

        return results

    except Error as e:
        print("❌ Lỗi khi truy vấn danh mục:", e)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            close_connection(connection)


# Test nhanh khi chạy trực tiếp file này
if __name__ == "__main__":
    get_all_danhmuc()
