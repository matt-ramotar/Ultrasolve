# Ultrasolve Privacy Policy

Effective date: 2026-07-19.

This policy covers the Ultrasolve plugin, the Agent Skills collection in this
repository, distributed for use with Claude Code, Codex, and other Agent
Skills clients. It is written by the plugin's author and applies to the
plugin itself, not to the host application you run it in.

## What Ultrasolve is

Ultrasolve's runtime surface is static instruction files in Markdown plus
JSON manifests and YAML host metadata. It executes nothing itself. There are no MCP servers, no
hooks, no bundled binaries, and no scripts that run in your session. The
repository also contains Python tests, a local checker, and a runtime bundle
builder. These are development tools and never auto-run in a host session.
The bundle builder copies an explicit set of runtime files and writes an
external content manifest; it makes no network or model calls. Your AI coding host loads the instructions
into a session the same way it loads any other text.

## Data collection

Ultrasolve collects no data. It has no telemetry, no analytics, no accounts,
and no cookies, and it initiates no network requests. The author receives
nothing when you install it, use it, or uninstall it.

## How your content is processed

The problems you bring to the router, and everything else in your session,
are processed by your host agent (for example Claude Code or Codex) under
that host's own privacy policy and settings. Ultrasolve adds instructions to
that session and nothing more. It does not see, store, or transmit your
content. No runtime service receives it.

## Files the plugin reads

The instructions direct the agent to read files inside the plugin's own
directory: the definition entry and its references, plus the router's
integrity preflight, shared workflow contract, and six method modules. They also permit the agent to
use tools already available in your host, such as research tools, when facts
are missing. Any such use runs under your host's permission controls and
policies, not under this plugin.

## Third-party links

The documentation cites external sources, including the Internet Archive,
the ACM Digital Library, and the RFC Editor. Following those links is
governed by those sites' policies. The plugin never fetches them on its own.

## Distribution platforms

If you install Ultrasolve through a marketplace or repository host, that
platform may collect installation or usage metrics under its own policy. The
author receives no personal data from distribution.

## Changes

Changes to this policy are made in this file and are visible in the
repository's version history.

## Contact

Contact Matt Ramotar at matt.ramotar@icloud.com.
