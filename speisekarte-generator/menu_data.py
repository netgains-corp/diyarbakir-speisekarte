# -*- coding: utf-8 -*-
# Inhalt 1:1 von https://diyarbakir-ocakbasi.pages.dev (Stand 13.07.2026), neu durchnummeriert.
# item: (nr, name, note, allergene, icons, preis, beschreibung)
# icons: v = vegetarisch (Blatt), s = scharf (Chili)

RESTAURANT = {
    "name": "DIYARBAKIR RESTAURANT",
    "subtitle": "",
    "address": ["Bleichstraße 33", "65183 Wiesbaden"],
    "phone": ["0611 56598008"],
    "tagline": "Gutes Essen, gute Freunde, gute Atmosphäre\n— das ist Diyarbakir",
    "welcome": "Herzlich willkommen in unserem Restaurant. Seit Jahren servieren wir traditionelle Speisen vom Holzkohlegrill und aus dem Holzofen.",
    "hours": "Mo – So: 11:00 – 00:00 Uhr",
    "quality": "Unser Drehspieß – frisch geschnitten, direkt vom Grill",
}

SECTIONS = [
    {
        "id": "suppen", "title": "SUPPEN",
        "items": [
            (1, "Linsensuppe", "", "6", "v", "7,00 €", ""),
            (2, "Tagessuppe", "", "6", "", "8,50 €", ""),
        ],
    },
    {
        "id": "meze", "title": "VORSPEISEN",
        "items": [
            (3, "Haydari", "", "1, 4, 6, 8", "v", "8,00 €", "Weichkäse, griechischer Joghurt, Gewürze und Olivenöl"),
            (4, "Yoğurtlu Patlıcan Ezme", "", "1, 4, 6, 8", "v", "8,00 €", "Gebratene und kleingehackte Auberginen mit griechischem Joghurt und Olivenöl"),
            (5, "Acılı Ezme", "(pikant)", "1, 6, 8", "sv", "8,00 €", "Frisches Gemüse, Walnüsse und Olivenöl"),
            (6, "Karışık Meze", "", "1, 4, 6, 8", "", "9,00 €", "Gemischter Vorspeisen-Teller"),
            (7, "Çiğ Köfte", "", "1, 4, 6, 8", "v", "10,00 €", "10 vegetarische rohe Frikadellenbällchen"),
        ],
    },
    {
        "id": "salate", "title": "SALATE",
        "note": "Salat-Dressings: Joghurt-Sauce · Knoblauch-Sauce · Olivenöl · Balsamico · Granatapfelsirup",
        "items": [
            (8, "Beilagen Salat", "", "1, 6, 8", "v", "5,00 €", "Eisbergsalat, Weißkraut, Tomaten, Gurken, Zwiebeln und Sauce"),
            (9, "Gemischter Salat", "", "1, 6, 8", "v", "7,00 €", "Eisbergsalat, Weißkraut, Tomaten, Gurken, Zwiebeln, Oliven und Sauce"),
            (10, "Bauernsalat", "", "1, 6, 8", "v", "8,00 €", "Eisbergsalat, Weißkraut, Tomaten, Gurken, Zwiebeln, Oliven, Weichkäse und Sauce"),
            (11, "Dönersalat", "", "1, 6, 8", "", "10,00 €", "Eisbergsalat, Weißkraut, Tomaten, Gurken, Zwiebeln, Dönerfleisch und Sauce"),
            (12, "Thunfischsalat", "", "1, 6, 8", "", "10,00 €", "Eisbergsalat, Weißkraut, Tomaten, Gurken, Zwiebeln, Oliven, Weichkäse, Thunfisch und Sauce"),
        ],
    },
    {
        "id": "grill", "title": "VOM HOLZKOHLEGRILL",
        "note": "Inkl. Beilagen Salat, Brot und wahlweise Bulgur, Pommes oder Reis",
        "items": [
            (13, "Adana Kebab", "", "1, 8", "s", "14,50 €", "2 Lammhackfleischspieße, gegrillte Tomaten und Peperoni"),
            (14, "Urfa Kebab", "", "1, 8", "", "14,50 €", "2 Lammhackfleischspieße, gegrillte Tomaten und Peperoni"),
            (15, "Tavuk Şiş", "", "1, 8", "", "14,50 €", "2 Hähnchenspieße mit gegrillten Tomaten und Peperoni"),
            (16, "Tavuk Kanat", "", "1, 8", "", "14,50 €", "1 Hähnchenflügelspieß mit gegrillten Tomaten und Peperoni"),
            (17, "Adana mit Joghurtsoße", "", "1, 2, 4, 6, 8", "s", "15,50 €", "2 Lammhackfleischspieße, gegrillte Tomaten, Peperoni auf Pidewürfeln mit Butter und pikanter Tomatensoße"),
            (18, "Kuzu Şiş", "", "1, 8", "", "20,00 €", "2 Lammspieße mit gegrillten Tomaten und Peperoni"),
            (19, "Beyti Kebab", "", "1, 2, 4, 6, 8", "", "17,00 €", "Lammhackfleischspieß gerollt in Dürüm, mit Joghurt-Butter-Tomatenmark-Soße"),
            (20, "Döner Beyti Kebab", "", "1, 2, 4, 8", "", "15,50 €", "Dönerfleisch gerollt in Dürüm, mit Joghurt-Butter-Tomatenmark-Soße"),
            (21, "Ali Nazik", "", "1, 2, 4, 6, 8", "", "20,00 €", "2 Lammspieße mit gegrillten Auberginen und Joghurt-Butter-Tomatenmark-Soße"),
            (22, "Kuzu Pirzola", "", "1, 8", "", "21,00 €", "4 Lammkoteletts mit gegrillten Tomaten und Peperoni"),
            (23, "Karışık Izgara", "", "1, 8", "", "1P 20,00 € · 2P 38,50 € · 4P 75,00 €", "1 Lammhackfleischspieß, 1 Lammspieß, 1 Hähnchenspieß und 1 Lammkotelett"),
        ],
    },
    {
        "id": "pizza", "title": "AUS DEM HOLZOFEN – PIZZA",
        "note": "Pizza ca. 30 cm · Grundbelag: Tomatensoße & Käse",
        "extras": "Extras: Fleischbelag +1,00 € · Gemüse oder Käse +1,00 €",
        "items": [
            (24, "Margherita", "", "3, 6, 8", "v", "7,50 €", ""),
            (25, "Putensalami", "", "3, 6, 8", "", "8,50 €", ""),
            (26, "Pepperoniwurst", "", "3, 6, 8", "s", "8,50 €", ""),
            (27, "Putenschinken", "", "3, 6, 8", "", "8,50 €", ""),
            (28, "Champignons", "", "3, 6, 8", "v", "8,50 €", ""),
            (29, "Vegetarisch", "", "3, 6, 8", "v", "8,50 €", "Zwiebeln, Champignons, Tomaten, Oliven und Mais"),
            (30, "Hawaii", "", "3, 6, 8", "", "9,50 €", "Putenschinken und Ananas"),
            (31, "Mafia", "", "3, 6, 8", "s", "9,50 €", "Putensalami, Putenschinken und scharfe Peperoni"),
            (32, "Calzone", "", "3, 6, 8", "", "9,50 €", "Putensalami, Putenschinken, Champignons und Paprika"),
            (33, "Thunfisch", "", "3, 6, 8", "", "9,50 €", "Thunfisch und Zwiebeln"),
            (34, "Sucuk m. Champignons", "", "3, 6, 8", "s", "9,50 €", "Sucuk und Champignons"),
            (35, "Mozzarella", "", "3, 6, 8", "v", "9,50 €", "Tomaten und Mozzarella"),
            (36, "Diyarbakır", "", "3, 6, 8", "", "9,50 €", "Dönerfleisch und Zwiebeln"),
            (37, "Gorgonzola", "", "3, 6, 8", "v", "9,50 €", "Gorgonzola und Spinat"),
            (38, "4 Käse", "", "3, 6, 8", "v", "9,50 €", "4 verschiedene Käsesorten"),
            (39, "Wiesbaden", "", "3, 6, 8", "s", "9,50 €", "Putensalami, Peperoniwurst, Putenschinken, Champignons und Zwiebeln"),
            (40, "Familien Pizza", "50×50 cm", "3, 6, 8", "", "25,00 €", "Tomatensoße, Käse und 3 weitere Zutaten nach Wahl · jede weitere Zutat 2,00 €"),
        ],
    },
    {
        "id": "doener", "title": "DÖNER KEBAB & BOX",
        "items": [
            (41, "Kinder-mini Döner", "", "2, 3, 6, 8", "", "6,00 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (42, "Döner Kebab", "", "2, 3, 6, 8", "", "7,00 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (43, "Döner m. Extra Fleisch", "", "2, 3, 6, 8", "", "8,00 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (44, "Döner Teller", "", "2, 6, 8", "", "13,00 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße · dazu Bulgur, Pommes oder Reis"),
            (45, "İskender Kebab", "", "1, 2, 4, 6, 8", "", "15,00 €", "Dönerfleisch, gegrillte Tomaten, Peperoni auf Pidewürfeln mit Butter, Joghurtsoße und Tomatensoße"),
            (46, "Döner Box", "", "2, 6, 8", "", "7,00 €", "Dönerfleisch und Soße · dazu Bulgur, Pommes, Reis oder Salat"),
        ],
    },
    {
        "id": "duerum", "title": "DÜRÜM & LAHMACUN",
        "items": [
            (47, "Döner Dürüm", "", "2, 3, 6, 8", "", "7,50 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (48, "Adana Dürüm", "", "2, 3, 6, 8", "", "9,00 €", "1 Lammhackfleischspieß, grüner Salat, Weißkraut, Tomaten und Zwiebeln"),
            (49, "Tavuk Şiş Dürüm", "", "2, 3, 6, 8", "", "9,00 €", "1 Hähnchenspieß, grüner Salat, Weißkraut, Tomaten und Zwiebeln"),
            (50, "Kuzu Şiş Dürüm", "", "2, 3, 6, 8", "", "12,00 €", "1 Lammspieß, grüner Salat, Weißkraut, Tomaten und Zwiebeln"),
            (51, "Lahmacun", "", "2, 3, 6, 8", "", "6,00 €", "Grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (52, "Döner Lahmacun", "", "2, 3, 6, 8", "", "8,50 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (53, "Diyarbakır Lahmacun Teller", "", "2, 3, 6, 8", "", "11,00 €", "Dönerfleisch, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
        ],
    },
    {
        "id": "pide", "title": "PIDE",
        "items": [
            (54, "Pide", "", "3, 6, 8", "v", "10,00 €", "Käse und Weichkäse"),
            (55, "Ispanaklı", "", "3, 6, 8", "v", "11,00 €", "Käse, Weichkäse und Spinat"),
            (56, "Kıymalı", "", "3, 6, 8", "", "11,00 €", "Lammhackfleisch und Käse"),
            (57, "Sucuk", "", "3, 6, 8", "s", "11,00 €", "Käse und Sucuk"),
            (58, "Döner Pide", "", "3, 6, 8", "", "11,00 €", "Dönerfleisch, Käse und Weichkäse"),
        ],
    },
    {
        "id": "veg", "title": "VEGETARISCHES & BEILAGEN",
        "items": [
            (59, "Vegetarisches Sandwich", "", "2, 3, 6, 8", "v", "6,00 €", "Weichkäse, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (60, "Çiğ Köfte Dürüm", "", "2, 3, 6, 8", "v", "6,00 €", "Vegetarische rohe Frikadellen, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (61, "Vegetarischer Dürüm", "", "2, 3, 6, 8", "v", "6,50 €", "Weichkäse, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (62, "Falafel Sandwich", "", "2, 3, 6, 8", "v", "6,00 €", "Falafel, grüner Salat, Weißkraut, Tomaten, Zwiebeln und Soße"),
            (63, "Falafel Teller", "", "2, 3, 6, 8", "v", "10,00 €", "6 Falafel, grüner Salat, Weißkraut, Tomaten, Zwiebeln, Soße und wahlweise Reis, Bulgur oder Pommes"),
            (64, "Beilagen", "", "", "v", "ab 5,00 €", "Bulgur / Pommes / Reis"),
        ],
    },
    {
        "id": "desserts", "title": "DESSERTS",
        "items": [
            (65, "Baklava", "", "", "v", "5,00 €", "3 gefüllte Blätterteigtaschen mit Nussfüllung"),
            (66, "Katmer", "", "", "v", "7,50 €", ""),
            (67, "Milchreis", "", "", "v", "3,50 €", ""),
            (68, "Künefe", "", "", "v", "7,50 €", "Teigspirale mit Käse, im Ofen gebacken"),
            (69, "Layali Lubnan", "", "", "v", "3,50 €", ""),
        ],
    },
    {
        "id": "heiss", "title": "GETRÄNKE",
        "subtitle": "Heiße Getränke",
        "items": [
            (70, "Tee", "", "", "", "2,50 €", ""),
            (71, "Kaffee", "", "", "", "2,50 €", ""),
            (72, "Espresso", "", "", "", "2,50 €", ""),
            (73, "Cappuccino", "", "", "", "3,00 €", ""),
        ],
    },
    {
        "id": "kalt", "title": "",
        "subtitle": "Kalte Getränke (0,33 L / 1 L)",
        "items": [
            (74, "Cola", "", "", "", "2,50 € / 3,50 €", ""),
            (75, "Cola Zero", "", "", "", "2,50 € / 3,50 €", ""),
            (76, "Fanta", "", "", "", "2,50 € / 3,50 €", ""),
            (77, "Sprite", "", "", "", "2,50 € / 3,50 €", ""),
            (78, "Spezi", "", "", "", "2,50 € / 3,50 €", ""),
        ],
    },
    {
        "id": "kalt2", "title": "",
        "subtitle": "",
        "items": [
            (79, "Pfirsich Eistee", "", "", "", "2,50 €", ""),
            (80, "Multivitaminsaft", "", "", "", "2,50 €", ""),
            (81, "Durstlöscher", "0,5 L", "", "", "2,00 €", ""),
            (82, "Uludag", "", "", "", "2,50 €", ""),
            (83, "Wasser", "0,5 L", "", "", "1,50 €", ""),
            (84, "Apfelsaftschorle", "", "", "", "2,50 €", ""),
            (85, "Ayran", "", "", "", "1,50 €", ""),
        ],
    },
]

ADDITIVES = [
    ("1.", "Konservierungsstoffe", "E 200–203: Sorbinsäure, PHB"),
    ("2.", "Antioxidationsmittel", "E 310–312: Gallate, BHT"),
    ("3.", "Farbstoffe", "E 101, 102: Lactoflavin, Tartrazin"),
    ("4.", "Emulgatoren", "E 322, 471: Lecithin, Diglyceride"),
    ("5.", "Geliermittel", "E 440: Pectine"),
    ("6.", "Verdickungsmittel", "E 407, 410: Carragen, JBK"),
    ("7.", "Stabilisatoren", "Phosphate"),
    ("8.", "Geschmacksverstärker", "E 620–625: Natriumglutamat"),
    ("9.", "Süßungsmittel", "E 420, 951: Sorbit, Aspartam"),
    ("10.", "Sonstiges", "Koffeinhaltig (Kaffee, Cola)"),
    ("11.", "Allergene", "Gluten, Eier, Nüsse"),
    ("12.", "Allergene", "Fisch, Krustentiere"),
]

DIYARBAKIR_TEXT = [
    "Diyarbakir liegt am Ufer des Tigris, mitten in Mesopotamien – einer der ältesten Kulturlandschaften der Welt. Seine mächtige schwarze Basaltmauer, die Hevsel-Gärten und die jahrtausendealte Altstadt gehören zum UNESCO-Welterbe.",
    "Über Jahrhunderte haben hier viele Völker und Kulturen zusammengelebt und ihre Spuren hinterlassen – in der Architektur, in der Musik und ganz besonders in der Küche. Genau diese Gastfreundschaft und diese Küche bringen wir nach Wiesbaden: Fleisch vom offenen Holzkohlegrill, frisches Brot aus dem Holzofen und Vorspeisen, wie sie seit Generationen zubereitet werden. Wir freuen uns, wenn Sie sich bei uns ein Stück davon schmecken lassen.",
]
