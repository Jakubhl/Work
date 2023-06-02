# Work
Analýza, kontrola a třídění souborů z průmyslových kamer

- vloží se cesta ke složce se soubory (Algoritmus ošetřen proti špatně zadané cestě)
- nezáleží pokud jsou soubory: 
  - smíchané přímo v cestě nebo ve složce
  - uložené ve více složkách (volí se základní)
  - jiného typu - např.: .txt atp.
  - různé délky v názvu
                              
- Algoritmus odstraňuje nevyužité, prázdné složky v cestě
- Algoritmus je ošetřen proti špatnému inputu ze strany uživatele
- Nyní je již algoritmus schopen zpracovat více formátů souboru (Nepracuje tedy, jako původně pouze se soubory typu: ".Height" a ".Normal", ale s neomezeným počtem typů).
	- Funguje na principu předpokladu podobné syntaxe názvu souboru (je splitován znakem "&")
	- Ošetřeno chybovým hlášením

## Verze 2.4 Lite:
- základní, rychlá kontrola bez možnosti vstoupit do "advanced modu"

![ukázka verze 2.4 Lite](images/24lite.PNG)

## Verze 2.4:
- Umožnuje vstoupit do "advanced modu", kde si lze zvolit způsob třídění souborů

![ukázka verze 2.4 moznosti](images/24_moznosti.PNG)

- Nejprve je provedeno základní třídění do OK a NOK složky:

![ukázka verze 2.4 základ](images/24_basic.PNG)

1) třídění podle typu souboru (jako 2.4 Lite)

![ukázka verze 2.4 - podle typu](images/24_type.PNG)


2) zvlášť do složek podle čísla funkce (s prefixem _Func a číslem funkce)

![ukázka verze 2.4-funkce](images/24func.PNG)

3) zvlášť do složek podle čísla kamery (s prefixem _Cam a číslem kamery)

![ukázka verze 2.4-camera](images/24cam.PNG)

4) obojí zároveň

![ukázka verze 2.4-both](images/24both.PNG)

5) manuální mód (manuální nastavení počtu zakrytých znaků)

![ukázka mannual. módu 2.4](images/24_manual.PNG)

## Verze 2.5 Lite:

- Zvláštní verze pro kontrolu odeslaných dvojic (i trojice... neomezeně) souborů za sebou (obsluha odejme paletu a opět vloží tu samou...)

- funguje pouze pro případ názvu v tomto tvaru: 2023_04_13-07_11_09_xxxx_   0020   _&Cam2Img.Height
	- tzn. musi se jednat o čtyřciferné číslo nalevo od _&
	- tvar x9xx je schválně ignorován
	- maximálni počet palet v sadě je přednastaven na: 55


- Nalezené dvojice kopíruje do složky: "PAIRS", ve které je rovněž roztřídí podle suffixu (.Normal/.Height...)

![ukázka verze 2.5 Lite](images/25basic.PNG)

- Ve složce PAIRS:

![ukázka verze 2.5 Lite pairs](images/25pairs.PNG)

## Verze 2.5:
- Stejné jako 2.5 Lite, jen je programovaná na spuštění ve složce, kde se nacházejí jednotlivé složky s datumy (2023_04_13) -> rozhoduje se podle složky A/B -> složky Height/Normal/Grey se soubory... a projde je všechny postupně s dotazem o povolení

## Aplikace s GUI
- Je nutné stáhnout zip soubor kvůli načítání obrázků, poté si lze třeba vytvořit shortcut exe souboru a přesunout si jej na plochu
- Byl přídán konfigurační text file pro definování základní cesty ve file exploreru