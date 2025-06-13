## Symulacja Wahadła Kapicy

# Autorzy

- Bartosz Wojtaś, Indeks: 337408
- Norbert Gościcki, Indeks: 337329

## Opis

Projekt zawiera skrypt Python (`nowy_kapitz3.py`), który symuluje ruch wahadła Kapicy – wahadła z punktem zawieszenia oscylującym w pionie. Symulacja wykorzystuje numeryczne rozwiązywanie równań różniczkowych i wizualizuje ruch za pomocą animacji w Matplotlib. Użytkownik może interaktywnie zmieniać częstotliwość oscylacji za pomocą suwaka oraz sterować animacją przyciskami pauzy/wznowienia i widoczności śladu.

## Funkcjonalność

- **Symulacja**: Rozwiązuje równania ruchu wahadła Kapicy za pomocą `scipy.integrate.solve_ivp` metodą RK45.
- **Wizualizacja**: Pokazuje trajektorię kulki, punkt zawieszenia i łączący je pręt, z opcjonalnym śladem ruchu kulki.
- **Interaktywność**: Suwak do zmiany częstotliwości oscylacji (`omega`) oraz przyciski do pauzowania/wznowienia animacji i przełączania widoczności śladu.
- **Tło**: Wykorzystuje obraz (`menu.jpg`) jako tło wykresu dla estetyki.
- **Parametry**: Parametry fizyczne (np. grawitacja, długość wahadła, amplituda) i ustawienia symulacji (np. czas, FPS) zdefiniowane na początku skryptu.

![Animacja Wahadła Kapicy](media/kapitza_animation.gif)
