# -*- coding: utf-8 -*


from PIL import Image
from loguru import logger
from po.tools.chineseocr_lite.model import OcrHandle
from io import BytesIO


class OcrLite:
    """
    获取图片文件
    """

    def __init__(self, img_path=None, img_source=None, img_PIL=None):
        self.img = None
        self.ocrhandle = OcrHandle()
        if img_source is None:
            if img_path is not None:
                try:
                    self.img = Image.open(img_path)
                except Exception as e:
                    logger.debug('错误：打开图片失败')
                    return
            elif img_PIL is not None:
                self.img = img_PIL
            else:
                return
        else:
            self.img = Image.open(BytesIO(img_source))

    def detectText(self):
        if self.img is None:
            return
        res = self.ocrhandle.text_predict(self.img)
        res_format = []
        width, height = self.img.size
        for i in res:
            res_format.append({'Text': i[1],
                               'Range': [i[0][0], i[0][2]],
                               'Center': [round((i[0][0][0] + i[0][2][0]) / 2 / width, 2),
                                          round((i[0][0][1] + i[0][2][1]) / 2 / height, 2)],
                               'Img-Size': [width, height]})
        logger.info(res_format)
        return res_format


if __name__ == '__main__':
    tr = OcrLite()
    tr.detectText()
