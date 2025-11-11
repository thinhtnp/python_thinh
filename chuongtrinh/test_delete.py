from common.deletedanhmuc import delete_danhmuc

while True:
    id = input("Nhập ID danh mục muốn xóa: ")
    delete_danhmuc(id)
    cont = input("TIẾP TỤC xóa? (Y/N): ").upper()
    if cont != "Y":
        break
