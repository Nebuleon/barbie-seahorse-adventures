import pygame
from pygame.locals import *

from cnst import *

import tiles_basic
from tile import *

# NOTE: If you add new tiles, use t_init for regular tiles.
#       tl_init and tr_init are for tiles that take up only half of the
#       16x16 tile, on the left or right side respectively.

TILES = {
    # general purpose tiles
    0x00: [t_init, [], None, ],
    0x01: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x02: [t_init, ['solid'], tiles_basic.hit_breakable, 1, 1, 1, 1, ],
    0x03: [t_init, ['player'], tiles_basic.hit_fire, ],
    0x04: [t_init, [], None, ],  # black background tile
    0x05: [t_init, [], None, ],  # exit sign
    0x10: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x11: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x12: [t_init, ['solid'], tiles_basic.hit_fally, 1, 1, 1, 1, ],
    0x14: [t_init, ['bubble'], tiles_basic.hit_replace, 0x15, ],
    0x15: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x21: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],

    # powerups and bonus items ...
    0x08: [t_init, ['player'], tiles_basic.hit_power, ],  # power-up
    0x0C: [t_init, ['player'], tiles_basic.hit_life, ],  # extra-life
    0x18: [t_init, ['player'], tiles_basic.hit_item, 100],  # points
    0x1A: [t_init, ['player'], tiles_basic.hit_item, 250],  # points
    0x1C: [t_init, ['player'], tiles_basic.hit_item, 500],  # points
    0x1E: [t_init, ['player'], tiles_basic.hit_item, 1000],  # points
    0x28: [t_init, ['player'], tiles_basic.hit_coin, ],  # coin

    # jungle tiles (0x40...)
    0x40: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x41: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x42: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x43: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x44: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x45: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0x51	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0x52	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0x54: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x55: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0x61	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0x62	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0x64: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x65: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x70: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x71: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x72: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x73: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x74: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x75: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],

    # dirt floor set
    0x47: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x48: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x49: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x57: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x58: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x59: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x67: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x68: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x69: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x77: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x78: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x79: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],

    # dirt floor set #2
    0x4A: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x4B: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x4C: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x5A: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x5B: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x5C: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x6A: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x6B: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x6C: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x7A: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x7B: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x7C: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],

    # volcano tiles (0x80...)
    0x80: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x81: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x82: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x83: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x84: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x85: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0x91	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0x92	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0x94: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0x95: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0xa1	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0xa2	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0xa4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xa5: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb0: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb1: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb2: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb3: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xb5: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],

    # volcano cave set
    0x87: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x88: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x89: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x97: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x98: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0x99: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xA7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xA8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xA9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xB7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xB8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xB9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],

    # moon tiles (0xC0...)
    0xc0: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xc1: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xc2: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xc3: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xc4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xc5: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0xd1	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0xd2	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0xd4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xd5: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    # 0xe1	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    # 0xe2	:[t_init,['solid'],tiles_basic.hit_block,1,1,1,1,],
    0xe4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xe5: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf0: [tr_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf1: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf2: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf3: [tl_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf4: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],
    0xf5: [t_init, ['solid'], tiles_basic.hit_block, 1, 0, 0, 0, ],

    # moon cave set
    0xC7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xC8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xC9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xD7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xD8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xD9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xE7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xE8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xE9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xF7: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xF8: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
    0xF9: [t_init, ['solid'], tiles_basic.hit_block, 1, 1, 1, 1, ],
}


TANIMATE = [
    #(starting_tile,animated list of frames incs),
    (0x08, [int(v) for v in '00000000000000000000000111222333']),  # powerup
    (0x0C, [int(v) for v in '00000001112223330000000000000000']),  # extra life
    (0x18, [int(v) for v in '1100000000000000000000000000000000000000000000000000000000000000']),  # veggies
    (0x1A, [int(v) for v in '0000000000000000110000000000000000000000000000000000000000000000']),
    (0x1C, [int(v) for v in '0000000000000000000000000000000011000000000000000000000000000000']),
    (0x1E, [int(v) for v in '0000000000000000000000000000000000000000000000001100000000000000']),
    (0x28, [int(v) for v in '00001111222233334444555566667777']),  # coin
    (0x30, [int(v) for v in '1111111111111111111111111111111111111111111111111111111111111111']),  # door
]

TREPLACE = [
    #(tile_to_replace,replace_with)
    (0x10, 0x00),
    (0x11, 0x00),
    (0x14, 0x00),
    (0x20, 0x00),
]

# Immutable tiles do not animate and cannot appear or disappear during a
# level. If found in the background or the foreground, they can be drawn to a
# secondary background surface, drawn after the level's primary background,
# part of which is drawn to the screen with one blit call. This saves on blit
# calls versus having to draw tiles with one blit call each.

# Decoration tiles are immutable, and so are platforms and anything that can
# participate in collision detection, as long as they don't ever change.
TIMMUTABLE = {
    0x04: True,  # black background tile
    0x05: True,  # exit sign

    # Jungle + jungle cave platforms and backdrop.
    0x40: True,
    0x41: True,
    0x42: True,
    0x43: True,
    0x44: True,
    0x45: True,
    0x46: True,  # alternate leaf/earth texture
    0x47: True,  # cave ...
    0x48: True,
    0x49: True,
    0x4A: True,
    0x4B: True,
    0x4C: True,  # ... end
    0x50: True,
    0x51: True,
    0x52: True,
    0x53: True,
    0x54: True,
    0x55: True,
    0x57: True,  # cave ...
    0x58: True,
    0x59: True,
    0x5A: True,
    0x5B: True,
    0x5C: True,  # ... end
    0x60: True,
    0x61: True,
    0x62: True,
    0x63: True,
    0x64: True,
    0x65: True,
    0x67: True,  # cave ...
    0x68: True,
    0x69: True,
    0x6A: True,
    0x6B: True,
    0x6C: True,  # ... end
    0x70: True,
    0x71: True,
    0x72: True,
    0x73: True,
    0x74: True,
    0x75: True,
    0x77: True,  # cave ...
    0x78: True,
    0x79: True,
    0x7A: True,
    0x7B: True,
    0x7C: True,  # ... end

    # Volcano + volcano cave platforms and backdrop.
    0x80: True,
    0x81: True,
    0x82: True,
    0x83: True,
    0x84: True,
    0x85: True,
    0x87: True,  # cave ...
    0x88: True,
    0x89: True,  # ... end
    0x90: True,
    0x91: True,
    0x92: True,
    0x93: True,
    0x94: True,
    0x95: True,
    0x97: True,  # cave ...
    0x98: True,
    0x99: True,  # ... end
    0xA0: True,
    0xA1: True,
    0xA2: True,
    0xA3: True,
    0xA4: True,
    0xA5: True,
    0xA7: True,  # cave ...
    0xA8: True,
    0xA9: True,  # ... end
    0xB0: True,
    0xB1: True,
    0xB2: True,
    0xB3: True,
    0xB4: True,
    0xB5: True,
    0xB7: True,  # cave ...
    0xB8: True,
    0xB9: True,  # ... end

    # Moon + moon cave platforms and backdrop.
    0xC0: True,
    0xC1: True,
    0xC2: True,
    0xC3: True,
    0xC4: True,
    0xC5: True,
    0xC7: True,  # cave ...
    0xC8: True,
    0xC9: True,  # ... end
    0xD0: True,
    0xD1: True,
    0xD2: True,
    0xD3: True,
    0xD4: True,
    0xD5: True,
    0xD7: True,  # cave ...
    0xD8: True,
    0xD9: True,  # ... end
    0xE0: True,
    0xE1: True,
    0xE2: True,
    0xE3: True,
    0xE4: True,
    0xE5: True,
    0xE7: True,  # cave ...
    0xE8: True,
    0xE9: True,  # ... end
    0xF0: True,
    0xF1: True,
    0xF2: True,
    0xF3: True,
    0xF4: True,
    0xF5: True,
    0xF7: True,  # cave ...
    0xF8: True,
    0xF9: True,  # ... end
}

# Decoration tiles do not participate in collision detection and can be safely
# kept in the Level's layer object as None.

# Decoration tiles are immutable, but immutable tiles are not necessarily
# decoration tiles. For example, platform tiles are immutable, so they can be
# drawn onto the precomputed background and removed from the tiles to draw,
# but they are not decoration and must be kept in the Level's layer object so
# they can participate in collision detection.
TDECORATION = {
    0x04: True,  # black background tile
    0x05: True,  # exit sign

    # Jungle backdrop sides.
    0x50: True,
    0x53: True,
    0x60: True,
    0x63: True,

    # Jungle backdrop.
    0x51: True,
    0x52: True,
    0x61: True,
    0x62: True,

    0x46: True,  # jungle alternate leaf/earth texture

    # Volcano backdrop sides.
    0x90: True,
    0x93: True,
    0xA0: True,
    0xA3: True,

    # Volcano backdrop.
    0x91: True,
    0x92: True,
    0xA1: True,
    0xA2: True,

    # Moon backdrop sides.
    0xD0: True,
    0xD3: True,
    0xE0: True,
    0xE3: True,

    # Moon backdrop.
    0xD1: True,
    0xD2: True,
    0xE1: True,
    0xE2: True,
}


def t_put(g, pos, n):
    x, y = pos
    try:
        v = TILES[n]
        return v[0](g, pygame.Rect(x * TW, y * TH, TW, TH), n, *v[1:])
    except KeyError:
        # print 'undefined tile:',x,y,'0x%02x'%n
        return t_init(g, pygame.Rect(x * TW, y * TH, TW, TH), n, [], None)
