import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import base64

htm=open("thesimpsons.htm","w")
csv=open("thesimpsons.csv","w")
htm_table_header = "<tr><th>img</th><th>episode</th><th>date</th><th>rating</th><th>title</th><th>summary</th>\n"
csv_table_header = "episode;date;rating;title;summary\n"
htm_script = '''<script>const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;
const comparer = (idx, asc) => (a, b) => ((v1, v2) => v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2))(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr) );
})));</script>\n'''
htm_style = '''<style>#hor-minimalist-b
{
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
	font-size: 10px;
	background: #fff;
	border-collapse: collapse;
	text-align: left;
}
#hor-minimalist-b th
{
	font-size: 12px;
	font-weight: normal;
	color: #039;
	padding: 10px 8px;
	border-bottom: 2px solid #6678b1;
	cursor: pointer;
}
#hor-minimalist-b td
{
	border-bottom: 1px solid #ccc;
	color: #669;
	padding: 3px 4px;
}</style>\n'''

episodes = []
seasons = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
#seasons = [34]

for season in seasons:
    url = f"https://www.imdb.com/title/tt0096697/episodes?season={season}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    seas = "S"+((soup.find("h3", {"id": "episode_top"}).contents[0]).split()[1]).rjust(2,"0")
    epi_list = soup.find_all("div", {"class": "list_item"})
    for epi in epi_list:
        try:
            episode = {}
            img = (base64.b64encode(requests.get((epi.find("img", {"class": "zero-z-index"}))["src"]).content)).decode()
            episode["img"] = img
            summary = epi.find("div", {"class": "item_description"}).contents[0].strip()
            episode["summary"] = summary
            rating = float(epi.find("span", {"class": "ipl-rating-star__rating"}).contents[0])
            episode["rating"] = rating
            title = epi.find("a", {"itemprop": "name"}).contents[0]
            episode["title"] = title
            date1 = (epi.find("div", {"class": "airdate"}).contents[0]).split()
            date2 = datetime.strptime( f"{date1[1][0:3]} {date1[0]} {date1[2]}", "%b %d %Y").date()
            episode["date"] = str(date2)
            number = "E" + (epi.find("meta", {"itemprop": "episodeNumber"})["content"]).rjust(2,"0")
            episode["episode"] = f'''{seas}{number}'''
            episodes.append(episode)
            print(f'''{episode["episode"]}''')
        except:
            break

htm.write(htm_style)
htm.write('''<table id="hor-minimalist-b">''')
csv.write(csv_table_header)
htm.write(htm_table_header)
for episode in episodes:
    htm_table_row = f'''<tr><td><img width="112" height="63" src="data:image/jpeg;base64, {episode["img"]}" /></td><td>{episode["episode"]}</td><td>{episode["date"]}</td><td>{episode["rating"]}</td><td>{episode["title"]}</td><td>{episode["summary"]}</td></tr>'''
    csv_table_row = f'''{episode["episode"]};{episode["date"]};{episode["rating"]};{episode["title"]};{episode["summary"]}\n'''
    csv.write(csv_table_row)
    htm.write(htm_table_row)
htm.write('''</table>''')
htm.write(htm_script)

