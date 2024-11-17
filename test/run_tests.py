import unittest


def load_tests(loader, tests, pattern):
    return loader.discover('.')


if __name__ == '__main__':
    unittest.main()
