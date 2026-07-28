# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This project adheres to both [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## [UNRELEASED]

## [0.0.1] - 2026-07-28

### Added

- This CHANGELOG file.
- `DummyChannelLayer` empty channel layer implementation
- `get_channel_layer` shortcut which raises an error for missing aliases
- `CurrentSiteMiddleware` that mimics django's own `CurrentSiteMiddleware`
- `JsonWebsocketConsumer` and `AsyncJsonWebsocketConsumer` for `orjson`-backed WebSocket JSON handling

[unreleased]: https://github.com/hartungstenio/channels-extensions/compare/0.0.1...HEAD
[0.0.1]: https://github.com/hartungstenio/channels-extensions/releases/tag/0.0.1
