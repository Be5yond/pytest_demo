import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="environment: (test|online|preonline) default is test")

