from pygame import K_w, K_a, K_s, K_d, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_f
from test_classes import ass, assD, assDR, RSimple, RSource, RBlock, RDelay, RDetect, RTwo180, RTwo90, RThree, RTick, BSimple, BDiag, BStrStr, BStrRight, BStrDiag, YNot, YAnd, YXor, YTrig1, YTrig2, ORand, OBtn1, OBtn2
from math import floor

def set_dir(e, type, dir):
    if type in ass: return None
    
    elif type in assD or type in assDR or type == 'v':
        if e.key == K_w: return (0, -1)
        if e.key == K_a: return (-1, 0)
        if e.key == K_s: return (0, 1)
        if e.key == K_d: return (1, 0)
        else: return dir

def set_ref(e, type, ref):
    if type in ass or type in assD: return None
    elif type in assDR or type == 'v':
        if e.key == K_f:
            if ref == -1 or ref == None: return 1
            else: return -1
        else: return ref

def set_tab(e, t):
    if e.key == K_1: return 'r'
    if e.key == K_2: return 'b'
    if e.key == K_3: return 'y'
    else: return t

#с отраженностью и направлением
assDR = {RTwo90, BDiag, BStrRight, BStrDiag}

def set_type_R(e, t, dir, ref):
    # type, dir, ref
    if e.key == K_1: return (RSimple, (0, -1), None)
    if e.key == K_2: return (RSource, None, None) 
    if e.key == K_3: return (RBlock,  (0, -1), None)
    if e.key == K_4: return (RDelay,  (0, -1), None)
    if e.key == K_5: return (RDetect, (0, -1), None)
    if e.key == K_6: return (RTwo180, (0, -1), None)
    if e.key == K_7: return (RTwo90,  (0, -1), 1)
    if e.key == K_8: return (RThree,  (0, -1), None)
    if e.key == K_9: return (RTick,   None, None)
    else: return (t, dir, ref)

def set_type_B(e, t, dir, ref):
    if e.key == K_1: return (BSimple,   (0, -1), None)
    if e.key == K_2: return (BDiag,     (0, -1), 1)
    if e.key == K_3: return (BStrStr,   (0, -1), None)
    if e.key == K_4: return (BStrRight, (0, -1), 1)
    if e.key == K_5: return (BStrDiag,  (0, -1), 1)
    else: return (t, dir, ref)

def set_type_Y(e, t, dir, ref):
    if e.key == K_1: return (YNot,   (0, -1), None)
    if e.key == K_2: return (YAnd,   (0, -1), None)
    if e.key == K_3: return (YXor,   (0, -1), None)
    if e.key == K_4: return (YTrig2, (0, -1), None)
    if e.key == K_5: return (YTrig1, (0, -1), None)
    if e.key == K_6: return (ORand,  (0, -1), None)
    if e.key == K_7: return (OBtn1,  None, None)
    if e.key == K_8: return (OBtn2,  (0, -1), None)
    else: return (t, dir, ref)

class Camera:
    def __init__(self):
        #мировые координаты камеры
        self.x = 0
        self.y = 0
        #предыдущие координаты камеры тоже мировые
        self.last_pos = (0,0)
        self.pos_bef_zoom = (0,0)
        

        self.zoom = 4
        self.max_zoom = 7
        self.min_zoom = 2
        self.cell_size = 16

        #экранные координаты
        self.start_move_cor = (0,0)
        #разрешает перемещение камеры
        self.moving_flag = False    
    
    def set_zoom(self):
        if self.zoom>self.max_zoom: self.zoom = self.max_zoom
        elif self.zoom<self.min_zoom: self.zoom = self.min_zoom

    def wrld_to_scr(self, w_cor):
        '''зачем? чтобы передать в метод draw у стрелочки.
        что делает? 1)получает мировые координаты, 2) вычетает из них позицию камеры, 3)умножает разность на cs
        вернет кортеж'''
        wx, wy = w_cor
        return ( (wx - self.x)*self.cell_size, (wy - self.y)*self.cell_size )
    
    def scr_to_wrld(self, s_cor):
        '''зачем? чтобы ставить стрелочку кликом.
        возможно чтобы отрисовывать прозрачную стрелочку под курсором (преобразовать позицию курсора в мировую, округлить и преобразовать обратно)
        что делает? получает экранные, делит на cs, прибавляет позицию камеры, округляет в меньшую сторону до целого
        вернет кортеж'''
        sx, sy = s_cor
        sx, sy = sx/self.cell_size + self.x, sy/self.cell_size + self.y

        return (floor(sx), floor(sy))
    
    def save_pos(self):
        self.last_pos = (self.x, self.y)