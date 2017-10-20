from Crawler import Crawler

site_url = 'http://nlotto.co.kr/gameResult.do?method=byWin&drwNo='
crawler = Crawler()
crawler.get_lucky(site_url)


