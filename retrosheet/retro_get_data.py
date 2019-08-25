import wget

years = range(1999,2019)

for year in years:
    url = "http://www.retrosheet.org/events/{}eve.zip".format(str(year))
    save_dir = "c:/retrosheet/downloads/zipped/{}eve.zip".format(str(year))
    print(url)
    wget.download(url, save_dir)


for year in years:
    url = "http://www.retrosheet.org/gamelogs/gl{}.zip".format(str(year))
    save_dir = "c:/retrosheet/downloads/zipped/{}gl.zip".format(str(year))
    print(url)
    wget.download(url, save_dir)
