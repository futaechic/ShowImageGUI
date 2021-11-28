import numpy as np
import io
import cv2
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance


def get_image(img, alpha_val, vivid_val, contrast_val):
    """
    画像の色調を変える
    :param img: 画像処理を施す画像
    :param alpha_val: 透過度パラメータ
    :param vivid_val: 彩度パラメータ
    :param contrast_val: コントラストパラメータ
    :return: 変換後の画像
    """
    image = img.copy()
    image = ImageEnhance.Color(image).enhance(float(vivid_val))
    image = ImageEnhance.Contrast(image).enhance(float(contrast_val))
    image.putalpha(int(alpha_val))

    return image


def set_image_data(filePath):
    """
    透明度あり，RGBの
    :param filePath: 画像ファイルパス
    :return:
    """
    image = Image.open(filePath).convert("RGBA")
    image.thumbnail((400, 400))
    return image


def make_histgram(img):
    """
    画像のヒストグラムを算出
    :param img: 彩度，コントラスト変換後の画像
    :return: Figure
    """
    img_numpy = np.array(img.copy(), dtype=np.uint8)
    color = ('r', 'g', 'b')  # PIL.Image --> ndarray なので 色の順番は"RGB"
    fig = plt.figure(facecolor="lightgray")
    for i, col in enumerate(color):
        hist = cv2.calcHist([img_numpy], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])
    return fig


def plot_image(fig):
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.close()
    return item.getvalue()
