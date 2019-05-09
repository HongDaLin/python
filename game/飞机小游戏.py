'''
1. 创建窗口
2.加载图片
3. 贴图
4. 刷新界面
5. 事件处理
6. 添加英雄飞机
7. 英雄飞机左右移动

程序 = 对象 + 对象 。。。。。。。

# 类： 属性 + 方法列表
'''
#  常量,窗口的宽度和高度
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 768

import pygame # 导入pygame所有动态模块
#from pygame import locals #导入本地
from pygame.locals import  * # *通配符，把本地的所有都导入进来
import sys
import time #导入时间模块
import random

score = 0

class Item:#把相同的部分抽取出来（属性，方法）
    """界面元素类"""
    window = None # 类属性，只开辟一个内存空间，可以同类，可以通过对象去使用
    #属性初始化
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)  # 图片
        self.x = x
        self.y = y

    #显示
    def display(self):
        self.window.blit(self.img, (self.x, self.y))  # 元祖表示位置坐标

#子弹
class Bullet(Item):
#属性定义；"""子弹类"""

    # 子弹向上移动
    def move_up(self):
        self.y -= 5

    #判断子弹和飞机是否相碰
    def is_hit_plane(self, enemy):
        bullet_rect = Rect(self.x,self.y,20,31) #子弹区域
        enemy_rect = Rect(enemy.x,enemy.y,100,68) # 敌人飞机的区域
        return pygame.Rect.colliderect(bullet_rect, enemy_rect) #判断两个区域是否相交，有返回真，没有假

class Map(Item):
    """背景图片类"""
    pass


class Base_Plane(Item):
    """飞机基类"""
    pass

#英雄飞机
class Hero_Plane(Base_Plane):
    """英雄飞机类"""
    """属性（数据），方法（操作）"""
#属性
    # 创建对象，自动调用 init 函数，定义实例属性，初始化
    def __init__(self,img_path,x,y):#形参（图片路径，x,y坐标， 窗口）
        """类属性"""
        super().__init__(img_path,x,y)
        self.bullets = [] # 定义列表，保存所有的子弹

#方法
      #向左移动
    def move_left(self):
        self.x -= 5
      #向右移动
    def move_right(self):
        self.x += 5
        #贴图显示

        #发射子弹
    def fire(self):
        # X = 英雄飞机x + W / 2.0 - 子弹宽度 / 2.0
        # Y = 英雄飞机Y - 子弹高度
        # 创建子弹对象
        bullet = Bullet("res/bullet_9.png",self.x + 50,self.y - 31)
        #bullet.display()
        self.bullets.append(bullet) # 列表尾部添加，保存子弹

    #显示所有子弹
    def display_bullet(self,enemy_list):
        # bullet_list = self.bullets  # 去除所有子弹
        del_bullets = [] # 定义空的将要删除的子弹列表
        for bullet in self.bullets :  # 显示子弹
            if bullet.y >= -31: #子弹方向坐标在窗口内部，显示并移动
                bullet.display()
                bullet.move_up()

                for enemy in enemy_list:
                   if bullet.is_hit_plane(enemy):
                       del_bullets.append(bullet)  # 记录将要删除的子弹
                       enemy.is_hitted = True #记录敌人飞机碰撞的状态

                       global score
                       score += 10

                       break; # 当子弹碰撞飞机时，销毁当前飞机后，直接跳出
            else:
                #self.bullets.remove(bullet)
                del_bullets.append(bullet)#记录将要删除的子弹

        for bullet in del_bullets: #删除超出窗口的子弹
            self.bullets.remove(bullet)

        print("len = ", len(self.bullets))

class Enemy_Plane(Base_Plane):
    """敌机类"""
    def __init__(self,img_path, x, y):
        super().__init__(img_path, x, y)
        self.is_hitted = False

    #敌人飞机向下移动
    def move_down(self):
        self.y += 5 #飞机向下飞行，Y坐标增大
        # 第一步：判断敌人飞机是否超出窗口下边缘
        # 第二步： 如果超出下边缘坐标Y，让它重新飞，如果不超出下边缘，继续飞
        if self.y >= WINDOW_HEIGHT or self.is_hitted:#第一步,如果相碰，重新去设置敌人飞机
            self.y = random.randint(-300,-68)
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1,7))
            self.is_hitted = False


#软件入口，相当于一个进程
def main():
    #初始化计算机硬件，文字
    pygame.init()
    # 创建窗口
    window = pygame.display.set_mode((WINDOW_WIDTH, 768))
    #给Item 的类属性进行赋值
    Item.window = window

    # 加载背景图片文件，返回图片对象
    map = Map("res/img_bg_level_1.jpg",0,0)
    # 创建英雄飞机对象
    hero_plane = Hero_Plane("res/hero2.png",196,500)#实参

    #创建敌人飞机对象
    #x 坐标范围： 0 ~ WINDOW_WIDTH - 100
    #enemy_plane = Enemy_Plane("res/img-plane_1.png",20,-68,window)
    #random 去取随机数
    enemy_plane_list = []
    for i in range(0,5):
        #  random.randint(startNum,endNum) 获取随机数，startNum起始值，endNum结束值
        enemy_plane = Enemy_Plane("res/img-plane_%d.png" % random.randint(1,7),random.randint(0, WINDOW_WIDTH - 100),random.randint(-300,-68))
        enemy_plane_list.append(enemy_plane)

    # 加载自定义字体，返回字体对象
    font_obj = pygame.font.Font("res/SIMHEI.TTF", 42)

    while True:
        # # 贴图(背景图）（指定坐标，将图片绘制到窗口）
        # window.blit(image, (0, 0))  # (x,y) 元组， []  列表， {} 字典
        # 贴图(背景图）（指定坐标，将图片绘制到窗口）
        map.display()

        hero_plane.display()# 显示英雄飞机

        hero_plane.display_bullet(enemy_plane_list) #批量显示子弹

        for enemy_plane in enemy_plane_list:
            enemy_plane.display()#敌人飞机显示
            enemy_plane.move_down()#敌人飞机移动

        # 设置文本，返回文本对象   render(文本内容， 抗锯齿，颜色)
        text_obj = font_obj.render("得分：%d" % score, 1, (255, 255, 255))

        # 设置文本的位置和尺寸   获取文本的Rect并修改Rect的中心点为 （300，300）
        text_rect = text_obj.get_rect(centerx = 100, centery = 50)

        window.blit(text_obj,text_rect)

        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

        # 获取事件
        for event in pygame.event.get():
            # 1. 鼠标点击关闭窗口事件
            if event.type == QUIT:
                print("点击关闭窗口按钮")
                sys.exit()  # 关闭程序

            # 2.键盘按下事件
            if event.type == KEYDOWN:
                # # 判断用户按键
                if event.key == K_SPACE:
                    print("space")
                    hero_plane.fire()


        #键盘长按事件
        # 获取当前键盘所有按键的状态（按下/没有按下），返回bool元组  (0, 0, 0, 0, 1, 0, 0, 0, 0)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            hero_plane.move_left() # 左移动

        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            hero_plane.move_right()# 右移动

        time.sleep(0.02) #缓冲0.02秒

if __name__ == '__main__':
    main()
