import pygame as pg
from random import getrandbits as randb

RSimple   = 1
RSource   = 2
RBlock    = 4
RDelay    = 3
RDetect   = 5
RTwo180   = 6
RTwo90    = 7
RThree    = 8
RTick     = 9
BSimple   = 10
BDiag     = 11
BStrStr   = 12
BStrRight = 13
BStrDiag  = 14
YNot      = 15
YAnd      = 16
YXor      = 17
YTrig1    = 18
YTrig2    = 19
ORand     = 20
OBtn1     = 21
OBtn2     = 22

def transform_field(cf, dir, ref):
    result = {}
    for cor, a in cf.items():
        arrow = fabric_arrows(a.type, a.direction, a.reflection)

        if arrow.direction is not None and ref==-1:
            if DefaultArrow.vectodeg[arrow.direction] == 90:
                arrow.direction = DefaultArrow.degtovec[270]

            elif DefaultArrow.vectodeg[arrow.direction] == 270:
                arrow.direction = DefaultArrow.degtovec[90]


        if arrow.reflection is not None:  arrow.reflection*=ref
        cor = (cor[0]*ref, cor[1])

        if   dir == (0, -1): result[cor] = arrow
        elif dir == (0, 1):
            cor = (-cor[0], -cor[1])
            if arrow.direction is not None: arrow.direction = DefaultArrow.degtovec[(DefaultArrow.vectodeg[dir] + DefaultArrow.vectodeg[arrow.direction])%360]
            result[cor] = arrow

        elif dir == (1, 0):
            cor = (-cor[1], cor[0])
            if arrow.direction is not None: arrow.direction = DefaultArrow.degtovec[(DefaultArrow.vectodeg[dir] + DefaultArrow.vectodeg[arrow.direction])%360]
            result[cor] = arrow 
        elif dir == (-1, 0):
            cor = (cor[1], -cor[0])
            if arrow.direction is not None: arrow.direction = DefaultArrow.degtovec[(DefaultArrow.vectodeg[dir] + DefaultArrow.vectodeg[arrow.direction])%360]
            result[cor] = arrow
    return result

def fcopy(set, f):
    cf = {}
    mx = min(pos[0] for pos in set)
    my = min(pos[1] for pos in set)
    for pos in set:
        cf[(pos[0]-mx, pos[1]-my)] = fabric_arrows(f[pos].type, f[pos].direction, f[pos].reflection)
    return cf

def fabric_arrows(type, dir, ref):
    if type   == RSimple  :return RedSimple(dir)
    elif type == RBlock   :return RedBlock(dir)
    elif type == RDelay   :return RedDelay(dir)
    elif type == RDetect  :return RedDetect(dir)
    elif type == RTwo180  :return RedTwo180(dir)
    elif type == RTwo90   :return RedTwo90(dir, ref)
    elif type == RThree   :return RedThree(dir)
    elif type == BSimple  :return BlueSimple(dir)
    elif type == BDiag    :return BlueDiag(dir, ref)
    elif type == BStrStr  :return BlueStrStr(dir)
    elif type == BStrRight:return BlueStrRight(dir, ref)
    elif type == BStrDiag :return BlueStrDiag(dir, ref)
    elif type == YNot     :return YellowNot(dir)
    elif type == YAnd     :return YellowAnd(dir)
    elif type == YXor     :return YellowXor(dir)
    elif type == YTrig1   :return YellowTrig1(dir)
    elif type == YTrig2   :return YellowTrig2(dir)
    elif type == ORand    :return OrangeRand(dir)
    elif type == OBtn2    :return OrangeBtn2(dir)
    elif type == RSource  :return RedSource()
    elif type == RTick    :return RedTick()
    elif type == OBtn1    :return OrangeBtn1()

#создаем табличку с доступными стрелочками
def sttable(ttype, assets, assets_cor):
    '''возращает поверхность с таблом стрелочек. хуй их знает'''
    surf = pg.Surface((9*64+6, 70))
    surf.fill((75, 0, 130))
    pg.draw.rect(surf, (250, 250, 250), (3, 3, 64*9, 64))
    if ttype == 'r':
        for i in range(1,10):
            surf.blit(pg.transform.scale(assets[i],   (64,64)), assets_cor[i])
    elif ttype == 'b':
        for i in range(10,15):
            surf.blit(pg.transform.scale(assets[i],   (64,64)), assets_cor[i])
    elif ttype == 'y':
        for i in range(15,23):
            surf.blit(pg.transform.scale(assets[i],   (64,64)), assets_cor[i])
    return surf

def get_sprite(sheet, cor):
    """Вырезает область из спрайт-листа"""
    # Создаём поверхность для спрайта
    sprite = pg.Surface((cor[2], cor[3]), pg.SRCALPHA)
    # Копируем указанную область
    sprite.blit(sheet, (0, 0), cor)
    return sprite

#без направления и отраженности
ass = {RSource, RTick, OBtn1}
#с направлением без отраженности
assD = {RSimple, RBlock, RDetect, RDelay, RTwo180, RThree, BSimple, BStrStr, YNot, YAnd, YXor, YTrig1, YTrig2, ORand, OBtn2}
#с отраженностью и направлением
assDR = {RTwo90, BDiag, BStrRight, BStrDiag}

class DefaultArrow:
    #словарь со всеми возможными поворотами и отражениями ассетов
    assets_cash = {}
    assets_alfa_cash = {}
    #направления ко всем соседям
    all_nei = ((0,-2), (0, -1), (0, 1), (0, 2),
              (-2, 0), (-1, 0), (1, 0), (2, 0),
              (-1, -1), (1, 1), (-1, 1), (1, -1)) #можно оптимизировать
    #только к близким
    near_nei = ((1,0), (-1,0), (0, 1), (0,-1))
    #преобразовать вектор в градусы
    vectodeg = {(0, -1): 0, (0, 1): 180, (1, 0): 270, (-1, 0): 90}
    degtovec = { 0:(0, -1), 180:(0, 1), 270:(1, 0), 90:(-1, 0)}

    @classmethod
    def init_asset_cash(cls, assets, size_cell):
        '''Инициализация кэша (вызывается один раз)
        словарь с ассетами assets должен иметь тип из text_classes в качестве ключа и сам ассет в качестве значения'''

        #DefaultArrow.assets_cash[(   self.type,    self.direction,    self.reflection   )]
        for type, sp in assets.items():
            sprite = pg.transform.scale(sp, (size_cell, size_cell))
            alfa_sprite = pg.transform.scale(sp, (size_cell, size_cell))
            alfa_sprite.set_alpha(128)
            if type in ass: 
                cls.assets_cash[(type, None, None)] = sprite
                cls.assets_alfa_cash[(type, None, None)] = alfa_sprite
                continue
            for d in ((0, -1), (0, 1), (1, 0), (-1, 0)):
                angle = cls.vectodeg[d]
                if type in assD:
                    cls.assets_cash[(type, d, None)] = pg.transform.rotate(sprite, angle)
                    cls.assets_alfa_cash[(type, d, None)] = pg.transform.rotate(alfa_sprite, angle)
                    continue
                for r in (1, -1):
                    cls.assets_cash[(type, d, r)] = pg.transform.rotate(pg.transform.flip(sprite, r==-1, False), angle)
                    cls.assets_alfa_cash[(type, d, r)] = pg.transform.rotate(pg.transform.flip(alfa_sprite, r==-1, False), angle)

    def __init__(self, dir = None, ref = None):
        self.type = None
        self.color = None
        self.direction = dir
        self.reflection = ref

        self.active = False
        self.next_active = False

    def get_ass(self, alfa):
        if alfa: return DefaultArrow.assets_alfa_cash[(self.type, self.direction, self.reflection)]
        return DefaultArrow.assets_cash[(self.type, self.direction, self.reflection)]
    #должны получать экранные координаты
    def draw(self, surface, size_cell, x, y, w, h, alfa = False):
        '''метод использует словарь со всеми возможными поворотами и отражениями ассетов, в качестве ключа кортеж с типом, направлением и отраженностью
        определен для всех классов, кроме задержки и единичного импульса'''
        if (x+size_cell < 0 or y+size_cell < 0 or x>w or y > h): return
        if self.active: pg.draw.rect(surface, self.color, (x, y, size_cell, size_cell))
        surface.blit(self.get_ass(alfa), (x, y))
    
    def next_tact(self):
        '''должен быть переопределен у только задержки'''
        self.active = self.next_active
    
    def actsum(self, x, y, field):
        '''перебираем активных соседей, у каждого вызываем is_fasing, проверяем на блок(вернет 0), возращаем сумму входящих сигналов и передаем в метод update
        определен для всех классов'''
        sum = 0
        for dx, dy in DefaultArrow.all_nei:
            #получаем координаты соседа
            nx, ny = x + dx, y + dy
            #и самого соседа
            arw = field.get((nx, ny))
            #проверяем наличие соседа и его аткивность
            if arw is None or not arw.active: continue
            #проверяем блок
            if arw.is_facing(x, y, nx, ny) == 2:
                return -1
            #проверяем направление
            if arw.is_facing(x, y, nx, ny): sum+=1
        return sum

    def update(self):
        '''условие активации. может быть определен для большинства'''
        pass

    def is_facing(self):
        '''направленна ли стрелка на цель?
        определить свой для каждого класса'''
        pass

#_________ОБЫЧНАЯ_____________________________________________________________________
class RedSimple(DefaultArrow):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RSimple
        self.color = (255,0,0)
        self.direction = dir

    def update(self, x, y, field):
        '''активируем, если количество входящих сигналов минимум 1
        определен для большинства
        НЕ подойдет для: источник, источник импульса, детектор, все желтые и оранжевые'''
        self.next_active = self.actsum(x, y, field)>=1
    
    def is_facing(self, tx, ty, x, y):
        '''сравниваем направление к цели с собственным
        подойдет для: обычной, задержки, детектора, всех желтых, рандома и проводящей кнопки'''
        return (tx-x, ty-y) == self.direction

#_________Желтые_____________________________________________________________________
class YellowNot(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = YNot
        self.color = (255, 255, 0)
    def update(self, x, y, field):
        self.next_active = self.actsum(x, y, field) == 0

class YellowAnd(YellowNot):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = YAnd
    def update(self, x, y, field):
        self.next_active = self.actsum(x, y, field) >= 2

class YellowXor(YellowNot):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = YXor
    def update(self, x, y, field):
        sum = self.actsum(x, y, field)
        self.next_active = sum!=-1 and sum%2 == 1

class YellowTrig1(YellowNot):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = YTrig1
    def update(self, x, y, field):
        sum = self.actsum(x, y, field)
        self.next_active = self.active and sum == 0 or not self.active and sum >= 1

class YellowTrig2(YellowNot):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = YTrig2
    def update(self, x, y, field):
        sum = self.actsum(x, y, field)
        self.next_active = self.active and (sum == 0 or sum >= 2) or not self.active and sum >= 2

#_________Синие_____________________________________________________________________
class BlueSimple(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = BSimple
        self.color = (0, 0, 255)
    def is_facing(self, tx, ty, x, y):
        return ((tx-x)/2, (ty-y)/2) == self.direction

class BlueStrStr(BlueSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = BStrStr
    def is_facing(self, tx, ty, x, y):
        return super().is_facing(tx, ty, x, y) or (tx-x, ty-y) == self.direction

class BlueDiag(BlueSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = BDiag
        self.reflection = ref   
    def is_facing(self, tx, ty, x, y):
        return (tx-x, ty-y) == (self.direction[0] - self.reflection*self.direction[1],  self.direction[1] + self.reflection*self.direction[0])

class BlueStrDiag(BlueDiag):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = BStrDiag
    def is_facing(self, tx, ty, x, y):
        return super().is_facing(tx, ty, x, y) or (tx-x, ty-y) == self.direction

class BlueStrRight(BlueDiag):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = BStrRight
    def is_facing(self, tx, ty, x, y):
        dx, dy = tx-x, ty-y
        return (dx/2, dy/2) == self.direction or (dy*self.reflection, -dx*self.reflection) == self.direction

class RedBlock(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RBlock
    def is_facing(self, tx, ty, x, y):
        if super().is_facing(tx, ty, x, y): return 2

class RedTwo180(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RTwo180
    def is_facing(self, tx, ty, x, y):
        return (tx-x, ty-y) == self.direction or (-(tx-x), -(ty-y)) == self.direction

class RedThree(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RThree
    def is_facing(self, tx, ty, x, y):
        dx, dy = tx-x, ty-y
        return (dx, dy) == self.direction or (-dy, dx) == self.direction or (dy, -dx) == self.direction

class RedTwo90(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RTwo90
        self.reflection = ref
    def is_facing(self, tx, ty, x, y):
        dx, dy = tx-x, ty-y
        return (dx, dy) == self.direction or (dy * self.reflection, -dx * self.reflection) == self.direction

class OrangeRand(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.color = (255, 128, 0)
        self.type = ORand
    def update(self, x, y, field):
        self.next_active = self.actsum(x, y, field)>=1 and bool(randb(1))

class RedDetect(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RDetect
    def update(self, x, y, field):
        if field.get((x-self.direction[0], y-self.direction[1])) is None: flag = False
        else: flag = field.get((x-self.direction[0], y-self.direction[1])).active
        self.next_active = self.actsum(x, y, field)!=-1 and flag

class RedSource(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RSource
        self.direction = None
        self.next_active = True
    def update(self, x, y, field):
        self.next_active = self.actsum(x, y, field)>=0
    def is_facing(self, tx, ty, x, y):
        dx,dy = tx-x, ty-y
        return (abs(dx) == 1 and dy == 0) or (abs(dy) == 1 and dx == 0)

class RedTick(RedSource):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RTick
        self.closed = False

    def update(self, x, y, field):
        self.next_active = not self.closed
        self.closed = self.actsum(x, y, field)>=0

    def draw(self, surface, size_cell, x, y, w, h, alfa = False):
        if (x+size_cell < 0 or y+size_cell < 0 or x>w or y > h): return
        if self.active: pg.draw.rect(surface, self.color, (x, y, size_cell, size_cell))
        elif self.closed: pg.draw.rect(surface, (0, 0, 255), (x, y, size_cell, size_cell))
        surface.blit(self.get_ass(alfa), (x, y))       

class RedDelay(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = RDelay
        self.state = False

    def update(self, x, y, field):
        k = self.actsum(x, y, field)
        if self.active:
            self.next_active = k>=1
            self.state = False
        else:
            self.next_active = self.state and k>=0
            self.state = k>=1
    
    def draw(self, surface, size_cell, x, y, w, h, alfa = False):
        if (x+size_cell < 0 or y+size_cell < 0 or x>w or y > h): return
        if self.active: pg.draw.rect(surface, (255, 0, 0), (x, y, size_cell, size_cell))
        elif self.state and not self.active: pg.draw.rect(surface, (0, 0, 255), (x, y, size_cell, size_cell))
        surface.blit(self.get_ass(alfa), (x, y)) 

class OrangeBtn1(RedSource):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = OBtn1
        self.color = (255, 128, 0)
        self.next_active = False
    def update(self, x, y, field):
        pass
    def click(self):
        self.active = not self.active

class OrangeBtn2(RedSimple):
    def __init__(self, dir=None, ref=None):
        super().__init__(dir, ref)
        self.type = OBtn2
        self.color = (255, 128, 0)
    def click(self):
        self.active = not self.active