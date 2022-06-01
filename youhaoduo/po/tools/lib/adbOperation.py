# -*- coding: utf-8 -*-
import platform
import subprocess
import re
import traceback
from time import sleep
import random
from po import config

system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class ADB(object):
    """
    单个设备，可不传入参数device_id
    """
    def __init__(self, serial):
        self.device_id = " -s %s" % serial
        self.adb_path = "adb"

    def adb(self, args):

        cmd = "%s %s %s" % (self.adb_path, self.device_id, str(args))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def shell(self, args):

        cmd = "%s %s shell %s" % (self.adb_path, self.device_id, str(args),)
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def minicap_screen_shot(self, path):
        vm_size, stderr = self.shell('wm size').communicate()
        vm_size = str(vm_size, encoding='utf-8').split(":")[1].strip()
        # stdout, stderr = self.shell('"LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0 -s > /data/local/tmp/temp.png"').communicate()
        cmd = 'LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}@{}/0 -s > {}'.format(vm_size, vm_size, path)
        stdout, stderr = self.shell(cmd).communicate()
        # print ("minicap_screen_shot ========", stdout, stderr)
        # self.pull("/data/local/tmp/temp.png", path)

    def check_file(self, file_path):
        stdout, stderr = self.shell("ls {path}".format(path=file_path)).communicate()
        print (stderr, stdout)
        if "No such file or directory" in stdout or stderr:
            return False
        return True

    def install_from_local(self, path):
        self.shell("pm install %s" % path).communicate()

    def get_devices_manufacturer(self):
        try:
            stdout, _ = self.shell("getprop ro.product.manufacturer").communicate()
            return stdout.decode()
        except Exception as e:
            print(e)
            return None

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").stdout.read().strip()

    def get_device_id(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def get_android_version(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        try:
            build_version, _ = self.shell("getprop ro.build.version.release").communicate()
            return build_version
        except Exception as e:
            print(e)
            return 0

    def get_sdk_version(self):
        """
        获取设备SDK版本号
        """
        try:
            sdk_version, _ = self.shell("getprop ro.build.version.sdk").communicate()
            return sdk_version.strip()
        except Exception as e:
            print(e)
            return None

    def get_device_model(self):
        """
        获取设备型号
        """
        try:
            model, _ = self.shell("getprop ro.product.model").communicate()
            return model
        except Exception as e:
            print(e)
            return ""

        # return self.shell("getprop ro.product.model").stdout.read().strip()
    
    def get_pids(self, package_name):
        pid, _ = self.shell("ps |{find} {pkg_name}".format(find=config.FIND_UTIL,
                                                           pkg_name=package_name)).communicate()
        if not pid:
            pid, _ = self.shell("ps -ef|{find} {pkg_name}".format(find=config.FIND_UTIL,
                                                                  pkg_name=package_name)).communicate()
        return [re.split(r"\s+", line)[1] for line in pid.splitlines() if package_name in re.split(r"\s+", line)]

    
    def get_pid(self, package_name):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        pid, _ = self.shell("ps |{find} {pkg_name}".format(find=config.FIND_UTIL,
                                                           pkg_name=package_name)).communicate()
        if not pid:
            pid, _ = self.shell("ps -ef|{find} {pkg_name}".format(find=config.FIND_UTIL,
                                                                  pkg_name=package_name)).communicate()

        for line in pid.splitlines():
            split_line = re.split(r"\s+", line)
            if split_line[-1] == package_name:
                return split_line[1]

        # return [re.split(r"\s+", line)[1] for line in pid.splitlines() if
        #         re.split(r"\s+", line)[-1] == package_name].pop()

    def get_uid(self, package_name):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        try:
            uid, _ = self.shell("ps |{find} {pkg_name}".format(find=config.FIND_UTIL, pkg_name=package_name)).communicate()
            if not uid:
                uid, _ = self.shell("ps -ef|{find} {pkg_name}".format(find=config.FIND_UTIL, pkg_name=package_name)).communicate()
                if not uid:
                    return None
            # print uid
            uid_list = [re.split(r"\s+", line)[0] for line in uid.splitlines() if re.split(r"\s+", line)[-1] == package_name].pop()
            return int(uid_list.partition("u0_a")[-1])+10000
        except Exception as e:
            print(e)
            return None

    def netstat(self, port):
        out = None
        if system is "Windows":
            out = self.shell("netstat |findstr %s" % port).stdout.read().strip()

        else:
            out = self.shell("netstat |grep %s" % port).stdout.read().strip()
        return out

    def kill_process(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.shell("kill %s" %
                              str(pid)).stdout.read().split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell("kill %s" %
                              str(pid)).stdout.read().split(": ")[-1]

    def quit_app(self, package_name):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        self.shell("am force-stop %s" % package_name).communicate()

    def get_focused_package_and_activity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        apilevel = int(self.get_api_level())
        a = []
        i = 0
        if apilevel < 26:
            while len(a) < 4 and i < 100:
                out, _ = self.shell(
                    "dumpsys activity activities | %s mFocusedActivity" %
                    find_util).communicate()
                a = out.strip().split(' ')
                i = i + 1
            if len(a) < 4:
                return ' / '
            out = out.strip().split(' ')[3]
        else:
            while len(a) < 4 and i < 100:
                out, _ = self.shell(
                    "dumpsys activity activities | %s ResumedActivity" %
                    find_util).communicate()
                a = out.strip().split(' ')
                i = i + 1
            if len(a) < 4:
                return ' / '
            out = out.strip().split(' ')[3]

        return out

    def get_current_package_name(self):
        """
        获取当前运行的应用的包名
        """
        return self.get_focused_package_and_activity().split("/")[0]

    def get_current_activity(self):
        """
        获取当前运行应用的activity
        """
        return self.get_focused_package_and_activity().split("/")[-1]

    def get_battery_level(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" %
                           find_util).stdout.read().split(": ")[-1]

        return int(level)

    def get_backstage_services(self, page_name):
        """

        :return: 指定应用后台运行的services
        """
        services_list = []
        for line in self.shell(
                        'dumpsys activity services %s' %
                        page_name).stdout.readlines():
            if line.strip().startswith('intent'):
                service_name = line.strip().split('=')[-1].split('}')[0]
                if service_name not in services_list:
                    services_list.append(service_name)

        return services_list

    def get_current_backstage_services(self):
        """

        :return: 当前应用后台运行的services
        """
        package = self.get_current_package_name()
        return self.get_backstage_services(package)

    def get_battery_status(self):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        status_dict = {1: "BATTERY_STATUS_UNKNOWN",
                       2: "BATTERY_STATUS_CHARGING",
                       3: "BATTERY_STATUS_DISCHARGING",
                       4: "BATTERY_STATUS_NOT_CHARGING",
                       5: "BATTERY_STATUS_FULL"}
        status = self.shell("dumpsys battery | %s status" %
                            find_util).stdout.read().split(": ")[-1]

        return status_dict[int(status)]

    def get_battery_temp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" %
                          find_util).stdout.read().split(": ")[-1]

        return int(temp) / 10.0

    def get_screen_resolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        try:
            out, _ = self.shell("dumpsys display | %s DisplayDeviceInfo" % find_util).communicate()
            pattern = re.compile(r"\d+")
            display = pattern.findall(out)
            return "{high}x{width}".format(high=display[2], width=display[1])
        except Exception as e:
            print(e)
            return None


    def reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def fast_boot(self):
        """
        进入fastboot模式
        """
        self.adb("reboot bootloader")

    def get_system_app_list(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp

    def get_third_app_list(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp

    def get_matching_app_list(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.shell(
                        "pm list packages %s" %
                        keyword).stdout.readlines():
            matApp.append(packages.decode().split(":")[-1].splitlines()[0])

        return matApp

    def get_app_start_total_time(self, component):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s | %s TotalTime" %
                          (component, find_util)).stdout.read().split(": ")[-1]
        return int(time)

    def get_api_level(self):
        try:
            stdout, _ = self.shell('getprop ro.build.version.sdk').communicate()
            api_level = int(stdout.decode().strip())
            return api_level
        except Exception as e:
            print(e)
            return 0

    def install_app(self, app_file):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("/Users/joko/Downloads/1.apk")
        INSTALL_FAILED_ALREADY_EXISTS	应用已经存在，或卸载了但没卸载干净	adb install 时使用 -r 参数，或者先 adb uninstall <packagename> 再安装
        INSTALL_FAILED_INVALID_APK	无效的 APK 文件
        INSTALL_FAILED_INVALID_URI	无效的 APK 文件名	确保 APK 文件名里无中文
        INSTALL_FAILED_INSUFFICIENT_STORAGE	空间不足	清理空间
        INSTALL_FAILED_DUPLICATE_PACKAGE	已经存在同名程序
        INSTALL_FAILED_NO_SHARED_USER	请求的共享用户不存在
        INSTALL_FAILED_UPDATE_INCOMPATIBLE	以前安装过同名应用，但卸载时数据没有移除	先 adb uninstall <packagename> 再安装
        INSTALL_FAILED_SHARED_USER_INCOMPATIBLE	请求的共享用户存在但签名不一致
        INSTALL_FAILED_MISSING_SHARED_LIBRARY	安装包使用了设备上不可用的共享库
        INSTALL_FAILED_REPLACE_COULDNT_DELETE	替换时无法删除
        INSTALL_FAILED_DEXOPT	dex 优化验证失败或空间不足
        INSTALL_FAILED_OLDER_SDK	设备系统版本低于应用要求
        INSTALL_FAILED_CONFLICTING_PROVIDER	设备里已经存在与应用里同名的 content provider
        INSTALL_FAILED_NEWER_SDK	设备系统版本高于应用要求
        INSTALL_FAILED_TEST_ONLY	应用是 test-only 的，但安装时没有指定 -t 参数
        INSTALL_FAILED_CPU_ABI_INCOMPATIBLE	包含不兼容设备 CPU 应用程序二进制接口的 native code
        INSTALL_FAILED_MISSING_FEATURE	应用使用了设备不可用的功能
        INSTALL_FAILED_CONTAINER_ERROR	sdcard 访问失败	确认 sdcard 可用，或者安装到内置存储
        INSTALL_FAILED_INVALID_INSTALL_LOCATION	不能安装到指定位置	切换安装位置，添加或删除 -s 参数
        INSTALL_FAILED_MEDIA_UNAVAILABLE	安装位置不可用	一般为 sdcard，确认 sdcard 可用或安装到内置存储
        INSTALL_FAILED_VERIFICATION_TIMEOUT	验证安装包超时
        INSTALL_FAILED_VERIFICATION_FAILURE	验证安装包失败
        INSTALL_FAILED_PACKAGE_CHANGED	应用与调用程序期望的不一致
        INSTALL_FAILED_UID_CHANGED	以前安装过该应用，与本次分配的 UID 不一致	清除以前安装过的残留文件
        INSTALL_FAILED_VERSION_DOWNGRADE	已经安装了该应用更高版本	使用 -d 参数
        INSTALL_FAILED_PERMISSION_MODEL_DOWNGRADE	已安装 target SDK 支持运行时权限的同名应用，要安装的版本不支持运行时权限
        INSTALL_PARSE_FAILED_NOT_APK	指定路径不是文件，或不是以 .apk 结尾
        INSTALL_PARSE_FAILED_BAD_MANIFEST	无法解析的 AndroidManifest.xml 文件
        INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION	解析器遇到异常
        INSTALL_PARSE_FAILED_NO_CERTIFICATES	安装包没有签名
        INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES	已安装该应用，且签名与 APK 文件不一致	先卸载设备上的该应用，再安装
        INSTALL_PARSE_FAILED_CERTIFICATE_ENCODING	解析 APK 文件时遇到 CertificateEncodingException
        INSTALL_PARSE_FAILED_BAD_PACKAGE_NAME	manifest 文件里没有或者使用了无效的包名
        INSTALL_PARSE_FAILED_BAD_SHARED_USER_ID	manifest 文件里指定了无效的共享用户 ID
        INSTALL_PARSE_FAILED_MANIFEST_MALFORMED	解析 manifest 文件时遇到结构性错误
        INSTALL_PARSE_FAILED_MANIFEST_EMPTY	在 manifest 文件里找不到找可操作标签（instrumentation 或 application）
        INSTALL_FAILED_INTERNAL_ERROR	因系统问题安装失败
        INSTALL_FAILED_USER_RESTRICTED	用户被限制安装应用
        INSTALL_FAILED_DUPLICATE_PERMISSION	应用尝试定义一个已经存在的权限名称
        INSTALL_FAILED_NO_MATCHING_ABIS	应用包含设备的应用程序二进制接口不支持的 native code
        INSTALL_CANCELED_BY_USER	应用安装需要在设备上确认，但未操作设备或点了取消	在设备上同意安装
        INSTALL_FAILED_ACWF_INCOMPATIBLE	应用程序与设备不兼容
        does not contain AndroidManifest.xml	无效的 APK 文件
        is not a valid zip file	无效的 APK 文件
        Offline	设备未连接成功	先将设备与 adb 连接成功
        unauthorized	设备未授权允许调试
        error: device not found	没有连接成功的设备	先将设备与 adb 连接成功
        protocol failure	设备已断开连接	先将设备与 adb 连接成功
        Unknown option: -s	Android 2.2 以下不支持安装到 sdcard	不使用 -s 参数
        No space left on devicerm	空间不足	清理空间
        Permission denied ... sdcard ...	sdcard 不可用
        """
        # for line in self.adb("install -r %s" % app_file).stdout.readlines():
        #     if 'Failure' in line:
        #         print line.strip()
        # return self.adb('install -r -g "%s"' % app_file)
        api_level = 22
        # 5.1 API level 22
        if int(self.get_api_level()) > api_level:
            return self.adb('install -r "%s"' % app_file)
        else:
            return self.adb('install -r "%s"' % app_file)

    def is_install(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        if self.get_matching_app_list(packageName):
            return True
        else:
            return False

    def remove_app(self, pkg_name):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        """
        print(self.shell("pm uninstall %s" % pkg_name).communicate())
        print(self.shell("pm clear %s " % pkg_name).communicate())

    def clear_app_data(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.shell(
                        "pm clear %s" %
                        packageName).stdout.read().splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def reset_current_app(self):
        """
        重置当前应用
        """
        packageName = self.get_current_package_name()
        component = self.get_focused_package_and_activity()
        self.clear_app_data(packageName)
        self.start_activity(component)

    def get_app_install_path(self, path_name):
        """
        获取第三方应用安装地址
        :return:
        """
        try:
            stdout, stderr = self.shell("pm path %s" % path_name).communicate()
            return stdout
        except Exception as e:
            print (e.message)
            print (traceback)

    def pull_install_app(self, save_path):
        """
        获取当前Android设备第三方应用包，并且pull到本地
        :param save_path: 存放路径
        :return:
        """
        for app_package_name in self.get_third_app_list():
            install_app_path = self.get_app_install_path(app_package_name)
            self.pull(install_app_path, save_path + '/' + app_package_name + '.apk')

    def start_activity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        return self.shell("am start -n %s" % component).communicate()

    def restart_activity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        self.shell("am start -R 1 %s" % component)

    def start_web_page(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        self.shell("am start -a android.intent.action.VIEW -d %s" % url)

    def call_phone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        self.shell(
            "am start -a android.intent.action.CALL -d tel:%s" %
            str(number))

    def send_key_event(self, keycode):
        """
        发送一个按键事件
        args:
        - keycode -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(keycode.HOME)
        """
        self.shell("input keyevent %s" % str(keycode))
        sleep(0.5)

    def long_press_key(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(keycode.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(keycode))
        sleep(0.5)

    def touch(self, e=None, x=None, y=None):
        """
        触摸事件
        usage: touch(e), touch(x=0.5,y=0.5)
        """
        width, high = self.get_screen_resolution()
        if (e is not None):
            x = e[0]
            y = e[1]
        if (0 < x < 1):
            x = x * width
        if (0 < y < 1):
            y = y * high

        self.shell("input tap %s %s" % (str(x), str(y)))
        sleep(0.5)

    def get_focused_package_xml(self, save_path):
        file_name = random.randint(10, 99)
        print("dump xml: ", self.shell('uiautomator dump /data/local/tmp/{}.xml'.format(file_name)).communicate())
        print("push xml: ", self.adb('pull /data/local/tmp/{}.xml {}'.format(file_name, save_path)).communicate())

    def touch_by_element(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))
        sleep(0.5)

    def touch_by_ratio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        self.shell("input tap %s %s" %
                   (str(ratioWidth *
                        self.get_screen_resolution()[0]), str(ratioHigh *
                                                              self.get_screen_resolution()[1])))
        sleep(0.5)

    def swipe_by_coord(self, start_x, start_y, end_x, end_y, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(start_x),
             str(start_y),
             str(end_x),
             str(end_y),
             str(duration)))
        sleep(0.5)

    def swipe(
            self,
            e1=None,
            e2=None,
            start_x=None,
            start_y=None,
            end_x=None,
            end_y=None,
            duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        width, high = self.get_screen_resolution()
        if (e1 is not None):
            start_x = e1[0]
            start_y = e1[1]
        if (e2 is not None):
            end_x = e2[0]
            end_y = e2[1]
        if (0 < start_x < 1):
            start_x = start_x * width
        if (0 < start_y < 1):
            start_y = start_y * high
        if (0 < end_x < 1):
            end_x = end_x * width
        if (0 < end_y < 1):
            end_y = end_y * high

        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(start_x),
             str(start_y),
             str(end_x),
             str(end_y),
             str(duration)))
        sleep(0.5)

    def swipe_by_ratio(
            self,
            start_ratioWidth,
            start_ratioHigh,
            end_ratioWidth,
            end_ratioHigh,
            duration=" "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        x_point, y_point = self.get_screen_resolution()
        self.shell("input swipe %s %s %s %s %s" %
                   (str(start_ratioWidth *
                        x_point), str(start_ratioHigh *
                                      y_point), str(end_ratioWidth *
                                                    x_point), str(end_ratioHigh *
                                                                  y_point), str(duration)))
        sleep(0.5)

    def swipe_to_left(self):
        """
        左滑屏幕
        """
        self.swipe_by_ratio(0.8, 0.5, 0.2, 0.5)

    def swipe_to_right(self):
        """
        右滑屏幕
        """
        self.swipe_by_ratio(0.2, 0.5, 0.8, 0.5)

    def swipe_to_up(self):
        """
        上滑屏幕
        """
        self.swipe_by_ratio(0.5, 0.8, 0.5, 0.2)

    def swipe_to_down(self):
        """
        下滑屏幕
        """
        self.swipe_by_ratio(0.5, 0.2, 0.5, 0.8)

    def long_press(self, e=None, x=None, y=None):
        """
        长按屏幕的某个坐标位置, Android 4.4
        usage: longPress(e)
               longPress(x=0.5, y=0.5)
        """
        self.swipe(
            e1=e,
            e2=e,
            start_x=x,
            start_y=y,
            end_x=x,
            end_y=y,
            duration=2000)

    def long_press_element(self, e):
        """
       长按元素, Android 4.4
        """
        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(
                e[0]), str(
                e[1]), str(
                e[0]), str(
                e[1]), str(2000)))
        sleep(0.5)

    def long_press_by_ratio(self, ratio_width, ratio_high):
        """
        通过比例长按屏幕某个位置, Android.4.4
        usage: longPressByRatio(0.5, 0.5) 长按屏幕中心位置
        """
        self.swipe_by_ratio(
            ratio_width,
            ratio_high,
            ratio_width,
            ratio_high,
            duration=2000)

    def screen_shot(self, appPath):
        """
        获取当前设备的截图,导出到指定目录
        """
        self.shell("screencap -p /sdcard/temp.png").communicate()
        self.adb("pull /sdcard/temp.png %s" % appPath).communicate()


    def version_name(self):
        """
        查询当前屏幕应用版本
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'versionName' in package:
                return package.split('=', 2)[1].strip()

    def specifies_app_version_name(self, package):
        """
        获取指定应用的versionName
        :param package:应用包名
        :return: 包名,versionName
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        package).stdout.readlines():
            if 'versionName' in package:
                return package.split('=', 2)[1].strip()

    def version_code(self):
        """
        查询当前屏幕应用versionCode
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'versionCode' in package:
                return package.split('=', 2)[1].split(' ', 2)[0]

    def first_install_time(self):
        """
        查询当前屏幕应用安装时间
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'firstInstallTime' in package:
                return package.split('=', 2)[1].strip()

    def last_update_time(self):
        """
        查询当前屏幕应用安装更新时间
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'lastUpdateTime' in package:
                return package.split('=', 2)[1].strip()

    def wifi_name(self):
        """
        查询连接wifi名称
        """
        for package in self.shell('dumpsys wifi').stdout.readlines():
            if package.startswith('mWifiInfo'):
                wifi_name = re.findall(r'SSID:([^"]+), BSSID', package)
                if not wifi_name:
                    return None
                else:
                    return wifi_name[0].strip()

    def get_network_state(self):
        """
        设备是否连上互联网
        :return:
        """
        if 'unknown' in self.shell('ping -w 1 www.baidu.com').stdout.readlines()[0]:
            return False
        else:
            return True

    def get_cpu(self, package_name):
        """
        获取当前cpu百分比
        """
        p = self.shell(
            "top -n 1 -d 0.5 | grep %s | awk '{print $3}' " %
            package_name)

        stdoutput, erroroutput = p.communicate()
        cpulist = stdoutput.split()
        cputotal = 0
        for item in cpulist:
            cputotal += float(item.strip('%'))
        return int(cputotal)

    def get_cpu_time(self):
        p = self.shell('cat /proc/stat|{} "cpu "'.format(find_util))
        stdoutput, erroroutput = p.communicate()    
        total_time = 0      
        if stdoutput:
            nums = stdoutput.split("\n")
            for item in nums[0].split():
                if item.isdigit():
                    total_time += int(item)

        return total_time


    def __mem_pss(self, package_name):
        """
        获取当前应用内存
        """
        p = self.shell(
            'top -n 1 -d 0.5 | %s %s' %
            (find_util, package_name))
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r.endswith(package_name):
                lst = [mem for mem in r.split(' ') if mem]
                return int(lst[6].split('K')[0])

    def get_related_pid(self, package_name):
        """
        获得app相关的所有进程的列表列表
        :return:
        """
        if system is "Windows":
            pidinfo = self.shell(
                "ps |findstr %s" %
                package_name).stdout.read()
        else:
            pidinfo = self.shell(
                "ps |%s %s" %
                (find_util, package_name)).stdout.read()
        if pidinfo == '':
            if system is "Windows":
                pidinfo = self.shell(
                    "ps -ef|findstr %s" %
                    package_name).stdout.read()
            else:
                pidinfo = self.shell(
                    "ps -ef|%s %s" %
                    (find_util, package_name)).stdout.read()
     
        if pidinfo == '':
            return None

        pidList = []
        pidinfo = pidinfo.strip().split("\n")
        for item in pidinfo:
            ss = item.split()
            if ss[1].isdigit():
                pidList.append(int(ss[1]))
        return pidList

        # pattern = re.compile(r"\d+")
        # result = pidinfo.split(" ")
        # result.remove(result[0])
        # print "get_pid", pattern.findall(" ".join(result))[0]

        # return pattern.findall(" ".join(result))[0]
        # p = self.shell('ps |{} {}'.format(find_util,package_name) + "|awk '{print $2}'")
        # stdoutput, erroroutput = p.communicate()
        # return stdoutput.split()

    def get_pid_status(self, pid):
        """
        获得Android系统的某个进程的cpu快照信息
        :return:
        """
        p = self.shell('cat /proc/{}/status'.format(pid))
        stdoutput, erroroutput = p.communicate()
        return stdoutput

    def get_cpu_shot(self, pid):
        """
        获得Android系统的目录文件/proc/pid/status下的uid信息
        :return:
        """
        p = self.shell('cat /proc/{}/stat'.format(pid))
        stdoutput, erroroutput = p.communicate()
        return stdoutput

    def get_flow_rcv(self, uid):
        '''
        Android系统的目录文件/proc/uid_stat/uid/下一般会有两个文件tcp_rcv，可获得下行流量。
        :return:
        '''
        p = self.shell("cat /proc/uid_stat/{}/tcp_rcv".format(uid))
        stdoutput, erroroutput = p.communicate()
        return int(stdoutput)

    def get_flow_cmd(self,pid):
        p= self.shell("cat /proc/{}/net/dev".format(pid))
        stdoutput, erroroutput = p.communicate()
        flow1 ={}
        flow1['ReceiveBytes'] = 0
        flow1['TransitBytes'] = 0
        if stdoutput:
            wlan0_rcv_bytes = re.findall(r'wlan0:.*',stdoutput)
            gprs_rcv_bytes = re.findall(r'gprs:.*',stdoutput)
            if wlan0_rcv_bytes:
                wlan0_rcv_bytes = wlan0_rcv_bytes[0].split()
                if wlan0_rcv_bytes[1].isdigit():
                    flow1['ReceiveBytes']+=int(wlan0_rcv_bytes[1])
                if wlan0_rcv_bytes[9].isdigit():
                    flow1['TransitBytes']+=int(wlan0_rcv_bytes[9])
            if gprs_rcv_bytes:
                gprs_rcv_bytes=gprs_rcv_bytes[0].split()
                if gprs_rcv_bytes[1].isdigit():
                    flow1['ReceiveBytes']+=int(gprs_rcv_bytes[1])
                if gprs_rcv_bytes[9].isdigit():
                    flow1['TransitBytes']+=int(gprs_rcv_bytes[9])

        return flow1

    def get_flow_snd(self, uid):
        '''
        获得Android系统的目录文件/proc/uid_stat/uid/下有个文件tcp_snd，可以获得上行流量。
        :return:
        '''
        p= self.shell("cat /proc/uid_stat/{}/tcp_snd".format(uid))
        stdoutput, erroroutput = p.communicate()
        return int(stdoutput)

    def get_cpu_kel(self):
        """
        查看被测试的设备中的cpu核数
        :return: CPU核的数量
        """
        p = self.shell("cat /proc/cpuinfo|{} processor".format(find_util))
        stdoutput, erroroutput =p.communicate()
        cpu_num=0
        if stdoutput:
            kelList = re.findall(r'\d+',stdoutput)
            for item in kelList:
                if item.isdigit():
                    cpu_num+=int(item)
        else:
            return None

        return (cpu_num)

    def get_mem_info(self, package_name):
        '''
        获得内存信息，主要是内存中的Dalvik Heap的pss total值和Heap Alloc的值,单位是KB
        1、获得Heap Alloc的值
        2、获得应用app相关的pid的列表,计算每个pid所用的内存的值
        :return:
        '''
        pssval = heapAlloc = pss_total = 0
        ##获得应用app相关的pid的列表
        app_pids = self.get_related_pid(package_name)
        if not app_pids:
            return None
        try:
            for item in app_pids:
                p = self.shell("dumpsys meminfo {}".format(item))
                stdoutput, erroroutput = p.communicate()
                if stdoutput:
                    des_str = re.findall(r"Dalvik Heap.*",stdoutput)
                    if des_str:
                        pssval += int(des_str[0].split()[2])
                        heapAlloc += int(des_str[0].split()[7])
                    total_str=re.findall(r"TOTAL\s+\d+",stdoutput)
                    if total_str:
                        pss_total += int(total_str[0].split()[1])

            return pssval/1024, heapAlloc/1024, pss_total/1024
        except Exception as e:
            return None

    def fill_disk(self):
        """
        填满手机磁盘，需root
        """
        self.shell('dd if=/dev/zero of=/mnt/sdcard/bigfile')

    def del_fill_disk(self):
        """
        删除填满磁盘的大文件
        """
        self.shell('rm -r /mnt/sdcard/bigfile')

    def backup_apk(self, package_name, path):
        """
        备份应用与数据
        - all 备份所有
        -f 指定路径
        -system|-nosystem
        -shared 备份sd卡
        """
        self.adb(
            'backup -apk %s -f %s/mybackup.ab' %
            (package_name, path))

    def restore_apk(self, path):
        """
        恢复应用与数据
        - all 备份所有
        -f 指定路径
        -system|-nosystem
        """
        self.adb('restore %s' % path)

    def clear_log_cat(self):
        """
        :return: 清理缓存中的log
        """
        return self.adb('logcat -c').communicate()

    def log_cat(self, log_path):
        return self.adb('logcat -v time >%s&' % log_path)

    def strict_mode_log_cat(self, log_path):
        return self.adb('logcat -v time -s StrictMode:D > %s&' % log_path)

    def leak_canary_log_cat(self, log_path):
        return self.adb('logcat -v time -s LeakCanary:D > %s&' % log_path)

    def err_log_cat(self, log_path):
        self.clear_log_cat()
        return self.adb('logcat -v time -s AndroidRuntime:E ActivityManager:E DEBUG:F ANRManager:E AEE/DEBUG:F >%s&' % log_path)

    def stop_log(self):
        stdout, _ = self.shell("ps |%s logcat" % config.FIND_UTIL).communicate()
        try:
            while stdout.decode().strip():
                pid = re.split("\s+", stdout.decode().strip())[1]
                print("pidNum", pid)
                self.shell("kill -10 %s" % pid)
                stdout, _ = self.shell("ps |%s logcat" % config.FIND_UTIL).communicate()
        except Exception as e:
            print(e)

    def get_cpu_version(self):
        """
        获取cpu基带版本）
        :return: arm64-v8a
        """
        try:
            abi, _ = self.shell("getprop ro.product.cpu.abi").communicate()
            return abi
        except Exception as e:
            print(e)
            return None

    def get_cpu_version_list(self):
        """
        获取cpu基带版本）
        :return: arm64-v8a
        """
        try:
            abi, _ = self.shell("getprop ro.product.cpu.abilist").communicate()
            return abi.strip().split(",")
        except Exception as e:
            print(e)
            return None

    def pull(self, remote_file, local_file):
        """

        :param remote_file: 拉取文件地址
        :param local_file: 存放文件地址
        :return:
        """
        return self.adb('pull %s %s' % (remote_file, local_file)).communicate()

    def push(self, local_file, remote_file):
        """

        :param remote_file: 目标存放文件地址
        :param local_file: 推送文件原地址
        :return:
        """

        return self.adb('push %s %s' % (local_file, remote_file)).communicate()

    def rm(self, remote_file):
        """

        :param remote_file: 删除文件地址
        :return:
        """
        return self.shell("rm -r %s" % remote_file).communicate()

    def rm_sdcard_file(self, remote_file):
        """

        :param remote_file: sdcard文件路径
        :return:
        """
        self.rm("rm -r /sdcard/%s" % remote_file)


    def clean_directory(self, dir):
        """

        :param dir: 传入的路径
        :return: 清空指定目录
        """
        self.shell("rm -rf "+dir)
        self.shell("mkdir -p "+dir)

    def mk_dir(self, directory):
        self.shell("mkdir -p " + directory).communicate()
        return self.check_directory_exist(directory)

    def upload_file_todir(self, directory, apk_path, filename):
        if self.mk_dir(directory):
            print("upload_file_todir:", u"文件夹创建成功", directory+filename)
            std, _ = self.push(apk_path, directory+filename)
            return self.check_file(directory+filename)
        return False

    def check_directory_exist(self, directory):
        stdout, stderr = self.shell("cd {dir_path}".format(dir_path=directory)).communicate()
        print("check_directory_exist: ", stdout, stderr)
        # 目录不存在
        # stderr 不为空
        if 'No such file or directory' in stdout.decode() or stderr.decode():
            return False
        else:
            return True


if __name__ == "__main__":
    a = ADB("NAB0220317000292")
    a.minicap_screen_shot('./abb.png')