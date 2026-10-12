# Chromium to firefox extension
Extension to allow on links in Chromium to open in Firefox with a right-click.

This extension was created for a very specific environment:
- Ubuntu OS
- Chromium installed as snap
- Firefox installed as snap

Chromium as a snap has greater restrictions than Chromium installed traditionally in `/usr/bin` or `/usr/local/bin`.
For example it cannot run a bash script that could launch Firefox with a specific url.
This extension therefore includes a "tiny" Python API server which Chromium does have permission to call on localhost.

## Files

- manifest.json
- background.js
- firefox_relay_server.py
- chromium-firefox-relay.desktop

## Instructions

