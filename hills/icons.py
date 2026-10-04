"""Line icons (24×24, stroke = currentColor). One per region, one per experience kind, plus UI icons.

Drawn for this site; render with {% icon "darjeeling" %} or {% icon "darjeeling" "icon--lg" %}.
"""

ICONS = {
    # ---- regions
    "east-sikkim":  # rhododendron bloom over Tsomgo's water
        '<circle cx="12" cy="8" r="2"/><path d="M12 6c-.6-2 .4-3.5 2-4 .6 1.8-.2 3.3-2 4z"/>'
        '<path d="M10.1 7.4C8.3 6.5 6.5 7 5.8 8.6c1.8.8 3.4.5 4.3-1.2z"/><path d="M13.9 7.4c1.8-.9 3.6-.4 4.3 1.2-1.8.8-3.4.5-4.3-1.2z"/>'
        '<path d="M10.6 9.6c-1.3 1.4-1.3 3.2 0 4.2 1-1.3 1.1-2.9 0-4.2zM13.4 9.6c1.3 1.4 1.3 3.2 0 4.2-1-1.3-1.1-2.9 0-4.2z"/>'
        '<path d="M2 18c2-.9 4-.9 6 0s4 .9 6 0 4-.9 6 0M4 21.5c1.6-.6 3.2-.6 4.8 0s3.2.6 4.8 0 3.2-.6 4.8 0"/>',
    "north-sikkim":  # snow peak above a high lake (Gurudongmar)
        '<path d="M2 16l6.5-10L12 11l2.5-3.5L22 16z"/><path d="M6.6 9l1.9 1.6L10 8.4"/><path d="M13.3 9.2l1.2 1 1.1-1.3"/>'
        '<path d="M4 19c2.7-.8 5.3-.8 8 0s5.3.8 8 0"/><path d="M7 21.5c1.7-.5 3.3-.5 5 0s3.3.5 5 0"/>',
    "west-sikkim":  # chorten with a strand of prayer flags
        '<path d="M5 21h14"/><path d="M7 21v-2h10v2"/><path d="M8.5 19v-2.5h7V19"/><path d="M9 16.5a3 3 0 0 1 6 0"/>'
        '<path d="M10.8 13.5h2.4V12h-2.4z"/><path d="M11.2 12L12 6l.8 6"/><path d="M12 6V4.2"/>'
        '<path d="M2 4.5c3.5 1.8 6.5 2 10 .5"/><path d="M4 5.6l.4 1.7 1.3-1.2M7.4 6.3l.4 1.6 1.2-1.3"/>',
    "darjeeling":  # toy train: B-class saddle-tank locomotive
        '<path d="M3 17h15v-5H8V9H4v8"/><path d="M8 12V7h4v5"/><path d="M5 9V6.5M4 6.5h2"/>'
        '<path d="M18 12h2.5v5H18"/><circle cx="6.5" cy="18.5" r="1.7"/><circle cx="11.5" cy="18.5" r="1.7"/><circle cx="16" cy="18.5" r="1.7"/>'
        '<path d="M2 21h20"/><path d="M5 4.5c1-1 2.5-1 3.5-2"/>',
    "kalimpong":  # orchid (cymbidium) spray
        '<path d="M12 21c0-5 1.5-9 5-12"/><path d="M12 11.5c-1.4-1.7-1.2-3.6.6-4.6 1 1.8.6 3.5-.6 4.6z"/>'
        '<path d="M11.3 12.6c-2.1.3-3.7-.8-3.9-2.8 2-.2 3.5.8 3.9 2.8zM13 12.6c2.1.3 3.7-.8 3.9-2.8-2-.2-3.5.8-3.9 2.8z"/>'
        '<path d="M12.2 13.2c-.9 1-1 2.2-.2 3 .9-.8 1-2 .2-3z"/><path d="M17 9c1.2-.4 2-1.3 2.2-2.6-1.3.1-2.2.9-2.2 2.6z"/>'
        '<path d="M8 21c.5-2 1.6-3.4 3-4.2M16 21c-.4-1.6-1.3-2.8-2.6-3.6"/>',
    "dooars":  # one-horned rhino
        '<path d="M3.5 14c0-3 2.6-5 6.5-5h4.5c2.3 0 3.8 1 4.6 2.6l1.4-1.8.5 3.2-1.2 1V17h-2v-2.4h-2.4V17h-2v-2.6H9V17H7v-2.8c-1.5 0-2.6-.5-3.5-1.2z"/>'
        '<path d="M19 11.6l1.6-3"/><path d="M17 11.2h.01"/><path d="M14 9.2c.4-1 .4-1.8 0-2.6"/><path d="M2 20h20"/>',
    "bhutan":  # dzong: battered walls, red band, golden roof
        '<path d="M2.5 21h19"/><path d="M4 21l1.2-8.5h13.6L20 21"/><path d="M5.2 12.5h13.6"/><path d="M5.5 14.5h13"/>'
        '<path d="M8.5 12.5V9h7v3.5"/><path d="M7 9l5-4 5 4z"/><path d="M12 5V3.2"/><path d="M10.5 21v-3a1.5 1.5 0 0 1 3 0v3"/>'
        '<path d="M7 17h.01M17 17h.01"/>',
    # ---- experience kinds
    "culture": '<path d="M3 21h18M4 9h16M12 3l9 6H3z"/><path d="M6 9v12M10 9v12M14 9v12M18 9v12"/>',
    "spiritual":  # prayer wheel on a handle
        '<rect x="7" y="5" width="8" height="9" rx="1.5"/><path d="M7 8h8M7 11h8"/><path d="M11 5V3M11 14v7"/><path d="M15 6.5c2 0 3.5-1 4.5-2.5"/><circle cx="20" cy="3.6" r="1"/>',
    "nature": '<path d="M2 20l7-11 4 6 3-4 6 9z"/><circle cx="17.5" cy="5.5" r="2"/>',
    "wildlife":  # hornbill
        '<path d="M4 16c1-4 4.5-6.5 8.5-6.5 2 0 3.3.7 4.2 1.8L21 12l-4 1.2c-.5 2.8-2.8 4.8-6 4.8H4z"/>'
        '<path d="M14 9.6c.8-1.3 2.2-2 3.6-1.8l-.9 3.5"/><path d="M15.3 11.2h.01"/><path d="M8 18l-1 3M11 18l.5 3"/>',
    "food":  # momo steamer with dumplings
        '<path d="M3 11h18"/><path d="M4 11v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6"/><path d="M4 14h16"/>'
        '<path d="M7 11c0-1.6 1.1-2.6 2.3-2.6s2.2 1 2.2 2.6M12.5 11c0-1.6 1.1-2.6 2.3-2.6s2.2 1 2.2 2.6"/>'
        '<path d="M9.3 6c0-1 .7-1.4.7-2.4M14.8 6c0-1 .7-1.4.7-2.4"/>',
    "adventure":  # trekking pole on a ridge
        '<path d="M3 20l6-9 3 4 3-5 6 10z"/><path d="M15 10l-2-7"/><path d="M12.4 3.2l1.4-.6"/><circle cx="6" cy="5" r="1.4"/>',
    "tea":  # two leaves and a bud
        '<path d="M12 21c-.5-5.5 1.5-10 7-13.5.5 6.5-2 11-7 13.5z"/><path d="M12 21c-4-1.5-7-5-7-10.5 4 1.5 6.5 4.5 7 10.5z"/>'
        '<path d="M12 21c.3-3 1.5-6 4-8.5M12 21c-1-2.5-2.5-5-5-7"/><path d="M12.5 7c-.8-1.6-.6-3 .5-4 1 1.2.9 2.6-.5 4z"/>',
    "snow": '<path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7"/><path d="M9.5 3.5L12 6l2.5-2.5M9.5 20.5L12 18l2.5 2.5"/>'
            '<path d="M3.2 10.4L6.6 9.5 5.7 6.1M18.3 17.9l-.9-3.4 3.4-.9M3.2 13.6l3.4.9-.9 3.4M18.3 6.1l-.9 3.4 3.4.9"/>',
    "craft":  # loom cloth with pattern
        '<path d="M4 3h16M4 21h16"/><path d="M6 3v18M18 3v18"/><path d="M6 8h12M6 16h12"/><path d="M9 8l3 4-3 4M15 8l-3 4 3 4"/>',
    "village":  # hill house with a stone path
        '<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-5h4v5"/><path d="M7.5 12.5h2M14.5 12.5h2"/><path d="M2 22c3-1 5-1 8 0"/>',
    # ---- UI
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h6"/>',
    "star": '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "bed": '<path d="M3 19V6M21 19v-6a3 3 0 0 0-3-3h-8v6"/><path d="M3 16h18"/><circle cx="6.5" cy="12" r="1.8"/>',
    "jeep":  # shared hill jeep with roof luggage
        '<path d="M3 16v-4l2-4h10l3 4h3v4"/><path d="M5 8V6.5h9V8"/><path d="M7 12h10"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>',
    "rupee": '<path d="M7 4h10M7 8.5h10M7 4c4.5 0 6 1.2 6 4.5S10.5 13 7 13l8 7"/>',
    "ticket": '<path d="M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4z"/><path d="M15 7v10" stroke-dasharray="1.5 2"/>',
    "mountain": '<path d="M2 20l7-12 4 6 2-3 7 9z"/><path d="M7.2 11l1.8 1.5 1.6-2"/>',
    "story": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/><path d="M9 8h6"/>',
    "permit": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h4"/><circle cx="16.5" cy="16.5" r="1.5"/>',
    "flag": '<path d="M2 6c4 2 8 2 12 0s6-1 8 0"/><path d="M4 7l1 4 2.5-3M9 7.6l.8 4 2.6-3.2M14.5 6.6l.8 4 2.6-3.1"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
}


def svg(name, cls=""):
    body = ICONS.get(name) or ICONS["sparkle"]
    return (f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')
