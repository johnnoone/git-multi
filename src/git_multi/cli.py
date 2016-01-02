#!/usr/bin/env python

import argparse
import sys


def dispatch(args=None):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(args or sys.argv[1:])
    return sys.exit(0)
