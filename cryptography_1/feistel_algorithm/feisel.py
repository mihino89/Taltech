#! /usr/bin/python
import sys, getopt


def process_args(argv):
    l0, r0, k0, r = 0, 0, 0, 6

    try: 
        opts, args = getopt.getopt(argv, "hl:r:k:r:", ["left=", "right=", "key=", "rounds="])
    except getopt.GetoptError:
        
        sys.exit(10)

    for opt, arg in opts:
        if opt == "-h":
            print("feisel.py -l <8 left bits of PT> -r <8 right bits of PT> -k <8 bits key>")
            sys.exit(0)
        elif opt in ("-l", "left"):
            l0 = int(arg)
        elif opt in ("-r", "right"):
            r0 = int(arg)
        elif opt in ("-k", "key"):
            k0 = int(arg)
        elif opt in ("-r", "rounds"):
            r = int(arg)
    
    print("l0, r0, k0", l0, r0, k0)
    return l0, r0, k0, r

def next_key(ki, i):
    return ki ^ i

def round_function(ki, x):
    return ki ^ x

def feisel_alg(li, ri, ki, i):
    # Step2 -  get Ei number defined by round function
    ei = round_function(ri, ki)
    
    # Step 3 - Li_plus_1 = Ri and Ri_plus_1 = Li xor Ei
    li_plus_1 = ri
    ri_plus_1 = li ^ ei
    ki_plus_1 = next_key(ki, i+1)

    # Step 4 omitted dua to splitting on li and ri part (we have only 2 bajt PT on input)
    return li_plus_1, ri_plus_1, ki_plus_1


def main(argv):
    l0, r0, k0, rounds = process_args(argv)
    li, ri, ki = l0, r0, k0

    for i in range(rounds):
        li, ri, ki = feisel_alg(li, ri, ki, i)
        print("After Round ", i, ": li, ri, ki", bin(li), bin(ri), bin(ki))
    print("Final message: ", bin(li), bin(ri))

if __name__ == '__main__':
    main(sys.argv[1:])

