import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

selected_files = []

def add_files():
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if files:
        for file in files:
            selected_files.append(file)
            file_listbox.insert(tk.END, file)

def delete_selected():
    selected_index = file_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        selected_files.pop(index)
        file_listbox.delete(index)
    else:
        messagebox.showwarning("No Selection", "Select a file to delete.")

def clear_list():
    selected_files.clear()
    file_listbox.delete(0, tk.END)

def move_up():
    index = file_listbox.curselection()
    if index and index[0] > 0:
        i = index[0]
        selected_files[i], selected_files[i-1] = selected_files[i-1], selected_files[i]
        file_listbox.delete(0, tk.END)
        for file in selected_files:
            file_listbox.insert(tk.END, file)
        file_listbox.select_set(i-1)

def move_down():
    index = file_listbox.curselection()
    if index and index[0] < len(selected_files) - 1:
        i = index[0]
        selected_files[i], selected_files[i+1] = selected_files[i+1], selected_files[i]
        file_listbox.delete(0, tk.END)
        for file in selected_files:
            file_listbox.insert(tk.END, file)
        file_listbox.select_set(i+1)

def merge_files():
    if not selected_files:
        messagebox.showwarning("No Files", "Please add at least one PDF file.")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save merged PDF as"
    )

    if not output_path:
        return

    try:
        merger = PdfMerger()
        for pdf in selected_files:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        messagebox.showinfo("Success", f"Merged PDF saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")

# GUI setup
root = tk.Tk()
root.title("PDF Merger with Reordering")
root.geometry("650x400")

tk.Label(root, text="📁 Select and arrange PDFs in the order you want to merge").pack(pady=5)

file_listbox = tk.Listbox(root, width=80, height=10)
file_listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="➕ Add PDFs", width=15, command=add_files).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="❌ Delete Selected", width=15, command=delete_selected).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="⬆️ Move Up", width=15, command=move_up).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="⬇️ Move Down", width=15, command=move_down).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="🧹 Clear All", width=15, command=clear_list).grid(row=0, column=4, padx=5)

tk.Button(root, text="🔀 Merge PDFs", width=20, height=2, command=merge_files).pack(pady=20)

root.mainloop()
