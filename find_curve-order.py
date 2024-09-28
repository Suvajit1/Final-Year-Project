import gmpy2
import sys

no_of_points = 0

def check_prime(m):
    """
    Check if the given number m is a prime of the form p ≡ 3 (mod 4).
    If not, find the next prime that satisfies p ≡ 3 (mod 4).
    
    Args:
        m (gmpy2.mpz): Input number to check for primality.
        
    Returns:
        gmpy2.mpz: A prime number p ≡ 3 (mod 4).
    """
    m = gmpy2.mpz(m)
    modprime = gmpy2.mpz(0)
    
    # If m is not prime, find the next prime
    if gmpy2.is_prime(m) < 1:
        m = gmpy2.next_prime(m)
    
    # Keep finding the next prime until p ≡ 3 (mod 4) is satisfied
    while True:
        modprime = m % 4
        if modprime == 3:
            return m
        else:
            m = gmpy2.next_prime(m)

def find_points(a, b, p):
    """
    Find all points on the elliptic curve y^2 = x^3 + ax + b (mod p).
    This function calculates points over the finite field defined by p.
    
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
        # Calculate y^2 = x^3 + ax + b (mod p)
        temp1 = gmpy2.powmod(x, 3, p)
        temp2 = (x * a) % p
        temp3 = (temp2 + b) % p
        xx = (temp3 + temp1) % p
        
        # Check if the equation is solvable for y
        if xx == 0:
            y = xx  # If xx == 0, y is also 0
            no_of_points += 1
        
        ret = gmpy2.legendre(xx, p)  # Check if xx is a quadratic residue
        if ret == 1:
            # Calculate square roots of xx (mod p) using the field properties
            temp1 = (p + 1) // 4
            y = gmpy2.powmod(xx, temp1, p)
            no_of_points += 1
            y = p - y  # The second square root (mod p)
            no_of_points += 1
    
    # Include the point at infinity
    no_of_points += 1

if __name__ == "__main__":
    """
    Main function to handle input and output.
    This function reads curve parameters a, b, and prime p from the command line
    and computes the points on the elliptic curve y^2 = x^3 + ax + b (mod p).
    """
    
    # Help message for usage
    if len(sys.argv) != 4:
        print("Usage: python find_curve_order.py <a> <b> <p>")
        print("Where:")
        print("  <a> is the coefficient of x in the elliptic curve equation.")
        print("  <b> is the constant term in the elliptic curve equation.")
        print("  <p> is a prime number defining the finite field.")
        print("Example: python find_curve_order.py 2 3 19")
        sys.exit(1)
    
    # Parse input arguments
    try:
        a = gmpy2.mpz(sys.argv[1])
        b = gmpy2.mpz(sys.argv[2])
        m = gmpy2.mpz(sys.argv[3])
    except ValueError:
        print("All inputs must be integers.")
        sys.exit(1)

    # Check if m is prime and satisfies p ≡ 3 (mod 4)
    m = check_prime(m)
    print(f"Prime field is: {m}")
    
    # Find points on the elliptic curve y^2 = x^3 + ax + b (mod p)
    find_points(a, b, m)
    
    # Output the total number of points found
    print(f"\nThe Order of the Curve is: {no_of_points}")
