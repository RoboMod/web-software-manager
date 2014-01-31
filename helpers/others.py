import argparse
import re


def chk_neg(value):
    v = int(value)
    if v < 0:
        raise argparse.ArgumentTypeError("%s isn't a valid positive int" % value)
    return v


def filter_versions(versions, version_regexp, unstable_regexp, only_stable, replace_lines=True):
    result = {}

    regexp_v = re.compile(version_regexp, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    regexp_u = re.compile(unstable_regexp, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if versions:
        for v in versions.keys():
            ver = regexp_v.match(v).group(1)
            unstable = regexp_u.match(v)
            unstable = unstable.group(1) if unstable else ""
            if ver:
                if replace_lines:
                    ver = ver.replace("_",".").replace("-",".")

                # take if:
                #  - only_stable = True => only stable versions (skip if res.group(2) is not empty)
                #  - only_stable = False => all versions
                if (not only_stable) or (not unstable):
                    result[ver + unstable] = versions.pop(v) #(unstable.group(1) if unstable else "")] = versions.pop(v)

    return result


def sort_versions(versions):
    # this sorts the versions to the "right" order, so 5.0.10 is higher than 5.0.9 and lower than 5.1.0
    # therefore it multiplies each part (separated by '.') by power of the reverse index and sums them up
    # e.q. 5.0.10 => 10*10^0 + 0*10^2 + 5*10^4 = 50010
    # 5.1.0 => 0*10^0 + 1*10^2 + 5*10^4 = 50100
    # 5.0.9 => 9*10^0 + 0*10^2 + 5*10^4 = 50009

    # filter to get only the "version" (e.q. 4.5.10RC1 => 4.5.10)
    regexp_version = re.compile('(\.?\d*)*', re.DOTALL | re.IGNORECASE | re.MULTILINE)
    filter_version = lambda key: regexp_version.match(key).group(0)

    # filter to get list of numbers of the "version" (e.q. 4.5.10 => (10, 5, 4))
    regexp_ints = re.compile('(\d*)', re.DOTALL | re.IGNORECASE | re.MULTILINE)
    filter_ints = lambda key: filter_version(key).split('.')

    # filter to get the rest (e.q. 4.5.10RC1 => RC1)
    filter_rest = lambda key: key.replace(filter_version(key), "")

    # find max number of sub releases
    nr_sub_rel = 0
    for v in versions:
        l = len(filter_ints(v))
        if l > nr_sub_rel:
            nr_sub_rel = l

    # find max length of rest
    max_val = 0
    for v in versions:
        l = len(filter_rest(v))
        if l > max_val:
            max_val = l

    # calculates the sort key
    sort_key = lambda ver: pow(10, max_val) * sum(pow(10,(nr_sub_rel - index)*2)*int(x) for index, x in enumerate(filter_ints(ver))) - sum(ord(c) for c in filter_rest(ver))

    return sorted(versions, key=sort_key, reverse=True)