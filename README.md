README für Dashboard zur Exploration der Zufriedenheit in der Schweiz
Einführung
Dieses Projekt entwickelt ein interaktives Dashboard zur Visualisierung der Zufriedenheit der Schweizer Bevölkerung, basierend auf Umfrageergebnissen des Bundesamtes für Sta-tistik aus den Jahren 2007 bis 2022. Die erhobenen Zufriedenheitsindizes werden in meh-reren Dimensionen analysiert, darunter allgemeine Zufriedenheit sowie spezifische Le-bensbereiche, wie beispielsweise finanzielle Lage oder gesundheitliche Aspekte.
Datenquelle und Zielgruppen
Der Datensatz wird vom Bundesamt für Statistik als Excel Tabelle zum Download bereitge-stellt (siehe Link). Diese Daten sind für verschiedene Interessengruppen von Bedeutung:
•	Regierungsbehörden: Sie können Trends erkennen und politische Entscheidungen initiieren.
•	Forschungsinstitute: Sie können neue Erkenntnisse über Faktoren gewinnen, die das Wohlbefinden beeinflussen.
•	NGOs und Wohltätigkeitsorganisationen: Sie können die Bedürfnisse der Bevöl-kerung besser verstehen und gezielte Investitionsprogramme entwickeln.
•	Öffentlichkeit: Sie kann die Entwicklung mit anderen Ländern vergleichen.
Da die Daten von einer öffentlichen Behörde stammen, werden sie jährlich aktualisiert. Das Dashboard enthält den Datenstand mit dem Veröffentlichungsdatum vom 26.03.2024.
Datenaufbereitung
Um nur relevante Informationen für das Dashboard zu behalten, wurde der Datensatz be-reinigt und in ein CSV-Format (mit ‘;’ als Trennzeichen) konvertiert. Das resultierende Data-frame hat die folgende Struktur:
•	Header: betrifft die erste Zeile mit den Spaltennamen Jahr, Alterskategorie, Ge-schlecht und den neuen Lebensbereichen Allgemein, Finanzen, Alleinleben, Zu-sammenleben, Beziehungen, Gesundheit, Wohnsituation, Arbeitsbedingungen und Arbeitsklima.
•	Jahr (Spalte): umfasst den Analysezeitraum von 2007 – 2022.
•	Alterskategorie (Spalte): umfasst fünf Altersgruppen 16-17, 18-24, 25-49, 50-64 und 65+.
•	Geschlecht (Spalte): umfasst die Ausprägung Männer, Frauen und Alle.
•	Lebensbereiche (9 Spalten): Die Teilbereiche beinhalten Werte von 0 – 10. Diese Werte entsprechen dem erhobenen mittleren Zufriedenheitsindex.
Datenverwendung
Das Dashboard ermöglicht eine Analyse in drei Dimensionen, wobei jede in einem eigenen Tab dargestellt ist:
•	Tab 1 – Analyse der Gesamtbevölkerung: Relevant sind Zeilen mit den Werten Al-terskategorie = ‘#NA’ UND Geschlecht = ‘Alle’ (über alle Jahre).
•	Tab 2 – Analyse nach Geschlecht: Relevant sind Zeilen mit den Werten Alterska-tegorie = ‘#NA’ UND Geschlecht = ‘Männer’ ODER ‘FRAUEN’ (über alle Jahre).
•	Tab 3 – Analyse nach Alterskategorie: Relevant sind Zeilen mit den Werten Al-terskategorie ≠ ‘#NA’ UND Geschlecht = ‘#NA’ (über alle Jahre).
Das Jahr dient in allen Grafiken als Filtervariable.
Technische Voraussetzungen
Um den Code auszuführen ist die Installation von Python Version 3.7 oder höher erforder-lich. Zudem müssen folgende Packages installier und importiert werden:
•	dash (Dash, dcc, html, Input, Output, State)
•	Dash Bootstrap Components
•	Plotly Express
•	Pandas
Installation und Verwendung der Applikation
1.	Repository klonen (Link zum Git Repository)
git clone <https://github.com/TamaraFHGR/Dashboard_Design.git>
2.	Benötigte Packages installieren (sofern nicht bereits vorhanden):
pip install dash dash-bootstrap-components plotly pandas
3.	Es muss sichergestellt sein, dass das Verzeichnis «assets» angelegt ist und die Dateien «Zufriedenheit_raw.csv» und «custom.css» im Verzeichnis vorhanden sind.
4.	Starten der Anwendung «app.py» mit Python:
python app.py
5.	Die Dash-Anwendung öffnet sich automatisch im Webbrowser mit dem URL http://127.0.0.1:8051/.
Codeaufbau
In diesem Projekt wird Python als Open-Source-Framework zur Erstellung einer reaktiven Webanwendungen verwendet. Dies ermöglicht es, Python-Code für die funktionalen Kom-ponenten zu schreiben und die Designkomponente in ein CSS (Cascading Style Sheets) auszulagern.
•	Dash Core Components: dcc-Komponenten bilden das Grundgerüst des Dash-boards und ermöglichen interaktive Elemente, wie z.B. Dropdown-Menüs (Wahl zwischen Light und Dark Mode, Auswahl von Teilbereichen), Range-Slider (Ein-schränkung der Analysejahre) oder die Organisation in Tabs.
•	Dash HTML Components: HTML-Komponenten werden verwendet, um die Struk-tur und das Layout der Dash-Anwendung zu definieren. Verschiedene html.Div Elemente dienen als Container um Inhalte zu gruppieren. Aber auch für Header und Textelemente werden HTML-Komponenten eingesetzt.
•	CSS (Cascading Style Sheets): Das File «custom.css» im Ordner «assets» wird genutzt, um das visuelle Erscheinungsbild des Dashboards zu gestalten.
•	Plotly-Diagramme: Die Bibliothek Plotly wird genutzt, um interaktive Diagramme darzustellen, die den Datensatz im Dashboard visualisieren. Jedes Diagramm ist in einem html-Container organisiert und ist durch eine Funktion definiert (def up-date_graph_X). Das Dashboard verfügt über sechs Grafiken.
•	Callbacks: Callbacks werden verwendet, um die Dash Core Components und Plot-ly-Diagramme miteinander zu verbinden und eine Interaktion mit dem Benutzer zu ermöglichen. Jeder «def-Funktion» geht ein Callback voraus, der den Output und Input der Funktion bestimmt.
Dashboard-Funktionalitäten
Das Dashboard ist in drei Tabs gegliedert, die jeweils unterschiedliche Aspekte der Zufrie-denheit analysieren:
1.	Analyse der Gesamtbevölkerung
•	Liniendiagramm: Entwicklung der allgemeinen Zufriedenheit über die Jahre
•	Streudiagramm: Zusammenhang zwischen den Teilbereichen
2.	Analyse nach Geschlecht
•	Liniendiagramm: Entwicklung der allgemeinen Zufriedenheit über die Jahre, aufgeschlüsselt nach Geschlecht
•	Histogramm: Verteilung der Zufriedenheiten pro Teilbereich, aufgeschlüsselt nach Geschlecht
3.	Analyse nach Alterskategorie
•	Liniendiagramm: Entwicklung der allgemeinen Zufriedenheit über die Jahre, aufgeschlüsselt nach Alterskategorie
•	Balkendiagramm: Darstellung von Teilbereichen nach Alterskategorie
Das Dashboard bietet ausserdem die Möglichkeit, zwischen einem hellen und dunklen Mo-dus zu wechseln. Zudem stellt es kontextbezogene Informationen zu den Grafiken bereit, entweder als Hover-Text über den jeweiligen Diagrammen oder als Pop-Out-Text für grund-legende Erläuterungen (oben rechts).
Autoren
Das Dashboard wurde im Auftrag der Fachhochschule Graubünden (FHGR) im Masterstu-diengang für Data Visualization entwickelt und am 31.05.2024 zum letzten Mal aktualisiert. Die Autoren sind:
•	Nyffeler Tamara
•	Pellegatta Serge
•	Reiser Sharon
