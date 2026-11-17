# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This project adheres to both [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## [Unreleased]

## [1.0.0] - 2026-11-17

### Added

- `ThreadSensitiveMiddleware`, which runs each connection in its own `ThreadSensitiveContext` and closes the database connections opened on that context's thread when the connection ends.
- Support for Python 3.15 and Django 6.1 (Django 6.1 is the only supported version on Python 3.15).

### Changed

- On Python 3.15+, `consumers`, `layers`, `middleware` and `sites` use lazy imports (`__lazy_modules__`). In particular, `channels_extensions.sites` can now be imported before the Django app registry is ready.
- Development Status classifier is now `Production/Stable`.

### Fixed

- `JsonWebsocketConsumer.encode_json` now uses `django_orjson.default`, matching `AsyncJsonWebsocketConsumer`.

## [0.0.1] - 2026-07-28

### Added

- This CHANGELOG file.
- `DummyChannelLayer` empty channel layer implementation
- `get_channel_layer` shortcut which raises an error for missing aliases
- `CurrentSiteMiddleware` that mimics django's own `CurrentSiteMiddleware`
- `JsonWebsocketConsumer` and `AsyncJsonWebsocketConsumer` for `orjson`-backed WebSocket JSON handling

[unreleased]: https://github.com/hartungstenio/channels-extensions/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hartungstenio/channels-extensions/compare/v0.0.1...v1.0.0
[0.0.1]: https://github.com/hartungstenio/channels-extensions/releases/tag/v0.0.1
