import os
import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Text, Button, Toplevel


def calculate_hash(file_path, algorithm):
    """Calculate the hash of a file using the specified algorithm."""
    BUF_SIZE = 65536  # reading in 64kb chunks
    hasher = None
    if algorithm == "sha1":
        hasher = hashlib.sha1()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    elif algorithm == "sha384":
        hasher = hashlib.sha384()
    elif algorithm == "sha512":
        hasher = hashlib.sha512()
    
    with open(file_path, 'rb') as file:
        buf = file.read(BUF_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BUF_SIZE)
    return hasher.hexdigest()


def copy_to_clipboard(content):
    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()
    messagebox.showinfo("Info", "Results copied to clipboard!")


def save_to_file(content):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save as", filetypes=[("Text files", "*.txt")])
    if not save_path:
        return
    with open(save_path, "w") as file:
        file.write(content)


def display_results(result):
    """Display the results in a new window with copy and save buttons."""
    result_win = Toplevel(root)
    result_win.title("Hash Results")
    
    text_widget = Text(result_win, wrap=tk.WORD)
    text_widget.insert(tk.END, result)
    text_widget.pack(padx=10, pady=10)

    copy_button = Button(result_win, text="Copy to Clipboard", command=lambda: copy_to_clipboard(text_widget.get(1.0, tk.END)))
    copy_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_button = Button(result_win, text="Save to File", command=lambda: save_to_file(text_widget.get(1.0, tk.END)))
    save_button.pack(side=tk.LEFT, padx=10, pady=10)


def prompt_for_input():
    """Prompt the user for input and compute the hash."""
    path = filedialog.askopenfilename(title="Select a file or directory")

    if os.path.isdir(path):
        answer = messagebox.askyesno("Multiple Files", "You've selected a directory. Generating hashes for multiple files might take a while. Continue?")
        if not answer:
            return

    algorithm = simpledialog.askstring("Algorithm", "Choose an algorithm:\n1. sha1\n2. sha256\n3. sha384\n4. sha512\n5. All of the above", initialvalue="1")

    algorithms_to_apply = []
    if algorithm == "1":
        algorithms_to_apply = ["sha1"]
    elif algorithm == "2":
        algorithms_to_apply = ["sha256"]
    elif algorithm == "3":
        algorithms_to_apply = ["sha384"]
    elif algorithm == "4":
        algorithms_to_apply = ["sha512"]
    elif algorithm == "5":
        algorithms_to_apply = ["sha1", "sha256", "sha384", "sha512"]

    result = "Results:\n"

    if os.path.isfile(path):
        result += f"File: {os.path.basename(path)}\n"
        for algo in algorithms_to_apply:
            result += f"{algo.upper()}: {calculate_hash(path, algo)}\n\n"
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file_name in files:
                full_file_path = os.path.join(root, file_name)
                result += f"File: {file_name}\n"
                for algo in algorithms_to_apply:
                    result += f"{algo.upper()}: {calculate_hash(full_file_path, algo)}\n\n"

    display_results(result)


root = tk.Tk()
root.withdraw()  # Hide the main window
prompt_for_input()
root.mainloop()
