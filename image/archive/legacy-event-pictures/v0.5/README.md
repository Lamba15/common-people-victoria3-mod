# Legacy event picture archive - v0.5

These DDS files were removed from `mod/gfx/event_pictures/` during the v0.5 rebuild because no current event references them.

They are kept here as non-shipped comparison material for the Layla art A/B pass. The active shipped event-art pool is audited by `script/audit-event-images.py --strict-size --strict-unused` and should remain:

```text
Referenced DDS: 112
Shipped DDS:    112
Missing:        0
Unused shipped: 0
Dimensions:     112 at 600x400
Non-standard referenced images: 0
```

Do not copy these files back into `mod/gfx/event_pictures/` unless an event is explicitly wired to use them again.
