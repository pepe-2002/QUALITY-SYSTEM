/* GÉOPOLIS — Données du monde
 * 197 nations. Valeurs approximatives (ordre de grandeur 2025-2026), calibrées
 * pour le jeu et non pour la statistique officielle.
 *
 * Format compact (une ligne par pays, séparateur « | ») :
 *   CODE | Nom | Continent | lat | lon | population(M) | PIB(Md$) |
 *   tech(0-100) | stabilité(0-100) | armée(0-100) | régime | dotations(9 chiffres)
 *
 * Dotations, dans l'ordre : pétrole, gaz, charbon, fer, cuivre, terres rares,
 * uranium, or, agriculture — chacune de 0 (rien) à 9 (colossal).
 * Régime : D démocratie · A autoritaire · M monarchie · P parti unique
 */
(function (G) {
  'use strict';

  const PAYS_BRUT = `
US|États-Unis|NA|39.5|-98.5|335|29000|95|72|100|D|787554558
CA|Canada|NA|58.0|-100.0|40|2200|88|84|48|D|766646975
MX|Mexique|NA|23.5|-102.0|129|1900|68|52|42|D|543434145
GT|Guatemala|NA|15.5|-90.3|18|110|44|46|14|D|100112024
BZ|Belize|NA|17.2|-88.7|0.41|3.3|38|58|3|D|100001013
SV|Salvador|NA|13.8|-88.9|6.3|35|46|50|12|D|000001013
HN|Honduras|NA|14.8|-86.5|10.4|35|40|44|12|D|000112124
NI|Nicaragua|NA|12.9|-85.2|7.0|18|38|40|13|A|000111124
CR|Costa Rica|NA|9.9|-84.0|5.2|95|62|82|5|D|000000023
PA|Panama|NA|8.5|-80.0|4.4|85|60|62|8|D|000101123
CU|Cuba|NA|21.8|-79.5|11|110|52|56|26|P|101031023
HT|Haïti|NA|19.0|-72.5|11.7|20|22|18|6|D|000001112
DO|République dominicaine|NA|18.8|-70.5|11.3|125|50|60|14|D|000111133
JM|Jamaïque|NA|18.1|-77.3|2.8|19|48|60|6|D|000030012
BS|Bahamas|NA|24.7|-77.4|0.41|14|58|76|3|D|100000012
BB|Barbade|NA|13.2|-59.5|0.28|6.5|56|80|2|D|000000012
TT|Trinité-et-Tobago|NA|10.5|-61.3|1.5|28|56|62|5|D|560000012
AG|Antigua-et-Barbuda|NA|17.1|-61.8|0.09|2.0|48|76|1|D|000000011
DM|Dominique|NA|15.4|-61.4|0.07|0.7|42|74|1|D|000000012
GD|Grenade|NA|12.1|-61.7|0.13|1.3|44|74|1|D|000000012
KN|Saint-Christophe-et-Niévès|NA|17.3|-62.7|0.05|1.1|46|76|1|D|000000011
LC|Sainte-Lucie|NA|13.9|-61.0|0.18|2.5|46|76|1|D|000000012
VC|Saint-Vincent-et-les-Grenadines|NA|13.2|-61.2|0.10|1.1|44|74|1|D|000000012
BR|Brésil|SA|-10.0|-52.0|216|2300|72|54|56|D|655864588
AR|Argentine|SA|-35.0|-65.0|46|640|70|46|32|D|453424497
CL|Chili|SA|-33.0|-71.0|19.6|330|70|64|28|D|101396234
CO|Colombie|SA|4.0|-73.0|52|420|60|48|34|D|534113254
PE|Pérou|SA|-10.0|-76.0|34|290|54|46|26|D|231295365
VE|Venezuela|SA|7.0|-66.0|28|100|44|22|24|A|951434235
EC|Équateur|SA|-1.5|-78.5|18|120|48|44|16|D|610112245
BO|Bolivie|SA|-17.0|-64.5|12.4|46|42|40|14|D|241197234
PY|Paraguay|SA|-23.4|-58.4|6.9|45|42|50|11|D|100101035
UY|Uruguay|SA|-32.8|-56.0|3.4|80|62|82|8|D|000000035
GY|Guyana|SA|5.0|-58.9|0.8|25|44|54|4|D|900012242
SR|Suriname|SA|4.1|-56.0|0.63|4.0|40|48|3|D|610012231
GB|Royaume-Uni|EU|54.0|-2.5|68|3600|92|70|68|D|343221126
FR|France|EU|46.5|2.5|68|3200|91|64|72|D|122232337
DE|Allemagne|EU|51.0|10.5|84|4700|92|72|54|D|125342126
IT|Italie|EU|42.8|12.5|59|2300|85|58|48|D|122211126
ES|Espagne|EU|40.2|-3.7|48|1700|83|64|42|D|012231126
PT|Portugal|EU|39.5|-8.0|10.4|300|76|72|18|D|001132225
NL|Pays-Bas|EU|52.2|5.5|17.8|1200|90|80|32|D|161010025
BE|Belgique|EU|50.6|4.6|11.7|660|86|70|22|D|001110014
LU|Luxembourg|EU|49.8|6.1|0.66|90|88|88|3|M|001110012
IE|Irlande|EU|53.2|-8.0|5.3|560|88|80|8|D|021110024
CH|Suisse|EU|46.8|8.2|8.9|950|94|92|20|D|000110113
AT|Autriche|EU|47.5|14.0|9.1|530|85|80|16|D|012120024
DK|Danemark|EU|56.0|10.0|5.9|420|89|88|18|D|140000025
SE|Suède|EU|62.0|15.0|10.6|620|91|84|30|D|002542124
NO|Norvège|EU|62.0|10.0|5.5|540|89|90|24|D|780110113
FI|Finlande|EU|64.0|26.0|5.6|300|88|86|28|D|002431223
IS|Islande|EU|65.0|-18.5|0.39|32|82|88|1|D|000000012
PL|Pologne|EU|52.0|19.5|37|900|76|66|48|D|119331125
CZ|Tchéquie|EU|49.8|15.5|10.9|340|80|72|22|D|018220124
SK|Slovaquie|EU|48.7|19.7|5.4|140|74|68|14|D|015211124
HU|Hongrie|EU|47.2|19.5|9.6|230|74|60|16|D|012110125
RO|Roumanie|EU|45.9|25.0|19|380|68|58|26|D|338221136
BG|Bulgarie|EU|42.7|25.5|6.5|110|66|58|16|D|117331124
HR|Croatie|EU|45.2|15.5|3.9|85|70|68|10|D|122110023
SI|Slovénie|EU|46.1|14.8|2.1|70|76|76|6|D|012120023
RS|Serbie|EU|44.0|20.9|6.6|80|64|50|18|D|118331124
BA|Bosnie-Herzégovine|EU|44.0|18.0|3.2|28|56|42|8|D|018331123
ME|Monténégro|EU|42.8|19.3|0.62|7.5|58|54|3|D|002210012
MK|Macédoine du Nord|EU|41.6|21.7|1.8|15|58|52|5|D|013231123
AL|Albanie|EU|41.0|20.0|2.8|26|56|54|7|D|213231123
XK|Kosovo|EU|42.6|20.9|1.8|11|50|40|4|D|017331112
GR|Grèce|EU|39.0|22.0|10.4|250|76|60|32|D|113121124
CY|Chypre|EU|35.1|33.3|1.3|34|72|62|5|D|130120012
MT|Malte|EU|35.9|14.4|0.54|22|74|76|2|D|000000012
EE|Estonie|EU|58.7|25.5|1.4|42|84|72|6|D|005110012
LV|Lettonie|EU|56.9|24.6|1.9|45|78|68|6|D|002110013
LT|Lituanie|EU|55.3|23.9|2.8|80|78|68|8|D|002110013
BY|Biélorussie|EU|53.7|28.0|9.2|75|62|46|26|A|123321124
UA|Ukraine|EU|49.0|32.0|36|190|66|32|58|D|228843237
MD|Moldavie|EU|47.2|28.5|2.6|17|54|46|5|D|000000025
RU|Russie|EU|60.0|90.0|144|2200|82|48|92|A|898756675
AD|Andorre|EU|42.5|1.5|0.08|3.7|66|84|1|M|000110011
MC|Monaco|EU|43.7|7.4|0.04|9.0|76|88|1|M|000000001
LI|Liechtenstein|EU|47.1|9.5|0.04|7.0|80|90|1|M|000110011
SM|Saint-Marin|EU|43.9|12.5|0.034|1.9|66|84|1|D|000000012
VA|Saint-Siège|EU|41.9|12.45|0.001|0.4|50|90|1|M|000000000
CN|Chine|AS|35.0|105.0|1412|19000|88|62|90|P|449769467
IN|Inde|AS|22.0|79.0|1430|4000|74|52|76|D|248653477
JP|Japon|AS|36.5|138.0|124|4200|93|80|58|D|001211114
KR|Corée du Sud|AS|36.5|127.8|51.7|1900|93|66|66|D|002210113
KP|Corée du Nord|AS|40.0|127.0|26|30|42|38|54|P|018342512
TW|Taïwan|AS|23.7|121.0|23.4|800|94|58|46|D|001110013
ID|Indonésie|AS|-2.0|118.0|278|1500|60|56|48|D|449544376
PH|Philippines|AS|12.5|122.0|117|470|56|48|30|D|113254254
VN|Viêt Nam|AS|16.0|107.0|100|470|58|58|42|P|328432265
TH|Thaïlande|AS|15.0|101.0|72|530|64|50|38|M|123222166
MY|Malaisie|AS|4.0|102.0|34|440|68|62|28|M|452232244
SG|Singapour|AS|1.35|103.8|5.9|550|94|88|22|D|000000001
BN|Brunei|AS|4.5|114.7|0.45|15|58|72|3|M|780000012
KH|Cambodge|AS|12.6|105.0|17|45|40|44|12|A|111212144
LA|Laos|AS|18.5|105.0|7.6|16|38|46|8|P|014322145
MM|Birmanie|AS|21.0|96.0|54|65|38|22|34|A|235433365
BD|Bangladesh|AS|24.0|90.0|173|460|46|42|32|D|050121145
PK|Pakistan|AS|30.0|70.0|240|375|48|30|68|D|146321245
AF|Afghanistan|AS|34.0|66.0|42|17|22|14|18|A|113442332
NP|Népal|AS|28.3|84.0|30|43|38|46|10|D|002110134
BT|Bhoutan|AS|27.4|90.4|0.78|3.0|44|72|2|M|000110022
LK|Sri Lanka|AS|7.5|80.7|22|85|52|44|16|D|000210134
MV|Maldives|AS|3.2|73.2|0.52|7.0|50|58|1|D|000000011
IR|Iran|AS|32.0|53.0|89|430|58|34|62|A|981543245
IQ|Irak|AS|33.0|44.0|45|260|42|28|30|D|960211124
SA|Arabie saoudite|AS|24.0|45.0|36|1100|66|58|64|M|970111022
AE|Émirats arabes unis|AS|24.0|54.0|9.5|550|78|72|44|M|870110012
QA|Qatar|AS|25.3|51.2|2.7|220|74|74|24|M|790000011
KW|Koweït|AS|29.3|47.7|4.3|160|64|66|18|M|960000011
BH|Bahreïn|AS|26.0|50.5|1.5|46|66|56|10|M|540000011
OM|Oman|AS|21.0|57.0|4.6|110|60|68|20|M|640121112
YE|Yémen|AS|15.5|48.0|34|21|22|10|14|A|420111123
JO|Jordanie|AS|31.3|36.5|11.3|53|56|56|20|M|000111112
LB|Liban|AS|33.9|35.9|5.4|20|54|22|8|D|010000013
SY|Syrie|AS|35.0|38.0|23|10|30|14|18|A|320111123
IL|Israël|AS|31.5|35.0|9.8|550|94|58|72|D|140010012
PS|Palestine|AS|31.9|35.2|5.4|18|42|12|3|A|010000012
TR|Turquie|AS|39.0|35.0|85|1300|70|46|70|D|127543356
GE|Géorgie|AS|42.2|43.5|3.7|32|60|46|8|D|113231123
AM|Arménie|AS|40.2|45.0|2.8|25|60|44|10|D|002331222
AZ|Azerbaïdjan|AS|40.3|47.8|10.1|78|56|48|22|A|770211223
KZ|Kazakhstan|AS|48.0|68.0|20|290|60|56|24|A|778659945
UZ|Ouzbékistan|AS|41.5|64.0|36|100|50|52|20|A|364322745
TM|Turkménistan|AS|39.0|59.0|6.5|65|44|48|12|A|590101122
KG|Kirghizistan|AS|41.5|74.5|7.0|14|46|42|8|D|013321752
TJ|Tadjikistan|AS|38.8|71.0|10|13|42|40|8|A|012331642
MN|Mongolie|AS|46.8|103.0|3.4|21|50|60|6|D|047568853
TL|Timor oriental|AS|-8.8|125.7|1.4|2.0|32|44|3|D|760000012
EG|Égypte|AF|27.0|30.0|110|380|52|38|58|A|455211144
LY|Libye|AF|27.0|17.0|7.0|50|38|20|14|A|970111012
TN|Tunisie|AF|34.0|9.5|12|52|54|44|14|D|230211123
DZ|Algérie|AF|28.0|2.0|45|250|48|44|38|A|780211123
MA|Maroc|AF|32.0|-6.0|38|160|52|56|30|M|013321134
MR|Mauritanie|AF|20.0|-11.0|4.9|11|30|38|8|A|400641621
SN|Sénégal|AF|14.5|-14.5|18|32|38|56|10|D|300221123
GM|Gambie|AF|13.5|-15.5|2.8|2.5|26|46|3|D|000000012
GW|Guinée-Bissau|AF|12.0|-15.0|2.1|2.0|22|30|2|A|100000012
GN|Guinée|AF|10.5|-11.0|14|24|26|32|8|A|000821533
SL|Sierra Leone|AF|8.5|-11.8|8.6|7.0|24|38|4|D|001411642
LR|Libéria|AF|6.5|-9.5|5.4|4.5|22|36|3|D|000710532
CI|Côte d'Ivoire|AF|7.5|-5.5|29|80|38|50|14|D|310121245
GH|Ghana|AF|8.0|-1.0|34|80|40|58|12|D|420211843
TG|Togo|AF|8.5|1.0|9.0|9.0|28|42|4|A|000110123
BJ|Bénin|AF|9.5|2.3|14|20|28|46|5|D|100010123
BF|Burkina Faso|AF|12.5|-1.5|23|21|24|24|8|A|000211732
NE|Niger|AF|17.0|9.0|26|17|22|22|8|A|400119622
ML|Mali|AF|17.0|-4.0|23|21|24|22|9|A|100211842
NG|Nigéria|AF|10.0|8.0|223|200|42|32|38|D|982321244
CM|Cameroun|AF|6.0|12.0|28|50|32|38|12|A|530111235
TD|Tchad|AF|15.0|19.0|18|13|20|22|8|A|610011121
CF|Centrafrique|AF|7.0|21.0|5.7|2.6|18|12|3|A|001411732
SS|Soudan du Sud|AF|7.5|30.0|11|6.0|18|10|6|A|810001122
SD|Soudan|AF|15.0|30.0|48|30|24|12|18|A|620311742
ER|Érythrée|AF|15.5|39.0|3.7|2.6|20|30|8|A|001521521
DJ|Djibouti|AF|11.6|42.6|1.1|4.0|30|46|3|A|000001011
ET|Éthiopie|AF|9.0|39.0|126|160|32|26|24|D|002311634
SO|Somalie|AF|6.0|46.0|18|12|16|8|6|A|310000012
KE|Kenya|AF|0.5|38.0|55|110|42|46|14|D|002221234
UG|Ouganda|AF|1.5|32.5|48|50|32|40|12|A|400111233
RW|Rwanda|AF|-2.0|30.0|14|14|36|58|8|A|001231622
BI|Burundi|AF|-3.5|30.0|13|3.0|18|22|5|A|001231512
TZ|Tanzanie|AF|-6.0|35.0|67|80|32|52|12|D|032321844
CD|RD Congo|AF|-3.0|23.0|102|70|22|14|16|A|213196853
CG|Congo|AF|-1.0|15.0|6.0|15|28|34|6|A|750111122
GA|Gabon|AF|-0.8|11.6|2.4|21|38|54|4|A|740721221
GQ|Guinée équatoriale|AF|1.6|10.5|1.7|12|32|38|3|A|870000011
ST|Sao Tomé-et-Principe|AF|0.2|6.6|0.23|0.7|26|54|1|D|200000012
CV|Cap-Vert|AF|16.0|-24.0|0.6|2.6|40|70|2|D|000000012
AO|Angola|AF|-12.0|18.0|36|90|28|32|22|A|861121533
ZM|Zambie|AF|-14.0|27.5|20|28|30|48|8|D|002295532
ZW|Zimbabwe|AF|-19.0|30.0|16|35|30|24|10|A|005236723
MW|Malawi|AF|-13.5|34.0|21|13|22|40|6|D|002111523
MZ|Mozambique|AF|-18.0|35.0|33|22|24|30|10|D|181312533
MG|Madagascar|AF|-19.0|47.0|30|16|24|32|6|D|002115523
KM|Comores|AF|-11.7|43.4|0.85|1.3|22|40|2|D|000000034
SC|Seychelles|AF|-4.6|55.5|0.1|2.2|48|76|1|D|000000012
MU|Maurice|AF|-20.3|57.5|1.3|15|56|76|2|D|000000023
NA|Namibie|AF|-22.0|17.0|2.6|13|38|60|5|D|012286632
BW|Botswana|AF|-22.0|24.0|2.6|20|44|72|5|D|004211721
ZA|Afrique du Sud|AF|-29.0|25.0|60|410|62|38|34|D|029745944
LS|Lesotho|AF|-29.5|28.2|2.3|2.0|26|44|2|M|002110412
SZ|Eswatini|AF|-26.5|31.5|1.2|5.0|28|48|2|M|003110312
AU|Australie|OC|-25.0|134.0|27|1800|88|82|46|D|368959975
NZ|Nouvelle-Zélande|OC|-41.0|174.0|5.2|250|84|86|12|D|132110125
PG|Papouasie-Nouvelle-Guinée|OC|-6.0|145.0|10.3|32|26|32|5|D|441196623
FJ|Fidji|OC|-17.8|178.0|0.93|5.5|38|54|2|D|000010512
SB|Îles Salomon|OC|-9.6|160.2|0.72|1.7|24|38|1|D|000110412
VU|Vanuatu|OC|-15.4|166.9|0.33|1.1|26|48|1|D|000000012
WS|Samoa|OC|-13.8|-172.1|0.22|0.9|30|60|1|D|000000012
TO|Tonga|OC|-21.2|-175.2|0.11|0.5|30|60|1|M|000000012
KI|Kiribati|OC|1.9|-157.4|0.13|0.25|24|56|1|D|000000001
TV|Tuvalu|OC|-8.5|179.2|0.011|0.06|22|58|1|D|000000001
NR|Nauru|OC|-0.53|166.9|0.012|0.15|26|54|1|D|000000001
MH|Îles Marshall|OC|7.1|171.2|0.04|0.3|28|56|1|D|000000001
FM|Micronésie|OC|6.9|158.2|0.11|0.45|28|58|1|D|000000001
PW|Palaos|OC|7.5|134.6|0.018|0.3|32|62|1|D|000000001
`;

  // ── Ressources ────────────────────────────────────────────────────────────
  // prix : $ par unité · base : consommation quotidienne par million d'habitants
  G.RES = [
    { id: 'nourriture', nom: 'Nourriture',   icone: '🌾', prix: 420,   strat: false },
    { id: 'petrole',    nom: 'Pétrole',      icone: '🛢️', prix: 78,    strat: true  },
    { id: 'gaz',        nom: 'Gaz',          icone: '🔥', prix: 44,    strat: true  },
    { id: 'charbon',    nom: 'Charbon',      icone: '⚫', prix: 110,   strat: false },
    { id: 'fer',        nom: 'Fer',          icone: '⛓️', prix: 130,   strat: false },
    { id: 'cuivre',     nom: 'Cuivre',       icone: '🟠', prix: 8600,  strat: true  },
    { id: 'terresrares',nom: 'Terres rares', icone: '💠', prix: 62000, strat: true  },
    { id: 'uranium',    nom: 'Uranium',      icone: '☢️', prix: 210000,strat: true  },
    { id: 'or',         nom: 'Or',           icone: '🥇', prix: 2.1e6, strat: true  },
    { id: 'electricite',nom: 'Électricité',  icone: '⚡', prix: 95,    strat: false },
    { id: 'puces',      nom: 'Puces',        icone: '🔲', prix: 480000,strat: true  },
    { id: 'biens',      nom: 'Biens manuf.', icone: '📦', prix: 1400,  strat: false },
    { id: 'calcul',     nom: 'Calcul IA',    icone: '🧠', prix: 900000,strat: true  }
  ];
  G.R = {}; G.RES.forEach((r, i) => { G.R[r.id] = i; });
  G.NRES = G.RES.length;

  // ── Bâtiments ─────────────────────────────────────────────────────────────
  // cout : M$ · jours : durée de chantier · entretien : M$/jour
  // prod / conso : { ressource: quantité par jour }
  G.BAT = [
    { id:'ferme',    nom:'Ferme moderne',        icone:'🚜', cat:'ressources', cout:180,   jours:60,  entretien:0.035, prod:{nourriture:900},        conso:{electricite:120},                     desc:'Nourrit la population. Sans nourriture, la faim fait tomber les gouvernements.' },
    { id:'puits',    nom:'Puits de pétrole',     icone:'🛢️', cat:'ressources', cout:900,   jours:150, entretien:0.22,  prod:{petrole:2600},          conso:{electricite:260},   dot:0,            desc:'Extrait le pétrole. Rendement proportionnel aux réserves du pays.' },
    { id:'gaziere',  nom:'Plateforme gazière',   icone:'🔥', cat:'ressources', cout:820,   jours:140, entretien:0.20,  prod:{gaz:4200},              conso:{electricite:230},   dot:1,            desc:'Extrait le gaz naturel.' },
    { id:'houillere',nom:'Mine de charbon',      icone:'⚫', cat:'ressources', cout:340,   jours:90,  entretien:0.09,  prod:{charbon:1300},          conso:{electricite:150},   dot:2,            desc:'Charbon bon marché, mais polluant et impopulaire.' },
    { id:'minefer',  nom:'Mine de fer',          icone:'⛓️', cat:'ressources', cout:400,   jours:100, entretien:0.10,  prod:{fer:1500},              conso:{electricite:180},   dot:3,            desc:'Le fer nourrit l\'industrie et l\'armement.' },
    { id:'minecuivre',nom:'Mine de cuivre',      icone:'🟠', cat:'ressources', cout:520,   jours:110, entretien:0.13,  prod:{cuivre:26},             conso:{electricite:210},   dot:4,            desc:'Indispensable aux réseaux électriques et à l\'électronique.' },
    { id:'mineterres',nom:'Mine de terres rares',icone:'💠', cat:'ressources', cout:1400,  jours:200, entretien:0.30,  prod:{terresrares:3.2},       conso:{electricite:420},   dot:5,            desc:'Le goulot d\'étranglement de la course aux puces et à l\'IA.' },
    { id:'mineuran', nom:'Mine d\'uranium',      icone:'☢️', cat:'ressources', cout:1200,  jours:190, entretien:0.28,  prod:{uranium:0.9},           conso:{electricite:380},   dot:6,            desc:'Combustible nucléaire — civil et militaire.' },
    { id:'mineor',   nom:'Mine d\'or',           icone:'🥇', cat:'ressources', cout:1100,  jours:170, entretien:0.26,  prod:{or:0.09},               conso:{electricite:300},   dot:7,            desc:'Réserve de valeur : se vend toujours, à bon prix.' },
    { id:'thermique',nom:'Centrale thermique',   icone:'🏭', cat:'energie',    cout:700,   jours:120, entretien:0.16,  prod:{electricite:5200},      conso:{charbon:900},                         desc:'Électricité immédiate, au prix du charbon et de la pollution.' },
    { id:'cycle',    nom:'Centrale à gaz',       icone:'♨️', cat:'energie',    cout:640,   jours:100, entretien:0.15,  prod:{electricite:5800},      conso:{gaz:2400},                            desc:'Plus propre et plus souple que le charbon.' },
    { id:'nucleaire',nom:'Centrale nucléaire',   icone:'⚛️', cat:'energie',    cout:6500,  jours:420, entretien:0.90,  prod:{electricite:24000},     conso:{uranium:0.14},      tech:55,          desc:'Énorme puissance stable. Exige de la technologie et de la patience.' },
    { id:'solaire',  nom:'Parc solaire & éolien',icone:'🌞', cat:'energie',    cout:900,   jours:110, entretien:0.10,  prod:{electricite:4200},                                                  desc:'Pas de combustible, aucune pollution, très apprécié.' },
    { id:'usine',    nom:'Usine',                icone:'🏗️', cat:'industrie',  cout:750,   jours:130, entretien:0.20,  prod:{biens:420},             conso:{fer:260,cuivre:4,electricite:900},    desc:'Transforme les matières premières en biens exportables. Cœur du PIB.' },
    { id:'fonderie', nom:'Fonderie de puces',    icone:'🔲', cat:'industrie',  cout:9500,  jours:500, entretien:1.60,  prod:{puces:5.5},             conso:{terresrares:1.1,cuivre:6,electricite:5200}, tech:70, desc:'Grave les semi-conducteurs. Sans puces, pas de course à l\'IA.' },
    { id:'datacenter',nom:'Centre de données IA',icone:'🖥️', cat:'ia',         cout:4200,  jours:220, entretien:1.10,  prod:{calcul:9.0},            conso:{puces:0.55,electricite:9000},  tech:60, desc:'Produit la puissance de calcul qui entraîne vos modèles.' },
    { id:'labo',     nom:'Laboratoire national', icone:'🔬', cat:'ia',         cout:1300,  jours:180, entretien:0.42,  rech:14,                      conso:{electricite:600},                     desc:'+14 points de recherche par jour.' },
    { id:'universite',nom:'Université',          icone:'🎓', cat:'social',     cout:800,   jours:200, entretien:0.34,  educ:1.0, rech:4,              conso:{electricite:300},                     desc:'Élève le niveau d\'éducation : productivité, recherche, stabilité.' },
    { id:'hopital',  nom:'Hôpital',              icone:'🏥', cat:'social',     cout:600,   jours:150, entretien:0.30,  sante:1.0,                    conso:{electricite:280},                     desc:'Santé publique : espérance de vie, approbation, main-d\'œuvre.' },
    { id:'route',    nom:'Axe autoroutier & rail',icone:'🛣️', cat:'social',    cout:520,   jours:120, entretien:0.18,  infra:1.0,                                                                desc:'Infrastructure : multiplie le rendement de tout le reste.' },
    { id:'port',     nom:'Port en eau profonde', icone:'⚓', cat:'social',     cout:1500,  jours:240, entretien:0.36,  export:1.0,                   conso:{electricite:400},                     desc:'Augmente la capacité d\'exportation et les recettes douanières.' },
    { id:'base',     nom:'Base militaire',       icone:'🎖️', cat:'militaire',  cout:1000,  jours:160, entretien:0.45,  milcap:1.0,                   conso:{electricite:350},                     desc:'Capacité d\'entretien et de projection des forces.' },
    { id:'silo',     nom:'Complexe nucléaire',   icone:'🚀', cat:'militaire',  cout:12000, jours:600, entretien:2.20,  nuke:1.0,                     conso:{uranium:0.05,electricite:1800}, tech:78, desc:'Permet de fabriquer et de lancer des ogives. Sanctions garanties.' }
  ];
  G.B = {}; G.BAT.forEach((b, i) => { G.B[b.id] = i; });
  G.NBAT = G.BAT.length;

  // ── Unités militaires ─────────────────────────────────────────────────────
  // cout : M$ · entretien : M$/jour · att/def : puissance · jours : délai
  G.UNI = [
    { id:'infanterie',nom:'Brigade d\'infanterie',icone:'🪖', cout:24,   jours:20,  entretien:0.012, att:8,   def:12,  hommes:4000, desc:'Occupe le terrain. Rien ne se tient sans elle.' },
    { id:'blindes',   nom:'Bataillon blindé',    icone:'🛡️', cout:180,  jours:45,  entretien:0.055, att:36,  def:26,  hommes:900,  conso:{petrole:90},  desc:'Perce les fronts.' },
    { id:'artillerie',nom:'Artillerie',          icone:'💥', cout:120,  jours:35,  entretien:0.030, att:30,  def:10,  hommes:600,  desc:'Frappe en profondeur, use l\'ennemi.' },
    { id:'dca',       nom:'Défense antiaérienne',icone:'📡', cout:210,  jours:50,  entretien:0.060, att:2,   def:34,  hommes:400,  desc:'Protège vos villes et vos usines des frappes.' },
    { id:'chasse',    nom:'Escadron de chasse',  icone:'✈️', cout:900,  jours:90,  entretien:0.240, att:70,  def:40,  hommes:300, tech:55, conso:{petrole:160}, desc:'La supériorité aérienne décide des guerres modernes.' },
    { id:'drones',    nom:'Escadre de drones',   icone:'🛸', cout:260,  jours:40,  entretien:0.055, att:44,  def:14,  hommes:80,  tech:60, ia:2, desc:'Bon marché, létal, et multiplié par votre niveau d\'IA.' },
    { id:'helico',    nom:'Aviation d\'appui',   icone:'🚁', cout:420,  jours:60,  entretien:0.110, att:48,  def:22,  hommes:250, tech:45, conso:{petrole:110}, desc:'Appui rapproché et mobilité.' },
    { id:'navire',    nom:'Frégate',             icone:'🚢', cout:1100, jours:150, entretien:0.260, att:52,  def:48,  hommes:250, tech:50, conso:{petrole:140}, desc:'Protège vos routes commerciales et vos exportations.' },
    { id:'sousmarin', nom:'Sous-marin',          icone:'🌊', cout:2200, jours:260, entretien:0.420, att:80,  def:34,  hommes:120, tech:68, conso:{petrole:90},  desc:'Frappe sans être vu. Dissuasion crédible.' },
    { id:'missile',   nom:'Missiles balistiques',icone:'🎯', cout:340,  jours:55,  entretien:0.050, att:96,  def:2,   hommes:60,  tech:66, desc:'Frappe stratégique à longue portée.' },
    { id:'ogive',     nom:'Ogive nucléaire',     icone:'☢️', cout:2600, jours:220, entretien:0.300, att:0,   def:0,   hommes:40,  tech:82, bat:'silo', conso:{uranium:0.02}, desc:'L\'arme qui ne sert qu\'à ne pas servir. Réputation dévastée.' }
  ];
  G.U = {}; G.UNI.forEach((u, i) => { G.U[u.id] = i; });
  G.NUNI = G.UNI.length;

  // ── Recherche ─────────────────────────────────────────────────────────────
  // Arbre volontairement court et lisible : chaque techno a un effet net.
  G.TECHS = [
    { id:'agro',     nom:'Agronomie de précision', cout:2600,   icone:'🌾', effet:'+35 % de rendement agricole',         req:[] },
    { id:'forage',   nom:'Forage profond',         cout:4200,   icone:'🛢️', effet:'+30 % d\'extraction pétrole et gaz',  req:[] },
    { id:'metallo',  nom:'Métallurgie avancée',    cout:5200,   icone:'⛓️', effet:'+30 % sur toutes les mines',          req:[] },
    { id:'reseau',   nom:'Réseau intelligent',     cout:6800,   icone:'⚡', effet:'+25 % d\'électricité, -10 % de pertes',req:['metallo'] },
    { id:'automat',  nom:'Automatisation',         cout:9500,   icone:'🤖', effet:'+35 % de production industrielle',    req:['metallo'] },
    { id:'litho',    nom:'Lithographie EUV',       cout:22000,  icone:'🔲', effet:'Débloque les fonderies performantes (+60 % de puces)', req:['automat','reseau'] },
    { id:'fission',  nom:'Fission de 4ᵉ génération',cout:18000, icone:'⚛️', effet:'+40 % des centrales nucléaires',      req:['reseau'] },
    { id:'medecine', nom:'Médecine génomique',     cout:12000,  icone:'🧬', effet:'+30 % de santé, +2 d\'approbation',   req:['agro'] },
    { id:'educ',     nom:'Éducation universelle',  cout:8500,   icone:'🎓', effet:'+30 % d\'éducation et de recherche',  req:[] },
    { id:'logistique',nom:'Logistique intégrée',   cout:11000,  icone:'🛣️', effet:'+25 % d\'infrastructure et d\'export',req:['automat'] },
    { id:'furtif',   nom:'Furtivité',              cout:26000,  icone:'✈️', effet:'+25 % de puissance aérienne et navale',req:['automat'] },
    { id:'hyperson', nom:'Missiles hypersoniques', cout:34000,  icone:'🎯', effet:'+50 % de puissance des missiles',     req:['furtif'] },
    { id:'cyber',    nom:'Cyberguerre',            cout:16000,  icone:'💻', effet:'Espionnage et sabotage, +défense',    req:['educ'] },
    { id:'quantique',nom:'Calcul quantique',       cout:48000,  icone:'🧿', effet:'+45 % de calcul IA',                  req:['litho'] },
    { id:'fusion',   nom:'Fusion nucléaire',       cout:90000,  icone:'🌟', effet:'Énergie quasi illimitée : +150 % d\'électricité', req:['fission','quantique'] }
  ];

  // Paliers de la course à l'IA — cumul de calcul (unités·jours)
  G.PALIERS_IA = [
    { n:0,  nom:'Aucun programme',     seuil:0,        bonus:'—' },
    { n:1,  nom:'Automatisation',      seuil:1500,     bonus:'+2 % de productivité' },
    { n:2,  nom:'Modèles de langue',   seuil:6000,     bonus:'+5 % de productivité, +10 % de recherche' },
    { n:3,  nom:'Agents autonomes',    seuil:20000,    bonus:'+9 % de productivité, drones renforcés' },
    { n:4,  nom:'IA industrielle',     seuil:55000,    bonus:'+14 % de productivité, -corruption' },
    { n:5,  nom:'IA scientifique',     seuil:140000,   bonus:'+20 % de productivité, +40 % de recherche' },
    { n:6,  nom:'IA stratégique',      seuil:330000,   bonus:'+27 % de productivité, +25 % militaire' },
    { n:7,  nom:'Quasi-AGI',           seuil:750000,   bonus:'+35 % de productivité, cyberdominance' },
    { n:8,  nom:'AGI restreinte',      seuil:1600000,  bonus:'+45 % de productivité' },
    { n:9,  nom:'AGI déployée',        seuil:3400000,  bonus:'+60 % de productivité, +50 % militaire' },
    { n:10, nom:'Superintelligence',   seuil:7000000,  bonus:'Victoire technologique' }
  ];

  // ── Doctrines / lois ──────────────────────────────────────────────────────
  G.LOIS = [
    { id:'servicemil', nom:'Service militaire obligatoire', icone:'🎖️', cout:0,  effets:'+40 % de recrutement, −6 d\'approbation' },
    { id:'liberalisme',nom:'Libéralisation économique',     icone:'📈', cout:0,  effets:'+8 % de croissance, +corruption, −égalité' },
    { id:'protection', nom:'Protectionnisme',               icone:'🚧', cout:0,  effets:'+douanes, −commerce extérieur' },
    { id:'antitrust',  nom:'Lutte anticorruption',          icone:'⚖️', cout:0,  effets:'−corruption progressive, −4 d\'approbation des élites' },
    { id:'ecologie',   nom:'Transition écologique',         icone:'🌱', cout:0,  effets:'+approbation, −rendement du charbon' },
    { id:'iaouverte',  nom:'IA ouverte et régulée',         icone:'🧠', cout:0,  effets:'−15 % de calcul, +approbation, −risque d\'accident' },
    { id:'surveillance',nom:'Surveillance généralisée',     icone:'👁️', cout:0,  effets:'+stabilité, −approbation, +espionnage' },
    { id:'gratuite',   nom:'Santé et école gratuites',      icone:'🏥', cout:0,  effets:'+approbation, +éducation, dépenses ×1,4' }
  ];

  // ── Blocs ─────────────────────────────────────────────────────────────────
  G.BLOCS = [
    { id:'otan', nom:'OTAN', membres:['US','GB','FR','DE','IT','ES','PT','NL','BE','LU','DK','NO','IS','PL','CZ','SK','HU','RO','BG','HR','SI','GR','TR','EE','LV','LT','AL','ME','MK','CA','FI','SE'] },
    { id:'ue',   nom:'Union européenne', membres:['FR','DE','IT','ES','PT','NL','BE','LU','IE','AT','DK','SE','FI','PL','CZ','SK','HU','RO','BG','HR','SI','GR','CY','MT','EE','LV','LT'] },
    { id:'brics',nom:'BRICS+', membres:['BR','RU','IN','CN','ZA','IR','EG','ET','AE','SA','ID'] },
    { id:'ua',   nom:'Union africaine', membres:['DZ','AO','BJ','BW','BF','BI','CV','CM','CF','TD','KM','CG','CD','DJ','EG','GQ','ER','SZ','ET','GA','GM','GH','GN','GW','CI','KE','LS','LR','LY','MG','MW','ML','MR','MU','MA','MZ','NA','NE','NG','RW','ST','SN','SC','SL','SO','ZA','SS','SD','TZ','TG','TN','UG','ZM','ZW'] },
    { id:'asean',nom:'ASEAN', membres:['ID','MY','PH','SG','TH','VN','MM','KH','LA','BN','TL'] },
    { id:'opep', nom:'OPEP+', membres:['SA','IR','IQ','AE','KW','VE','NG','LY','DZ','AO','CG','GQ','GA','RU','KZ','OM','BH','BN','SD','SS','MX'] }
  ];

  // ── Analyse ───────────────────────────────────────────────────────────────
  G.PAYS = PAYS_BRUT.trim().split('\n').map((ligne, idx) => {
    const c = ligne.split('|');
    const dot = c[11];
    return {
      i: idx,
      code: c[0],
      nom: c[1],
      cont: c[2],
      lat: +c[3],
      lon: +c[4],
      pop: +c[5] * 1e6,
      pib: +c[6],
      tech: +c[7],
      stab: +c[8],
      arm: +c[9],
      reg: c[10],
      dot: [0,1,2,3,4,5,6,7,8].map(k => +dot[k]),
      drapeau: drapeau(c[0])
    };
  });
  G.N = G.PAYS.length;
  G.PARCODE = {};
  G.PAYS.forEach(p => { G.PARCODE[p.code] = p.i; });

  G.CONTINENTS = {
    AF: 'Afrique', EU: 'Europe', AS: 'Asie',
    NA: 'Amériques du Nord', SA: 'Amérique du Sud', OC: 'Océanie'
  };

  function drapeau(code) {
    if (code === 'XK' || code === 'VA') return '🏳️';
    return String.fromCodePoint(
      code.charCodeAt(0) + 127397,
      code.charCodeAt(1) + 127397
    );
  }
})(window.GEO = window.GEO || {});
