Generic Async Functions for Python
==================================

This is a refactoring of the non-I/O related parts of Python's ```asyncio```
package, to try to determine what parts of the implementation are generally
usable outside of an I/O related context.

Most of the code is a direct copy of the relevant parts of the ```asyncio```
package, and has only been minimally altered for this refactoring.

The ```philosophers.py``` script implements the classic "dining philosophers"
problem using this library.

The ```single_file``` directory contains a very trivial implementation of the
basic loop and synchronisation primitives as a single file, to test some of the
implementation without hitting circular import issues, which have been causing
problems with the main implementation.
