import gmpy2
import os
import sys

no_of_points = 0

def find_the_order(a, b, p, x, y):
    """
    Call an external script to find the order of a point on the elliptic curve.
    """
    # Construct the command to call the external script
    cmd = f"./find_order_of_a_point {a} {b} {p} {x} {y}"
    
    # Execute the command using the system shell
    os.system(cmd)

def check_prime(m):
    """
    Check if m is a prime, if not, find the next prime.
    
    Args:
        m (gmpy2.mpz): The number to check.
        
    Returns:
        int: 1 if m or the next found prime is prime.
    """
    modprime = gmpy2.mpz(0)
    temp = gmpy2.mpz(0)

    # If m is already prime, return 1
    if gmpy2.is_prime(m, 500):
        return 1
    else:
        # Increment m by 1 and check for the next prime
        m += 1
        while True:
            if gmpy2.is_prime(m, 500):
                return 1
            else:
                m += 1

def find_points(a, b, p):
    """
    Find all points on the elliptic curve y^2 = x^3 + ax + b (mod p).
    
    Args:
        a (gmpy2.mpz): Coefficient of x in the elliptic curve equation.
        b (gmpy2.mpz): Constant term in the elliptic curve equation.
        p (gmpy2.mpz): A prime number defining the finite field.
    """
    global no_of_points
    x = gmpy2.mpz(0)
    xx = gmpy2.mpz(0)
    y = gmpy2.mpz(0)
    temp1 = gmpy2.mpz(0)
    temp2 = gmpy2.mpz(0)
    temp3 = gmpy2.mpz(0)

    # Iterate over all possible x values in the finite field defined by p
    for x in range(int(p)):
        # Compute y^2 = x^3 + ax + b (mod p)
        temp1 = gmpy2.powmod(x, 3, p)
        temp2 = (x * a) % p
        temp3 = (temp2 + b) % p
        xx = (temp3 + temp1) % p

        if xx == 0:
            y = xx
            print(f"({x}, {y}): ", end="")
            find_the_order(a, b, p, x, y)
            print()
            no_of_points += 1

        ret = gmpy2.legendre(xx, p)
        if ret == 1:
            # Compute square root of xx mod p
            temp1 = (p + 1) // 4
            y = gmpy2.powmod(xx, temp1, p)
            print(f"({x}, {y})", end="\t")
            no_of_points += 1
            y = p - y
            print(f"({x}, {y}): ", end="")
            find_the_order(a, b, p, x, y)
            no_of_points += 1

    # Include the point at infinity
    no_of_points += 1

if __name__ == "__main__":
    """
    Main function to handle input and calculate points on the elliptic curve.
    """
    if len(sys.argv) != 4:
        print("Usage: python find_points_n_order.py <a> <b> <p>")
        print("Where:")
        print("  <a> is the coefficient of x in the elliptic curve equation.")
        print("  <b> is the constant term in the elliptic curve equation.")
        print("  <p> is a prime number defining the finite field.")
        print("Example: python find_points_n_order.py 2 3 19")
        sys.exit(1)

    # Initialize variables
    a = gmpy2.mpz(sys.argv[1])
    b = gmpy2.mpz(sys.argv[2])
    m = gmpy2.mpz(sys.argv[3])

    # Check if m is prime and satisfies the prime check
    check_prime(m)
    print(f"Prime field is: {m}")

    # Find points on the elliptic curve y^2 = x^3 + ax + b (mod p)
    find_points(a, b, m)

    # Output the total number of points found, including the point at infinity
    print(f"Number of Total Points (including O point) is: {no_of_points}")
