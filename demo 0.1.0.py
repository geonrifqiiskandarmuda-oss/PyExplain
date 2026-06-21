import tkinter as tk
import io
import contextlib

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

def run_code():
    code = code_box.get("1.0", tk.END)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

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

    output_box.insert("1.0", result)
    output_box.config(state="disabled")

run_button = tk.Button(root, text="Run", command=run_code, width=20, height=2)
run_button.pack(side="bottom")

root.mainloop()