#!/usr/bin/env python3

import maxhk
import subprocess as sp

def main():
    pypi_creds = maxhk.op.get_item("pypi.org", ["username", "password"])
    sp.check_call('python3 -m build')


if __name__ == "__main__":
    main()
