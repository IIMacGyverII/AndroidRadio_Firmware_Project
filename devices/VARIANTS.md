# Firmware variants: the registry

One phone model can ship with more than one module firmware, and one module version string can sit on top of
more than one stock-app asset. The loader's identity check answers "is this exactly a known variant?"; this
registry is where the known variants, and the unknown ones people have seen, are recorded.

Each device folder has a `variants.json`:

```json
{
  "device": "ulefone-armor-26-ultra",
  "variants": [
    {
      "moduleVersion": "DMR003.UV4T.V022",
      "stockApp": { "package": "com.pri.prizeinterphone", "version": "V1.0" },
      "assetSha256": "90e361fd…",
      "assetSize": 378620,
      "supportedBase": true,
      "reports": 1,
      "firstSeen": "2026-10-13",
      "lastSeen": "2026-10-25",
      "source": "measured",
      "notes": "the reference phone"
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `moduleVersion` | what `0x34` returned, verbatim |
| `stockApp` | the stock radio app's package and version on that phone |
| `assetSha256`, `assetSize` | the firmware asset inside that stock APK; `null` until someone extracts it |
| `supportedBase` | true only when this repository holds that stock image and patches are built on it |
| `reports` | how many distinct device reports showed this combination (never who) |
| `firstSeen`, `lastSeen` | dates of those reports |
| `source` | `measured` (we ran it), `report` (a device report), `read` (stock app code only) |

`scripts/build_catalog.py` folds every `variants.json` into the signed catalogue under `variants`, so SignalDeck
can tell a user "this variant is known, seen N times, not supported yet" instead of only "unknown". A variant
becomes `supportedBase: true` only when its stock image is added under `firmware/` with its manifest.

**How variants get here:** the "Firmware variant seen" issue form, filled from a SignalDeck device report. The
report contains the version string and the asset hash; nothing about the person is copied.
