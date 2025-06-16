def format_number(val):
    try:
        n = float(val)
        if not n.is_integer():
            return f"#{n}"
        if 0 <= n < 399:
            return f"#{int(n)}"
        return str(int(n))
    except:
        return str(val)
