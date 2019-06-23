from selenium import webdriver


def spider(url='https://baidu.com'):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    d = webdriver.Chrome('/home/sunny/wx/LOLGokEnv/chromedriver', chrome_options=chrome_options)
    d.get(url)
    print(d.page_source)


spider()
