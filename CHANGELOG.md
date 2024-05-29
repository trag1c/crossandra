# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2.2.1] - 2024-05-29

### Fixed
- Fixed mypyc wheels failing to generate a tree for a non-empty enum ([#36])

[#36]: https://github.com/trag1c/crossandra/issues/36

## [2.2.0] - 2024-05-29

### Added
* `RuleGroup.apply`
* `common.ANY_INT`
* `common.ANY_FLOAT`
* `common.ANY_NUMBER`

## [2.1.0] - 2024-05-01

This release should also include mypyc wheels for Python 3.12 on PyPI.

### Added
- `Rule` objects now accept `re.Pattern` for `pattern`
- Improved typing for `Rule.__eq__`, `Rule.__or__`, and `RuleGroup.__or__`
- `Rule` objects can now be unioned with `RuleGroups`

### Fixed
- The `common.NUMBER` and `common.SIGNED_NUMBER` rule groups now correctly
  prioritize floats over integers

## [2.0.0] - 2023-04-29

### Added
- Aliases for enums
- API tests
- Common pattern tests (big thanks to [@qexat](https://github.com/qexat))
- Docstrings
- Python 3.8 support
- Typehints and docstrings are now supported when using mypyc wheels (big thanks
  to [@Lunarmagpie](https://github.com/Lunarmagpie))

### Changed
- Allowed underscores in numeric literal patterns
- `CrossandraTokenizationError` and `CrossandraValueError` are now raised
  instead of `CrossandraError` (it can be used to catch both exceptions)
- Improved documentation
- `Rule` objects are now comparable, hashable, and immutable
- Slightly improved performance when tokenizing with empty enums (up to 10%
  faster)
- The `IGNORED`/`NOT_APPLIED` constants (and their types) can now be imported
  directly
- The pre-tokenization CRLF to LF conversion can now be disabled through the
  `Crossandra(convert_crlf=...)` parameter
- Updated `Rule` signature:
  - `Rule(converter=True)` -> `Rule(converter=None)`
  - `Rule(converter=False)` -> `Rule(ignore=True)`
  - `flags` is now a keyword-only argument

### Fixed
- Fixed bad traversal bug (big thanks to
  [@CircuitSacul](https://github.com/CircuitSacul))
- Fixed common patterns:
  - `CHAR`
  - `DECIMAL`
  - `FLOAT` (and its derivatives)


## [1.3.0] - 2023-03-07

### Added
- `py.typed`
- more very explicit typehints


## [1.2.4] - 2022-12-10

### Changed
- Speed improvements (up to 5x faster for pure Python wheels & up to 30% faster
  for mypyc-compiled wheels)

Big thanks to [@CircuitSacul](https://github.com/CircuitSacul) for implementing
the faster algorithm! ❤️


## [1.2.3] - 2022-11-22

### Fixed
- Crossandra now builds correctly for Python 3.10+ (big thanks to 
  [@Lunarmagpie](https://github.com/Lunarmagpie) for fixing that)


## [1.2.2] - 2022-11-18

### Fixed
- Fixed `Ignored` objects being included in the output


## [1.2.1] - 2022-11-18

### Fixed
- Made `Rule` a regular class to comply with mypyc


## [1.2.0] - 2022-11-18

### Added
- Building with `mypyc`

### Changed
- `Rule.converter` is now of type `Callable | bool` and defaults to `True`

### Fixed
- Rule converters can now return `None`


## [1.1.0] - 2022-11-17

### Added
- Included `CrossandraError` in `__all__`
- RegEx flag support for `Rule`


## [1.0.0] - 2022-11-17

Initial release 🎉

[1.0.0]: https://github.com/trag1c/crossandra/releases/tag/1.0.0
[1.1.0]: https://github.com/trag1c/crossandra/compare/1.0.0...1.1.0
[1.2.0]: https://github.com/trag1c/crossandra/compare/1.1.0...1.2.0
[1.2.1]: https://github.com/trag1c/crossandra/compare/1.2.0...1.2.1
[1.2.2]: https://github.com/trag1c/crossandra/compare/1.2.1...1.2.2
[1.2.3]: https://github.com/trag1c/crossandra/compare/1.2.2...1.2.3
[1.2.4]: https://github.com/trag1c/crossandra/compare/1.2.3...1.2.4
[1.3.0]: https://github.com/trag1c/crossandra/compare/1.2.4...1.3.0
[2.0.0]: https://github.com/trag1c/crossandra/compare/1.3.0...2.0.0
[2.1.0]: https://github.com/trag1c/crossandra/compare/2.0.0...2.1.0
[2.2.0]: https://github.com/trag1c/crossandra/compare/2.1.0...2.2.0
[2.2.1]: https://github.com/trag1c/crossandra/compare/2.2.0...2.2.1
