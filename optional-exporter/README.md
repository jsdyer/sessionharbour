# Optional local Chrome / Edge tab exporter

Use the browser's normal **Bookmark all tabs** and bookmark export features if you prefer not to install an extension. This small Manifest V3 extension is another option when the original browser is available but its on-disk session file is encrypted.

1. Download or clone this repository.
2. Open Chrome's Extensions page (`chrome://extensions`) or Edge's equivalent.
3. Enable Developer mode, choose **Load unpacked**, and select this `optional-exporter` folder.
4. Open the extension popup and click **Download tab export**.
5. Import the JSON file into Session Harbour.
6. Remove the extension from the Extensions page when finished.

The extension asks for **tabs** permission because reading all open tab titles/URLs requires it. There is no background script, host permission, network request, telemetry, sync storage or remote code. Export happens only on the popup button click. Incognito tabs are excluded and incognito access is not needed. Browser-internal links may be exported but Session Harbour excludes them from opening/restoration.

The export is a portable link inventory, not cookies, passwords, browsing-history recovery or a full session restore. Files can contain private URLs. Review this tiny source before installing; this optional helper is not required for the main tool.
