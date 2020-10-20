# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

def normalize_to_unicode(value):
    """
    string convert to unicode
    """
    if hasattr(value, "decode") and not isinstance(value, str):
        return value.decode("utf-8")
    return value


def normalize_to_str(value):
    """
    unicode convert to string
    """
    if hasattr(value, "encode") and isinstance(value, str):
        return value.encode("utf-8")
    return value
