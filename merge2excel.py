import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def select_file(entry, combobox, is_first):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        try:
            df = pd.read_excel(file_path)
            columns = df.columns.tolist()
            combobox['values'] = columns
            if is_first:
                global df1_columns
                df1_columns = columns
            else:
                global df2_columns
                df2_columns = columns
        except Exception as e:
            messagebox.showerror("Error", f"Error reading {file_path}: {str(e)}")

def merge_files():
    file1 = entry1.get()
    file2 = entry2.get()
    key1 = combobox1.get()
    key2 = combobox2.get()
    join_type = join_combobox.get()

    if not file1 or not file2 or not key1 or not key2 or not join_type:
        messagebox.showerror("Error", "请选择两个excel文件, 合并依据字段, 合并类型.")
        return

    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        merged_df = pd.merge(df1, df2, left_on=key1, right_on=key2, how=join_type)
        
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls")])
        if save_path:
            merged_df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"合并文件保存在 {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 创建主窗口
root = tk.Tk()
root.title("合并Excel")

df1_columns = []
df2_columns = []

# 文件1选择
tk.Label(root, text="选择第一个 Excel 文件:").grid(row=0, column=0, padx=10, pady=10)
entry1 = tk.Entry(root, width=50)
entry1.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="文件", command=lambda: select_file(entry1, combobox1, True)).grid(row=0, column=2, padx=10, pady=10)

# Join key1选择
tk.Label(root, text="选择第1个表的合并依据字段:").grid(row=1, column=0, padx=10, pady=10)
combobox1 = ttk.Combobox(root, width=47)
combobox1.grid(row=1, column=1, padx=10, pady=10)

# 文件2选择
tk.Label(root, text="选择第二个 Excel 文件:").grid(row=2, column=0, padx=10, pady=10)
entry2 = tk.Entry(root, width=50)
entry2.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="文件", command=lambda: select_file(entry2, combobox2, False)).grid(row=2, column=2, padx=10, pady=10)

# Join key2选择
tk.Label(root, text="选择第2个表的合并依据字段::").grid(row=3, column=0, padx=10, pady=10)
combobox2 = ttk.Combobox(root, width=47)
combobox2.grid(row=3, column=1, padx=10, pady=10)

# Join方式选择
tk.Label(root, text="选择合并类型:").grid(row=4, column=0, padx=10, pady=10)
join_combobox = ttk.Combobox(root, values=["left", "right", "inner", "outer"], width=47)
join_combobox.grid(row=4, column=1, padx=10, pady=10)

# 合并按钮
tk.Button(root, text="合并", command=merge_files).grid(row=5, column=1, pady=20)

# 运行主循环
root.mainloop()
