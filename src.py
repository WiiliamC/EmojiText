from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np


class TextProcesser:
    def __init__(self, back='😘', fore='❤️', col_num=12):
        self.background = back  # 背景表情
        self.foreground = fore  # 前景表情
        self.col_num = col_num  # 微信-11，qq-12
        self.debug = True  # 是否为调试模式
        self._image_size = (256, 256)  # 绘制文字的图像尺寸
        self._font_size = 210  # 文字字体大小

    def _draw_word(self, word):
        """将字符绘制为图像"""
        # 预设合适的字体，对于中文尤其重要，否则会乱码，这里使用常见的黑体
        font = ImageFont.truetype("simhei", self._font_size, encoding='utf-8')
        # 灰度图
        image = Image.new('1', self._image_size, 'white')
        draw = ImageDraw.Draw(image)
        draw.text((1, 1), word, font=font)
        if self.debug:
            plt.imshow(image)  # 使用matplotlib显示
            plt.show()
            print(np.array(image, dtype=bool))  # 转数组
        # 获取roi
        image, w_h = self._get_roi(image)
        # 调整分辨率
        image = image.resize(self.col_num)
        return image

    def _get_roi(self, image):
        """获取图像的文字区域roi"""

    def process(self, text):
        """将文本处理为emoji字符串"""
        emojis = ""
        # 遍历文字
        for word in text:
            # 画图
            image = self._draw_word(word)

        return emojis


if __name__ == '__main__':
    tp = TextProcesser()
    print(tp.process("这是一个你爱中文的我吴青ILOVEYOU"))
