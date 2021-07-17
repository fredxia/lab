#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--abcd", required=False)
subparser = parser.add_subparsers(dest="sub1", help="help1")
sub_p1 = subparser.add_parser("cmd1", help="sub_p1_help")
#sub_p1.add_argument("--sub_p1")
subparser2 = sub_p1.add_subparsers()
sub_p2 = subparser2.add_parser("cmd2", help="sub_p2_helper")
sub_p2 = subparser2.add_parser("cmd3", help="sub_p3_helper")
sub_p2.add_argument("--sub_p2")

args = parser.parse_args()

