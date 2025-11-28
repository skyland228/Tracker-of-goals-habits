import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(["habits", "users"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()