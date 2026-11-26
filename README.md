# Session Harbour

[Open Session Harbour](https://coolcode.ca/sessionharbour/) — inspect exported browser tabs and bookmarks locally, find duplicates, and export the useful links.

<!-- coolcode:guide -->
Import JSON sessions, bookmark HTML, URL lists or unencrypted Chromium SNSS v1/v3. Search titles/URLs, filter domains and duplicate URLs, select matching tabs, and export browser-importable bookmarks, portable JSON or URL text. Files, filenames and imported URLs never leave this browser tab unless you deliberately open a link. Reloading clears imported data.
<!-- /coolcode:guide -->

## Use

1. Choose a supported file (maximum 20 MB / 20,000 valid tabs), paste JSON/URLs, or try the example.
2. Search and filter. **Show one of each URL** compares exact normalized URLs; ignoring fragments is optional. Query parameters are preserved because they can identify different documents.
3. Click **Select matching** to replace the selection with the current filtered view. Filters do not silently alter your selection.
4. Export **Bookmark HTML** and import it in your browser to restore the chosen links. JSON and plain URL exports also work.

No source page, favicon or preview is fetched. Imported links open individually with `noopener noreferrer`; there is no automatic bulk-open behaviour.

## Formats

- JSON with URL/title objects in arrays, tabs/windows, session containers, or bookmark trees.
- Firefox session JSON selects the current navigation per tab and excludes closed-tab/closed-window containers.
- Netscape bookmark HTML.
- Plain HTTP(S) URLs, one per line; an optional tab-separated title is accepted.
- Chromium **SNSS v1/v3**, unencrypted, recovers tab URL/title/window/pinned information using session commands. It does not restore cookies, passwords, sign-ins, full navigation history or tab groups. If no selected navigation is available, the last recorded navigation is shown. Truncated/invalid commands fail rather than pretending the entire file was restored.
- Encrypted Chromium SNSS versions (including OS-bound **v5**) are explicitly rejected. Export from the original browser or use the [optional local tab exporter](optional-exporter/README.md).

Only HTTP(S) URLs without embedded credentials are accepted for opening/export. Browser-internal, file, data and JavaScript links are counted as excluded. Imports render as text; HTML is never inserted as application markup.

## Privacy

Files and imported values stay in memory. There is no upload endpoint, persistent session storage, remote favicon retrieval or remote preview. The ordinary CoolCode pageview counter sends only the tool ID and respects GPC / Do Not Track; imported URLs, titles, filenames and searches are never included. Clicking an imported link intentionally visits that site. Exported files may contain private URLs.

## Expand or customize

Parser and limits: `web/model.mjs`. UI and display batch size: `web/app.mjs`. Add a format by converting it to `{url,title,group,pinned}` rows and passing it through `normalizeTabs`; add fixtures for unsafe schemes, malformed data and a real structural edge case. Import supports arbitrary valid sites; the sample is not an allowlist. Raising limits should be tested with large exports first.

No API key, server, scheduled collection or collector watchdog target is required. The optional exporter is installable only by choice; using the main browser app requires no extension.

## Build and publish

```bash
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

The production tool has no package dependencies. Test-only Playwright/Chromium runs `tests/browser_smoke.py`. Main pushes and manual workflow runs test and publish GitHub Pages.

## Chromium format references

- [Session commands](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sessions/core/session_service_commands.cc)
- [Navigation serialization](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sessions/core/serialized_navigation_entry.cc)
- [Storage versions and OS-bound encryption](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sessions/core/command_storage_backend.cc)

The parser is an independent bounded implementation of the documented source layout; it is not a Chromium component or an official browser recovery service.

## Ready-to-use example

[Find Duplicate Tabs in a Browser Session](https://coolcode.ca/sessionharbour/duplicate-tabs.html) opens this scenario in the same tool. Explore a small example session containing repeated links. Inspect the duplicated tabs, change the matching rules and export selected links. Choose your own session export to run the same comparison locally.
