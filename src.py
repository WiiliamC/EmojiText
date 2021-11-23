from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np


class TextProcesser:
    def __init__(self, back='😘', fore='❤️', col_num=12, debug=False):
        self.background = back  # 背景表情
        self.foreground = fore  # 前景表情
        self.col_num = col_num  # 微信-11，qq-12
        self.debug = debug  # 是否为调试模式
        self._del_set = {' ', '\n'}

    def _draw_word(self, word):
        """将字符绘制为图像"""
        # 预设合适的字体，对于中文尤其重要，否则会乱码，这里使用常见的黑体
        # 根据中英文确定绘制位置
        if word.encode("UTF-8").isalnum():
            pos = (round(self.col_num / 4), -1)  # 文字位置
            font_size = self.col_num  # 字体大小
            font = ImageFont.truetype("tahoma", size=font_size)  # 文字设置
            image_size = (self.col_num, round(self.col_num * 1.2))  # 图像大小
        else:
            pos = (0, -1)  # 文字位置
            font_size = self.col_num  # 字体大小
            font = ImageFont.truetype("simhei", font_size, encoding='utf-8')  # 文字设置
            image_size = (self.col_num, self.col_num)  # 图像大小
        # 灰度图
        image = Image.new('1', image_size, 'white')
        draw = ImageDraw.Draw(image)
        draw.text(pos, word, font=font)
        if self.debug:
            plt.imshow(image)  # 使用matplotlib显示
            plt.show()
            print(np.array(image, dtype=bool))  # 转数组
        # 居中平移。不同的字符在同一位置绘制的位置不同，因此需要将他们平移到上下居中、左右居中的位置上。
        image = self._move(image)
        return image

    def _move(self, image):
        """
        居中平移。不同的字符在同一位置绘制的位置不同，因此需要将他们平移到上下居中、左右居中的位置上。
        输入PIL的Image类，返回bool型ndarray类。
        """
        image = np.array(image, dtype=bool)
        # 行开始
        for i in range(image.shape[0]):
            if np.all(image[i, :]) and not np.all(image[i + 1, :]):
                top = i
                break
            elif not image[i, :].all():
                top = i
                break
        # 行结束
        for i in range(image.shape[0] - 1, 0, -1):
            if image[i, :].all() and not image[i - 1, :].all():
                bottom = i
                break
            elif not image[i, :].all():
                bottom = i
                break
        # 列开始
        for i in range(image.shape[1]):
            if image[:, i].all() and not image[:, i + 1].all():
                left = i
                break
            elif not image[:, i].all():
                left = i
                break
        # 列结束
        for i in range(image.shape[1] - 1, 0, -1):
            if np.all(image[:, i]) and not np.all(image[:, i - 1]):
                right = i
                break
            elif not image[:, i].all():
                right = i
                break
        # 左右上下居中
        new_image = np.ones_like(image)
        h, w = bottom - top - 1, right - left - 1
        t, l = round((image.shape[0] - h) / 2), round((image.shape[1] - w) / 2)
        new_image[t:t + h, l:l + w] = image[top + 1:bottom, left + 1:right]
        return new_image

    def _is_chinese(self, word):
        """判断字符是不是汉字"""
        if u'\u4e00' <= word <= u'\u9fa5':
            return True
        else:
            return False

    def process(self, text):
        """将文本处理为emoji字符串"""
        emojis = ""
        # 遍历文字
        for word in text:
            if word in self._del_set:
                continue
            # 画图
            image = self._draw_word(word)
            for r in range(image.shape[0]):
                for c in range(image.shape[1]):
                    if image[r][c]:
                        emojis += self.background
                    else:
                        emojis += self.foreground
                emojis += '\n'
            emojis += '\n\n'
        return emojis


if __name__ == '__main__':
    tp = TextProcesser(debug=True)
    print(tp.process("！"))
