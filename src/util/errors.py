import traceback


def format_exception(error: Exception):
    return "".join(traceback.format_exception(type(error), error, error.__traceback__, 4))
