# Gra-planszowa-Budowniczowie
Projekt na przedmiot Podstawy Języków Funkcyjnych

🎲 Implementacja gry planszowej BUDOWNICZOWIE zainspirowanej logiczną grą planszową Santorini.<br>
🎲 Rozgrywka przeznaczona dla 2-3 osób.<br>



## PRZYGOTOWANIE DO GRY:

1️⃣. W menu należy wybrać liczbę graczy biorących udział w rozgrywce (opcją podstawową jest 2 graczy).<br>
2️⃣. Każdy z graczy wybiera jedną z dostępnyc mocy (opcją podstawową jest brak mocy specjalnych).<br>
3️⃣. Każdy z graczy ustawia po 2 pionki na planszy<br>

## ROZGRYWKA

Gracze wykonują naprzemiennie swoje tury, każda tura składa się z:

1️⃣. fazy ruchu - gracz musi ruszyć jednym ze swoich pionków na sąsiednie pole, musi ono być niezajęte, a jego wysokość może być maksymalnie o 1 wyższa od wysokości pola, na którym jest pionek (4 piętro - dach - również jest niedostępne dla pionków).<br>
 <br><br> ![Ruch gracza](ScreenShots/player_move.jpg) <br><br>
2️⃣. fazy budowania - gracz stawia na sąsiednim niezajętym polu blok budowli, przy czym nie można przekorczyć 4 pięter, parter liczy się jako pierwsze piętro.<br>
 <br><br> ![Budowanie_przez_gracza](ScreenShots/player_build.jpg) <br><br>

Gra toczy się dopóki, któryś z graczy nie wejdzie w fazie ruchu na 3 piętro, lub inny gracze nie odpadną z gry. Odpaść można, jeśli w skutek działań przeciwnika lub własnych błędów:

1️⃣. Żaden z pionków gracza nie może wykonać ruchu w jego turze.<br>
2️⃣. Ruszony pionek nie może wybudować budowli.<br>
 <br><br> ![Wygrana gracza](ScreenShots/game_over.jpg)

## MOCE SPECJALNE

W grze występuje 8 mocy specjalnych, modyfikujących rozgrywkę. Są to:

 • DWUSKOK: Gracz może wykonać dwa ruchy (drugi ruch opcjonalny), jednak nie może wrócić na pole, z którego startował.<br>
 • WOJOWNIK: Gracz może wykonać ruch na pole zajęte przez przeciwnika, pionki zamieniają się wtedy miejscami.<br>
 • OSZUST: Gracz może w fazie budowania postawić kopułę na dowolnej wysokości.<br>
 • DEWELOPER: Gracz możę w fazie budowania postawić dwa bloki, jednak nie mogą być one na tym samym polu.<br>
 • WYSOKOŚCIOWIEC: Gracz może postawić dwa bloki na tym samym polu, chyba że drugi blok byłby kopułą.<br>
 • SPYCHACZ: Gracz może wejść na pole zajęte przez przeciwnika, przepychając go zgodnie z kierunkiem ruchu.<br>
 • POŚPIESZNY: Jeśli twój pionek nie zmienia wysokości może przesunąć się o dowolną liczbę pól w wybranym kierunku (o ile to możliwe).<br>
 • SKOCZEK: Zyskujesz możliwość wygrania poprzez przemieszczenie się o minimum dwa pola w dół.<br>
