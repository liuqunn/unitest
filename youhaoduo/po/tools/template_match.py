#!/usr/bin/env python


import cv2


def match(target, template):
    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    w, h = template.shape[::-1]
    w2, h2 = cv2.imread(target, 0).shape[::-1]
    # print(w, h)
    # print(w2, h2)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 得到最大和最小值位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)

    top_left = max_loc  # 左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位置

    xx = (max_loc[0] + 0.5 * w) / w2    # 相对坐标
    yy = (max_loc[1] + 0.5 * h) / h2    # 相对坐标
    # print(xx, yy)
    return xx, yy, max_val