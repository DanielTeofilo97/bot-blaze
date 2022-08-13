import pathlib
from os import path


appDir = str(pathlib.Path().resolve())
pathChromeDriver = str(appDir)+"\\web-driver\\chromedriver.exe"
dirDownloads = str(path.join(path.expanduser("~"), "Downloads"))
filtroUrls = "jurisprudencia/pesquisa"
showBrowser = True # não alterar
esperar_range = 15
qtd_erro = 5
