import importlib
import logging
import wrapt


logger = logging.getLogger("provda.patch")


@wrapt.decorator
def report(wrapped, instance, args, kwargs):
    logger.info("I/O on instance {} args {} kwargs {}".format(
        instance, args, kwargs
    ))
    return wrapped(*args, **kwargs)


def wrap_modules():
    m = importlib.import_module("csv")
    m.writer = report(m.writer)


if __name__ == "__main__":
    spamwriter = csv.writer(open("eggs.csv", mode="w"))
