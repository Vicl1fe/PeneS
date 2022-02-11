from webbrowser import open_new


class GlobalC:
    def __init__(self):
        pass

    @staticmethod
    def brower_open(url):
        # 　url：需要打开的网址
        # 　　new：指定打开方式
        # 　　　　0：在同一个浏览器窗口中打开
        # 　　　　1：在新的浏览器窗口中打开
        # 　　　　2：新的浏览器tab会被打开
        # 　　autoraise：一般保持默认值即可
        open_new(url=url)

if __name__ == '__main__':
    GlobalC.brower_open("www.baidu.com")