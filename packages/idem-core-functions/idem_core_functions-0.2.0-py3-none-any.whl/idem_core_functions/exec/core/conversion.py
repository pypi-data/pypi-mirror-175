import json
from typing import Dict

__contracts__ = ["soft_fail"]


async def to_json(
    hub,
    data,
    skip_keys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
) -> Dict:
    """
    Serialize an object to a string of JSON

    Args:
        data: It serializes the data as a JSON formatted.
        skip_keys: The default parameter for skipkeys is False, but if it is True, then dict keys that are not of a basic type (str, int, float, bool, None) will be skipped instead of raising a TypeError.
        ensure_ascii: The default value for ensure_ascii is True, and the output is assured to have all incoming non-ASCII characters escaped.
        check_circular: The default value for check_circular is True and if it is False, then the circular reference check for container types will be skipped, and a circular reference will result in an OverflowError.
        allow_nan: The default value for check_circular is True and if it is False, then it will be a ValueError to serialize out-of-range float values (nan, inf, -inf) in strict acquiescence with the JSON specification.
        indent:
            If indent is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level.
            An indent level of 0, negative, or ” ” will only insert newlines. None (the default) selects the most compact representation.
            A positive integer indent indents that many spaces per level. If indent is a string (such as “\t”), that string is used to indent each level.
        separators: If specified, separators should be an (item_separator, key_separator) tuple. The default is (‘, ‘, ‘: ‘) if indent is None and (‘, ‘, ‘: ‘) otherwise. To get the most compact JSON representation, you should specify (‘, ‘, ‘:’) to trim whitespace.
        default: If specified, the default should be a function called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a TypeError. If not specified, TypeError is raised.
        sort_keys: The sort_keys parameter value is False by default, but if it is true, then the output of dictionaries will be sorted by key.
    """
    result = dict(comment=[], ret=None, result=True)
    if not data:
        result["result"] = False
        result["comment"].append(f"data for json conversion is empty")
        return result

    json_string = json.dumps(
        data,
        skipkeys=skip_keys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
    result["ret"] = {"data": json_string}
    return result
