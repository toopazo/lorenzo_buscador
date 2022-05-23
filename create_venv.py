#!/usr/bin/env python3

import subprocess
import argparse


def test_subprocess():
    cmd = ['python', '--`version']
    # result = subprocess.run(cmd, stdout=subprocess.PIPE)
    # result = subprocess.run(cmd, stdout=subprocess.PIPE,
    #                         stderr=subprocess.PIPE)
    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    # result = subprocess.run(cmd, capture_output=True)
    # print('cmd %s result %s' % (cmd, result))
    print('result.stdout %s' % result.stdout)
    # cmd = 'ls /usr/bin/python'


def check_python3_version():
    for i in range(9, 6, -1):
        pver = 'python3.%s' % i
        cmd = [pver, '--version']
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            # print('result.stdout %s' % result.stdout)
            _ = result
            return pver
        except FileNotFoundError:
            result = 'FileNotFoundError'
            # print('cmd %s result %s' % (cmd, result))
            _ = result
    return 'No python 3.x found'


def exec_cmd_and_report(cmd_str, decode):
    result = subprocess.run(
        cmd_str, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('cmd %s' % cmd_str)
    print('result.stdout %s' % result.stdout)
    if decode:
        bstr = result.stdout
        result_str = bstr.decode()
        print('result_str')
        print(result_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Operations related to Python venv')
    parser.add_argument('--pver', action='store_true',
                        help='Get highest python3 version')

    args = parser.parse_args()

    if args.pver:
        upver = check_python3_version()
        print(upver)


