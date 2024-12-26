import os
import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Text, Button, Toplevel, StringVar, OptionMenu


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


def format_size(size_bytes):
    """Format file size in human-readable units."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.2f} MB"
    elif size_bytes < 1024 ** 4:
        return f"{size_bytes / 1024 ** 3:.2f} GB"
    else:
        return f"{size_bytes / 1024 ** 4:.2f} TB"


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

    def copy_without_results_line():
        content = "\n".join(result.splitlines()[1:])  # Remove the first line ("Results:")
        copy_to_clipboard(content)

    copy_button = Button(result_win, text="Copy to Clipboard", command=copy_without_results_line)
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

    algorithm_var = StringVar()
    algorithm_var.set("sha1")  # Set default value

    algorithm_window = Toplevel(root)
    algorithm_window.title("Select Hash Algorithm")
    tk.Label(algorithm_window, text="Select a hash algorithm:").pack(padx=10, pady=10)

    OptionMenu(algorithm_window, algorithm_var, "sha1", "sha256", "sha384", "sha512", "All").pack(padx=10, pady=10)

    def on_algorithm_selected():
        algorithm_window.destroy()
        selected_algorithm = algorithm_var.get()

        algorithms_to_apply = []
        if selected_algorithm == "All":
            algorithms_to_apply = ["sha1", "sha256", "sha384", "sha512"]
        else:
            algorithms_to_apply = [selected_algorithm]

        result = "Results:\n"

        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            result += f"File: {os.path.basename(path)}\n"
            for algo in algorithms_to_apply:
                result += f"{algo.upper()}: {calculate_hash(path, algo)}\n"
            result += f"Size: {format_size(file_size)}\n\n"
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file_name in files:
                    full_file_path = os.path.join(root, file_name)
                    file_size = os.path.getsize(full_file_path)
                    result += f"File: {file_name}\n"
                    for algo in algorithms_to_apply:
                        result += f"{algo.upper()}: {calculate_hash(full_file_path, algo)}\n"
                    result += f"Size: {format_size(file_size)}\n\n"

        display_results(result)

    Button(algorithm_window, text="OK", command=on_algorithm_selected).pack(pady=10)


root = tk.Tk()
root.withdraw()  # Hide the main window
prompt_for_input()
root.mainloop()
