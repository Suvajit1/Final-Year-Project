import gmpy2
import sys

def add_point(a, b, p, xp, yp, xq, yq):
    """
    Add two points (xp, yp) and (xq, yq) on an elliptic curve over a finite field defined by p.
    Returns the result point (xr, yr).
    """
    if xp == 0 and yp == 0:
        return xq, yq

    if xq == 0 and yq == 0:
        return xp, yp

    pm = (p - yq) % p

    if xp == xq and yp == pm:
        return gmpy2.mpz(0), gmpy2.mpz(0)  # Point at infinity

    mody = (yq - yp) % p
    modx = gmpy2.invert(xq - xp, p)
    l = (modx * mody) % p

    xr = (l * l - xp - xq) % p
    yr = (l * (xp - xr) - yp) % p

    return xr, yr


def double_point(a, b, p, xp, yp):
    """
    Double a point (xp, yp) on an elliptic curve over a finite field defined by p.
    Returns the result point (xr, yr).
    """
    if yp == 0:
        return gmpy2.mpz(0), gmpy2.mpz(0)  # Point at infinity

    modx = (3 * xp * xp + a) % p
    mody = gmpy2.invert(2 * yp, p)
    l = (modx * mody) % p

    xr = (l * l - 2 * xp) % p
    yr = (l * (xp - xr) - yp) % p

    return xr, yr


def find_order(a, b, p, xp, yp):
    """
    Find the order of the point (xp, yp) on an elliptic curve defined by y^2 = x^3 + ax + b (mod p).
    """
    xq, yq = xp, yp
    order = gmpy2.mpz(1)

    # Double the point first
    xr, yr = double_point(a, b, p, xq, yq)
    if xr == 0 and yr == 0:
        return gmpy2.mpz(2)  # Point has order 2 (doubled point results in point at infinity)

    order += 1
    xq, yq = xr, yr

    # Add points repeatedly until we reach the point at infinity
    while True:
        order += 1
        if xq == xp:
            return order

        xr, yr = add_point(a, b, p, xp, yp, xq, yq)
        xq, yq = xr, yr


def main():
    if len(sys.argv) != 6:
        print("Usage: python elliptic_curve_order.py <a> <b> <p> <xp> <yp>")
        print("Example: python elliptic_curve_order.py 2 3 19 1 5")
        return

    # Initialize variables from command line arguments
    a = gmpy2.mpz(sys.argv[1])
    b = gmpy2.mpz(sys.argv[2])
    p = gmpy2.mpz(sys.argv[3])
    xp = gmpy2.mpz(sys.argv[4])
    yp = gmpy2.mpz(sys.argv[5])

    # Find the order of the point
    order = find_order(a, b, p, xp, yp)

    print(f"\nOrder is: {order}\n")


if __name__ == "__main__":
    main()
