from common.insertdanhmuc import insert_danhmuc
while True:
    ten_danh_muc=input("Nhập vào tên danh mục")
    mo_ta=input("Nhập vào mô tả")
    insert_danhmuc(ten_danh_muc, mo_ta)
    con=input("TIẾP TỤC y, Thoát THÌ ẤN KÝ TỰ BẤT KỲ")
    if con != "y":
        break