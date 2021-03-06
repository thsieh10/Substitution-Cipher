"""
Usage: if key_file is not specified, this program will print out the plaintext corresponding to the solution
and cipher text; otherwise, an accuracy analysis will print.
See below for argparse arguments.

This script currently assumes plain and cipher alphabets are both
_ a b c d e f g h i j k l m n o p q r s t u v w x y
"""
import argparse
import re
from pprint import pprint

def inv_decode(sol, cipher_file):
    inv_sol = {v: k for k, v in sol.iteritems()}
    cf = open(cipher_file, 'r')
    plain = ''
    for l in cf:
        for c in l:
            plain += inv_sol[c]
    print plain

def decode(key, sol, cipher_file):
    # reverse mappping to decode
    inv_sol = {v: k for k, v in sol.iteritems()}
    inv_key = {v: k for k, v in key.iteritems()}
    cf = open(cipher_file, 'r')
    count_right = 0
    count_total = 0
    for l in cf:
        for c in l:
            count_total += 1
            if inv_sol[c] == inv_key[c]:
                count_right += 1

    # print accuracy of decoded text
    print '{}/{} ({}%) characters were solved correctly'.format(count_right, count_total, 100.0 * count_right / count_total)


def key_accuracy(key_file, solution_file):

    # read original keys
    kf = open(key_file, 'r')
    pattern = r'\'([A-Za-z0-9_\./\\-]*)\''

    # key dict is a mapping from plain text to cipher text (created by cipher.py)
    key = {}
    key[' '] = '_'
    for l in kf:
        m = re.findall(pattern, l)
        if len(m) == 2:
            key[m[0]] = m[1]

    # solution dict is a mapping from solution text (solved by solver) to cipher text
    sol = get_solution(solution_file)

    # count number of keys guessed correct
    count_right = 0
    for k in key:
        if key[k] == sol[k]:
            count_right += 1

    # print accuracy of character mappings
    print '{}/{} ({}%) keys were solved correctly'.format(count_right, len(key), 100.0 * count_right / len(key))

    return (key,sol)


def get_solution(solution_file):
    sol = {}
    sf = open(solution_file, 'r')
    for l in sf:
        if "Solution: " in l:
            s = l[l.find('{') + 1: l.find('}')]
            for pair in s.split(','):
                (cipher, solution) = pair.split(":")
                sol[chr(int(cipher) + ord('a') - 1)] = chr(int(solution) + ord('a') - 1)
            del sol[chr(ord('a') - 1)]
        # TODO: Modify to use only one of these two
        if "Solution alphabet: " in l:
            s = l[l.find('{') + 1: l.find('}')]
            for pair in s.split(','):
                (cipher, solution) = pair.split(":")
                sol[cipher] = solution
    sol[' '] = '_'
    return sol


parser = argparse.ArgumentParser()
parser.add_argument("--key_file", help='file containing the original keys generated by cipher.py', default=None)
parser.add_argument("cipher_file", help='file of cipher text')
parser.add_argument("solution_file", help='file containing the solution')

args = parser.parse_args()

key_file = args.key_file
cipher_file = args.cipher_file
solution_file = args.solution_file

if not key_file:
    sol = get_solution(solution_file)
    inv_decode(sol, cipher_file)
    exit(0)
(key, sol) = key_accuracy(key_file, solution_file)
decode(key, sol, cipher_file)
