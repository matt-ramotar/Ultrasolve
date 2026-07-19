# Ultrasolve Privacy Policy

Effective date: 2026-07-19.

This policy covers the Ultrasolve plugin, the Agent Skills collection in this
repository, distributed for use with Claude Code, Codex, and other Agent
Skills clients. It is written by the plugin's author and applies to the
plugin itself, not to the host application you run it in.

## What Ultrasolve is

Ultrasolve's runtime surface is static instruction files in Markdown plus
JSON manifests. It executes nothing itself. There are no MCP servers, no
hooks, no bundled binaries, and no scripts that run in your session. The
repository also contains a Python test suite, which is development tooling
and is never loaded by your host. Your AI coding host loads the instructions
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
content. There is no code and no service behind it that could.

## Files the plugin reads

The instructions direct the agent to read files inside the plugin's own
directory, specifically the router's integrity preflight and the six method
files. They also permit the agent to use tools already available in your
host, such as research tools, when facts are missing. Any such use runs
under your host's permission controls and policies, not under this plugin.

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
