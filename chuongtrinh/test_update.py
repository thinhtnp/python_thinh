from common.updatedanhmuc import update_danhmuc

while True:
    id = input("Nhập ID danh mục cần sửa: ")
    ten = input("Nhập tên danh mục mới: ")
    mo_ta = input("Nhập mô tả mới: ")

    update_danhmuc(id, ten, mo_ta)

    tieptuc = input("TIẾP TỤC cập nhật? (Y/N): ").upper()
    if tieptuc != "Y":
        break
