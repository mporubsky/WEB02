#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zostavenie webu BABYLAND — slovenská aj anglická verzia z jedného zdroja.

Obe jazykové verzie majú ROVNAKÝ obsah aj rovnakú stavbu stránok. Anglická
verzia nie je samostatný web, ale preklad slovenskej: skript vezme obsah
slovenskej stránky, prepíše v ňom texty podľa prekladovej mapy nižšie
a poopravuje cesty a odkazy. Vďaka tomu sa obe verzie nemôžu rozísť —
zmena v slovenskej stránke sa po spustení skriptu prejaví aj v anglickej.

Spustenie (z koreňa projektu):

    python3 scripts/build_site.py
    python3 .claude/skills/local-business-website/scripts/bump_assets_version.py

Skript prepisuje HTML súbory. Slovenské stránky pritom vyjdú znak po znaku
rovnako ako predtým — mení sa len menu a pätička, ktoré generuje tiež.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://www.babyland-centrum.sk/"

# ── Stránky ──────────────────────────────────────────────────────────────
# (slovenský súbor, anglický súbor, položka v menu SK, položka v menu EN)
PAGES = [
    ("index.html",       "index.html",      "Úvod",                    "Home"),
    ("ponuka.html",      "offer.html",      "Ponuka",                  "What we offer"),
    ("kurzy.html",       "courses.html",    "Kurzy AJ pre deti",       "English courses"),
    ("filozofia.html",   "philosophy.html", "Naša filozofia",          "Our philosophy"),
    ("na-navsteve.html", "visit.html",      "Na návšteve u&nbsp;nás",  "A visit with us"),
    ("kontakt.html",     "contact.html",    "Kontakt",                 "Contact"),
]

SK_TO_EN = {sk: en for sk, en, _, _ in PAGES}

# ── Titulky a popisy pre vyhľadávače ─────────────────────────────────────
META = {
    "index.html": (
        "BABYLAND – súkromná materská škola, Bratislava",
        "Súkromná materská škola rodinného typu v Bratislave. Rodinná atmosféra, "
        "malé skupinky, individuálny prístup a cudzí jazyk formou hier.",
        "BABYLAND – private kindergarten in Bratislava",
        "A family-run private kindergarten in Bratislava. A family atmosphere, small "
        "groups, an individual approach and a foreign language learned through play."),
    "ponuka.html": (
        "Ponuka – súkromná materská škola v Bratislave | BABYLAND",
        "Celodenná opatera v pondelok až piatok 7:30 – 17:30. Gustáva Mallého 2, "
        "851 01 Bratislava. Malé skupinky a odborný pedagogický personál.",
        "What we offer – private kindergarten in Bratislava | BABYLAND",
        "All-day care Monday to Friday, 7:30 – 17:30. Gustáva Mallého 2, 851 01 "
        "Bratislava. Small groups and qualified teaching staff."),
    "kurzy.html": (
        "Kurzy angličtiny pre deti od 3 rokov | BABYLAND Bratislava",
        "Kurzy anglického jazyka pre deti už od 3 rokov, cez týždeň aj cez víkendy. "
        "Angličtina a nemčina pre deti do 6 rokov, skupina pre deti do 2 rokov.",
        "English courses for children from age 3 | BABYLAND Bratislava",
        "English courses for children from the age of 3, on weekdays and at weekends. "
        "English and German for children up to 6, a group for children up to 2."),
    "filozofia.html": (
        "Naša filozofia | BABYLAND Bratislava",
        "Súkromná materská škola rodinného typu: maličké skupinky, individuálny prístup, "
        "rozvoj IQ aj EQ, jazyková výchova prirodzenou metódou a učenie formou hier.",
        "Our philosophy | BABYLAND Bratislava",
        "A family-run private kindergarten: very small groups, an individual approach, "
        "IQ and EQ alike, language learning by a natural method and learning through play."),
    "na-navsteve.html": (
        "Na návšteve u nás | BABYLAND Bratislava",
        "Fotografie z priestorov súkromnej materskej školy BABYLAND v Bratislave — "
        "herňa, výtvarné aktivity, voľná hra a pobyt vonku.",
        "A visit with us | BABYLAND Bratislava",
        "Photographs of the BABYLAND private kindergarten in Bratislava — the playroom, "
        "art activities, free play and time outdoors."),
    "kontakt.html": (
        "Kontakt – Gustáva Mallého 2, Bratislava | BABYLAND",
        "Kontakt na súkromnú materskú školu BABYLAND: Gustáva Mallého 2, "
        "851 01 Bratislava, telefón 0908 41 40 91, info@babyland-centrum.sk.",
        "Contact – Gustáva Mallého 2, Bratislava | BABYLAND",
        "Contact BABYLAND private kindergarten: Gustáva Mallého 2, 851 01 Bratislava, "
        "phone 0908 41 40 91, info@babyland-centrum.sk."),
}

# ── Prekladová mapa ──────────────────────────────────────────────────────
# Uplatňuje sa od najdlhšieho reťazca po najkratší (poradie v zozname teda
# nehrá rolu). Kľúč musí sedieť so slovenským HTML vrátane &nbsp; — tie sa
# z anglickej verzie odstránia až nakoniec. Na zalomení riadkov nezáleží.
TRANSLATE = [
    # ── úvodná stránka ──
    ("Súkromná materská škola BABYLAND –\n          rodinná atmosféra, malé skupinky a&nbsp;cudzí jazyk, ktorý sa deti učia\n          prirodzene, formou hier.",
     "BABYLAND private kindergarten — a family atmosphere, small groups and\n          a foreign language that children pick up naturally, through play."),
    ("Želáme pohodu a&nbsp;pokoj, úsmev vo vašom srdci i&nbsp;na tváričkách\n      všetkých tých, ktorých ľúbite. A&nbsp;to každý deň, každú chvíľu, ktorú nám život\n      ponúka. K&nbsp;vašej pohode chceme prispieť aj my našimi službami.",
     "We wish you calm and ease, a smile in your heart and on the faces of everyone\n      you love — every day, every moment life offers. We would like our work to add\n      to that ease of yours."),
    ("Kresba BABYLAND: usmiate slniečko, nápis BABYLAND a dve deti – dievčatko v oranžových šatách a chlapček v zelenom tričku",
     "The BABYLAND drawing: a smiling sun, the BABYLAND wordmark and two children — a girl in an orange dress and a boy in a green shirt"),
    ("Kde a&nbsp;kedy sme, aké formy opatery ponúkame a&nbsp;kto sa o&nbsp;deti stará.",
     "Where and when to find us, what care we offer and who looks after the children."),
    ("Angličtina a&nbsp;nemčina hravou formou – už od 3 rokov, cez týždeň aj cez víkendy.",
     "English and German through play — from the age of 3, on weekdays and at weekends."),
    ("Ako pristupujeme k&nbsp;výchove, čo rešpektujeme a&nbsp;prečo je u&nbsp;nás hra taká dôležitá.",
     "How we approach bringing children up, what we respect and why play matters so much here."),
    ("Radi privítame akékoľvek ďalšie otázky alebo pripomienky.\n      Na požiadanie vám radi povieme viac.",
     "We will be glad to answer any further questions or comments.\n      We will gladly tell you more on request."),
    ("Best for your child", "Best for your child"),
    ("…aby bolo vaše dieťa šťastné", "…so that your child is happy"),
    ("Rodinná atmosféra", "A family atmosphere"),
    ("Malé skupinky", "Small groups"),
    ("Profesionálny pedagóg", "A professional teacher"),
    ("Kde nás nájdete", "Where to find us"),
    ("Krásny deň!", "Have a lovely day!"),
    ("Čo u&nbsp;nás nájdete", "What you will find here"),
    ("Zobraziť ponuku", "See what we offer"),
    ("Zobraziť kurzy", "See the courses"),
    ("Čítať filozofiu", "Read our philosophy"),
    ("Tešíme sa na vašu návštevu", "We look forward to your visit"),

    # ── ponuka ──
    ("Kde nás nájdete, kedy máme otvorené, čo ponúkame a&nbsp;kto sa o&nbsp;deti stará.",
     "Where to find us, when we are open, what we offer and who looks after the children."),
    ("individuálny prístup k&nbsp;dieťatku", "an individual approach to every child"),
    ("rozvoj osobnosti, kreativity", "developing personality and creativity"),
    ("<span lang=\"en\">full time in English</span> – dieťa sa učí cudzí jazyk prirodzene, formou hier",
     "full time in English — the child picks the language up naturally, through play"),
    ("efektívne a&nbsp;bez problémov zvládne jazyk na komunikatívnej úrovni",
     "reaching a conversational level of the language easily and effectively"),
    ("výborný prístup autom", "easy to reach by car"),
    ("MHD v&nbsp;blízkosti", "public transport nearby"),
    ("V&nbsp;pondelok až piatok, 7:30 – 17:30 hod.", "Monday to Friday, 7:30 – 17:30."),
    ("– vysokoškolské pedagogické vzdelanie", "— a university degree in education"),
    ("– výborný prístup k&nbsp;deťom, schopnosť empatie, tvorivosť",
     "— a real way with children, empathy, creativity"),
    ("– dlhodobý pobyt v&nbsp;zahraničí alebo dlhoročné jazykové štúdium",
     "— a long stay abroad or years of language study"),
    ("– v&nbsp;medzinárodných materských školách, prípadne iných\n          špecializovaných školách, napríklad pre nadané deti",
     "— in international kindergartens, or other specialised\n          schools, for instance for gifted children"),
    ("Čo ponúkame", "What we offer"),
    ("rodinná atmosféra", "a family atmosphere"),
    ("profesionálny pedagóg", "a professional teacher"),
    ("malé skupinky", "small groups"),
    ("Formy opatery", "Forms of care"),
    ("Celodenná opatera", "All-day care"),
    ("Odborný pedagogický personál", "Qualified teaching staff"),
    ("Kritériá výberu:", "How we choose them:"),
    ("Vzdelanostné", "Education"),
    ("Osobnostné", "Character"),
    ("Jazykové", "Languages"),
    ("Prax", "Experience"),

    # ── kurzy ──
    ("Angličtina a&nbsp;nemčina hravou formou – malé skupinky, profesionálni učitelia.",
     "English and German through play — small groups, professional teachers."),
    ("Ponúkame kurzy anglického jazyka pre vaše deti – už od 3 rokov!",
     "English courses for your children — from the age of 3!"),
    ("Cez týždeň aj cez víkendy.", "On weekdays and at weekends."),
    ("Využívame vekové osobitosti a&nbsp;schopnosť dieťaťa učiť sa jazyk\n      prirodzene a&nbsp;ľahko. Investujte do budúcnosti svojho dieťaťa. My robíme všetko\n      preto, aby boli „naše“ deti šťastné.",
     "We make use of what children of this age do best — picking a language up\n      naturally and easily. Invest in your child's future. We do everything we can\n      for “our” children to be happy."),
    ("Každé stretnutie tematicky zamerané – učenie podporované hrou\n           a&nbsp;výtvarnými aktivitami.",
     "Each session has its own theme — learning supported by play\n           and art activities."),
    ("Aktuálne termíny, obsadenosť skupín\n      a&nbsp;ceny vám radi povieme telefonicky.",
     "We will gladly tell you the current dates, group availability\n      and prices over the phone."),
    ("Kurzy AJ pre deti", "English courses for children"),
    ("Garantujeme", "We guarantee"),
    ("profesionálnych učiteľov", "professional teachers"),
    ("príjemnú atmosféru", "a pleasant atmosphere"),
    ("učenie hrou", "learning through play"),
    ("Aktuálna ponuka", "Currently on offer"),
    ("Hravou formou spoznávame cudzí jazyk", "Getting to know a language through play"),
    ("Angličtina a&nbsp;nemčina", "English and German"),
    ("Pre deti do 6 rokov.", "For children up to the age of 6."),
    ("Skupina pre najmenších", "A group for the youngest"),
    ("Špeciálne pre deti do 2 rokov.", "Specially for children up to the age of 2."),
    ("Sobotné hravé dopoludnia", "Saturday play mornings"),

    # ── na návšteve ──
    ("Pár záberov z&nbsp;našich priestorov.", "A few pictures of our rooms."),
    ("Na návšteve u&nbsp;nás", "A visit with us"),
    ("Herňa centra BABYLAND – detský nábytok, police s hračkami a rastliny",
     "The BABYLAND playroom — children's furniture, shelves of toys and plants"),
    ("Deti sa hrajú na koberci s veľkým plyšovým medveďom",
     "Children playing on the rug with a large teddy bear"),
    ("Deti pri stole s pani učiteľkou počas výtvarných aktivít",
     "Children at the table with their teacher during art activities"),
    ("Deti sa hrajú vonku v pieskovisku", "Children playing outside in the sandpit"),
    ("Herňa", "The playroom"),
    ("Farebné priestory pre deti", "Colourful rooms for children"),
    ("Voľná hra", "Free play"),
    ("Spoločné hranie v&nbsp;malej skupinke", "Playing together in a small group"),
    ("Výtvarné aktivity", "Art activities"),
    ("Učenie podporované hrou", "Learning supported by play"),
    ("Pieskovisko", "The sandpit"),
    ("Pobyt na čerstvom vzduchu", "Time in the fresh air"),
    ("Tešíme sa na vašu návštevu.", "We look forward to your visit."),

    # ── kontakt ──
    ("Zriaďovateľ a&nbsp;fakturačné údaje", "Founder and company details"),
    ("Číslo živnostenského registra:", "Trade register number:"),
    ("Pekný deň! Tešíme sa na vašu návštevu.", "Have a nice day! We look forward to your visit."),
    ("Zavolajte nám", "Call us"),
    ("Napíšte nám", "Write to us"),
    ("Zobraziť na mape", "Show on the map"),
    ("Otváracie hodiny", "Opening hours"),
    ("IČO:", "Company ID (IČO):"),

    # ── filozofia ──
    ("Charakteristickým znakom vzdelávacej politiky EÚ je zvyšovanie kvality\n      vzdelávania – čo je aj naším cieľom.",
     "A defining feature of EU education policy is raising the quality of education —\n      which is our aim too."),
    ("I&nbsp;keď je situácia v&nbsp;oblasti rozvoja školstva na Slovensku taká,\n      aká je, potreba rodičov nájsť zariadenie s&nbsp;príjemnou atmosférou a&nbsp;čo\n      najlepšími podmienkami pre ich ratolesť tu je – prítomná a&nbsp;aktuálna.\n      Nepochybne dôležitý a&nbsp;náročný krok. Asi preto sme sa teraz stretli na týchto\n      stránkach. Sme radi, že k&nbsp;výchove svojho dieťatka pristupujete zodpovedne\n      a&nbsp;s&nbsp;láskou.",
     "Whatever the state of schooling in Slovakia may be, the need parents have to\n      find a place with a pleasant atmosphere and the best possible conditions for\n      their little one is very much here. It is an important and demanding step. That\n      is probably why we have met on these pages. We are glad you approach bringing\n      your child up responsibly and with love."),
    ("„Výber štátnej školy či obdobného alternatívneho súkromného\n        zariadenia? Ešte keby tak bolo v&nbsp;angličtine… a&nbsp;boli maličké skupinky,\n        kde sa môjmu drobcovi naozaj môžu venovať… a…“",
     "“A state school, or something alternative and private? If only it were in\n        English as well… and in very small groups, where they really can give my\n        little one their time… and…”"),
    ("Vznikom nášho zariadenia sa snažíme prispieť k&nbsp;zaplneniu bielych\n      miest. Chceme ponúkať to, čo vieme robiť dobre, a&nbsp;v&nbsp;podmienkach, ktoré si naše\n      deti zaslúžia. Ponúkame alternatívu – ak vyberáte pre svoje dieťatko materskú\n      školu, ale uprednostníte súkromné zariadenie rodinného typu, s&nbsp;jazykovým\n      vzdelaním, maličkými skupinkami, individuálnym prístupom, príjemnou atmosférou,\n      farebnými priestormi, možnosťou ďalších kurzov pre deti (napríklad tenis,\n      plávanie) a&nbsp;doplnkovými službami pre vás, rodičov…",
     "By opening our kindergarten we are trying to help fill in the blank spots. We\n      want to offer what we know how to do well, in the conditions our children\n      deserve. We offer an alternative — if you are choosing a kindergarten for your\n      little one but would rather have a family-run private one, with language\n      teaching, very small groups, an individual approach, a pleasant atmosphere,\n      colourful rooms, the option of further courses for children (tennis or swimming,\n      for instance) and extra services for you, the parents…"),
    ("Náš zámer:", "What we intend:"),
    ("ponúkať kvalitné komplexné služby. Ponúknuť vám,\n      rodičom, pre vaše deti to najlepšie. Pre ich žiarivé očká dnes a&nbsp;šťastnú\n      budúcnosť zajtra.",
     "to offer a complete service of real quality. To offer\n      you, the parents, the best for your children — for their bright eyes today and\n      a happy future tomorrow."),
    ("Súčasťou našej filozofie je nájsť v&nbsp;každom dieťati jeho potenciál\n      a&nbsp;tie formou hier rozvíjať v&nbsp;najširšej možnej miere. Kladieme dôraz na\n      komplexný rozvoj osobnosti a&nbsp;tvorivosti detí, pričom garantujeme individuálny\n      prístup ku každému dieťaťu – a&nbsp;to v&nbsp;príjemnej atmosfére spoluvytvorenej\n      deťmi a&nbsp;profesionálnymi skúsenými pedagógmi. Jazykovú výchovu prirodzenou\n      metódou a&nbsp;PC gramotnosť vnímame ako nevyhnutný predpoklad úspešnej\n      budúcnosti, preto sú nevyhnutnou samozrejmosťou nášho programu.",
     "Part of our philosophy is to find the potential in every child and to develop\n      it as far as it will go, through play. We put the emphasis on the child's whole\n      personality and creativity, and we guarantee an individual approach to each\n      one — in a pleasant atmosphere the children build together with professional,\n      experienced teachers. Language teaching by a natural method, and being at ease\n      with a computer, we see as necessary for a successful future, so both are a\n      matter of course in our programme."),
    ("Rešpektujeme Štátny vzdelávací program pre predprimárne\n      vzdelávanie,\n      a&nbsp;to ako otvorený dokument prezentujúci základné a&nbsp;rámcové smerovanie,\n      dopĺňajúc ho o&nbsp;najnovšie trendy z&nbsp;pedagogického výskumu a&nbsp;praxe\n      u&nbsp;nás i&nbsp;v&nbsp;zahraničí.",
     "We follow the Slovak State Educational Programme for pre-primary education as\n      an open document setting out the basic direction, and add to it the newest\n      thinking from research and practice at home and abroad."),
    ("Vysoká kvalita výchovno-vzdelávacieho procesu bude zabezpečená",
     "High quality in teaching and care is secured by"),
    ("dôsledným výberom pedagógov – s&nbsp;dôrazom na ich vzdelanostný, ale aj osobnostný potenciál",
     "choosing teachers carefully — for what they know, but for who they are as well"),
    ("garantovaním nízkych počtov detí v&nbsp;skupine", "guaranteeing low numbers of children per group"),
    ("využívaním alternatívnych výchovno-vzdelávacích metód", "using alternative teaching methods"),
    ("kvalitnými materiálno-didaktickými prostriedkami a&nbsp;technickým zabezpečením školy",
     "good teaching materials and equipment"),
    ("medzinárodnou spoluprácou – nadviazaním kontaktov s&nbsp;partnerskými školami v&nbsp;zahraničí",
     "working internationally — building contacts with partner schools abroad"),
    ("individuálnym prístupom a&nbsp;podporou talentovaných detí",
     "an individual approach and support for gifted children"),
    ("rozvojom IQ aj EQ, komplexným rozvojom osobnosti, posilneným rozvojom kreativity a&nbsp;sociálnych zručností",
     "developing IQ and EQ alike, the whole personality, and creativity and social skills in particular"),
    ("dôrazom na podporu maximálneho rozvoja konkrétnych špecifických schopností u&nbsp;každého dieťaťa",
     "supporting each child's particular abilities as far as they will go"),
    ("environmentálnou, morálnou a&nbsp;multikultúrnou výchovou, výchovou k&nbsp;zdravému životnému štýlu",
     "environmental, moral and multicultural education, and education towards a healthy way of life"),
    ("Cieľom jazykovej prípravy je zvládnuť cudzí jazyk na komunikatívnej úrovni.",
     "The aim of the language teaching is a conversational command of the language."),
    ("Z&nbsp;moderných trendov v&nbsp;školstve rešpektujeme", "Of the modern trends in education, we follow"),
    ("individuálny prístup", "an individual approach"),
    ("prácu s&nbsp;malými skupinkami detí", "working with small groups of children"),
    ("rodinnú atmosféru", "a family atmosphere"),
    ("rozvoj osobnosti, emocionálnej inteligencie, tvorivosti",
     "developing personality, emotional intelligence and creativity"),
    ("zavádzanie sociálneho kurikula, ktoré obsahuje prax v&nbsp;riešení životných situácií, najmä konfliktov, učenie sa zodpovednosti a&nbsp;spoločenským normám",
     "a social curriculum — practice in handling everyday situations, conflicts above all, and learning responsibility and how people behave together"),
    ("zvýrazňuje sa výchova charakteru – podporuje sa, aby sa dieťa učilo kritickému mysleniu, hodnotám, morálke",
     "an emphasis on character — encouraging the child towards critical thinking, values and morals"),
    ("výchovu k&nbsp;zdravému životnému štýlu, environmentálnu výchovu",
     "education towards a healthy way of life, and environmental education"),
    ("primárne učenie sa formou hier a&nbsp;experimentovania a&nbsp;metód praktickej činnosti",
     "learning first of all through play, experiment and hands-on activity"),
    ("presadzovanie kooperatívneho vyučovania", "co-operative teaching"),
    ("učenie sa cudzím jazykom", "learning foreign languages"),
    ("podporu PC gramotnosti", "being at ease with a computer"),
    ("uplatňuje sa multikultúrna výchova", "multicultural education"),
    ("Hra má u&nbsp;nás významné postavenie", "Play has an important place here"),
    ("Vnímame ju ako prostriedok, pomocou ktorého sa cielene rozvíjajú\n        jednotlivé štrukturálne znaky osobnosti dieťaťa.",
     "We see it as the means by which the separate parts of a child's personality\n        are deliberately developed."),
    ("Tvorivá hra", "Creative play"),
    ("Dáva dieťaťu príležitosť vlastného vyjadrenia, umožňuje mu prežívať radosť\n           z&nbsp;vnútorného prejavu, čo rozvíja jeho samostatnosť, motiváciu, fantáziu\n           a&nbsp;imagináciu, učí ho riešiť problémy a&nbsp;zoznamuje sa s&nbsp;pocitom\n           zodpovednosti.",
     "Gives the child a chance to express itself and to feel the joy of doing so,\n           which builds independence, motivation and imagination, teaches it to solve\n           problems and introduces it to the feeling of responsibility."),
    ("Didaktická hra", "Didactic play"),
    ("Prináša predovšetkým určité poznanie.", "Brings knowledge above all."),
    ("Výchovná hra", "Educational play"),
    ("Kladie dôraz na prežívanie, zážitky a&nbsp;skúsenosť.",
     "Puts the emphasis on living something through, and on experience."),
    ("Predpokladáme, že doceníte kvalitné vzdelanie pre svoje dieťa. Ak sme si\n      názorovo blízki v&nbsp;myšlienkach o&nbsp;výchove a&nbsp;vyhovujú vám podmienky,\n      ktoré ponúkame – či chcete sa dozvedieť o&nbsp;nás viac – prosím, kontaktujte nás\n      telefonicky alebo e-mailom.",
     "We assume a good education for your child matters to you. If we think alike\n      about bringing children up and the conditions we offer suit you — or if you\n      would like to know more about us — please call or e-mail us."),
    ("Radi spolu s&nbsp;vami budeme vytvárať svet, v&nbsp;ktorom bude vaše\n      dieťa šťastné a&nbsp;vy spokojní.",
     "We will be glad to build, together with you, a world in which your child is\n      happy and you are content."),
    ("Naša filozofia", "Our philosophy"),
    ("Kvalita", "Quality"),
    ("Moderné trendy", "Modern trends"),
    ("Hra", "Play"),

    # ── spoločné (na konci, aby neprepísali dlhšie vety vyššie) ──
    ("Domov", "Home"),
    ("Ponuka", "What we offer"),
    ("Kontakt", "Contact"),
    ("Kde", "Where"),
    ("Kedy", "When"),
    ("Čo", "What"),
    ("Kto", "Who"),
    ("Pondelok – Piatok", "Monday – Friday"),
    ("Súkromná materská škola", "Private kindergarten"),
    ("tel.", "tel."),
]


PHONE_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')

WORDS = {
    "sk": dict(lang="sk", locale="sk_SK", other="en", other_label="English",
               home="domov", nav="Hlavná navigácia", skip="Preskočiť na obsah",
               tag="Súkromná materská škola", pages="Stránky", contact="Kontakt",
               hours="Po – Pi: 7:30 – 17:30", ico="IČO",
               about=("Súkromná materská škola rodinného typu v&nbsp;Bratislave. Malé skupinky, "
                      "individuálny prístup a&nbsp;cudzí jazyk, ktorý sa deti učia prirodzene – formou hier.")),
    "en": dict(lang="en", locale="en_GB", other="sk", other_label="Slovensky",
               home="home", nav="Main navigation", skip="Skip to content",
               tag="Private kindergarten", pages="Pages", contact="Contact",
               hours="Mon – Fri: 7:30 – 17:30", ico="Company ID",
               about=("A family-run private kindergarten in Bratislava. Small groups, an "
                      "individual approach and a foreign language that children pick up "
                      "naturally — through play.")),
}


def head(page, lang, title, desc, extra=""):
    """Zloží <head> stránky vrátane odkazu na druhú jazykovú verziu.

    :param page:  cesta od koreňa webu, napr. "ponuka.html" alebo "en/offer.html"
    :param lang:  "sk" alebo "en"
    :param title: titulok stránky
    :param desc:  popis pre vyhľadávače
    :param extra: doplnkový obsah pred </head> (napr. blok JSON-LD)
    :returns:     HTML od <!DOCTYPE> po <body>
    """
    w = WORDS[lang]
    up = "../" if page.startswith("en/") else ""
    url = DOMAIN + ("" if page in ("index.html",) else page)
    # Partnerská stránka v druhom jazyku. Chybová stránka ju nemá — server ju
    # vracia pre každú neexistujúcu adresu, nech je v ktoromkoľvek jazyku.
    name = page.split("/")[-1]
    has_pair = name in SK_TO_EN or name in SK_TO_EN.values()
    if not has_pair:
        alt_block = ""
    else:
        if lang == "sk":
            alt = "en/" + SK_TO_EN[name]
        else:
            alt = {v: k for k, v in SK_TO_EN.items()}[name]
        alt_url = DOMAIN + ("" if alt == "index.html" else alt)
        alt_block = (f'\n  <link rel="alternate" hreflang="{w["other"]}" href="{alt_url}">'
                     f'\n  <link rel="alternate" hreflang="{w["lang"]}" href="{url}">'
                     f'\n  <link rel="alternate" hreflang="x-default" href="{DOMAIN}">')
    return f"""<!DOCTYPE html>
<html lang="{w['lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.className+=" js";</script>
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#5A3312">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{w['locale']}">
  <meta property="og:site_name" content="BABYLAND">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}assets/img/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{DOMAIN}assets/img/og-image.png">
  <link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
  <link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
  <link rel="manifest" href="{up}site.webmanifest">
  <link rel="preload" href="{up}css/styles.css" as="style">
  <link rel="stylesheet" href="{up}css/styles.css">{alt_block}{extra}
</head>
<body>
<a class="skip-link" href="#obsah">{w['skip']}</a>
"""


def header(current, lang):
    """Hlavička s menu. Menu má v oboch jazykoch rovnaké položky v rovnakom poradí.

    :param current: názov súboru aktuálnej stránky, napr. "offer.html"
    :param lang:    "sk" alebo "en"
    :returns:       HTML bloku <header>
    """
    w = WORDS[lang]
    up = "../" if lang == "en" else ""
    items = []
    for sk_file, en_file, sk_label, en_label in PAGES:
        href = sk_file if lang == "sk" else en_file
        label = sk_label if lang == "sk" else en_label
        mark = ' aria-current="page"' if href == current else ""
        items.append(f'      <a href="{href}"{mark}>{label}</a>')
    other = "en/index.html" if lang == "sk" else "../index.html"
    items.append(f'      <a class="nav-lang" href="{other}" lang="{w["other"]}" '
                 f'hreflang="{w["other"]}">{w["other_label"]}</a>')
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="BABYLAND – {w['home']}">
      <img class="brand__mark" src="{up}assets/logo-mark.svg" alt="" width="40" height="40">
      <span class="brand__text">
        <img class="brand__word" src="{up}assets/logo-babyland.svg" alt="" width="535" height="84">
        <span class="brand__tag">{w['tag']}</span>
      </span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="{w['nav']}">
{chr(10).join(items)}
    </nav>
    <div class="header-actions">
      <a class="header-phone" data-mh-tel href="tel:+421908414091">{PHONE_SVG}<span data-mh="business.phone">0908 41 40 91</span></a>
      <button class="nav-toggle" aria-label="Menu" aria-controls="main-nav" aria-expanded="false">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
  </div>
</header>
"""


def footer(lang):
    """Pätička. V oboch jazykoch rovnaké bloky a rovnaké odkazy.

    :param lang: "sk" alebo "en"
    :returns:    HTML bloku <footer>
    """
    w = WORDS[lang]
    other = WORDS["en" if lang == "sk" else "sk"]
    up = "../" if lang == "en" else ""
    to_other = "en/" if lang == "sk" else "../"

    own, cross = [], []
    for sk_file, en_file, sk_label, en_label in PAGES:
        here = (sk_file, sk_label) if lang == "sk" else (en_file, en_label)
        there = (en_file, en_label) if lang == "sk" else (sk_file, sk_label)
        own.append(f'          <li><a href="{here[0]}">{here[1]}</a></li>')
        cross.append(f'          <li><a href="{to_other}{there[0]}" lang="{w["other"]}" '
                     f'hreflang="{w["other"]}">{there[1]}</a></li>')

    legal = ('<span data-mh="business.name">' if lang == "sk"
             else '<span lang="sk" data-mh="business.name">')
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <span class="brand">
          <img class="brand__mark" src="{up}assets/logo-mark.svg" alt="" width="40" height="40">
          <span class="brand__text">
            <img class="brand__word" src="{up}assets/logo-babyland.svg" alt="" width="535" height="84">
            <span class="brand__tag">{w['tag']}</span>
          </span>
        </span>
        <p>{w['about']}</p>
      </div>

      <div>
        <h2>{w['pages']}</h2>
        <ul class="footer-links">
{chr(10).join(own)}
        </ul>
      </div>

      <div>
        <h2>{other['other_label'] if lang == 'en' else 'English'}</h2>
        <ul class="footer-links">
{chr(10).join(cross)}
        </ul>
      </div>

      <div>
        <h2>{w['contact']}</h2>
        <div class="footer-contact">
          <p><a data-mh-tel href="tel:+421908414091"><span data-mh="business.phone">0908 41 40 91</span></a></p>
          <p><a data-mh-mail href="mailto:info@babyland-centrum.sk"><span data-mh="business.email">info@babyland-centrum.sk</span></a></p>
          <p><span data-mh="business.showroom.full">Gustáva Mallého 2, 851 01 Bratislava</span></p>
          <p><span{' data-mh="business.hoursShort"' if lang == 'sk' else ''}>{w['hours']}</span></p>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>© <span data-mh-year>2026</span> {legal}Mgr. Jana Kamenská – 1. súkromné opatrovateľské centrum BABYLAND</span>,
         {w['ico']} <span data-mh="business.ico">40 646 149</span></p>
    </div>
  </div>
</footer>
<script src="{up}js/config.js"></script>
<script src="{up}js/main.js"></script>
</body>
</html>
"""


# jednopísmenové predložky a spojky, po ktorých nesmie riadok zalomiť
SK_ONE_LETTER = "aiouvszkAIOUVSZK"


def sk_typography(html):
    """Doladí slovenskú typografiu — pomlčky a nezalomiteľné medzery.

    Robí dve veci:

      1. dlhú pomlčku „—" nahradí pomlčkou „–"; slovenská norma STN 01 6910
         dlhú pomlčku nepozná, tá patrí do angličtiny
      2. po jednopísmenovej predložke alebo spojke vloží nezalomiteľnú
         medzeru, aby písmeno nezostalo visieť na konci riadka

    Nezalomiteľné medzery sa vkladajú len do textu medzi značkami — nie do
    atribútov ani do hlavičky <head> — a nie do textu označeného lang="en",
    ktorý je v pätičke (odkazy na anglickú verziu).

    :param html: celá stránka ako reťazec
    :returns:    tá istá stránka s upravenou typografiou
    """
    scripts = []

    def stash(m):
        scripts.append(m.group(0))
        return "\x00S%d\x00" % (len(scripts) - 1)

    html = re.sub(r"<script\b.*?</script>", stash, html, flags=re.S)
    html = re.sub(r"(?<=\s)—(?=\s)", "–", html)

    head_part, sep, body = html.partition("<body")
    if sep:
        pattern = re.compile(r"(^|[\s(„]|&nbsp;)([" + SK_ONE_LETTER + r"]) (?=[^\s<])")

        def fix(text):
            while True:
                fixed = pattern.sub(r"\1\2&nbsp;", text)
                if fixed == text:
                    return text
                text = fixed

        parts, in_en = [], 0
        for part in re.split(r"(<[^>]*>)", body):
            if part.startswith("<"):
                if 'lang="en"' in part:
                    in_en += 1
                elif in_en and part.startswith("</"):
                    in_en -= 1
                parts.append(part)
            else:
                parts.append(part if in_en else fix(part))
        html = head_part + sep + "".join(parts)

    for i, original in enumerate(scripts):
        html = html.replace("\x00S%d\x00" % i, original)
    return html


def to_english(main_html):
    """Preloží obsah slovenskej stránky do angličtiny.

    Štruktúra HTML zostáva nedotknutá — menia sa len texty, cesty k súborom
    a odkazy medzi stránkami. Tým je zaručené, že obe verzie vyzerajú rovnako.

    :param main_html: obsah <main> slovenskej stránky
    :returns:         ten istý obsah v angličtine
    """
    out = main_html
    # Od najdlhšieho po najkratší: „Kde nás nájdete" je začiatkom vety
    # „Kde nás nájdete, kedy máme otvorené…", a keby sa uplatnilo skôr,
    # rozbilo by ju. Poradie v mape tak nemusí nikto strážiť.
    for sk, en in sorted(TRANSLATE, key=lambda pair: -len(pair[0])):
        # Zhoda sa hľadá bez ohľadu na to, kde je text v HTML zalomený —
        # inak by stačilo presunúť jedno slovo na ďalší riadok a preklad by
        # sa prestal uplatňovať, ticho a bez chyby.
        pattern = r"\s+".join(re.escape(part) for part in sk.split())
        out = re.sub(pattern, lambda m, en=en: en, out)

    # odkazy na slovenské stránky → anglické náprotivky
    for sk_file, en_file, _, _ in PAGES:
        out = out.replace(f'href="{sk_file}"', f'href="{en_file}"')

    # obrázky a ostatné súbory sú o priečinok vyššie
    out = re.sub(r'(src|href)="(assets/)', r'\1="../\2', out)

    # Tabuľku hodín na anglických stránkach nevypĺňa JavaScript — v config.js
    # sú slovenské názvy dní. Zostáva napísaná priamo v HTML.
    out = out.replace(' data-mh-hours', '')

    # V angličtine sa nezalomiteľné medzery po jednopísmenových slovách
    # nepoužívajú (to je pravidlo slovenskej typografie).
    out = out.replace("&nbsp;", " ")
    return out


def check_no_slovak(page, main_html):
    """Nájde text, ktorý ostal po preklade slovenský.

    Hľadá slová s písmenami, ktoré angličtina nepozná. Vlastné mená a texty
    označené lang="sk" sú v poriadku a preskakujú sa.

    :param page:      názov stránky (do hlásenia)
    :param main_html: preložený obsah <main>
    :returns:         zoznam podozrivých slov
    """
    allowed = {"Gustáva", "Mallého", "Bratislava", "Kamenská", "Jána", "Kostku",
               "Malacky", "BABYLAND", "IČO", "Mgr", "súkromné", "opatrovateľské",
               "centrum", "Súkromná", "materská", "škola"}
    text = re.sub(r'<(script|style|svg)\b.*?</\1>', " ", main_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    bad = []
    for word in re.findall(r"[A-Za-zÀ-ž]+", text):
        if word in allowed:
            continue
        if re.search(r"[ áäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ]".replace(" ", ""), word):
            bad.append(word)
    return sorted(set(bad))


JSONLD = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Preschool",
    "@id": "https://www.babyland-centrum.sk/#babyland",
    "name": "BABYLAND – súkromná materská škola",
    "legalName": "Mgr. Jana Kamenská – 1. súkromné opatrovateľské centrum BABYLAND",
    "url": "https://www.babyland-centrum.sk/",
    "image": "https://www.babyland-centrum.sk/assets/img/og-image.png",
    "logo": "https://www.babyland-centrum.sk/assets/logo-mark.svg",
    "telephone": "+421908414091",
    "email": "info@babyland-centrum.sk",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Gustáva Mallého 2",
      "addressLocality": "Bratislava",
      "postalCode": "851 01",
      "addressCountry": "SK"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 48.1208342,
      "longitude": 17.0963077
    },
    "openingHoursSpecification": [{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:30",
      "closes": "17:30"
    }]
  }
  </script>"""


ERROR_PAGE = """
<section class="section">
  <div class="container container--narrow text-center">
    <div class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
    <h1>Túto stránku sa nám nepodarilo nájsť</h1>
    <p class="lead mt-1">Možno sa presunula alebo ste sa preklikli.
      Skúste to z&nbsp;úvodnej stránky.</p>
    <p class="mt-2">
      <a class="btn btn--primary btn--lg" href="index.html">Späť na úvod</a>
      <a class="btn btn--secondary btn--lg" href="kontakt.html">Kontakt</a>
    </p>
  </div>
</section>
"""


def write_error_page():
    """Chybová stránka. Nemá anglický náprotivok — server ju vracia pre každú
    neexistujúcu adresu bez ohľadu na jazyk — a preto ani odkaz hreflang."""
    title = "Stránka sa nenašla | BABYLAND"
    desc = "Požadovaná stránka neexistuje. Prejdite na úvodnú stránku škôlky BABYLAND."
    page = head("404.html", "sk", title, desc,
                extra='\n  <meta name="robots" content="noindex">')
    return sk_typography(page + header("404.html", "sk")
                         + '<main id="obsah" tabindex="-1">' + ERROR_PAGE + "</main>\n"
                         + footer("sk"))


def main():
    problems = []
    written = []

    for sk_file, en_file, _, _ in PAGES:
        source = (ROOT / sk_file).read_text(encoding="utf-8")
        body = re.search(r"<main[^>]*>(.*?)</main>", source, re.S).group(1)
        sk_title, sk_desc, en_title, en_desc = META[sk_file]
        extra = JSONLD if sk_file == "index.html" else ""

        # slovenská stránka: obsah ostáva, mení sa len hlavička a pätička
        (ROOT / sk_file).write_text(sk_typography(
            head(sk_file, "sk", sk_title, sk_desc, extra)
            + header(sk_file, "sk")
            + '<main id="obsah" tabindex="-1">' + body + "</main>\n"
            + footer("sk")), encoding="utf-8")
        written.append(sk_file)

        # anglická stránka: ten istý obsah, preložený
        en_body = to_english(body)
        left = check_no_slovak(en_file, en_body)
        if left:
            problems.append(f"en/{en_file}: nepreložené — {', '.join(left[:8])}")
        (ROOT / "en" / en_file).write_text(
            head("en/" + en_file, "en", en_title, en_desc, extra)
            + header(en_file, "en")
            + '<main id="obsah" tabindex="-1">' + en_body + "</main>\n"
            + footer("en"), encoding="utf-8")
        written.append("en/" + en_file)

    (ROOT / "404.html").write_text(write_error_page(), encoding="utf-8")
    written.append("404.html")

    print(f"Zapísaných stránok: {len(written)}")
    for name in written:
        print("  ", name)
    if problems:
        print("\n### NEPRELOŽENÉ ZVYŠKY\n")
        for p in problems:
            print("  -", p)
        return 1
    print("\n✅ V anglickej verzii neostal slovenský text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
