# Gra-karciana-sen
"Sen" to cyfrowa adaptacja gry karcianej, w której gracz rywalizuje z botami, aby uzyskać jak najmniejszą liczbę punktów w swojej ręce. Gra została napisana w Pythonie, korzystając z biblioteki Pygame, zapewniającej prosty i przyjazny graficzny interfejs użytkownika.

## Funkcjonalności

- **Gra dla każdego** – zasady są super proste!
- **Wiele wariantów** - aż 3 warianty gry do wyboru
- **Dynamiczny interfejs graficzny** – intuicyjne sterowanie i czytelne elementy gry.
- **Automatyczne liczenie punktów** – system automatycznie oblicza wynik każdej rundy.
- **Symulacja talii kart** – w grze dostępne są losowe karty zgodne z zasadami oryginalnej gry.

## Wymagania

Aby uruchomić grę, potrzebujesz:
- Python 3.8 lub nowszy
- Biblioteka Pygame 2.1.0 lub nowsza

## Instalacja

1. Sklonuj repozytorium gry:
   ```bash
   git clone https://github.com/uzytkownik/gra-sen.git
2. Przejdź do katalogu projektu:
    ```bash
   cd gra-sen
3. Zanistaluj wymagane zależności:
    ```bash
   pip install -r requirements.txt
4. Uruchom grę:
    ```bash
   python main.py

## Jak grać?
Uruchom grę poleceniem python main.py. Wybierz wariant i rozpocznij rozgrywkę. Każdy gracz (zarówno użytkownik jak i bot) ma możliwość wymiany kart, dążąc do uzyskania jak najmniejszej liczby punktów. Gra kończy się, gdy któryś z graczy ogłosi "Pobudka!", a pozostałe karty zostaną rozliczone. Wygrywa gracz z najmniejszą liczbą punktów.

![Screenshot of the menu](../assets/Zrzut ekranu menu.png "Menu Screenshot")  
![Screenshot of the variants](../assets/Zrzut ekranu warianty.png "Warianty Screenshot")  
![Screenshot of the gameplay](../assets/Zrzut ekranu gra.png "Gra Screenshot")

## Licencja
Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku LICENSE

## Autorzy
- **Wojciech Cieślik** - Gameplay
- **Magdalena Majda** - Warianty, logika gry
- **Wiktoria Szczepaniak** - Warianty, logika gry
- **Joanna Frączyk** - Warianty, logika gry
- **Olga Russell** - Boty
- **Maja Skóra** - Menu
- **Hanna Szlęk** - Grafika
