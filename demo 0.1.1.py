import tkinter as tk
import io
import contextlib
import threading

def explain_error(error):
    error_name = type(error).__name__
    error_text = str(error)

    if error_name == "SyntaxError":
        if "unterminated string literal" in error_text:
            return "You forgot to close a quote (\") or (')."

        return "Python cannot understand how this line is written."

    elif error_name == "NameError":
        return "You used a variable or function that does not exist yet."

    elif error_name == "IndentationError":
        return "The spacing at the beginning of a line is incorrect."

    elif error_name == "ZeroDivisionError":
        return "You tried to divide by zero."

    elif error_name == "TypeError":
        return "You tried to use the wrong type of data for this operation."
    
    elif error_name == "IndexError":
        return "You tried to access an item at a position that doesn't exist in your list."

    elif error_name == "KeyError":
        return "You tried to look up a key in a dictionary that doesn't exist."

    elif error_name == "AttributeError":
        return "You tried to use a feature or action that doesn't exist on this type of data."

    elif error_name == "ValueError":
        return "You gave the right type of data, but the value doesn't make sense here."

    elif error_name == "FileNotFoundError":
        return "Python couldn't find the file you're trying to open. Check the filename and location."

    elif error_name == "MemoryError":
        return "Your program tried to use more memory than your computer can handle."

    return error_text


def get_error_line(error):
    if isinstance(error, SyntaxError):
        return error.lineno

    tb = error.__traceback__
    last_lineno = None
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == "<string>":
            last_lineno = tb.tb_lineno
        tb = tb.tb_next
    return last_lineno


root = tk.Tk()
root.title("===PyExplain===")
root.geometry("800x600")

code_box = tk.Text(root, font=("consolas", 11))
code_box.pack(expand=True, fill="both")

output_box = tk.Text(root, font=("consolas", 11), height=8, bg="#f0f0f0")
output_box.pack(expand=True, fill="both")
output_box.insert("1.0", "Output will show up here...")
output_box.config(state="disabled")

def update_output(result):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", result)
    output_box.config(state="disabled")

def check_timeout(thread):
    if thread.is_alive():
        update_output("=== PyExplain ===\nYour code took too long to run. You might have an infinite loop!")

def run_code():
    code = code_box.get("1.0", tk.END)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", "Running...")
    output_box.config(state="disabled")

    def execute():
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                exec(code)
            result = captured.getvalue()
            if not result:
                result = "(ran with no output)"
        except Exception as e:
            lineno = get_error_line(e)
            result = "=== PyExplain ===\n"
            if lineno is not None:
                result += f"Line {lineno}:\n"
            result += explain_error(e) + "\n\n"
            result += "Technical details:\n"
            result += str(e)

        root.after(0, update_output, result)

    thread = threading.Thread(target=execute, daemon=True)
    thread.start()
    root.after(5000, lambda: check_timeout(thread))

run_button = tk.Button(root, text="Run", command=run_code, width=20, height=2)
run_button.pack(side="bottom")

root.mainloop()