#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moneyball.settings")
#     os.environ.setdefault("DYLD_LIBRARY_PATH",'/Library/PostgreSQL/9.3/lib')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
