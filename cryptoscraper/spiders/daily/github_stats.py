import json
import scrapy
from posixpath import join as join_paths
from urllib.parse import urljoin, urlparse, parse_qs
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
        '''
        - Method used to construct a github api url that is meant to get all the commmits 
          tied to a specific url
        - This method takes the a url in the form /owner/repo/ and creates a full github api url
        '''          
        api_base_url = 'https://api.github.com'
        repo_path = join_paths('repos',urlparse(repo).path.lstrip('/'), 'commits?per_page=1')
        api_url = urljoin(api_base_url,repo_path)
        return api_url

    def construct_github_repo_url(self, repo):
        api_base_url='https://api.github.com'
        repo_path=join_paths('repos',urlparse(repo).path.lstrip('/'))
        api_url = urljoin(api_base_url,repo_path)
        return api_url

    def github_next_url(self,link_data):
        '''
        - Returns a github API url from the header data that is returned from a github request
        - The Url is the page url for api's that return multi pages.
        '''
        if link_data is not None:
            data=link_data.decode("utf-8")
            links=data.split(',')

            for link in links:
                if 'rel="next"' in link:
                    return {'next_status': True,'url':link[link.find("<")+1:link.find(">")]}

        return {'next_status': False}

    def get_item_num(self, link):
        if link is not None:
            data=link.decode("utf-8")
            links=data.split(',')

            for item in links:
                if 'rel="last"' in item:
                    url=item[item.find("<")+1:item.find(">")]
                    parsed=urlparse(url)
                    return parse_qs(parsed.query)['page'][0]


    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/developer_tab".format(coin)
        	yield response.follow(url, callback=self.get_github_stats, meta={'data_coin_id':int(coin)})

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_github_stats(self, response):
        '''
        - Retrieves initial commit data from coingeck developer tab.
        - Passes on repo_name and url to get-initial_git_data to get the rest of the data.
        '''
        data = GithubStatsItem()
        data['data_coin_id'] = response.meta['data_coin_id']
        for github in response.css('div.card-block'):
            data['repo_name'] = github.css('span.text-xl a::text').get()
            data['url'] = github.css('span.text-xl a::attr(href)').get()
            # data['stars'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[0].get())
            # data['watchers'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[1].get())
            # data['forks'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[2].get())
            data['contributors'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[3].get())
            data['merged_pr'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[4].get())
            data['issues'] = sanitize_string(github.css('div.pt-2.pb-2.font-light::text')[5].get())

            url=self.construct_github_repo_url(data['url'])
            yield scrapy.Request(url=url,
                                headers=self.headers,
                                callback=self.get_initial_git_data,
                                meta={'data':data})

    def get_initial_git_data(self, response):
        '''
        - Gets forks,stars ad watchers numbers from github repo API endpoint.
        '''
        data=response.meta['data']
        if response.status!= 404:
            git_data = json.loads(response.body)
            data['forks']=git_data['forks_count']
            data['stars']=git_data['stargazers_count']
            data['watchers']=git_data['subscribers_count']
        else:
            data['forks']=None
            data['stars']=None   
            data['watchers']=None         

        url = self.construct_github_api_url(data['url'])
        yield scrapy.Request(url=url,
                                headers=self.headers,
                                callback=self.get_github_commits, 
                                meta={'data':data})

    def get_github_commits(self, response):
        '''
        - Gets a repo's total number of commits.
        '''
        data = response.meta['data']
        if response.status != 404:
            link = response.headers.get('Link', None)
            data['commits']=self.get_item_num(link)
            yield data
        else:
            data['commits']=None
            yield data

