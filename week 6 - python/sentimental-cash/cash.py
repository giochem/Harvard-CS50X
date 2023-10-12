import cs50

while True:
    dollars = cs50.get_float("Change owed: ")
    if dollars >= 0:
        cents = int(dollars * 100)
        break

quarters = int(cents / 25)
cents = cents - quarters * 25

dimes = int(cents / 10)
cents = cents - dimes * 10

nickels = int(cents / 5)
cents = cents - nickels * 5

pennies = int(cents / 1)
cents = cents - pennies * 1

coins = quarters + dimes + nickels + pennies
print(coins)
