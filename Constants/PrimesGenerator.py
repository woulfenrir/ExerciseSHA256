#! python3


from math import ceil


def check_prime(num2check: int):

    if num2check == 2:

        return True

    else:

        mid = int(ceil((num2check+1)/2))

        for i in range(mid, 1, -1):

            if num2check % i < 1:

                return False

        return True


def generate_primes(total=64):

    i = 0
    j = 2
    while i < total:

        if check_prime(j):

            i += 1
            yield j
            j += 1

        else:

            j += 1
