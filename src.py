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
        image = self._get_roi(image)
        if self.debug:
            plt.imshow(image)  # 使用matplotlib显示
            plt.show()
            print(np.array(image, dtype=bool))  # 转数组
        # 调整分辨率
        new_size = (int(self.col_num * image.size[0] / image.size[1]) + 1, self.col_num)
        image = image.resize(new_size)
        if self.debug:
            plt.imshow(image)  # 使用matplotlib显示
            plt.show()
            print(np.array(image, dtype=bool))  # 转数组
        return image

    def _get_roi(self, image0):
        """获取图像的文字区域roi"""
        image = np.array(image0, dtype=bool)
        roi = [-1, -1, -1, -1]
        for i in range(image.shape[0] - 1):
            # 行
            if roi[0] == -1 and image[i, :].all() and not image[i + 1, :].all():
                roi[0] = i - 1
            elif not image[i, :].all() and image[i + 1, :].all():
                roi[1] = i + 2
            # 列
            if roi[2] == -1 and image[:, i].all() and not image[:, i + 1].all():
                roi[2] = i - 1
            elif not image[:, i].all() and image[:, i + 1].all():
                roi[3] = i + 2
        return image0.crop((roi[2], roi[0], roi[3], roi[1]))

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
    print(tp.process("ILOVEYOU"))
