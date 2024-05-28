import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def process_excel(file_path):
    df = pd.read_excel(file_path, header=None)
    df.fillna(method='ffill', inplace=True)
    return df

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        try:
            df = process_excel(file_path)
            # 显示处理后的数据
            show_dataframe(df)
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错: {e}")

def show_dataframe(df):
    top = tk.Toplevel()
    text = tk.Text(top, wrap='none')
    text.pack(expand=1, fill='both')
    
    # 显示DataFrame内容
    text.insert(tk.END, df.to_string())
    
    # 添加滚动条
    scroll_y = tk.Scrollbar(text, orient='vertical', command=text.yview)
    scroll_y.pack(side='right', fill='y')
    text.configure(yscrollcommand=scroll_y.set)
    
    scroll_x = tk.Scrollbar(text, orient='horizontal', command=text.xview)
    scroll_x.pack(side='bottom', fill='x')
    text.configure(xscrollcommand=scroll_x.set)

def create_gui():
    root = tk.Tk()
    root.title("Excel合并单元格处理")
    
    open_button = tk.Button(root, text="打开Excel文件", command=open_file)
    open_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
