def describe_user(name, age):
    if age >= 18:
        status = "an adult"
    else:
        status = "a minor"
    return f"{name} is {age} years old and is {status}."

try:
    name = input("Enter your name: ")
    age_input = input("Enter your age: ")
    age = int(age_input)
    result = describe_user(name, age)
    print(result)

except ValueError:
    print("Please enter a valid number for age.")
