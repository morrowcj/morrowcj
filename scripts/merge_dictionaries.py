import inspect
from copy import deepcopy
from functools import partial
from typing import Callable
from dictdiffer import diff

def diff_dicts(x: dict|list|set, y: dict|list|set, **kwargs) -> list[tuple]:
    """Display the difference between two dictionaries.

    Parameters
    ----------
        x: dict
            the first "from" dictionary
        y: dict
            the second "to" dictionary
        **kwargs:
            additional arguments passed to dictdiffer.diff

    Returns
    -------
    A list if "diff" tuples, which indicate a change, addition, or removal from x to y. diff tuples take the form
    ("type", "where", "what"): type is if it is a "change", "add" or "remove; "where" is the location of the difference
    (note that a.b indicates the "b" sub-key of the "a" key); and "what" is a tuple (or list of tuples) of the form
    ("from", "to") that shows the old "x" and new "y" values, respectively.

    See the Examples below.

    Examples
    --------
        a = {"x": 1, "y": {"p": 20}}
        b = {"x": 100, "z": 0.75}
        c = {"y": {"p": 20000, "q": 80}}
        diff_dicts(a, b)
        diff_dicts(a, c)
        diff_dicts(b, c)
    """
    diff_results = diff(x, y, **kwargs)

    return list(diff_results)



def overwrite_combine(source: dict, target: dict, inplace = False) -> dict | None:
    """
    Recursively add elements of a source dictionary into a target dictionary. When a terminal key (i.e., a key 
    whose value is not itself a dictionary) occurs in both dictionaries, the source's value overwrites the target's.


    Returns
    -------
    A combined dictionary with all unique keys and sub-keys of both original dictionaries, but with values from source
    overwriting corresponding values of target. If inplace = True, the target dictionary is modified in-place and the
    function returns None.

    Parameters
    ----------
        source: source dictionary
            the source from which all elements are copied
        target: target dictionary
            the target into which elements are added
        inplace: boolean, default False
            should target be modified directly? if False, returns the new dictionary, without altering target.

    Examples
    --------
    source = {"x": 7, "y": {"p": 90, "q": 10}}
    sync = {"z": 5, "y":{"p": 0.01, "n": 20}}

    new = overwrite_combine(source, sync)
    print(new)
    print(sync) # unchanged
    print(source) # unchanged

    overwrite_combine(source, sync, inplace = True)
    print(sync) # updated

    See Also
    --------
    novel_combine: which is the inverse of this function, that only updates target with novel elements from source
    """

    target_copy = deepcopy(target)

    for k, v in source.items():
        if isinstance(v, dict):
            overwrite_combine(v, target_copy.setdefault(k, {}), inplace=True)
        else:
            target_copy[k] = v

    if inplace:
        target.update(target_copy)
        return None

    return target_copy

def novel_combine(source: dict, target: dict, inplace = False) -> dict | None:
    """
    Recursively add novel elements of a source dictionary into a target dictionary. When a terminal key (i.e., a key
    whose value is not itself a dictionary) occurs in both dictionaries, the target's value is not overwritten by the
    source's.


    Returns
    -------
    A combined dictionary including unique keys and sub-keys the target dictionary, but with values from source
    added if they were not present in the target. If inplace = True, the target dictionary is modified in-place and
    the function returns None.

    Parameters
    ----------
        source: source dictionary
            the source from which missing elements are copied
        target: target dictionary
            the target into which novel elements are added
        inplace: boolean, default False
            should target be modified directly? if False, returns the new dictionary, without altering target.

    See Also
    --------
    overwrite_combine: The inverse of this function, that overwrites elements with source elements
    """
    target_copy = deepcopy(target)
    source_copy = deepcopy(source)

    overwrite_combine(target_copy, source_copy, inplace = True)

    if inplace:
        target.update(source_copy)
        return None

    return source_copy

def sequentially_combine(*dicts: dict, method: str|Callable = "overwrite", **kwargs) -> dict:
    """
    Merge dictionaries by sequentially updating keys and sub-keys to a new dictionary, recursively.

    Notes
    -----
    Important: Order matters: dictionaries in *dicts are joined into the new dictionary sequentially, so if
    *dict[i] and *dict[j] both have terminal key (a key whose value is not a dictionary) k, then the value from
    dict[j] will overwrite the value of dict[i] in the results for all j > i.

    See the Examples for a demonstration of this behavior.

    Parameters
    ----------
        *dicts: dictionaries
            the dictionaries to be merged together.
        method: str|callable, default 'overwrite'
            the combine method to use; one of "overwrite", "novel", or a custom callable. The "overwrite" and "novel"
            methods can be abbreviated to "o" or "n" and correspond to overwrite_combine and novel_combine,
            respectively. If specifying a callable, it must accept dictionaries as its first two positional arguments,
            and it must return a dictionary.
        **kwargs:
            additional keyword arguments passed to the combine method.

    Examples
    --------
        a = {"x": 1, "y": {"p": 20}}
        b = {"x": 100, "z": 0.75}
        c = {"y": {"p": 20000, "q": 80}}
        print(sequentially_combine(c, b, a))
        print(sequentially_combine(a, b, c))
        print(sequentially_combine(a, b, c, method = 'novel')) # use novel method
        print(sequentially_combine(a, b, c, method = novel_combine, inplace = False)) # pass as callable, with args

    See Also
    --------
    overwrite_combine: Recursively elements of a source dictionary into a target dictionary (via overwrite).
    novel_combine: Recursively add novel elements of a source dictionary into a target dictionary.
    """

    combine_fun: Callable
    if callable(method) and "inplace" in inspect.signature(method).parameters:
        combine_fun = partial(method, **kwargs)
        print("using custom combine method")
    elif method in {"overwrite", "o"}:
        # combine_fun = overwrite_combine
        combine_fun = partial(overwrite_combine, inplace = False, **kwargs)
    elif method in {"novel", "n"}:
        # combine_fun = novel_combine
        combine_fun = partial(novel_combine, inplace = False, **kwargs)
    else:
        raise ValueError(f"method {method} must be '(o)verwrite' or '(n)ovel' or a callable")

    combined = {}

    for d in dicts:
        combined = combine_fun(d, combined)

    return combined