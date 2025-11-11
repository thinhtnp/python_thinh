import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql, close_connection


class DanhMucApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Danh Mục (Tkinter + MySQL)")
        self.geometry("880x520")
        self.resizable(False, False)

        # ====== Form nhập liệu ======
        frm_form = ttk.LabelFrame(self, text="Thông tin danh mục")
        frm_form.pack(fill="x", padx=12, pady=8)

        ttk.Label(frm_form, text="ID:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        ttk.Label(frm_form, text="Tên danh mục:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        ttk.Label(frm_form, text="Mô tả:").grid(row=2, column=0, padx=8, pady=6, sticky="ne")

        self.var_id = tk.StringVar()
        self.ent_id = ttk.Entry(frm_form, textvariable=self.var_id, width=12, state="readonly")
        self.ent_id.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        self.var_ten = tk.StringVar()
        self.ent_ten = ttk.Entry(frm_form, textvariable=self.var_ten, width=50)
        self.ent_ten.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        self.txt_mota = tk.Text(frm_form, width=60, height=4)
        self.txt_mota.grid(row=2, column=1, padx=8, pady=6, sticky="w")

        # ====== Nút chức năng ======
        frm_btn = ttk.Frame(frm_form)
        frm_btn.grid(row=3, column=0, columnspan=2, pady=6, sticky="w")

        self.btn_add = ttk.Button(frm_btn, text="➕ Thêm", command=self.add_dm)
        self.btn_update = ttk.Button(frm_btn, text="📝 Cập nhật", command=self.update_dm)
        self.btn_delete = ttk.Button(frm_btn, text="🗑️ Xóa", command=self.delete_dm)
        self.btn_clear = ttk.Button(frm_btn, text="🧹 Xóa trắng", command=self.clear_form)
        self.btn_reload = ttk.Button(frm_btn, text="🔄 Tải lại", command=self.load_data)

        for i, b in enumerate([self.btn_add, self.btn_update, self.btn_delete, self.btn_clear, self.btn_reload]):
            b.grid(row=0, column=i, padx=6)

        # ====== Bảng danh sách ======
        frm_table = ttk.LabelFrame(self, text="Danh sách danh mục")
        frm_table.pack(fill="both", expand=True, padx=12, pady=8)

        self.tree = ttk.Treeview(frm_table, columns=("id", "ten", "mota", "ngay"), show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("ten", text="Tên danh mục")
        self.tree.heading("mota", text="Mô tả")
        self.tree.heading("ngay", text="Ngày tạo")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("ten", width=220)
        self.tree.column("mota", width=400)
        self.tree.column("ngay", width=160, anchor="center")

        vsb = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Tải dữ liệu lần đầu
        self.load_data()

    # ====== Helpers ======
    def get_current_form(self):
        _id = self.var_id.get().strip() or None
        ten = self.var_ten.get().strip()
        mota = self.txt_mota.get("1.0", "end").strip()
        return _id, ten, mota

    def clear_form(self):
        self.var_id.set("")
        self.var_ten.set("")
        self.txt_mota.delete("1.0", "end")
        self.ent_ten.focus()

    def on_select(self, _evt):
        item = self.tree.focus()
        if not item:
            return
        row = self.tree.item(item, "values")
        self.var_id.set(row[0])
        self.var_ten.set(row[1])
        self.txt_mota.delete("1.0", "end")
        self.txt_mota.insert("1.0", row[2])

    # ====== DB ops ======
    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = connect_mysql()
        if conn is None:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL.")
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, ten_danh_muc, IFNULL(mo_ta,''), ngay_tao FROM danhmuc ORDER BY id DESC")
            for r in cur.fetchall():
                self.tree.insert("", "end", values=r)
        except Error as e:
            messagebox.showerror("Lỗi truy vấn", str(e))
        finally:
            try:
                cur.close()
            except:
                pass
            close_connection(conn)

    def add_dm(self):
        _id, ten, mota = self.get_current_form()
        if not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập TÊN danh mục.")
            self.ent_ten.focus()
            return
        conn = connect_mysql()
        if conn is None:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL.")
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO danhmuc (ten_danh_muc, mo_ta) VALUES (%s, %s)", (ten, mota))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm danh mục: {ten}")
            self.clear_form()
            self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi thêm", str(e))
        finally:
            try:
                cur.close()
            except:
                pass
            close_connection(conn)

    def update_dm(self):
        _id, ten, mota = self.get_current_form()
        if not _id:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn bản ghi cần cập nhật từ danh sách.")
            return
        if not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập TÊN danh mục.")
            return
        conn = connect_mysql()
        if conn is None:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL.")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE danhmuc SET ten_danh_muc=%s, mo_ta=%s WHERE id=%s",
                (ten, mota, _id)
            )
            conn.commit()
            if cur.rowcount:
                messagebox.showinfo("Thành công", f"Đã cập nhật danh mục ID = {_id}")
                self.load_data()
            else:
                messagebox.showwarning("Không có thay đổi", "Không tìm thấy ID để cập nhật.")
        except Error as e:
            messagebox.showerror("Lỗi cập nhật", str(e))
        finally:
            try:
                cur.close()
            except:
                pass
            close_connection(conn)

    def delete_dm(self):
        _id = self.var_id.get().strip()
        if not _id:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn bản ghi cần xóa từ danh sách.")
            return
        if not messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa ID = {_id}?"):
            return

        conn = connect_mysql()
        if conn is None:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL.")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM danhmuc WHERE id=%s", (_id,))
            conn.commit()
            if cur.rowcount:
                messagebox.showinfo("Thành công", f"Đã xóa danh mục ID = {_id}")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", "ID không tồn tại.")
        except Error as e:
            messagebox.showerror("Lỗi xóa", str(e))
        finally:
            try:
                cur.close()
            except:
                pass
            close_connection(conn)


if __name__ == "__main__":
    app = DanhMucApp()
    app.mainloop()
