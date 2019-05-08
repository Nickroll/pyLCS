# /usr/bin/env python


from pyLCS import liquidCrawler, matchCrawler, saveJSON

lc = liquidCrawler.liquidCrawler(region='na', year=2019, split='spring', playoffs=False)
mls = lc.match_links(render=True)

mc = matchCrawler.postMatchCrawl(mls[:2])
json_data = mc.download_json_data()

print(saveJSON.flatten_json(json_data))
