#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import os
from loguru import logger
import cv2
import subprocess
from PIL import Image
from io import BytesIO
from skimage.metrics import structural_similarity
import requests
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webelement import WebElement
from po.tools.template_match import match
from po.tools.get_webauth_cookie import get_cookies
from po.tools.get_webauth_cookie import get_cookies_mod
from po.tools.del_user import num_to_a
from po.tools.lib import adbOperation
from po.tools.chineseocr_lite.main import OcrLite
from po.tools.lib.adbOperation import ADB


class BasePage(object):
    click_black = [
        # 弹窗 用户须知
        (By.XPATH, "//*[@text='同意~ 进入APP']"),
        # 系统弹窗 始终允许
        (By.XPATH, "//*[@text='允许']"),
        (By.XPATH, "//*[@text='始终允许']"),
        (By.XPATH, "//*[@text='禁止后不再提示']"),
        # 必玩弹窗
        (By.XPATH, "//*[@text='遗憾错过']"),
        (By.XPATH, "//*[@text='一键加载']"),
        # 系统更新
        (By.XPATH, "//*[@text='稍后']"),
        # 登录后真人认证弹窗 稍后再说
        (By.XPATH, "//*[@text='稍后再说']")

    ]

    # 左上角返回
    _left_top_goback = "//*[contains(@content-desc, '转到上一层级')]"
    # 飞行模式按钮
    _airplane_mode_btn = (By.XPATH, "//android.widget.Switch[@content-desc='飞行模式']")

    picture_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../test_pics/"))  # 测试Case时截取的图片
    os.makedirs(picture_path) if not os.path.exists(picture_path) else None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../template_pics"))
        self.expected_pics = os.path.abspath(os.path.join(os.path.dirname(__file__), "../expected_pics"))

    def popups_ele(self):
        for e in self.click_black:
            try:
                elements = self.driver.find_elements(*e)
                if len(elements) > 0:
                    elements[0].click()
                    break
            except:
                pass

    def find(self, loc, times=2):
        try:
            ele = self.driver.find_element(*loc)
            return ele
        except:
            if times == 0:
                ele = self.driver.find_element(*loc)
                return ele
            else:
                logger.info(f'未找到{str(loc)}元素，进行弹窗处理')
                logger.info('第{}次弹窗处理'.format(3 - times))
                self.popups_ele()
                times = times - 1
                return self.find(loc, times)

    def find_direct(self, loc):
        ele = self.driver.find_element(*loc)
        return ele

    def exists(self, loc, times=2):
        try:
            self.finds(*loc)
            return True
        except:
            if times == 0:
                ele = self.finds(*loc)
                if not ele:
                    return False
                else:
                    return True
            else:
                logger.info('第{}次弹窗处理'.format(3 - times))
                self.popups_ele()
                times = times - 1
                return self.find(loc, times)

    def finds(self, loc, times=2):
        try:
            eles = self.driver.find_elements(*loc)
            return eles
        except:
            if times == 0:
                ele = self.driver.find_element(*loc)
                return ele
            else:
                logger.info('第{}次弹窗处理'.format(3 - times))
                self.popups_ele()
                times = times - 1
                return self.finds(loc, times)

    def is_exist(self, loc):
        # 如果a元素不存在,返回False,否则返回True,简单粗暴
        eles = self.driver.find_elements(*loc)
        if eles == []:
            return False
        else:
            return eles

    def find_id(self, id):
        return self.find((By.ID, id))

    def find_ids(self, id):
        return self.finds((By.ID, id))

    def find_xpath(self, xpath):
        return self.find((By.XPATH, xpath))

    def find_text(self, text):
        return self.find((By.XPATH, "//*[@text='%s']" % text))

    def find_toast(self):
        return self.find((By.XPATH, "//*[@class='android.widget.Toast']"))

    def long_press(self, ele: WebElement, duration=1500):
        # TouchAction(self.driver).long_press(ele).perform()
        location = ele.location
        self.driver.tap([(location['x'], location['y'])], duration=duration)

    def long_press_text(self, text, duration=1500):
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]'.format(text))
        location = ele.location
        self.driver.tap([(location['x'], location['y'])], duration=duration)

    def long_press_location(self, a, b, duration=1500):
        x, y = self.get_size()
        aa = x * a
        bb = y * b
        self.driver.tap([(aa, bb)], duration=duration)

    def get_size(self):
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        return x, y

    def swipe(self, direction='up'):
        time.sleep(1)
        x, y = self.get_size()
        if direction == 'up':
            self.driver.swipe(0.5 * x, 0.7 * y, 0.5 * x, 0.2 * y, 300)
        elif direction == 'down':
            self.driver.swipe(0.5 * x, 0.2 * y, 0.5 * x, 0.7 * y, 300)
        elif direction == 'left':
            self.driver.swipe(0.8 * x, 0.5 * y, 0.2 * x, 0.5 * y, 300)
        elif direction == 'right':
            self.driver.swipe(0.2 * x, 0.5 * y, 0.8 * x, 0.5 * y, 300)
        time.sleep(2)

    # 传入xy的比例进行滑动
    def swipe_ratio(self, start_xx, start_yy, end_xx, end_yy, d=None):
        time.sleep(1)
        x, y = self.get_size()
        self.driver.swipe(start_xx * x, start_yy * y, end_xx * x, end_yy * y, d)
        time.sleep(2)

    # 相对位置点击
    def offset_click(self, ele: WebElement, a, b):
        loc = ele.location
        size = ele.size
        x = loc['x'] + a * size['width']
        y = loc['y'] + b * size['height']
        self.driver.tap([(x, y)])
        return (x, y)

    # 相对位置点击通过adb
    def offset_click_adb(self, ele: WebElement, a, b):
        loc = ele.location
        size = ele.size
        x = loc['x'] + a * size['width']
        y = loc['y'] + b * size['height']
        self.driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap', x, y],
            'includeStderr': True,
            'timeout': 5000
        })

    # 相对坐标点击
    def offset_position_click(self, a, b):
        x, y = self.get_size()
        aa = x * a
        bb = y * b
        self.driver.tap([(aa, bb)])

    def tap(self, positions):
        self.driver.tap(positions)

    def center_click(self):
        x, y = self.get_size()
        self.driver.tap([(1 / 2 * x, 1 / 2 * y)])

    def half_click(self):
        x, y = self.get_size()
        self.driver.tap([(1 / 2 * x, 1 / 4 * y)])

    def enter(self):
        self.driver.activate_ime_engine("com.sohu.inputmethod.sogou/.SogouIME")
        time.sleep(0.8)
        self.driver.press_keycode(66)
        self.driver.activate_ime_engine("io.appium.settings/.UnicodeIME")

    def goback(self):
        self.driver.back()
        # self.driver.press_keycode(4)
        self.sleep(0.5)

    def background(self, s):
        self.driver.background_app(s)

    def sleep(self, t):
        time.sleep(t)

    def quit(self):
        time.sleep(0.5)
        return self.driver.quit()

    def close_app(self):
        self.driver.close_app()
        self.sleep(2)

    def launch_app(self):
        self.driver.launch_app()

    def switch_app(self, package, activity):
        self.driver.start_activity(package, activity)
        self.sleep(2)

    def switch_setting_app(self):
        self.switch_app('com.android.settings', '.HWSettings')

    def click_home(self):
        self.driver.press_keycode(3)

    def set_clipboard(self, text):
        return self.driver.set_clipboard_text(text)

    def lock_screen(self):
        # 按电源键，锁屏
        self.driver.press_keycode(26)
        self.driver.implicitly_wait(2)
        self.sleep(3)
        # 按电源键，无锁屏密码
        self.driver.press_keycode(26)
        self.sleep(3)
        self.swipe(direction='up')

    def screenshot(self, file):
        """
        截取图片
        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.

        :Usage:
            对driver.get_screenshot_as_file的封装
            driver.get_screenshot_as_file('/Screenshots/foo.png')
        """
        self.driver.get_screenshot_as_file(file)

    def screenshot_minicap(self, udid, file):
        return ADB(udid).minicap_screen_shot(file)

    def image_crop(self, file_path, percentage_rangle):
        base_image = Image.open(file_path)
        x, y = base_image.size
        new_image = base_image.crop((int(percentage_rangle[0] * x), int(percentage_rangle[1] * y),
                                     int(percentage_rangle[2] * x), int(percentage_rangle[3] * y)))
        new_image.save(file_path)
        return file_path
    
    def screenshot_crop(self, filename, percentage_rangle=None):
        """
        截取部分图片
        :Args:
            filename: 文件名，不包含.png。存储在self.picture_path文件夹
            percentage_rangle: 截取图片的起始X百分比、起始Y百分比、结束X百分比、结束Y百分比的元祖

        :Usage:
            screenshot_crop('test', (0, 0, 0.8, 0.8))

        :Returns:
            保存成功为True，失败为False
        """
        file_path = os.path.join(self.picture_path, filename)
        if not self.driver.get_screenshot_as_file(file_path):
            return False
        if percentage_rangle:
            base_image = Image.open(file_path)
            x, y = base_image.size
            new_image = base_image.crop((int(percentage_rangle[0] * x), int(percentage_rangle[1] * y),
                                         int(percentage_rangle[2] * x), int(percentage_rangle[3] * y)))
            new_image.save(file_path)
        return file_path

    # 截图判断图片匹配度，大于0.9返回相对坐标
    def is_match(self, template):
        # template = '../../template_pics/is_auth.png'
        target = self.template_path + '/target.png'
        self.screenshot(target)
        xx, yy, val = match(target, template)
        if val > 0.9:
            return xx, yy
        else:
            return False

    def is_match_part(self, template, part):
        """
        部分图像识别匹配
        Args:
            template:
            part: x,y最大值
        Returns:
        """
        # template = '../../template_pics/is_auth.png'
        target = self.template_path + '/target.png'
        self.screenshot_crop(target, [0, 0, part[0], part[1]])
        target = self.template_path + '/target.png'
        xx, yy, val = match(target, template)
        logger.info('相对坐标 ({},{}), 匹配度 {}'.format(xx, yy, val))
        if val > 0.9:
            return xx * part[0], yy * part[1]
        else:
            logger.info('模板匹配失败')
            return False

    # 截图判断图片匹配度，大于0.9返回相对坐标和匹配度
    def is_match_plus(self, template):
        """
        Args:
            template: 目标图片
        Returns:
            相对坐标x, y, 百分比
        """
        # template = '../../template_pics/is_auth.png'
        target = self.template_path + '/target.png'
        self.screenshot(target)
        xx, yy, val = match(target, template)
        logger.info('相对坐标 ({},{}), 匹配度 {}'.format(xx, yy, val))
        if val > 0.9:
            return xx, yy, val
        else:
            logger.info('模板匹配失败')
            return False

    # 左上角返回
    def left_top_goback(self):
        time.sleep(1)
        self.driver.tap([(75, 185)])

    # schema跳转
    def schema(self, schema):
        self.driver.get(schema)

    # 从一个元素滚动到另一个元素，两个元素必须可见
    def scroll(self, start_ele, end_ele):
        return self.driver.scroll(start_ele, end_ele)

    # 粘贴输入(英文和数字 不支持中文)
    def paste_keys(self, text):
        cmd = "adb shell input text " + text
        print(cmd)
        os.popen(cmd)

    def send_test_idlepush(self, title):
        # 测试环境
        url = 'http://push-web.staging1.p1staff.com/idlepush'
        data = {
            'uid': '116414',
            'title': title,
            'ticker': '你好',
            'link': 'tantanapp://conversations',
            'sound': '',
            'channel': '',
            'push_version': 'v1'
        }
        response = requests.get(url=url, params=data)
        return response.status_code

    def send_idlepush(self, uid, title):
        # 线上push
        url = 'https://growth-algo.p1staff.com/idlepush'
        data = {
            'uid': uid,
            'title': title,
            'ticker': '你好',
            'url': 'tantanapp://conversations',
            'sound': '',
            'push_channel': '',
            'push_grpc_version': 'v1'
        }
        cookies = get_cookies()
        response = requests.get(url=url, cookies=cookies, verify=False, params=data)
        return response.status_code

    # 执行adb shell命令
    def execute_adb_shell(self, command, serial):
        # serial = DriverYouHaoduo().android_udid
        cmd = "adb -s {serial} shell {shell_command}".format(serial=serial, shell_command=command)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) \
            .stdout.read().decode("utf-8").split('\n')

    # 执行adb命令
    def execute_adb(self, command, serial):
        # serial = DriverYouHaoduo().android_udid
        cmd = "adb -s {serial} {shell_command}".format(serial=serial, shell_command=command)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) \
            .stdout.read().decode("utf-8").split('\n')

    def use_allow(self):
        try:
            self.driver.find_element_by_xpath("//*[contains(@text, '使用')]").click()
            self.sleep(2)
        except:
            pass

    def always_allow(self):
        try:
            self.driver.find_element_by_xpath("//*[@text='始终允许']").click()
            self.sleep(2)
        except:
            pass

    def permission_forbidden(self):
        try:
            self.driver.find_element_by_xpath("//*[@text='禁止']").click()
            self.sleep(2)
        except:
            try:
                self.driver.find_element_by_xpath("//*[@text='拒绝']").click()
                self.sleep(2)
            except:
                pass
        try:
            self.driver.find_element_by_xpath("//*[@text='开启权限']")
            self.driver.swipe(300, 300, 300, 300)  # 点击任意位置关闭开启权限弹窗
        except:
            pass

    def permission_agree(self):
        try:
            self.driver.find_element_by_xpath("//*[@text='始终允许']").click()
            self.sleep(1)
        except:
            pass

    def during_use_permission_agree(self):
        try:
            self.driver.find_element_by_xpath("//*[@text='仅使用期间允许']").click()
            self.sleep(1)
        except:
            pass

    def camera_permission_agree(self, serial):
        # 小米相机权限开启方式特殊
        try:
            adb = adbOperation.ADB(serial)
            brand = adb.get_devices_manufacturer()
            # print(brand)
            self.driver.find_element_by_xpath("//*[@text='始终允许']").click()
            self.sleep(1)
        except:
            pass

    def compare_image(self, path1, path2):
        """
        对比两个图片
        Args:
            path1: 图片1路径
            path2: 图片2路径

        Returns:
            图片相似度
        """
        image1 = cv2.imread(path1)
        image2 = cv2.imread(path2)
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        score = structural_similarity(gray1, gray2)
        logger.info('图片相似度{}'.format(score))
        return score

    def compare_image_by_name(self, name1, name2):
        """
        对比两个图片
        Args:
            name1: 图片1名称，需存储在self.picture_path文件夹
            name2: 图片2名称，需存储在self.picture_path文件夹
        Usage:
            compare_image_by_name('test1.png', 'test2.png')

        Returns:
            图片相似度
        """
        return self.compare_image(path1=os.path.join(self.picture_path, name1),
                                  path2=os.path.join(self.picture_path, name2))

    def ocr_get_text(self, crop=None):
        """
        使用OCR 返回OCR结果
        Returns: OCR获取的所有文字
        """
        if crop is None:
            ol = OcrLite(img_source=(self.driver.get_screenshot_as_png()))
        else:
            base_image = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            x, y = base_image.size
            new_image = base_image.crop((int(crop[0] * x), int(crop[1] * y),
                                         int(crop[2] * x), int(crop[3] * y)))
            ol = OcrLite(img_PIL=new_image)
        return ol.detectText()

    def ocr_find_text(self, text, crop=None):
        """
        使用OCR 返回是否存在查找的文字
        Args:
            text: 要查找的问题
            crop: 是否检查部分内容 如只检查部分，crop = [x轴起始百分比， y轴起始百分比, x轴结束百分比, y轴结束百分比]
        Returns: True文字存在 False文字不存在
        """
        if crop is None:
            ol = OcrLite(img_source=self.driver.get_screenshot_as_png())
        else:
            base_image = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            x, y = base_image.size
            new_image = base_image.crop((int(crop[0] * x), int(crop[1] * y),
                                         int(crop[2] * x), int(crop[3] * y)))
            ol = OcrLite(img_PIL=new_image)
        res = ol.detectText()
        for i in res:
            if text in i['Text']:
                return True
        return False
    
    def shotscreen_find_text(self,filename, text, crop):
        """
        使用OCR 返回是否存在查找的文字
        Args:
            filename : 根据给出比例的截图
            text: 要查找的问题
            crop: 是否检查部分内容 如只检查部分，crop = [x轴起始百分比， y轴起始百分比, x轴结束百分比, y轴结束百分比]
        Returns: True文字存在 False文字不存在
        """
        if crop is None:
            ol = OcrLite(img_source=self.driver.get_screenshot_as_png())
        else:
            base_image = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            x, y = base_image.size
            new_image = base_image.crop((int(crop[0] * x), int(crop[1] * y),
                                         int(crop[2] * x), int(crop[3] * y)))
            file_path = os.path.join(self.picture_path, filename)
            new_image.save(file_path)
            ol = OcrLite(img_PIL=new_image)
        res = ol.detectText()
        for i in res:
            if text in i['Text']:
                return True
        return False

    def ocr_find_texts(self, *text):
        """
        使用OCR 返回是否存在查找的所有文字
        Args:
            *text: 要查找的文字集
        Returns: True 文字都存在 False 文字部分不存在或均不存在
        """
        ol = OcrLite(img_source=self.driver.get_screenshot_as_png())
        res = ol.detectText()
        num = len(text)
        check_text = list(text)
        for i in check_text:
            for j in res:
                if i in j['Text']:
                    num -= 1
                    res.remove(j)
                    break
        return True if num == 0 else False

    def ocr_search_text(self, text_list):
        """
        使用OCR 返回包含
        Args:
            text_list: 要查找的文字数组
        Returns: 包含查找数组的文字list, 包含文字内容'Text'和文字位置'Center'
            eg [{'Text': '要找我么？', 'Center': [111, 222]}, {'Text': '要测试么？OKK', 'Center': [80, 333]}]
            如无包含的Text则返回None
        """
        ol = OcrLite(img_source=self.driver.get_screenshot_as_png())
        res = ol.detectText()
        search_result = []
        for i in res:
            mark = True
            for single_text in text_list:
                if single_text not in i['Text']:
                    mark = False
                    break
            if mark:
                search_result.append({'Text': i['Text'], 'Center': i['Center']})
        return search_result if search_result != [] else None

    def ocr_return_text_location(self, text, position=1):
        """
        使用OCR 返回查找文字对应位置
        Args:
            text: 要查找的文字
            position: 如果查找的文字有重复，填写position可查找第position个文字。默认第一个
        Returns:
            文字中心位置x, y或无该文字时返None
        """
        ol = OcrLite(img_source=self.driver.get_screenshot_as_png())
        res = ol.detectText()
        for i in res:
            if text in i['Text']:
                if position > 1:
                    position = position - 1
                    pass
                else:
                    return i['Center']
        return

    def ocr_click_text_location(self, text, position=1):
        """
        使用OCR 点击查找文字的位置
        若没查找到文字，返False
        Args:
            text: 要查找的文字
            position: 如果查找的文字有重复，填写position可查找第position个文字。默认为第一个
        Returns:
            查找到并进行了点击 True
            未查找到 False
        """
        location = self.ocr_return_text_location(text, position)
        if not location:
            return False
        [x, y] = location
        self.offset_position_click(x, y)
        return True

    def turn_airplane_mode(self):
        """
        开启/关闭 飞行模式
        Returns: None
        """
        self.swipe_ratio(0.5, 0, 0.5, 0.7, 300)
        self.sleep(1)
        self.find(self._airplane_mode_btn).click()
        self.sleep(5)
        self.goback()

    def disagree_click(self):
        self.driver.find_element_by_xpath('//*[@text="禁止"]').click()
        self.sleep(1.5)

    def disagree_tips_click(self):
        self.driver.find_element_by_xpath('//*[@text="禁止后不再提示"]').click()
        self.sleep(1.5)

    def iknow(self):
        self.driver.find_element_by_xpath('//*[@text="开启权限"]').click()
        self.sleep(1)

    def cancel_click(self):
        self.driver.find_element_by_xpath('//*[@text="取消"]').click()
        self.sleep(1.5)

    def exist_text(self, text):
        if self.is_exist((By.XPATH, '//*[@text="{}"]'.format(text))):
            return True
        else:
            return False

    def num_to_a(self, num):
        return num_to_a(num)

