# Modules

The radio module is the part the firmware actually runs on. Several phones share one module family, so the chip
facts, the protocol, and the update mode are written once here and the device pages refer to them. Addresses inside
an image are per image; a module page says which image each address was read from.

| Folder | Module | Found in |
|---|---|---|
| `sa818-class-pb202` | SA818-class analog FM module, AT commands over a UART; version `PB202EU05` | ANYSECU W6+ (measured) |
| `hr-c7000` | HR-C7000 baseband (C-SKY V2 core) + AT1846S RF IC; version strings `DMR003.*` and `DMR006.*` | Ulefone Armor 26 Ultra (measured), Armor 20WT, Armor 3WT, Unihertz Atom XL, Blackview Xplore 1 (read or reported) |
