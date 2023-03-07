# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2023-03-07

### Added
- `py.typed`
- more very explicit typehints

## [1.2.4] - 2022-12-10

### Changed
- Speed improvements (up to 5x faster for pure Python wheels & up to 30% faster for mypyc-compiled wheels)

Big thanks to [@CircuitSacul](https://github.com/CircuitSacul) for implementing the faster algorithm! ❤️

## [1.2.3] - 2022-11-22

### Fixed
- Crossandra now builds correctly for Python 3.10+ (big thanks to [@Lunarmagpie](https://github.com/Lunarmagpie) for fixing that)

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
