# Kommunesuite — hjemmeside

Dansk præsentationsside for Kommunesuite: en familie af enkle værktøjer til kommunernes hverdag. Siden viser produktidéer, funktioner, eksempler, samspil og den aktuelle status.

## Status 19. oktober 2026

Kataloget indeholder **11 værktøjer**: KommunePDF i privat Mac-RC1 og 10 planlagte værktøjer. De nye forslag i kategorien **Medier & filer** er KommuneAfspiller, KommuneKlip, KommuneLyd, KommunePak, KommuneSkærm og KommuneBillede. Sammenligninger med fx VLC, Clipchamp, Audacity, WinRAR og 7-Zip beskriver hverdagsopgaver; de er ikke løfter om identiske funktioner.

Kommunesuite-launcheren 0.1.3 og KommunePDF 0.1.4 findes som private testudgaver til Mac med Apple Silicon. Launcheren viser fortsat de oprindelige ni værktøjer og åbner en manuelt installeret KommunePDF. Hjemmesidens katalog er opdateret uden at ændre appene. Installation efter frisk download på en anden Mac med macOS 27, Apple-signering, notarisering og bred accept mangler fortsat. Hentning og automatisk opdatering fra launcheren er ikke aktiveret.

De øvrige værktøjer og samspillet mellem dem er planlagt. Der er ingen automatisk overførsel af filer, deltagere eller status mellem appene. Windows og udvikling af de øvrige apps afventer en stabil Mac-version.

## Byg og afprøv lokalt

Kræver Python 3 og ingen ekstra Python-pakker:

```sh
python3 build_site.py
```

Forventet output for det aktuelle katalog:

```text
Built 11 product cards, 10 planned apps and product content.
```

Åbn `dist/index.html` i en browser. Produktdialoger, filtre, pause af animationer og direkte produktlinks virker uden en server. Fontene Familjen Grotesk og Public Sans hentes fra Google Fonts; browserens systemfont bruges uden netforbindelse. Bodoni Moda til logoet er inkluderet lokalt med sin fontlicens.

Kontrollér statusafsnittet, produktdialoger og en mobilbredde på 390 px før udgivelse. `dist/index.html` skal indeholde `Beta · privat Mac-RC1` og `id="status"`.

## Kilde og opbygning

- `catalog.json`: produktindhold, status, seks funktionspunkter pr. værktøj, eksempler og forbindelser.
- `index.template.html`: sidens sektioner i det eksisterende design.
- `build_site.py`: genererer ikoner, kort, katalogantal, danske talord, planlagte links og `dist/index.html`.
- `dist/app.js`: produktdialoger, filtre, tastaturfokus og animationstilstand.
- `dist/theme.css`: typografi, layout og responsive visninger.
- `dist/brand-logos.css` og `dist/assets`: eksisterende logoer, portrætter, fontfiler og appikoner. De nye appikoner følger den eksisterende ikonstil.

Bygningen opdaterer også `dist/source.zip` fra en eksplicit liste med hjemmesidens kilder og assets. Arkivet indeholder ikke Git-historik, `.vercel`, miljøfiler eller native app-/testpakker. Det indeholder ikke sig selv. Antal beregnes fra kataloget frem for at være skrevet ind flere steder.

Indholdsopdateringen tager udgangspunkt i overleveringen “Kommunesuite forside.md” fra 19. oktober 2026 og den efterfølgende beslutning om at fjerne Booking, Sign, Flow og WebTjek fra hjemmesidens udvalg. Eksisterende portrætter og logoer bevares.

## Udgivelse

Siden bruger det eksisterende Vercel-projekt bag `https://kommunesuite.vercel.app`. `vercel.json` peger på `dist`. Kontrollér den lokale projektbinding før deployment:

```sh
vercel project inspect --non-interactive
vercel deploy --prod
```

Kør fra projektroden med korrekt `.vercel/project.json`. Kontrollér derefter `/#status` og `/source.zip`. Testpakker og udviklingsrepos er private; hjemmesiden linker ikke til det private downloadrepo.

## Licenser og kreditering

Hjemmesidens egen kode har EUPL 1.2 som licensgrundlag; se `LICENSE`. KommunePDF bygger på PdfCraft og bevarer dets MIT- og Apache-2.0-licenser og relevante tredjepartsnotitser. “Sidens kode” er alene denne hjemmeside, ikke appenes kilder.

Portrætter og logoer har særskilte vilkår; se `NOTICE` og `NAMES.md`. Disse vilkår og fontlicensen skal bevares ved genbrug.
