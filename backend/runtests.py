#!/usr/bin/env python
import os
import shutil
import sys

import django
from django.conf import settings
# from django.test.utils import get_runner

import pytest

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()
    # TestRunner = get_runner(settings)
    # test_runner = TestRunner()
    # failures = test_runner.run_tests(["reagents"])
    retcode = pytest.main(["-v"])
    if retcode == 0:
        try:
            shutil.rmtree(settings.BASE_DIR / "reagents" / "tests" / "media")
        except FileNotFoundError:
            pass
    sys.exit(retcode)
