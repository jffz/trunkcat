#!/usr/bin/env python3

"""A simple python script which concat splitted logs."""

import sys
import argparse
import json


def split_log(line: str, *args):
    """An helper function which return elements of log line"""
    fields = line.split()
    log_dict = {}
    log_dict['date'] = " ".join(fields[0:3])
    log_dict['src'] = fields[3]
    log_dict['svc'] = fields[4]
    log_dict['log'] = "".join(fields[5:])
    args_ok = log_dict.keys()

    if args:
        if set(args) - set(args_ok):
            raise ValueError(f"Wrong type.\nAllowed args: {', '.join(args_ok)}")
        return [log_dict[arg] for arg in args]
    return log_dict['date'], log_dict['src'], log_dict['svc'], log_dict['log']


def concat_logs(lines: list):
    cnt = 0
    last_line = len(lines)

    while cnt < last_line:
        date, src, svc, log = split_log(lines[cnt])

        if log.startswith('{') and not log.endswith('}'):
            while True:
                cnt += 1
                try:
                    json.loads(log)
                except json.decoder.JSONDecodeError:
                    nxt_src, nxt_log = split_log(lines[cnt], 'src', 'log')
                    log += nxt_log
                break

            print(date, src, svc, log)
            cnt += 1

        else:
            print(lines[cnt], end='')
            cnt += 1


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Logfile", type=argparse.FileType('r'))
    # parser.add_argument('-o', '--outfile', help="Output file",
    #                     default=sys.stdout, type=argparse.FileType('w'))

    args = parser.parse_args(arguments)
    concat_logs(args.infile.readlines())


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
