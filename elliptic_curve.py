import sys
import matplotlib.pyplot as plt
from sympy import nextprime, isprime

def euler_formula(n, p):
    """
    Compute square roots of n modulo p using Euler's formula.
    This works when p ≡ 3 (mod 4).
    """
    # Check if n is a quadratic residue modulo p
    if pow(n, (p - 1) // 2, p) != 1:
        raise AssertionError("n is not a quadratic residue modulo p")
    
    # Compute the square root of n modulo p
    x = pow(n, (p + 1) // 4, p)
    return x, p - x

def tonelli_shanks(n, p):
    """
    Compute square roots of n modulo p using the Tonelli-Shanks algorithm.
    This works when p ≡ 1 (mod 4).
    """
    # Ensure n is a quadratic residue modulo p
    assert pow(n, (p - 1) // 2, p) == 1, "n is not a quadratic residue modulo p"
    
    # Initialize variables for the Tonelli-Shanks algorithm
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    
    # Iterate until t becomes 1
    while t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r, p - r

def find_square_root(n, p, first_call):
    """
    Determine the method to compute the square root of n modulo p.
    Uses Euler's formula for p ≡ 3 (mod 4) and Tonelli-Shanks for p ≡ 1 (mod 4).
    """
    if p % 4 == 3:
        if first_call:
            print(f"Using Euler's formula for p = {p} (p ≡ 3 mod 4)")
        return euler_formula(n, p)
    elif p % 4 == 1:
        if first_call:
            print(f"Using Tonelli–Shanks algorithm for p = {p} (p ≡ 1 mod 4)")
        return tonelli_shanks(n, p)
    else:
        raise ValueError("p must be an odd prime of the form 4k+1 or 4k+3")

def elliptic_curve_points(a, b, p):
    """
    Generate all points (x, y) on the elliptic curve y^2 = x^3 + ax + b (mod p).
    If (0,0) is not present, add it to the list.
    """
    points = []  # List to store points on the elliptic curve
    first_call = True  # To track the first call for square root computation

    # Iterate over all possible x values in the finite field defined by p
    for x in range(p):
        n = (x**3 + a*x + b) % p  # Calculate y^2 for the current x
        if n == 0:
            points.append((x, 0))  # Include the (x, 0) points where y = 0
        else:
            try:
                # Find the square roots of n modulo p
                y1, y2 = find_square_root(n, p, first_call)
                first_call = False  # Ensure the message is only printed once
                points.append((x, y1))
                if y1 != y2:
                    points.append((x, y2))
            except AssertionError:
                continue  # No valid y, skip this x

    # Add (0,0) if it is not already present in points
    if (0, 0) not in points:
        points.append((0, 0))
    
    return points

def plot_elliptic_curve(points, a, b, p):
    """
    Plot the points of the elliptic curve on a 2D graph.
    """
    # Extract x and y values from the points
    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]

    # Plotting the elliptic curve points
    plt.figure(figsize=(8, 8))
    plt.scatter(x_vals, y_vals, color='blue')
    plt.title(f'Elliptic Curve: y^2 = x^3 + {a}x + {b} (mod {p})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to handle input, process elliptic curve points, and plot the curve.
    """
    # Command-line argument handling
    if len(sys.argv) != 4:
        print("Usage: python elliptic_curve.py <a> <b> <p>")
        print("Example: python elliptic_curve.py 2 3 19")
        return
    
    # Parse input arguments
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        p = int(sys.argv[3])
    except ValueError:
        print("All inputs must be integers.")
        return
    
    # Check if p is prime, if not, find the next prime
    if not isprime(p):
        original_p = p
        p = nextprime(p)
        print(f"The given number {original_p} was not a prime, so the next closest prime {p} is taken instead.")

    # Print the input parameters
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"p = {p}\n")

    # Generate all points on the elliptic curve
    points = elliptic_curve_points(a, b, p)
    print("Elliptic Curve Points (x, y):")
    for point in points:
        print(point)
    
    # Output the total number of points
    print(f"\nTotal number of points on the curve : {len(points)}")
    
    # Plot the elliptic curve points
    plot_elliptic_curve(points, a, b, p)

if __name__ == "__main__":
    main()
