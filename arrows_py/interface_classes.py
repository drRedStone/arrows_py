import pygame as pg


keys ={
    pg.K_q            :"й",
    pg.K_w            :"ц",
    pg.K_e            :"у",
    pg.K_r            :"к",
    pg.K_t            :"е",
    pg.K_y            :"н",
    pg.K_u            :"г",
    pg.K_i            :"ш",
    pg.K_o            :"щ",
    pg.K_p            :"з",
    pg.K_LEFTBRACKET  :"х",
    pg.K_RIGHTBRACKET :"ъ",
    pg.K_a            :"ф",
    pg.K_s            :"ы",
    pg.K_d            :"в",
    pg.K_f            :"а",
    pg.K_g            :"п",
    pg.K_h            :"р",
    pg.K_j            :"о",
    pg.K_k            :"л",
    pg.K_l            :"д",
    pg.K_SEMICOLON    :"ж",
    pg.K_QUOTE        :"э",
    pg.K_z            :"я",
    pg.K_x            :"ч",
    pg.K_c            :"с",
    pg.K_v            :"м",
    pg.K_b            :"и",
    pg.K_n            :"т",
    pg.K_m            :"ь",
    pg.K_COMMA        :"б",
    pg.K_PERIOD       :"ю",
    pg.K_1            :"1",
    pg.K_2            :"2",
    pg.K_3            :"3",
    pg.K_4            :"4",
    pg.K_5            :"5",
    pg.K_6            :"6",
    pg.K_7            :"7",
    pg.K_8            :"8",
    pg.K_9            :"9",
    pg.K_0            :"0",
    pg.K_SPACE        :" "
}

class new_map:
    def __init__(self):
        self.text = 'хачу нёвий'

    #должен получить экранные координаты
    def draw(self, screen, y, h):
        if (y+element.height < 0 or y>h): return
        surf = pg.Surface((500, 50))

        font = pg.font.SysFont(None, 45)
        txt = font.render(self.text, False, (255, 255, 255))

        pg.draw.rect(surf, (100, 100, 100), (5, 5, 140, 40))
        surf.blit(txt,(155, 12))

        screen.blit(surf, (0, y))       

class element:
    height = 50

    def __init__(self, text):

        self.rename_color = (255, 255, 0)
        self.text = text

    #должен получить экранные координаты
    def draw(self, screen, y, h):
        if (y+element.height < 0 or y>h): return
        surf = pg.Surface((500, 50))

        font = pg.font.SysFont(None, 45)
        txt = font.render(self.text, False, (255, 255, 255))
        #здесь могли бы быть ваши ассеты
        pg.draw.rect(surf, (0, 255, 0), (5, 5, 40, 40))
        pg.draw.rect(surf, (255, 0, 0), (55, 5, 40, 40))
        pg.draw.rect(surf, self.rename_color, (105, 5, 40, 40))
        surf.blit(txt,(155, 12))

        screen.blit(surf, (0, y))