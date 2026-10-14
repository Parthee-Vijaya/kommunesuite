# Kommunesuite

En præsentationsside for ni planlagte kommunale open source-værktøjer.
Siden er et produktkatalog og beskriver en fremtidig portefølje. Den udfører ikke de beskrevne produkters opgaver.

## Indhold

PDF-værksted, Spørgeskema, Tidsbestilling, Fildeling, Underskriftsforløb,
Arbejdsgange, Tilgængelighedstjek, Dokumentmaskering og Læringsforløb.
Produktindholdet er samlet i `catalog.json`. Ikonerne genereres som originale SVG-filer.

“Om initiativet” beskriver gratis software, fri adgang uden medlemskrav,
selvstændige apps, eget Docker-setup og valgfri betalt hosting/support.
Sektionen præsenterer Parthee Vijayamohan og Bjørn Skalkam med officielle
portrætter, korte biografier og links til AI Alliancen og Komplai.

## Byg

Kør `python3 build_site.py`. Den statiske hjemmeside ligger i `dist/` og kan hostes uden en serverapplikation.

## Brugerflade

Responsiv produktoversigt, kategorifiltre, produktdialoger med delbare links, næste/forrige-navigation og motiongrafik.
Animationer kan sættes på pause og følger systemets indstilling for reduceret bevægelse.
Der bruges ingen cookies, eksterne scripts eller analytics i siden.
Portrætterne ligger lokalt i `dist/assets/`. AI Alliancens og Komplais
ordmærker er genskabt som gennemsigtig SVG-typografi direkte i HTML'en.
AI Alliancens originale Bodoni Moda-font leveres lokalt med sin OFL-licens.
Komplais ordmærke bruger virksomhedens typografi og den blå skråstreg.

## Licens og navne

Egen kode, produkttekster og appikoner er udgivet under EUPL 1.2. Se `LICENSE`.
Tredjepartsfotos og logoer er undtaget; se `NOTICE` for rettigheder og kilder.
Navnene er beskrivende danske funktionsnavne under fællesnavnet Kommunesuite.
Se `NAMES.md` for den indledende navnescreening og dens afgrænsning.

## Produktion

https://kommunesuite.vercel.app/
Vercel publicerer den statiske mappe `dist/`.
`dist/source.zip` indeholder den tilsvarende hjemmesidekilde til download.

## Design

Designet følger den brugerleverede reference “Kommunesuite forside.html” og
de tilhørende billeder: hvide flader, mørkegrå tekst og knapper, et mosaiklogo
med seks produktfarver og en rolig 3×3-oversigt over værktøjerne.
Ikonerne anvender logoets blå, koralrøde, lilla, orange, indigoblå og gule farver.

Forsidens tekst er: “Enkle værktøjer til kommunen. Gør de små opgaver små igen.
Ni enkle værktøjer til kommunens hverdag. Åben kode, fælles retning og plads til
jeres egne behov.” De to knapper fører til værktøjer og sammenhængen.

Typografi: Familjen Grotesk og Public Sans via Google Fonts, med systemfonte
som fallback. Ingen eksterne JavaScript-biblioteker bruges.
