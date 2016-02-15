#!/usr/bin/env python3.5

import argparse
import os.path

# from myslicelib.util.certificate import Keypair, Certificate
from myslicelib.util import Credential

def certificate(pkey, email, hrn):
        '''
        Generate the certificate

        :param keyfile:
        :param email:
        :param hrn:
        :return:
        '''

        if not pkey or not email or not hrn:
            exit("private key, email and hrn must be specified")
        else:
            return Credential(hrn=hrn, email=email, private_key=pkey).certificate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MySlice console interface.')
    parser.add_argument('command', nargs=1, help='command to execute')
    parser.add_argument('argument', nargs=1, help='argument')

    parser.add_argument('--pkey', nargs=1, help='pkey help')
    parser.add_argument('--hrn', nargs=1, help='hrn help')
    parser.add_argument('--email', nargs=1, help='email help')


    args = parser.parse_args()

    # hrn
    if args.hrn:
        hrn = args.hrn[0]
    else:
        hrn = None

    # email
    if args.email:
        email = args.email[0]
    else:
        email = None

    # private key filename
    if args.pkey:
        if os.path.isfile(args.pkey[0]):
            pkey = args.pkey[0]
        else:
            print("private key file does not exists or is not readable")
            exit(1)
    else:
        pkey = None

    command = args.command[0]
    argument = args.argument[0]

    if command == 'help':
        print("help for", argument)

    elif command == 'certificate':

        if argument == 'create':
            print(certificate(pkey, email, hrn))

        else:
            print(command, argument, "not understood")
            exit(1)