import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xmlrpc.client
import pandas as pd

class OdooApp:
    def __init__(self, root):
        self.root = root
        self.root.title("更新文本字段")

        # URL Entry
        tk.Label(root, text="网站地址:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.url_entry = tk.Entry(root)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Database Entry
        tk.Label(root, text="数据库:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.db_entry = tk.Entry(root)
        self.db_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Username Entry
        tk.Label(root, text="用户名:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Password Entry
        tk.Label(root, text="密码:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Model Entry
        tk.Label(root, text="数据表:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.model_entry = tk.Entry(root)
        self.model_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        # Fetch Fields Button
        self.fetch_button = tk.Button(root, text="点击获取字段", command=self.fetch_fields)
        self.fetch_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Matching Fields Dropdown
        tk.Label(root, text="定位字段:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.matching_fields_combobox = ttk.Combobox(root, state="readonly")
        self.matching_fields_combobox.grid(row=6, column=1, padx=10, pady=5, sticky='w')

        # Updating Fields Dropdown
        tk.Label(root, text="需要更新的字段:").grid(row=7, column=0, padx=10, pady=5, sticky='e')
        self.updating_fields_combobox = ttk.Combobox(root, state="readonly")
        self.updating_fields_combobox.grid(row=7, column=1, padx=10, pady=5, sticky='w')

        # Load Excel Button
        self.load_excel_button = tk.Button(root, text="加载本地excel", command=self.load_excel)
        self.load_excel_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Excel Matching Field Dropdown
        tk.Label(root, text="Excel定位字段:").grid(row=9, column=0, padx=10, pady=5, sticky='e')
        self.excel_matching_fields_combobox = ttk.Combobox(root, state="readonly")
        self.excel_matching_fields_combobox.grid(row=9, column=1, padx=10, pady=5, sticky='w')

        # Excel Updating Field Dropdown
        tk.Label(root, text="Excel 填充字段:").grid(row=10, column=0, padx=10, pady=5, sticky='e')
        self.excel_updating_fields_combobox = ttk.Combobox(root, state="readonly")
        self.excel_updating_fields_combobox.grid(row=10, column=1, padx=10, pady=5, sticky='w')

        # Update Button
        self.update_button = tk.Button(root, text="更新", command=self.update_odoo)
        self.update_button.grid(row=11, column=0, columnspan=2, pady=10)

    def fetch_fields(self):
        url = self.url_entry.get()
        db = self.db_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        model_name = self.model_entry.get()

        if not url or not db or not username or not password or not model_name:
            messagebox.showerror("Error", "请显示所有字段")
            return

        try:
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
                fields = models.execute_kw(db, uid, password, model_name, 'fields_get', [])
                self.field_map = {fields[field]['string']: field for field in fields}
                field_labels = list(self.field_map.keys())
                self.matching_fields_combobox['values'] = field_labels
                self.updating_fields_combobox['values'] = field_labels
                if field_labels:
                    self.matching_fields_combobox.current(0)
                    self.updating_fields_combobox.current(0)
            else:
                messagebox.showerror("Error", "认证出错")
        except Exception as e:
            messagebox.showerror("Error", f"抓取字段失败: {str(e)}")

    def load_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                column_names = list(self.df.columns)
                self.excel_matching_fields_combobox['values'] = column_names
                self.excel_updating_fields_combobox['values'] = column_names
                if column_names:
                    self.excel_matching_fields_combobox.current(0)
                    self.excel_updating_fields_combobox.current(0)
            except Exception as e:
                messagebox.showerror("Error", f"加载excel表失败: {str(e)}")

    def update_odoo(self):
        url = self.url_entry.get()
        db = self.db_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        model_name = self.model_entry.get()
        matching_field_label = self.matching_fields_combobox.get()
        updating_field_label = self.updating_fields_combobox.get()
        excel_matching_field = self.excel_matching_fields_combobox.get()
        excel_updating_field = self.excel_updating_fields_combobox.get()

        if not url or not db or not username or not password or not model_name or not matching_field_label or not updating_field_label or not excel_matching_field or not excel_updating_field:
            messagebox.showerror("Error", "请填入所有字段")
            return

        matching_field = self.field_map.get(matching_field_label)
        updating_field = self.field_map.get(updating_field_label)

        try:
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
                for _, row in self.df.iterrows():
                    search_domain = [(matching_field, '=', row[excel_matching_field])]
                    record_ids = models.execute_kw(db, uid, password, model_name, 'search', [search_domain])
                    if record_ids:
                        values = {updating_field: row[excel_updating_field]}
                        models.execute_kw(db, uid, password, model_name, 'write', [record_ids, values])
                messagebox.showinfo("Success", "更新成功")
            else:
                messagebox.showerror("Error", "认证失败")
        except Exception as e:
            messagebox.showerror("Error", f"更新记录失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OdooApp(root)
    root.mainloop()
