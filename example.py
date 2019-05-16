# /usr/bin/env python


from pyLCS import liquidCrawler, matchCrawler, saveJSON

lc = liquidCrawler.liquidCrawler(region='na', year=2019, split='spring', playoffs=False)
mls = lc.match_links(render=True)

mc = matchCrawler.download_json_data(mls[0])

print(saveJSON.flatten_json(mc))
