print("=== Coding Accessibility Demo ===")

while True:
    code = input("\nEnter Python code (or type exit): ")

    if code.lower() == "exit":
        break

    try:
        exec(code)
    except Exception as e:
        print("\nFriendly explanation:")
        print("Something broke, but here’s the idea:")
        print(e)