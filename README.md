# Work
Analýza, kontrola a třídění souborů (.height, .normal) z kamer...

- vloží se cesta ke složce se soubory (Algoritmus ošetřen proti špatně zadané složce)
- nezáleží pokud jsou soubory: 
-- smíchané přímo v cestě nebo ve složce
-- uložené ve více složkách (volí se základní)
-- jiného typu - např.: .txt atp.
-- různé délky v názvu
                              
- Algoritmus odstraňuje nevyužité, prázdné složky v cestě
- Algoritmus je ošetřen proti špatnému inputu ze strany uživatele

## Verze 1.8.2:
- základní kontrola bez možnosti vstoupit do "advanced modu"

## Verze 2.3:
- Umožnuje vstoupit do "advanced modu", kde si lze zvolit způsob třídění a to buď: 
1) zvlášť do složek podle čísla kamery (s prefixem _Cam a číslem kamery)
2) zvlášť do složek podle čísla funkce (s prefixem _Func a číslem funkce)
3) obojí zároveň
