#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-06-29
# modified: 2025-06-29
#
# Prints the classes, methods and functions of a script, in color. Requires colorama.
#
# Usage:
#     python3 api.py <filename.py>
#     micropython api.py <filename.py>
#
# In the MicroPython REPL:
#     > import api
#     > api.exec('<filename.py>')
#

import sys

try:
    from colorama import Fore, Style
except ImportError:
    print("colorama module not found. Install it with 'pip install colorama'")
    sys.exit(1)

try:
    from colorama import init
    init()  # Only in CPython
except ImportError:
    pass

def exec(path):
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except OSError:
        print("File not found: {}".format(path))
        return

    print()
    current_class = None
    class_indent = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(line.lstrip())

        # reset current_class if we've left the class block
        if class_indent is not None and indent <= class_indent and not stripped.startswith('def'):
            current_class = None
            class_indent = None

        if stripped.startswith('class '):
            class_name = stripped.split()[1].split('(')[0].strip(':')
            current_class = class_name
            class_indent = indent
            print('{}class{} {}:'.format(
                Fore.WHITE, Style.RESET_ALL, Fore.CYAN + class_name + Style.RESET_ALL))

        elif stripped.startswith('def ') or stripped.startswith('async def '):
            is_async = stripped.startswith('async def ')
            open_paren = stripped.find('(')
            close_paren = stripped.rfind(')')
            func_name = stripped[(10 if is_async else 4):open_paren].strip()
            arg_string = stripped[open_paren:close_paren + 1] if open_paren != -1 and close_paren != -1 else '()'

            # reset current_class if we're back to top level
            if current_class and indent <= class_indent:
                current_class = None
                class_indent = None

            # style dim if name starts with _
            name_style_start = Style.DIM if func_name.startswith('_') else ''
            name_style_end = Style.RESET_ALL if func_name.startswith('_') else ''

            color_prefix = ''
            if is_async:
                color_prefix += '{}async{} '.format(Fore.YELLOW, Style.RESET_ALL)
            color_prefix += '{}def{} '.format(Fore.WHITE, Style.RESET_ALL)

            full_signature = '{}{}{}{}{}'.format(
                name_style_start, Fore.CYAN, func_name + arg_string, Style.RESET_ALL, name_style_end
            )

            if current_class:
                print('    {}{}'.format(color_prefix, full_signature))
            else:
                print('{}{}'.format(color_prefix, full_signature))

# --- Cross-compatible __main__ block ---


if __name__ == '__main__':
    try:
        argv = sys.argv
    except AttributeError:
        argv = ['api.py', 'main.py']  # fallback for MicroPython

    if len(argv) < 2:
        print('Usage: {} <script.py>'.format(argv[0]))
        try:
            sys.exit(1)  # Works in CPython
        except AttributeError:
            pass        # sys.exit doesn't exist in MicroPython
    else:
        exec(argv[1])
