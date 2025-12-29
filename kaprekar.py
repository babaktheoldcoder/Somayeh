

def kaprekar(num):
    largest = ''.join(sorted(num, reverse=True))
    smallest = ''.join(sorted(num))
    difference = int(largest) - int(smallest)
    print(f"Largest number: {largest}")
    print(f"Smallest number: {smallest}")
    print(f"Difference: {difference}")  
    print("-------------------------")
    return difference

num = input("Enter a 4-digit number (not all digits the same): ")
if len(num) != 4 or len(set(num)) == 1 or not num.isdigit():
    print("Invalid input. Please enter a 4-digit number (digits only) and not all digits the same (e.g., 1111).")
    exit()

step = 0
while num != "6174":
    step += 1
    print(f"Step {step}:")
    num = str(kaprekar(num)).zfill(4)
    print(f"Next number: {num}")
print(f"Reached Kaprekar's constant 6174! in {step} steps.")