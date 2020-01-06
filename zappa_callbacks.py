import os

ZAPPA_COMMANDS_REQUIRE_SQLITE3 = ("deploy", "update")
SQLITE3_SO_FILENAME = "_sqlite3.so"
PROJECT_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(PROJECT_DIR, "lib")


def activate_shared_object(filename):
    """
    Move the shared object file to the top-level
    """
    os.rename(os.path.join(LIB_DIR, filename), os.path.join(PROJECT_DIR, filename))


def deactivate_shared_object(filename):
    """
    Move the shared object file back to lib/
    """
    os.rename(os.path.join(PROJECT_DIR, filename), os.path.join(LIB_DIR, filename))


def after_settings(zappa_cli):
    """
    Activate sqlite3 so that it will be included in the zip package
    """
    if zappa_cli.command in ZAPPA_COMMANDS_REQUIRE_SQLITE3:
        activate_shared_object(SQLITE3_SO_FILENAME)


def after_zip(zappa_cli):
    """
    Deactivate sqlite3 so that it won't be used during development
    """
    if zappa_cli.command in ZAPPA_COMMANDS_REQUIRE_SQLITE3:
        deactivate_shared_object(SQLITE3_SO_FILENAME)
