# Chromium-to-Firefox extension

![License](https://img.shields.io/github/license/44digits/chromium_to_firefox_extension)
![Platform](https://img.shields.io/badge/platform-Ubuntu%20%28Snap%29-E95420)
![Browsers](https://img.shields.io/badge/browsers-Chromium%20%7C%20Firefox-blue)

This extension adds a right-click option for opening links from Chromium in Firefox.

It was created to keep Google applications (such as Gmail and Gemini) in Chromium while
opening other websites in Firefox. Right-click any link in Chromium and select the option
to open it in Firefox.

## Prerequisites

This extension was created for a specific setup:
- Ubuntu
- Chromium installed as a Snap
- Firefox installed as a Snap

Snap-packaged Chromium has tighter restrictions than a traditional installation in
`/usr/bin` or `/usr/local/bin`. For example, it cannot directly run a shell script to
launch Firefox with a specific URL. This extension therefore includes a small Python API
server that Chromium can contact on the local machine.

## How it works

The extension consists of four files:
- `manifest.json`: Defines the extension for Chromium.
- `background.js`: Adds the right-click option and forwards selected link URLs.
- `firefox_relay_server.py`: Runs the Python server that receives requests on port 18080.
- `chromium-firefox-relay.desktop`: Launches the Python server and Chromium together.

When you right-click a link in Chromium and select **Open link in Firefox**, the extension
sends its URL to the Python server on port 18080. The server then launches Firefox with
that URL.

## Installation

1. **Prepare the files.**
   - Place the extension files in a permanent location, such as `~/bin/chromium_to_firefox_extension/`.
   - Edit `chromium-firefox-relay.desktop` and replace `<<PATH TO EXTENSION>>` in the `Exec` line with the full path to that directory.
2. **Load the extension in Chromium.**
   - Open `chrome://extensions/`.
   - Turn on **Developer mode** in the upper-right corner.
   - Select **Load unpacked**, then choose the directory containing `manifest.json`.
3. **Install the desktop launcher.**
   - Copy `chromium-firefox-relay.desktop` to `~/.local/share/applications/`.
   - Find Chromium in the Ubuntu app menu and add its launcher to the dock.
4. Launch Chromium using the desktop launcher so the Python server starts too.
5. Right-click a link in Chromium and select **Open link in Firefox**.

## Limitations and security

This extension is intended for a single user and is not configured for system-wide use.
The Python server does not authenticate requests. 
It listens on the local machine and opens URLs requested by clients that can reach it.