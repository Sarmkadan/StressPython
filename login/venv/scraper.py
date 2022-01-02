import requests
import os
import urllib
import urllib3
import urllib3.request
import urllib.request
from xml.etree.cElementTree import Element, SubElement, tostring

def existdeleteFile(filename):
    if os.path.exists(filename):
        os.remove(filename)

def getOfac(filename):
    url = 'https://www.treasury.gov/ofac/downloads/' + filename
    # in case you need a session
    cd = {'sessionid': '123..'}
    r = requests.get(url, cookies=cd)
    existdeleteFile(filename)
    text_file = open(filename, "wb")
    n = text_file.write(r.content)
    text_file.close()

def getEUblackList(path):
    existdeleteFile(path)
    url = "https://webgate.ec.europa.eu/europeaid/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=dG9rZW4tMjAxNw"
    urllib.request.urlretrieve(url, path)

def getrusBlackList(path):
    existdeleteFile(path)
    url = 'http://www.fedsfm.ru/documents/terrorists-catalog-portal-act'
    r = requests.get(url)
    text_file = open(filename, "wb")
    n = text_file.write(r.content)
    text_file.close()

def getUABlacklist(path):
    q = []
    urlparse = 'http://www.sdfm.gov.ua/articles.php?cat_id=87&lang=en'
    urltodoc = 'http://www.sdfm.gov.ua/content/file/Site_docs/Black_list/'
    r = requests.get(urlparse)
    for x in r.text.split('/content/file/Site_docs/Black_list/'):
        fromxstring = x.split('.xml')[0]
        if len(fromxstring) < 30:
            q.append(fromxstring)

    for filename in q:
        existdeleteFile('UA'+filename+'.xml')
        text_file = open('UA'+filename+'.xml', "wb")
        n = text_file.write(r.content)
        text_file.close()

def getFatFblackList(path):
    url = 'https://ofsistorage.blob.core.windows.net/publishlive/ConList.xml'
    r = requests.get(url)
    existdeleteFile('FaTF.xml')
    text_file = open('FaTF.xml', "wb")
    n = text_file.write(r.content)
    text_file.close()


# createfile('sdn.pip')
# createfile('add.pip')
# createfile('alt.pip')
#getEUblackList('ConsolidatedFinancialSanctionsFile.xml')

#getEUblackList('bla.xml')
#bla = getrusBlackList("")

#listforeginers = bla.text.split('<a data-toggle="collapse" href="#foreignUL">Иностранные юридические лица</a>')[1].split('</div>')[1].split('<ol class="terrorist-list">')[1].replace('<li>','').replace('</li>','').replace('</ol>','').replace('<ol>','')


#getUABlacklist('bla.xml')


def generatexmlelement(name,id,inn,birdthdate,description,adress,birthplace,passport):
    # create xml
    root = Element('TERRORISTS')

    child = SubElement(root, 'TERRORISTS_NAME')
    child.text = "&lt;![CDATA[" + name + "]]&gt;"

    child = SubElement(root, 'ID_NEW')
    child.text = "&lt;![CDATA["+id + "]]&gt;"

    child = SubElement(root, 'PERSON_TYPE')
    child.text = "&lt;![CDATA["+'some text'+ "]]&gt;"

    child = SubElement(root, 'IS_TERRORIST')
    child.text = "&lt;![CDATA["+'some text'+ "]]&gt;"

    child = SubElement(root, 'INN')
    child.text = "&lt;![CDATA[" + inn+ "]]&gt;"

    child = SubElement(root, 'BIRTH_DATE')
    child.text = "&lt;![CDATA["+ birdthdate + "]]&gt;"

    child = SubElement(root, 'DESCRIPTION')
    child.text = "&lt;![CDATA[" + description+ "]]&gt;"

    child = SubElement(root, 'ADDRESS')
    child.text = "&lt;![CDATA[" + adress+ "]]&gt;"

    child = SubElement(root, 'TERRORISTS_RESOLUTION')
    child.text = "&lt;![CDATA["+'some text'+ "]]&gt;"

    child = SubElement(root, 'BIRTH_PLACE')
    child.text = "&lt;![CDATA["+birthplace+ "]]&gt;"

    child = SubElement(root, 'PASSPORT')
    child.text = "&lt;![CDATA["+passport+ "]]&gt;"


    roteky = Element("TERRORISTS_CATALOG", {'NUM':"362ПЭ",
                              'DATE':"26.12.2019",
                              'ID':"html_url",
                              })


    roteky.insert(0, root)

    print(tostring(roteky))

generatexmlelement("sd","sd","sd","sd","sd","sd","sd","sd")

'''
def getsessionafterredirect(host, data):
    res = requests.post(
        host,
        data=data,
        allow_redirects=False)
    if res.status_code == 302:  # expected here
        jar = res.cookies
        redirect_URL2 = res.headers['Location']
        res2 = requests.get(redirect_URL2, cookies=jar)
        print(res2.cookies)# res2 is made with cookies collected during res' 302 redirect
        return res2
    else:
        return res

host = 'https://webgate.ec.europa.eu/cas/login'
data = {'username': 'rutova2@gmail.com'}
        #'TxId': ''}
result2 = getsessionafterredirect(host, data)

result3 = getsessionafterredirect(result2.url, data)

urltopost = result3.text.split('<form id="languageForm" method="post" action="')[1].split(';')[0]
txid = result3.text.split('input type="hidden" name="TxId" value="')[1].split('"')[0]
here = result3.text.split('name="here" value="')[1].split('"')[0]

data2 = {'username': 'rutova2@gmail.com',
         'TxId': txid,
         'here': here,
         'bg': 'en'}

#result4 = getsessionafterredirect(urltopost, data)
'''

'''
data2 = {'password': ''}
'''
'https://ofsistorage.blob.core.windows.net/publishlive/ConList.csv'