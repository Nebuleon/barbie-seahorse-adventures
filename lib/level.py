# this file is licensed under the LGPL

import os

import pygame
from pygame.locals import *

from cnst import *
from rendercache import RenderCache

import data

import tiles
import codes
import menu
import levels


def load_level(fname):
    img = pygame.image.load(fname)
    w, h = img.get_width(), img.get_height()
    fg, bg, codes = [[[0] * w for y in xrange(h)] for _ in xrange(3)]
    rw, rh = xrange(w), xrange(h)
    for y in rh:
        for x in rw:
            fg[y][x], bg[y][x], codes[y][x], _ = img.get_at((x, y))
    return fg, bg, codes


def load_tiles(fname):
    img = pygame.image.load(fname).convert_alpha()
    w, h = img.get_width() / TW, img.get_height() / TH
    return [img.subsurface((n % w) * TW, (n / w) * TH, TW, TH) for n in xrange(w * h)]


def load_images(dname):
    r = {}
    for root, dirs, files in os.walk(dname):
        relative_root = root[len(dname):]
        if relative_root.find('.svn') != -1:
            continue
        relative_root = relative_root.replace('\\', '/')
        if relative_root != '' and not relative_root.endswith('/'):
            relative_root += '/'
        if relative_root.startswith('/'):
            relative_root = relative_root[1:]
        # print relative_root
        for a in files:
            parts = a.split('.')
            if parts[0] == '' or len(parts) != 2:
                continue
            # print 'loading image',a

            key = relative_root + parts[0]
            img = pygame.image.load(os.path.join(root, a)).convert_alpha()
            r[key] = img

            if 'left' in key:
                key = key.replace('left', 'right')
                # print 'creating flipped image',key
                img = pygame.transform.flip(img, 1, 0)
                r[key] = img
            elif 'right' in key:
                key = key.replace('right', 'left')
                # print 'creating flipped image',key
                img = pygame.transform.flip(img, 1, 0)
                r[key] = img

    return r


class Tile:

    def __init__(self, n, pos):
        self.image = n
        pass


def pre_load():
    Level._tiles = load_tiles(data.filepath('tiles.tga'))
    Level._images = load_images(data.filepath('images'))


class Level:

    def __init__(self, game, fname, parent):
        self.game = game
        self.fname = fname
        self.parent = parent
        self.font = RenderCache(self.game.fonts['level'])

    def init(self):
        self._tiles = Level._tiles
        fname = self.fname
        if fname is None:
            fname, self.title = levels.LEVELS[self.game.lcur]
            fname = data.filepath(os.path.join('levels', fname))
        else:
            self.title = os.path.basename(self.fname)
        fg, bg, codes_data = load_level(fname)

        self.images = Level._images
        self.images[None] = pygame.Surface((1, 1), pygame.SRCALPHA)

        import tiles
        self.tile_animation = []
        for m in xrange(IROTATE):
            r = list(self._tiles)
            for n, incs in tiles.TANIMATE:
                n2 = n + incs[m % len(incs)]
                r[n] = self._tiles[n2]
            for n1, n2 in tiles.TREPLACE:
                r[n1] = self._tiles[n2]
            self.tile_animation.append(r)

        self.size = len(bg[0]), len(bg)

        self._bkgr_fname = None
        self.set_bkgr('1.png')
        self.bkgr_scroll = pygame.Rect(0, 0, 1, 1)

        self.view = pygame.Rect(0, 0, SW, SH)
        self.bounds = pygame.Rect(0, 0, self.size[0] * TW, self.size[1] * TH)

        self.sprites = []
        self.player = None
        self.frame = 0
        self.codes = {}
        self.codes_data = codes_data

        # initialize all the tiles ...
        self.layer = [[None] * self.size[0] for y in xrange(self.size[1])]
        self.drawfg = [[0] * self.size[0] for y in xrange(self.size[1])]

        # Create a surface containing solely the immutable background.
        # Part of this surface is drawn onto the screen using one blit call,
        # followed by the mutable tiles, drawn using one blit call per tile.
        # See tiles.TIMMUTABLE for the full definition of 'immutable'.
        self.bg2 = pygame.Surface((self.size[0] * TW, self.size[1] * TH), pygame.SRCALPHA)
        rw, rh = xrange(self.size[0]), xrange(self.size[1])
        for y in rh:
            fg_row, bg_row, codes_row = fg[y], bg[y], codes_data[y]
            for x in rw:
                fg_tile, bg_tile, codes_tile = fg_row[x], bg_row[x], codes_row[x]
                if bg_tile != 0:
                    self.bg2.blit(self._tiles[bg_tile], (x * TW, y * TH))
                if fg_tile != 0:
                    tiles.t_put(self, (x, y), fg_tile)
                    if fg_tile in tiles.TIMMUTABLE:
                        self.bg2.blit(self._tiles[fg_tile], (x * TW, y * TH))
                        self.drawfg[y][x] = 0
                if codes_tile != 0:
                    codes.c_init(self, (x, y), codes_tile)

        # just do a loop, just to get things all shined up ..
        self.status = None
        self.loop()
        self.status = '_first'
        self.player.image = None
        self.player.exploded = 30

    def set_bkgr(self, fname):
        if self._bkgr_fname == fname:
            return
        self._bkgr_fname = fname
        self.bkgr = pygame.image.load(data.filepath(os.path.join('bkgr', fname))).convert()

    def run_codes(self, r):
        rw = xrange(max(r.left / TW, 0), min(r.right / TW, self.size[0]))
        rh = xrange(max(r.top / TH, 0), min(r.bottom / TH, self.size[1]))
        for y in rh:
            row = self.codes_data[y]
            for x in rw:
                coords = (x, y)
                if coords not in self.codes:
                    n = row[x]
                    if n != 0:
                        s = codes.c_run(self, coords, n)
                        if s is not None:
                            s._code = coords
                            self.codes[coords] = s

    def get_border(self, dist):
        r = pygame.Rect(self.view)
        r.x -= dist
        r.y -= dist
        r.w += dist * 2
        r.h += dist * 2
        return r

    def paint(self, screen):
        self.view.clamp_ip(self.bounds)

        # TODO: optimize sometime, maybe ...
        # screen.fill((0,0,0))

        v = self.view
        dh = (screen.get_height() - v.h) / 2
        if dh:
            screen.fill((0, 0, 0), (0, 0, SW, dh))
            screen.fill((0, 0, 0), (0, SH - dh, SW, dh))
        dw = (screen.get_width() - v.w) / 2
        if dw:
            screen.fill((0, 0, 0), (0, 0, dw, SH))
            screen.fill((0, 0, 0), (SW - dw, 0, dw, SH))
        _screen = screen
        screen = screen.subsurface(dw, dh, v.w, v.h)

        bg = self.bkgr
        r = pygame.Rect(0, 0, bg.get_width(), bg.get_height())
        if r.w > self.bounds.w:
            d = r.w - self.bounds.w
            r.x = d / 2
            r.w -= d
        if r.h > self.bounds.h:
            d = r.h - self.bounds.h
            r.y = d / 2
            r.h -= d
        # that picked out the center of the surface ...
        # DrPetter likes the top ...
        r.y = 0

        bg = bg.subsurface(r)

        vw = bg.get_width() - self.view.w
        bw = max(1, self.bounds.w - self.view.w)
        x = vw * (self.view.x - self.bounds.x) / bw

        vw = bg.get_height() - self.view.h
        bw = max(1, self.bounds.h - self.view.h)
        y = vw * (self.view.y - self.bounds.y) / bw

        dx, dy = -x, -y

        if self.bkgr_scroll.y == 0:

            screen.blit(bg, (dx, dy))
        else:

            # dx += self.bkgr_scroll.x*self.frame
            dy += self.bkgr_scroll.y * self.frame
            # dx = dx % bg.get_width()
            dy = dy % bg.get_height()

            screen.blit(bg, (dx, dy))
            screen.blit(bg, (dx, dy - bg.get_height()))

        v = self.view

        screen.blit(self.bg2, (0, 0), v)

        tiles = self.tile_animation[self.frame % IROTATE]
        rw = xrange(v.left - v.left % TW, v.right, TW)
        rh = xrange(v.top - v.top % TH, v.bottom, TH)
        for y in rh:
            row = self.drawfg[y / TH]
            for x in rw:
                s = row[x / TW]
                if s != 0:
                    screen.blit(tiles[s], (x - v.left, y - v.top))

        for s in self.sprites:
            try:
                img = tiles[s.image]
            except:
                img = self.images[s.image]
            if s.exploded == 0:
                screen.blit(img, (s.rect.x - s.shape.x - v.x, s.rect.y - s.shape.y - v.y))
            else:
                w = img.get_width()
                top = s.rect.y - s.shape.y - v.y - img.get_height() / 2 * s.exploded
                for ty in xrange(img.get_height()):
                    screen.blit(img, (s.rect.x - s.shape.x - v.x, top + ty * (1 + s.exploded)), (0, ty, w, 1))

        screen = _screen
        self.paint_text(screen)

        self.font.end_frame()
        self.game.flip()

    def update(self, screen):
        return self.paint(screen)

    def loop(self):
        # record the high scores
        self.game.high = max(self.game.high, self.game.score)

        if self.status != '_first':
            # start up some new sprites ...
            r = self.get_border(INIT_BORDER)
            self.run_codes(pygame.Rect(r.x, r.y, r.w, TH))  # top
            self.run_codes(pygame.Rect(r.right - TW, r.y, TW, r.h))  # right
            self.run_codes(pygame.Rect(r.x, r.bottom - TH, r.w, TH))  # bottom
            self.run_codes(pygame.Rect(r.x, r.y, TW, r.h))  # left

            # grab the current existing sprites
            # doing this avoids a few odd situations
            sprites = self.sprites[:]

            # mark off the previous rect
            for s in sprites:
                s.prev = pygame.Rect(s.rect)

            # let the sprites do their thing
            for s in sprites:
                if s.loop is not None:
                    s.loop(self, s)

            # re-calculate the groupings
            groups = {}
            for s in sprites:
                for g in s.groups:
                    if g not in groups:
                        groups[g] = []
                    groups[g].append(s)

            # hit them sprites! w-tsh!
            for s1 in sprites:
                for g in s1.hit_groups:
                    if g in groups:
                        for s2 in groups[g]:
                            if s1.rect.colliderect(s2.rect):
                                s1.hit(self, s1, s2)

            # hit walls and junk like that
            for s in sprites:
                if len(s.groups):
                    r = s.rect
                    hits = []
                    rw = xrange(max(r.left - r.left % TW, 0), min(r.right, self.size[0] * TW), TW)
                    rh = xrange(max(r.top - r.top % TH, 0), min(r.bottom, self.size[1] * TH), TH)
                    for y in rh:
                        row = self.layer[y / TH]
                        for x in rw:
                            t = row[x / TW]
                            if t is not None and t.hit_groups.intersection(s.groups):
                                dist = abs(t.rect.centerx - s.rect.centerx) + abs(t.rect.centery - s.rect.centery)
                                hits.append([dist, t])

                    hits.sort()
                    for dist, t in hits:
                        if t.rect.colliderect(s.rect):
                            t.hit(self, t, s)

            # remove inactive sprites
            border = self.get_border(DEINIT_BORDER)
            for s in sprites:
                if s.auto_gc and not border.colliderect(s.rect):
                    s.active = False
                if not s.active:
                    self.sprites.remove(s)  # this removes 'em from the real list!
                    if hasattr(s, 'deinit'):
                        s.deinit(self, s)
                    if hasattr(s, '_code'):
                        if s._code not in self.codes:
                            print 'error in code GC', s._code
                            continue
                        del self.codes[s._code]

            # pan the screen
            if self.player is not None:
                self.player.pan(self, self.player)

        # more frames
        self.frame += 1
        if (self.frame % FPS) == 0:
            pass
            # print self.player.rect.bottom
            # print ''
            # print 'frame:',self.frame
            # print 'sprites:',len(self.sprites)
            # print 'codes:',len(self.codes)

        # handle various game status'
        if self.status == '_first':
            if self.player.exploded:
                self.player.loop(self, self.player)
            else:
                self.status = 'first'
        elif self.status == 'first':
            self.status = None
            return menu.Pause(self.game, 'get ready', self)
        elif self.status == 'exit':
            self.game.lcur = (self.game.lcur + 1) % len(levels.LEVELS)
            if self.game.lcur == 0:
                # you really won!!!
                self.game.music_play('finish')
                next = menu.Transition(self.game, self.parent)
                return menu.Pause(self.game, 'CONGRATULATIONS!', next)

            else:
                self.game.music_play('lvlwin', 1)
                l2 = Level(self.game, self.fname, self.parent)
                next = menu.Transition(self.game, l2)
                return menu.Pause(self.game, 'good job!', next)

        elif self.status == 'dead':
            if self.game.lives:
                self.game.lives -= 1
                return menu.Transition(self.game, Level(self.game, self.fname, self.parent))
            else:
                next = menu.Transition(self.game, self.parent)
                return menu.Pause(self.game, 'game over', next)
        elif self.status == 'transition':
            self.status = None
            return menu.Transition(self.game, self)

    def event(self, e):
        # if e.type is KEYDOWN and e.key in (K_ESCAPE,):
        if e.type is USEREVENT and e.action == 'exit':
            next = menu.Transition(self.game, self.parent)
            return menu.Prompt(self.game, 'paused (' + EXIT_HELP + ')', next, self)
        elif self.player is not None:
            self.player.event(self, self.player, e)

    def paint_text(self, screen):
        fnt = self.font
        pad = 4

        top_y = pad

        blit = screen.blit
        text = '%05d' % self.game.score
        c = (0, 0, 0)
        img = fnt.render(text, 1, c)
        x, y = 0 + pad, top_y
        # blit(img,(x-1,y)); blit(img,(x+1,y)) ; blit(img,(x,y-1)); blit(img,(x-1,y+1))
        blit(img, (x + 1, y + 1))
        c = (255, 255, 255)
        img = fnt.render(text, 1, c)
        blit(img, (x, y))

        # text = 'LIVES: %d'%self.game.lives
        for i in xrange(self.game.lives):
            img = self._tiles[0x0C]  # the extra life tile
            x, y = SW - 1.05 * img.get_width() * i - img.get_width() - pad, pad
            blit(img, (x, y))
        # text = '%d . %02d'%(self.game.lives,self.game.coins)
        # c = (0,0,0)
        # img = fnt.render(text,1,c)
        # x,y = SW-img.get_width()-pad,0
        # blit(img,(x-1,y)); blit(img,(x+1,y)) ; blit(img,(x,y-1)); blit(img,(x-1,y+1))
        # blit(img,(x+1,y+1))
        # c = (255,255,255)
        # img = fnt.render(text,1,c)
        # blit(img,(x,y)) ; blit(img,(x,y))

        text = '%02d' % self.game.coins
        c = (0, 0, 0)
        img = fnt.render(text, 1, c)
        x, y = SW - img.get_width() - pad, TH + pad + top_y
        blit(img, (x + 1, y + 1))
        c = (255, 255, 255)
        img = fnt.render(text, 1, c)
        blit(img, (x, y))

        textheight = img.get_height()

        img = self._tiles[0x28]  # The coin
        x, y = x - img.get_width() - pad, y - img.get_height() / 2 + textheight / 2
        blit(img, (x, y))

        text = self.title
        c = (0, 0, 0)
        img = fnt.render(text, 1, c)
        x, y = (SW - img.get_width()) / 2, top_y
        # blit(img,(x-1,y)); blit(img,(x+1,y)) ; blit(img,(x,y-1)); blit(img,(x-1,y+1))
        blit(img, (x + 1, y + 1))
        c = (255, 255, 255)
        img = fnt.render(text, 1, c)
        blit(img, (x, y))
