"""Event loop."""

__all__ = ['get_event_loop', 'set_event_loop']

import functools
import inspect
import reprlib
import sys

_PY34 = sys.version_info >= (3, 4)


def _get_function_source(func):
    if _PY34:
        func = inspect.unwrap(func)
    elif hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    if inspect.isfunction(func):
        code = func.__code__
        return (code.co_filename, code.co_firstlineno)
    if isinstance(func, functools.partial):
        return _get_function_source(func.func)
    if _PY34 and isinstance(func, functools.partialmethod):
        return _get_function_source(func.func)
    return None


def _format_args(args):
    """Format function arguments.

    Special case for a single parameter: ('hello',) is formatted as ('hello').
    """
    # use reprlib to limit the length of the output
    args_repr = reprlib.repr(args)
    if len(args) == 1 and args_repr.endswith(',)'):
        args_repr = args_repr[:-2] + ')'
    return args_repr


def _format_callback(func, args, suffix=''):
    if isinstance(func, functools.partial):
        if args is not None:
            suffix = _format_args(args) + suffix
        return _format_callback(func.func, func.args, suffix)

    func_repr = getattr(func, '__qualname__', None)
    if not func_repr:
        func_repr = repr(func)

    if args is not None:
        func_repr += _format_args(args)
    if suffix:
        func_repr += suffix

    source = _get_function_source(func)
    if source:
        func_repr += ' at %s:%s' % source
    return func_repr

g_loop = None

def get_event_loop():
    return g_loop

def set_event_loop(loop):
    global g_loop
    g_loop = loop
