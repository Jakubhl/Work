# TRIMAZKON
<p align="center">
  <img src="readme_images/logo_TRIMAZKON.png" alt="TRIMAZKON logo" width="150">
</p>

- Vývoj aplikace byl zpočátku směrován pro zpracování velkých objemů obrázkových dat z průmyslových kamer na výrobních linkách.
- Dále se vyvinuté GUI postupně doplňovalo i o další pomocné programy.
- V současnosti je aplikace rozdělena na tři subaplikace:
	- TRIMAZKON.exe
	- jhv_MAZ.exe
	- jhv_IP.exe

![installer setup](readme_images/installer_setup.png)

## Obecné vlastnosti aplikace:
- vlastní .msi installer
- licencování podle HWID
- JSON konfigurace
- autoupdate (Sharepoint)
- pipeline komunikace
- nabídka v System Tray (tray ikonka):
<p align="center">
  <img src="readme_images/tray_menu.png" alt="tray menu" width="150">
</p>
- Windows baloon tip (oznámení)
- čtení z SQL databáze
- tooltip (doplňující informace pod kurzorem nad tlačítky)

<p align="center">
  <img src="readme_images/main_menu.png" alt="main menu">
</p>

## Hlavní funkce aplikace
### Práce se soubory:
- Konverze souborů (obrázky se suffixem .ifz) pomocí externí aplikace do .jpg nebo .bmp
<p align="center">
  <img src="readme_images/converting_menu.png" alt="converting menu">
</p>

- Třídění podle syntaxe/vzorů názvů souborů, třídění párů apod.
<p align="center">
  <img src="readme_images/sorting_menu.png" alt="sorting menu">
</p>

- Mazání souborů jako služba na pozadí (využívá task scheduler, Windows baloon tip)
  - ukládá log mazání
<p align="center">
  <img src="readme_images/deleting_menu.png" alt="deleting menu">
</p>
<p align="center">
  <img src="readme_images/deleting_log.png" alt="deleting log">
</p>
### Prohlížeč obrázků na míru s podporou speciálních formátů (.ifz)
- lze nastavit jako základní prohlížeč obrázků
- malování přes obrázek (pro poziční kontroly)
- možnost otevření obrázku v dalším okně
<p align="center">
  <img src="readme_images/image_browser.png" alt="image browser">
</p>

### Pomocník pro nastavování IP adresy počítače a mapování disků
- ukládá vložené adresy/ disky do .xlsx souboru, možné doplnit poznámkami
- možnost importu .xlsx
- adresu lze měnit přes nabídku tray icons
<p align="center">
  <img src="readme_images/ipset_ip.png" alt="ip setting menu">
</p>
<p align="center">
  <img src="readme_images/ipset_disky.png" alt="disk mapping menu">
</p>
<p align="center">
  <img src="readme_images/tray_ukazka.gif" alt="tray icons menu, ukázka">
</p>

### Tvorba katalogu komponentů včetně kusovníku (s daty z SQL)
- GUI na sestavení katalogu + login do SQL
- filtruje komponenty z SQL databáze podle zvoleného výrobce
- možnost exportu do .xml, .xlsx, xlsm a do databáze, kde vytvoří tabulku
- možnost importu vyexportovaného projektu .xml

<p align="center">
  <img src="readme_images/katalog_main.png" alt="katalog - main">
</p>
<p align="center">
  <img src="readme_images/katalog_okno.png" alt="katalog - edit">
</p>

