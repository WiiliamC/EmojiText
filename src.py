from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np


class TextProcesser:
    def __init__(self, back='😘', fore='❤️', col_num=12, debug=False):
        self.background = back  # 背景表情
        self.foreground = fore  # 前景表情
        self.col_num = col_num  # 微信-11，qq-12
        self.debug = debug  # 是否为调试模式
        self._image_size = (col_num, col_num)  # 绘制文字的图像尺寸
        self._font_size = col_num + 1  # 文字字体大小
        # todo: 中英文识别

    def _draw_word(self, word):
        """将字符绘制为图像"""
        # 预设合适的字体，对于中文尤其重要，否则会乱码，这里使用常见的黑体
        font = ImageFont.truetype("simhei", self._font_size, encoding='utf-8')
        # 灰度图
        image = Image.new('1', self._image_size, 'white')
        draw = ImageDraw.Draw(image)
        draw.text((0, -1), word, font=font)
        if self.debug:
            plt.imshow(image)  # 使用matplotlib显示
            plt.show()
            print(np.array(image, dtype=bool))  # 转数组
        return np.array(image, dtype=bool)

    def process(self, text):
        """将文本处理为emoji字符串"""
        emojis = ""
        # 遍历文字
        for word in text:
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
    tp = TextProcesser()
    print(tp.process("爱你呦青"))
