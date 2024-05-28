import pandas as pd
from tkinter import filedialog, messagebox, Tk
from tkinter.filedialog import askdirectory
import os
import tkinter
def merge_excel_files():
    # Get the selected folder path
    folder_path = askdirectory()
    
    if not folder_path:
        return
    
    # List all Excel files in the folder
    excel_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    if not excel_files:
        messagebox.showinfo('提示', '没有找到 Excel 文件')
        return
    
    # Merge Excel files
    df_list = []
    for file in excel_files:
        df = pd.read_excel(file)
        df_list.append(df)
    
    # Merge dataframes
    merged_df = pd.concat(df_list, ignore_index=True)
    
    # Save the merged result to a new Excel file
    output_file_path = os.path.join(folder_path, 'merged_data.xlsx')
    merged_df.to_excel(output_file_path, index=False)
    
    messagebox.showinfo('提示', f'合并完成，结果保存在 {output_file_path}')

root = Tk()
root.title('Excel 文件合并工具')

# Create a label and button
label = tkinter.Label(root, text='请选择文件夹：')
label.pack()

button = tkinter.Button(root, text='开始合并', command=merge_excel_files)
button.pack()

root.mainloop()