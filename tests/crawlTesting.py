from ..crawler import _create_connection

conn_test = _create_connection('https://liquidpedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage',
                               render=True)
links = conn_test.html.find('a[href*=matchhistory]')
print(links)
