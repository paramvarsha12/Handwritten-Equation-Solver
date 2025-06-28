from sympy import symbols, Eq, solve

def evaluate_equation(eq_str):
    eq_str = eq_str.replace('=', '==') if '=' in eq_str else eq_str
    eq_str = eq_str.replace('x', '*') if '=' not in eq_str and 'x' in eq_str else eq_str

    if all(c.isdigit() or c in "+-*/=() " for c in eq_str):
        try:
            result = eval(eq_str.replace('==', ''))
            return f"{eq_str.replace('==', '=')} = {result}"
        except:
            return "Invalid arithmetic expression"

    try:
        variables = ['x', 'y', 'z']
        used_vars = [v for v in variables if v in eq_str]
        if not used_vars:
            return "No solvable variable found"

        var = symbols(used_vars[0])
        left, right = eq_str.split("==")
        equation = Eq(eval(left), eval(right))
        solution = solve(equation, var)
        return f"{used_vars[0]} = {solution[0]}"
    except:
        return "Could not solve equation"
