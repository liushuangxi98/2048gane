import pygame
import os
import keyboard as keyboard
import random
import math
from pygame import K_ESCAPE, KEYDOWN


class Game(object):
    def __init__(self):
        # 初始化
        pygame.init()
        # 创建窗口
        self.window = pygame.display.set_mode((400, 500))
        # 定义变量
        self.grid = []  # 棋盘上存放的数据
        self.score = 0  # 游戏分数
        # 加载图片
        self.pict_path = {'2': os.getcwd() + '/图片/2.png', '4': os.getcwd() + '/图片/4.jpg',
                          '8': os.getcwd() + '/图片/8.jpg',
                          '16': os.getcwd() + '/图片/16.jpg', '32': os.getcwd() + '/图片/32.jpg',
                          '64': os.getcwd() + '/图片/64.jpg',
                          '128': os.getcwd() + '/图片/128.jpg', '256': os.getcwd() + '/图片/256.jpg'}
        self.pict_2 = pygame.image.load(self.pict_path['2'])
        self.pict_4 = pygame.image.load(self.pict_path['4'])
        self.pict_8 = pygame.image.load(self.pict_path['8'])
        self.pict_16 = pygame.image.load(self.pict_path['16'])
        self.pict_32 = pygame.image.load(self.pict_path['32'])
        self.pict_64 = pygame.image.load(self.pict_path['64'])
        self.pict_128 = pygame.image.load(self.pict_path['128'])
        self.pict_256 = pygame.image.load(self.pict_path['256'])
        self.di = pygame.image.load('./图片/di.jpg')
        self.load = [0, self.pict_2, self.pict_4, self.pict_8, self.pict_16, self.pict_32, self.pict_64, self.pict_128,
                     self.pict_256]
        # 播放背景音乐
        pygame.mixer.music.load('./图片/读者.mp3')
        pygame.mixer.music.play(-1)

    def reset(self):
        # 初始化棋盘
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # 初始化分数
        self.score = 0
        # 在棋盘上创建2个随机的数字
        self.rnd_2()
        self.rnd_2()
        # 显示屏幕
        self.display()

    def rnd_2(self):
        """
        当游戏没有输的时候并且棋盘没有满的时候执行，随机生成值和坐标，当坐标的原有值不为0时返回此函数重新随机，为0时可以进行赋值，
        :return:
        """
        if (not self.is_lose()) and self.not_full():
            value = 4 if random.randrange(100) > 89 else 2
            x, y = random.choice([(x, y) for x in [0, 1, 2, 3] for y in [0, 1, 2, 3]])
            if self.grid[x][y] != 0:
                return self.rnd_2()
            self.grid[x][y] = value

    def not_full(self):
        """
        循环棋盘列表，当有一个值为0时返回1，any任何一个值为1时都视为没有满
        :return:
        """
        return any([1 for i in self.grid for j in i if j == 0])

    def display(self):
        y = 0
        # 显示背景
        self.window.fill((205, 193, 180))
        self.window.blit(self.di, (0, 400))
        # 显示窗口名字
        pygame.display.set_caption("刘双喜的2048小游戏")
        # 显示底部文字
        text1 = pygame.font.Font('c:/Windows/Fonts/simhei.ttf', 30)
        text1_load = text1.render(' Q:退出游戏    R:重新开始', True, (249, 246, 242))
        self.window.blit(text1_load, (0, 420))
        text2 = pygame.font.Font('c:/Windows/Fonts/simhei.ttf', 30)
        text2_load = text2.render(f' 分数：{self.score}', True, (249, 246, 242))
        self.window.blit(text2_load, (0, 460))
        # 显示棋盘和图片
        for i in self.grid:
            x = 0
            for j in i:
                if j != 0:
                    self.window.blit(self.load[int(math.log(j, 2))], (x, y))
                x += 100
            y += 100
        # 更新
        pygame.display.update()

    def move(self):
        def combine_left():
            """
            遍历棋盘列表，当相邻两个值相等时相加，值赋给左边的元素
            :return:
            """
            for i in self.grid:  # 相加
                if i[0] == i[1]:
                    i[0] = i[0] * 2
                    i[1] = 0
                    self.score = self.score + i[0]
                if i[1] == i[2]:
                    i[1] = i[1] * 2
                    i[2] = 0
                    self.score = self.score + i[1]
                if i[2] == i[3]:
                    i[2] = i[2] * 2
                    i[3] = 0
                    self.score = self.score + i[2]

        def combine_right():
            """
            遍历棋盘列表，当相邻两个值相等时相加,值赋给右边的元素
            :return:
            """
            for i in self.grid:  # 相加
                if i[2] == i[3]:
                    i[3] = i[3] * 2
                    i[2] = 0
                    self.score = self.score + i[3]
                if i[1] == i[2]:
                    i[2] = i[2] * 2
                    i[1] = 0
                    self.score = self.score + i[2]
                if i[0] == i[1]:
                    i[1] = i[1] * 2
                    i[0] = 0
                    self.score = self.score + i[1]

        def move_left():
            """
            循环棋盘列表，当遇到0时删除0，同时在列表末尾加0，实现左移；然后再相加，再左移
            :return:
            """
            for i in self.grid:  # 去0
                for j in i:
                    if j == 0:
                        i.remove(j)
                        i.append(0)
            combine_left()
            for i in self.grid:  # 去0
                for j in i:
                    if j == 0:
                        i.remove(j)
                        i.append(0)

        def move_right():
            """
            循环棋盘列表，当遇到0时删除，同时在列表头加0，实现右移；再相加，再右移
            :return:
            """
            for i, ls in enumerate(self.grid):  # 去0
                for index, value in enumerate(ls):
                    if value == 0:
                        ls.pop(index)
                        ls.insert(0, 0)
            combine_right()
            for i, ls in enumerate(self.grid):  # 去0
                for index, value in enumerate(ls):
                    if value == 0:
                        ls.pop(index)
                        ls.insert(0, 0)

        # 当按键时，依次执行移动相加-生成新的数字-显示；上下移动时通过转置再反转置
        if keyboard.is_pressed('left'):
            print('键入left')
            move_left()
            self.rnd_2()
            self.display()
        elif keyboard.is_pressed('right'):
            print('键入right')
            move_right()
            self.rnd_2()
            self.display()
        elif keyboard.is_pressed('up'):
            print('键入up')
            self.grid = list(map(list, zip(*self.grid)))  # 转置
            move_left()
            self.grid = list(map(list, zip(*self.grid)))  # 转置
            self.rnd_2()
            self.display()
        elif keyboard.is_pressed('down'):
            print('键入down')
            self.grid = list(map(list, zip(*self.grid)))  # 转置
            move_right()
            self.grid = list(map(list, zip(*self.grid)))  # 转置
            self.rnd_2()
            self.display()
        else:
            self.display()

    def is_win(self):
        """
        循环棋盘列表，，返回大于设定的值到列表，当列表不为空是返回Ture，视为赢
        :return:
        """
        return any([j for i in self.grid for j in i if j >= 64])

    def is_lose(self):
        """
        循环棋盘列表，当有上下相邻值相等或者左右相邻值相等或者值为0，认为没有输，列表返回0.all函数里没有0时（为空）返回Ture，认为输
        :return:
        """
        return all(
            [0 for i, j, k, l in self.grid if i == j or j == k or k == l or i == 0 or j == 0 or k == 0 or l == 0] +
            [0 for i, j, k, l in list(map(list, zip(*self.grid))) if
             i == j or j == k or k == l or i == 0 or j == 0 or k == 0 or l == 0]
        )


def main():
    # 初始化的状态，执行复位函数，进入游戏状态
    def init():
        game.reset()
        return 'Gaming'

    # 游戏状态，循环判断退出Q和重新开始R按键，执行移动按键检测函数，执行判断输赢函数
    def gaming():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'Quit'
            if keyboard.is_pressed('Q'):
                return 'Quit'
            if keyboard.is_pressed('R'):
                return 'Init'
            game.move()
        if game.is_win():
            return 'Win'
        if game.is_lose():
            return 'Lose'
        return "Gaming"

    # 赢状态，打印You Win！的提示，循环判断退出Q和重新开始R按键
    def win():
        text = pygame.font.Font('c:/Windows/Fonts/simhei.ttf', 50)
        text_load = text.render('You Win!', True, (255, 0, 0))
        game.window.blit(text_load, (100, 150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'Quit'
            if keyboard.is_pressed('Q'):
                return 'Quit'
            if keyboard.is_pressed('R'):
                return 'Init'
        return 'Win'

    # 输状态，打印You Lose！的提示，循环判断退出Q和重新开始R按键
    def lose():
        text = pygame.font.Font('c:/Windows/Fonts/simhei.ttf', 50)
        text_load = text.render('You Lose!', True, (255, 0, 0))
        game.window.blit(text_load, (100, 150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'Quit'
            if keyboard.is_pressed('Q'):
                return 'Quit'
            if keyboard.is_pressed('R'):
                return 'Init'
        return 'Lose'

    # 储存状态的字典
    states = {
        'Init': init,
        'Gaming': gaming,
        'Win': win,
        'Lose': lose,
    }
    # 实例化
    game = Game()
    # 进游戏的时候默认是初始状态
    state = 'Init'
    # 循环状态机，执行状态函数
    while state != 'Quit':
        state = states[state]()


if __name__ == '__main__':
    main()
