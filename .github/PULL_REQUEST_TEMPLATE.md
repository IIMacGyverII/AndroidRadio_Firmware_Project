## What this changes

<!-- one paragraph -->

## Checklist

- [ ] No callsign, DMR ID, location, phone serial, passcode or IP address anywhere in the diff or the commit messages.
- [ ] `python scripts/build_catalog.py --check` passes.
- [ ] If an image was added: it is stock or released (not bench or beta); `manifest.json` has provenance that reproduces the bytes (commit + script, or stock app asset + hash); its `README.md` says what it changes; the device's `variants.json` row is updated.
- [ ] If the catalogue changed: `serial` bumped, `firmware.json` and `firmware.json.sig` committed together, `python scripts/verify_catalog.py` passes.
- [ ] If a device was added or changed: `README.md`, `device.json` (schema-valid) and `variants.json`, each fact with its source.
- [ ] `CHANGELOG.md` entry, newest first.
- [ ] `CLAUDE.md` and `GROK.md` still byte-identical (`git diff --no-index CLAUDE.md GROK.md` prints nothing).
