import math
def testcase_import() -> tuple[int, list[int]]:
    with open("test_sol.txt", "r") as f:
        code = f.read()
    syms = [int(x) for x in code.replace("\n", " ").split() if x.isdigit()]
    size = math.isqrt(len(syms))
    if size**2 != len(syms):
        raise ValueError("Invalid number of symbols")
    return size, syms