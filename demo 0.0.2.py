print("=== PyExplain v0.0.2 ===")

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


while True:
    code = input("\nEnter Python code (or type exit): ")

    if code.lower() == "exit":
        break

    try:
        exec(code)

    except Exception as e:
        print("\n=== PyExplain ===")
        print(explain_error(e))

        print("\nTechnical details:")
        print(e)