from pkg.calculator import Calculator
from pkg.render import render

calculator = Calculator()
expression = "3 + 7 * 2"
result = calculator.evaluate(expression)
to_print = render(expression, result)
print(to_print)