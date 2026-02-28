def sum(num1, num2 : int = 20):
    sum = num1 + num2
    substract = num1 - num2
    return {
        "sum": sum,
        "substract": substract
    }


# num1 = int(input("Enter first number: "))
# num2 = int(input("Enter second number: "))
# result = sum(num2)
# print("The sum of " + str(num1) + " and " + str(num2) + " is: " + str(result["sum"]))
# print("The substraction of " + str(num1) + " and " + str(num2) + " is: " + str(result["substract"]))

# print(result)

result = sum(10, 44)
print(result["sum"])