# Work
Analýza, kontrola a třídění souborů (.height, .normal) z kamer...

- vloží se cesta ke složce se soubory (Algoritmus ošetřen proti špatně zadané cestě)
- nezáleží pokud jsou soubory: 
  - smíchané přímo v cestě nebo ve složce
  - uložené ve více složkách (volí se základní)
  - jiného typu - např.: .txt atp.
  - různé délky v názvu
                              
- Algoritmus odstraňuje nevyužité, prázdné složky v cestě
- Algoritmus je ošetřen proti špatnému inputu ze strany uživatele

## Verze 1.8.2:
- základní kontrola bez možnosti vstoupit do "advanced modu"

![ukázka verze 1.8.2](images/obrazek182.PNG)

## Verze 2.3:
- Umožnuje vstoupit do "advanced modu", kde si lze zvolit způsob třídění a to buď: 
1) zvlášť do složek podle čísla kamery (s prefixem _Cam a číslem kamery)

![ukázka verze 2.3-camera](images/23cam.PNG)

2) zvlášť do složek podle čísla funkce (s prefixem _Func a číslem funkce)

![ukázka verze 2.3-function](images/23func.PNG)

3) obojí zároveň

![ukázka verze 2.3-both](images/23both.PNG)

## Verze 2.4:
- Univerzální verze vůči více formátům souboru (Nepracuje tedy, jako původně pouze se soubory typu: ".Height" a ".Normal", ale s neomezeným počtem typů).

- Algoritmus funguje na principu předpokladu podobné syntaxe názvu souboru (je splitován znakem "&")
- Ošetřeno chybovým hlášením

- Nejprve je provedeno základní třídění do OK a NOK složky:

![ukázka verze 2.4 základ](images/24_basic.PNG)

- Dodatečné třídění umožňuje stejné možnosti třídění, jako předchozí verze 2.3. + manuální nastavení počtu zakrytých znaků:
![ukázka verze 2.4-both](images/24_slozky.PNG)

![ukázka mannual. módu 2.4](images/24_manual.PNG)
