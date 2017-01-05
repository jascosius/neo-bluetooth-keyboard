# -*- coding: utf-8 -*-
#
# www.linuxuser.co.uk/tutorials/emulate-a-bluetooth-keyboard-with-the-raspberry-pi
#
#
#
# Convert value returned from Linux event device ("evdev") to a HID code. This
# is reverse of what's actually hardcoded in the kernel.
#
# Lubomir Rintel <lkundrak@v3.sk>
# License: GPL
#
# Ported to a Python module by Liam Fraser.
#

#[LShift 2,LAlt 4]

converttable = [
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]],
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]],
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]],
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]],
  [[[0,0],0x18],[[1,0],0x18],[[1,1],0x24],[[0,0],0x4A],[[0,0],0x00],[[0,0],0x00]], # 4 0x04 - US: A         , DE: A         , Layer 1: u         , Layer 2: U         , Layer 3: \         , Layer 4: Pos1
  [[[0,0],0x1C],[[1,0],0x1C],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], # 5 0x05 - US: B         , DE: B         , Layer 1: z         , Layer 2: Z         , Layer 3: `         , Layer 4: 
  [[[0,0],0x34],[[1,0],0x34],[[0,1],0x24],[[0,0],0x49],[[0,0],0x00],[[0,0],0x00]], # 6 0x06 - US: C         , DE: C         , Layer 1: ä         , Layer 2: Ä         , Layer 3: |         , Layer 4: Einfügen
  [[[0,0],0x04],[[1,0],0x04],[[0,1],0x25],[[0,0],0x51],[[0,0],0x00],[[0,0],0x00]], # 7 0x07 - US: D         , DE: D         , Layer 1: a         , Layer 2: A         , Layer 3: {         , Layer 4: Untere Pf.
  [[[0,0],0x0F],[[1,0],0x0F],[[0,1],0x22],[[0,0],0x52],[[0,0],0x00],[[0,0],0x00]], # 8 0x08 - US: E         , DE: E         , Layer 1: l         , Layer 2: L         , Layer 3: [         , Layer 4: Obere Pf.
  [[[0,0],0x08],[[1,0],0x08],[[0,1],0x26],[[0,0],0x4F],[[0,0],0x00],[[0,0],0x00]], # 9 0x09 - US: F         , DE: F         , Layer 1: e         , Layer 2: E         , Layer 3: }         , Layer 4: Rechte Pf.
  [[[0,0],0x12],[[1,0],0x12],[[1,0],0x30],[[0,0],0x4D],[[0,0],0x00],[[0,0],0x00]], #10 0x0A - US: G         , DE: G         , Layer 1: o         , Layer 2: O         , Layer 3: *         , Layer 4: Ende
  [[[0,0],0x16],[[1,0],0x16],[[1,0],0x2D],[[0,1],0x2D],[[0,0],0x00],[[0,0],0x00]], #11 0x0B - US: H         , DE: H         , Layer 1: s         , Layer 2: S         , Layer 3: ?         , Layer 4: ¿
  [[[0,0],0x0A],[[1,0],0x0A],[[1,0],0x35],[[0,0],0x25],[[0,0],0x00],[[0,0],0x00]], #12 0x0C - US: I         , DE: I         , Layer 1: g         , Layer 2: G         , Layer 3: >         , Layer 4: 8
  [[[0,0],0x11],[[1,0],0x11],[[1,0],0x25],[[0,0],0x21],[[0,0],0x00],[[0,0],0x00]], #13 0x0D - US: J         , DE: J         , Layer 1: n         , Layer 2: N         , Layer 3: (         , Layer 4: 4
  [[[0,0],0x15],[[1,0],0x15],[[1,0],0x26],[[0,0],0x22],[[0,0],0x00],[[0,0],0x00]], #14 0x0E - US: K         , DE: K         , Layer 1: r         , Layer 2: R         , Layer 3: )         , Layer 4: 5
  [[[0,0],0x17],[[1,0],0x17],[[0,0],0x38],[[0,0],0x23],[[0,0],0x00],[[0,0],0x00]], #15 0x0F - US: L         , DE: L         , Layer 1: t         , Layer 2: T         , Layer 3: -         , Layer 4: 6
  [[[0,0],0x10],[[1,0],0x10],[[1,0],0x22],[[0,0],0x1E],[[0,1],0x10],[[0,0],0x00]], #16 0x10 - US: M         , DE: M         , Layer 1: m         , Layer 2: M         , Layer 3: %         , Layer 4: 1         , Layer 5: μ
  [[[0,0],0x05],[[1,0],0x05],[[0,0],0x30],[[1,0],0x37],[[0,0],0x00],[[0,0],0x00]], #17 0x11 - US: N         , DE: N         , Layer 1: b         , Layer 2: B         , Layer 3: +         , Layer 4: :
  [[[0,0],0x09],[[1,0],0x09],[[1,0],0x27],[[0,0],0x26],[[0,0],0x00],[[0,0],0x00]], #18 0x12 - US: O         , DE: O         , Layer 1: f         , Layer 2: F         , Layer 3: =         , Layer 4: 9
  [[[0,0],0x14],[[1,0],0x14],[[1,0],0x23],[[0,0],0x30],[[0,0],0x00],[[0,0],0x00]], #19 0x13 - US: P         , DE: P         , Layer 1: q         , Layer 2: Q         , Layer 3: &         , Layer 4: +
  [[[0,0],0x1B],[[1,0],0x1B],[[0,1],0x37],[[0,0],0x4B],[[0,0],0x00],[[0,0],0x00]], #20 0x14 - US: Q         , DE: Q         , Layer 1: x         , Layer 2: X         , Layer 3: …         , Layer 4: Bild hoch
  [[[0,0],0x06],[[1,0],0x06],[[0,1],0x23],[[0,0],0x4C],[[0,0],0x00],[[0,0],0x00]], #21 0x15 - US: R         , DE: R         , Layer 1: c         , Layer 2: C         , Layer 3: ]         , Layer 4: Entfernen
  [[[0,0],0x0C],[[1,0],0x0C],[[1,0],0x24],[[0,0],0x50],[[0,0],0x00],[[0,0],0x00]], #22 0x16 - US: S         , DE: S         , Layer 1: i         , Layer 2: I         , Layer 3: /         , Layer 4: Linke Pf.
  [[[0,0],0x1A],[[1,0],0x1A],[[0,0],0x00],[[0,0],0x4E],[[0,0],0x00],[[0,0],0x00]], #23 0x17 - US: T         , DE: T         , Layer 1: w         , Layer 2: W         , Layer 3: ^         , Layer 4: Bild runt.
  [[[0,0],0x0B],[[1,0],0x0B],[[0,0],0x35],[[0,0],0x24],[[0,0],0x00],[[0,0],0x00]], #24 0x18 - US: U         , DE: U         , Layer 1: h         , Layer 2: H         , Layer 3: <         , Layer 4: 7
  [[[0,0],0x13],[[1,0],0x13],[[0,1],0x11],[[0,0],0x28],[[0,0],0x00],[[0,0],0x00]], #25 0x19 - US: V         , DE: V         , Layer 1: p         , Layer 2: P         , Layer 3: ~         , Layer 4: Enter
  [[[0,0],0x19],[[1,0],0x19],[[1,0],0x38],[[0,0],0x2A],[[0,0],0x00],[[0,0],0x00]], #26 0x1A - US: W         , DE: W         , Layer 1: v         , Layer 2: V         , Layer 3: _         , Layer 4: Löschen
  [[[0,0],0x33],[[1,0],0x33],[[1,0],0x21],[[0,0],0x2B],[[0,0],0x00],[[0,0],0x00]], #27 0x1B - US: X         , DE: X         , Layer 1: ö         , Layer 2: Ö         , Layer 3: $         , Layer 4: Tab
  [[[0,0],0x0E],[[1,0],0x0E],[[1,0],0x1E],[[0,1],0x1E],[[0,0],0x00],[[0,0],0x00]], #28 0x1C - US: Y         , DE: Z         , Layer 1: k         , Layer 2: K         , Layer 3: !         , Layer 4: ¡
  [[[0,0],0x2F],[[1,0],0x2F],[[0,0],0x31],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #29 0x1D - US: Z         , DE: Y         , Layer 1: ü         , Layer 2: Ü         , Layer 3: #         , Layer 4: 
  [[[0,0],0x1E],[[1,1],0x2F],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #30 0x1E - US: 1         , DE: 1         , Layer 1: 1         , Layer 2: °         , Layer 3: ¹         , Layer 4:
  [[[0,0],0x1F],[[1,0],0x20],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #31 0x1F - US: 2         , DE: 2         , Layer 1: 2         , Layer 2: §         , Layer 3: ²         , Layer 4:
  [[[0,0],0x20],[[0,1],0x07],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #32 0x20 - US: 3         , DE: 3         , Layer 1: 3         , Layer 2:           , Layer 3: ³         , Layer 4: 
  [[[0,0],0x21],[[1,1],0x14],[[1,1],0x11],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #33 0x21 - US: 4         , DE: 4         , Layer 1: 4         , Layer 2: »         , Layer 3: ›         , Layer 4: 
  [[[0,0],0x22],[[0,1],0x14],[[1,1],0x05],[[1,1],0x26],[[0,0],0x00],[[0,0],0x00]], #34 0x22 - US: 5         , DE: 5         , Layer 1: 5         , Layer 2: «         , Layer 3: ‹         , Layer 4: ·
  [[[0,0],0x23],[[1,0],0x21],[[0,1],0x21],[[1,1],0x21],[[0,0],0x00],[[0,0],0x00]], #35 0x23 - US: 6         , DE: 6         , Layer 1: 6         , Layer 2: $         , Layer 3: ¢         , Layer 4: £
  [[[0,0],0x24],[[0,1],0x08],[[0,1],0x1D],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #36 0x24 - US: 7         , DE: 7         , Layer 1: 7         , Layer 2: €         , Layer 3: ¥         , Layer 4: 
  [[[0,0],0x25],[[1,1],0x1A],[[0,1],0x16],[[0,0],0x2B],[[0,0],0x00],[[0,0],0x00]], #37 0x25 - US: 8         , DE: 8         , Layer 1: 8         , Layer 2: „         , Layer 3: ‚         , Layer 4: Tab
  [[[0,0],0x26],[[0,1],0x1F],[[0,1],0x31],[[1,0],0x24],[[0,0],0x00],[[0,0],0x00]], #38 0x26 - US: 9         , DE: 9         , Layer 1: 9         , Layer 2: “         , Layer 3: ‘         , Layer 4: /
  [[[0,0],0x27],[[1,1],0x1F],[[0,0],0x00],[[1,0],0x30],[[0,0],0x00],[[0,0],0x00]], #39 0x27 - US: 0         , DE: 0         , Layer 1: 0         , Layer 2: ”         , Layer 3: ’         , Layer 4: *
  [[[0,0],0x28],[[1,0],0x28],[[0,0],0x28],[[0,1],0x28],[[0,0],0x28],[[0,0],0x28]], #40 0x28 - US: ENTER     , DE: Enter     , Layer 1: Enter     , Layer 2: Enter     , Layer 3: Enter     , Layer 4: Enter
  [[[0,0],0x29],[[0,0],0x29],[[0,0],0x29],[[0,0],0x29],[[0,0],0x29],[[0,0],0x29]], #41 0x29 - US: ESC       , DE: Escape    , Layer 1: Escape    , Layer 2: Escape    , Layer 3: Escape    , Layer 4: Escape
  [[[0,0],0x2A],[[0,0],0x2A],[[0,0],0x2A],[[0,0],0x2A],[[0,0],0x2A],[[0,0],0x2A]], #42 0x2A - US: BACKSPACE , DE: Löschen   , Layer 1: Löschen   , Layer 2: Löschen   , Layer 3: Löschen   , Layer 4: Löschen
  [[[0,0],0x2B],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #43 0x2B - US: TAB       , DE: Tab       , Layer 1: Tab       , Layer 2:           , Layer 3:           , Layer 4: 
  [[[0,0],0x2C],[[1,0],0x2C],[[0,0],0x2C],[[0,1],0x27],[[0,0],0x00],[[0,0],0x00]], #44 0x2C - US: SPACE     , DE: Leerzei.  , Layer 1: Leerzei.  , Layer 2: Leerzei.  , Layer 3: Leerzei.  , Layer 4: 0
  [[[0,0],0x38],[[1,1],0x38],[[0,0],0x00],[[0,0],0x38],[[0,0],0x00],[[0,0],0x00]], #45 0x2D - US: MINUS     , DE: ß         , Layer 1: -         , Layer 2:           , Layer 3:           , Layer 4: -
  [[[1,0],0x2E],[[1,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #46 0x2E - US: EQUAL     , DE: Akzent    , Layer 1: `         , Layer 2:           , Layer 3:           , Layer 4: 
  [[[0,0],0x2D],[[0,0],0x00],[[0,0],0x00],[[0,1],0x38],[[0,0],0x00],[[0,0],0x00]], #47 0x2F - US: LEFTBRACE , DE: Ü         , Layer 1: ß         , Layer 2:           , Layer 3:           , Layer 4: −
  [[[0,0],0x2E],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #48 0x30 - US: RIGHTBRACE, DE: Plus      , Layer 1: ´         , Layer 2:           , Layer 3:           , Layer 4: 
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #49 0x31 - US: BACKSLASH , DE: Raute     , Mod 3 
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #50 0x32 - US: 102ND     , DE: spitze K. , Mod 4
  [[[0,0],0x07],[[1,0],0x07],[[1,0],0x37],[[0,0],0x36],[[0,0],0x00],[[0,0],0x00]], #51 0x33 - US: SEMICOLON , DE: Ö         , Layer 1: d         , Layer 2: D         , Layer 3: :         , Layer 4: ,
  [[[0,0],0x1D],[[1,0],0x1D],[[0,1],0x0F],[[0,0],0x37],[[0,0],0x00],[[0,0],0x00]], #52 0x34 - US: APOSTROPHE, DE: Ä         , Layer 1: y         , Layer 2: Y         , Layer 3: @         , Layer 4: .
  [[[1,1],0x23],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #53 0x35 - US: GRAVE     , DE: Zirkumflex, Layer 1: ^         , Layer 2:           , Layer 3:           , Layer 4: 
  [[[0,0],0x36],[[0,1],0x38],[[1,0],0x1F],[[0,0],0x1F],[[0,0],0x00],[[0,0],0x00]], #54 0x36 - US: COMMA     , DE: Komma     , Layer 1: ,         , Layer 2: –         , Layer 3: "         , Layer 4: 2
  [[[0,0],0x37],[[0,1],0x2F],[[1,0],0x31],[[0,0],0x20],[[0,0],0x00],[[0,0],0x00]], #55 0x37 - US: DOT       , DE: Punkt     , Layer 1: .         , Layer 2: •         , Layer 3: '         , Layer 4: 3
  [[[0,0],0x0D],[[1,0],0x0D],[[1,0],0x36],[[1,0],0x36],[[0,0],0x00],[[0,0],0x00]], #56 0x38 - US: SLASH     , DE: Bindestr. , Layer 1: j         , Layer 2: J         , Layer 3: ;         , Layer 4: ;
  [[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #57 0x39 - US: CAPSLOCK  , DE: Umschalt  , Mod 3 
  [[[0,0],0x3A],[[0,0],0x3A],[[0,0],0x3A],[[0,0],0x3A],[[0,0],0x3A],[[0,0],0x3A]], #58 0x3A - US: F1        , DE: F1        , Layer 1: F1        , Layer 2: F1        , Layer 3: F1        , Layer 4: F1
  [[[0,0],0x3B],[[0,0],0x3B],[[0,0],0x3B],[[0,0],0x3B],[[0,0],0x3B],[[0,0],0x3B]], #59 0x3B - US: F2        , DE: F2        , Layer 1: F2        , Layer 2: F2        , Layer 3: F2        , Layer 4: F2
  [[[0,0],0x3C],[[0,0],0x3C],[[0,0],0x3C],[[0,0],0x3C],[[0,0],0x3C],[[0,0],0x3C]], #60 0x3C - US: F3        , DE: F3        , Layer 1: F3        , Layer 2: F3        , Layer 3: F3        , Layer 4: F3
  [[[0,0],0x3D],[[0,0],0x3D],[[0,0],0x3D],[[0,0],0x3D],[[0,0],0x3D],[[0,0],0x3D]], #61 0x3D - US: F4        , DE: F4        , Layer 1: F4        , Layer 2: F4        , Layer 3: F4        , Layer 4: F4
  [[[0,0],0x3E],[[0,0],0x3E],[[0,0],0x3E],[[0,0],0x3E],[[0,0],0x3E],[[0,0],0x3E]], #62 0x3E - US: F5        , DE: F5        , Layer 1: F5        , Layer 2: F5        , Layer 3: F5        , Layer 4: F5
  [[[0,0],0x3F],[[0,0],0x3F],[[0,0],0x3F],[[0,0],0x3F],[[0,0],0x3F],[[0,0],0x3F]], #63 0x3F - US: F6        , DE: F6        , Layer 1: F6        , Layer 2: F6        , Layer 3: F6        , Layer 4: F6
  [[[0,0],0x40],[[0,0],0x40],[[0,0],0x40],[[0,0],0x40],[[0,0],0x40],[[0,0],0x40]], #64 0x40 - US: F7        , DE: F7        , Layer 1: F7        , Layer 2: F7        , Layer 3: F7        , Layer 4: F7
  [[[0,0],0x41],[[0,0],0x41],[[0,0],0x41],[[0,0],0x41],[[0,0],0x41],[[0,0],0x41]], #65 0x41 - US: F8        , DE: F8        , Layer 1: F8        , Layer 2: F8        , Layer 3: F8        , Layer 4: F8
  [[[0,0],0x42],[[0,0],0x42],[[0,0],0x42],[[0,0],0x42],[[0,0],0x42],[[0,0],0x42]], #66 0x42 - US: F9        , DE: F9        , Layer 1: F9        , Layer 2: F9        , Layer 3: F9        , Layer 4: F9
  [[[0,0],0x43],[[0,0],0x43],[[0,0],0x43],[[0,0],0x43],[[0,0],0x43],[[0,0],0x43]], #67 0x43 - US: F10       , DE: F10       , Layer 1: F10       , Layer 2: F10       , Layer 3: F10       , Layer 4: F10
  [[[0,0],0x44],[[0,0],0x44],[[0,0],0x44],[[0,0],0x44],[[0,0],0x44],[[0,0],0x44]], #68 0x44 - US: F11       , DE: F11       , Layer 1: F11       , Layer 2: F11       , Layer 3: F11       , Layer 4: F11
  [[[0,0],0x45],[[0,0],0x45],[[0,0],0x45],[[0,0],0x45],[[0,0],0x45],[[0,0],0x45]], #69 0x45 - US: F12       , DE: F12       , Layer 1: F12       , Layer 2: F12       , Layer 3: F12       , Layer 4: F12
  [[[0,0],0x46],[[0,0],0x46],[[0,0],0x46],[[0,0],0x46],[[0,0],0x46],[[0,0],0x46]], #70 0x46 - US: PRINT     , DE: Drucken   , Layer 1: Drucken   , Layer 2: Drucken   , Layer 3: Drucken   , Layer 4: Drucken
  [[[0,0],0x47],[[0,0],0x47],[[0,0],0x47],[[0,0],0x47],[[0,0],0x47],[[0,0],0x47]], #71 0x47 - US: SCROLLLOCK, DE: Scrollen  , Layer 1: Scrollen  , Layer 2: Scrollen  , Layer 3: Scrollen  , Layer 4: Scrollen
  [[[0,0],0x48],[[0,0],0x48],[[0,0],0x48],[[0,0],0x48],[[0,0],0x48],[[0,0],0x48]], #72 0x48 - US: PAUSE     , DE: Pause     , Layer 1: Pause     , Layer 2: Pause     , Layer 3: Pause     , Layer 4: Pause
  [[[0,0],0x49],[[0,0],0x49],[[0,0],0x49],[[0,0],0x49],[[0,0],0x49],[[0,0],0x49]], #73 0x49 - US: INSERT    , DE: Einfügen  , Layer 1: Einfügen  , Layer 2: Einfügen  , Layer 3: Einfügen  , Layer 4: Einfügen
  [[[0,0],0x4A],[[0,0],0x4A],[[0,0],0x4A],[[0,0],0x4A],[[0,0],0x4A],[[0,0],0x4A]], #74 0x4A - US: HOME      , DE: Pos1      , Layer 1: Pos1      , Layer 2: Pos1      , Layer 3: Pos1      , Layer 4: Pos1
  [[[0,0],0x4B],[[0,0],0x4B],[[0,0],0x4B],[[0,0],0x4B],[[0,0],0x4B],[[0,0],0x4B]], #75 0x4B - US: PAGEUP    , DE: Bild hoch , Layer 1: Bild hoch , Layer 2: Bild hoch , Layer 3: Bild hoch , Layer 4: Bild hoch
  [[[0,0],0x4C],[[0,0],0x4C],[[0,0],0x4C],[[0,0],0x4C],[[0,0],0x4C],[[0,0],0x4C]], #76 0x4C - US: DELETE    , DE: Entfernen , Layer 1: Entfernen , Layer 2: Entfernen , Layer 3: Entfernen , Layer 4: Entfernen
  [[[0,0],0x4D],[[0,0],0x4D],[[0,0],0x4D],[[0,0],0x4D],[[0,0],0x4D],[[0,0],0x4D]], #77 0x4D - US: END       , DE: Ende      , Layer 1: Ende      , Layer 2: Ende      , Layer 3: Ende      , Layer 4: Ende
  [[[0,0],0x4E],[[0,0],0x4E],[[0,0],0x4E],[[0,0],0x4E],[[0,0],0x4E],[[0,0],0x4E]], #78 0x4E - US: PAGEDOWN  , DE: Bild runt., Layer 1: Bild runt., Layer 2: Bild runt., Layer 3: Bild runt., Layer 4: Bild runt.
  [[[0,0],0x4F],[[0,0],0x4F],[[0,0],0x4F],[[0,0],0x4F],[[0,0],0x4F],[[0,0],0x4F]], #79 0x4F - US: RIGHT     , DE: Rechte Pf., Layer 1: Rechte Pf., Layer 2: Rechte Pf., Layer 3: Rechte Pf., Layer 4: Rechte Pf.
  [[[0,0],0x50],[[0,0],0x50],[[0,0],0x50],[[0,0],0x50],[[0,0],0x50],[[0,0],0x50]], #80 0x50 - US: LEFT      , DE: Linke Pf. , Layer 1: Linke Pf. , Layer 2: Linke Pf. , Layer 3: Linke Pf. , Layer 4: Linke Pf.
  [[[0,0],0x51],[[0,0],0x51],[[0,0],0x51],[[0,0],0x51],[[0,0],0x51],[[0,0],0x51]], #81 0x51 - US: DOWN      , DE: Untere Pf., Layer 1: Untere Pf., Layer 2: Untere Pf., Layer 3: Untere Pf., Layer 4: Untere Pf.
  [[[0,0],0x52],[[0,0],0x52],[[0,0],0x52],[[0,0],0x52],[[0,0],0x52],[[0,0],0x52]], #82 0x52 - US: UP        , DE: Obere Pf. , Layer 1: Obere Pf. , Layer 2: Obere Pf. , Layer 3: Obere Pf. , Layer 4: Obere Pf.
  [[[0,0],0x2B],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #83 0x53 - US: NUMLOCK   , DE: Numlock   , Layer 1: Tab       , Layer 2:           , Layer 3:           , Layer 4:
  [[[1,0],0x24],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #84 0x54 - US: KPSLASH   , DE: NB Slash  , Layer 1: /         , Layer 2:           , Layer 3:           , Layer 4: 
  [[[1,0],0x30],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #85 0x55 - US: KPASTERISK, DE: NB Stern  , Layer 1: *         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x38],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #86 0x56 - US: KPMINUS   , DE: NB Minus  , Layer 1: -         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x30],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #87 0x57 - US: KPPLUS    , DE: NB Plus   , Layer 1: +         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x28],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #88 0x58 - US: KPENTER   , DE: NB Enter  , Layer 1: Enter     , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x1E],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #89 0x59 - US: KP1       , DE: NB 1      , Layer 1: 1         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x1F],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #90 0x5A - US: KP2       , DE: NB 2      , Layer 1: 2         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x20],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #91 0x5B - US: KP3       , DE: NB 3      , Layer 1: 3         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x21],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #92 0x5C - US: KP4       , DE: NB 4      , Layer 1: 4         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x22],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #93 0x5D - US: KP5       , DE: NB 5      , Layer 1: 5         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x23],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #94 0x5E - US: KP6       , DE: NB 6      , Layer 1: 6         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x24],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #95 0x5F - US: KP7       , DE: NB 7      , Layer 1: 7         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x25],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #96 0x60 - US: KP8       , DE: NB 8      , Layer 1: 8         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x26],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #97 0x61 - US: KP9       , DE: NB 9      , Layer 1: 9         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x27],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]], #98 0x62 - US: KP0       , DE: NB 0      , Layer 1: 0         , Layer 2:           , Layer 3:           , Layer 4:
  [[[0,0],0x36],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00],[[0,0],0x00]]  #99 0x63 - US: KPDOT     , DE: NB Punkt  , Layer 1: ,         , Layer 2:           , Layer 3:           , Layer 4:
]

# Map modifier keys to array element in the bit array
mod = {
   "RMOD4" : 1,
   "RMOD2" : 2,
   "LMOD2" : 6,
   "LMOD3" : 8,
   "RMOD3" : 9,
   "LMOD4" : 10
}

def convert(hex_key,mods,state_mods,lock):
    state_mods[0] = mods[0]
    state_mods[3] = mods[3]
    state_mods[4] = mods[4]
    state_mods[7] = mods[7]
    state_mods[1] = 0
    state_mods[2] = 0
    state_mods[5] = 0 #LALT
    state_mods[6] = 0 #LSHIFT
    layer = 1
    if ((((mods[mod["RMOD2"]] or mods[mod["LMOD2"]]) and not lock == 2) or 
          (lock == 2 and not (mods[mod["RMOD2"]] or mods[mod["LMOD2"]]))) and not 
        (mods[mod["RMOD3"]] or mods[mod["RMOD4"]] or mods[mod["LMOD3"]] or mods[mod["LMOD4"]])):
        layer = 2
    elif ((((mods[mod["RMOD3"]] or mods[mod["LMOD3"]]) and not lock == 3) or
            (lock == 3 and not (mods[mod["RMOD3"]] or mods[mod["LMOD3"]]))) and not
          (mods[mod["RMOD2"]] or mods[mod["RMOD4"]] or mods[mod["LMOD2"]] or mods[mod["LMOD4"]])):
        layer = 3
    elif ((((mods[mod["RMOD4"]] or mods[mod["LMOD4"]]) and not lock == 4) or
            (lock == 4 and not (mods[mod["RMOD4"]] or mods[mod["LMOD4"]]))) and not
          (mods[mod["RMOD2"]] or mods[mod["RMOD3"]] or mods[mod["LMOD2"]] or mods[mod["LMOD3"]])):
        layer = 4
    elif (((mods[mod["RMOD2"]] or mods[mod["LMOD2"]]) and (mods[mod["RMOD3"]] or mods[mod["LMOD3"]])) and not
           (mods[mod["RMOD4"]] or mods[mod["LMOD4"]])):
        layer = 5
    elif (((mods[mod["RMOD3"]] or mods[mod["LMOD3"]]) and (mods[mod["RMOD4"]] or mods[mod["LMOD4"]])) and not
           (mods[mod["RMOD2"]] or mods[mod["LMOD2"]])):
        layer = 6

    entry=converttable[hex_key][layer-1]
    state_mods[6] = entry[0][0] #Press Shift?
    state_mods[5] = entry[0][1] #Press Alt?
    return entry[1]


def locks(mods,lock):
    if (mods[mod["RMOD2"]] and mods[mod["LMOD2"]]) and not (mods[mod["RMOD3"]] or mods[mod["RMOD4"]] or mods[mod["LMOD3"]] or mods[mod["LMOD4"]]):
        if lock == 2:
            return 1
        else:
            return 2
    elif (mods[mod["RMOD3"]] and mods[mod["LMOD3"]]) and not (mods[mod["RMOD2"]] or mods[mod["RMOD4"]] or mods[mod["LMOD2"]] or mods[mod["LMOD4"]]):
        if lock == 3:
            return 1
        else:
            return 3
    elif (mods[mod["RMOD4"]] and mods[mod["LMOD4"]]) and not (mods[mod["RMOD2"]] or mods[mod["RMOD3"]] or mods[mod["LMOD2"]] or mods[mod["LMOD3"]]):
        if lock == 4:
            return 1
        else:
            return 4
    return lock
