import codeop

print("=== PyExplain v0.0.3 ===")


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


def print_error(error):
    print("/n=== PyExplain ===")
    print(explain_error(error))

    print("/nTechnical details")
    print(error)


buffer = ""
    
while True:
    # "..." shows up while we're still waiting on more lines
    # (e.g. mid def/for/if block) instead of running half a statement
    prompt = "... " if buffer else "\nEnter Python code (or type exit): "
    line = input(prompt)
 
    if line.lower() == "exit" and not buffer:
        break
 
    buffer += line + "\n"
 
    try:
        # None        -> statement is incomplete, keep collecting lines
        # code object -> statement is complete, ready to run
        # raises      -> statement is just plain broken
        code_obj = codeop.compile_command(buffer, "<input>", "exec")
    except (SyntaxError, OverflowError, ValueError) as e:
        print_error(e)
        buffer = ""
        continue
 
    if code_obj is None:
        continue
 
    try:
        exec(code_obj)
    except Exception as e:
        print_error(e)
 
    buffer = ""
 
