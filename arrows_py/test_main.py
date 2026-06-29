import pygame as pg
import os
# отключим масштабирование
import ctypes; ctypes.windll.user32.SetProcessDPIAware()
import pickle

import assets_conf as acon
import test_classes as ac
import funcs as f
import time
from math import floor

import interface_classes as ic

from SET import pp, width, height

#_______________________________________________
def scr_wrld(cam_pos, y):
    '''вернет неокругленную мировую координату у'''
    return cam_pos + y/50
    
def wrld_scr(cam_pos, y):
    return (y - cam_pos)*50

def update_map_list(path):
    list_names = os.listdir(path)
    maps = {}

    maps[0] = ic.new_map()
    c = 1
    for i in list_names:
        
        maps[c] = ic.element(i)
        c+=1
    
    return maps

def create_map(path):
    c = 0
    names = os.listdir(path)
    name = ''
    while True:
        if not f'Карта {c}' in names:
            name = f'Карта {c}'
            break
        c+=1
    with open(path+'/'+name, 'w'):
        return name

def save_map(field, path, name):
    list_of_dicks = []
    for cor, arrow in field.items():
        list_of_dicks.append((cor, arrow.type, arrow.direction, arrow.reflection))
    with open(path+'/'+name, 'wb') as file:
        pickle.dump(list_of_dicks, file)

def load_map(path, name):
    field = {}
    with open(path+'/'+name, 'rb') as file:
        list_of_cocks = pickle.load(file)
    for cor, type, dir, ref in list_of_cocks:
        field[cor] = ac.fabric_arrows(type, dir, ref)
    return field
    

path = pp + R'arrows_py/saves'
maps = update_map_list(path)
wrld_main_cam_y = 0
map_name = ''
entr_flg = False
where_input = 0
#_______________________________________________

w,h = width, height
theme = (0,0,0)

field = {}
copy_field = {}
copy_field_transform = {}

delay = 0.4

delay_min = 0
delay_max = 1

#флаги для циклов
npause   = False
run      = True
Rflag    = False
PainFlag = False
TABflag = False

selecting = False
multislct = False

main_menu = True

#параметры для выделения
slct_start_cor = (0,0)
slct_end_cor = (0,0)
slct_set = set()


#параметры для установки стрелочки
dir  = None
ref = None
type = 0
tabtype = 'r'

cum = f.Camera()

pg.init()
sc = pg.display.set_mode((w,h))

#всратая надпись "пауза"
font = pg.font.SysFont(None, 54)
font_delay = pg.font.SysFont(None, 36)

ts = font.render("Пауза", False, (0, 255, 0))

#загружаем ассеты
sprite_sheet = pg.image.load(pp+"arrows_py/assets/atlas.png").convert_alpha()
sprite_sheet.set_alpha(230)
assets = { 
    ac.RSimple  : ac.get_sprite(sprite_sheet, acon.assets["RedSimple"   ]),
    ac.RSource  : ac.get_sprite(sprite_sheet, acon.assets["RedSource"   ]),
    ac.RBlock   : ac.get_sprite(sprite_sheet, acon.assets["RedBlock"    ]),
    ac.RDelay   : ac.get_sprite(sprite_sheet, acon.assets["RedDelay"    ]),
    ac.RDetect  : ac.get_sprite(sprite_sheet, acon.assets["RedDetect"   ]),
    ac.RTwo180  : ac.get_sprite(sprite_sheet, acon.assets["RedTwo180"   ]),
    ac.RTwo90   : ac.get_sprite(sprite_sheet, acon.assets["RedTwo90"    ]),
    ac.RThree   : ac.get_sprite(sprite_sheet, acon.assets["RedThree"    ]),
    ac.RTick    : ac.get_sprite(sprite_sheet, acon.assets["RedTick"     ]),
    ac.BSimple  : ac.get_sprite(sprite_sheet, acon.assets["BlueSimple"  ]),
    ac.BDiag    : ac.get_sprite(sprite_sheet, acon.assets["BlueDiag"    ]),
    ac.BStrStr  : ac.get_sprite(sprite_sheet, acon.assets["BlueStrStr"  ]),
    ac.BStrRight: ac.get_sprite(sprite_sheet, acon.assets["BlueStrRight"]),
    ac.BStrDiag : ac.get_sprite(sprite_sheet, acon.assets["BlueStrDiag" ]),
    ac.YNot     : ac.get_sprite(sprite_sheet, acon.assets["YellowNot"   ]),
    ac.YAnd     : ac.get_sprite(sprite_sheet, acon.assets["YellowAnd"   ]),
    ac.YXor     : ac.get_sprite(sprite_sheet, acon.assets["YellowXor"   ]),
    ac.YTrig1   : ac.get_sprite(sprite_sheet, acon.assets["YellowTrig1" ]),
    ac.YTrig2   : ac.get_sprite(sprite_sheet, acon.assets["YellowTrig2" ]),
    ac.ORand    : ac.get_sprite(sprite_sheet, acon.assets["OrangeRand"  ]),
    ac.OBtn1    : ac.get_sprite(sprite_sheet, acon.assets["OrangeBtn1"  ]),
    ac.OBtn2    : ac.get_sprite(sprite_sheet, acon.assets["OrangeBtn2"  ])
}
ac.DefaultArrow.init_asset_cash(assets, cum.cell_size)

#создаем таблички с доступными стрелками
rtable = ac.sttable('r', assets, acon.ass_cor)
btable = ac.sttable('b', assets, acon.ass_cor)
ytable = ac.sttable('y', assets, acon.ass_cor)

start_time = time.time()
while run:
    sc.fill(theme)

#ГЛАВНОЕ МЕНЮ____________________________________________________________________
    if main_menu:
        for y, element in maps.items():
            y = wrld_scr(wrld_main_cam_y, y)
            element.draw(sc, y, h)
        
        if entr_flg:
            
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if maps[where_input].text == "введите другое имя" or maps[where_input].text == "введите имя" or maps[where_input].text == 'введите dick': maps[where_input].text = ''
                    if not ic.keys.get(e.key) is None:
                        maps[where_input].text += ic.keys[e.key]
                    if e.key == pg.K_BACKSPACE and maps[where_input].text:
                        maps[where_input].text = maps[where_input].text[:-1]
                    if e.key == pg.K_RETURN:
                        if maps[where_input].text == '' or maps[where_input].text == 'введите имя' or maps[where_input].text in os.listdir(path) or maps[where_input].text== 'введите dick': maps[where_input].text = 'введите другое имя'
                        elif maps[where_input].text == 'введите другое имя': maps[where_input].text = 'введите dick'
                        else:
                            os.rename(path+'/'+map_name, path+'/'+maps[where_input].text)
                            entr_flg = False
                            maps[where_input].rename_color = (255,255,0)
            pg.display.flip()
            continue


        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_F1: theme = (255,255,255) if theme == (0, 0, 0) else (0,0,0)
                if e.key == pg.K_ESCAPE: run = False

            if e.type == pg.MOUSEWHEEL:
                wrld_main_cam_y -= 0.5*e.y
                if wrld_main_cam_y<0:  wrld_main_cam_y = 0
                elif wrld_main_cam_y > max(maps.keys()): wrld_main_cam_y = max(maps.keys())

            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == pg.BUTTON_LEFT:
                    y = floor(scr_wrld(wrld_main_cam_y, e.pos[1]))

                    if y == 0:
                        if 5<e.pos[0]<145:
                            field = {}
                            map_name = create_map(path)
                            main_menu = False

                    elif maps.get(y) is not None:
                        if 5<e.pos[0]<45:
                            
                            field = load_map(path, maps[y].text)
                            map_name = maps[y].text
                            main_menu = False

                        if 55<e.pos[0]<95:
                            os.remove(path+'/'+ maps[y].text)
                            maps = update_map_list(path)

                        if 105<e.pos[0]<145:
                            #здесь будем переименовывать карту
                            entr_flg = True
                            where_input = y
                            map_name = maps[y].text
                            maps[y].text = 'введите имя'
                            maps[y].rename_color = (255,126,0)

        pg.display.flip()
        continue


#________________________________________________________________________



    #перебираем все стрелочки для отрисовки
    for cor, arrow in field.items():
        x, y = cum.wrld_to_scr(cor)
        arrow.draw(sc, cum.cell_size, x, y, w, h)
    #отрисовываем рамки вокруг выделенных стрелочек
    for cor in slct_set:
        x,y = cum.wrld_to_scr(cor)
        if (x+cum.cell_size < 0 or y+cum.cell_size < 0 or x>w or y > h): continue
        pg.draw.rect(sc, (0, 255, 0), (x, y, cum.cell_size, cum.cell_size), 2)

    #получаем мировые кординаты мыши
    pos_mouse = cum.scr_to_wrld(pg.mouse.get_pos())

    #проверяем текущий тип, чтобы отрисовать полупрозрачную стрелочку этого типа под курсором
    if type != 0 and type != 'v':
        sc.blit(ac.DefaultArrow.assets_alfa_cash[(type, dir, ref)], cum.wrld_to_scr(pos_mouse))

    #отрисовываем стрелки из буфера
    elif type == 'v':
        #добавить преобразование сюда   поворот, отражение
        for cor, arrow in ac.transform_field(copy_field, dir, ref).items():
            x, y = cum.wrld_to_scr((pos_mouse[0] + cor[0], pos_mouse[1] + cor[1]))
            if (x+cum.cell_size < 0 or y+cum.cell_size < 0 or x>w or y > h): continue
            arrow.draw(sc, cum.cell_size, x, y, w, h, True)

    for e in pg.event.get():
        #меняем масштаб
        if e.type == pg.MOUSEWHEEL:
            cum.pos_bef_zoom = cum.scr_to_wrld(pg.mouse.get_pos())

            cum.zoom += e.y/3
            cum.set_zoom()
            cum.cell_size = 2**cum.zoom

            ac.DefaultArrow.init_asset_cash(assets, cum.cell_size)

            x,y = cum.scr_to_wrld(pg.mouse.get_pos())
            dx, dy = cum.pos_bef_zoom[0]-x, cum.pos_bef_zoom[1]-y
            cum.x += dx
            cum.y += dy
        #действия клавишами
        if e.type == pg.KEYDOWN:
            #уменьшаем задержку
            if e.key == pg.K_MINUS:
                delay -= 0.2
                if delay<delay_min: delay = delay_min
            #увеличиваем задержку
            if e.key == pg.K_EQUALS:
                delay += 0.2
                if delay>delay_max: delay = delay_max
            if type == 0:
                    if not field.get(pos_mouse) is None:
                        aaa = field[pos_mouse]
                        aaa.direction = f.set_dir(e, aaa.type, aaa.direction)
                        aaa.reflection = f.set_ref(e, aaa.type, aaa.reflection)
            else: 
            #отражаем стрелку
                ref = f.set_ref(e, type, ref)
            #изменить поворот
                dir = f.set_dir(e, type, dir)
            #вставляем
            if e.key == pg.K_v:
                type = 'v'
                dir = (0, -1)
                ref = 1
            #копируем
            if e.key == pg.K_c and slct_set:
                copy_field = ac.fcopy(slct_set, field)
                slct_set.clear()
            #вырезаем
            if e.key == pg.K_x and slct_set:
                copy_field = ac.fcopy(slct_set, field)
                for pos in slct_set: del field[pos]
                slct_set.clear()
            #множественное выделение
            if e.key == pg.K_LSHIFT: multislct = True
            #выделение
            if e.key == pg.K_e:
                if not multislct: slct_set.clear()
                selecting = True
                slct_start_cor = pos_mouse
            #удаление выделеного
            if e.key == pg.K_BACKSPACE:
                for i in slct_set: del field[i]
                slct_set.clear()
            #выход
            if e.key == pg.K_ESCAPE:
                slct_set.clear()
                save_map(field, path, map_name)
                maps = update_map_list(path)
                main_menu = True
            #смена темы
            if e.key == pg.K_F1: theme = (255,255,255) if theme == (0, 0, 0) else (0,0,0)
            #пауза
            if e.key == pg.K_SPACE: npause = not npause
            #нажатие R активирует флаг, чтобы удалять все при зажатой R
            if e.key == pg.K_r:
                Rflag = True
                slct_set.clear()
            #меняем табличку с доступными стрелочками
            if e.key == pg.K_TAB: TABflag = True
            #выбираем тип таблички
            if TABflag: tabtype = f.set_tab(e, tabtype)
            if   tabtype == 'r': type, dir, ref = f.set_type_R(e, type, dir, ref)
            elif tabtype == "b": type, dir, ref = f.set_type_B(e, type, dir, ref)
            elif tabtype == 'y': type, dir, ref = f.set_type_Y(e, type, dir, ref)
            #пипетка
            if e.key == pg.K_q:
                #получаем выбранную стрелку
                if not field.get(pos_mouse) is None:
                    aaa = field[pos_mouse]
                    #копируем ее параметры
                    type = aaa.type
                    dir = aaa.direction
                    ref = aaa.reflection
                else: type = 0
        #деактивируем флаги отжатием клавиш
        if e.type == pg.KEYUP:
            if e.key == pg.K_r: Rflag = False
            if e.key == pg.K_TAB: TABflag = False
            if e.key == pg.K_LSHIFT: multislct = False

            if e.key == pg.K_e:
                selecting = False
                slct_end_cor = pos_mouse
                for pos in field.keys():
                    stx, sty = slct_start_cor
                    enx, eny = slct_end_cor
                    x, y = pos
                    if min(stx, enx) <= x <= max(stx, enx) and min(sty, eny) <= y <= max(sty, eny):
                        slct_set.add(pos)

        if e.type == pg.MOUSEBUTTONDOWN:
            #нажатие ПКМ позволяет рисовать стрелочками или активировать кнопку
            if e.button == pg.BUTTON_LEFT:
                if not type and not field.get(pos_mouse) is None and (field.get(pos_mouse).type == ac.OBtn1 or field.get(pos_mouse).type == ac.OBtn2): field.get(pos_mouse).click()
                elif type:
                    PainFlag = True
                    slct_set.clear()
            
            if e.button == pg.BUTTON_MIDDLE:
                cum.moving_flag = True
                cum.save_pos()
                cum.start_move_cor = e.pos
        #отжатие ПКМ
        if e.type == pg.MOUSEBUTTONUP:
            if e.button == pg.BUTTON_LEFT: PainFlag = False
            if e.button == pg.BUTTON_MIDDLE: cum.moving_flag = False

    #ПРОВЕРЯЕМ ФЛАГИ
    #пока выделяем, рисуем прямоугольник
    if selecting:
        x1, y1  = cum.wrld_to_scr(slct_start_cor)
        x2, y2 = pg.mouse.get_pos()
        x, y = min(x1, x2), min(y1, y2)
        rw, rh = abs(x1 - x2), abs(y1 - y2)

        slct_surf = pg.Surface((rw, rh), pg.SRCALPHA)
        slct_surf.fill((0, 255, 0, 60))
        sc.blit(slct_surf,(x, y))
        pg.draw.rect(sc, (0, 255, 0), (x, y, rw, rh), 1)

    if cum.moving_flag:
        #текущая позиция мыши
        x_mouse, y_mouse = pg.mouse.get_pos()
        #позиция, в которой был активирован флаг moving_flag
        x_move, y_move = cum.start_move_cor
        #их разность деленная на cell_size
        dx, dy = (x_move - x_mouse)/cum.cell_size, (y_move - y_mouse)/cum.cell_size
        #обновляем позицию камеры
        cum.x = cum.last_pos[0] + dx
        cum.y = cum.last_pos[1] + dy

    #удаляем все под курсором, пока Rflag
    if Rflag: field.pop(pos_mouse, None)
    #рисуем, пока Paintflag
    if PainFlag:
        if type == 'v':
            for pos, arrow in ac.transform_field(copy_field, dir, ref).items():
                pos = (pos[0]+pos_mouse[0], pos[1]+pos_mouse[1])
                field[pos] = ac.fabric_arrows(arrow.type, arrow.direction, arrow.reflection)

        else: field[pos_mouse] = ac.fabric_arrows(type, dir, ref)

    delay = round(delay, 1)
    if not npause and (time.time() - start_time) > delay:
    #RUN tudududududu
        for cor, arrow in field.items():
            x,y = cor
            arrow.update(x, y, field)
        for arrow in field.values():
            arrow.next_tact()
        
        start_time = time.time()

    #отрисовываем текст паузы
    if npause: sc.blit(ts, (0, 40))
    if   tabtype == 'r': sc.blit(rtable, (669, 1010))
    elif tabtype == 'b': sc.blit(btable, (669, 1010))
    elif tabtype == 'y': sc.blit(ytable, (669, 1010))
    delay_text = font_delay.render(f'Задержка: {delay}', False, (0, 128, 0))
    sc.blit(delay_text, (0, 0))
    #обновляем экран
    pg.display.flip()

'''
проблемы: 
    1. графика. не отображаются некоторые ассеты при максимальном отдалении, растровые изображения вместо векторных
    2. возможно, с размером экрана


нужно:

    1. подсвечивать карту, в которой только что был
    2. автосохранение

    ∞. удалить нахуй весь код и написать новый с нуля (на с++), потому что получилась хуйня
'''