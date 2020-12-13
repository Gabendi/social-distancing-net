# social-distancing-net
_Készítők: Pogány Domonkos, Pallag Jonatán, Németh Gábor, Bodnár Anna_

A program célja, hogy a a koronvírus okozta világjárvány elleni küzdelmet segítse. Segítségével térfigyelő kamerák képét elemezve pontosabb képet kaphatunk arról, milyen helyzetekben nem tartják be az emberek a WHO által ajánlott távolságtartást.

A program megfelelő erőforrások biztosítása mellett képes akár HD kamerák real-time feldolgozására is. De ha nem rendelkezünk nagy mennyiségű számítási erőforrással, akkor előre rögzíthetünk térfigyelő kamera felvételeket, majd utasíthatjuk a programot a már előre felvett videó 
feldolgozására is.

A feldolgozás során a program felismeri a megfigyelt területen mozgó embereket, és jelzi, ha emberek túl közel tartózkodtak egymáshoz. A program felismeri az együtt mozgó családokat, és nem jelez, ha családtagok tartózkodtak túl közel egymáshoz.

A feldolgozás végeztével a program egy hőtérképen jelzi a legzsúfoltabb helyeket. Azaz azon pontokat, ahol a legtöbbször szegték meg a járókelők az ajánlott távolságtartást.

A program által készített elemzés megtekintése, illetve a hőtérkép alapos vizsgálata segítheti a bolt tulajdonosokat, hogy úgy alakítsák ki belső tereiket, hogy a lehető legalacsonyabb legyen a fertőzés kockázata, illetve az önkormányzatokat a közterek hasonló célú átrendezésében.

Útmutató a program telepítéséhez, használatához, továbbá a forráskód dokumentációja [itt](https://gabendi.github.io/social-distancing-net/) érhető el.

## Elemzés menete

A program minden képkockát egyesével dolgoz fel. Először detektálja a képkockán látható embereket egy előre betanított YOLO neurális hálózat segítségével. A YOLO hálózat megadja a képen található személyek határolókeretét, illetve egy magabiztossági pontszámot. A pontszám megadja mennyire biztos a hálózat abban, hogy az adott helyen ember található.

A detektált határoló kereteket a program ezután az egyes emberekhez rendeli. A cél az, hogy elérhető legyen az, hogy milyen útvonalat jártak be az emberek a program futása során. A határolókeretekben szereplő emberek azonosítására, Kálmán-filtert alkalmaztunk. A Kálmán-filter megfigyeli az objektumok mozgását, majd ebből a mozgásból előrevetíti, hogy a következő képkockán hol fognak elhelyezkedni, és ha tényleg megjelenik az előrejelzett helyen egy határolókeret, akkor azt az objektumhoz rendeli, és pontosítja a keret pontos helyzetével a mozgáselőrejelzést.

Az emberek mozgását ismerve már megállapítható mely személyek mozognak tartósan egymás mellett. A program feltételezi, hogy a tartósan együtt mozgó emberek ismerik egymást, egy háztartást alkotnak, és figyelmen kívül hagyja, ha a csoport tagjai egymás között nem tartják az elvárt távolságot.

Végül a program detektálja ha két nem egy csoportba tartozó ember túl közel került egymáshoz, és egyrészt elmenti ezeket az eseteket, másrészt sötétkék vonallal összeköti azokat az embereket, akik túl közel álltak egymáshoz.

A program a futása végén egy hőtérképen is ábrázolja, hogy hol szegték meg a legtöbbször az ajánlott távolságtartást.

## Kalibrálás
A video elemzése előtt szükség van a program kalibrációjára is.

A kamera kép készítése során a 3D világot a kamera síkjára vetíti és az így keletkező képet jeleníti meg. A program képes megfelelő kalibráció esetén a vetített képből meghatározni az emberek pontos elhelyezkedését. Az emberekről a program felteszi, hogy egy síkon (a földön) állnak, így távolságukat ezen a síkon határozza meg.
