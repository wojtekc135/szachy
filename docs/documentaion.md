# Dokumentacja

## Assets
Wszystkie karty i grafiki rysowane przez Hanię Szlęk.

Muzyka: https://pixabay.com/pl/music

## Menu

 - Możliwość wyboru jednego z trzech wariantów
 - Ustawienia
	- Zmiana muzyki (3 dostępne)
	- Zmiana głośności
	- Zmiana pomiędzy trybem okienkowym, a pełnoekranowym
	- Wyświetlenie autorów gry
- Podpięcie instrukcji .pdf

### Menu button
Klasa do przycisków w menu.

	- Wyświetla przyciski w zależności od proprocji ekranu
	- Przyciski podświetlają się po najechaniu

## Round
Odpowiedzialne za rozgrywkę.

- **example state**
	- State: Słownik trzymający wszystkie karty dostępne w rozgrywce
	- Do kart przypisywana odpowiednia ilość kruków i specielne umiejętności
	- Karty przypisywane do odpowiednich stosów

- **human/bot_show_2_cards**
	- Podglądniecie kart na początku rozgrywki
- **human/bot_turn_idz_na_calosc**
	- Obsługa tury gracza lub bota w wariancie drugim
- **variant3_options oraz check_two_cards oraz show_text_bar**
	- Obsługa rozgrywki i przycisków dla wariantu trzeciego

## Special Abilities
Odpowiedzialne za użycie umiejętności

- Look
	- Podglądnięcie karty z ręki dowolnego gracza
- Swap
	- Zamiana dwóch kart z rąk dowolnych graczy, bez podglądania
- Take two
	- Zabranie dwóch kart ze stosu zakrtego, karty przez chwilę wyświetlają się w tymczasowej lokacji. Gracz wybiera, którą z dwóch kart chce użyć, wtedy druga przenosi się na stos odkryty.

## Input Handler
Odpowiedzialny za wykrywanie kliknięć myszy na ekranie

## Card
- **Atrybuty**
	- przód i tył karty (obraz)
	- czy kliknięta
	- czy zaznaczona (indykacja na ekranie poprzez małe przemieszczenie się wyżej)
	- lokacja jako nazwa stosu do którego aktualnie należy
	- nr. lokacji w swoim stosie (od 1-4) dla rąk i zmienne dla stosów odkrytego i zakrytego
	- ilość kruków
	- id
	- umiejętność (look, swap, take two, none)

- Oblicza poprawną pozycję karty do wyświetlania zależną od wielkości ekranu i pozycji karty w swoim stosie

## Player
- **Atrybuty**
	- isHuman - czy gracz jest botem
	- player_number - numer gracza od 1 do 4
	- crows - aktualna ilość kruków gracza do liczenia punktów
## Action button
Klasa przycisku dla rozgrywek

## Utils
- **load_assets**
	- Ładuje zasoby gry (karty, tło, rewers kart) z folderu.
- **scale_assets**
	- Skaluje zasoby gry (karty, tło, rewers kart) do określonych rozmiarów.
- **get_card_size**
	- Oblicza rozmiar karty na podstawie wysokości ekranu.
- **message_box**
	- Rysuje prostokąt z wycentrowanym tekstem w zadanej lokalizacji na ekranie.

## Game renderer
Odpowiedzialny za wyświetlanie stanu gry na ekranie

## End Screen
Wyświetla aktualną tabelkę punktów po naciśnięciu przycisku pobudka.
Jeżeli po pobudce następuje koniec gry to wyświetla ostateczne punkty i czy gracz wygrał czy przegrał.

## Boty
Zarządza działaniem botów za pomocą biblioteki random. Boty mogą:

	- Brać karty ze stosu odkrytego i zakrytego
	- Używać umiejętności specialnej
	- Zarządzić pobudkę


<center><h1>Warianty</h1></center>

## Variant1
Obsługa grywalności wariantu pierwszego, tak jak w instrukcji. Wariant inicjuje graczy, rozgrywkę, rozdanie kart. Zarządza, którego gracza jest tura i obsługa końca gry po przeliczeniu kruków w sposób "Nie takie kruki straszne"

## Variant2
Obsługa grywalności wariantu drugiego tak jak w instrukcji. Wariant inicjuje graczy, rozgrywkę, rozdanie kart. Zarządza, którego gracza jest tura i obsługa końca gry po przeliczeniu kruków w sposób "Idź na całość!"

## Variant3
Obsługa grywalności wariantu trzeciego. Nowa opcja na początku tury, aby zgadnać ilość kruków na dwóch karatch poprzez wpisanie jej z klawiatury do wyśweitlanego okienka na środku ekranu.
Z ograniczeń technicznych wyświetlania ilości kart zamiast kary, jaką jest dobranie kolejnej karty po niepoprawnym zgadnięciu ilości kruków na kartach, gracz dostaje +3 kruki. Nagrodą jest -3 kruki.  Wariant inicjuje graczy, rozgrywkę, rozdanie kart. Zarządza, którego gracza jest tura i obsługa końca gry po przeliczeniu kruków w sposób "Wiem co mam"

## Błędy
- Na Linuxie karty specialne zamieniają się z kartami o tej samej liczbie kurków. Prawdopodobnie przez kolejność zczytywania z folderu.
- Przy użyciu umiejętności "Take Two" kilka razy, mieszają się stosy, ale po turze już błąd mija.
- Jeżeli stos się skończy to gra ma fatal error