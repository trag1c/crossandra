# Crossandra
Crossandra is a fast and simple tokenization library for Python operating on
enums and regular expressions, with a decent amount of configuration.

## Installation
Crossandra is available on PyPI and can be installed with pip, or any other
Python package manager:
```console
$ pip install crossandra
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip`
instead)

## Contributing

Contributions are welcome!

Please open an issue before submitting a pull request (unless it's a minor
change like fixing a typo).

To get started:

1. Clone your fork of the project.
2. Set up the project with `just install` (uses [uv]).
3. After you're done, run `just check` to check your changes.

!!! note
    If you don't want to use [`just`][just], simply look up the recipes
    in the project's [`justfile`][justfile].

## License
Crossandra is licensed under the MIT License.

If you have any questions, or would like to get in touch, join my
[Discord server]!

[Documentation]: https://github.com/trag1c/crossandra/wiki/The-Crossandra-class
[Discord server]: https://discord.gg/C8QE5tVQEq
[just]: https://github.com/casey/just
[justfile]: https://github.com/trag1c/crossandra/blob/main/justfile
[uv]: https://github.com/astral-sh/uv
