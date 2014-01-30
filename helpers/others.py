import argparse


def chk_neg(value):
    v = int(value)
    if v < 0:
        raise argparse.ArgumentTypeError("%s isn't a valid positive int" % value)
    return v
