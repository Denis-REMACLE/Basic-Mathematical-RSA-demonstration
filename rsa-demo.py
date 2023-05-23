#!/usr/bin/env python3
#Author : Denis REMACLE
#Name : Basic-Mathematical-RSA-demonstration
#file : rsa-demo.py
# !!! This is not a viable RSA implementation !!!

import argparse
import os
from math import sqrt, gcd
#from qiskit import IBMQ
#from qiskit.utils import QuantumInstance
#from qiskit.algorithms import Shor

#def shor(n):
#    # Enter your API token here
#    IBMQ.enable_account(os.getenv('API_TOKEN_IBM')) 
#    provider = IBMQ.get_provider(hub='ibm-q')
#
#    # Specifies the quantum device
#    backend = provider.get_backend('ibmq_qasm_simulator')
#    factors = Shor(n)
#
#    result_dict = factors.run(QuantumInstance(
#        backend, shots=1, skip_qobj_validation=False))
#
#    # Get factors from results
#    result = result_dict['factors']
#
#    print(result)
#    return results

def break_key(number):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    for p in primes:
        factor = number % p
        if factor == 0:
            q = number // p
            return p, q

def check_if_prime(number):
    flag = 0

    if(number > 1):
        for k in range(2, int(sqrt(number)) + 1):
            if (number % k == 0):
                flag = 1
            break
        return flag
    else:
        return 1

def factorise_p_and_q(p, q):
    print("Secondly we must factorise P and Q to get the modulus (N) for both private and public key.\n")
    print("The modulus is a part of the public key : this is why RSA is threatened by the Shor's algorithm.")
    print("The shors algorithm finds the primes factors of an integer using quantum computers\n")
    n = p * q
    print(f"The value of N is : {n} = {p} x {q}\n")
    return n

def get_phi_n(p, q):
    print("Thirdly we must get the λ(n) (the Carmichael's totien function) or the φ(n) (the Euler's totien function).\n")
    phi = (p-1)*(q-1)
    print(f"The value of φ(n) is : {phi} = ({p}-1)x({q}-1)\n")
    return phi

def find_relative_primes(phi):
    print("Fourthly we must chose a number e thats is relatively prime with λ(n) or φ(n) depending on which one you calculated\n")
    for i in range(2, phi):
        if gcd(i,phi)==1:
            print(f"The number e is {i}\n")
            return i

def mod_inverse(e,phi):
    print("Finally we must find the modular inverse of e with modulus λ(n) or φ(n)\n")
    d = pow(e, -1, phi)
    print(f"The modular inverse of e is {d} as {e}x{d} ≡ {(e*d)%phi} mod {phi}\n")
    return d

def cipher(msg, public_key):
    ciphertext = []
    for letter in msg:
        value = pow(ord(letter), public_key["E"]) % public_key["N"]
        print(f"Ciphering {letter} (ASCII value = {ord(letter)}) : pow({ord(letter)}, {public_key['E']})%{public_key['N']} = {value}")
        ciphertext.append(value)
    return ciphertext

def decipher(msg, private_key):
    cleartext = []
    for letter in msg:
        value = chr(pow(letter,private_key["SecretExponent"])%private_key["N"])
        print(f"Deciphering {letter}\t:\tpow({letter}, {private_key['SecretExponent']})%\t{private_key['N']}\t=\t{ord(value)}\t=\t{value}")
        cleartext.append(value)
    return cleartext

def main():
    # initialize the ArgumentParser
    parser = argparse.ArgumentParser()

    # add the arguments
    parser.add_argument("-p", "--pvalue", help="Value for P", default=13, type=int)
    parser.add_argument("-q", "--qvalue", help="Value for Q", default=17, type=int)
    parser.add_argument("-m", "--msg", help="String to use for the demo", default="hello", type=str)
    parser.add_argument("-d", "--decipher", help="String to decipher using the generated key", nargs='+', type=int)
    parser.add_argument("-c", "--cipher", help="String to cipher using the generated key", default="", type=str)
    parser.add_argument("-s", "--shor", help="Use shor's algorithm to break the key", type=int)
    parser.add_argument("-b", "--break_key", help="Use bruteforce to break the key", type=int)

    # and then parse them
    args = parser.parse_args()
    if args.pvalue == args.qvalue:
        print("The P and Q values must not be equal")
    elif check_if_prime(args.pvalue) == 1:
        print("The P value must be prime")
    elif check_if_prime(args.qvalue) == 1:
        print("The Q value must be prime")
    else:
        p, q = args.pvalue, args.qvalue
        print("Firstly we must select prime numbers that will allow us to work.\n")
        print("All values are prime so we can start ;-)\n")

    

    n = factorise_p_and_q(p, q)
    phi = get_phi_n(p, q)
    e = find_relative_primes(phi)
    d = mod_inverse(e, phi)

    private_key = {"N": n, "SecretExponent": d}
    public_key = {"N": n, "E": e}

    print("Let's take a look at the keys generated.\n")
    print(f"The private key is composed of the factorisation of the primes number and the secret exponent.\n{private_key}\n")
    print(f"The public key is composed of the factorisation of the primes number and the modular inverse.\n{public_key}\n")

    print(f"Let's imagine Bob wants to say hello to Alice, he'll use Alice's public key to cipher the letter array  \"{args.msg}\".")
    ciphertext = cipher(args.msg, public_key)
    print(f"The ciphertext is {ciphertext}\n")

    print("Alice wants to decipher the text sent by Bob so she uses her private key")
    cleartext = decipher(ciphertext, private_key)
    print(f"The cleartext is {cleartext}\n")

    if args.decipher:
        print("You wanted to decipher a string.")
        cleartext = decipher(args.decipher, private_key)
        print(f"The cleartext is {cleartext}\n")

    if args.cipher:
        print("You wanted to cipher a string.")
        ciphertext = cipher(args.cipher, public_key)
        print(f"The ciphertext is {ciphertext}\n")

    if args.shor:
        shor(args.shor)
    if args.break_key:
        p, q = break_key(args.break_key)
        print(f"The factors are {p} and {q}")


if __name__ == "__main__":
    main()
