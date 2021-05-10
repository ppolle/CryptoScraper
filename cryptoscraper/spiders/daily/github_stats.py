import json
import scrapy
from posixpath import join as join_paths
from urllib.parse import urljoin, urlparse
from cryptoscraper.items import GithubStatsItem
from cryptoscraper.utils import get_num, sanitize_string

class GithubStatsSpider(scrapy.Spider):
    name = 'github_stats'
    start_urls = ['http://www.coingecko.com/en/']
    handle_httpstatus_list = [404]
    headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token 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',
                }

    def construct_github_api_url(self, repo):           
        api_base_url = 'https://api.github.com'
        repo_path = join_paths('repos',urlparse(repo).path.lstrip('/'), 'commits?per_page=100')
        api_url = urljoin(api_base_url,repo_path)
        return api_url

    def github_next_url(self,link_data):
        #decode byte code into a string
        if link_data is not None:
            data=link_data.decode("utf-8")
            links=data.split(',')

            for link in links:
                if 'rel="next"' in link:
                    return {'next_status': True,'url':link[link.find("<")+1:link.find(">")]}

        return {'next_status': False}

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/developer_tab".format(coin)
        	yield response.follow(url, callback=self.get_github_stats, meta={'data_coin_id':int(coin)})

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_github_stats(self, response):
        data = GithubStatsItem()
        data['data_coin_id'] = response.meta['data_coin_id']
        for github in response.css('div.card-block'):
            data['repo_name'] = github.css('span.text-xl a::text').get()
            data['url'] = github.css('span.text-xl a::attr(href)').get()
            data['stars'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[0].get())
            data['watchers'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[1].get())
            data['forks'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[2].get())
            data['contributors'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[3].get())
            data['merged_pr'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[4].get())
            data['issues'] = sanitize_string(github.css('div.pt-2.pb-2.font-light::text')[5].get())

            url = self.construct_github_api_url(data['url'])
            print(url)
            yield scrapy.Request(url=url,
                                headers=self.headers,
                                callback=self.get_github_commits, 
                                meta={'data':data})

    def get_github_commits(self, response):
        data = response.meta['data']
        if response.status != 404:
            commits = json.loads(response.body)
            total_commits = len(commits)
            link = response.headers.get('Link', None)
            
            if 'commits' in data.keys():
                data['commits'] = data['commits'] + total_commits
            else:
                data['commits'] = total_commits

            url = self.github_next_url(link)
            if link is not None and url['next_status'] is True:
                yield scrapy.Request(url=url['url'],
                                    headers=self.headers,
                                    callback=self.get_github_commits,
                                    meta={'data':data})
            else:
                yield data

        else:
            data['commits'] = 0
            yield data

