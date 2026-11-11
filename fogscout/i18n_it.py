"""Italian texts (1.47): the German text of the code is the key, as in i18n_en.EN – a text missing here
shows in English (i18n.table). Made from the English texts; tests/test_i18n.py checks keys and placeholders."""
T = {
    'Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\nKurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden.':
        'Fog Scout è già in esecuzione ma non risponde (o si sta chiudendo).\n\nAttendi un momento e avvialo di nuovo. Se non basta: termina «{exe}» (Fog Scout) in Gestione attività alla voce «Dettagli».',
    'Fog Scout konnte nicht neu gestartet werden: Die alte Kopie läuft noch im Hintergrund.\n\nIm Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden und das Programm neu starten.':
        'Fog Scout non è riuscito a riavviarsi: la vecchia copia è ancora in esecuzione in background.\n\nTermina «{exe}» (Fog Scout) in Gestione attività alla voce «Dettagli» e avvia di nuovo il programma.',
    'Start fehlgeschlagen:':
        'Avvio non riuscito:',
    'Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt unverändert.':
        'Finora Fog Scout veniva usato tramite start.bat:\n{folder}\n\nTrasferire impostazioni, round, dati partita, backup e immagini mappa personali nella versione installata? La vecchia cartella resta invariata.',
    'Übernahme fehlgeschlagen: {error}':
        'Trasferimento non riuscito: {error}',
    'Kein Windows: Fenstersuche, Hotkeys und Click-Through sind nur unter Windows aktiv.':
        'Non è Windows: ricerca finestra, hotkey e clic passanti funzionano solo su Windows.',
    'Bereit. {n} Maps geladen, Spielsprachen: {langs}.':
        'Pronto. {n} mappe caricate, lingue di gioco: {langs}.',
    'Bildschirm {w}×{h} ohne schwarze Balken neben dem Spielbild: Systemwerte, „Heute“ und Musik im Spiel sind ausgeschaltet (sie lägen sonst auf dem Spielbild) – einschalten auf der Seite Overlay.':
        "Schermo {w}×{h} senza barre nere accanto all'immagine di gioco: valori di sistema, «oggi» e musica nel gioco sono disattivati (finirebbero sull'immagine di gioco) – attivali nella pagina Overlay.",
    'Automatisch (Windows-Sprache)':
        'Automatica (lingua di Windows)',
    'Erkennung':
        'Rilevamento',
    'Overlay':
        'Overlay',
    'System':
        'Sistema',
    'Fehler':
        'Errore',
    'automatisch':
        'automatico',
    'oben links':
        'in alto a sinistra',
    'oben rechts':
        'in alto a destra',
    'unten links':
        'in basso a sinistra',
    'unten rechts':
        'in basso a destra',
    'eigene Position':
        'posizione personalizzata',
    'Karte ein/aus':
        'Mappa on/off',
    'Layout-Variante':
        'Variante layout',
    'Bildschirm scannen':
        'Scansiona schermo',
    'Vorherige Map':
        'Mappa precedente',
    'Nächste Map':
        'Mappa successiva',
    'Grösser':
        'Più grande',
    'Kleiner':
        'Più piccola',
    'Mit Maus verschieben':
        'Sposta col mouse',
    'Noch keine Map':
        'Ancora nessuna mappa',
    'Karte ausblenden':
        'Nascondi mappa',
    'Karte einblenden':
        'Mostra mappa',
    'Scannen':
        'Scansiona',
    'Overlay testen':
        'Prova overlay',
    'Test beenden':
        'Termina prova',
    'Bild hinzufügen …':
        'Aggiungi immagine …',
    'Zuordnen …':
        'Assegna …',
    'Server':
        'Server',
    'Einstellungen':
        'Impostazioni',
    'Layout {n} von {total}':
        'Layout {n} di {total}',
    '(unsicher)':
        '(incerto)',
    'manuell gewählt':
        'scelta a mano',
    'per Scan gefunden':
        'trovata con la scansione',
    'Letzte Runde: {time}':
        'Ultimo round: {time}',
    'Unbekannte Map gelesen: „{text}“':
        'Letta mappa sconosciuta: «{text}»',
    'Im Menü – Karte pausiert ({map})':
        'In un menu – mappa in pausa ({map})',
    'Runde vorbei – wartet auf das nächste Match':
        'Round finito – in attesa della prossima partita',
    'Karte ausgeblendet ({map})':
        'Mappa nascosta ({map})',
    'Wartet auf DBD':
        'In attesa di DBD',
    'DBD läuft – automatische Erkennung ist aus (Map von Hand wählen)':
        'DBD è in esecuzione – rilevamento automatico disattivato (scegli la mappa a mano)',
    'Wartet auf das nächste Match':
        'In attesa della prossima partita',
    'Simulation – wartet auf das Map-Banner':
        'Simulazione – in attesa del banner della mappa',
    'Im Match: {map}':
        'In partita: {map}',
    'Karte eingeblendet':
        'Mappa mostrata',
    'Kartenbild hinzufügen …':
        'Aggiungi immagine mappa …',
    'eigenes Bild für eine Map (Hintergrund wird entfernt)':
        "un'immagine personale per una mappa (lo sfondo viene rimosso)",
    'Eigene Bilder':
        'Immagini personali',
    'Position':
        'Posizione',
    'Zurücksetzen':
        'Ripristina',
    'Horizontal':
        'Orizzontale',
    'Vertikal':
        'Verticale',
    'Fertig':
        'Fatto',
    '0 % = links/oben, 100 % = rechts/unten':
        '0 % = sinistra/alto, 100 % = destra/basso',
    'Karte im schwarzen Rand halten':
        'Tieni la mappa nella barra nera',
    'Darstellung':
        'Aspetto',
    'Grösse':
        'Dimensione',
    'Karte anzeigen':
        'Mostra la mappa',
    'Karte im Overlay eingeblendet.':
        "Mappa mostrata nell'overlay.",
    'Karte im Overlay aus – es werden nur Timer, Ort und Ping angezeigt.':
        "Mappa nell'overlay disattivata – vengono mostrati solo timer, posizione e ping.",
    'nichts anzuzeigen':
        'niente da mostrare',
    'Aus: Das Overlay zeigt nur Rundentimer, Serverregion und Ping – ohne Karte. Erkennung, Rundenende und Statistik laufen wie gewohnt.':
        "Off: l'overlay mostra solo il timer del round, la regione del server e il ping – senza la mappa. Rilevamento, fine del round e statistiche funzionano come al solito.",
    'Für diese Map zurücksetzen':
        'Ripristina per questa mappa',
    'eigene Grösse {n} % (Hotkeys/Strg+Mausrad)':
        'dimensione propria {n} % (hotkey/Ctrl+rotellina)',
    'gedreht um {deg}°':
        'ruotata di {deg}°',
    'Killer':
        'Killer',
    'Survivor':
        'Sopravvissuto',
    'Rolle':
        'Ruolo',
    'Rolle: {role}':
        'Ruolo: {role}',
    'Alle Rollen':
        'Tutti i ruoli',
    'Custom Game':
        'Partita personalizzata',
    'Custom Games':
        'Partite personalizzate',
    'Farming':
        'Farming',
    'Stil':
        'Stile',
    'Original':
        'Originale',
    'Dunkel':
        'Scuro',
    'Die Karten mit lila Boden, wie sie mitgeliefert werden – gilt auch im Spiel.':
        'Le mappe con il pavimento viola, così come sono – vale anche nel gioco.',
    'Klassisch':
        'Classico',
    'Glas-Karten':
        'Schede in vetro',
    'Chips & Icons':
        'Chip e icone',
    'Minimal Line':
        'Linea minimale',
    'SYSTEM':
        'SISTEMA',
    'Farming an/aus':
        'Farming attivo/disattivato',
    'Farming-Runden':
        'Round di farming',
    'Runden ohne Crossplay als Farming zählen':
        'Conta i round senza cross-play come farming',
    'Alle Runden auf':
        'Tutti i round on',
    'Farming-Runden zählen in Statistik und Aufnahmen überall mit; das Häkchen „Farming ausblenden“ (bei den Filtern) hält sie heraus, der Reiter Statistik → Farming listet sie immer. Crossplay aus erkennt das Programm an der Weltkugel mit rotem Kreuz neben dem Lobby-Knopf; Runden auf der gewählten Region zählen immer als Farming, auch ältere. Einzelne Runden: „Farming an/aus“ unter „Letzte Runden“.':
        'I round di farming contano ovunque nelle statistiche e nelle registrazioni; la casella «Nascondi farming» (accanto ai filtri) li esclude, la scheda Statistiche → Farming li elenca sempre. Il cross-play disattivato viene letto dal globo con la croce rossa accanto al pulsante della lobby; i round nella regione scelta contano sempre come farming, anche quelli più vecchi. Singoli round: «Farming on/off» in «Ultimi round».',
    '{map} ({when}) zählt jetzt als Farming-Runde.':
        '{map} ({when}) ora conta come round di farming.',
    '{map} ({when}) zählt wieder als normale Runde.':
        '{map} ({when}) conta di nuovo come round normale.',
    'Hinweis: Runden auf {region} zählen laut Einstellung weiter als Farming.':
        "Nota: i round su {region} contano comunque come farming per via dell'impostazione.",
    'Crossplay war aus – die Runde zählt als Farming-Runde.':
        'Il cross-play era disattivato – il round conta come round di farming.',
    'Crossplay war aus, die Lobby sah aus wie ein Custom Game – die Runde zählt als Farming-Runde, sobald die Stats-Seite sie als öffentliches Match zeigt.':
        'Il cross-play era disattivato e la lobby sembrava una partita personalizzata – il round conta come round di farming non appena la pagina delle statistiche lo mostra come partita pubblica.',
    '{off} von {n} Blicken mit Kreuz':
        '{off} di {n} controlli con la croce',
    'letzter Blick':
        'ultimo controllo',
    'Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.':
        'Il cross-play è disattivato ({looks}) – il prossimo round conta come round di farming.',
    'Crossplay ist an ({looks}) – keine Farming-Runde.':
        'Il cross-play è attivo ({looks}) – nessun round di farming.',
    'Als Custom Game erkannt – die Runde zählt nicht als Farming (unter „Letzte Runden“ mit „Farming an/aus“ korrigierbar).':
        'Riconosciuta come partita personalizzata – il round non conta come farming (correggilo in «Ultimi round» con «Farming on/off»).',
    'Keine Lobby zur Runde ({why}) – sie zählt nicht als Farming.':
        'Nessuna lobby per questo round ({why}) – non conta come farming.',
    'Lobby zu alt':
        'lobby troppo vecchia',
    'Lobby nicht gesehen':
        'lobby non vista',
    'Diese Runde als Farming-Runde zählen bzw. wieder als normale Runde – Farming-Runden zählen überall mit, bis „Farming ausblenden“ sie heraushält; der Reiter „Farming“ listet sie immer. Runden auf der Farming-Region (Einstellungen → Match-Daten) bleiben Farming.':
        'Conta questo round come round di farming o di nuovo come round normale – i round di farming contano ovunque finché «Nascondi farming» non li esclude; la scheda «Farming» li elenca sempre. I round nella regione di farming (Impostazioni → Dati partita) restano farming.',
    'Farming ausblenden':
        'Nascondi farming',
    'An: Farming-Runden (Crossplay aus, Farming-Region, Farming-Gegner) bleiben aus Statistik, Aufnahmen und Clips draussen – ein Schalter für alle drei. Aus: sie zählen wie jede andere Runde. Der Reiter Statistik → Farming zeigt sie immer.':
        'On: i round di farming (cross-play disattivato, regione di farming, partner di farming) restano fuori da statistiche, registrazioni e clip – un solo interruttore per tutti e tre. Off: contano come qualsiasi altro round. La scheda Statistiche → Farming li mostra sempre.',
    'Zeigt die Lobby die Weltkugel mit rotem Kreuz (Crossplay aus), zählt die nächste Runde als Farming-Runde.':
        'Se la lobby mostra il globo con la croce rossa (cross-play disattivato), il prossimo round conta come round di farming.',
    'Custom Game – keine Wartezeit.':
        'Partita personalizzata – nessun tempo di attesa.',
    'Suche läuft: {time}':
        'Ricerca: {time}',
    'Suche nach einem Match gestartet.':
        'Ricerca di una partita avviata.',
    'Lobby verlassen – sie zählt für keine Runde.':
        'Lobby abbandonata – non conta per nessun round.',
    'Suche abgebrochen.':
        'Ricerca annullata.',
    'Lobby gefunden nach {time}{role}.':
        'Lobby trovata dopo {time}{role}.',
    'Lobby gefunden{role}.':
        'Lobby trovata{role}.',
    'Lobby nur kurz gesehen – Rolle und Crossplay von dort, ohne Wartezeit.':
        'Lobby vista solo brevemente – ruolo e cross-play da lì, nessun tempo di attesa.',
    'Wartezeit {time}':
        'atteso {time}',
    'Verbindung in dieser Runde: {n} × Aussetzer, längster {s} s.':
        'Connessione in questo round: {n} × interruzioni, la più lunga {s} s.',
    '{n}× Aussetzer':
        '{n}× interruzioni',
    'Ergebnisbildschirm (zweiter Blick): gespielt als {role}.':
        'Schermata dei risultati (secondo controllo): giocato come {role}.',
    'Ergebnisbildschirm: gespielt als {role}.':
        'Schermata dei risultati: giocato come {role}.',
    'Wartezeit':
        'Tempo di attesa',
    'Regionen':
        'Regioni',
    'Markierte Runde:':
        'Round selezionato:',
    'Benachrichtigungen':
        'Notifiche',
    'Runde auf {map} nicht gezählt: ihr Ende wurde nicht erkannt.':
        'Round su {map} non contato: la sua fine non è stata rilevata.',
    'Einstellungen exportieren …':
        'Esporta impostazioni …',
    'Einstellungen importieren …':
        'Importa impostazioni …',
    'Einstellungen exportieren':
        'Esporta impostazioni',
    'Einstellungen importieren':
        'Importa impostazioni',
    'Export fehlgeschlagen: {error}':
        'Esportazione non riuscita: {error}',
    'Einstellungen gesichert: {path}':
        'Impostazioni salvate: {path}',
    'Das ist keine Einstellungsdatei von Fog Scout ({error}).':
        'Questo non è un file di impostazioni di Fog Scout ({error}).',
    'Alle Einstellungen durch die aus der Datei ersetzen? Das Programm startet danach neu.':
        'Sostituire tutte le impostazioni con quelle del file? Il programma si riavvierà subito dopo.',
    'Einstellungen importiert aus {path}.':
        'Impostazioni importate da {path}.',
    'Bitte das Programm jetzt neu starten.':
        'Riavvia ora il programma.',
    'Speichert alle Einstellungen in eine Datei: Hotkeys, Grösse und Drehung pro Map, eigene Map-Zuordnungen, Overlay, Regionen … Die Statistik (rounds.jsonl) gehört nicht dazu.':
        'Salva tutte le impostazioni in un file: hotkey, dimensione e rotazione per mappa, assegnazioni personali delle mappe, overlay, regioni … Le statistiche (rounds.jsonl) non ne fanno parte.',
    'Lädt eine exportierte Einstellungsdatei und startet das Programm neu. Fehlende Werte (ältere Sicherung) bekommen ihren Standard.':
        'Carica un file di impostazioni esportato e riavvia il programma. I valori mancanti (backup più vecchio) ricevono il loro valore predefinito.',
    'Ton und Meldung, wenn eine Lobby gefunden wurde':
        'Suono e notifica quando è stata trovata una lobby',
    'Erinnern, wenn der Lobby-Countdown abläuft und READY noch nicht gedrückt ist':
        'Avvisami quando il conto alla rovescia della lobby sta per scadere e READY non è ancora premuto',
    'Nur wenn DBD nicht das aktive Fenster ist':
        'Solo quando DBD non è la finestra attiva',
    'Die Meldung erscheint unten rechts über allen Fenstern – auch bei „Nicht stören“ – und nimmt dem aktiven Fenster nicht den Fokus. Klick darauf schliesst sie.':
        'La notifica compare in basso a destra sopra tutte le finestre – anche con «Non disturbare» – e non toglie lo stato attivo alla finestra attiva. Fai clic per chiuderla.',
    'Meldung testen':
        'Prova notifica',
    'Zeigt die Meldung und spielt den Ton – so siehst du, wo sie erscheint.':
        'Mostra la notifica e riproduce il suono – così vedi dove compare.',
    'Lobby gefunden':
        'Lobby trovata',
    'nach {time}':
        'dopo {time}',
    'READY drücken.':
        'Premi READY.',
    'Lobby startet gleich':
        'La lobby inizia a breve',
    'Noch {n} s – READY ist noch nicht gedrückt.':
        'Mancano {n} s – READY non è ancora premuto.',
    'Lobby-Countdown läuft ab, READY ist noch nicht gedrückt.':
        'Il conto alla rovescia della lobby sta per scadere, READY non è premuto.',
    'Ø Ping':
        'Ping medio',
    'Spielt einen Hinweiston und zeigt eine Windows-Meldung, sobald DBD eine Lobby gefunden hat – praktisch, wenn du während der Suche etwas anderes machst.':
        'Riproduce un suono e mostra una notifica di Windows appena DBD ha trovato una lobby – utile se fai altro durante la ricerca.',
    'Noch einmal melden, wenn der Countdown der Lobby unter 15 s fällt und du READY nicht gedrückt hast.':
        'Avvisa di nuovo quando il conto alla rovescia della lobby scende sotto i 15 s e non hai premuto READY.',
    'Keine Meldung, solange DBD im Vordergrund ist – dann siehst du die Lobby ja selbst.':
        'Nessuna notifica mentre DBD è in primo piano – in quel caso vedi la lobby da solo.',
    'Bilanz der Sitzung zeigen, wenn DBD beendet wurde':
        'Mostra i numeri della sessione quando DBD viene chiuso',
    'Etwa 15 s nachdem DBD geschlossen wurde: eine Meldung mit den Runden der Sitzung, der Spielzeit und – mit Match-Daten – Ø Kills, Entkommen und Bloodpoints. Steht auch im Log.':
        'Circa 15 s dopo la chiusura di DBD: una notifica con i round della sessione, il tempo di gioco e – con i dati partita – Ø uccisioni, fughe e Punti Sangue. Anche nel log.',
    'Sitzung beendet':
        'Sessione finita',
    '1 Runde':
        '1 round',
    '{bp} BP':
        '{bp} BP',
    'Melden, wenn eine Runde keine Blutpunkte gebracht hat (Cap erreicht)':
        'Avvisa quando un round non ha portato Punti Sangue (limite raggiunto)',
    'Fog Scout liest in der Lobby den Blutpunkte-Stand oben rechts. Ist er nach einer gezählten Runde derselbe wie davor, ist das Cap erreicht (normal 5 Millionen, nach Tome-Belohnungen auch mehr) – die Punkte der Runde sind verfallen. Ton und Meldung kommen auch, wenn DBD im Vordergrund ist; Custom Games zählen nicht.':
        'Fog Scout legge il saldo dei Punti Sangue in alto a destra nella lobby. Se dopo un round contato è uguale a prima, il limite è raggiunto (di norma 5 milioni, di più dopo le ricompense dei Tomi) – i punti del round vanno persi. Suono e notifica arrivano anche mentre DBD è in primo piano; le partite personalizzate non contano.',
    'Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte dieser Runde sind verfallen.':
        'Punti Sangue invariati: {bp} prima e dopo il round – il limite è raggiunto, i punti di questo round sono persi.',
    'Blutpunkte-Cap erreicht':
        'Limite di Punti Sangue raggiunto',
    '{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die nächste Runde nichts.':
        '{bp} BP prima e dopo il round – spendili nella Rete Sanguinaria, altrimenti anche il prossimo round non porterà nulla.',
    'Blutpunkte: +{gain} in dieser Runde, Stand {bp}.':
        'Punti Sangue: +{gain} in questo round, saldo {bp}.',
    'Blutpunkte: Stand {bp} nach der Runde, vorher {before}.':
        'Punti Sangue: saldo {bp} dopo il round, {before} prima.',
    'BP-Stand':
        'Saldo BP',
    'Aussetzer':
        'Blocchi',
    'Alles sichern (ZIP) …':
        'Salva tutto (ZIP) …',
    'Aus Sicherung wiederherstellen (ZIP) …':
        'Ripristina da backup (ZIP) …',
    'Aus Sicherung wiederherstellen':
        'Ripristina da backup',
    'Führt eine Sicherung von „Alles sichern“ mit den jetzigen Daten zusammen: Runden, Match-Daten, Kartenbilder und Banner, die fehlen, kommen dazu – Vorhandenes bleibt, wie es ist. Zeigt vorher, was dazukommt. Die Einstellungen der Sicherung nur auf eigene Rückfrage.':
        "Unisce un backup di «Salva tutto» con i dati che hai ora: round, dati partita, immagini mappa e banner mancanti vengono aggiunti – ciò che c'è già resta com'è. Prima mostra cosa verrebbe aggiunto. Le impostazioni del backup solo con una domanda a parte.",
    'Während einer Runde nicht möglich – nach dem Rundenende noch einmal.':
        'Non possibile durante un round – riprova quando è finito.',
    'Das ist keine Sicherung von Fog Scout ({error}).':
        'Questo non è un backup di Fog Scout ({error}).',
    '{rounds} Runden, {lost} nicht gezählte Runden, {matches} Matches, {files} Bilder/Banner':
        '{rounds} round, {lost} round non contati, {matches} partite, {files} immagini/banner',
    'Alles aus der Sicherung ist schon da – nichts hinzuzufügen.':
        "Tutto ciò che è nel backup c'è già – niente da aggiungere.",
    'Aus der Sicherung hinzufügen: {what}. Schon vorhanden (bleibt, wie es ist): {known}. Vorher kommt eine Kopie der Runden und Match-Daten nach backup/.':
        "Aggiungi dal backup: {what}. Già presente (resta com'è): {known}. Prima viene salvata una copia dei round e dei dati partita in backup/.",
    'Zusammenführen':
        'Unisci',
    'Wiederherstellen fehlgeschlagen: {error}':
        'Ripristino non riuscito: {error}',
    'Aus der Sicherung hinzugefügt: {what}.':
        'Aggiunto dal backup: {what}.',
    'Einstellungen der Sicherung nicht lesbar: {error}':
        'Impossibile leggere le impostazioni del backup: {error}',
    'Die Sicherung enthält auch Einstellungen – übernehmen ersetzt die aktuellen.':
        'Il backup contiene anche impostazioni – prenderle sostituisce quelle attuali.',
    'Installation prüfen':
        'Verifica installazione',
    'Installation wird geprüft …':
        "Verifica dell'installazione …",
    'Installation prüfen – Fehler: {line}':
        'Verifica installazione – errore: {line}',
    '{n} von {total} Prüfungen fehlgeschlagen – Einzelheiten im Log. Eine Neuinstallation (Setup erneut ausführen) behebt fehlende Dateien meist.':
        '{n} di {total} controlli non superati – dettagli nel log. Reinstallare (eseguire di nuovo il setup) di solito ripristina i file mancanti.',
    'Alle {n} Prüfungen bestanden: {names}.':
        'Tutti i {n} controlli superati: {names}.',
    'Installation prüfen: {text}':
        'Verifica installazione: {text}',
    'Prüft, ob alles da ist und läuft: Programmdateien, Kartenbilder, Bibliotheken, alle Module, Telemetrie aus, Texterkennung, ffmpeg, Qt – derselbe Selbsttest wie bei jedem Build. Läuft als eigener Prozess, Ergebnis im Log.':
        'Controlla che tutto sia presente e funzioni: file del programma, immagini mappa, librerie, ogni modulo, telemetria disattivata, riconoscimento del testo, ffmpeg, Qt – lo stesso autocontrollo di ogni build. Gira come processo a sé, risultato nel log.',
    'Alles sichern':
        'Salva tutto',
    'Gesichert: {n} Dateien in {path}':
        'Salvati: {n} file in {path}',
    'Sichern fehlgeschlagen: {error}':
        'Backup non riuscito: {error}',
    'Packt Runden, Match-Daten, die Einstellungen (ohne Passwörter und PC-eigene Werte), eigene Kartenbilder und den Banner-Korpus in eine ZIP-Datei – zum Aufbewahren oder für einen anderen PC. Aufnahmen und Logs bleiben draussen.':
        'Mette round, dati partita, impostazioni (senza password e valori propri di questo PC), immagini mappa personali e il corpus dei banner in un unico file ZIP – da conservare o per un altro PC. Registrazioni e log restano fuori.',
    'Spielmodus':
        'Modalità di gioco',
    'Eigener Charakter':
        'Personaggio proprio',
    'Eigene Perks':
        'Perk propri',
    'JSON (für eigene Auswertungen)':
        'JSON (per analisi personali)',
    'Eine Liste mit einem Objekt je Runde, die Spaltentitel als Schlüssel – für eigene Auswertungen (Python, Tabellen, jq).':
        'Un elenco con un oggetto per round, i titoli delle colonne come chiavi – per analisi personali (Python, fogli di calcolo, jq).',
    'Rolle für {map} ({when}) auf {role} geändert.':
        'Ruolo per {map} ({when}) cambiato in {role}.',
    'Rolle konnte nicht gespeichert werden: {error}':
        'Impossibile salvare il ruolo: {error}',
    'Diese Runde als Killer-Runde zählen (falls die Erkennung falsch lag).':
        'Conta questo round come round da Killer (se il rilevamento era sbagliato).',
    'Diese Runde als Survivor-Runde zählen (falls die Erkennung falsch lag).':
        'Conta questo round come round da Sopravvissuto (se il rilevamento era sbagliato).',
    'Diese Runde als Custom Game zählen – sie fliesst dann nicht in die Wartezeit ein.':
        'Conta questo round come partita personalizzata – viene quindi escluso dal tempo di attesa.',
    'Noch keine Wartezeiten in dieser Auswahl.':
        'Ancora nessun tempo di attesa in questa selezione.',
    'nach Wochentag':
        'per giorno della settimana',
    'nach Uhrzeit':
        'per ora del giorno',
    'nach Region':
        'per regione',
    'Wann/Wo':
        'Quando/dove',
    'Ø Wartezeit':
        'Attesa media',
    'Kürzeste':
        'Più breve',
    'Warten':
        'Attesa',
    'Uhr':
        'h',
    'Montag':
        'Lunedì',
    'Dienstag':
        'Martedì',
    'Mittwoch':
        'Mercoledì',
    'Donnerstag':
        'Giovedì',
    'Freitag':
        'Venerdì',
    'Samstag':
        'Sabato',
    'Sonntag':
        'Domenica',
    'Gemessen von „CANCEL“ (Suche läuft) bis zur gefundenen Lobby – nur wenn das Programm die Suche gesehen hat. Custom Games haben keine Wartezeit.':
        'Misurato da «CANCEL» (ricerca) fino alla lobby trovata – solo se il programma ha visto la ricerca. Le partite personalizzate non hanno tempo di attesa.',
    'Map-Namen oben einfügen (wie bei den mitgelieferten Karten)':
        'Metti il nome della mappa in alto (come nelle mappe incluse)',
    'Das Bild hat oben schon einen Namen – es wird keiner hinzugefügt.':
        "L'immagine ha già un nome in alto – non ne viene aggiunto un altro.",
    'Schreibt den Map-Namen weiss mit Schatten über die Karte, im Stil der mitgelieferten Karten. Hat das Bild oben schon einen Namen, passiert nichts. Beim Drehen bleibt der Name aufrecht.':
        "Scrive il nome della mappa in bianco con un'ombra sopra la mappa, nello stile delle mappe incluse. Se l'immagine ha già un nome in alto, non succede nulla. Il nome resta dritto quando la mappa viene ruotata.",
    'Drehen':
        'Ruota',
    'Karte drehen':
        'Ruota mappa',
    'Etage wechseln':
        'Cambia piano',
    'Beide Etagen':
        'Entrambi i piani',
    'Etage {n} von {total}':
        'Piano {n} di {total}',
    'Diese Map hat nur eine Etage.':
        'Questa mappa ha un solo piano.',
    'Wechselt die Anzeige bei Karten mit Etagen (Midwich): beide untereinander → unten → oben → beide. Gilt bis zur nächsten Map.':
        "Cambia ciò che mostrano le mappe con piani (Midwich): entrambi uno sotto l'altro → inferiore → superiore → entrambi. Vale fino alla prossima mappa.",
    'Etagen untereinander zeigen':
        "Mostra i piani uno sotto l'altro",
    'An: Karten mit Etagen (Midwich) zeigen alle Etagen untereinander, oben über unten – jede so groß wie eine normale Karte, soweit der Platz reicht. Aus: Sie starten mit der unteren Etage. Der Knopf „Etage“ oder der Hotkey schaltet jederzeit um.':
        "On: le mappe con piani (Midwich) mostrano tutti i piani uno sotto l'altro, il superiore sopra l'inferiore – ognuno grande come una mappa normale, per quanto lo spazio lo consente. Off: iniziano con il piano inferiore. Il pulsante «Piano» o l'hotkey cambia in qualsiasi momento.",
    '{map} um {deg}° gedreht.':
        '{map} ruotata di {deg}°.',
    'Drehung für {map} entfernt.':
        'Rotazione per {map} rimossa.',
    'Dreht die angezeigte Karte um 90° im Uhrzeigersinn (für jede Map gemerkt). Der Map-Name darüber bleibt aufrecht, die Zahlen in der Karte drehen sich mit.':
        'Ruota la mappa mostrata di 90° in senso orario (memorizzato per ogni mappa). Il nome della mappa sopra resta dritto, i numeri dentro la mappa ruotano con essa.',
    'Eigene Grösse für {map} entfernt – es gilt wieder der Schieberegler.':
        'Dimensione propria per {map} rimossa – vale di nuovo il cursore.',
    'Entfernt eigene Grösse und Drehung der angezeigten Map – danach gilt wieder der Schieberegler für alle Maps.':
        'Rimuove la dimensione propria e la rotazione della mappa mostrata – vale di nuovo il cursore per tutte le mappe.',
    'Deckkraft':
        'Opacità',
    'Nur zeigen, wenn DBD das aktive Fenster ist':
        'Mostra solo mentre DBD è la finestra attiva',
    'Map-Namen über der Karte anzeigen':
        'Mostra il nome della mappa sopra la mappa',
    'Rundentimer unter der Karte anzeigen':
        'Mostra il timer del round sotto la mappa',
    'Verbundenen Server unter der Karte':
        'Server connesso sotto la mappa',
    'Transparenter Rand um die Karte':
        'Bordo trasparente intorno alla mappa',
    'Map beim Match-Start automatisch erkennen':
        "Rileva la mappa automaticamente all'inizio di una partita",
    'Overlay ausblenden, sobald ich nicht mehr in der Runde bin':
        "Nascondi l'overlay appena sono fuori dal round",
    'erkennt Ergebnisbildschirm, Lobby/Menüs, Ladebildschirm und geschlossenes DBD':
        'rileva schermata dei risultati, lobby/menu, schermata di caricamento e chiusura di DBD',
    'Overlay pausieren, solange ein DBD-Menü offen ist':
        "Metti in pausa l'overlay mentre è aperto un menu di DBD",
    'erkannt am sichtbaren Mauszeiger (ESC-Menü, Ergebnisbildschirm, Lobby)':
        'rilevato dal puntatore del mouse visibile (menu ESC, schermata dei risultati, lobby)',
    'Spielsprache (Map-Namen)':
        'Lingua di gioco (nomi delle mappe)',
    'Erweitert':
        'Avanzate',
    'Erweitert (Fehlersuche)':
        'Avanzate (risoluzione problemi)',
    'Technik':
        'Tecnico',
    'Auch erkennen, wenn andere Fenster über DBD liegen':
        'Rileva anche quando altre finestre coprono DBD',
    'Fensteraufnahme wie bei OBS, nur solange DBD im Hintergrund ist':
        'cattura finestra come OBS, solo mentre DBD è in background',
    'Scans/Sek.':
        'Scansioni/s',
    'Rundenende-Erkennung: {state}':
        'Rilevamento fine round: {state}',
    'Debug-Bilder speichern':
        'Salva immagini di debug',
    'Banner jeder Erkennung für „Erkennung prüfen“ sammeln':
        'Conserva il banner di ogni rilevamento per «Verifica rilevamento»',
    '{n} Banner gesammelt':
        '{n} banner conservati',
    '1 Banner gesammelt':
        '1 banner conservato',
    'letzte Prüfung: {hits} von {total} erkannt':
        'ultima verifica: {hits} di {total} riconosciuti',
    'Erkennung prüfen':
        'Verifica rilevamento',
    'Korpus exportieren …':
        'Esporta corpus …',
    'Korpus exportieren':
        'Esporta corpus',
    'Korpus-Ordner öffnen':
        'Apri cartella corpus',
    'Noch keine Banner gesammelt – sie kommen mit jeder erkannten Map.':
        'Ancora nessun banner conservato – arrivano con ogni mappa rilevata.',
    'Erkennung prüfen: {n} Banner werden neu gelesen …':
        'Verifica rilevamento: rilettura di {n} banner …',
    'Erkennung prüfen fehlgeschlagen: {error}':
        'Verifica rilevamento non riuscita: {error}',
    '{hits} von {total} Bannern wieder erkannt ({seconds} s).':
        '{hits} di {total} banner riconosciuti di nuovo ({seconds} s).',
    '{n} nicht lesbar.':
        '{n} illeggibili.',
    'Erkennung prüfen: {text}':
        'Verifica rilevamento: {text}',
    'Erkennung prüfen – {stamp}: erwartet {want}, gelesen „{read}“ → {got}':
        'Verifica rilevamento – {stamp}: previsto {want}, letto «{read}» → {got}',
    'Die Treffer, die fehlen, stehen im Log.':
        'I banner non riconosciuti sono nel log.',
    'Korpus exportiert: {n} Dateien nach {path}':
        'Corpus esportato: {n} file in {path}',
    'Korpus exportieren fehlgeschlagen: {error}':
        'Esportazione del corpus non riuscita: {error}',
    'Speichert bei jeder erkannten Map den Ausschnitt um die Banner-Linie (Name und Realm) im Datenordner unter corpus/, höchstens 300 Stück – die Grundlage für „Erkennung prüfen“. Der Ausschnitt kann den linken HUD-Rand mit Spielernamen zeigen; er bleibt auf diesem PC.':
        "Conserva, per ogni mappa rilevata, la parte intorno alla linea del banner (nome e Realm) nella cartella dati sotto corpus/, al massimo 300 – la base di «Verifica rilevamento». La parte può mostrare il bordo sinistro dell'HUD con nomi dei giocatori; resta su questo PC.",
    'Liest alle gesammelten Banner mit der Erkennung neu und zählt, wie viele wieder die gespeicherte Map ergeben – nach einem Update oder einer geänderten Spielsprache. Läuft im Hintergrund, Ergebnis im Log.':
        'Rilegge tutti i banner conservati con il rilevamento e conta quanti restituiscono di nuovo la mappa salvata – dopo un aggiornamento o un cambio di lingua di gioco. Gira in background, risultato nel log.',
    'Packt alle gesammelten Banner mit ihren Angaben in eine ZIP-Datei – z. B. um sie für die Tests des Projekts weiterzugeben. Vorher die Bilder ansehen: sie können Spielernamen zeigen.':
        'Mette tutti i banner conservati con i loro dettagli in un file ZIP – ad es. per darli ai test del progetto. Guarda prima le immagini: possono mostrare nomi dei giocatori.',
    'Öffnet den Ordner corpus/ im Datenordner.':
        'Apre la cartella corpus/ nella cartella dati.',
    'Bildschirm jetzt scannen':
        'Scansiona lo schermo ora',
    'Diagnose kopieren':
        'Copia diagnostica',
    'Verbundener Spielserver':
        'Server di gioco connesso',
    'Serverregionen':
        'Regioni server',
    'DBD sucht Matches nur in den angehakten Regionen (über die Windows-hosts-Datei, das Spiel wird nicht verändert). Nach „Auswahl anwenden“ DBD neu starten.':
        'DBD cerca partite solo nelle regioni spuntate (tramite il file hosts di Windows, il gioco non viene modificato). Riavvia DBD dopo «Applica selezione».',
    'Region':
        'Regione',
    'hosts-Datei':
        'File hosts',
    'Ping messen':
        'Misura ping',
    'Auswahl anwenden':
        'Applica selezione',
    'Alles freigeben':
        'Consenti tutte',
    'Mit VPN unzuverlässig. Region-Tools sind von BHVR weder erlaubt noch verboten – auf eigene Verantwortung.':
        'Inaffidabile con una VPN. Gli strumenti di regione non sono né consentiti né vietati da BHVR – a tuo rischio.',
    'Warte auf Windows (Administratorrechte) …':
        'In attesa di Windows (diritti di amministratore) …',
    'Aus':
        'Disattivato',
    'Zeigt Region und Ping des Spielservers, auch im Overlay (braucht Administratorrechte).':
        "Mostra regione e ping del server di gioco, anche nell'overlay (richiede diritti di amministratore).",
    'DBD läuft mit {w}×{h}, kleiner als 1920×1080: die Erkennung ist unsicherer (vor allem Lobby-Knopf und Killername). Fenster größer ziehen oder „Fenster-Vollbild“ nutzen.':
        'DBD gira a {w}×{h}, meno di 1920×1080: il rilevamento è meno affidabile (soprattutto il pulsante della lobby e il nome del Killer). Ingrandisci la finestra o usa «Schermo intero in finestra».',
    'DBD-Fenster ist schmaler als 16:9 ({w}×{h}): diese Form ist ungetestet, Map- und Rundenende-Erkennung können danebenliegen. Am sichersten: 16:9 oder breiter.':
        'La finestra di DBD è più stretta di 16:9 ({w}×{h}): questa forma non è testata, il rilevamento di mappa e fine round potrebbe sbagliare. Più sicuro: 16:9 o più largo.',
    'Verbunden mit: {server}':
        'Connesso a: {server}',
    'pausiert, bis DBD läuft':
        'in pausa finché DBD non è avviato',
    'Anzeige des Spielservers beendet.':
        'Visualizzazione server di gioco fermata.',
    'Spielserver-Anzeige: {error}':
        'Visualizzazione server di gioco: {error}',
    'Spielserver-Anzeige läuft (liest nur Paketköpfe, keine Inhalte).':
        'Visualizzazione server di gioco attiva (legge solo le intestazioni dei pacchetti, nessun contenuto).',
    'Spielserver-Anzeige pausiert – DBD läuft nicht (startet automatisch mit DBD).':
        'Visualizzazione server di gioco in pausa – DBD non è in esecuzione (riparte con DBD).',
    'Spielserver-Anzeige beendet: {error}':
        'Visualizzazione server di gioco fermata: {error}',
    ' – nicht in deiner Regionsauswahl':
        ' – non nella tua selezione di regioni',
    'Verbunden mit Spielserver: {region}{note}.':
        'Connesso al server di gioco: {region}{note}.',
    'hosts-Datei nicht lesbar: {error}':
        'File hosts non leggibile: {error}',
    'Aktiv: nur {regions} erlaubt.':
        'Attivo: consentite solo {regions}.',
    '(keine)':
        '(nessuna)',
    'Keine eigene Auswahl aktiv, aber andere Einträge sperren Regionen.':
        'Nessuna selezione propria attiva, ma altre voci bloccano delle regioni.',
    'Keine Region gesperrt – DBD wählt selbst.':
        'Nessuna regione bloccata – DBD sceglie da solo.',
    'anderen Programmen':
        'altri programmi',
    ' Es gibt {n} Einträge von {who} für DBD-Server (werden beim Anwenden ersetzt).':
        " Ci sono {n} voci di {who} per i server di DBD (sostituite all'applicazione).",
    'Serverregionen: {text}':
        'Regioni server: {text}',
    'Messe Ping zu den Serverregionen …':
        'Misurazione del ping verso le regioni server …',
    'Ping fehlgeschlagen: {error}':
        'Ping non riuscito: {error}',
    'Am schnellsten: {list}.':
        'Più veloci: {list}.',
    'Keine Region hat geantwortet (Internet/Firewall/VPN?).':
        'Nessuna regione ha risposto (internet/firewall/VPN?).',
    'Bitte mindestens eine Region anhaken.':
        'Spunta almeno una regione.',
    'Erlaubt bleiben: {names}.\n\nAlle anderen DBD-Serverregionen werden in der Windows-hosts-Datei gesperrt. Windows fragt gleich nach Administratorrechten.':
        'Consentite: {names}.\n\nTutte le altre regioni server di DBD vengono bloccate nel file hosts di Windows. Windows chiederà i diritti di amministratore.',
    '{n} vorhandene Einträge anderer Programme (z. B. Make Your Choice) für DBD-Server werden dabei entfernt.':
        '{n} voci esistenti di altri programmi (ad es. Make Your Choice) per i server di DBD verranno rimosse.',
    'Danach DBD neu starten, damit es wirkt.':
        'Poi riavvia DBD perché abbia effetto.',
    'Serverregionen anwenden':
        'Applica regioni server',
    'Nur noch {names} erlaubt':
        'Consentite solo {names}',
    'Es ist nichts gesperrt.':
        'Nulla è bloccato.',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen (auch die von Make Your Choice)?':
        'Rimuovere dal file hosts tutti i blocchi delle regioni server di DBD (compresi quelli di Make Your Choice)?',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen?':
        'Rimuovere dal file hosts tutti i blocchi delle regioni server di DBD?',
    'Windows fragt gleich nach Administratorrechten. Danach DBD neu starten.':
        'Windows chiederà i diritti di amministratore. Poi riavvia DBD.',
    'Serverregionen freigeben':
        'Consenti regioni server',
    'Alle Regionen freigegeben':
        'Tutte le regioni consentite',
    'Serverregionen: {text}. DBD neu starten, damit es wirkt.':
        'Regioni server: {text}. Riavvia DBD perché abbia effetto.',
    '{text}. DBD jetzt neu starten.':
        '{text}. Riavvia DBD ora.',
    'Keine Änderung nötig.':
        'Nessuna modifica necessaria.',
    'unbekannter Fehler':
        'errore sconosciuto',
    'Firewall-Regeln von Make Your Choice („Enforced“) gefunden – sie sperren Regionen unabhängig von der hosts-Datei. In Make Your Choice „Revert to Default“ drücken.':
        'Trovate regole firewall di Make Your Choice («Enforced») – bloccano le regioni indipendentemente dal file hosts. Premi «Revert to Default» in Make Your Choice.',
    'Achtung: Firewall-Regeln von Make Your Choice aktiv (siehe Log).':
        'Attenzione: sono attive regole firewall di Make Your Choice (vedi log).',
    'Europa':
        'Europa',
    'Amerika':
        'Americhe',
    'Asien':
        'Asia',
    'Ozeanien':
        'Oceania',
    'frei':
        'consentita',
    'gesperrt':
        'bloccata',
    'gesperrt (fremd)':
        'bloccata (altro programma)',
    'umgeleitet (fremd)':
        'reindirizzata (altro programma)',
    'Frankfurt':
        'Francoforte',
    'Irland':
        'Irlanda',
    'London':
        'Londra',
    'USA Ost (N. Virginia)':
        'US Est (N. Virginia)',
    'USA Ost (Ohio)':
        'US Est (Ohio)',
    'USA West (N. Kalifornien)':
        'US Ovest (N. California)',
    'USA West (Oregon)':
        'US Ovest (Oregon)',
    'Kanada (Zentral)':
        'Canada (Centrale)',
    'Südamerika (São Paulo)':
        'Sud America (San Paolo)',
    'Tokio':
        'Tokyo',
    'Seoul':
        'Seul',
    'Mumbai':
        'Mumbai',
    'Singapur':
        'Singapore',
    'Hongkong':
        'Hong Kong',
    'Sydney':
        'Sydney',
    'Name nicht auflösbar':
        'nome non risolvibile',
    'Start mit Administratorrechten fehlgeschlagen (Fehler {code}).':
        'Avvio con diritti di amministratore non riuscito (errore {code}).',
    'Hilfsprogramm nicht gestartet.':
        'Programma di supporto non avviato.',
    'Das Hilfsprogramm hat kein Ergebnis geliefert (Code {code}).':
        'Il programma di supporto non ha restituito alcun risultato (codice {code}).',
    'Zeitüberschreitung beim Schreiben der hosts-Datei.':
        'Timeout durante la scrittura del file hosts.',
    'Abgebrochen (keine Administratorrechte erteilt).':
        'Annullato (diritti di amministratore non concessi).',
    'Warte auf Match …':
        'In attesa di una partita …',
    'Global':
        'Globale',
    'keine Daten vom Mitschnitt':
        'nessun dato dalla cattura',
    'Nur unter Windows verfügbar.':
        'Disponibile solo su Windows.',
    'Mitschnitt beendet (Code {code}).':
        'Cattura terminata (codice {code}).',
    'Fehler: {error}':
        'Errore: {error}',
    'Statistik':
        'Statistiche',
    'Maps':
        'Mappe',
    'Map':
        'Mappa',
    'Runden':
        'Round',
    'Ø Dauer':
        'Durata media',
    'Letzte Runden':
        'Ultimi round',
    'Gesamter Zeitraum':
        'Sempre',
    'Heute':
        'Oggi',
    'Diese Woche':
        'Questa settimana',
    'Dieser Monat':
        'Questo mese',
    'Dieses Jahr':
        "Quest'anno",
    'Alle Regionen':
        'Tutte le regioni',
    'Alle Killer':
        'Tutti i Killer',
    'Häufigste Map':
        'Mappa più frequente',
    'Der markierte Name (Skin oder neuer Killer) zählt ab jetzt als der gewählte Killer – auch in allen bisherigen Runden.':
        "Il nome selezionato (skin o nuovo Killer) conta d'ora in poi come il Killer scelto – anche in tutti i round passati.",
    'Entfernt alle eigenen Killer-Zuordnungen; die Namen erscheinen wieder so, wie sie gelesen wurden.':
        'Rimuove tutte le assegnazioni personali dei Killer; i nomi compaiono di nuovo come sono stati letti.',
    'Zuordnen':
        'Assegna',
    'Warte auf Map':
        'In attesa della mappa',
    'Solange DBD läuft und keine Karte eingeblendet ist, zeigt das Overlay eine kleine Karte: „Warte auf Map“, darunter Suche/Lobby (z. B. „Suche läuft: 02:13 · Nurse“) oder die letzte Runde. Gilt nicht, wenn du die Karte selbst ausgeblendet hast.':
        "Mentre DBD è in esecuzione e nessuna mappa è mostrata, l'overlay mostra una piccola scheda: «In attesa della mappa», sotto la ricerca/lobby (ad es. «Ricerca: 02:13 · Nurse») o l'ultimo round. Non quando hai nascosto tu la mappa.",
    'Ohne Karte: „Warte auf Map“ und Lobby-Status anzeigen':
        'Senza mappa: mostra «In attesa della mappa» e lo stato della lobby',
    'Killer der Runde:':
        'Killer del round:',
    'Killer setzen':
        'Imposta Killer',
    'Notiz zum Killer:':
        'Nota sul Killer:',
    'Um diese Tageszeit ({span} Uhr) am schnellsten: {region} – Wartezeit {wait} (Median), {n} Runden':
        "Più veloce a quest'ora ({span} h): {region} – attesa {wait} (mediana), {n} round",
    'Ø {ping} ms':
        'Ø {ping} ms',
    'danach {region} ({wait})':
        'poi {region} ({wait})',
    'Notiz speichern':
        'Salva nota',
    'Notiz zu {killer} gespeichert.':
        'Nota su {killer} salvata.',
    'Notiz zu {killer} gelöscht.':
        'Nota su {killer} rimossa.',
    'Eigene Notiz zum markierten Killer, z. B. „Lithe, nicht vaulten“. Erscheint im Spiel unter der Map-Notiz, sobald dieser Killer in der Runde ist (eigener Killer oder, als Survivor, der aus der Lobby). Leer speichern löscht sie.':
        'La tua nota sul Killer selezionato, ad es. «agile, non scavalcare». Mostrata nel gioco sotto la nota della mappa appena questo Killer è nel round (il tuo Killer o, da Sopravvissuto, quello della lobby). Salvarla vuota la rimuove.',
    'Killer konnte nicht gespeichert werden: {error}':
        'Impossibile salvare il Killer: {error}',
    'Killer für {map} ({when}) auf {killer} gesetzt.':
        'Killer per {map} ({when}) impostato su {killer}.',
    'Map der Runde:':
        'Mappa del round:',
    'Setzt die Map nur für die markierten Runden – wenn das Banner falsch gelesen wurde. Statistik, eigener Rekord und die Verknüpfung mit den Match-Daten folgen; die Aufnahme behält ihren Namen.':
        'Imposta la mappa solo per i round selezionati – quando il banner è stato letto male. Statistiche, record personale e collegamento ai dati partita si adeguano; la registrazione mantiene il suo nome.',
    'Map setzen':
        'Imposta mappa',
    'Map konnte nicht gespeichert werden: {error}':
        'Impossibile salvare la mappa: {error}',
    'Map der Runde vom {when} auf {map} gesetzt.':
        'Mappa del round del {when} impostata su {map}.',
    'Setzt den Killer nur für die markierte Runde und zählt sie als Killer-Runde – z. B. wenn sie fälschlich als Survivor gezählt wurde oder der Name falsch gelesen wurde.':
        'Imposta il Killer solo per il round selezionato e lo conta come round da Killer – ad es. se è stato contato per errore come Sopravvissuto o il nome è stato letto male.',
    'Zuordnungen löschen':
        'Elimina assegnazioni',
    '„{name}“ zählt jetzt als {killer}.':
        '«{name}» ora conta come {killer}.',
    'Alle eigenen Killer-Zuordnungen löschen?':
        'Eliminare tutte le assegnazioni personali dei Killer?',
    'Killer-Zuordnungen gelöscht.':
        'Assegnazioni dei Killer eliminate.',
    'ohne Region':
        'nessuna regione',
    'Anteil':
        'Quota',
    'Region nur bekannt, wenn im Tab Server „Verbundener Spielserver“ an war.':
        'Regione nota solo se «Server di gioco connesso» era attivo nella scheda Server.',
    'Wann':
        'Quando',
    'Dauer':
        'Durata',
    'Alle Runden löschen …':
        'Elimina tutti i round …',
    'Runde löschen':
        'Elimina round',
    'Ø {kills} Kills · {n} Runden':
        'Ø {kills} uccisioni · {n} round',
    'Killer: Ø {kills} Kills, {four}× 4K ({n})':
        'Killer: Ø {kills} uccisioni, {four}× 4K ({n})',
    'Survivor: {share} entkommen ({n})':
        'Sopravvissuto: {share} fughe ({n})',
    '{share} entkommen · {n} Runden':
        '{share} fughe · {n} round',
    'Eigene Bilanz unter dem Timer':
        'Record personale sotto il timer',
    'Eigene Notiz unter dem Timer':
        'Nota personale sotto il timer',
    'Zeigt deine eigene Notiz zur Map unter dem Rundentimer – geschrieben auf der Seite Maps (Map anklicken oder Rechtsklick → „Notiz bearbeiten …“), höchstens vier Zeilen.':
        'Mostra la tua nota sulla mappa sotto il timer del round – scritta nella pagina Mappe (clic su una mappa o clic destro → «Modifica nota …»), al massimo quattro righe.',
    'Deine Notiz zu dieser Map – wird beim Tippen gespeichert und im Spiel unter dem Timer gezeigt (höchstens vier Zeilen). Leer = keine Notiz.':
        'La tua nota su questa mappa – salvata mentre scrivi e mostrata nel gioco sotto il timer (al massimo quattro righe). Vuota = nessuna nota.',
    'Eigene Notiz (im Spiel unter dem Timer)':
        'Nota personale (nel gioco sotto il timer)',
    'z. B. Shack links vom Main, Gen im Keller …':
        'ad es. capanno a sinistra del main, generatore nel seminterrato …',
    'Notiz bearbeiten …':
        'Modifica nota …',
    'Map-Stile':
        'Stili mappa',
    'Alle auf einmal':
        'Tutti insieme',
    'Kartenstile für {map} werden im Hintergrund erstellt.':
        'Gli stili mappa di {map} vengono creati in background.',
    'Kartenstil {style} für {map} wird im Hintergrund erstellt.':
        'Lo stile mappa {style} di {map} viene creato in background.',
    'Eigene Notiz':
        'Nota personale',
    'Eigene Notiz: {note}':
        'Nota personale: {note}',
    'Zeigt unter dem Rundentimer, wie es dir auf dieser Map bisher ging: als Killer Ø Kills, als Survivor den Anteil Escapes – aus den Runden mit Daten der Stats-Seite, ab 3 Runden.':
        'Mostra sotto il timer del round come ti è andata finora su questa mappa: media uccisioni da Killer, quota di fughe da Sopravvissuto – dai round con dati della pagina statistiche, a partire da 3 round.',
    'Entfernt die markierte Runde aus der Statistik – z. B. eine Map, die mitten im Match falsch erkannt wurde. Fragt vorher nach.':
        'Rimuove il round selezionato dalle statistiche – ad es. una mappa letta male a metà partita. Prima chiede conferma.',
    'Runde {what} aus der Statistik löschen?':
        'Eliminare il round {what} dalle statistiche?',
    'Runde konnte nicht gelöscht werden: {error}':
        'Impossibile eliminare il round: {error}',
    'Runde gelöscht: {map} ({when}).':
        'Round eliminato: {map} ({when}).',
    'Noch keine Runden gespeichert.':
        'Ancora nessun round salvato.',
    'Alle Runden löschen':
        'Elimina tutti i round',
    'Alle gespeicherten Runden löschen? Vorher wird eine Kopie in {folder}/ angelegt.':
        'Eliminare tutti i round salvati? Prima viene salvata una copia in {folder}/.',
    'Es sind keine Runden gespeichert.':
        'Nessun round salvato.',
    'Die Kopie in {folder}/ konnte nicht angelegt werden – die Runden bleiben gespeichert.':
        'Non è stato possibile creare la copia in {folder}/ – i round restano salvati.',
    'Nicht angewendet – 1 Änderung. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        'Non applicato – 1 modifica. «Applica selezione» la applica; poi riavvia DBD.',
    'Nicht angewendet – {n} Änderungen. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        'Non applicato – {n} modifiche. «Applica selezione» le applica; poi riavvia DBD.',
    'Öffnet die markierten Runden bzw. Clips nacheinander im grossen Editor – als eine Montage (mehrere markieren: Strg- oder Umschalt-Klick).':
        "Apre i round o le clip selezionati uno dopo l'altro nel grande editor – come un montaggio (selezionane più di uno: Ctrl o Shift+clic).",
    'Ursache: {cause}':
        'Causa: {cause}',
    'Keine Region angehakt – für „Auswahl anwenden“ mindestens eine anhaken.':
        'Nessuna regione spuntata – spuntane almeno una per «Applica selezione».',
    'Anwenden':
        'Applica',
    'Freigeben':
        'Sblocca',
    'Importieren':
        'Importa',
    'Markieren':
        'Segna',
    'Trotzdem beenden':
        'Esci comunque',
    'Rundenverlauf gelöscht.':
        'Cronologia dei round eliminata.',
    'Löscht alle gespeicherten Runden (Datei rounds.jsonl) – nach einer Rückfrage, vorher kommt eine Kopie in den Ordner backup.':
        'Elimina tutti i round salvati (file rounds.jsonl) – dopo una conferma; prima viene salvata una copia nella cartella di backup.',
    'Anzeigen:':
        'Mostra:',
    'Leeren':
        'Svuota',
    'Log-Datei öffnen':
        'Apri file di log',
    'Sprache und Darstellung':
        'Lingua e aspetto',
    'Wirkt nach dem nächsten Start des Programms.':
        'Ha effetto al prossimo avvio del programma.',
    'Sprache geändert – wirkt nach dem nächsten Start des Programms.':
        'Lingua cambiata – ha effetto al prossimo avvio del programma.',
    'Dark Mode':
        'Modalità scura',
    'Hotkeys':
        'Hotkey',
    'Standard':
        'Predefiniti',
    'Zum Ändern anklicken und die neue Tastenkombination drücken.':
        'Fai clic per cambiare, poi premi la nuova combinazione di tasti.',
    'Start und Infobereich':
        'Avvio e area di notifica',
    'Beim Minimieren in den Infobereich':
        "Riduci a icona nell'area di notifica",
    'Mit Windows starten':
        'Avvia con Windows',
    'Updates':
        'Aggiornamenti',
    'Beim Start Updates installieren':
        "Installa aggiornamenti all'avvio",
    'nur über start.bat bzw. die Desktop-Verknüpfung; eigene Änderungen werden nie überschrieben':
        'solo tramite start.bat o il collegamento sul desktop; le tue modifiche non vengono mai sovrascritte',
    'Eigene Map-Zuordnungen':
        'Assegnazioni mappa personali',
    'Jetzt nach Updates suchen':
        'Cerca aggiornamenti ora',
    'Aktualisieren und neu starten':
        'Aggiorna e riavvia',
    'Suche nach Updates …':
        'Ricerca aggiornamenti …',
    'Beim Start nach Updates suchen':
        "Cerca aggiornamenti all'avvio",
    'Laden und Installieren nur nach deiner Bestätigung; das Setup wird per SHA-256 geprüft':
        'scaricati e installati solo dopo la tua conferma; il setup viene verificato con SHA-256',
    'Update-Prüfung fehlgeschlagen: {error}':
        'Ricerca aggiornamenti non riuscita: {error}',
    'Kein Update – Version {version} (Build {build}) ist aktuell.':
        'Nessun aggiornamento – la versione {version} (build {build}) è aggiornata.',
    'Update verfügbar: {old} → {new} (Build {build}).':
        'Aggiornamento disponibile: {old} → {new} (build {build}).',
    'Lade Update …':
        "Download dell'aggiornamento …",
    'GitHub antwortet gerade nicht (HTTP {code}) – bitte in einigen Minuten erneut versuchen.':
        'GitHub al momento non risponde (HTTP {code}) – riprova tra qualche minuto.',
    'Keine Antwort von GitHub (Zeitüberschreitung/Verbindung) – bitte später erneut versuchen.':
        'Nessuna risposta da GitHub (timeout/connessione) – riprova più tardi.',
    'GitHub antwortet nicht – neuer Versuch {n} von {total} …':
        'GitHub non risponde – tentativo {n} di {total} …',
    'Lade Update … {pct} %':
        "Download dell'aggiornamento … {pct} %",
    'Update nicht geladen: {error}':
        'Aggiornamento non scaricato: {error}',
    'Update {version} (Build {build}) geladen und geprüft.':
        'Aggiornamento {version} (build {build}) scaricato e verificato.',
    'Update installieren':
        'Installa aggiornamento',
    'Fog Scout {version} (Build {build}) ist geladen und per SHA-256 geprüft. Jetzt installieren? Das Programm schliesst sich und startet danach neu.':
        'Fog Scout {version} (build {build}) è scaricato e verificato con SHA-256. Installarlo ora? Il programma si chiude e poi si riavvia.',
    'Installieren':
        'Installa',
    'Update gesperrt: eine Runde läuft oder ein Clip wird gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Aggiornamento bloccato: è in corso un round o si sta salvando una clip. Dopo fai di nuovo clic su «Aggiorna e riavvia».',
    'Programm schliesst sich und installiert das Update …':
        "Il programma si chiude e installa l'aggiornamento …",
    'Das Update wurde nicht gestartet: Die Setup-Datei hat sich seit dem Download verändert oder fehlt. Bitte das Update noch einmal laden.':
        "L'aggiornamento non è stato avviato: il file di setup è cambiato dopo il download o manca. Scarica di nuovo l'aggiornamento.",
    'Das Update wurde nicht gestartet: Die Setup-Datei liess sich nicht sicher bereitstellen ({error}). Bitte das Update noch einmal laden.':
        "L'aggiornamento non è stato avviato: non è stato possibile collocare il file di setup in modo sicuro ({error}). Scarica di nuovo l'aggiornamento.",
    'Das Setup konnte nicht gestartet werden (Abfrage nach Administratorrechten abgebrochen?). Erneut versuchen oder das Setup selbst starten:\n{path}':
        'Impossibile avviare il setup (richiesta di amministratore annullata?). Riprova o avvia tu il setup:\n{path}',
    'Neustart nicht möglich: {error}':
        'Riavvio non possibile: {error}',
    'Nur unter Windows: bitte das Programm über start.bat neu starten.':
        'Solo Windows: riavvia il programma tramite start.bat.',
    'Programm startet neu und installiert das Update …':
        "Il programma si riavvia e installa l'aggiornamento …",
    'Fragt GitHub, ob es eine neue Version gibt (nur bei diesem Klick). Installiert wird erst mit „Aktualisieren und neu starten“.':
        "Chiede a GitHub se c'è una nuova versione (solo con questo clic). Viene installata solo con «Aggiorna e riavvia».",
    'Beendet das Programm und startet es über start.bat neu – dabei wird das Update installiert. Die installierte Version lädt das Setup, prüft es per SHA-256 und fragt vor dem Installieren.':
        "Chiude il programma e lo riavvia tramite start.bat – che installa l'aggiornamento. La versione installata scarica il setup, lo verifica con SHA-256 e chiede prima di installare.",
    'Fragt nach jedem Start einmal GitHub, ob es ein neues Release gibt. Geladen und installiert wird nur nach deinem Klick und einer Rückfrage.':
        "Chiede a GitHub una volta dopo ogni avvio se c'è una nuova release. Download e installazione avvengono solo dopo il tuo clic e una conferma.",
    'Alle löschen':
        'Elimina tutto',
    'Datenordner öffnen':
        'Apri cartella dati',
    'Karten-Ordner öffnen':
        'Apri cartella mappe',
    'liest nur Bildschirmpixel, sendet keine Eingaben ans Spiel.':
        'legge solo i pixel dello schermo, non invia alcun input al gioco.',
    'Inoffizielles Fan-Tool, nicht von Behaviour Interactive genehmigt – Nutzung auf eigene Gefahr (siehe LICENSE).':
        'Strumento non ufficiale creato da un fan, non approvato da Behaviour Interactive – usalo a tuo rischio (vedi LICENSE).',
    'Kartenbilder: Lethia (hens333.com/callouts, mit Erlaubnis von Hens) · Map-Namen: Luca Fontanot (DBD Map Overlay).':
        'Immagini mappa: Lethia (hens333.com/callouts, con il permesso di Hens) · nomi mappa: Luca Fontanot (DBD Map Overlay).',
    'Keine. Unbekannte Map-Namen lassen sich nach dem Match im Hauptfenster zuordnen.':
        'Nessuna. I nomi di mappa sconosciuti possono essere assegnati nella finestra principale dopo la partita.',
    'Eigene Zuordnungen':
        'Assegnazioni personali',
    'Alle eigenen Map-Zuordnungen löschen?':
        'Eliminare tutte le assegnazioni mappa personali?',
    'Eigene Map-Zuordnungen gelöscht.':
        'Assegnazioni mappa personali eliminate.',
    'Spielsprachen: {langs}':
        'Lingue di gioco: {langs}',
    'Änderbar, wenn das Programm über die Desktop-Verknüpfung gestartet wurde (verknuepfung_erstellen.bat einmal ausführen).':
        'Modificabile se il programma è stato avviato tramite il collegamento sul desktop (esegui una volta verknuepfung_erstellen.bat).',
    'Wird eingerichtet …':
        'Configurazione …',
    'Startet ab jetzt mit Windows im Infobereich.':
        "D'ora in poi si avvia con Windows nell'area di notifica.",
    'Startet nicht mehr mit Windows.':
        'Non si avvia più con Windows.',
    'Startet ab jetzt mit Windows im Infobereich (abschaltbar unter Einstellungen → Start und Infobereich).':
        "D'ora in poi si avvia con Windows nell'area di notifica (disattivabile in Impostazioni → Avvio e area di notifica).",
    'Autostart mit Windows fehlgeschlagen: {error}':
        "Impossibile configurare l'avvio con Windows: {error}",
    'Fehlgeschlagen: {error}':
        'Non riuscito: {error}',
    'Nur unter Windows.':
        'Solo Windows.',
    'Tipp: Fog Scout über die Verknüpfung im Startmenü starten – dann läuft es ohne Windows-Abfrage mit den nötigen Rechten.':
        'Suggerimento: avvia Fog Scout con il collegamento nel menu Start – così gira con i diritti necessari, senza richiesta di Windows.',
    'Änderbar, wenn das Programm über die Verknüpfung im Startmenü gestartet wurde.':
        'Modificabile se il programma è stato avviato con il collegamento nel menu Start.',
    'Tipp: Einmal als Administrator starten (Rechtsklick auf start.bat → „Als Administrator ausführen“) – dann richtet das Programm die Desktop-Verknüpfung ein, die künftig ohne Windows-Abfrage startet.':
        'Suggerimento: avvialo una volta come amministratore (clic destro su start.bat → «Esegui come amministratore») – il programma crea allora il collegamento sul desktop, che da quel momento lo avvia senza richiesta di Windows.',
    'Desktop-Verknüpfung eingerichtet/aktualisiert: startet ab jetzt ohne Windows-Abfrage.':
        "Collegamento sul desktop creato/aggiornato: d'ora in poi si avvia senza richiesta di Windows.",
    'Einrichtung der Verknüpfung fehlgeschlagen: {error}':
        'Creazione del collegamento non riuscita: {error}',
    'Verknüpfung erstellt: {path}':
        'Collegamento creato: {path}',
    'Aufgabe konnte nicht angelegt werden: {error}':
        "Impossibile creare l'attività pianificata: {error}",
    'Verknüpfung konnte nicht angelegt werden: {error}':
        'Impossibile creare il collegamento: {error}',
    '(Autostart nicht erneuert: {error})':
        '(avvio automatico non rinnovato: {error})',
    'Symbol im Infobereich nicht verfügbar ({error}) – Minimieren wie gewohnt.':
        "Icona nell'area di notifica non disponibile ({error}) – la riduzione a icona funziona come al solito.",
    'Öffnen nur unter Windows: {path}':
        "L'apertura funziona solo su Windows: {path}",
    'Kann {path} nicht öffnen: {error}':
        'Impossibile aprire {path}: {error}',
    'Fenster öffnen':
        'Apri finestra',
    'Beenden':
        'Esci',
    'Hotkey: {keys}':
        'Hotkey: {keys}',
    'Hotkey {keys} ({action}) nicht verfügbar: {why}.':
        'Hotkey {keys} ({action}) non disponibile: {why}.',
    '{n} Hotkey(s) nicht verfügbar – siehe Log.':
        '{n} hotkey non disponibili – vedi log.',
    '– aus –':
        '– disattivato –',
    'Tasten drücken …':
        'Premi i tasti …',
    'Neue Kombination drücken – Esc bricht ab, Entf schaltet den Hotkey aus.':
        "Premi la nuova combinazione – Esc annulla, Del disattiva l'hotkey.",
    '{keys} ist schon „{action}“ – andere wählen.':
        "{keys} è già «{action}» – scegline un'altra.",
    'aus':
        'disattivato',
    'an':
        'attivo',
    'Hotkey {action}: {keys}.':
        'Hotkey {action}: {keys}.',
    'Standard-Hotkeys wiederhergestellt.':
        'Hotkey predefiniti ripristinati.',
    'Strg':
        'Ctrl',
    'Taste „{key}“ geht nicht als Hotkey':
        'Il tasto «{key}» non può essere usato come hotkey',
    'Bitte mit Strg und/oder Alt kombinieren':
        'Combinalo con Ctrl e/o Alt',
    'schon von einem anderen Programm belegt':
        'già usato da un altro programma',
    'Für „{map}“ gibt es kein Bild.':
        "Non c'è un'immagine per «{map}».",
    'Bild konnte nicht geladen werden: {path} ({error})':
        "Impossibile caricare l'immagine: {path} ({error})",
    'Map gewählt: {map}':
        'Mappa scelta: {map}',
    'Noch keine Map gewählt.':
        'Ancora nessuna mappa scelta.',
    'Overlay eingeblendet.':
        'Overlay mostrato.',
    'Overlay ausgeblendet.':
        'Overlay nascosto.',
    '„{map}“ hat nur ein Layout.':
        '«{map}» ha un solo layout.',
    'Layout manuell gewechselt':
        'layout cambiato a mano',
    'Scanne den Bildschirm nach Map- oder Realm-Namen …':
        'Scansione dello schermo alla ricerca di nomi di mappe o Realm …',
    'Testanzeige':
        'visualizzazione di prova',
    'Test: Overlay 10 s lang an seiner normalen Position, mit Systemwerten, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – nochmal drücken beendet den Test.':
        "Prova: overlay per 10 s nella sua posizione normale, con valori di sistema, «Oggi» e musica (valori di esempio se non c'è nulla) – premi di nuovo per terminare la prova.",
    'Links':
        'Sinistra',
    'Mittig':
        'Centrato',
    'Rechts':
        'Destra',
    'Im Balken':
        'Nella barra',
    'Abstand':
        'Distanza',
    'Zeile CPU (Temperatur, Last)':
        'Riga CPU (temperatura, carico)',
    'Zeile GPU (Temperatur, Last)':
        'Riga GPU (temperatura, carico)',
    'Zeile Hotspot / GPU-Speicher (HWiNFO)':
        'Riga hot spot / memoria GPU (HWiNFO)',
    'Zeile VRAM':
        'Riga VRAM',
    'Zeile RAM':
        'Riga RAM',
    'Zeile in den Systemwerten an/aus. Die Warnungen „CPU/GPU DROSSELT“ erscheinen immer.':
        'Riga dei valori di sistema on/off. Gli avvisi «CPU/GPU THROTTLED» compaiono sempre.',
    'Zeile in den Systemwerten an/aus – Hotspot und Memory Junction kommen nur mit HWiNFO.':
        'Riga dei valori di sistema on/off – hot spot e memory junction arrivano solo con HWiNFO.',
    'Zeile in den Systemwerten an/aus.':
        'Riga dei valori di sistema on/off.',
    'Test beendet.':
        'Prova terminata.',
    'Diagnose in die Zwischenablage kopiert (auch als diagnose.txt gespeichert).':
        'Diagnostica copiata negli appunti (salvata anche come diagnose.txt).',
    'Alle Elemente mit der Maus ziehen (im Spiel oder in der Vorschau): Karte, Infos, Systemwerte, Heute, Eingaben, Musik. Rechtsklick auf ein Element = Menü (Ausblenden, Position zurücksetzen, Sperren), Strg+Mausrad = Grösse. Danach „Fertig“ oder Hotkey.':
        "Trascina ogni elemento col mouse (nel gioco o nell'anteprima): mappa, info, valori di sistema, oggi, input, musica. Clic destro su un elemento = menu (nascondi, ripristina posizione, blocca), Ctrl+rotellina = dimensione. Poi «Fatto» o l'hotkey.",
    '{name} wieder an seinem üblichen Platz.':
        '{name} di nuovo al suo posto abituale.',
    'Karte':
        'Mappa',
    'Systemwerte':
        'Valori di sistema',
    'Musik':
        'Musica',
    'Eingaben':
        'Input',
    'Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = Grösse, Rechtsklick = Menü':
        'Spostamento attivo – trascina (si aggancia, Alt = libero), frecce = di precisione, angolo/Ctrl+rotellina = dimensione, clic destro = menu',
    'Position zurücksetzen':
        'Ripristina posizione',
    'Rückgängig':
        'Annulla',
    'Karte darf grösser als der Balken werden':
        'La mappa può diventare più grande della barra',
    'Karte füllt den Balken aus':
        'La mappa riempie la barra',
    'Erlaubt jede Kartengrösse: Ist die Karte breiter als der schwarze Balken, bleibt sie an dessen Aussenrand und ragt ins Spielbild. Aus: Die Karte wird nie breiter als der Balken (auf 3440×1440 etwa 31 % der Bildhöhe).':
        "Consente qualsiasi dimensione della mappa: se la mappa è più larga della barra nera, resta sul bordo esterno della barra e sconfina nell'immagine di gioco. Off: la mappa non è mai più larga della barra (circa il 31 % dell'altezza su 3440×1440).",
    'Die Karte wird so gross, dass sie den schwarzen Balken von links bis rechts ausfüllt (bis auf den Abstand zum Rand); der Grössen-Regler gilt dann nicht. Eine hohe Karte stoppt an der Bildhöhe.':
        "La mappa cresce finché non riempie la barra nera da sinistra a destra (tranne la distanza dal bordo); in quel caso il cursore della dimensione non si applica. Una mappa alta si ferma all'altezza dell'immagine.",
    'Nimmt die letzte Änderung an Position oder Grösse zurück (Karte, Systemwerte, Musik) – auch mit Strg+Z auf dieser Seite. Ein ganzes Ziehen zählt als ein Schritt.':
        "Annulla l'ultima modifica di posizione o dimensione (mappa, valori di sistema, musica) – anche con Ctrl+Z in questa pagina. Un intero trascinamento conta come un passo.",
    'Merkt Position und Grösse aller Elemente getrennt für jede Grösse des DBD-Fensters (z. B. Vollbild 3440×1440 und ein kleineres Fenster) und lädt sie automatisch, sobald DBD in dieser Grösse läuft.':
        'Memorizza posizione e dimensione di ogni elemento separatamente per ogni dimensione della finestra di DBD (ad es. schermo intero 3440×1440 e una finestra più piccola) e le carica da solo appena DBD gira a quella dimensione.',
    'Nichts rückgängig zu machen.':
        'Niente da annullare.',
    'Position/Grösse rückgängig gemacht.':
        'Posizione/dimensione annullata.',
    'Position und Grösse je DBD-Fenstergrösse merken':
        'Memorizza posizione e dimensione per dimensione della finestra di DBD',
    'DBD-Fenster {size}: Layout für diese Grösse geladen.':
        'Finestra di DBD {size}: caricato il layout di questa dimensione.',
    'DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.':
        "Finestra di DBD {size}: nuova dimensione – d'ora in poi il layout viene memorizzato per essa.",
    'Aktuell: Layout für {size} · {n} Grössen gemerkt':
        'Ora: layout per {size} · {n} dimensioni memorizzate',
    'Position zurückgesetzt (automatisch).':
        'Posizione ripristinata (automatica).',
    'keine Map':
        'nessuna mappa',
    'ausgeblendet':
        'nascosto',
    'Menü offen':
        'menu aperto',
    'aktives Fenster ist {window}':
        'la finestra attiva è {window}',
    'DBD-Fenster {w}×{h}':
        'Finestra di DBD {w}×{h}',
    'Bildschirm':
        'schermo',
    'Overlay sichtbar bei {pos} über {src}.':
        'Overlay visibile in {pos} su {src}.',
    'Overlay pausiert: {reason}.':
        'Overlay in pausa: {reason}.',
    '{text} – Details in fogscout.log':
        '{text} – dettagli in fogscout.log',
    '{text} ({n}× seit {since}) – Details in fogscout.log':
        '{text} ({n}× dal {since}) – dettagli in fogscout.log',
    'Erkennung neu gestartet ({n}/{total})':
        'Rilevamento riavviato ({n}/{total})',
    'Map-Banner gefunden, lese …':
        'Banner della mappa trovato, lettura …',
    'automatisch erkannt ({p})':
        'rilevata automaticamente ({p})',
    'Layout {n} ({p})':
        'Layout {n} ({p})',
    'Rundentimer gestartet.':
        'Timer del round avviato.',
    'Rundentimer gestoppt: {time}.':
        'Timer del round fermato: {time}.',
    'Erkannt: {map} – gelesen „{name}“ / „{realm}“':
        'Rilevata: {map} – letto «{name}» / «{realm}»',
    'Layout unsicher – falls falsch: Layout-Knopf oder {keys}.':
        'Layout incerto – se sbagliato: pulsante layout o {keys}.',
    'Mitten in der Runde „{name}“ / „{realm}“ gelesen (am ehesten {map}) – ignoriert: Map-Banner gibt es nur am Rundenstart, und die Lesung war nicht eindeutig.':
        "Letto «{name}» / «{realm}» a metà round (più vicina: {map}) – ignorato: i banner delle mappe compaiono solo all'inizio di un round e la lettura non era chiara.",
    'Banner gesehen, aber keine bekannte Map: „{text}“. Map manuell wählen oder mit „Zuordnen …“ dauerhaft zuordnen.':
        'Banner visto, ma nessuna mappa nota: «{text}». Scegli la mappa a mano o assegnala in modo permanente con «Assegna …».',
    'Runde vorbei ({reason}) – Overlay ausgeblendet.':
        'Round finito ({reason}) – overlay nascosto.',
    'Runde vorbei ({reason}).':
        'Round finito ({reason}).',
    'Menü offen (Mauszeiger sichtbar) – Overlay pausiert.':
        'Menu aperto (puntatore del mouse visibile) – overlay in pausa.',
    'Zurück im Spiel – Overlay wieder sichtbar.':
        'Di nuovo in gioco – overlay di nuovo visibile.',
    'Die Erkennung ist abgestürzt – Details in fogscout.log':
        'Il rilevamento si è bloccato – dettagli in fogscout.log',
    'Die Erkennung ist abgestürzt:':
        'Il rilevamento si è bloccato:',
    'Die Erkennung ist abgestürzt – bitte Fog Scout neu starten.':
        'Il rilevamento si è bloccato – riavvia Fog Scout.',
    'Nichts gefunden':
        'Nessun risultato',
    'Runde gilt jetzt für {map} (vorher {old}).':
        'Il round ora conta per {map} (prima: {old}).',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen. Bis zum Neustart wird nichts gespeichert.':
        'Impossibile leggere settings.json ({error}) – caricati i valori predefiniti. Nulla viene salvato fino al riavvio.',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen, die alte Datei liegt als settings.json.broken daneben.':
        'Impossibile leggere settings.json ({error}) – caricati i valori predefiniti, il vecchio file è stato conservato come settings.json.broken.',
    'Scan fehlgeschlagen: {error}':
        'Scansione non riuscita: {error}',
    'per Scan gefunden: „{text}“':
        'trovata con la scansione: «{text}»',
    'Scan ({s} s): {map}':
        'Scansione ({s} s): {map}',
    'Realm „{realm}“ hat nur diese Map':
        'Il Realm «{realm}» ha solo questa mappa',
    'Scan: Realm „{realm}“ gefunden – bitte Map in der Liste wählen.':
        "Scansione: trovato il Realm «{realm}» – scegli la mappa nell'elenco.",
    'Scan ({s} s): kein Map- oder Realm-Name auf dem Bildschirm.':
        'Scansione ({s} s): nessun nome di mappa o Realm sullo schermo.',
    'Ergebnisbildschirm':
        'schermata dei risultati',
    'Lobby/Menü':
        'lobby/menu',
    'Ladebildschirm':
        'schermata di caricamento',
    'Clip wird geladen …':
        'Caricamento clip …',
    'Vorschaubild und Zeitleiste kommen aus der Aufnahme.':
        'Immagine di anteprima e timeline vengono lette dalla registrazione.',
    '{n} von {total} Bildern':
        '{n} di {total} immagini',
    'Lädt länger als erwartet – das Fenster ist trotzdem bedienbar.':
        'Ci vuole più del previsto – la finestra funziona comunque.',
    'DBD wurde geschlossen':
        'DBD è stato chiuso',
    'Menü/Lobby (Mauszeiger lange sichtbar)':
        'menu/lobby (puntatore del mouse visibile a lungo)',
    'keine Map angezeigt':
        'nessuna mappa mostrata',
    'Runde vorbei ({reason})':
        'round finito ({reason})',
    'wartet, bis du im Match bist (Map manuell gewählt)':
        'in attesa che tu sia in partita (mappa scelta a mano)',
    'Menü offen – Overlay pausiert':
        'menu aperto – overlay in pausa',
    'im Match':
        'in partita',
    'Ausblenden nach der Runde aus':
        'nascondi dopo il round disattivato',
    'Mauszeiger-Hinweis aus':
        'indizio del puntatore del mouse disattivato',
    'Mauszeiger-Hinweis ab dem nächsten Map-Banner':
        'indizio del puntatore del mouse dal prossimo banner della mappa',
    'Mauszeiger: –':
        'puntatore del mouse: –',
    'Mauszeiger sichtbar':
        'puntatore del mouse visibile',
    'Mauszeiger verborgen':
        'puntatore del mouse nascosto',
    'aus (Einstellung)':
        'off (impostazione)',
    'Runde vorbei – wartet auf die nächste Map':
        'round finito – in attesa della prossima mappa',
    'Automatische Erkennung ist aus':
        'Il rilevamento automatico è disattivato',
    'DBD ist minimiert':
        'DBD è ridotto a icona',
    'DBD gefunden ({w}×{h}) – warte auf Map-Banner':
        'DBD trovato ({w}×{h}) – in attesa del banner della mappa',
    'DBD nicht gefunden – Erkennung startet, sobald DBD läuft':
        'DBD non trovato – il rilevamento parte quando DBD è avviato',
    'Bildschirmaufnahme fehlgeschlagen: {error}':
        'Cattura schermo non riuscita: {error}',
    'Aufnahme ist schwarz – DBD im Modus „Fenster-Vollbild“ betreiben':
        'La cattura è nera – avvia DBD in modalità «Schermo intero in finestra»',
    'Fensteraufnahme nicht möglich, nutze Bildschirmaufnahme ({error})':
        'Cattura finestra non possibile, uso la cattura schermo ({error})',
    'DBD im Hintergrund – Fensteraufnahme aktiv: die Map wird auch erkannt, wenn andere Fenster darüber liegen.':
        'DBD in background – cattura finestra attiva: la mappa viene rilevata anche quando altre finestre la coprono.',
    'Rundenende-Erkennung für die gewählte Map ist jetzt aktiv.':
        'Il rilevamento di fine round per la mappa scelta è ora attivo.',
    'Mauszeiger war beim Map-Banner sichtbar – Menü-Erkennung per Mauszeiger ist für diese Runde aus.':
        'Il puntatore del mouse era visibile al banner della mappa – il rilevamento del menu tramite puntatore è disattivato per questo round.',
    'Map zuordnen':
        'Assegna mappa',
    'Gelesen: „{text}“':
        'Letto: «{text}»',
    'Welche Map war das? Der Name wird künftig automatisch erkannt.':
        "Che mappa era? D'ora in poi il nome verrà riconosciuto automaticamente.",
    'Bitte eine Map auswählen.':
        'Scegli una mappa.',
    'Abbrechen':
        'Annulla',
    '„{text}“ wird jetzt als {map} erkannt (eigene Zuordnung).':
        '«{text}» ora viene riconosciuto come {map} (assegnazione personale).',
    'zugeordnet: „{text}“':
        'assegnato: «{text}»',
    'Der gelesene Text ist zu kurz.':
        'Il testo letto è troppo corto.',
    'Unbekannte Map.':
        'Mappa sconosciuta.',
    '„{text}“ ist schon der Name von {map}.':
        '«{text}» è già il nome di {map}.',
    'Kartenbild hinzufügen':
        'Aggiungi immagine mappa',
    'eigenes Bild':
        'immagine personale',
    'Kartenbild gespeichert: {path}':
        'Immagine mappa salvata: {path}',
    'Eigenes Kartenbild für {map} gespeichert: {path}':
        'Immagine mappa personale per {map} salvata: {path}',
    'wird ab jetzt automatisch erkannt.':
        "d'ora in poi viene rilevata automaticamente.",
    'Eigenes Kartenbild für {map} gelöscht – das mitgelieferte gilt wieder.':
        'Immagine mappa personale per {map} eliminata – si usa di nuovo quella inclusa.',
    'Bitte den Namen der Map eingeben.':
        'Inserisci il nome della mappa.',
    '„{name}“ gibt es schon ({map}) – dann „Bild einer vorhandenen Map ersetzen“ wählen.':
        "«{name}» esiste già ({map}) – scegli invece «Sostituisci l'immagine di una mappa esistente».",
    'Noch kein Bild gewählt (PNG, JPG, WebP, GIF)':
        'Ancora nessuna immagine scelta (PNG, JPG, WebP, GIF)',
    'Für welche Map?':
        'Per quale mappa?',
    'Ergebnis':
        'Risultato',
    'Eigenes Bild löschen':
        'Elimina immagine personale',
    'Speichern':
        'Salva',
    'Bilder':
        'Immagini',
    'Kartenbild wählen':
        'Scegli immagine mappa',
    'Für diese Map lässt sich kein Bild speichern.':
        "Per questa mappa non è possibile salvare un'immagine.",
    'Erst ein Bild wählen.':
        "Scegli prima un'immagine.",
    'Das ist kein lesbares Bild: {error}':
        "Questa non è un'immagine leggibile: {error}",
    'Bild konnte nicht verarbeitet werden: {error}':
        "Impossibile elaborare l'immagine: {error}",
    'Speichern fehlgeschlagen: {error}':
        'Salvataggio non riuscito: {error}',
    'Eigenes Bild für „{map}“ löschen?':
        'Eliminare la tua immagine per «{map}»?',
    'Löschen fehlgeschlagen: {error}':
        'Eliminazione non riuscita: {error}',
    'Bild wählen …':
        'Scegli immagine …',
    'Bild einer vorhandenen Map ersetzen':
        "Sostituisci l'immagine di una mappa esistente",
    'Neue Map (fehlt im Programm)':
        'Nuova mappa (mancante nel programma)',
    'Name':
        'Nome',
    'Name so, wie er im Map-Banner steht – dann wird die Map automatisch erkannt.':
        'Nome come appare nel banner della mappa – così la mappa viene rilevata automaticamente.',
    'Hintergrund entfernen (Dunkelblau und Graulila der Community-Karten) und Rand abschneiden':
        'Rimuovi lo sfondo (blu scuro e viola grigio delle mappe della community) e taglia il bordo',
    'Ordner öffnen':
        'Apri cartella',
    'Animiertes GIF: wird unverändert übernommen.':
        'GIF animata: usata senza modifiche.',
    'Wird gestartet …':
        'Avvio …',
    'Version {version}':
        'Versione {version}',
    'Lade Maps …':
        'Caricamento mappe …',
    'Bereite Overlay vor …':
        "Preparazione dell'overlay …",
    'Baue Oberfläche …':
        "Creazione dell'interfaccia …",
    'Starte Erkennung …':
        'Avvio del rilevamento …',
    'Öffne Fenster …':
        'Apertura della finestra …',
    'Fog Scout ist bereit.':
        'Fog Scout è pronto.',
    'Automatische Erkennung':
        'Rilevamento automatico',
    'Aufnahmen mit OBS':
        'Registrazioni con OBS',
    'Lobby-Meldung':
        'Notifica lobby',
    'Spielserver anzeigen':
        'Mostra server di gioco',
    'Systemwerte im Spiel':
        'Valori di sistema in gioco',
    '„Heute“ im Spiel':
        '«Oggi» in gioco',
    'Musik im Spiel':
        'Musica in gioco',
    'Discord-Status':
        'Stato Discord',
    'Spotify „Als nächstes“':
        'Spotify «Prossimi brani»',
    'YouTube-Upload':
        'Caricamento su YouTube',
    '{name} eingeschaltet.':
        '{name} attivato.',
    '{name} ausgeschaltet.':
        '{name} disattivato.',
    'Erkennt die Map beim Match-Start am Banner und blendet die Karte ein. Aus: nur noch von Hand (Scannen, Map wählen). Dasselbe Häkchen steht unter Einstellungen → Erkennung.':
        "Legge la mappa dal banner all'inizio della partita e mostra la mappa. Off: solo a mano (scansione, scelta mappa). La stessa casella è in Impostazioni → Rilevamento.",
    'OBS nimmt jede Runde auf: Start beim Map-Banner, Stopp beim Rundenende. Aus: keine neue Aufnahme und keine F8-Clips – eine laufende Aufnahme endet normal mit der Runde. Alles Weitere unter Einstellungen → Aufnahmen.':
        'OBS registra ogni round: avvio al banner della mappa, stop alla fine del round. Off: nessuna nuova registrazione e nessuna clip F8 – una registrazione in corso termina col round come al solito. Tutto il resto in Impostazioni → Registrazioni.',
    'Ton und Hinweisfenster, sobald DBD eine Lobby gefunden hat. Die Erinnerung beim Countdown und „nur wenn DBD nicht vorne ist“ bleiben unter Einstellungen → Erkennung → Benachrichtigungen.':
        'Suono e finestra di notifica appena DBD ha trovato una lobby. Il promemoria del conto alla rovescia e «solo quando DBD non è in primo piano» restano in Impostazioni → Rilevamento → Notifiche.',
    'Zeigt Region und Ping des verbundenen Spielservers – auf der Seite Server, im Overlay und in der Statistik. Einschalten fragt Windows einmal nach Administratorrechten; gelesen werden nur Paketköpfe, nie Inhalte.':
        "Mostra regione e ping del server di gioco connesso – nella pagina Server, nell'overlay e nelle statistiche. All'attivazione Windows chiede una volta i diritti di amministratore; vengono lette solo le intestazioni dei pacchetti, mai i contenuti.",
    'Die Karte mit CPU-/GPU-Temperatur, Last und Speicher im schwarzen Balken. Einschalten bringt sie an die Position, an der sie zuletzt stand; Position und Zeilen unter Overlay → Systemwerte.':
        "La scheda con temperatura, carico e memoria di CPU/GPU nella barra nera. Attivandola torna dove si trovava l'ultima volta; posizione e righe in Overlay → Valori di sistema.",
    'Die Karte „Heute“ im Spiel: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit. Position unter Overlay → Heute.':
        'La scheda «Oggi» in gioco: round, tempo di gioco, Ø uccisioni/fughe, orologio. Posizione in Overlay → Oggi.',
    'Die Musikkarte „Läuft gerade“ im Spiel (Titel, Interpret, Cover aus der Windows-Mediensteuerung). Position und Aussehen unter Overlay → Musik.':
        'La scheda musicale «In riproduzione» in gioco (titolo, artista, copertina dai controlli multimediali di Windows). Posizione e aspetto in Overlay → Musica.',
    'Rich Presence: Map, Rolle und Rundenzeit in deinem Discord-Status. Application-ID und Einzelheiten unter Einstellungen → Verbindungen → Discord.':
        'Rich Presence: mappa, ruolo e durata del round nel tuo stato Discord. ID applicazione e dettagli in Impostazioni → Connessioni → Discord.',
    'Die Liste „Als nächstes“ aus Spotify in der Musikkarte. Client-ID und Anmeldung unter Einstellungen → Verbindungen → Spotify.':
        "L'elenco «Prossimi brani» di Spotify sulla scheda musicale. Client ID e accesso in Impostazioni → Connessioni → Spotify.",
    'Neue Clips (F8, Editor) gehen von selbst auf YouTube. Aus: nichts Neues wird eingereiht – was schon in der Warteschlange steht, lädt fertig; Runden lädst du weiter per Rechtsklick hoch. Einstellungen → Verbindungen → YouTube.':
        'Le nuove clip (F8, editor) vanno su YouTube da sole. Off: nulla di nuovo viene messo in coda – ciò che è già in coda viene completato; i round si caricano comunque col clic destro. Impostazioni → Connessioni → YouTube.',
    'Werkzeuge für die Fehlersuche ein- oder ausklappen: Live-Zustand der Rundenende-Erkennung, Debug-Bilder, Bildschirm scannen.':
        'Mostra o nascondi gli strumenti di risoluzione problemi: stato in tempo reale del rilevamento di fine round, immagini di debug, scansione dello schermo.',
    'Klicken und die neue Tastenkombination drücken: Strg/Alt + Taste, oder eine Taste allein (F1–F12, Numpad, Pause, Rollen, Einfg, Pos1, Ende, Bild↑/↓ – die gilt nur, solange DBD vorne ist). Esc bricht ab, Entf schaltet den Hotkey aus.':
        "Fai clic e premi la nuova combinazione di tasti: Ctrl/Alt + tasto, oppure un singolo tasto (F1–F12, tastierino numerico, Pause, Scroll Lock, Insert, Home, End, Page Up/Down – funziona solo mentre DBD è in primo piano). Esc annulla, Del disattiva l'hotkey.",
    'Bild↑':
        'PgUp',
    'Bild↓':
        'PgDn',
    'Einfg':
        'Insert',
    'Pos1':
        'Home',
    'Ende':
        'End',
    'Rollen':
        'Scroll Lock',
    'Gilt nur, solange DBD im Vordergrund ist – DBD selbst bekommt {keys} dann nicht mehr (in DBD nicht belegt?).':
        'Funziona solo mentre DBD è in primo piano – DBD stesso non riceve più {keys} (non assegnato in DBD?).',
    'Map-Namen in dieser Spielsprache erkennen. Nur die Sprachen anhaken, in denen du spielst – weniger Sprachen, weniger Verwechslungen.':
        'Riconosci i nomi delle mappe in questa lingua di gioco. Spunta solo le lingue in cui giochi – meno lingue, meno confusioni.',
    'Meldungen der Art „{category}“ im Log anzeigen.':
        'Mostra i messaggi «{category}» nel log.',
    'Karte ausblenden (die automatische Erkennung läuft weiter).':
        'Nascondi la mappa (il rilevamento automatico continua).',
    'Karte wieder einblenden.':
        'Mostra di nuovo la mappa.',
    'Die Erkennung war beim Layout nicht sicher – stimmt es nicht, hier weiterschalten.':
        'Il rilevamento non era sicuro del layout – se è sbagliato, cambia qui.',
    'Wechselt zum nächsten Layout dieser Map (z. B. Coal Tower ↔ Coal Tower II). Die Layouts ab II gibt es seit Patch 8.6.0 nur noch in Custom Games.':
        'Passa al layout successivo di questa mappa (ad es. Coal Tower ↔ Coal Tower II). Dalla patch 8.6.0 i layout dal II in poi esistono solo nelle partite personalizzate.',
    'Test sofort beenden.':
        'Termina ora la prova.',
    'Zeigt 10 s lang alles, was das Overlay im Match zeigt – Karte, Systemwerte, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – an den eingestellten Stellen, auch ohne DBD. Nochmal drücken beendet den Test.':
        "Mostra per 10 s tutto ciò che l'overlay mostra in partita – mappa, valori di sistema, «Oggi» e musica (valori di esempio se non c'è nulla) – nelle loro posizioni, anche senza DBD. Premi di nuovo per terminare la prova.",
    'Verschieben beenden.':
        'Smetti di spostare.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen – falls die automatische Erkennung das Banner verpasst hat.':
        'Cerca subito un nome di mappa o Realm su tutto lo schermo – nel caso il rilevamento automatico abbia perso il banner.',
    'Eigenes Kartenbild für diese unbekannte Map anlegen – Name und Realm sind schon eingetragen, der Hintergrund wird automatisch entfernt.':
        'Crea la tua immagine per questa mappa sconosciuta – nome e Realm sono già compilati, lo sfondo viene rimosso automaticamente.',
    'Der gelesene Name gehört zu einer vorhandenen Map (z. B. anders geschrieben)? Einmal zuordnen – danach wird er automatisch erkannt.':
        'Il nome letto appartiene a una mappa esistente (ad es. scritto diversamente)? Assegnalo una volta – poi verrà riconosciuto automaticamente.',
    'Hinweis ausblenden.':
        'Nascondi questo avviso.',
    'Eigenes Bild für eine Map wählen: vorhandenes Bild ersetzen oder neue Map anlegen. Rand und Hintergrund werden automatisch entfernt.':
        "Scegli un'immagine personale per una mappa: sostituisci un'immagine esistente o crea una nuova mappa. Bordo e sfondo vengono rimossi automaticamente.",
    'Position wieder auf „automatisch“ stellen (auf Ultrawide im linken schwarzen Rand).':
        'Riporta la posizione su «automatico» (su ultrawide nella barra nera sinistra).',
    'Auf breiten Monitoren bleibt die Karte im schwarzen Balken, in dem sie liegt, und wird bei Bedarf verkleinert. Mitten über dem Spiel platziert gilt keine Begrenzung. Ohne schwarze Balken neben dem Spielbild (16:9, z. B. 1920×1080) sind die Balken-Optionen ausgegraut.':
        "Sui monitor larghi la mappa resta dentro la barra nera in cui si trova e se serve viene rimpicciolita. Posizionata sopra il centro del gioco non c'è limite. Senza barre nere accanto all'immagine di gioco (16:9, ad es. 1920×1080) le opzioni della barra sono disattivate.",
    'Karte ausblenden, solange ein anderes Fenster (Browser, Discord …) im Vordergrund ist.':
        "Nascondi la mappa mentre un'altra finestra (browser, Discord …) è in primo piano.",
    'Zusätzliche Namenszeile über der Karte – die meisten Kartenbilder tragen den Namen schon selbst.':
        'Riga extra con il nome sopra la mappa – la maggior parte delle immagini mappa mostra già il nome.',
    'Zeit seit dem Einblenden der Karte, gross unter der Karte.':
        'Tempo trascorso da quando è comparsa la mappa, grande sotto la mappa.',
    'Region und Ping des Spielservers unter der Karte. Braucht „Verbundener Spielserver“ im Tab Server.':
        'Regione e ping del server di gioco sotto la mappa. Richiede «Server di gioco connesso» nella scheda Server.',
    'Aus: Karte liegt auf einem dunklen Rechteck – besser lesbar über hellen Spielszenen.':
        'Off: la mappa poggia su un rettangolo scuro – più leggibile sopra scene di gioco chiare.',
    'Liest das Map-Banner am Match-Anfang und blendet die passende Karte ein. Aus: Map nur von Hand wählen.':
        "Legge il banner della mappa all'inizio di una partita e mostra la mappa corrispondente. Off: scegli la mappa solo a mano.",
    'Blendet die Karte nach der Runde aus (Ergebnisbildschirm, Lobby, Ladebildschirm, DBD beendet).':
        'Nasconde la mappa dopo il round (schermata dei risultati, lobby, schermata di caricamento, DBD chiuso).',
    'Karte verschwindet, solange der Mauszeiger im Spiel sichtbar ist (ESC-Menü), und kommt danach wieder.':
        'La mappa scompare mentre il puntatore del mouse è visibile nel gioco (menu ESC) e poi ritorna.',
    'Fensteraufnahme wie bei OBS: erkennt das Banner auch, wenn DBD verdeckt ist. Nur solange DBD im Hintergrund ist.':
        'Cattura finestra come OBS: rileva il banner anche quando DBD è coperto. Solo mentre DBD è in background.',
    'Speichert gelesene Banner und verkleinerte Bilder der Runde im Ordner debug/ – nur zur Fehlersuche, kostet Speicherplatz.':
        'Salva i banner letti e piccole immagini del round nella cartella debug/ – solo per la risoluzione problemi, occupa spazio su disco.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen.':
        'Cerca subito un nome di mappa o Realm su tutto lo schermo.',
    'Kopiert technische Infos (Fenster, Overlay, letzte Rundenende-Prüfungen) in die Zwischenablage – zum Weitergeben bei Problemen.':
        'Copia informazioni tecniche (finestra, overlay, ultimi controlli di fine round) negli appunti – da inoltrare quando qualcosa non va.',
    'Misst den Ping zu allen AWS-Regionen (UDP-Beacon von Amazon GameLift).':
        'Misura il ping verso tutte le regioni AWS (beacon UDP di Amazon GameLift).',
    'Nur die angehakten Regionen erlauben – trägt die übrigen in die Windows-hosts-Datei ein (fragt nach Administratorrechten).':
        'Consenti solo le regioni spuntate – aggiunge le altre al file hosts di Windows (chiede i diritti di amministratore).',
    'Entfernt die Einträge des Programms aus der hosts-Datei – alle Regionen wieder erlaubt.':
        'Rimuove le voci del programma dal file hosts – di nuovo tutte le regioni consentite.',
    'Log-Anzeige leeren (die Log-Datei bleibt).':
        'Svuota la vista del log (il file di log resta).',
    'Öffnet fogscout.log mit allen Details.':
        'Apre fogscout.log con tutti i dettagli.',
    'Dunkle oder helle Darstellung des Steuerfensters.':
        'Aspetto scuro o chiaro della finestra di controllo.',
    'Alle Hotkeys auf die Voreinstellung zurücksetzen.':
        'Ripristina tutti gli hotkey ai valori predefiniti.',
    'Minimieren versteckt das Fenster im Infobereich; Doppelklick auf das Symbol holt es zurück.':
        "Riducendo a icona la finestra va nell'area di notifica; doppio clic sull'icona per riportarla.",
    'Startet das Programm bei der Anmeldung im Infobereich. Nur als Administrator änderbar.':
        "Avvia il programma nell'area di notifica quando accedi. Modificabile solo come amministratore.",
    'Holt beim Start über die Verknüpfung den neuen Stand von GitHub. Eigene Änderungen werden nie überschrieben.':
        'Scarica la versione più recente da GitHub quando viene avviato tramite il collegamento. Le tue modifiche non vengono mai sovrascritte.',
    'Alle eigenen Map-Zuordnungen löschen (die Namen werden dann wieder als unbekannt gemeldet).':
        'Elimina tutte le assegnazioni mappa personali (i nomi vengono di nuovo segnalati come sconosciuti).',
    'Öffnet den Ordner mit den mitgelieferten Kartenbildern.':
        'Apre la cartella con le immagini mappa incluse.',
    'PNG, JPG, WebP oder GIF auswählen – zum Beispiel ein Original mit Hintergrund.':
        'Scegli un PNG, JPG, WebP o GIF – ad esempio un originale con sfondo.',
    'Dein Bild ersetzt das mitgelieferte Bild dieser Map (bzw. dieses Layouts). Löschen stellt das Original wieder her.':
        "La tua immagine sostituisce quella inclusa di questa mappa (o di questo layout). Eliminandola torna l'originale.",
    'Legt eine neue Map an. Sie wird erkannt, wenn der Name so geschrieben ist wie im Map-Banner.':
        'Crea una nuova mappa. Viene rilevata se il nome è scritto come nel banner della mappa.',
    'Öffnet den Ordner user_maps mit deinen eigenen Kartenbildern.':
        'Apre la cartella user_maps con le tue immagini mappa.',
    'Löscht dein Bild für die gewählte Map – danach gilt wieder das mitgelieferte.':
        'Elimina la tua immagine per la mappa scelta – si usa di nuovo quella inclusa.',
    'Bild umwandeln und speichern; die Karte wird sofort angezeigt.':
        "Converti e salva l'immagine; la mappa viene mostrata subito.",
    'Schliessen, ohne etwas zu ändern.':
        'Chiudi senza modificare nulla.',
    'Macht Dunkelblau (#282a42) und Graulila (#535781) der Community-Karten transparent, schneidet den gleichfarbigen Rand ab und bringt das Bild auf 1280 px Höhe.':
        "Rende trasparenti il blu scuro (#282a42) e il viola grigio (#535781) delle mappe della community, taglia il bordo dello stesso colore e porta l'immagine a 1280 px di altezza.",
    '? unsicher – {keys} = falsch':
        '? incerto – {keys} = sbagliata',
    'Falsch erkannt':
        'Mappa sbagliata',
    'Stimmt':
        'Corretta',
    'Unsicher erkannt: {map} (gelesen „{name}“)':
        'Rilevamento incerto: {map} (letto «{name}»)',
    'Unsicher erkannt: {map} – gelesen „{name}“, Passung {fit}. Falls falsch: {keys} oder „Falsch erkannt“.':
        'Rilevamento incerto: {map} – letto «{name}», corrispondenza {fit}. Se sbagliata: {keys} o «Mappa sbagliata».',
    '{map} bestätigt.':
        '{map} confermata.',
    'Nichts zu verwerfen: keine automatisch erkannte Map eingeblendet.':
        'Niente da scartare: nessuna mappa rilevata automaticamente è mostrata.',
    'Verworfen: {map} – die Runde wird nicht gezählt.':
        'Scartata: {map} – il round non viene contato.',
    'Die erkannte Map stimmt nicht: Karte ausblenden, Timer zurücksetzen, die Runde wird nicht gezählt. Geht auch im Spiel mit dem Hotkey (Standard Strg+Alt+X).':
        "La mappa rilevata è sbagliata: nasconde la mappa, azzera il timer, il round non viene contato. Funziona anche in gioco con l'hotkey (predefinito Ctrl+Alt+X).",
    'Die Map stimmt – Hinweis „unsicher“ ausblenden.':
        "La mappa è giusta – nascondi l'avviso «incerto».",
    'als falsch verworfen':
        'scartata come sbagliata',
    'Ping {ms} ms':
        'ping {ms} ms',
    'Ø Kills':
        'Ø uccisioni',
    '4K':
        '4K',
    'Entkommen':
        'Fuggiti',
    'entkommen':
        'fuggito',
    'tot':
        'morto',
    'aufgegeben':
        'abbandonato',
    'verlassen':
        'uscito',
    'Stats-Seite öffnen, wenn DBD beendet wird':
        'Apri la pagina statistiche quando DBD viene chiuso',
    'Userscript kopieren':
        'Copia userscript',
    'Stats-Seite öffnen':
        'Apri pagina statistiche',
    '⚠ Unbekannter Status auf der Stats-Seite: {list} – zählt nicht. Bitte melden („Diagnose kopieren“).':
        '⚠ Stato sconosciuto nella pagina statistiche: {list} – non contato. Segnalalo («Copia diagnostica»).',
    '⚠ Lücke: zwischen {start} und {end} fehlen vielleicht Matches – die Seite zeigt nur die letzten 30. Seite öfter öffnen.':
        '⚠ Lacuna: potrebbero mancare partite tra {start} e {end} – la pagina mostra solo le ultime 30. Apri la pagina più spesso.',
    '⚠ {n}× andere Map als erkannt, zuletzt {when}: erkannt {ours}, laut Seite {theirs}.':
        "⚠ {n}× una mappa diversa da quella rilevata, l'ultima {when}: rilevata {ours}, la pagina dice {theirs}.",
    '⚠ Das Userscript ist veraltet (Version {old}, aktuell {new}) – „Userscript kopieren“ und in Tampermonkey ersetzen.':
        "⚠ L'userscript è obsoleto (versione {old}, attuale {new}) – «Copia userscript» e sostituiscilo in Tampermonkey.",
    'Stats-Seite konnte nicht geöffnet werden: {error}':
        'Impossibile aprire la pagina statistiche: {error}',
    'DBD beendet – Stats-Seite geöffnet; das Userscript speichert die Matches.':
        "DBD chiuso – pagina statistiche aperta; l'userscript salva le partite.",
    'Userscript nicht gefunden: {error}':
        'Userscript non trovato: {error}',
    'Userscript in die Zwischenablage kopiert. In Tampermonkey: „Neues Skript erstellen“ → alles ersetzen (Strg+A, Strg+V) → Speichern. Danach stats.deadbydaylight.com öffnen und anmelden.':
        'Userscript copiato negli appunti. In Tampermonkey: «Crea un nuovo script» → sostituisci tutto (Ctrl+A, Ctrl+V) → Salva. Poi apri stats.deadbydaylight.com e accedi.',
    'Offizielle Match-Daten: {n} Matches gelesen, {new} neu – Datei gelöscht.':
        'Dati partita ufficiali: {n} partite lette, {new} nuove – file eliminato.',
    'Offizielle Match-Daten: zwischen {start} und {end} fehlen vielleicht Matches (die Seite zeigt nur die letzten 30).':
        'Dati partita ufficiali: potrebbero mancare partite tra {start} e {end} (la pagina mostra solo le ultime 30).',
    '{name} gelesen, aber nicht gelöscht: {error}':
        '{name} letto, ma non eliminato: {error}',
    '{name} ist keine Match-Datei von Fog Scout – bleibt liegen.':
        "{name} non è un file partite di Fog Scout – lasciato com'è.",
    'Unbekannter Status auf der Stats-Seite: „{status}“ – zählt nicht für Kills/Escapes. Bitte melden.':
        'Stato sconosciuto nella pagina statistiche: «{status}» – non contato per uccisioni/fughe. Segnalalo.',
    'Schliesst du DBD nach mindestens einer Runde, öffnet das Programm stats.deadbydaylight.com im Browser. Das Userscript speichert dann die letzten 30 Matches, das Programm liest sie ein und löscht die Datei. Nie während DBD läuft.':
        "Quando chiudi DBD dopo almeno un round, il programma apre stats.deadbydaylight.com nel browser. L'userscript salva allora le ultime 30 partite; il programma le legge ed elimina il file. Mai mentre DBD è in esecuzione.",
    'Kopiert das Userscript in die Zwischenablage. In Tampermonkey „Neues Skript erstellen“, alles ersetzen und speichern. Es liest nur die Match-Liste, die die Seite selbst lädt – keine Konto- oder Login-Daten – und schickt nichts irgendwohin.':
        "Copia l'userscript negli appunti. In Tampermonkey «Crea un nuovo script», sostituisci tutto e salva. Legge solo l'elenco delle partite che la pagina carica da sé – nessun dato di account o di accesso – e non invia nulla da nessuna parte.",
    'Öffnet stats.deadbydaylight.com jetzt. Mit installiertem Userscript kommen die Matches gleich danach an.':
        "Apre ora stats.deadbydaylight.com. Con l'userscript installato le partite arrivano subito dopo.",
    'Vom Programm erkannt: {seen} von {n} ({share})':
        'Rilevati dal programma: {seen} di {n} ({share})',
    'Nicht erkannt (oder das Programm lief nicht): {list}':
        'Non rilevati (o il programma non era in esecuzione): {list}',
    'Rundenende erkannt: Median {off} gegenüber dem Ende laut Seite ({n} Runden; + = später)':
        'Fine round rilevata: mediana {off} rispetto alla fine sulla pagina ({n} round; + = più tardi)',
    '{n} Mio.':
        '{n}M',
    'Ø BP':
        'Ø BP',
    '✓ {n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '✓ {n} × fine round non rilevata, ma contata con la durata dalla pagina statistiche.',
    'Runden vom Map-Banner bis zum Rundenende (ab 1 min), nur lokal gespeichert. Kills, Escapes und Bloodpoints laut stats.deadbydaylight.com, sobald eine Runde dort zugeordnet ist.':
        'Round dal banner della mappa alla fine del round (da 1 min), salvati solo in locale. Uccisioni, fughe e Punti Sangue da stats.deadbydaylight.com appena un round è collegato a una partita lì.',
    '{n}× Abandon':
        '{n}× abbandoni',
    'Ein Skin oder neuer Killer steht unter seinem eigenen Namen? Zeile markieren, Killer wählen, „Zuordnen“ – gilt auch rückwirkend.':
        'Un outfit o un nuovo Killer compare con un nome proprio? Seleziona la riga, scegli il Killer, «Assegna» – vale anche per i round passati.',
    'Abgleich mit der Stats-Seite':
        'Confronta con la pagina statistiche',
    'Noch keine offiziellen Daten.':
        'Ancora nessun dato ufficiale.',
    'Neu seit {version}':
        'Novità dalla {version}',
    'sofort':
        'immediato',
    'HWiNFO läuft nicht: CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen.':
        'HWiNFO non è in esecuzione: mancano temperatura CPU, potenza CPU, core e FPS.',
    'Systemwerte: HWiNFO läuft nicht – CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen in dieser Runde.':
        'Valori di sistema: HWiNFO non è in esecuzione – in questo round mancano temperatura CPU, potenza CPU, core e FPS.',
    'Vorwoche {value}':
        'settimana scorsa {value}',
    '{n} Pkt.':
        '{n} pt',
    'Montag bis jetzt gegenüber der Vorwoche (Mo–So); Custom und Farming zählen nicht.':
        'Da lunedì a ora rispetto alla settimana precedente (lun–dom); partite personalizzate e farming non contano.',
    'Sicherung: {files} nach {folder}/ kopiert (die letzten {n} Stände bleiben).':
        'Backup: {files} copiati in {folder}/ (vengono conservate le ultime {n} copie).',
    '{n} Dateien, zuletzt {day}':
        '{n} file, ultimo {day}',
    '1 Datei, zuletzt {day}':
        '1 file, ultimo {day}',
    'behalten (nie aufgeräumt)':
        'conservata (mai ripulita)',
    'wartet auf den YouTube-Upload':
        'in attesa del caricamento su YouTube',
    'auf YouTube':
        'su YouTube',
    'Karte im Spiel':
        'Mappa nel gioco',
    'OBS läuft nicht, oder sein WebSocket-Server ist aus':
        'OBS non è in esecuzione o il suo server WebSocket è disattivato',
    'OBS antwortet nicht':
        'OBS non risponde',
    'OBS hat die Verbindung getrennt':
        'OBS ha chiuso la connessione',
    'noch keine':
        'ancora nessuno',
    'Tägliche Kopie von rounds.jsonl und official.jsonl nach {folder}/ (nur bei Änderungen, die letzten {n} Stände je Datei; vor „Alle Runden löschen“ eine zusätzliche): {state}':
        'Copia giornaliera di rounds.jsonl e official.jsonl in {folder}/ (solo se ci sono modifiche, le ultime {n} copie per file; una in più prima di «Elimina tutti i round»): {state}',
    'Verstanden':
        'Ho capito',
    'Aus HISTORY.md (Deutsch), die neuesten zuerst.':
        'Da HISTORY.md (in tedesco), i più recenti per primi.',
    'Blendet die Karte „Neu seit …“ aus, bis die nächste neue Version kommt.':
        'Nasconde la scheda «Novità dalla …» fino alla prossima nuova versione.',
    'Offizielle Match-Daten':
        'Dati partita ufficiali',
    'Einmal einrichten: Tampermonkey im Browser installieren, „Userscript kopieren“ und dort als neues Skript einfügen und speichern, auf stats.deadbydaylight.com anmelden. Chrome/Edge: in den Details der Erweiterung „Allow User Scripts“ einschalten, sonst läuft kein Skript. Beim Öffnen der Seite speichert das Skript neue Matches (die letzten 30) im Download-Ordner; das Programm liest die Datei und löscht sie. Es geht dafür selbst nicht ins Internet.':
        "Configurazione una tantum: installa Tampermonkey nel browser, «Copia userscript», incollalo lì come nuovo script e salvalo, accedi su stats.deadbydaylight.com. Chrome/Edge: attiva «Consenti script utente» nei dettagli dell'estensione, altrimenti nessuno script viene eseguito. Quando la pagina si apre, lo script salva le nuove partite (le ultime 30) nella cartella dei download; il programma legge il file e lo elimina. Per questo non va online da sé.",
    'Alle Matches neu speichern':
        'Salva di nuovo tutte le partite',
    'Öffnet die Stats-Seite so, dass das Userscript ihre letzten 30 Matches noch einmal speichert, auch wenn keines neu ist – nach einer Neuinstallation oder wenn die Datei verloren ging.':
        "Apre la pagina statistiche in modo che l'userscript salvi ancora una volta le sue ultime 30 partite anche se nessuna è nuova – dopo una nuova installazione o se il file è andato perso.",
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) speichert ihre letzten 30 Matches noch einmal, auch wenn keines neu ist; das Programm übernimmt sie gleich – bekannte zählen nur einmal. Kommt keine Datei: in der Console des Browsers (F12) steht, ob das Skript läuft. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        "La pagina statistiche si apre nel browser. L'userscript (versione {n} o più recente) salva ancora una volta le sue ultime 30 partite anche se nessuna è nuova; il programma le prende subito – quelle già note contano una volta sola. Se non arriva nessun file: la console del browser (F12) dice se lo script è in esecuzione. Userscript più vecchi: prima «Copia userscript» e sostituiscilo in Tampermonkey.",
    'Verlauf':
        'Andamento',
    'Nur Runden, die einem Match auf der Stats-Seite zugeordnet sind. Die Maus über einer Säule zeigt Wert und Anzahl der Runden.':
        'Solo round collegati a una partita sulla pagina statistiche. Passa il mouse su una colonna per il suo valore e il numero di round.',
    'Killer – Ø Kills {per}':
        'Killer – Ø uccisioni {per}',
    'Survivor – entkommen {per}':
        'Sopravvissuto – fughe {per}',
    'pro Stunde':
        "all'ora",
    'pro Tag':
        'al giorno',
    'pro Woche':
        'a settimana',
    'KW {n}':
        'S{n}',
    '{when}: Ø {kills} Kills · {n} Runden':
        '{when}: Ø {kills} uccisioni · {n} round',
    '{when}: {share} entkommen · {n} Runden':
        '{when}: {share} fughe · {n} round',
    'Keine Killer-Runden mit offiziellen Daten in dieser Auswahl.':
        'Nessun round da Killer con dati ufficiali in questa selezione.',
    'Keine Survivor-Runden mit offiziellen Daten in dieser Auswahl.':
        'Nessun round da Sopravvissuto con dati ufficiali in questa selezione.',
    'Ø {kills} Kills':
        'Ø {kills} uccisioni',
    '{share} entkommen':
        '{share} fughe',
    'Meldung, wenn Match-Daten eingelesen und gelöscht wurden':
        'Avvisa quando i dati partita sono stati letti ed eliminati',
    'Zeigt unten rechts kurz, wie viele Matches gelesen wurden und dass die Datei gelöscht ist – nicht, solange DBD im Vordergrund ist. Im Log steht es immer.':
        'Mostra brevemente in basso a destra quante partite sono state lette e che il file è stato eliminato – non mentre DBD è in primo piano. Il log lo riporta sempre.',
    '{n} Matches gelesen, davon {new} neu. Die Datei wurde gelöscht.':
        '{n} partite lette, di cui {new} nuove. Il file è stato eliminato.',
    '{name} wurde gelesen, konnte aber nicht gelöscht werden – Details im Log.':
        '{name} è stato letto ma non è stato possibile eliminarlo – dettagli nel log.',
    'Links oben (über der Karte)':
        'In alto a sinistra (sopra la mappa)',
    'Rechts oben':
        'In alto a destra',
    'GPU: {name}':
        'GPU: {name}',
    'GPU: keine NVIDIA-Karte gefunden':
        'GPU: nessuna scheda NVIDIA trovata',
    'CPU-Temperatur: aus HWiNFO':
        'Temperatura CPU: da HWiNFO',
    'Systemwerte (CPU/GPU-Temperatur, Auslastung, VRAM, RAM)':
        'Valori di sistema (temperatura CPU/GPU, carico, VRAM, RAM)',
    'nach Map':
        'per mappa',
    'nach Killer':
        'per Killer',
    'GPU Ø °C':
        'GPU Ø °C',
    'GPU max':
        'GPU max',
    'CPU Ø °C':
        'CPU Ø °C',
    'CPU max':
        'CPU max',
    'GPU Ø Last':
        'GPU Ø carico',
    'Ø Watt':
        'Ø watt',
    'Noch keine Systemwerte in dieser Auswahl (Tab Overlay → Systemwerte einschalten).':
        'Ancora nessun valore di sistema in questa selezione (scheda Overlay → attiva i valori di sistema).',
    'GPU DROSSELT (TEMP.)':
        'GPU THROTTLED (TEMP.)',
    'GPU DROSSELT (HW)':
        'GPU THROTTLED (HW)',
    'Hotspot max {v} °C':
        'hot spot max {v} °C',
    'Hotspot max':
        'Hot spot max',
    'GPU-Temperatur – Ø {per}':
        'Temperatura GPU – media {per}',
    'Noch keine GPU-Temperaturen in dieser Auswahl.':
        'Ancora nessuna temperatura GPU in questa selezione.',
    '{when}: Ø {avg} °C · max {max} °C · {n} Runden':
        '{when}: Ø {avg} °C · max {max} °C · {n} round',
    'Werte der Systemwerte-Anzeige (Tab Overlay) während der Runden – nur Runden, in denen sie eingeschaltet war. CPU-Temperatur nur mit HWiNFO. „Wann/Wo“ zeigt, auf welchen Maps oder zu welcher Tageszeit der PC am heißesten läuft. „Gedrosselt“: Sekunden, in denen die GPU wegen Temperatur oder Hardware langsamer lief (nur NVIDIA). „–“: in diesen Runden nicht erfasst – CPU-Temperatur, -Leistung, Kerne und FPS gibt es nur, solange HWiNFO läuft, und jeder Wert braucht mindestens 10 Sekunden Messwerte in der Runde.':
        'Valori della visualizzazione valori di sistema (scheda Overlay) durante i round – solo i round in cui era attiva. Temperatura CPU solo con HWiNFO. «Quando/dove» mostra su quali mappe o a che ora del giorno il PC scalda di più. «Throttled»: secondi in cui la GPU è andata più lenta per temperatura o hardware (solo NVIDIA). «–»: non registrato in quei round – temperatura CPU, potenza, core e FPS esistono solo mentre HWiNFO è in esecuzione, e ogni valore richiede almeno 10 secondi di letture nel round.',
    'Eigene Position (mit der Maus verschieben)':
        'Posizione personalizzata (trascina col mouse)',
    'SYSTEMWERTE':
        'VALORI DI SISTEMA',
    'Direkt über der Karte (wandert mit)':
        'Subito sopra la mappa (si sposta con essa)',
    'Schriftgrösse':
        'Dimensione carattere',
    'Übersicht':
        'Panoramica',
    'Aktuelle Map':
        'Mappa attuale',
    'Rundenzeit':
        'Durata round',
    'Ping':
        'Ping',
    'läuft':
        'in corso',
    'letzte Runde':
        'ultimo round',
    'startet':
        'avvio',
    '4K: {n} von {total}':
        '4K: {n} di {total}',
    '{n} Survivor-Runden':
        '{n} round da Sopravvissuto',
    '{n} normal':
        '{n} normali',
    '{n} Farming-Runden · Ø {bp} BP':
        '{n} round di farming · Ø {bp} BP',
    'Spielzeit heute: {time}':
        'Giocato oggi: {time}',
    'Systemwerte sind aus (Tab Overlay → Systemwerte).':
        'I valori di sistema sono disattivati (scheda Overlay → Valori di sistema).',
    'Systemwerte gibt es nur unter Windows.':
        'I valori di sistema sono disponibili solo su Windows.',
    'Erscheinen, sobald DBD läuft.':
        'Compaiono appena DBD è in esecuzione.',
    'OK':
        'OK',
    '4 Kills · leer = weniger als {n} Runden':
        '4 uccisioni · vuoto = meno di {n} round',
    'Killer × Map – Ø Kills laut Stats-Seite':
        'Killer × mappa – Ø uccisioni dalla pagina statistiche',
    'Maps – am häufigsten gespielt':
        'Mappe – le più giocate',
    'Median {time}':
        'mediana {time}',
    'Noch keine Killer-Runde mit Ergebnis von der Stats-Seite.':
        'Ancora nessun round da Killer con un risultato dalla pagina statistiche.',
    'keine Killer-Runden mit Stats-Daten':
        'nessun round da Killer con dati statistici',
    'keine Survivor-Runden mit Stats-Daten':
        'nessun round da Sopravvissuto con dati statistici',
    '{map} · {killer}: Ø {kills} Kills ({n} Runden)':
        '{map} · {killer}: Ø {kills} uccisioni ({n} round)',
    '{n} Matches':
        '{n} partite',
    '{time} gespielt':
        '{time} giocati',
    'Ø Bloodpoints':
        'Ø Punti Sangue',
    'Ø Rundendauer':
        'Ø durata round',
    'Anzeigen':
        'Mostra',
    'Kartenbild nicht lesbar: {error}':
        'Immagine mappa non leggibile: {error}',
    'Keine Map gewählt':
        'Nessuna mappa selezionata',
    'Blendet die gewählte Map jetzt als Overlay ein – die Erkennung übernimmt beim nächsten Match wieder.':
        "Mostra ora la mappa selezionata nell'overlay – alla prossima partita il rilevamento riprende il controllo.",
    'Ziehen, um den Kasten zu verschieben':
        'Trascina per spostare questo riquadro',
    'Anordnung zurücksetzen':
        'Ripristina disposizione',
    'Die Kästen der Seiten lassen sich am Griff rechts im Titel verschieben.':
        'I riquadri delle pagine si possono spostare con la maniglia a destra del titolo.',
    'Stellt die Kästen auf allen Seiten, die Reiter-Reihen (Statistik, Overlay) und die Navigation links wieder in die ursprüngliche Reihenfolge.':
        "Riporta nell'ordine originale i riquadri di tutte le pagine, le righe di schede (Statistiche, Overlay) e la navigazione a sinistra.",
    'Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der du Dead by Daylight spielst (mehrere gehen).':
        "Il programma legge il nome della mappa dall'immagine all'inizio di una partita. Spunta la lingua in cui giochi a Dead by Daylight (anche più di una).",
    'Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.':
        "La mappa compare da sola all'inizio di una partita e sparisce dopo il round. «automatico» la mette nel bordo nero accanto all'immagine di gioco (ultrawide) o accanto alla finestra di DBD.",
    'Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle Tasten findest du später unter Einstellungen.':
        'I tasti più importanti – fai clic su uno per cambiarlo, poi premi la nuova combinazione. Tutti i tasti sono poi in Impostazioni.',
    'Einrichtung starten':
        'Avvia configurazione',
    'Öffnet noch einmal die Einrichtung vom ersten Start: Spielsprache, Overlay-Position und die wichtigsten Tasten.':
        "Riapre la configurazione del primo avvio: lingua di gioco, posizione dell'overlay e i tasti più importanti.",
    'Suchen (Strg+F)':
        'Cerca (Ctrl+F)',
    'Strg+F':
        'Ctrl+F',
    'Suchen: Einstellung, Seite, Map, Aktion, Runde …':
        'Cerca: impostazione, pagina, mappa, azione, round …',
    'Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst':
        'Frecce scelgono · Enter apre · Ctrl+Enter nel gioco o nella registrazione · Esc chiude',
    'Aktionen':
        'Azioni',
    'Seiten':
        'Pagine',
    'Vorschlag von Claude':
        'Suggerito da Claude',
    'Enter':
        'Enter',
    'Strg+Enter':
        'Ctrl+Enter',
    'Claude fragen: „{q}“':
        'Chiedi a Claude: «{q}»',
    'Schickt nur die Frage und die Namen der Einstellungen an Claude':
        'Invia a Claude solo la domanda e i nomi delle impostazioni',
    'Claude denkt nach …':
        'Claude sta pensando …',
    'Claude hat nichts Passendes gefunden.':
        'Claude non ha trovato nulla di adatto.',
    'Claude hat die Frage abgelehnt.':
        'Claude ha rifiutato la domanda.',
    'Claude hat unverständlich geantwortet.':
        'Claude ha dato una risposta illeggibile.',
    'Claude ist nicht erreichbar – keine Internetverbindung?':
        'Claude non è raggiungibile – nessuna connessione internet?',
    'Claude: Zu viele Anfragen – gleich noch einmal versuchen.':
        'Claude: troppe richieste – riprova tra un momento.',
    'Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen.':
        'Nessuna chiave API – inseriscila in Impostazioni → Connessioni → Claude.',
    'Zeigt im grossen Clip-Editor den Abschnitt „Mit Claude bearbeiten“: Du schreibst, was mit dem Schnitt passieren soll, Claude schlägt Schritte vor, du übernimmst oder verwirfst sie. Gesendet werden nur deine Bitte und der Schnitt als Zahlen – kein Bild, kein Dateiname. Braucht einen eigenen API-Key.':
        'Mostra la sezione «Modifica con Claude» nel grande editor di clip: scrivi cosa deve succedere al montaggio, Claude suggerisce i passi, tu li applichi o li scarti. Vengono inviati solo la tua richiesta e il montaggio come numeri – nessuna immagine, nessun nome di file. Richiede una tua chiave API.',
    'Claude':
        'Claude',
    'Im Clip-Editor Claude nutzen':
        "Usa Claude nell'editor di clip",
    'Mit Claude bearbeiten':
        'Modifica con Claude',
    'z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short':
        'ad es. togli i primi 10 s, velocità doppia da 0:40, come short',
    'Vorschlagen':
        'Suggerisci',
    'Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst.':
        'Invia a Claude la tua richiesta e il montaggio come numeri (tempi, velocità, dissolvenze – nessuna immagine, nessun nome di file); nulla cambia finché non lo applichi.',
    'Übernehmen':
        'Applica',
    'Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z).':
        'Esegue i passi suggeriti – un solo passo da annullare (Ctrl+Z).',
    'Verwerfen':
        'Scarta',
    'Vergisst den Vorschlag; der Schnitt bleibt, wie er ist.':
        "Dimentica il suggerimento; il montaggio resta com'è.",
    'Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude nutzen“ einschalten und einen API-Key eintragen.':
        "Off – attiva «Usa Claude nell'editor di clip» in Impostazioni → Connessioni → Claude e inserisci una chiave API.",
    'Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen.':
        'Nel frattempo il montaggio è cambiato – chiedi di nuovo un suggerimento.',
    'Claude hat keinen passenden Schritt gefunden.':
        'Claude non ha trovato alcun passo adatto.',
    'Übernommen – Strg+Z macht es rückgängig.':
        'Applicato – Ctrl+Z lo annulla.',
    'übersprungen: {why}':
        'saltato: {why}',
    'unbekannte Aktion':
        'azione sconosciuta',
    'Zeiten fehlen':
        'tempi mancanti',
    'Bereich zu kurz oder ausserhalb':
        'intervallo troppo corto o fuori',
    'Tempo nicht erlaubt':
        'velocità non disponibile',
    '{a}–{b} mit Tempo {f}×':
        '{a}–{b} a velocità {f}×',
    'würde alles entfernen':
        'rimuoverebbe tutto',
    '{a}–{b} herausgeschnitten':
        '{a}–{b} tagliato',
    'nur {a}–{b} behalten':
        'tenuto solo {a}–{b}',
    'Stelle ausserhalb':
        'momento fuori',
    'Schnitt bei {a}':
        'diviso a {a}',
    'keine Änderung':
        'nessuna modifica',
    'Blende ungültig':
        'dissolvenza non disponibile',
    'Standbild: Dauer ungültig':
        'fermo immagine: durata non consentita',
    'Untertitel zu kurz':
        'sottotitolo troppo corto',
    '{n} weitere Schritte nicht ausgeführt (höchstens {max})':
        'altri {n} passi non eseguiti (al massimo {max})',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen.':
        'Non possibile ora – termina prima la modifica in corso, poi applica.',
    'Standbild bei {a} für {s} s':
        'fermo immagine a {a} per {s} s',
    'Blende ohne Dauer':
        'dissolvenza senza durata',
    'Blenden: ein {i} s, aus {o} s':
        'dissolvenze: entrata {i} s, uscita {o} s',
    'Export-Art unbekannt':
        'tipo di esportazione sconosciuto',
    'Export-Art: {m}':
        'tipo di esportazione: {m}',
    'nur bei Export-Art Short':
        'solo con tipo di esportazione Short',
    'Text fehlt':
        'testo mancante',
    'Short-Titel „{t}“':
        'titolo dello short «{t}»',
    'Untertitel: Zeiten fehlen':
        'sottotitolo: tempi mancanti',
    'zu viele Untertitel':
        'troppi sottotitoli',
    'Untertitel {a}–{b}':
        'sottotitolo {a}–{b}',
    'Claude: Der API-Key wird nicht angenommen – unter Einstellungen → Verbindungen prüfen („API-Key holen“ öffnet die Anthropic Console).':
        'Claude: la chiave API non viene accettata – controllala in Impostazioni → Connessioni («Ottieni chiave API» apre la Anthropic Console).',
    'Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen → Verbindungen → „Guthaben aufladen“.':
        "Claude: credito esaurito sull'account API – Impostazioni → Connessioni → «Aggiungi credito».",
    'API-Key holen':
        'Ottieni chiave API',
    'Guthaben aufladen':
        'Aggiungi credito',
    'Öffnet die Seite „API keys“ der Anthropic Console im Browser (platform.claude.com). Dort einen Key anlegen und hier einfügen – er beginnt mit sk-ant-.':
        'Apre nel browser la pagina «API keys» della Anthropic Console (platform.claude.com). Crea lì una chiave e incollala qui – inizia con sk-ant-.',
    'Öffnet die Seite „Billing“ der Anthropic Console im Browser. Die API wird getrennt von einem Claude-Abo im Voraus bezahlt; dort lässt sich auch ein monatliches Ausgabenlimit setzen.':
        "Apre nel browser la pagina «Billing» della Anthropic Console. L'API si paga in anticipo, separatamente da un abbonamento Claude; lì puoi anche impostare un limite di spesa mensile.",
    'Zeigt in der Suche (Strg+F) die Zeile „Claude fragen“. Erst wenn du sie wählst, gehen deine Frage und die Namen der Einstellungen, Seiten und Aktionen an Claude (api.anthropic.com) – nie Runden, Maps oder Spieldaten. Braucht einen eigenen API-Key.':
        'Mostra la riga «Chiedi a Claude» nella ricerca (Ctrl+F). Solo quando la scegli, la tua domanda e i nomi di impostazioni, pagine e azioni vengono inviati a Claude (api.anthropic.com) – mai round, mappe o dati di gioco. Richiede una tua chiave API.',
    'Schickt eine kleine Probefrage an Claude und sagt, ob der API-Key angenommen wird (kostet einen kleinen Betrag deines API-Guthabens).':
        'Invia a Claude una piccola domanda di prova e dice se la chiave API viene accettata (costa una piccola parte del tuo credito API).',
    'Entfernt den API-Key von diesem PC; die Suche fragt Claude dann nicht mehr.':
        'Rimuove la chiave API da questo PC; la ricerca non chiederà più a Claude.',
    'In der Suche Claude fragen können':
        'Lascia che la ricerca chieda a Claude',
    'API-Key':
        'Chiave API',
    'Key prüfen':
        'Verifica chiave',
    'Key löschen':
        'Elimina chiave',
    'Claude: Key funktioniert.':
        'Claude: la chiave funziona.',
    'Claude: prüfe den Key …':
        'Claude: verifica della chiave …',
    'Claude: kein API-Key eingetragen.':
        'Claude: nessuna chiave API inserita.',
    'Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-).':
        'Claude: non sembra una chiave API (inizia con sk-ant-).',
    'Claude: Key eingetragen.':
        'Claude: chiave inserita.',
    'Schritt {n} von {total}':
        'Passo {n} di {total}',
    'Sprache':
        'Lingua',
    'Sprache dieses Programms:':
        'Lingua di questo programma:',
    'Weiter':
        'Avanti',
    'Zurück':
        'Indietro',
    'Überspringen':
        'Salta',
    'Einrichtung: {step}':
        'Configurazione: {step}',
    'Aufgeteilt':
        'Dettaglio',
    'CPU-Temperatur':
        'Temperatura CPU',
    'GPU gedrosselt':
        'GPU rallentata',
    'GPU-Leistung':
        'Potenza GPU',
    'GPU-Speicher':
        'Memoria GPU',
    'GPU-Temperatur':
        'Temperatura GPU',
    'Hotspot':
        'Hot spot',
    'Höchstwert':
        'Massimo',
    'Höchstwerte':
        'Valori massimi',
    'RAM':
        'RAM',
    'Runden, zusammen {time}':
        'round, {time} in totale',
    'VRAM':
        'VRAM',
    'Wert':
        'Valore',
    '{n} von {total}':
        '{n} di {total}',
    'Ø CPU-Temperatur':
        'Ø temperatura CPU',
    'Ø GPU-Last':
        'Ø carico GPU',
    'Ø GPU-Leistung':
        'Ø potenza GPU',
    'Ø GPU-Temperatur':
        'Ø temperatura GPU',
    'über {n} Runden':
        'su {n} round',
    'Bilanz: Ø 2,8 Kills · 12 Runden':
        'Record: Ø 2.8 uccisioni · 12 round',
    'Infos und Schrift (Name, Timer, Bilanz, Server)':
        'Info e testo (nome, timer, record, server)',
    'Eigenes Element unter der Karte':
        'Elemento a sé sotto la mappa',
    'Eigenes Element über der Karte':
        'Elemento a sé sopra la mappa',
    'Eigenes Element, eigene Position':
        'Elemento a sé, posizione propria',
    'Mit der Karte verbunden, unten':
        'Unito alla mappa, sotto',
    'Mit der Karte verbunden, oben':
        'Unito alla mappa, sopra',
    'Infos':
        'Info',
    'INFOS':
        'INFO',
    'Infos (Timer, Bilanz, Server)':
        'Info (timer, record, server)',
    'In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine Sofort-Clips (F8) und keinen Vorlauf.':
        'Il buffer di replay di OBS non è attivato – OBS: Impostazioni → Uscita → Buffer di replay → «Abilita buffer di replay» e applica. Senza di esso non ci sono clip istantanee (F8) né pre-roll.',
    'Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)':
        'Buffer di replay non attivato in OBS (Impostazioni → Uscita → Buffer di replay)',
    'Karten im selben Balken gleich breit':
        'Schede nella stessa barra larghe uguali',
    'Zu einer Spalte zusammenführen':
        'Unisci in una colonna',
    'Die Karten, die im selben schwarzen Balken stehen, werden so breit gezeichnet wie die breiteste von ihnen – untereinander ergeben sie eine Spalte mit bündigen Rändern.':
        "Le schede che stanno nella stessa barra nera vengono disegnate larghe quanto la più larga – una sotto l'altra formano una colonna con bordi allineati.",
    'Heute unter die Systemwerte, die Musik unter Heute, alle gleich breit – eine Spalte im Balken der Systemwerte. Rückgängig mit Strg+Z.':
        'Oggi sotto i valori di sistema, la musica sotto oggi, tutti con la stessa larghezza – una colonna nella barra dei valori di sistema. Annulla con Ctrl+Z.',
    'Cover':
        'Copertina',
    'Discord-Overlay freihalten':
        "Tieni libero l'overlay di Discord",
    'Karte, Infos, Systemwerte, Heute und Musik weichen den Stellen aus, an denen Discords Overlay seine Widgets zeigt (in der Vorschau schraffiert). Das Programm liest nichts aus Discord – die Flächen sind fest.':
        "Mappa, info, valori di sistema, oggi e musica stanno lontani dai punti in cui l'overlay di Discord mostra i suoi widget (tratteggiati nell'anteprima). Il programma non legge nulla da Discord – le aree sono fisse.",
    'Wie der Stil':
        'Come lo stile',
    'Rund':
        'Arrotondato',
    'Eckig':
        'Quadrato',
    '{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr (der schwarze Balken ist voll).':
        '{what} è già al massimo qui – da {cap} % in su il cursore non cambia nulla (la barra nera è piena).',
    'Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).':
        "Più grande con «La mappa può diventare più grande della barra» (sconfina poi nell'immagine di gioco).",
    'Spielbild':
        'Immagine di gioco',
    'Map-Name':
        'Nome mappa',
    'Farbthema':
        'Tema colori',
    'Gold (Standard)':
        'Oro (predefinito)',
    'Blutrot':
        'Rosso sangue',
    'Eisblau':
        'Blu ghiaccio',
    'Giftgrün':
        'Verde tossico',
    'Lila':
        'Viola',
    '„Heute“: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit':
        '«Oggi»: round, tempo di gioco, Ø uccisioni/fughe, orologio',
    'Eine eigene Karte, solange eine Map im Match zu sehen ist: wie viele Runden du heute gespielt hast, wie lange, Ø Kills bzw. Entkommen laut Stats-Seite und die Uhrzeit. Position darunter, Grösse über den Grössenregler („Heute“ wählen).':
        "Una scheda a sé mentre in partita c'è una mappa sullo schermo: quanti round hai giocato oggi, per quanto tempo, Ø uccisioni o fughe dalla pagina statistiche e l'ora. Posizione sotto, dimensione tramite il cursore della dimensione (scegli «Oggi»).",
    'Dunkle Fläche hinter „Heute“':
        'Area scura dietro «Oggi»',
    'Vorlage':
        'Preimpostazione',
    'Vorlage anwenden':
        'Applica preimpostazione',
    'Alles links':
        'Tutto a sinistra',
    'Alles rechts':
        'Tutto a destra',
    'Verteilt: Karte links, Werte rechts':
        'Distribuito: mappa a sinistra, valori a destra',
    'Vorlage „{name}“ angewendet.':
        'Preimpostazione «{name}» applicata.',
    'Setzt Karte, Systemwerte, „Heute“ und Musik auf einmal auf die gewählte Anordnung. „Rückgängig“ holt die vorherige zurück.':
        'Mette subito mappa, valori di sistema, «Oggi» e musica nella disposizione scelta. «Annulla» riporta quella precedente.',
    'Weich ein- und ausblenden':
        'Dissolvenza morbida in entrata e uscita',
    'In kleinen DBD-Fenstern ausblenden':
        'Nascondi nelle finestre di DBD piccole',
    'Läuft DBD in einem kleinen Fenster (Bild kleiner als 1920×1080 oder schmaler als 16:9), zeigt das Programm im Spiel nichts – wie der Hauptschalter. Map-Erkennung, Statistik und OBS-Aufnahmen laufen weiter. Wird das Fenster wieder gross, erscheint das Overlay von selbst.':
        "Se DBD gira in una finestra piccola (immagine più piccola di 1920×1080 o più stretta di 16:9), il programma non mostra nulla nel gioco – come l'interruttore generale. Rilevamento mappa, statistiche e registrazioni OBS continuano. Quando la finestra torna grande, l'overlay ritorna da solo.",
    'Kleines DBD-Fenster ({w}×{h}) – Overlay ausgeblendet, Runden werden weiter gezählt und aufgenommen.':
        'Finestra di DBD piccola ({w}×{h}) – overlay nascosto, i round vengono comunque contati e registrati.',
    'Update gesperrt: eine Runde läuft. Nach dem Rundenende noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Aggiornamento bloccato: è in corso un round. Fai di nuovo clic su «Aggiorna e riavvia» quando il round è finito.',
    'Alle Farming-Runden der Auswahl (Zeitraum, Region, Map, Modus) – unabhängig vom Rollen-Filter und von „Farming ausblenden“. Farming = Crossplay war in der Lobby aus (oder die eingestellte Farming-Region); korrigieren unter „Letzte Runden“ mit „Farming an/aus“. Aufnahmen liegen im Unterordner „Farming“ des Aufnahmeordners. Wartezeit „sofort“: die Lobby war voll, bevor eine Suchzeit messbar war. Server nur, wenn „Verbunden mit“ auf der Seite Server läuft.':
        'Tutti i round di farming della selezione (periodo, regione, mappa, modalità) – qualunque cosa dicano il filtro ruolo e «Nascondi farming». Farming = il cross-play era disattivato nella lobby (o la regione di farming che hai impostato); correggilo in «Ultimi round» con «Farming on/off». Le registrazioni sono nella sottocartella «Farming» della cartella registrazioni. Attesa «immediato»: la lobby era piena prima che si potesse misurare un tempo di ricerca. Server solo mentre «Connesso a» è attivo nella pagina Server.',
    'Keine Farming-Runden in dieser Auswahl.':
        'Nessun round di farming in questa selezione.',
    '{n} als Killer · {m} als Survivor':
        '{n} da Killer · {m} da Sopravvissuto',
    'Spielzeit':
        'Tempo di gioco',
    'vom Map-Banner bis zum Rundenende':
        'dal banner della mappa alla fine del round',
    'BP':
        'BP',
    '{n} gespeicherte Matches haben ein Loadout, aber keines davon ist in dieser Auswahl. Custom Games zählen nur mit dem Rollen-Filter „Custom Games“, Farming-Runden nicht mit „Farming ausblenden“, Matches ohne erkannte Runde gar nicht.':
        '{n} partite salvate hanno un loadout, ma nessuna è in questa selezione. Le partite personalizzate contano solo con il filtro ruolo «Partite personalizzate», i round di farming non con «Nascondi farming», le partite senza un round rilevato mai.',
    'DBD-Fenster wieder gross genug – Overlay wieder an.':
        'Finestra di DBD di nuovo abbastanza grande – overlay di nuovo attivo.',
    'Overlay anzeigen':
        "Mostra l'overlay",
    'Hauptschalter: aus = das Programm zeigt im Spiel nichts (Karte, Systemwerte, Heute, Musik). Erkennung, Statistik und Aufnahmen laufen weiter. Auch als Knopf in der Übersicht.':
        'Interruttore generale: off = il programma non mostra nulla nel gioco (mappa, valori di sistema, Oggi, musica). Rilevamento, statistiche e registrazioni continuano. Anche come pulsante nella panoramica.',
    'Overlay eingeschaltet.':
        'Overlay attivato.',
    'Overlay ausgeschaltet – die Erkennung läuft weiter.':
        'Overlay disattivato – il rilevamento continua.',
    'Overlay ausschalten':
        'Disattiva overlay',
    'Overlay einschalten':
        'Attiva overlay',
    'Blendet alles aus, was das Programm im Spiel zeigt – Karte, Systemwerte, Heute, Musik. Die Erkennung, Statistik und Aufnahmen laufen weiter.':
        'Nasconde tutto ciò che il programma mostra nel gioco – mappa, valori di sistema, Oggi, musica. Rilevamento, statistiche e registrazioni continuano.',
    'Zeigt das Overlay im Spiel wieder an.':
        "Mostra di nuovo l'overlay nel gioco.",
    'Karte, Systemwerte und „Heute“ blenden in einer Drittelsekunde ein und aus, statt hart zu erscheinen. Die Musik hat ihr eigenes Häkchen.':
        'Mappa, valori di sistema e «Oggi» compaiono e scompaiono in dissolvenza in un terzo di secondo invece di apparire di colpo. La musica ha una casella a sé.',
    'Unter „Heute“':
        'Sotto «Oggi»',
    'Unter der Musik':
        'Sotto la musica',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter „Heute“.':
        "Un'area scura semitrasparente con angoli arrotondati dietro «Oggi».",
    'HEUTE':
        'OGGI',
    'ENTKOMMEN ':
        'FUGHE ',
    'HEUTE ':
        'OGGI ',
    'UHR ':
        'TEMPO ',
    '{n} RUNDEN · {time}':
        '{n} ROUND · {time}',
    'Ø KILLS ':
        'Ø UCCISIONI ',
    'NORMAL ':
        'NORMALI ',
    'FARMING ':
        'FARMING ',
    'BP/H ':
        'BP/H ',
    'OLED-Schwarz':
        'Nero OLED',
    'Hintergründe in echtem Schwarz statt Dunkelgrau – passt zu OLED-Bildschirmen und geht mit jeder Akzentfarbe. Im hellen Modus ohne Wirkung.':
        "Sfondi in nero puro invece che grigio scuro – adatto agli schermi OLED e sta bene con ogni colore d'accento. Nessun effetto in modalità chiara.",
    'Eigene Farbe':
        'Colore personalizzato',
    'Eigene Farbe …':
        'Colore personalizzato …',
    'Beliebige Farbe wählen – das Programm passt die Helligkeit an, bis alles lesbar ist.':
        'Scegli un colore qualsiasi – il programma ne regola la luminosità finché tutto è leggibile.',
    '„Läuft gerade“: Titel, Interpret und Cover':
        '«In riproduzione»: titolo, artista e copertina',
    'Liest Titel und Interpret aus der Windows-Mediensteuerung (dieselbe Liste wie beim Lautstärkeregler von Windows) – nur Anzeige, das Programm steuert nichts und speichert nichts.':
        'Legge titolo e artista dai controlli multimediali di Windows (lo stesso elenco del pannello volume di Windows) – solo visualizzazione, il programma non controlla nulla e non salva nulla.',
    'Unter den Systemwerten':
        'Sotto i valori di sistema',
    'Rechts unten im Balken':
        'In basso a destra nella barra',
    'Links unten im Balken':
        'In basso a sinistra nella barra',
    'MUSIK':
        'MUSICA',
    'läuft gerade':
        'in riproduzione',
    'Albumcover zeigen':
        "Mostra la copertina dell'album",
    'Auch Videos zeigen (YouTube, Twitch …) – aus: nur Musik':
        'Mostra anche i video (YouTube, Twitch …) – off: solo musica',
    'Die Mediensteuerung meldet auch Videos aus dem Browser. An: ein Video erscheint als „▶ Titel“ mit dem Kanal darunter. Aus: die Karte zeigt nur Musik. Unterschieden wird am Album: Musikdienste melden eins, ein Video nicht.':
        "I controlli multimediali segnalano anche i video del browser. On: un video compare come «▶ Titolo» con il canale sotto. Off: la scheda mostra solo musica. Distinti dall'album: i servizi musicali ne indicano uno, un video no.",
    'Balken in der Farbe des Covers':
        'Barra nel colore della copertina',
    'Dunkle Fläche hinter Karte und Infos':
        'Area scura dietro la mappa e le sue righe',
    'Dunkle Fläche hinter den Systemwerten':
        'Area scura dietro i valori di sistema',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Karte, Timer und Infozeilen (auch hinter „Warte auf Map“) – gut lesbar über hellen Stellen im Spiel.':
        "Un'area scura semitrasparente con angoli arrotondati dietro mappa, timer e righe di info (anche dietro «In attesa della mappa») – facile da leggere sopra le parti chiare del gioco.",
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Systemwerten und „Heute“.':
        "Un'area scura semitrasparente con angoli arrotondati dietro i valori di sistema e «Oggi».",
    'Restzeit statt Länge (−1:46)':
        'Tempo rimanente invece della durata (−1:46)',
    'Dunkle Fläche hinter der Musikkarte':
        'Area scura dietro la scheda musicale',
    'Weich ein- und ausblenden (auch beim nächsten Lied)':
        'Dissolvenza morbida in entrata e uscita (anche al brano successivo)',
    'Der Fortschrittsbalken nimmt die Hauptfarbe des Albumcovers an, wie bei Spotify. Graue Cover: weiss.':
        'La barra di avanzamento prende il colore principale della copertina, come in Spotify. Copertine grigie: bianco.',
    'Rechts neben dem Balken steht, wie lange das Lied noch läuft, statt seiner Gesamtlänge.':
        'A destra della barra: quanto dura ancora il brano invece della sua durata totale.',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Cover und Text – gut lesbar, wenn die Karte über hellen Stellen im Spiel liegt.':
        "Un'area scura semitrasparente con angoli arrotondati dietro copertina e testo – facile da leggere quando la scheda sta sopra parti chiare del gioco.",
    'Die Musikkarte blendet in einer Drittelsekunde ein und aus, statt hart zu erscheinen – auch wenn ein neues Lied beginnt.':
        'La scheda musicale compare e scompare in dissolvenza in un terzo di secondo invece di apparire di colpo – anche quando inizia un nuovo brano.',
    'Das Bild zum Lied links neben Titel und Interpret – Windows liefert es mit; es bleibt nur im Speicher.':
        "L'immagine del brano a sinistra di titolo e artista – la fornisce Windows; resta solo in memoria.",
    'Gross – Cover oben, Titel darunter':
        'Grande – copertina sopra, titolo sotto',
    'Kompakt – Cover links':
        'Compatta – copertina a sinistra',
    'Fortschritt des Lieds zeigen':
        "Mostra l'avanzamento del brano",
    'Unter Titel und Künstler: wie weit das Lied ist, mit Balken und Länge – wie in Spotify.':
        'Sotto titolo e artista: a che punto è il brano, con una barra e la sua durata – come in Spotify.',
    'KARTE · Strg+Mausrad = Grösse':
        'MAPPA · Ctrl+rotellina = dimensione',
    'Ziehst: {name}':
        'Trascinamento: {name}',
    'Unter der Maus: {name}':
        'Sotto il mouse: {name}',
    'Kartenstil':
        'Stile mappa',
    'Kartenstil: {style}.':
        'Stile mappa: {style}.',
    'Map wählen …':
        'Scegli mappa …',
    'Zur Seite Maps: eine Map von Hand anzeigen (Doppelklick oder „Anzeigen“). Beim nächsten Match übernimmt die automatische Erkennung wieder.':
        'Alla pagina Mappe: mostra una mappa a mano (doppio clic o «Mostra»). Alla prossima partita il rilevamento automatico riprende il controllo.',
    'Erscheint automatisch, sobald im Match das Map-Banner kommt – oder von Hand über „Map wählen“.':
        'Compare da sola appena in partita arriva il banner della mappa – oppure a mano con «Scegli mappa».',
    'Wann zeigen':
        'Quando mostrare',
    'Alle Maps':
        'Tutte le mappe',
    'Zuletzt gespielt':
        'Giocate per ultime',
    'Suchen: Name, Realm, Abkürzung …':
        'Cerca: nome, Realm, abbreviazione …',
    'Klick oder Enter = groß ansehen · Doppelklick oder Strg+Enter = jetzt anzeigen. Die Erkennung übernimmt beim nächsten Match wieder.':
        'Clic o Enter = vista grande · doppio clic o Ctrl+Enter = mostra ora. Alla prossima partita il rilevamento riprende il controllo.',
    'Zurück zu den Karten des Realms (Esc).':
        'Torna alle mappe del Realm (Esc).',
    'Allgemein':
        'Generale',
    'Alle Einstellungen zurücksetzen':
        'Ripristina tutte le impostazioni',
    'Alle Einstellungen auf die Auslieferung zurücksetzen? Runden, Match-Daten und eigene Bilder bleiben. Das Programm startet danach neu.':
        'Riportare ogni impostazione allo stato di consegna? Round, dati partita e immagini personali restano. Il programma si riavvierà subito dopo.',
    'Alle Einstellungen zurückgesetzt.':
        'Tutte le impostazioni ripristinate.',
    'Standard wiederherstellen':
        'Ripristina predefinito',
    'Ausschalten':
        'Disattiva',
    '{free} von {total} Regionen freigegeben':
        '{free} di {total} regioni consentite',
    'DBD läuft gerade – die Änderung gilt erst nach einem Neustart von DBD.':
        'DBD è in esecuzione – la modifica ha effetto solo dopo il riavvio di DBD.',
    'Suchen …':
        'Cerca …',
    'Setzt jede Einstellung auf die Auslieferung zurück (Overlay, Hotkeys, Erkennung, Server-Auswahl im Programm …). Runden, Match-Daten und eigene Bilder bleiben; das Programm startet danach neu. Vorher sichern: „Einstellungen exportieren“.':
        'Riporta ogni impostazione allo stato di consegna (overlay, hotkey, rilevamento, la scelta delle regioni nel programma …). Round, dati partita e immagini personali restano; poi il programma si riavvia. Prima fai un backup: «Esporta impostazioni».',
    'Grösse {pct} %':
        'dimensione {pct} %',
    'Eigene Einstellungen dieser Map: {what}':
        'Impostazioni proprie di questa mappa: {what}',
    'Eigene Grösse und Drehung zurücksetzen':
        'Ripristina dimensione e rotazione proprie',
    'Kartenbild ersetzen …':
        'Sostituisci immagine mappa …',
    'Im schwarzen Rand, solange die Karte im Match zu sehen ist. GPU-Werte von NVIDIA (Treiber), CPU-Temperatur nur mit HWiNFO („Shared Memory Support“ an) – kein eigener Treiber.':
        'Nella barra nera mentre in partita la mappa è sullo schermo. Valori GPU da NVIDIA (driver), temperatura CPU solo con HWiNFO («Shared Memory Support» attivo) – nessun driver proprio.',
    'Standard (wie ausgeliefert)':
        'Standard (come consegnato)',
    'Fenster {size}':
        'finestra {size}',
    'alle Fenstergrössen':
        'tutte le dimensioni di finestra',
    'Gilt für: {window}':
        'Vale per: {window}',
    'Gilt für: {maps} · {window}':
        'Vale per: {maps} · {window}',
    'nur {map}':
        'solo {map}',
    'alle Maps (keine Map eingeblendet)':
        'tutte le mappe (nessuna mappa sullo schermo)',
    'Letzte 7 Tage':
        'Ultimi 7 giorni',
    'Letzte 30 Tage':
        'Ultimi 30 giorni',
    'Rolle/Killer':
        'Ruolo/Killer',
    'Weitere 100 Runden anzeigen':
        'Mostra altri 100 round',
    'Runden exportieren':
        'Esporta round',
    '{n} Runden exportiert: {path}':
        '{n} round esportati: {path}',
    'Median':
        'Mediana',
    '{n} Runden':
        '{n} round',
    'Längste':
        'Più lunga',
    'Die Liste zeigt die neuesten 100 Runden der Auswahl; jeder Klick hängt 100 ältere an.':
        "L'elenco mostra i 100 round più recenti della selezione; ogni clic ne aggiunge 100 più vecchi.",
    'Server-Tab öffnen':
        'Apri la scheda Server',
    'Match-Daten einrichten …':
        'Configura dati partita …',
    'Einrichten …':
        'Configura …',
    'Noch keine Runden heute':
        'Ancora nessun round oggi',
    'Stats-Seite':
        'Pagina statistiche',
    'nicht eingerichtet':
        'non configurato',
    'Match-Daten':
        'Dati partita',
    'Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → Match-Daten → Offizielle Match-Daten).':
        'Uccisioni, fughe e Punti Sangue dei tuoi round arrivano da stats.deadbydaylight.com – caricati dal tuo browser, non dal programma. Configurabile anche più tardi (Impostazioni → Dati partita → Dati partita ufficiali).',
    'Zur Seite Server: dort „Spielserver anzeigen“ anhaken – Region und Ping stehen dann hier und im Overlay.':
        "Alla pagina Server: spunta lì «Mostra server di gioco» – regione e ping compaiono poi qui e nell'overlay.",
    'Zu Einstellungen → Match-Daten → Offizielle Match-Daten: einmal das Userscript in den Browser, danach zählen Kills, Entkommen und Bloodpoints in der Statistik.':
        "A Impostazioni → Dati partita → Dati partita ufficiali: l'userscript nel browser una volta, poi uccisioni, fughe e Punti Sangue contano nelle statistiche.",
    'CPU DROSSELT (TEMP.)':
        'CPU THROTTLED (TEMP.)',
    'CPU gedr.':
        'CPU rall.',
    'GPU gedr.':
        'GPU rall.',
    'CPU gedrosselt':
        'CPU rallentata',
    'CPU Ø W':
        'CPU Ø W',
    'CPU-Leistung':
        'Potenza CPU',
    'Kern Ø %':
        'Core Ø %',
    'Ø CPU-Leistung':
        'Ø potenza CPU',
    'Ø stärkster CPU-Kern':
        'Ø core CPU più carico',
    'Niedrigstes FPS-Tief':
        'FPS low minimo',
    'Ø FPS':
        'Ø FPS',
    'Ø FPS-Tief':
        'Ø FPS low',
    'FPS Ø':
        'FPS Ø',
    'FPS Tief':
        'FPS low',
    'Klick: sortieren · Rechtsklick: Spalten ein-/ausblenden':
        'Clic: ordina · clic destro: mostra/nascondi colonne',
    'Alle Spalten zeigen':
        'Mostra tutte le colonne',
    'Exportieren …':
        'Esporta …',
    'Zeitraum':
        'Intervallo di tempo',
    'Von':
        'Da',
    'Bis':
        'A',
    'TT.MM.JJJJ HH:MM – auch nur ein Datum (ganzer Tag) oder nur eine Uhrzeit (heute); leer = offen.':
        "GG.MM.AAAA HH:MM – va bene anche solo una data (tutto il giorno) o solo un'ora (oggi); vuoto = aperto.",
    'Gestern':
        'Ieri',
    'Alles':
        'Tutto',
    'Eigener Zeitraum':
        'Intervallo personalizzato',
    'Filter':
        'Filtri',
    'Custom Games einschliessen':
        'Includi partite personalizzate',
    'Farming-Runden einschliessen':
        'Includi round di farming',
    'Spalten':
        'Colonne',
    'Start':
        'Inizio',
    'Realm':
        'Realm',
    'Ping (ms)':
        'Ping (ms)',
    'Kills':
        'Uccisioni',
    'Normal':
        'Normale',
    'ja':
        'sì',
    'nein':
        'no',
    'CSV-Datei (Excel)':
        'File CSV (Excel)',
    'Textliste (eine Zeile je Runde)':
        'Elenco di testo (una riga per round)',
    '{n} Runden, {m} Spalten':
        '{n} round, {m} colonne',
    'Zeitangabe nicht lesbar: „{text}“ – Format TT.MM.JJJJ HH:MM.':
        "Impossibile leggere l'ora «{text}» – formato GG.MM.AAAA HH:MM.",
    'Nichts zu kopieren – keine Runde passt, oder keine Spalte gewählt.':
        'Niente da copiare – nessun round corrisponde, o nessuna colonna scelta.',
    'Nichts zu speichern – keine Runde passt, oder keine Spalte gewählt.':
        'Niente da salvare – nessun round corrisponde, o nessuna colonna scelta.',
    'In Zwischenablage kopieren':
        'Copia negli appunti',
    'Als Datei speichern …':
        'Salva come file …',
    'Schliessen':
        'Chiudi',
    '{n} Runden in die Zwischenablage kopiert.':
        '{n} round copiati negli appunti.',
    'Spalte „{name}“ mit ausgeben.':
        'Includi la colonna «{name}».',
    'Öffnet das Export-Fenster: Zeitraum (auch von–bis), Rolle, Killer, Map, Region, Spalten nach Wahl – als CSV für Excel oder als Textliste in die Zwischenablage. Die Filter der Statistik sind vorbelegt.':
        'Apre la finestra di esportazione: intervallo di tempo (anche da–a), ruolo, Killer, mappa, regione, colonne a scelta – come CSV per Excel o come elenco di testo negli appunti. I filtri delle statistiche sono preimpostati.',
    'Kopiert die Runden in der gewählten Form (CSV oder Textliste) in die Zwischenablage – zum Einfügen in Discord, Excel oder einen Editor.':
        'Copia i round nella forma scelta (CSV o elenco di testo) negli appunti – da incollare in Discord, Excel o un editor.',
    'Speichert die Runden als Datei: CSV (Semikolon, UTF-8 mit BOM – Excel öffnet sie direkt) oder Textliste (.txt).':
        'Salva i round come file: CSV (punto e virgola, UTF-8 con BOM – Excel lo apre direttamente) o elenco di testo (.txt).',
    'Schliesst das Fenster.':
        'Chiude la finestra.',
    'Aus: Custom Games (eigene Lobbys, Bots) bleiben draussen.':
        'Off: le partite personalizzate (lobby proprie, bot) restano fuori.',
    'Aus: Farming-Runden (Crossplay aus bzw. Farming-Region) bleiben draussen.':
        'Off: i round di farming (cross-play disattivato o la regione di farming) restano fuori.',
    'Eine Zeile je Runde, Spalten durch Semikolon getrennt, mit Kopfzeile.':
        "Una riga per round, colonne separate da punto e virgola, con una riga d'intestazione.",
    'Eine Zeile je Runde, die gewählten Spalten mit „ · “ getrennt, ohne Kopfzeile – zum Einfügen in einen Chat.':
        'Una riga per round, le colonne scelte separate da « · », senza intestazione – da incollare in una chat.',
    'Verbindungen':
        'Connessioni',
    'Ton':
        'Suono',
    'Aufräumen':
        'Pulizia',
    'Jede Runde mit OBS aufnehmen':
        'Registra ogni round con OBS',
    'Port':
        'Porta',
    'Passwort':
        'Password',
    'Verbindung testen':
        'Prova connessione',
    'Aufnahmeordner wählen …':
        'Scegli cartella registrazioni …',
    '(kein Ordner gewählt)':
        '(nessuna cartella scelta)',
    'Platz für Aufnahmen':
        'Spazio per le registrazioni',
    'Ganze Platte (Älteste weg, wenn sie voll wird)':
        'Intera unità (le più vecchie vengono eliminate quando si riempie)',
    'Vorlauf aus dem OBS-Wiederholungspuffer sichern':
        "Tieni un'introduzione dal buffer di replay di OBS",
    'OBS nimmt auf, das Programm sagt nur wann: Start beim Map-Banner, Stopp beim erkannten Rundenende, Datei nach Datum, Map und Killer benannt. Dafür in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server einschalten und Port und Passwort unter Verbindungen → OBS-Verbindung eintragen; Verbindung nur auf diesem PC (127.0.0.1). Empfohlen: Aufnahmeformat MKV oder Hybrid-MP4 (bleibt bei Abbruch lesbar), Fenster- oder Bildschirmaufnahme statt Spielaufnahme. Der Ordner wird über sein Laufwerk gemerkt – ist die Platte nicht angeschlossen, wird nicht aufgenommen.':
        "Registra OBS, il programma dice solo quando: avvio al banner della mappa, stop alla fine del round rilevata, file chiamato con data, mappa e Killer. In OBS attiva il server in Strumenti → Impostazioni server WebSocket e inserisci porta e password in Connessioni → Connessione OBS; la connessione resta su questo PC (127.0.0.1). Consigliato: formato di registrazione MKV o MP4 ibrido (resta leggibile dopo un crash), cattura finestra o schermo anziché cattura gioco. La cartella viene memorizzata in base alla sua unità – con l'unità scollegata non viene registrato nulla.",
    'Ordner für die Aufnahmen (z. B. auf der externen Platte)':
        "Cartella per le registrazioni (ad es. sull'unità esterna)",
    'Aufnahmeordner: {path}':
        'Cartella registrazioni: {path}',
    'Verbinde mit OBS …':
        'Connessione a OBS …',
    'Aufnahme: {text}':
        'Registrazione: {text}',
    'Aufnahme gespeichert: {file}':
        'Registrazione salvata: {file}',
    'Aufnahmen gelöscht (Platz): {n}':
        'Registrazioni eliminate (spazio): {n}',
    'OBS hat die Verbindung geschlossen':
        'OBS ha chiuso la connessione',
    'OBS antwortet nicht auf die Anfrage {kind}':
        'OBS non risponde alla richiesta {kind}',
    'OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})':
        'OBS non raggiungibile – OBS è in esecuzione con il suo server WebSocket attivo? ({error})',
    'Keine Antwort von obs-websocket':
        'Nessuna risposta da obs-websocket',
    'Kein obs-websocket auf diesem Port':
        'Nessun obs-websocket su questa porta',
    'Falsche WebSocket-Antwort':
        'Risposta WebSocket errata',
    'Unerwartete Begrüssung von OBS':
        'Saluto inatteso da OBS',
    'OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)':
        'OBS richiede una password (OBS: Strumenti → Impostazioni server WebSocket)',
    'OBS hat die Anmeldung abgelehnt – Passwort falsch?':
        "OBS ha rifiutato l'accesso – password sbagliata?",
    'OBS {version} verbunden':
        'OBS {version} connesso',
    'nimmt gerade auf':
        'registrazione in corso',
    'bereit':
        'pronto',
    'Wiederholungspuffer läuft':
        'buffer di replay attivo',
    'Wiederholungspuffer aus (kein Vorlauf)':
        'buffer di replay disattivato (nessun pre-roll)',
    'Ordner: {folder}':
        'Cartella: {folder}',
    'Ordner/Laufwerk nicht gefunden':
        'cartella/unità non trovata',
    'Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen':
        'Unità di registrazione non collegata – il round non viene registrato',
    'Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen':
        'Unità di registrazione quasi piena – il round non viene registrato',
    'OBS nimmt schon auf (von Hand?) – nichts gestartet':
        'OBS sta già registrando (a mano?) – nulla avviato',
    'Nimmt die Runde auf':
        'Registrazione del round',
    'OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet':
        'OBS non ha fornito un nome di file – registrazione non assegnata',
    "Aufnahme liegt in OBS' eigenem Ordner: {path}":
        'La registrazione è nella cartella di OBS: {path}',
    'Gespeichert: {file}':
        'Salvata: {file}',
    'Das Programm startet die OBS-Aufnahme beim Map-Banner und stoppt sie beim erkannten Rundenende (obs-websocket, nur auf diesem PC). OBS muss laufen.':
        'Il programma avvia la registrazione di OBS al banner della mappa e la ferma alla fine del round rilevata (obs-websocket, solo su questo PC). OBS deve essere in esecuzione.',
    'Verbindet sich einmal mit OBS und zeigt Version, Aufnahmezustand, Wiederholungspuffer und ob der Aufnahmeordner erreichbar ist.':
        'Si connette una volta a OBS e mostra la sua versione, se sta registrando, il buffer di replay e se la cartella registrazioni è raggiungibile.',
    'Ordner, in den OBS die Runden legt – z. B. auf der externen Platte. Gemerkt wird das Laufwerk, nicht der Buchstabe: bekommt die Platte einen anderen, findet das Programm den Ordner trotzdem.':
        "Cartella in cui OBS mette i round – ad es. sull'unità esterna. Viene memorizzata l'unità, non la sua lettera: se l'unità ne riceve un'altra, il programma trova comunque la cartella.",
    'Läuft in OBS der Wiederholungspuffer, wird er beim Map-Banner gespeichert – der Anfang (Spawn) fehlt dann nicht, aber die Datei enthält auch Lobby und Ladebildschirm. Seit 1.5.5 standardmässig aus (Wunsch des Nutzers: nur die Runde). Die Datei liegt als „(Vorlauf)“ neben der Runde.':
        "Se il buffer di replay di OBS è attivo, viene salvato al banner della mappa – così l'inizio (spawn) non manca, ma il file contiene anche la lobby e la schermata di caricamento. Disattivato per impostazione predefinita dalla 1.5.5 (desiderio dell'utente: solo il round). Il file sta accanto al round come «(Vorlauf)».",
    'Wiederholungspuffer mit DBD starten und stoppen':
        'Avvia e ferma il buffer di replay con DBD',
    'Nur das DBD-Fenster aufnehmen':
        'Registra solo la finestra di DBD',
    'Dafür die OBS-Spielaufnahme verwenden':
        'Usa per questo la cattura gioco di OBS',
    'Statt der Fensteraufnahme legt das Programm in OBS eine Spielaufnahme „Fog Scout – DBD-Spiel“ an und blendet die Fensteraufnahme aus. Die Spielaufnahme braucht etwas weniger Leistung; OBS hängt sich dafür mit seinem Anti-Cheat-kompatiblen Hook ins Spiel – das macht OBS, nicht dieses Programm. Ihr eigener Ton bleibt aus, der Spielton kommt weiter über die Tonquelle „Fog Scout – DBD“. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“.':
        "Invece della cattura finestra il programma crea in OBS una cattura gioco «Fog Scout – DBD-Spiel» e nasconde la cattura finestra. La cattura gioco richiede un po' meno risorse; per farlo OBS si aggancia al gioco con il suo hook compatibile con l'anti-cheat – lo fa OBS, non questo programma. Il suo audio resta disattivato, l'audio del gioco arriva comunque tramite la fonte audio «Fog Scout – DBD». Solo insieme a «Registra solo la finestra di DBD».",
    'Bildquelle {name} über {over} gelegt':
        'Fonte immagine {name} messa sopra {over}',
    'Bildquelle angelegt: {name} (Szene „{scene}“)':
        'Fonte immagine creata: {name} (scena «{scene}»)',
    'Bildquelle in der Szene „{scene}“ ausgeblendet: {name}':
        'Fonte immagine nascosta nella scena «{scene}»: {name}',
    'Bildquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'Fonte immagine aggiunta alla scena «{scene}»: {name}',
    'Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'Fonte immagine mostrata di nuovo nella scena «{scene}»: {name}',
    'Bildquelle {name} zeigt jetzt {exe}':
        'La fonte immagine {name} ora mostra {exe}',
    'DBD-Fenster in OBS nicht eingerichtet: {error}':
        'Finestra di DBD non configurata in OBS: {error}',
    'OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin keine Sofort-Clips (F8) und kein Vorlauf.':
        "OBS non è riuscito ad avviare il buffer di replay (OBS segnala un errore di uscita, per lo più l'encoder – dettagli nel log di OBS). Il programma riprova solo al prossimo avvio di DBD; fino ad allora niente clip istantanee (F8) né pre-roll.",
    'Das Programm legt in OBS eine Fensteraufnahme „Fog Scout – DBD-Fenster“ an (oben in der laufenden Szene, auf die Leinwand eingepasst) und stellt sie auf Steam, Epic oder Store um. Aufgenommen wird dann nur das Spiel – ohne Discord, Benachrichtigungen und ohne das Overlay dieses Programms. OBS nimmt dabei über Windows auf; die Spielaufnahme gibt es als Häkchen darunter. Aus: die Quelle wird nur ausgeblendet, deine eigene Bildschirmaufnahme bleibt unangetastet.':
        "Il programma crea in OBS una cattura finestra «Fog Scout – DBD-Fenster» (in cima alla scena in onda, adattata alla tela) e la imposta su Steam, Epic o Store. Così viene registrato solo il gioco – senza Discord, notifiche e senza l'overlay di questo programma. Qui OBS cattura tramite Windows; la cattura gioco è la casella sotto. Off: la fonte viene solo nascosta, la tua cattura schermo resta intatta.",
    'Das Programm startet den Wiederholungspuffer in OBS, sobald DBD läuft, und stoppt ihn, wenn DBD zu ist – so kostet er ausserhalb des Spiels nichts und du musst nicht daran denken.':
        'Il programma avvia il buffer di replay di OBS appena DBD è in esecuzione e lo ferma quando DBD viene chiuso – così fuori dal gioco non costa nulla e non devi pensarci.',
    'Nachlauf nach dem Rundenende':
        'Coda dopo la fine del round',
    'Overlay mit in die Aufnahme':
        'Overlay nella registrazione',
    'Die Fensteraufnahme enthält das Overlay dieses Programms nicht (eigene Fenster). Mit Häkchen schreibt das Programm das sichtbare Overlay – Karte, Infos, Systemwerte, Heute, Musik – als Bild in seinen Cache-Ordner und legt in OBS eine Bildquelle „Fog Scout – Overlay“ darauf an, genau dort, wo das Overlay über dem DBD-Fenster liegt. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“; bei einer Bildschirmaufnahme ist das Overlay ohnehin im Bild. Aus: die Quelle wird nur ausgeblendet.':
        "La cattura finestra non contiene l'overlay di questo programma (finestre proprie). Se spuntato, il programma scrive l'overlay visibile – mappa, righe, valori di sistema, oggi, musica – come immagine nella sua cartella cache e crea su di essa in OBS una fonte immagine «Fog Scout – Overlay», esattamente dove l'overlay sta sopra la finestra di DBD. Solo insieme a «Registra solo la finestra di DBD»; una cattura schermo mostra comunque l'overlay. Off: la fonte viene solo nascosta.",
    'Overlay in OBS nicht eingerichtet: {error}':
        'Overlay non configurato in OBS: {error}',
    '{n} s':
        '{n} s',
    'keiner':
        'nessuno',
    'Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen.':
        'Unità di registrazione non collegata – i round non vengono registrati.',
    'OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})':
        'OBS non è in esecuzione – i round non vengono registrati. ({error})',
    'OBS bereit – Runden werden aufgenommen':
        'OBS pronto – i round vengono registrati',
    'Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).':
        'La registrazione sembra danneggiata ({why}): {file} – controlla le impostazioni di OBS (encoder, unità).',
    'Aufnahme':
        'Registrazione',
    'Vorlauf und Runde zu einer Datei zusammenfügen':
        'Unisci pre-roll e round in un file',
    'Nach der Runde hängt ffmpeg den Vorlauf vorne an die Aufnahme – ohne Neukodierung, in Sekunden. Seit 1.5.5 standardmässig aus: Am PC des Nutzers lief der Rundenteil der zusammengefügten Datei zu schnell. Klappt es nicht, bleiben beide Dateien liegen.':
        "Dopo il round ffmpeg mette il pre-roll davanti alla registrazione – senza ricodifica, pochi secondi di lavoro. Disattivato per impostazione predefinita dalla 1.5.5: sul PC dell'utente la parte del round del file unito veniva riprodotta troppo veloce. Se non riesce, restano entrambi i file.",
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start; bis dahin bleibt der Vorlauf eine eigene Datei.':
        'Manca ffmpeg (pacchetto imageio-ffmpeg) – start.bat lo installa al prossimo avvio; fino ad allora il pre-roll resta un file a sé.',
    'Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben':
        'Salvata: {file} – pre-roll non unito, sta accanto come file a sé',
    'Clip-Marke setzen':
        'Imposta segno clip',
    'Clip-Marke {n} bei {pos} gesetzt.':
        'Segno clip {n} impostato a {pos}.',
    'Keine Aufnahme läuft – keine Clip-Marke gesetzt.':
        'Nessuna registrazione in corso – nessun segno clip impostato.',
    'Aufnahmen':
        'Registrazioni',
    'Aufnahmen einrichten …':
        'Configura registrazioni …',
    'Öffnet die Einstellungen für die Aufnahmen mit OBS (Ordner, Verbindung).':
        'Apre le impostazioni delle registrazioni con OBS (cartella, connessione).',
    'Platte nicht angeschlossen':
        'unità non collegata',
    'kein Ordner gewählt':
        'nessuna cartella scelta',
    'Platz wird gemessen …':
        'misurazione spazio …',
    '{n} mit Marke':
        '{n} con un segno',
    'älteste {date}':
        'la più vecchia {date}',
    '{size} frei':
        '{size} liberi',
    '1 Aufnahme':
        '1 registrazione',
    '{n} Aufnahmen':
        '{n} registrazioni',
    'Abspielen':
        'Riproduci',
    'Alle Aufnahmen':
        'Tutte le registrazioni',
    'Aufnahme fehlt: {file}':
        'Registrazione mancante: {file}',
    'Aufnahme gelöscht: {file}':
        'Registrazione eliminata: {file}',
    'Aufnahme löschen':
        'Elimina registrazione',
    'Aufnahme nicht gelöscht ({error}): {file}':
        'Registrazione non eliminata ({error}): {file}',
    'Aufnahme wird behalten: {file}':
        'La registrazione viene conservata: {file}',
    'Aufnahme wird nicht mehr behalten: {file}':
        'La registrazione non viene più conservata: {file}',
    'Aufnahme-Laufwerk nicht angeschlossen.':
        'Unità di registrazione non collegata.',
    'Aufnahmeordner öffnen':
        'Apri cartella registrazioni',
    'Behalten':
        'Conserva',
    'Beschädigt':
        'Danneggiata',
    'Datei':
        'File',
    'Einschalten unter Einstellungen → Aufnahmen.':
        'Attivala in Impostazioni → Registrazioni.',
    'Im Explorer zeigen':
        'Mostra in Esplora file',
    'Keine Marken – F8 während der Runde setzt eine.':
        'Nessun segno – F8 durante il round ne imposta uno.',
    'Marken: {list}':
        'Segni: {list}',
    'Mit Marke':
        'Con un segno',
    'Nicht mehr behalten':
        'Non conservare più',
    'Noch kein Aufnahmeordner gewählt.':
        'Ancora nessuna cartella registrazioni scelta.',
    'fehlt':
        'mancante',
    '{file} von der Platte löschen?':
        "Eliminare {file} dall'unità?",
    'Spielt die markierte Aufnahme im Standard-Videoplayer ab.':
        'Riproduce la registrazione selezionata nel lettore video predefinito.',
    'Öffnet den Explorer mit der markierten Datei.':
        'Apre Esplora file con il file selezionato evidenziato.',
    'Eine behaltene Aufnahme wird nie fürs Aufräumen gelöscht, wenn die Platte Platz braucht. Nochmal drücken hebt es auf.':
        "Una registrazione conservata non viene mai eliminata dalla pulizia quando l'unità ha bisogno di spazio. Premi di nuovo per annullare.",
    'Löscht die markierte Aufnahme (und ihren Vorlauf) von der Platte – nach Rückfrage.':
        "Elimina la registrazione selezionata (e il suo pre-roll) dall'unità – dopo una conferma.",
    'Öffnet den Aufnahmeordner im Explorer.':
        'Apre la cartella registrazioni in Esplora file.',
    'Farming-Runden im Unterordner „Farming“ ablegen':
        'Metti i round di farming nella sottocartella «Farming»',
    'Runden, die das Programm als Farming erkennt (Crossplay aus oder die Farming-Region), landen im Unterordner „Farming“ des Aufnahmeordners statt zwischen den normalen Runden. Clips gehen immer in den Ordner „Clips“.':
        'I round che il programma riconosce come farming (cross-play disattivato o regione di farming) finiscono nella sottocartella «Farming» della cartella registrazioni invece che tra i round normali. Le clip vanno sempre nella cartella «Clips».',
    'Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in debug/lobby).':
        'Indicatore cross-play non leggibile – il round non conta come farming (ritaglio in debug/lobby).',
    'Rolle für {n} Runden auf {role} geändert.':
        'Ruolo di {n} round cambiato in {role}.',
    '{n} Runden aus der Statistik löschen?':
        'Eliminare {n} round dalle statistiche?',
    '{n} Runden gelöscht.':
        '{n} round eliminati.',
    '{n} Runden zählen jetzt als Farming-Runden.':
        '{n} round ora contano come round di farming.',
    '{n} Runden zählen wieder als normale Runden.':
        '{n} round contano di nuovo come round normali.',
    'Clip bearbeiten …':
        'Modifica clip …',
    'Öffnet den Clip-Editor für die markierte Aufnahme: Vorschau, Zeitleiste mit Marken, Start/Ende setzen, Ausschnitt als MP4 in den Ordner „Clips“ speichern.':
        "Apre l'editor di clip per la registrazione selezionata: anteprima, timeline con segni, imposta inizio/fine, salva il taglio come MP4 nella cartella «Clips».",
    'Clip bearbeiten – {name}':
        'Modifica clip – {name}',
    'Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)':
        "Veloce (sui fotogrammi chiave, l'inizio può essere qualche secondo prima)",
    'Genau (Bild neu kodiert, dauert etwas)':
        'Preciso (immagine ricodificata, richiede un momento)',
    '5 Sekunden vor (Shift+→)':
        '5 secondi avanti (Shift+→)',
    '5 Sekunden zurück (Shift+←)':
        '5 secondi indietro (Shift+←)',
    '▶ Abspielen':
        '▶ Riproduci',
    '⏸ Pause':
        '⏸ Pausa',
    'Abspielen / Pause (Leertaste)':
        'Riproduci / pausa (barra spaziatrice)',
    'Start setzen':
        'Imposta inizio',
    'Ende setzen':
        'Imposta fine',
    'Der Clip beginnt am Abspielkopf (Taste I).':
        'La clip inizia alla testina (tasto I).',
    'Der Clip endet am Abspielkopf (Taste O).':
        'La clip finisce alla testina (tasto O).',
    'Zur Marke ▸':
        'Al segno ▸',
    'Marken (F8)':
        'Segni (F8)',
    'Clip um Marke':
        'Clip intorno al segno',
    'Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der nächsten am Abspielkopf) und endet {after} s danach.':
        'La clip inizia {before} s prima del segno scelto (nessuno scelto: quello più vicino alla testina) e finisce {after} s dopo.',
    'Springt zur nächsten F8-Marke (Taste M).':
        'Salta al prossimo segno F8 (tasto M).',
    'Clip: {start} – {end} ({length} s)':
        'Clip: {start} – {end} ({length} s)',
    'Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows).':
        "Riproduci l'audio della registrazione insieme all'anteprima (Windows).",
    'Ton im Clip':
        'Audio nella clip',
    'Abspielkopf hierher':
        'Testina qui',
    'Als Custom Game':
        'Come partita personalizzata',
    'Als Killer-Runde':
        'Come round da Killer',
    'Als Survivor-Runde':
        'Come round da Sopravvissuto',
    'Ausblenden':
        'Nascondi',
    'Bild':
        'Immagine',
    'Clip beginnt hier':
        'La clip inizia qui',
    'Clip endet hier':
        'La clip finisce qui',
    'Dunkle Fläche dahinter':
        'Area scura dietro',
    'Grösse zurücksetzen':
        'Ripristina dimensione',
    'Standbild gespeichert: {file}':
        'Fermo immagine salvato: {file}',
    'Standbild hier speichern':
        'Salva un fermo immagine qui',
    'Standbild nicht gespeichert.':
        'Fermo immagine non salvato.',
    '{n} Runden löschen':
        'Elimina {n} round',
    'Grosser Editor …':
        'Editor grande …',
    'Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle und allen Tasten.':
        'Apre la clip in una finestra propria – con censura, un livello per ogni fonte audio e tutti i tasti.',
    'Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton.':
        'Chat vocale Discord – traccia OBS 3. Off = la clip non ha audio Discord.',
    'Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird).':
        'Il tuo microfono – traccia OBS 4 (solo se OBS lo registra).',
    'Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen).':
        'Livello di questa fonte nella clip (100 % = come registrato).',
    'Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen).':
        'Una sola traccia audio – per il mixaggio OBS registra con le tracce 1–4 (Impostazioni → Registrazioni).',
    'ohne Ton':
        'senza audio',
    'Ton neu gemischt':
        'audio rimixato',
    'Clip speichern':
        'Salva clip',
    'Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen.':
        'Scrive il taglio come MP4 nella cartella «Clips» accanto alle registrazioni.',
    'Clips-Ordner öffnen':
        'Apri cartella clip',
    'Öffnet den Ordner „Clips“ im Explorer.':
        'Apre la cartella «Clips» in Esplora file.',
    'Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau.':
        'File non leggibile o ffmpeg mancante – nessuna anteprima.',
    'Clips-Ordner nicht anlegbar: {error}':
        'Impossibile creare la cartella clip: {error}',
    'Schreibe {file} …':
        'Scrittura di {file} …',
    'Clip gespeichert: {file}':
        'Clip salvata: {file}',
    'Clip nicht gespeichert: {why}':
        'Clip non salvata: {why}',
    '(Sofort-Clip)':
        '(clip istantanea)',
    'Aufnahme schon am Ladebildschirm starten':
        'Avvia la registrazione alla schermata di caricamento',
    'Aufnahme-Laufwerk nicht angeschlossen':
        'Unità di registrazione non collegata',
    'Clip':
        'Clip',
    'DBD':
        'DBD',
    'Discord':
        'Discord',
    'F8 speichert die letzten Sekunden als Sofort-Clip':
        'F8 salva gli ultimi secondi come clip istantanea',
    'Kein Sofort-Clip: {why}':
        'Nessuna clip istantanea: {why}',
    'Ladebildschirm vorbei – das Match beginnt.':
        'Schermata di caricamento finita – la partita inizia.',
    'Mikrofon':
        'Microfono',
    'Spiel':
        'Gioco',
    'Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner':
        'Registrazione – dalla fine della schermata di caricamento, in attesa del banner della mappa',
    'Nimmt die Runde auf (seit dem Ladebildschirm)':
        'Registrazione del round (dalla schermata di caricamento)',
    'OBS hat den Puffer nicht gespeichert':
        'OBS non ha salvato il buffer',
    'Sofort-Clip gespeichert ({n} s): {file}':
        'Clip istantanea salvata ({n} s): {file}',
    'Ton in OBS einstellen, sobald DBD startet:':
        "Imposta l'audio in OBS appena DBD si avvia:",
    'Ton in OBS nicht eingestellt: {error}':
        'Audio in OBS non impostato: {error}',
    'OBS bereit – Runden werden aufgenommen. {problem}':
        'OBS pronto – i round vengono registrati. {problem}',
    'Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)':
        "Per il mix audio nell'editor di clip, in OBS: Impostazioni → Uscita → Modalità di uscita «Avanzata» → scheda Registrazione → spunta le tracce audio da 1 a 5 (1 tutto, 2 gioco, 3 Discord, 4 microfono, 5 sottofondo)",
    'Jede Tonquelle auf eine eigene OBS-Tonspur':
        'Ogni fonte audio su una propria traccia OBS',
    'Dafür in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken. Das Programm prüft das beim DBD-Start und meldet es im Kasten „Aufnahmen mit OBS“; es ändert nichts am OBS-Profil.':
        "Per farlo, in OBS: Impostazioni → Uscita → Modalità di uscita «Avanzata» → scheda Registrazione → spunta le tracce audio da 1 a 5. Il programma lo controlla all'avvio di DBD e lo segnala nella scheda «Registrazioni con OBS»; non cambia nulla nel profilo di OBS.",
    'Sofort-Clip (F8) mit Ton von:':
        'Clip istantanea (F8) con audio da:',
    'Wie bei Medal: Das Programm weist in OBS jede Tonquelle der Spur 1 (alles – spielt in jedem Player) und ihrer eigenen Spur zu: nur DBD 2, Discord 3, Mikrofon 4, alle anderen Tonquellen in OBS (z. B. Spotify, Browser) 5 = Hintergrund. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt deshalb nur auf Spur 1. Im Clip-Editor schaltest du jede Quelle an oder aus und regelst ihre Lautstärke; beim Speichern mischt ffmpeg sie zusammen. OBS schreibt die Spuren nur im Ausgabemodus „Erweitert“ mit Audiospur 1 bis 5 angehakt (MKV oder MP4, nicht FLV); das Programm prüft das beim DBD-Start und meldet es, ändert aber nichts am OBS-Profil. Aus = Spuren bleiben, wie sie in OBS stehen.':
        "Come Medal: il programma assegna ogni fonte audio in OBS alla traccia 1 (tutto – si riproduce in qualsiasi lettore) e a una traccia propria: solo DBD 2, Discord 3, microfono 4, ogni altra fonte audio in OBS (ad es. Spotify, browser) 5 = sottofondo. L'audio desktop di Windows contiene anche DBD e Discord e per questo sta solo sulla traccia 1. Nell'editor di clip attivi o disattivi ogni fonte e ne imposti il livello; ffmpeg le mixa al salvataggio. OBS scrive le tracce solo in modalità di uscita «Avanzata» con le tracce audio da 1 a 5 spuntate (MKV o MP4, non FLV); il programma lo controlla all'avvio di DBD e lo segnala, ma non cambia nulla nel profilo di OBS. Off = le tracce restano come impostate in OBS.",
    'Nur der Ton von DBD im Sofort-Clip.':
        "Solo l'audio di DBD nella clip istantanea.",
    'Ton von Discord (Sprachchat) in der Aufnahme bzw. im Sofort-Clip.':
        'Audio di Discord (chat vocale) nella registrazione o nella clip istantanea.',
    'Dein Mikrofon – die Quelle „Mikrofon/AUX“ in OBS bzw. seine Spur im Sofort-Clip.':
        'Il tuo microfono – la fonte «Mic/Aux» in OBS, o la sua traccia nella clip istantanea.',
    'Hintergrund':
        'Sottofondo',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.':
        "Altri programmi con una propria fonte audio in OBS (ad es. Spotify, browser) – traccia OBS 5. L'audio desktop di Windows contiene anche DBD e Discord e sta solo sulla traccia 1.",
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) im Sofort-Clip – OBS-Spur 5.':
        'Altri programmi con una propria fonte audio in OBS (ad es. Spotify, browser) nella clip istantanea – traccia OBS 5.',
    'Tonquelle angelegt: {name}':
        'Fonte audio creata: {name}',
    'Farming-Aufnahmen löschen nach':
        'Elimina le registrazioni di farming dopo',
    'nie':
        'mai',
    '{n} Tagen':
        '{n} giorni',
    'Alte Farming-Aufnahmen gelöscht (älter als {days} Tage): {n}':
        'Vecchie registrazioni di farming eliminate (più vecchie di {days} giorni): {n}',
    '{name} – keine Quelle':
        '{name} – nessuna fonte',
    '{name} – in OBS aus':
        '{name} – disattivata in OBS',
    'In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf Spur 5.':
        'OBS non aveva una fonte di sottofondo per questa registrazione. Per Spotify, il browser e simili aggiungi in OBS una cattura audio applicazione per programma – il programma la mette sulla traccia 5.',
    'Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen ausgeschaltet.':
        'Questa fonte audio era disattivata in Impostazioni → Registrazioni quando è stata fatta la registrazione.',
    'Tonquelle {name} hört jetzt auf {exe}':
        'La fonte audio {name} ora ascolta {exe}',
    'Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}':
        'Sulla traccia 5 (sottofondo) invece che con gioco/Discord/microfono: {names}',
    'Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.':
        'Sulla traccia {n} non si sente nulla in tutta la registrazione.',
    'Tonquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'Fonte audio aggiunta alla scena «{scene}»: {name}',
    'Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'Fonte audio mostrata di nuovo nella scena «{scene}»: {name}',
    '{name} (Spur {n})':
        '{name} (traccia {n})',
    'Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.':
        'Muto in questa registrazione: {names} – OBS non ha registrato nulla lì. Controlla in OBS: fonte nella scena registrata, non silenziata, traccia spuntata.',
    '{name} – still':
        '{name} – muto',
    'Nur der Ton von Dead by Daylight – OBS-Spur 2.':
        "Solo l'audio di Dead by Daylight – traccia OBS 2.",
    'Unbekannte Map':
        'Mappa sconosciuta',
    'Wiederholungspuffer in OBS läuft nicht':
        'Il buffer di replay di OBS non è attivo',
    'Übriger Desktop-Ton':
        'Altro audio desktop',
    'Das Map-Banner kommt erst einige Sekunden nach dem Spawn. Mit diesem Häkchen startet OBS schon, wenn der Ladebildschirm nach der Lobby endet – ohne Lobby, mit Spawn. Das Banner benennt die Aufnahme danach. Kommt 3 Minuten lang kein Banner, endet die Aufnahme und heisst „Unbekannte Map“.':
        'Il banner della mappa arriva qualche secondo dopo lo spawn. Con questa casella OBS parte appena finisce la schermata di caricamento dopo la lobby – niente lobby, con lo spawn. Il banner dà poi il nome alla registrazione. Senza banner per 3 minuti la registrazione termina e si chiama «Mappa sconosciuta».',
    'F8 sichert den Wiederholungspuffer von OBS und legt die letzten Sekunden als MP4 in den Ordner „Clips“ – Bild ohne Neukodierung, in Sekunden. Spur 1 ist die unten gewählte Tonmischung (spielt überall), dahinter liegen die Einzelspuren des Puffers für den Clip-Editor. Der Wiederholungspuffer muss in OBS eingerichtet sein. Die Marke in der Rundenaufnahme setzt F8 weiterhin.':
        "F8 salva il buffer di replay di OBS e mette i suoi ultimi secondi come MP4 nella cartella «Clips» – immagine senza ricodifica, pochi secondi di lavoro. La traccia 1 è il mix audio scelto sotto (si riproduce ovunque), dietro ci sono le tracce del buffer per l'editor di clip. Il buffer di replay va configurato in OBS. F8 imposta comunque il segno nella registrazione del round.",
    'Das Programm legt in der aktuellen OBS-Szene je eine Anwendungs-Audioaufnahme für DBD und Discord an (einmalig) und schaltet die Tonquellen wie gewählt stumm oder laut – beim Start von DBD und bei jeder Änderung hier, auch mitten in der Runde. Aufnehmen tut OBS, das Programm fasst DBD nicht an. Braucht OBS 28 oder neuer.':
        "Il programma crea nella scena OBS attuale una cattura audio applicazione ciascuna per DBD e Discord (una volta) e silenzia o riattiva le fonti audio come scelto – all'avvio di DBD e a ogni modifica qui, anche a metà round. La cattura la fa OBS, il programma non tocca DBD. Richiede OBS 28 o più recente.",
    'Ton des Spiels in der Aufnahme.':
        "L'audio del gioco nella registrazione.",
    'Alles andere, was am PC zu hören ist (Musik, Browser, Systemtöne) – die Quelle „Desktop-Audio“ in OBS.':
        'Tutto il resto che senti sul PC (musica, browser, suoni di sistema) – la fonte «Audio desktop» di OBS.',
    'Als Farming markieren':
        'Segna come farming',
    'Grund':
        'Motivo',
    'Ist Farming':
        'È farming',
    'Kein Farming':
        'Non è farming',
    'Alle als Farming':
        'Tutti come farming',
    'Alle ignorieren':
        'Ignora tutti',
    'Custom Game, laut Stats-Seite öffentlich':
        'Partita personalizzata, pubblica sulla pagina statistiche',
    'kurze Serie, gleicher Gegner':
        'partita breve, stesso avversario',
    '{n} Runden bleiben normale Runden (kein Farming).':
        '{n} round restano round normali (non farming).',
    'Markiert alle Runden der Liste als Farming-Runden (mit Rückfrage) – wie „Ist Farming“ für jede.':
        "Segna ogni round dell'elenco come round di farming (prima chiede) – come «È farming» per ciascuno.",
    'Keine der Runden der Liste mehr vorschlagen – sie bleiben, wie sie sind.':
        "Non suggerire mai più alcun round dell'elenco – restano come sono.",
    'Die markierten Runden der Liste sind Farming-Runden (und kein Custom Game mehr); ihre Aufnahmen wandern in den Ordner „Farming“. Zurück: „Farming an/aus“ unter „Letzte Runden“.':
        "I round selezionati dell'elenco sono round di farming (e non più partite personalizzate); le loro registrazioni vanno nella cartella «Farming». Per tornare indietro: «Farming on/off» in «Ultimi round».",
    'Die markierten Runden der Liste sind normale Runden – sie bleiben, wie sie sind, und werden nie wieder vorgeschlagen.':
        "I round selezionati dell'elenco sono round normali – restano come sono e non vengono mai più suggeriti.",
    'Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB.':
        'Discord: 10 MB senza Nitro, Nitro Basic 50 MB, Nitro 500 MB.',
    'Format':
        'Formato',
    'Für Discord (passt unter die Zielgrösse)':
        'Per Discord (sta sotto la dimensione obiettivo)',
    'Gespeichert: {file} ({mb} MB)':
        'Salvata: {file} ({mb} MB)',
    'Ignorieren':
        'Ignora',
    'Runden nicht geändert: {error}':
        'Round non modificati: {error}',
    'Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück.':
        'Riproduce esattamente la clip e poi torna al suo inizio.',
    'Zeigt den zuletzt gespeicherten Clip im Explorer.':
        "Mostra in Esplora file l'ultima clip salvata.",
    '{n} Runden als Farming markiert.':
        '{n} round segnati come farming.',
    '{n} Runden als Farming-Runden markieren?':
        'Segnare {n} round come round di farming?',
    '{n} Runden sehen nach Farming aus: {reasons}. Zuletzt: {map}, {when}.':
        '{n} round sembrano farming: {reasons}. Il più recente: {map}, {when}.',
    '{n} als Custom Game gespeichert, laut Stats-Seite aber öffentliche Matches (vor 1.5.5 so erkannt)':
        '{n} salvati come partite personalizzate ma partite pubbliche sulla pagina statistiche (letti così prima della 1.5.5)',
    '{n} kurze Runden (bis 3 min) hintereinander gegen denselben Charakter':
        '{n} round brevi (fino a 3 min) di fila contro lo stesso personaggio',
    'Farming?':
        'Farming?',
    'Runden sehen nach Farming aus':
        'round sembrano farming',
    'Farming prüfen …':
        'Controlla farming …',
    'Öffnet die Statistik-Übersicht mit der Zeile, die sagt, warum diese Runden nach Farming aussehen – dort markieren oder ignorieren.':
        'Apre la panoramica delle statistiche con la riga che spiega perché questi round sembrano farming – segnali o ignorali lì.',
    'etwa {mb} MB':
        'circa {mb} MB',
    'wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB':
        'diventa {h}p {fps} fps, ≈ {kbps} kbit/s, sotto {mb} MB',
    '≤ {n} MB':
        '≤ {n} MB',
    '▶ Clip ansehen':
        '▶ Guarda clip',
    'Markiert alle genannten Runden als Farming-Runden (und nicht mehr als Custom Game); ihre Aufnahmen wandern in den Ordner „Farming“. Einzeln zurück: „Farming an/aus“ unter „Letzte Runden“.':
        'Segna tutti questi round come round di farming (non più partite personalizzate); le loro registrazioni vanno nella cartella «Farming». Per tornare indietro uno alla volta: «Farming on/off» in «Ultimi round».',
    'Diese Runden nicht mehr vorschlagen – sie bleiben, wie sie sind.':
        'Non suggerire più questi round – restano come sono.',
    'Alle':
        'Tutti',
    'BP/h':
        'BP/h',
    'BP/h mit Wartezeit':
        'BP/h con attesa',
    'Bloodpoints':
        'Punti Sangue',
    'Bloodpoints laut Stats-Seite. BP/h = je Stunde im Match; mit Wartezeit = je Stunde aus Match und Suche zusammen. Was das Farmen allein bringt, steht im Reiter „Farming“; „Farming ausblenden“ rechnet hier ohne Farming-Runden.':
        "Punti Sangue dalla pagina statistiche. BP/h = all'ora di partita; con attesa = all'ora di partita e ricerca insieme. Quanto rende il solo farming è nella scheda «Farming»; «Nascondi farming» esclude qui i round di farming.",
    'Bloodpoints pro Stunde':
        "Punti Sangue all'ora",
    'Summe':
        'Totale',
    'mit Wartezeit {bp}':
        'con attesa {bp}',
    'Rekorde':
        'Record',
    'Serien zählen Runden mit Ergebnis laut Stats-Seite in zeitlicher Reihenfolge – „aktuell“ ist die Serie der neuesten Runden der Auswahl. Beste Woche ab {n} Runden mit Ergebnis. Eine Sitzung endet nach 45 Minuten ohne Runde.':
        'Le serie contano i round con un risultato dalla pagina statistiche in ordine di tempo – «attuale» è la serie dei round più recenti della selezione. Settimana migliore da {n} round con un risultato. Una sessione finisce dopo 45 minuti senza round.',
    'Noch keine Runden in dieser Auswahl.':
        'Ancora nessun round in questa selezione.',
    'aktuell {n}':
        'attuale {n}',
    'zuletzt {date}':
        'ultima {date}',
    '4K-Serie':
        'Serie di 4K',
    'Ø {kills} Kills · {n} Runden als {killer}':
        'Ø {kills} uccisioni · {n} round come {killer}',
    '{share} entkommen · {n} Runden gegen {killer}':
        '{share} fughe · {n} round contro {killer}',
    '4K-Serie {n}':
        'Serie di 4K {n}',
    'Entkommen-Serie {n}':
        'Serie di fughe {n}',
    'Entkommen-Serie':
        'Serie di fughe',
    'Beste Woche als Killer':
        'Settimana migliore da Killer',
    'ab {date} · {n} Runden':
        'dal {date} · {n} round',
    'ab {n} Killer-Runden in einer Woche':
        'da {n} round da Killer in una settimana',
    'Beste Woche als Survivor':
        'Settimana migliore da Sopravvissuto',
    'ab {n} Survivor-Runden in einer Woche':
        'da {n} round da Sopravvissuto in una settimana',
    'Meiste Runden an einem Tag':
        'Più round in un giorno',
    'Längste Sitzung':
        'Sessione più lunga',
    'Längste Runde':
        'Round più lungo',
    'Spielstatus in Discord anzeigen (Rich Presence)':
        'Mostra lo stato di gioco in Discord (Rich Presence)',
    'Application-ID':
        'ID applicazione',
    'Discord testen':
        'Prova Discord',
    'Developer-Portal öffnen':
        'Apri portale sviluppatori',
    'Killer in Discord anzeigen':
        'Mostra il Killer in Discord',
    'Auch Lobby, Suche und Menü anzeigen':
        'Mostra anche lobby, ricerca e menu',
    'Zeigt in deinem Discord-Status, was gerade läuft: „Nurse auf Coal Tower“ mit Rundenzeit, in der Lobby „Sucht ein Match“. Discord braucht dafür eine Application-ID: im Developer-Portal „New Application“ anlegen (als Name z. B. „Dead by Daylight“ – so steht es im Status), die Application-ID kopieren und hier eintragen. Das Programm spricht nur mit dem Discord-Client auf diesem PC (lokale Pipe), ohne ID wird nichts gesendet; Discord erfährt nur Map, Rolle, Killer und die Startzeit.':
        'Mostra nel tuo stato Discord cosa succede: «Nurse su Coal Tower» con la durata del round, nella lobby «Cerca una partita». Per questo Discord richiede un ID applicazione: crea una «New Application» nel portale sviluppatori (chiamala ad es. «Dead by Daylight» – è ciò che mostra lo stato), copia il suo Application ID e inseriscilo qui. Il programma parla solo con il client Discord su questo PC (pipe locale); senza ID non viene inviato nulla; Discord apprende solo mappa, ruolo, Killer e ora di inizio.',
    'Verbinde mit Discord …':
        'Connessione a Discord …',
    'Discord nicht gefunden – läuft es?':
        'Discord non trovato – è in esecuzione?',
    'Killer · {killer}':
        'Killer · {killer}',
    'Im Match':
        'In partita',
    'Sucht ein Match':
        'Cerca una partita',
    'In der Lobby':
        'Nella lobby',
    'Bereit machen':
        'In preparazione',
    'Im Menü':
        'Nel menu',
    'Discord: aus':
        'Discord: disattivato',
    'Discord: Fehler – {error}':
        'Discord: errore – {error}',
    'Application-ID fehlt – im Developer-Portal anlegen und hier eintragen.':
        'ID applicazione mancante – creane uno nel portale sviluppatori e inseriscilo qui.',
    'Ungültige Application-ID ({error})':
        'ID applicazione non valido ({error})',
    'Discord: verbunden':
        'Discord: connesso',
    'Als Killer steht dein Killer im Status („Killer · The Nurse“); aus = nur „Killer“.':
        "Da Killer nello stato c'è il tuo Killer («Killer · The Nurse»); off = solo «Killer».",
    'Aus = der Status erscheint nur während einer Runde; sonst auch „Sucht ein Match“, „In der Lobby“ und „Im Menü“, solange DBD läuft.':
        'Off = lo stato compare solo durante un round; altrimenti anche «Cerca una partita», «Nella lobby» e «Nel menu» mentre DBD è in esecuzione.',
    'Dein Discord-Status zeigt Map, Rolle, Killer und die Rundenzeit (in der Lobby: Suche/Lobby). Braucht eine Application-ID aus dem Discord-Developer-Portal; das Programm spricht nur mit dem Discord-Client auf diesem PC.':
        'Il tuo stato Discord mostra mappa, ruolo, Killer e durata del round (nella lobby: ricerca/lobby). Richiede un ID applicazione dal portale sviluppatori di Discord; il programma parla solo con il client Discord su questo PC.',
    'Verbindet sich einmal mit dem laufenden Discord und zeigt, ob die Application-ID angenommen wird.':
        "Si connette una volta al Discord in esecuzione e mostra se l'ID applicazione viene accettato.",
    'Öffnet discord.com/developers im Browser: „New Application“ anlegen (Name z. B. „Dead by Daylight“), die Application-ID kopieren und links eintragen.':
        'Apre discord.com/developers nel browser: crea una «New Application» (nome ad es. «Dead by Daylight»), copia il suo Application ID e inseriscilo a sinistra.',
    'Ø pro Runde':
        'Ø per round',
    'BP/h im Match':
        'BP/h in partita',
    'Spielzeit laut Stats-Seite':
        'tempo di gioco dalla pagina statistiche',
    'Match und Suche zusammen':
        'partita e ricerca insieme',
    'Beste Runde':
        'Round migliore',
    'Ø BP als Killer':
        'Ø BP da Killer',
    'Ø BP als Survivor':
        'Ø BP da Sopravvissuto',
    '{when}: Ø {bp} BP · {n} Runden · Summe {sum}':
        '{when}: Ø {bp} BP · {n} round · totale {sum}',
    'Ø Bloodpoints pro Runde {per}':
        'Ø Punti Sangue per round {per}',
    'Keine Runden mit Bloodpoints in dieser Auswahl.':
        'Nessun round con Punti Sangue in questa selezione.',
    'Verpixelt':
        'Pixelato',
    'Verwischt':
        'Sfocato',
    'Schwarz':
        'Nero',
    'Zensieren':
        'Censura',
    'Beim Speichern anwenden':
        'Applica al salvataggio',
    'Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das Bild neu kodiert, auch im Format „Schnell“).':
        "I riquadri vengono nascosti nella clip salvata (per questo l'immagine viene ricodificata, anche nel formato «Veloce»).",
    'Kasten zeichnen':
        'Disegna riquadro',
    'Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug.':
        "Trascina un'area sull'immagine; i riquadri si possono spostare e ridimensionare dall'angolo in basso a destra. Premi di nuovo per terminare lo strumento.",
    'Namen links unten':
        'Nomi in basso a sinistra',
    'Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        "Mette un riquadro dove DBD mostra i nomi dei Sopravvissuti (in basso a sinistra nell'immagine di gioco) – spostalo se serve.",
    'Kasten entfernen':
        'Rimuovi riquadro',
    'Entfernt den markierten Kasten (Taste Entf).':
        'Rimuove il riquadro selezionato (tasto Del).',
    'Alle entfernen':
        'Rimuovi tutti',
    'Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ lässt dich einen aufziehen.':
        'Ancora nessun riquadro. «Nomi in basso a sinistra» ne mette uno sui nomi dei Sopravvissuti, «Disegna riquadro» ti fa trascinarne uno.',
    '{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.':
        '{n} riquadri – trascina = sposta, angolo in basso a destra = dimensione, clic = seleziona.',
    '{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.':
        '{n} riquadri memorizzati – valgono anche per la prossima clip.',
    'mit Zensur neu kodiert (wie „Genau“)':
        'ricodificata per la censura (come «Preciso»)',
    'Retusche (aus der Umgebung übermalt)':
        'Ritocco (coperto con i dintorni)',
    'Spotify':
        'Spotify',
    '„Als nächstes“ aus Spotify in der Musikkarte zeigen':
        'Mostra «Prossimi brani» di Spotify sulla scheda musicale',
    'Client-ID':
        'Client ID',
    'Developer-Dashboard öffnen':
        'Apri dashboard sviluppatori',
    'Mit Spotify verbinden':
        'Connetti a Spotify',
    'Spotify-Verbindung trennen':
        'Disconnetti Spotify',
    'Spotify: öffne die Anmeldung im Browser …':
        "Spotify: apertura dell'accesso nel browser …",
    'YouTube':
        'YouTube',
    'Privat':
        'Privato',
    'Nicht gelistet':
        'Non in elenco',
    'Öffentlich':
        'Pubblico',
    'Client-Secret':
        'Client secret',
    'Sichtbarkeit':
        'Visibilità',
    'Clips automatisch auf YouTube hochladen':
        'Carica clip su YouTube automaticamente',
    'Google Cloud Console öffnen':
        'Apri console Google Cloud',
    'Client-Datei laden …':
        'Carica file client …',
    'Client-Datei laden':
        'Carica file client',
    'Client-Datei von Google laden':
        'Carica il file client di Google',
    'Das ist keine Client-Datei von Google ({error}).':
        'Questo non è un file client di Google ({error}).',
    'YouTube: Client-ID und Client-Secret aus {file} übernommen – jetzt „Mit YouTube verbinden“ klicken.':
        'YouTube: client ID e client secret presi da {file} – ora fai clic su «Connetti a YouTube».',
    'YouTube: Client-Daten aus {file} übernommen.':
        'YouTube: dati client presi da {file}.',
    'Datei zu gross':
        'file troppo grande',
    'nicht lesbar: {error}':
        'non leggibile: {error}',
    'kein JSON: {error}':
        'non è JSON: {error}',
    'kein JSON-Objekt':
        'non è un oggetto JSON',
    'OAuth-Client vom Typ „Webanwendung“ – in der Cloud Console einen vom Typ „Desktop-App“ anlegen':
        'Client OAuth di tipo «Applicazione web» – creane uno di tipo «App desktop» nella console Cloud',
    'kein Abschnitt „installed“':
        'nessuna sezione «installed»',
    'Client-ID fehlt oder endet nicht auf .apps.googleusercontent.com':
        'client ID mancante o non termina con .apps.googleusercontent.com',
    'Client-Secret fehlt':
        'client secret mancante',
    'Mit YouTube verbinden':
        'Connetti a YouTube',
    'YouTube-Verbindung trennen':
        'Disconnetti YouTube',
    'Auf YouTube hochladen':
        'Carica su YouTube',
    'YouTube-Link kopieren':
        'Copia link YouTube',
    'Auf YouTube öffnen':
        'Apri su YouTube',
    'YouTube: Client-ID (…apps.googleusercontent.com) und Client-Secret eintragen.':
        'YouTube: inserisci il client ID (…apps.googleusercontent.com) e il client secret.',
    'YouTube: öffne die Anmeldung im Browser …':
        "YouTube: apertura dell'accesso nel browser …",
    'Hochgeladen: {file}':
        'Caricato: {file}',
    'YouTube: nicht hochgeladen – {file}: {why}':
        'YouTube: non caricato – {file}: {why}',
    'YouTube: in die Warteschlange – {file}':
        'YouTube: in coda – {file}',
    'YouTube-Link kopiert: {url}':
        'Link YouTube copiato: {url}',
    'Clip: {what}':
        'Clip: {what}',
    'Dauer {d}':
        'Durata {d}',
    'Aufgenommen mit Fog Scout':
        'Registrato con Fog Scout',
    'keine Upload-Sitzung erhalten':
        'nessuna sessione di caricamento ricevuta',
    'Antwort ohne Video-ID':
        'risposta senza ID video',
    'nicht angemeldet':
        'non connesso',
    'Datei nicht gefunden':
        'file non trovato',
    'Aufnahmeordner nicht da':
        'cartella registrazioni non presente',
    'YouTube: aus':
        'YouTube: disattivato',
    'YouTube: nicht verbunden – „Mit YouTube verbinden“ klicken.':
        'YouTube: non connesso – fai clic su «Connetti a YouTube».',
    'Mit YouTube verbunden – du kannst dieses Fenster schliessen.':
        'Connesso a YouTube – puoi chiudere questa finestra.',
    'Google hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        "Google ha rifiutato l'accesso – puoi chiudere questa finestra.",
    'YouTube: Anmeldung nicht möglich – {error}':
        'YouTube: accesso non possibile – {error}',
    'YouTube: Browser nicht geöffnet – {error}':
        'YouTube: browser non aperto – {error}',
    'YouTube: Anmeldung abgelehnt ({error})':
        'YouTube: accesso rifiutato ({error})',
    'YouTube: Google gab kein dauerhaftes Token – in der Cloud Console den OAuth-Client als „Desktop“ anlegen und den Zustimmungsbildschirm veröffentlichen.':
        'YouTube: Google non ha fornito un token duraturo – crea il client OAuth come «App desktop» nella console Cloud e pubblica la schermata di consenso.',
    'YouTube: verbunden':
        'YouTube: connesso',
    'YouTube: Anmeldung abgelaufen – noch einmal „Mit YouTube verbinden“ klicken.':
        'YouTube: accesso scaduto – fai clic ancora una volta su «Connetti a YouTube».',
    'YouTube: {n} in der Warteschlange – wartet, bis Lobby und Runde vorbei sind':
        'YouTube: {n} in coda – in attesa che lobby e round siano finiti',
    'YouTube: {n} in der Warteschlange – Tageskontingent aufgebraucht, weiter ab {when}':
        'YouTube: {n} in coda – quota giornaliera esaurita, continua alle {when}',
    'YouTube: lädt {file} hoch ({pct} %)':
        'YouTube: caricamento di {file} ({pct} %)',
    'YouTube: hochgeladen – {file}':
        'YouTube: caricato – {file}',
    'YouTube: {error} – neuer Versuch in {s} s':
        'YouTube: {error} – nuovo tentativo tra {s} s',
    'YouTube: {n} in der Warteschlange – {why}':
        'YouTube: {n} in coda – {why}',
    'Uploads in Playlists einsortieren':
        'Ordina i caricamenti in playlist',
    'Playlists laden':
        'Carica playlist',
    'Clips in':
        'Clip in',
    'Runden in':
        'Round in',
    'YouTube: lade Playlists …':
        'YouTube: caricamento playlist …',
    'YouTube: zuerst „Uploads in Playlists einsortieren“ anhaken.':
        'YouTube: spunta prima «Ordina i caricamenti in playlist».',
    'YouTube: {n} Playlists geladen – im Kasten auswählen':
        'YouTube: {n} playlist caricate – sceglile nella casella',
    'YouTube: keine Playlists auf dem Kanal – zuerst auf YouTube eine anlegen':
        'YouTube: nessuna playlist sul canale – creane prima una su YouTube',
    'YouTube: Playlists nicht geladen – {why}':
        'YouTube: playlist non caricate – {why}',
    'YouTube: {file} in Playlist „{name}“ einsortiert':
        'YouTube: {file} inserito nella playlist «{name}»',
    'YouTube: {file} hochgeladen, aber nicht in die Playlist – {why}':
        'YouTube: {file} caricato, ma non nella playlist – {why}',
    'Berechtigung fehlt – noch einmal „Mit YouTube verbinden“ klicken':
        'permesso mancante – fai clic ancora una volta su «Connetti a YouTube»',
    'YouTube: verbunden – für Playlists einmal neu „Mit YouTube verbinden“ klicken.':
        'YouTube: connesso – per le playlist fai clic ancora una volta su «Connetti a YouTube».',
    'Nach dem Upload kommt jedes Video in die gewählte Playlist – für Clips und Runden getrennt wählbar, beide dürfen dieselbe sein. Braucht bei Google die Berechtigung „YouTube-Konto verwalten“ statt nur „Videos hochladen“: nach dem Anhaken einmal neu „Mit YouTube verbinden“. Das Programm nutzt davon nur Playlists auflisten und Video einsortieren (50 Einheiten je Video; es bleiben sechs Uploads am Tag).':
        'Dopo il caricamento ogni video va nella playlist scelta – separatamente per clip e round, possono anche essere la stessa. Richiede il permesso di Google «Gestire il tuo account YouTube» invece del solo «Caricare video»: dopo averla spuntata, fai clic ancora una volta su «Connetti a YouTube». Il programma lo usa solo per elencare le playlist e inserirvi un video (50 unità per video; restano sei caricamenti al giorno).',
    'Holt die Liste deiner Playlists von YouTube (1 Einheit) in die beiden Auswahlfelder. Neue Playlists legst du auf YouTube an und lädst die Liste danach neu.':
        "Recupera da YouTube l'elenco delle tue playlist (1 unità) nelle due scelte. Le nuove playlist le crei su YouTube, poi carichi di nuovo l'elenco.",
    'YouTube: Fehler – {error}':
        'YouTube: errore – {error}',
    'Jeder neue Clip (F8 und aus dem Editor) kommt in die Warteschlange und geht auf deinen Kanal, sobald du weder in einer Lobby noch in einer Runde bist – mit der Sichtbarkeit rechts, Standard privat. Runden lädst du nur auf Wunsch hoch (Rechtsklick unter Aufnahmen). Google erlaubt etwa sechs Uploads am Tag, der Rest wartet bis zum nächsten Tag. Die Datei bleibt auf der Platte.':
        "Ogni nuova clip (F8 e dall'editor) entra in coda e va sul tuo canale appena non sei né in una lobby né in un round – con la visibilità a destra, privata per impostazione predefinita. I round vengono caricati solo su richiesta (clic destro in Registrazioni). Google consente circa sei caricamenti al giorno, il resto aspetta il giorno dopo. Il file resta sul disco.",
    'Öffnet die Anmeldedaten der Google Cloud Console im Browser: Projekt anlegen, „YouTube Data API v3“ aktivieren, OAuth-Client „Desktop-App“ erstellen, Client-ID und -Secret hier einfügen.':
        'Apre nel browser la pagina delle credenziali della console Google Cloud: crea un progetto, attiva «YouTube Data API v3», crea un client OAuth «App desktop», incolla qui client ID e secret.',
    'Vergisst die Google-Freigabe auf diesem PC; die Warteschlange wartet, bis du dich neu verbindest. In deinem Google-Konto unter Sicherheit → Drittanbieter-Apps lässt sich der Zugriff ebenfalls entfernen.':
        "Dimentica il consenso Google su questo PC; la coda aspetta finché non ti connetti di nuovo. Nel tuo account Google in Sicurezza → App di terze parti puoi anche rimuovere l'accesso.",
    'Die markierte Datei in die YouTube-Warteschlange (Sichtbarkeit wie in den Einstellungen, Standard privat). Hochgeladen wird, sobald du weder in einer Lobby noch in einer Runde bist und das Tageskontingent reicht; der Link erscheint danach im Rechtsklick-Menü.':
        'Il file selezionato nella coda di YouTube (visibilità come nelle impostazioni, privata per impostazione predefinita). Caricato appena non sei né in una lobby né in un round e la quota giornaliera lo consente; il link compare poi nel menu del clic destro.',
    'Spotify: Client-ID sieht falsch aus – erwartet werden 32 Zeichen aus 0–9 und a–f (Dashboard → deine App → Settings → Basic Information → Client ID).':
        'Spotify: il Client ID sembra sbagliato – sono previsti 32 caratteri tra 0–9 e a–f (dashboard → la tua app → Settings → Basic Information → Client ID).',
    'ALS NÄCHSTES':
        'PROSSIMI',
    'Unter dem Lied':
        'Sotto il brano',
    'Rechts neben dem Lied':
        'A destra del brano',
    'Als nächstes':
        'Prossimi brani',
    'Anzahl Titel':
        'Brani mostrati',
    'Die Liste kommt aus Spotify – einrichten unter Einstellungen → Verbindungen → Spotify.':
        "L'elenco arriva da Spotify – configuralo in Impostazioni → Connessioni → Spotify.",
    'Spotify: aus':
        'Spotify: disattivato',
    'Spotify: Client-ID fehlt – im Developer-Dashboard anlegen und hier eintragen.':
        'Spotify: Client ID mancante – crealo nella dashboard sviluppatori e inseriscilo qui.',
    'Spotify: nicht verbunden – „Mit Spotify verbinden“ klicken.':
        'Spotify: non connesso – fai clic su «Connetti a Spotify».',
    'Spotify: Anmeldung im Browser offen – dort bei Spotify anmelden und zustimmen …':
        'Spotify: accesso aperto nel browser – accedi lì a Spotify e acconsenti …',
    'Spotify: Port {port} ist belegt – Anmeldung nicht möglich.':
        'Spotify: la porta {port} è occupata – accesso non possibile.',
    'Spotify: Browser konnte nicht geöffnet werden ({error})':
        'Spotify: impossibile aprire il browser ({error})',
    'Spotify: Anmeldung fehlgeschlagen ({error})':
        'Spotify: accesso non riuscito ({error})',
    'Spotify: Anmeldung abgelehnt ({error})':
        'Spotify: accesso rifiutato ({error})',
    'Spotify: keine Antwort vom Browser – Anmeldung abgebrochen.':
        'Spotify: nessuna risposta dal browser – accesso annullato.',
    'Spotify: verbunden':
        'Spotify: connesso',
    'Spotify: Anmeldung abgelaufen – bitte neu verbinden.':
        'Spotify: accesso scaduto – connettiti di nuovo.',
    'Spotify: kein Zugriff ({error}) – ist dein Spotify-Konto in der Developer-App unter „User Management“ eingetragen?':
        "Spotify: nessun accesso ({error}) – il tuo account Spotify è elencato nell'app sviluppatore in «User Management»?",
    'Spotify: Fehler – {error}':
        'Spotify: errore – {error}',
    'Spotify: Kontingent der Developer-App aufgebraucht – „Als nächstes“ pausiert bis {time}.':
        "Spotify: la quota dell'app sviluppatore è esaurita – «Prossimi brani» in pausa fino alle {time}.",
    'keine Antwort mit Token':
        'nessuna risposta con un token',
    'Mit Spotify verbunden – du kannst dieses Fenster schliessen.':
        'Connesso a Spotify – puoi chiudere questa finestra.',
    'Spotify hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        "Spotify ha rifiutato l'accesso – puoi chiudere questa finestra.",
    'Die nächsten Titel deiner Spotify-Warteschlange unter oder neben dem laufenden Lied. Braucht eine eigene App im Spotify-Developer-Dashboard (Client-ID) und einmal die Anmeldung im Browser; nur solange Spotify spielt.':
        'I prossimi brani della tua coda Spotify sotto o accanto al brano attuale. Richiede una tua app nella dashboard sviluppatori di Spotify (Client ID) e un accesso nel browser; solo mentre Spotify riproduce.',
    'Öffnet developer.spotify.com/dashboard im Browser: „Create app“, Redirect URI wie unten angegeben eintragen, die Client-ID kopieren und links einfügen.':
        "Apre developer.spotify.com/dashboard nel browser: «Create app», inserisci l'URI di reindirizzamento indicato sotto, copia il Client ID e incollalo a sinistra.",
    'Vergisst die Spotify-Freigabe auf diesem PC; die Liste verschwindet. In Spotify selbst lässt sich die App unter Konto → Apps ebenfalls entfernen.':
        "Dimentica il consenso Spotify su questo PC; l'elenco sparisce. In Spotify stesso puoi anche rimuovere l'app in Account → App.",
    'Alle Arten':
        'Tutti i tipi',
    'Art':
        'Tipo',
    'Clip abspielen':
        'Riproduci clip',
    'Clip im Editor öffnen …':
        "Apri clip nell'editor …",
    'Im Editor öffnen …':
        "Apri nell'editor …",
    'Datei kopieren (zum Einfügen)':
        'Copia file (da incollare)',
    'Zur Runde springen':
        'Vai al round',
    'Farming-Runde':
        'Round di farming',
    'Datei fehlt: {file}':
        'File mancante: {file}',
    '{file} kopiert – mit Strg+V z. B. in Discord einfügen.':
        '{file} copiato – incollalo con Ctrl+V, ad es. in Discord.',
    'Die Aufnahme dieser Runde gibt es nicht mehr.':
        "La registrazione di questo round non c'è più.",
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start.':
        'Manca ffmpeg (pacchetto imageio-ffmpeg) – start.bat lo installa al prossimo avvio.',
    'Öffnet den markierten Clip (auch Sofort-Clips von F8) im Clip-Editor: kürzen, zensieren, Ton mischen. Gespeichert wird ein neuer Clip, der alte bleibt.':
        "Apre la clip selezionata (anche le clip istantanee F8) nell'editor di clip: taglia, censura, mixa l'audio. Salva una nuova clip, quella vecchia resta.",
    'Clip fehlt: {file}':
        'Clip mancante: {file}',
    'Keine Videodatei: {file}':
        'Non è un file video: {file}',
    'Clip gelöscht: {file}':
        'Clip eliminata: {file}',
    'Clip im Explorer zeigen':
        'Mostra clip in Esplora file',
    'Clip löschen':
        'Elimina clip',
    'Clip nicht gelöscht ({error}): {file}':
        'Clip non eliminata ({error}): {file}',
    'Kein Aufnahmeordner – die Clips liegen in seinem Ordner „Clips“.':
        'Nessuna cartella registrazioni – le clip vengono conservate nella sua cartella «Clips».',
    'Länge':
        'Durata',
    'Noch keine Clips – „Clip bearbeiten …“ bei einer Runde oder F8 im Spiel.':
        'Ancora nessuna clip – «Modifica clip …» su un round, o F8 nel gioco.',
    'Sofort-Clip':
        'Clip istantanea',
    'Sofort-Clips (F8)':
        'Clip istantanee (F8)',
    'Standbild':
        'Fermo immagine',
    'Standbilder':
        'Fermi immagine',
    '{n} von {total} Clips':
        '{n} di {total} clip',
    'Spielt den markierten Clip im Standard-Player von Windows ab.':
        'Riproduce la clip selezionata nel lettore predefinito di Windows.',
    'Öffnet den Explorer mit dem markierten Clip.':
        'Apre Esplora file con la clip selezionata.',
    'Löscht den markierten Clip von der Platte – nach Rückfrage. Nur Dateien, die das Programm selbst angelegt hat.':
        "Elimina la clip selezionata dall'unità – dopo una conferma. Solo file creati dal programma stesso.",
    'Öffnet den Ordner „Clips“ neben den Aufnahmen im Explorer.':
        'Apre in Esplora file la cartella «Clips» accanto alle registrazioni.',
    'Clips':
        'Clip',
    'Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        'Linee grigie nelle barre = limiti (off) – trascinane una per attivarli',
    'mit kurzer Meldung':
        'con una breve notifica',
    'Clip wird gespeichert …':
        'Salvataggio clip …',
    'Die letzten {n} s aus dem Puffer von OBS':
        'Gli ultimi {n} s dal buffer di OBS',
    'Clip gespeichert ✓':
        'Clip salvata ✓',
    '{n} s · im Tab Aufnahmen → Clips':
        '{n} s · nella scheda Registrazioni → Clip',
    'Kein Clip':
        'Nessuna clip',
    'Zeigt beim Sofort-Clip (F8) unten rechts ein kleines Hinweisfenster – „Clip wird gespeichert …“ und danach „Clip gespeichert“ bzw. warum nicht. Auch im Spiel, ohne Ton; nimmt nie den Fokus.':
        'Mostra una piccola finestra di notifica in basso a destra per la clip istantanea (F8) – «Salvataggio clip …» e poi «Clip salvata» o perché no. Anche nel gioco, senza suono; non prende mai lo stato attivo.',
    'Grenzen oben und unten in den schwarzen Balken':
        'Limiti in alto e in basso delle barre nere',
    'Grenzen zurücksetzen':
        'Ripristina limiti',
    'Links und rechts gleich':
        'Sinistra e destra uguali',
    'In jedem schwarzen Balken (links und rechts) eine Linie oben und eine unten: Karte, Systemwerte, Heute und Musik bleiben dazwischen – z. B. frei für eine FPS-Anzeige oder Benachrichtigungen. Die Karte wird bei Bedarf kleiner.':
        'Una linea in alto e una in basso in ogni barra nera (sinistra e destra): mappa, valori di sistema, oggi e musica restano tra le due – ad es. per lasciare spazio a un contatore FPS o alle notifiche. Se serve la mappa diventa più piccola.',
    'Eine Linie ziehen bewegt die gleiche Linie im anderen Balken mit.':
        "Trascinando una linea si sposta anche la stessa linea nell'altra barra.",
    'Setzt alle vier Linien auf 8 % vom Rand zurück.':
        "Riporta tutte e quattro le linee all'8 % dal bordo.",
    'Dunkelgrauer Boden mit hellem Rand – gilt auch im Spiel.':
        'Pavimento grigio scuro con un bordo chiaro – anche nel gioco.',
    'Dunkelgrauer Boden – die Form der Map bleibt auf dem schwarzen Balken sichtbar. Gilt auch im Spiel.':
        'Pavimento grigio scuro – la forma della mappa resta visibile sulla barra nera. Anche nel gioco.',
    'Dunkles Lila mit lila Rand, erinnert an die Originalfarbe – gilt auch im Spiel.':
        'Lilla scuro con un bordo lilla, vicino al colore originale – anche nel gioco.',
    'Durchsichtiger Boden mit dunklem Rand – gilt auch im Spiel.':
        'Pavimento trasparente con un bordo scuro – anche nel gioco.',
    'Grau':
        'Grigio',
    'Grau mit Rand':
        'Grigio con bordo',
    'Lila dunkel':
        'Lilla scuro',
    'Lila transparent':
        'Lilla trasparente',
    'Lila Boden, halb durchsichtig – gilt auch im Spiel.':
        'Pavimento lilla, semitrasparente – anche nel gioco.',
    'Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe unsichtbar.':
        'Importante: in DBD in Impostazioni → Grafica scegli la modalità di visualizzazione «Schermo intero in finestra». A schermo intero esclusivo Windows non può mostrare una finestra sopra il gioco – la mappa resterebbe invisibile.',
    'Ungültiger Servername im Auftrag: {name}':
        'Nome server non valido nel processo: {name}',
    'Die hosts-Datei wurde direkt nach dem Schreiben wieder verändert (Virenschutz oder ein anderes Programm?).':
        'Il file hosts è stato modificato di nuovo subito dopo la scrittura (antivirus o un altro programma?).',
    'Keine Schreibrechte auf die hosts-Datei (Administratorrechte?).':
        'Nessun permesso di scrivere il file hosts (diritti di amministratore?).',
    'Aufbau der Match-Daten speichern':
        'Salva la struttura dei dati partita',
    'Öffnet die Stats-Seite so, dass das Userscript einmal den Aufbau ihrer Match-Daten im Download-Ordner speichert: nur Feldnamen und Arten, keine Werte. Damit lässt sich entscheiden, welche Daten das Programm zusätzlich auswerten könnte.':
        "Apre la pagina statistiche in modo che l'userscript salvi una volta la struttura dei suoi dati partita nella cartella dei download: solo nomi e tipi dei campi, nessun valore. Mostra quali altri dati il programma potrebbe usare.",
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) legt danach „{file}“ in den Download-Ordner: nur die Namen und Arten der Felder, die die Seite liefert – keine Werte, keine Namen, keine IDs. Das Programm liest diese Datei nicht; du kannst sie weitergeben, um zu entscheiden, welche Felder zusätzlich übernommen werden sollen. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        "La pagina statistiche si apre nel browser. L'userscript (versione {n} o più recente) mette poi «{file}» nella cartella dei download: solo i nomi e i tipi dei campi che la pagina invia – nessun valore, nessun nome, nessun ID. Il programma non legge questo file; puoi inoltrarlo per decidere quali altri campi prendere. Userscript più vecchi: prima «Copia userscript» e sostituiscilo in Tampermonkey.",
    'Gegner':
        'Avversari',
    'Charakter':
        'Personaggio',
    'Begegnungen':
        'Incontri',
    'Geopfert':
        'Sacrificati',
    'Getötet':
        'Uccisi',
    'Aufgegeben':
        'Abbandonati',
    'Laut Stats-Seite: als Killer die Survivor gegen dich und wie ihr Match endete, als Survivor der Killer und wie dein Match endete. „Getötet“ = vom Killer direkt getötet (z. B. Mori), „Aufgegeben“ schließt verlassene Matches ein. „Ø Kills ohne Aufgaben“ zählt nur Matches, in denen kein Survivor aufgab oder ging. „Farming“ = Begegnungen in Farming-Runden, die „Begegnungen“ nicht zählen.':
        'Dalla pagina statistiche: da Killer i Sopravvissuti contro di te e come è finita la loro partita, da Sopravvissuto il Killer e come è finita la tua partita. «Uccisi» = uccisi direttamente dal Killer (ad es. un mori), «Abbandonati» include le partite lasciate. «Ø uccisioni pulite» conta solo le partite in cui nessun Sopravvissuto ha abbandonato o lasciato. «Farming» = incontri nei round di farming, che «Incontri» esclude.',
    'Noch keine Runden mit Daten der Stats-Seite in dieser Auswahl.':
        'Ancora nessun round con dati della pagina statistiche in questa selezione.',
    'Schnellste 4K':
        '4K più veloce',
    '{n} von {total} Runden':
        '{n} di {total} round',
    '{n} Survivor':
        '{n} Sopravvissuti',
    'Ø Kills ohne Aufgaben':
        'Ø uccisioni pulite',
    'OBS mit DBD starten, falls es noch nicht läuft':
        'Avvia OBS con DBD se non è ancora in esecuzione',
    'Startet DBD und ist OBS nicht erreichbar, startet das Programm OBS einmal minimiert im Infobereich – nur, wenn kein OBS-Fenster offen ist. OBS bleibt offen, wenn DBD beendet wird. OBS läuft dann mit denselben Rechten wie das Programm (Administrator).':
        "Quando DBD si avvia e OBS non è raggiungibile, il programma avvia OBS una volta, ridotto a icona nell'area di notifica – solo se nessuna finestra di OBS è aperta. OBS resta aperto quando DBD viene chiuso. OBS gira poi con gli stessi diritti del programma (amministratore).",
    'OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS è stato avviato ma non è raggiungibile – in OBS in Strumenti → Impostazioni server WebSocket attiva il server e controlla porta/password. ({error})',
    'OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio).':
        'OBS non trovato – avvia OBS tu stesso (cercato in Program Files\\obs-studio).',
    'OBS konnte nicht gestartet werden: {error}':
        'Impossibile avviare OBS: {error}',
    'OBS wird gestartet …':
        'Avvio di OBS …',
    'OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS è aperto ma non è raggiungibile – in OBS in Strumenti → Impostazioni server WebSocket attiva il server e controlla porta/password. ({error})',
    'Builds':
        'Build',
    'Build (4 Perks)':
        'Build (4 perk)',
    'Perk':
        'Perk',
    'Add-on':
        'Add-on',
    'Opfergabe':
        'Offerta',
    'Kraft/Item':
        'Potere/oggetto',
    'ohne':
        'senza',
    'Dein Loadout laut Stats-Seite (ab Userscript Version 3). „Ergebnis“ = als Killer Ø Kills, als Survivor Anteil entkommen; „ohne“ = dasselbe in deinen Runden derselben Rolle ohne diesen Eintrag. Builds ab {n} Runden. Embleme: Ø Stufe von keins (0) bis Iri (4); „voll“ = Kategorie mit {max} Punkten.':
        'Il tuo loadout dalla pagina statistiche (userscript versione 3 o più recente). «Risultato» = da Killer Ø uccisioni, da Sopravvissuto la quota di fughe; «senza» = lo stesso nei tuoi round di quel ruolo senza questa voce. Build da {n} round. Emblemi: Ø livello da nessuno (0) a iri (4); «pieno» = categoria a {max} punti.',
    'Event-Modus':
        'Modalità evento',
    'keins':
        'nessuno',
    'Bronze':
        'Bronzo',
    'Silber':
        'Argento',
    'Gold':
        'Oro',
    'Iri':
        'Iri',
    'Emblem':
        'Emblema',
    'Ø Stufe':
        'Ø livello',
    'Punktekategorie':
        'Categoria punteggio',
    'Ø Punkte':
        'Ø punti',
    'voll':
        'pieno',
    'Killer-Wertung: {list}':
        'Valutazione Killer: {list}',
    'Noch keine Matches mit Loadout in dieser Auswahl – die Stats-Seite liefert es ab Userscript Version 3 (Einstellungen → Match-Daten → Offizielle Match-Daten → „Userscript kopieren“).':
        "Ancora nessuna partita con un loadout in questa selezione – la pagina statistiche lo invia dall'userscript versione 3 (Impostazioni → Dati partita → Dati partita ufficiali → «Copia userscript»).",
    'Alle Modi':
        'Tutte le modalità',
    '„{name}“ nicht mehr als Farming-Gegner':
        '«{name}» non più partner di farming',
    '„{name}“ als Farming-Gegner (Runden mit diesem Charakter zählen als Farming)':
        '«{name}» come partner di farming (i round con questo personaggio contano come farming)',
    '„{name}“ gilt jetzt als Farming-Gegner – {n} Runden zählen als Farming (auch ältere; Aufnahmen bleiben, wo sie sind).':
        '«{name}» ora conta come partner di farming – {n} round contano come farming (anche quelli più vecchi; le registrazioni restano dove sono).',
    '„{name}“ gilt nicht mehr als Farming-Gegner.':
        '«{name}» non conta più come partner di farming.',
    'Farming-Gegner (Rechtsklick auf einen Charakter im Reiter „Gegner“): {names}':
        'Partner di farming (clic destro su un personaggio nella scheda «Avversari»): {names}',
    'Gegner & Builds':
        'Avversari e build',
    'Maps, Server & PC':
        'Mappe, server e PC',
    'Bloodpoints & Farming':
        'Punti Sangue e farming',
    'Aufnahme markieren: abspielen, Clip schneiden, behalten, löschen – oder Rechtsklick.':
        'Seleziona una registrazione: riproduci, taglia una clip, conserva, elimina – oppure clic destro.',
    'Clip markieren: abspielen, im Editor öffnen, löschen – oder Rechtsklick.':
        "Seleziona una clip: riproduci, apri nell'editor, elimina – oppure clic destro.",
    'Filter{count}':
        'Filtri{count}',
    'Filter zurücksetzen':
        'Ripristina filtri',
    'Alle Filter der Statistik zurück auf „alle“ – Zeitraum, Rolle, Region, Killer, Map, Modus und „Farming ausblenden“.':
        'Ogni filtro delle statistiche di nuovo su «tutti» – periodo, ruolo, regione, Killer, mappa, modalità e «Nascondi farming».',
    'Region, Killer, Map, Modus und „Farming ausblenden“ ein- oder ausklappen. Die Zahl sagt, wie viele davon gerade filtern.':
        'Mostra o nascondi regione, Killer, mappa, modalità e «Nascondi farming». Il numero indica quanti filtrano in questo momento.',
    'Noch keine Runden gespeichert':
        'Ancora nessun round salvato',
    'Eine Runde zählt vom Map-Banner bis zum Rundenende (ab 1 Minute) und erscheint hier von selbst. Kills, Escapes und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'Un round conta dal banner della mappa alla fine del round (da 1 minuto) e compare qui da solo. Uccisioni, fughe e Punti Sangue arrivano dalla pagina statistiche – per questo configura una volta i dati partita.',
    'Noch keine Aufnahmen – OBS nimmt ab dem nächsten Map-Banner auf. Runden erscheinen hier, Clips (F8 oder aus dem Editor) im Reiter „Clips“.':
        "Ancora nessuna registrazione – OBS registra dal prossimo banner della mappa. I round compaiono qui, le clip (F8 o dall'editor) nella scheda «Clip».",
    'Runden pro Tag – letzte {n} Tage':
        'Round al giorno – ultimi {n} giorni',
    '{when}: {n} Runden ({k} Killer, {s} Survivor)':
        '{when}: {n} round ({k} Killer, {s} Sopravvissuto)',
    '1 s ab Abspielkopf':
        '1 s dalla testina',
    '10 s ab Abspielkopf':
        '10 s dalla testina',
    '100 % = unverändert.':
        '100 % = invariato.',
    '3 s ab Abspielkopf':
        '3 s dalla testina',
    '5 s ab Abspielkopf':
        '5 s dalla testina',
    '9:16 (Hochformat)':
        '9:16 (verticale)',
    'Alle Bilder':
        'Tutte le immagini',
    'Alle Zeichnungen entfernen':
        'Rimuovi tutti i disegni',
    'Alles zurücksetzen':
        'Ripristina tutto',
    'Anderen Ordner …':
        'Altra cartella …',
    'Aufgenommen (F12)':
        'Scattate (F12)',
    'Ausschnitt':
        'Ritaglia',
    'Ausschnitt {w}×{h}':
        'ritaglio {w}×{h}',
    'Bearbeitet':
        'Modificate',
    'Bearbeitete Bilder öffnen':
        'Apri immagini modificate',
    'Bild bearbeiten – {name}':
        'Modifica immagine – {name}',
    'Bild bearbeiten …':
        'Modifica immagine …',
    'Bild gespeichert: {file}':
        'Immagine salvata: {file}',
    'Bild im Explorer zeigen':
        'Mostra immagine in Esplora file',
    'Bild nicht gespeichert: {error}':
        'Immagine non salvata: {error}',
    'Speichert …':
        'Salvataggio …',
    'Bild nicht lesbar: {error}':
        'Immagine non leggibile: {error}',
    'Bild speichern':
        'Salva immagine',
    'Der Clip beginnt aus Schwarz und mit leisem Ton.':
        "La clip parte dal nero con l'audio che sale.",
    'Der Clip endet in Schwarz, der Ton wird leiser.':
        "La clip finisce nel nero, l'audio sfuma.",
    'Dick':
        'Spesso',
    'Dünn':
        'Sottile',
    'Eigener Ordner':
        'Cartella propria',
    'Eigener Ordner nicht gefunden: {path}':
        'Cartella propria non trovata: {path}',
    'Einblenden':
        'Dissolvenza in entrata',
    'Entfernt den markierten Kasten (Entf).':
        'Rimuove il riquadro selezionato (Del).',
    'Entfernt die markierte Zeichnung (Entf).':
        'Rimuove il disegno selezionato (Del).',
    'Farbe':
        'Colore',
    'Farbe zurücksetzen':
        'Ripristina colore',
    'Frei':
        'Libero',
    'Freihand':
        'A mano libera',
    'GIF (ohne Ton, für Chats)':
        'GIF (senza audio, per chat)',
    'GIF {h}p, {fps} Bilder/s, ohne Ton':
        'GIF {h}p, {fps} fotogrammi/s, senza audio',
    'Helligkeit':
        'Luminosità',
    'Helligkeit, Kontrast und Sättigung auf 100 %.':
        'Luminosità, contrasto e saturazione di nuovo al 100 %.',
    'Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats).':
        'Altezza della GIF – più piccola = file più piccolo (Discord, chat).',
    'Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern.':
        "Trascina un'area nell'immagine che viene resa illeggibile – nomi, chat, lista amici. I riquadri si possono spostare e ridimensionare dall'angolo in basso a destra.",
    'Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt sie, Entf löscht sie.':
        "Trascina nell'immagine (testo: clic). Fai clic su un disegno per selezionarlo, trascina per spostarlo, Del lo rimuove.",
    'Immer':
        'Sempre',
    'In Zwischenablage':
        'Negli appunti',
    'In die Zwischenablage kopiert – in Discord mit Strg+V einfügen.':
        'Copiata negli appunti – incollala in Discord con Ctrl+V.',
    'Ohne schwarze Ränder':
        'Senza bordi neri',
    'Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das Spielbild, „Kein Ausschnitt“ das ganze Bild.':
        "La registrazione ha bordi neri: «Senza bordi neri» salva solo l'immagine di gioco, «Nessun ritaglio» l'intera immagine.",
    'Kein Ausschnitt':
        'Nessun ritaglio',
    'Kein Screenshot-Ordner von Steam für DBD gefunden – noch kein F12-Screenshot, oder Steam speichert woanders („Anderen Ordner …“).':
        'Nessuna cartella screenshot di Steam per DBD trovata – ancora nessuno screenshot F12, o Steam salva altrove («Altra cartella …»).',
    'Kontrast':
        'Contrasto',
    'Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C).':
        "Copia l'immagine modificata – incollala in Discord con Ctrl+V (Ctrl+C).",
    'Kreis':
        'Ellisse',
    'Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen':
        'Space riproduci · ←/→ 1 s · Shift 5 s · Ctrl 1 fotogramma · I/O inizio/fine · A parte · M segno · Home/End inizio/fine · Del rimuove riquadro/disegno · Esc chiudi',
    'Letzten Schritt zurücknehmen (Strg+Z).':
        "Annulla l'ultimo passo (Ctrl+Z).",
    'Linie':
        'Linea',
    'Links und rechts tauschen.':
        'Scambia sinistra e destra.',
    'Mittel':
        'Medio',
    'Oben und unten tauschen.':
        'Scambia sopra e sotto.',
    'Ordner mit deinen Screenshots':
        'Cartella con i tuoi screenshot',
    'Ordner nicht anlegbar: {error}':
        'Impossibile creare la cartella: {error}',
    'PNG: verlustfrei · JPG: kleinere Datei.':
        'PNG: senza perdita · JPG: file più piccolo.',
    'Pfeil':
        'Freccia',
    'Rahmen':
        'Riquadro',
    'Rahmen bearbeiten':
        'Modifica cornice',
    'Rahmen im Bild ziehen, verschieben, an den Ecken ändern.':
        "Trascina la cornice nell'immagine, spostala, modificala dagli angoli.",
    'Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. Nochmal drücken beendet das Werkzeug.':
        "Sposta la cornice nell'anteprima o trascina i suoi angoli per ingrandirla/rimpicciolirla. Premi di nuovo per terminare lo strumento.",
    'Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen.':
        "Ritaglia un'area dall'immagine – 9:16 per YouTube Shorts e TikTok, 1:1 per Instagram. Sposta la cornice nell'anteprima e trascina i suoi angoli.",
    'Screenshots':
        'Screenshot',
    'Sehr dick':
        'Molto spesso',
    'Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den Ecken ziehen.':
        "Proporzioni del ritaglio; sposta la cornice nell'immagine e trascina i suoi angoli.",
    'Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im Screenshot-Ordner von Steam) bleibt unverändert (Strg+S).':
        "Salva una copia modificata nella cartella di Fog Scout – l'originale (ad es. nella cartella screenshot di Steam) resta com'è (Ctrl+S).",
    'Steam (F12)':
        'Steam (F12)',
    'Steam-Ordner verwenden':
        'Usa la cartella di Steam',
    'Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf Markiertes löschen · Esc schliessen':
        "Ctrl+Z annulla · Ctrl+Y ripeti · Ctrl+C copia · Ctrl+S salva · Del rimuove l'elemento selezionato · Esc chiudi",
    'Strichstärke bzw. Textgrösse.':
        'Spessore della linea o dimensione del testo.',
    'Sättigung':
        'Saturazione',
    'Tempo':
        'Velocità',
    'Text':
        'Testo',
    'Text für das Text-Werkzeug':
        'Testo per lo strumento testo',
    'Um 90° gegen den Uhrzeigersinn drehen.':
        'Ruota di 90° in senso antiorario.',
    'Um 90° im Uhrzeigersinn drehen.':
        'Ruota di 90° in senso orario.',
    'Verwirft alle Änderungen – das Original bleibt ohnehin unverändert.':
        "Scarta tutte le modifiche – l'originale resta comunque com'è.",
    'Wie der Bereich unkenntlich wird.':
        "Come l'area viene resa illeggibile.",
    'Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des Abspielkopfs. Gilt für neue und für die markierte Zeichnung.':
        'Per quanto tempo il disegno si vede nella clip – dalla testina in poi. Per i nuovi disegni e quello selezionato.',
    'Zeichnen':
        'Disegna',
    'Zeichnung entfernen':
        'Rimuovi disegno',
    'Zeigt das zuletzt gespeicherte Bild im Explorer.':
        "Mostra in Esplora file l'ultima immagine salvata.",
    'Zurückgenommenen Schritt wiederholen (Strg+Y).':
        'Ripeti il passo annullato (Ctrl+Y).',
    'Zuschneiden':
        'Ritaglio',
    'neu kodiert (wie „Genau“)':
        'ricodificato (come «Preciso»)',
    'normal':
        'normale',
    '{n} Abschnitt(e), {length} s':
        '{n} parti, {length} s',
    '{w} × {h} Pixel · Original bleibt unverändert':
        "{w} × {h} pixel · l'originale resta com'è",
    '↶ Rückgängig':
        '↶ Annulla',
    '↷ Wiederholen':
        '↷ Ripeti',
    '⇅ Kippen':
        '⇅ Capovolgi',
    '⇆ Spiegeln':
        '⇆ Specchia',
    '⟲ Links drehen':
        '⟲ Ruota a sinistra',
    '⟳ Rechts drehen':
        '⟳ Ruota a destra',
    'Öffnet das markierte Bild im Bild-Editor: zuschneiden, drehen, Pfeile und Text, zensieren, Farbe – gespeichert wird eine Kopie, das Original bleibt.':
        "Apre l'immagine selezionata nell'editor di immagini: ritaglia, ruota, frecce e testo, censura, colore – viene salvata una copia, l'originale resta.",
    'Zeigt die Bilddatei im Explorer.':
        "Mostra il file dell'immagine in Esplora file.",
    'Öffnet den Ordner mit den bearbeiteten Bildern (Screenshots neben den Aufnahmen bzw. Bilder/Fog Scout).':
        'Apre la cartella con le immagini modificate (Screenshots accanto alle registrazioni, o Immagini/Fog Scout).',
    'Bilder aus einem eigenen Ordner zeigen – z. B. wenn Steam die Screenshots unkomprimiert in einen anderen Ordner speichert.':
        "Mostra le immagini da una tua cartella – ad es. quando Steam salva screenshot non compressi in un'altra cartella.",
    'Wieder die Screenshots aus Steams Ordner für DBD zeigen (F12 im Spiel).':
        'Mostra di nuovo gli screenshot dalla cartella DBD di Steam (F12 nel gioco).',
    'Bild anklicken: bearbeiten (zuschneiden, zeichnen, zensieren), im Explorer zeigen – Doppelklick öffnet den Editor.':
        "Fai clic su un'immagine: modificala (ritaglia, disegna, censura), mostrala in Esplora file – un doppio clic apre l'editor.",
    'F12 im Spiel ist Steams Screenshot-Taste; das Programm liest Steams Ordner nur. Bearbeitete Bilder sind Kopien im Ordner „Screenshots“ neben den Aufnahmen.':
        'F12 nel gioco è il tasto screenshot di Steam; il programma legge solo la cartella di Steam. Le immagini modificate sono copie nella cartella «Screenshots» accanto alle registrazioni.',
    '1 Bild':
        '1 immagine',
    '{n} Bilder':
        '{n} immagini',
    '★ behalten (nie aufgeräumt) · ⚑ Marken (F8 in der Runde) · ▶ auf YouTube · Rechtsklick auf die Spaltenköpfe: Spalten ein-/ausblenden':
        '★ conservata (mai ripulita) · ⚑ segni (F8 nel round) · ▶ su YouTube · clic destro sulle intestazioni: mostra/nascondi colonne',
    'Clips aus dem Editor, Sofort-Clips (F8) und Standbilder, mit ihrer Runde · ▶ auf YouTube · gelöscht werden nur Dateien, die das Programm selbst angelegt hat':
        "Clip dall'editor, clip istantanee (F8) e fermi immagine, con il loro round · ▶ su YouTube · vengono eliminati solo file creati dal programma stesso",
    'Status':
        'Stato',
    'Schnell (ohne Neukodieren)':
        'Veloce (senza ricodifica)',
    'Genau (neu kodiert)':
        'Preciso (ricodificato)',
    'Für Discord (Zielgrösse)':
        'Per Discord (dimensione obiettivo)',
    'GIF (ohne Ton)':
        'GIF (senza audio)',
    'Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als Video speichern.':
        'Una GIF dura al massimo {limit} s, questa clip {seconds} s – accorciala o salvala come video.',
    'beim Beenden abgebrochen':
        'fermata alla chiusura del programma',
    'Update gesperrt: ein Clip wird noch gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Aggiornamento bloccato: si sta ancora salvando una clip. Dopo fai di nuovo clic su «Aggiorna e riavvia».',
    '(gerade {n})':
        '(ora {n})',
    'Aufnahme gestartet':
        'Registrazione avviata',
    'Aufnahme läuft weiter':
        'Registrazione ripresa',
    'Aufnahme läuft weiter.':
        'Registrazione ripresa.',
    'Aufnahme pausieren/weiter':
        'Pausa/riprendi registrazione',
    'Aufnahme pausiert':
        'Registrazione in pausa',
    'Aufnahme pausiert.':
        'Registrazione in pausa.',
    'Aufnahme starten':
        'Avvia registrazione',
    'Aufnahme starten/stoppen':
        'Avvia/ferma registrazione',
    'Aufnahme stoppen':
        'Ferma registrazione',
    'Aufnahme von Hand gestartet.':
        'Registrazione avviata a mano.',
    'Aufnahme wird beendet …':
        'Arresto della registrazione …',
    'Aufnahme-Laufwerk fast voll – Aufnahme beendet':
        'Unità di registrazione quasi piena – registrazione fermata',
    'Aufnahme-Laufwerk fast voll – nichts gestartet':
        'Unità di registrazione quasi piena – nulla avviato',
    'Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet':
        'Unità di registrazione non collegata – nulla avviato',
    'Aufnahmen sind aus.':
        'Le registrazioni sono disattivate.',
    'Ausgewogen':
        'Bilanciata',
    'Automatisch':
        'Automatico',
    'Bereit':
        'Pronto',
    'Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert.':
        "Altezza dell'immagine della clip – più piccola della registrazione la riduce, mai la ingrandisce.",
    'CPU (x264/x265)':
        'CPU (x264/x265)',
    'Clip speichern (F8)':
        'Salva clip (F8)',
    "Der Sofort-Clip (F8) ist auf {clip} s eingestellt, OBS' Wiederholungspuffer hält nur {buf} s – in OBS: Einstellungen → Ausgabe → Wiederholungspuffer → Maximale Wiederholungszeit.":
        'La clip istantanea (F8) è impostata su {clip} s, ma il buffer di replay di OBS contiene solo {buf} s – in OBS: Impostazioni → Uscita → Buffer di replay → Tempo massimo di replay.',
    'Die Datei erscheint im Tab Aufnahmen':
        'Il file compare nella scheda Registrazioni',
    'Es läuft schon eine Aufnahme':
        'È già in corso una registrazione',
    'H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel kleiner, braucht aber einen neueren Player.':
        'H.264 si riproduce ovunque; HEVC (H.265) è circa un terzo più piccolo a parità di qualità ma richiede un lettore più recente.',
    'Hoch':
        'Alta',
    'Kein Aufnahmeordner gewählt – Einstellungen → Aufnahmen.':
        'Nessuna cartella registrazioni scelta – Impostazioni → Registrazioni.',
    'Keine Aufnahme':
        'Nessuna registrazione',
    'Keine Aufnahme läuft':
        'Nessuna registrazione in corso',
    'Keine Aufnahme läuft.':
        'Nessuna registrazione in corso.',
    'Kodiere {file} … ({how}, dauert etwas)':
        'Codifica di {file} … ({how}, richiede un momento)',
    'Kodierung':
        'Codifica',
    'Marke setzen':
        'Imposta segno',
    'Nimmt auf':
        'Registrazione',
    'Nimmt auf (von Hand gestartet)':
        'Registrazione (avviata a mano)',
    'Nimmt die Runde in der laufenden Aufnahme auf':
        "Registrazione del round all'interno della registrazione in corso",
    'OBS lässt Bilder aus ({n} von {total}, Kodierer überlastet) – in OBS Voreinstellung oder Auflösung senken.':
        'OBS salta fotogrammi ({n} di {total}, encoder sovraccarico) – abbassa il preset o la risoluzione in OBS.',
    'OBS nicht erreichbar':
        'OBS non raggiungibile',
    'OBS starten, WebSocket-Server einschalten, Port/Passwort prüfen (Einstellungen → Verbindungen → OBS-Verbindung → Verbindung testen). {why}':
        'Avvia OBS, attiva il suo server WebSocket, controlla porta/password (Impostazioni → Connessioni → Connessione OBS → Prova connessione). {why}',
    'OBS verpasst Bilder beim Rendern ({n} von {total}, Grafikkarte ausgelastet).':
        'OBS perde fotogrammi durante il rendering ({n} di {total}, scheda grafica occupata).',
    'Pause':
        'Pausa',
    'Pausiert':
        'In pausa',
    'Schnell':
        'Veloce',
    'Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. Hoch: grösser, nahe am Original.':
        "Veloce: più piccolo e rapido, visibilmente più morbido. Bilanciata: come prima. Alta: più grande, vicina all'originale.",
    'Stoppen mit demselben Hotkey oder im Tab Aufnahmen':
        'Ferma con lo stesso hotkey o nella scheda Registrazioni',
    'Warte auf OBS …':
        'In attesa di OBS …',
    'Wie aufgenommen':
        'Come registrato',
    'Wiederholungspuffer aus':
        'Buffer di replay disattivato',
    'Wiederholungspuffer in OBS nicht aktiviert':
        'Buffer di replay non attivato in OBS',
    'Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; „Automatisch“ nimmt die erste, die geht.':
        'Cosa codifica la clip: la scheda grafica (NVENC, AMF, Quick Sync – solo se ffmpeg può davvero usarla qui) carica appena il processore; «Automatico» prende il primo che funziona.',
    'letzter Clip {file} (vor {age})':
        'ultima clip {file} ({age} fa)',
    'Fortsetzen':
        'Riprendi',
    'von Hand gestartet':
        'avviata a mano',
    'von OBS selbst gestartet':
        'avviata in OBS stesso',
    'Beendet die laufende Aufnahme jetzt (bei einer Runde ohne Nachlauf) und legt sie in den Aufnahmeordner.':
        'Ferma ora la registrazione in corso (un round senza la coda) e la archivia nella cartella registrazioni.',
    'Hält die laufende Aufnahme an (OBS pausiert); „Fortsetzen“ setzt sie in derselben Datei fort. Marken bleiben an ihrer Stelle.':
        'Mette in pausa la registrazione in corso (OBS si mette in pausa); «Riprendi» la continua nello stesso file. I segni mantengono la loro posizione.',
    'Merkt diesen Moment in der laufenden Aufnahme (⚑) – der Clip-Editor springt später dorthin. Ohne Sofort-Clip.':
        "Annota questo momento nella registrazione in corso (⚑) – l'editor di clip ci salta più tardi. Senza clip istantanea.",
    'Setzt die pausierte Aufnahme fort.':
        'Continua la registrazione in pausa.',
    'Startet jetzt eine OBS-Aufnahme von Hand – auch ausserhalb einer Runde. Sie läuft, bis du sie stoppst oder DBD beendet wird; ein Map-Banner benennt sie. Hotkey einstellbar.':
        'Avvia ora a mano una registrazione OBS – anche fuori da un round. Dura finché non la fermi o DBD si chiude; un banner della mappa le dà il nome. Hotkey configurabile.',
    'Wie F8: speichert die letzten Sekunden aus dem OBS-Wiederholungspuffer als Sofort-Clip (Länge unter Einstellungen → Aufnahmen) und setzt eine Marke, falls eine Aufnahme läuft.':
        'Come F8: salva gli ultimi secondi del buffer di replay di OBS come clip istantanea (durata in Impostazioni → Registrazioni) e imposta un segno se è in corso una registrazione.',
    '1 Eintrag':
        '1 voce',
    '{n} Einträge':
        '{n} voci',
    '5 Sekunden vor (Shift+→).':
        '5 secondi avanti (Shift+→).',
    '5 Sekunden zurück (Shift+←).':
        '5 secondi indietro (Shift+←).',
    'Auf der Zeitleiste öffnen':
        'Apri sulla timeline',
    'Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s':
        'Registrazione {start} – {end} · sulla timeline da {at} · {length} s',
    'Auswahl':
        'Seleziona',
    'Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).':
        'Sfoca aree – nomi, chat, lista amici (X).',
    'Bibliothek':
        'Libreria',
    'Bibliothek ein-/ausblenden.':
        'Mostra/nascondi la libreria.',
    'Bildausschnitt – den Rahmen in der Vorschau ziehen (C).':
        'Ritaglia – trascina la cornice nel visualizzatore (C).',
    'Clip entfernt – die Aufnahme bleibt, wie sie ist.':
        "Clip rimossa – la registrazione resta com'è.",
    'Clip geteilt – jetzt {n} Clips.':
        'Clip divisa – ora {n} clip.',
    'Clip {n} von {total}':
        'Clip {n} di {total}',
    'Clips auf der Zeitleiste wählen, verschieben und trimmen (V).':
        'Seleziona, sposta e rifila le clip sulla timeline (V).',
    'Den ganzen Schnitt einpassen (Strg+0).':
        "Adatta l'intero montaggio (Ctrl+0).",
    'Der Clip unter dem Abspielkopf beginnt hier (Taste I).':
        'La clip sotto la testina inizia qui (tasto I).',
    'Der Clip unter dem Abspielkopf endet hier (Taste O).':
        'La clip sotto la testina finisce qui (tasto O).',
    'Diese Aufnahme ist schon auf der Zeitleiste.':
        'Questa registrazione è già sulla timeline.',
    'Ein Bild vor (Strg+→); → eine Sekunde.':
        'Un fotogramma avanti (Ctrl+→); → un secondo.',
    'Ein Bild zurück (Strg+←); ← eine Sekunde.':
        'Un fotogramma indietro (Ctrl+←); ← un secondo.',
    'Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt.':
        'Rimuove la clip selezionata dalla timeline (Del) – la registrazione resta.',
    'Export':
        'Esporta',
    'Exportieren':
        'Esportazione',
    'Fog Scout · Editor':
        'Fog Scout · Editor',
    'Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze.':
        'Niente da dividere qui – la testina è sul bordo di una clip.',
    'Hier teilen':
        'Dividi qui',
    'Inspector':
        'Ispettore',
    'Inspector ein-/ausblenden.':
        "Mostra/nascondi l'ispettore.",
    'Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine andere Videodatei.':
        'Nessuna registrazione – qui compaiono registrazioni e clip di OBS, «Importa» aggiunge un altro file video.',
    'Keine Clips auf der Zeitleiste.':
        'Nessuna clip sulla timeline.',
    'Kürzeste zuerst':
        'Prima le più corte',
    'Lautstärke der Vorschau (nicht des Clips).':
        "Volume dell'anteprima (non della clip).",
    '? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export':
        '? tutte le scorciatoie · Space riproduci · ←/→ 1 s · Shift 5 s · Ctrl o ,/. 1 fotogramma · I/O la clip inizia/finisce qui · S dividi · Del elimina · Ctrl+Z/Y annulla/ripeti · F schermo intero · Ctrl+S progetto · Ctrl+E esporta',
    'Längste zuerst':
        'Prima le più lunghe',
    'Löschen':
        'Elimina',
    'Name A–Z':
        'Nome A–Z',
    'Name des Projekts – auch der Name des exportierten Clips.':
        'Nome del progetto – anche il nome della clip esportata.',
    'Neueste zuerst':
        'Prima le più recenti',
    'Pause (Leertaste)':
        'Pausa (Space)',
    'Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D).':
        "Disegna frecce, riquadri, a mano libera e testo sull'immagine (D).",
    'Projekt':
        'Progetto',
    'Projekt geladen: {name}':
        'Progetto caricato: {name}',
    'Projekt gespeichert: {file}':
        'Progetto salvato: {file}',
    'Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten.':
        'Salva il progetto (Ctrl+S) – taglio, ritaglio, disegni, censura e impostazioni di esportazione di questa registrazione, per continuare più tardi.',
    'Runde':
        'Round',
    'Rückgängig (Strg+Z).':
        'Annulla (Ctrl+Z).',
    'Rückgängig.':
        'Annullato.',
    'Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen (Strg+E) – Format und Kodierung im Inspector unter Export.':
        "Scrive il montaggio come clip nella cartella «Clips» accanto alle registrazioni (Ctrl+E) – formato e codifica nell'ispettore in Esportazione.",
    'Sichtbar':
        'Visibile',
    'Sortierung der Bibliothek.':
        'Ordine della libreria.',
    'Spielt den ganzen Schnitt von vorn ab und springt danach zurück.':
        "Riproduce l'intero montaggio dall'inizio e poi torna indietro.",
    'Standbild am Abspielkopf als PNG neben den Clips speichern.':
        'Salva un fermo immagine alla testina come PNG accanto alle clip.',
    'Stärke':
        'Peso',
    'Teilen':
        'Dividi',
    'Teilt den Clip unter dem Abspielkopf in zwei (Taste S).':
        'Divide in due la clip sotto la testina (tasto S).',
    'Ton der Vorschau an/aus (Windows).':
        'Audio anteprima on/off (Windows).',
    'Videodatei importieren':
        'Importa file video',
    'Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie eine Aufnahme öffnen.':
        'Importa un file video – compare nella libreria e si apre come una registrazione.',
    'Videos':
        'Video',
    'Vollbild – nur die Vorschau (F, Esc beendet).':
        'Schermo intero – solo il visualizzatore (F, Esc lo termina).',
    'Wiederholen (Strg+Y).':
        'Ripeti (Ctrl+Y).',
    'Wiederholt.':
        'Ripetuto.',
    'Zeitleiste':
        'Timeline',
    'Zeitleiste ein-/ausblenden.':
        'Mostra/nascondi la timeline.',
    'Zeitleiste einpassen':
        'Adatta timeline',
    'Zeitleiste herauszoomen (−, Strg+Mausrad).':
        'Riduci lo zoom della timeline (−, Ctrl+rotellina).',
    'Zeitleiste hineinzoomen (+, Strg+Mausrad).':
        'Aumenta lo zoom della timeline (+, Ctrl+rotellina).',
    'Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit.':
        "Rallentatore o avanti veloce per la clip selezionata. L'audio segue.",
    'Zum Anfang (Pos1).':
        "All'inizio (Home).",
    'Zum Ende (Ende).':
        'Alla fine (End).',
    '{at} liegt in keinem Clip der Zeitleiste.':
        '{at} non si trova in nessuna clip della timeline.',
    '{n} Clip(s) · {length} s':
        '{n} clip · {length} s',
    'Älteste zuerst':
        'Prima le più vecchie',
    'Öffnen aus der Bibliothek ist hier nicht verfügbar.':
        "L'apertura dalla libreria non è disponibile qui.",
    'Fehler in {step} – siehe Log.':
        'Errore in {step} – vedi il log.',
    'Strg+{n}':
        'Ctrl+{n}',
    'Tastenkürzel':
        'Scorciatoie da tastiera',
    'Schliessen (? oder Esc)':
        'Chiudi (? o Esc)',
    'Wiedergabe':
        'Riproduzione',
    'Werkzeuge':
        'Strumenti',
    'Leertaste':
        'Space',
    'Abspielen / Anhalten':
        'Riproduci / pausa',
    '1 Sekunde zurück / vor':
        '1 secondo indietro / avanti',
    'Shift+← / →':
        'Shift+← / →',
    '5 Sekunden zurück / vor':
        '5 secondi indietro / avanti',
    'Strg+← / →  ·  , / .':
        'Ctrl+← / →  ·  , / .',
    '1 Bild zurück / vor':
        '1 fotogramma indietro / avanti',
    'Pos1 / Ende':
        'Home / End',
    'Zum Anfang / zum Schluss':
        "All'inizio / alla fine",
    'Zur nächsten Marke':
        'Al prossimo segno',
    'Untertitel {a}–{b}.':
        'Sottotitolo {a}–{b}.',
    '{file} wartet – {n} Export(e) davor.':
        '{file} è in attesa – {n} esportazioni prima.',
    'Kodiere {file} …':
        'Codifica di {file} …',
    'Titel & Vorschaubild':
        'Titolo e miniatura',
    'Claude fragt: {question}':
        'Claude chiede: {question}',
    'Deine Antwort …':
        'La tua risposta …',
    'Name der Vorlage':
        'Nome del modello',
    'Als Vorlage speichern':
        'Salva come modello',
    'Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen.':
        "Conserva i passi appena fatti (senza riquadri di censura) come modello – tempi dall'inizio o dalla fine, così vanno bene anche per altre durate.",
    'Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, kostenlos; erst „Übernehmen“ ändert den Schnitt.':
        'Propone i passi del modello per questo montaggio – senza Claude, gratis; solo «Applica» cambia il montaggio.',
    'Vorlage löschen':
        'Elimina modello',
    'Entfernt die gewählte Vorlage.':
        'Rimuove il modello scelto.',
    'Bitte einen Namen für die Vorlage eingeben.':
        'Inserisci un nome per il modello.',
    'Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu).':
        'Niente che funzioni come modello (i riquadri di censura non ne fanno parte).',
    'Vorlage „{name}“ gespeichert.':
        'Modello «{name}» salvato.',
    'Vorlage „{name}“':
        'Modello «{name}»',
    'Vorlage „{name}“ gelöscht.':
        'Modello «{name}» eliminato.',
    'Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts wird hochgeladen.':
        "Invia a Claude gli stessi otto fermi immagine di «Controlla l'esportazione»; Claude sceglie la miniatura migliore e propone un titolo. Il titolo lo prendi tu, la miniatura viene solo salvata come immagine in «Clips» – non viene caricato nulla.",
    'Claude sucht unter {n} Standbildern ein Vorschaubild …':
        'Claude sta scegliendo una miniatura tra {n} fermi immagine …',
    'Als Short-Titel: „{title}“':
        'Come titolo dello short: «{title}»',
    'Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für YouTube kopierst du ihn selbst.':
        'Prende il titolo come titolo dello short (un passo da annullare). Per YouTube lo copi tu.',
    'Vorschaubild bei {at} speichern':
        'Salva la miniatura a {at}',
    'Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im Export, mit dem Titel. Hochgeladen wird nichts.':
        "Salva questo fermo immagine a grandezza piena come PNG in «Clips» – censurato come nell'esportazione, con il titolo. Non viene caricato nulla.",
    'Short-Titel übernommen.':
        'Titolo dello short preso.',
    'Vorschaubild':
        'Miniatura',
    'Export prüfen':
        "Controlla l'esportazione",
    'Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf einen Fund springt hin und schlägt einen Zensurkasten vor.':
        "Invia a Claude otto fermi immagine del montaggio finito (ritagliati come nell'esportazione, aree censurate censurate); Claude segnala nomi o chat ancora leggibili e qualsiasi altra cosa che non andrebbe condivisa così. Un clic su un risultato salta lì e suggerisce un riquadro di censura.",
    'Claude prüft {n} Standbilder des fertigen Schnitts …':
        'Claude sta controllando {n} fermi immagine del montaggio finito …',
    'Claude hat nichts gefunden, das so nicht geteilt werden sollte.':
        'Claude non ha trovato nulla che non andrebbe condiviso così.',
    'Springt hin und schlägt einen Zensurkasten für diese Stelle vor.':
        'Salta lì e suggerisce un riquadro di censura per questo punto.',
    'Springt hin.':
        'Salta lì.',
    'Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.':
        'Suggerimento a {at} – «Accetta i suggerimenti» nasconde il punto.',
    'Name lesbar':
        'Nome leggibile',
    'Chat lesbar':
        'Chat leggibile',
    'Auffällig':
        "Salta all'occhio",
    'Text finden':
        'Trova testo',
    'Sucht auf dem Bild am Abspielkopf nach Text (Namen, Chat) – auf diesem PC, nichts wird gesendet. Die Fundstellen erscheinen nummeriert.':
        "Cerca testo (nomi, chat) nell'immagine alla testina – su questo PC, non viene inviato nulla. I risultati compaiono numerati.",
    'Vorschläge übernehmen':
        'Accetta i suggerimenti',
    'Macht aus den nummerierten Fundstellen Zensurkästen (ein Schritt zum Rückgängigmachen).':
        'Trasforma i risultati numerati in riquadri di censura (un passo da annullare).',
    'Vorschläge verwerfen':
        'Scarta i suggerimenti',
    'Claude: nur Namen':
        'Claude: solo nomi',
    'Schickt das Standbild (zensierte Bereiche bleiben zensiert) mit den nummerierten Fundstellen an Claude; Claude nennt nur die Nummern, die Namen oder Chat zeigen – die übrigen Vorschläge fallen weg.':
        'Invia a Claude il fermo immagine (le aree censurate restano censurate) con i risultati numerati; Claude indica solo i numeri che mostrano nomi o chat – gli altri suggerimenti vengono scartati.',
    'Die Texterkennung ist in dieser Installation nicht vorhanden.':
        'Il rilevamento del testo non è disponibile in questa installazione.',
    'Suche Text im Bild …':
        "Ricerca di testo nell'immagine …",
    'Das Bild liess sich nicht nach Text durchsuchen.':
        "Impossibile cercare testo nell'immagine.",
    'Kein Text gefunden, der nicht schon verdeckt ist.':
        'Nessun testo trovato che non sia già nascosto.',
    '{n} Textstellen gefunden – „Vorschläge übernehmen“ verdeckt sie.':
        '{n} punti con testo trovati – «Accetta i suggerimenti» li nasconde.',
    '{n} Kästen gesetzt.':
        '{n} riquadri impostati.',
    'Claude sieht sich {n} Fundstellen an …':
        'Claude sta esaminando {n} risultati …',
    'Claude hält keine Fundstelle für einen Namen oder Chat.':
        'Secondo Claude nessuno dei risultati è un nome o una chat.',
    '{n} Fundstellen zeigen laut Claude Namen oder Chat.':
        '{n} risultati mostrano nomi o chat, secondo Claude.',
    'Kasten ab hier':
        'Riquadro da qui',
    'Kasten bis hier':
        'Riquadro fino a qui',
    'Kasten immer':
        'Riquadro sempre',
    'Der markierte Kasten gilt erst ab dem Bild am Abspielkopf – z. B. wenn ein Name erst später erscheint.':
        "Il riquadro selezionato vale solo dall'immagine alla testina in poi – ad es. quando un nome compare solo più tardi.",
    'Der markierte Kasten gilt nur bis zum Bild am Abspielkopf.':
        "Il riquadro selezionato vale solo fino all'immagine alla testina.",
    'Der markierte Kasten gilt wieder für die ganze Aufnahme.':
        "Il riquadro selezionato vale di nuovo per l'intera registrazione.",
    'Kasten {n} gilt von {a} bis {b} der Aufnahme.':
        'Il riquadro {n} vale da {a} a {b} della registrazione.',
    'Kasten {n} gilt für die ganze Aufnahme.':
        "Il riquadro {n} vale per l'intera registrazione.",
    'Am Anfang der Aufnahme gibt es kein „bis hier“.':
        "All'inizio della registrazione non c'è un «fino a qui».",
    '{n} davon nur zeitweise.':
        '{n} di essi solo per un certo tempo.',
    'Zurückspringen / Anhalten / Abspielen – L mehrmals: ×2, ×4':
        'Indietro / stop / riproduci – premi di nuovo L: ×2, ×4',
    'Vollbild an / aus':
        'Schermo intero on / off',
    'Clip beginnt / endet am Abspielkopf':
        'La clip inizia / finisce alla testina',
    'S oder Strg+B':
        'S o Ctrl+B',
    'Clip am Abspielkopf teilen':
        'Dividi la clip alla testina',
    'Entf':
        'Del',
    'Markierten Clip löschen':
        'Elimina la clip selezionata',
    'Hinein- / herauszoomen':
        'Zoom avanti / indietro',
    'Strg+0':
        'Ctrl+0',
    'Ganze Zeitleiste zeigen':
        "Mostra l'intera timeline",
    'Auswählen':
        'Seleziona',
    'Bildausschnitt':
        'Ritaglia',
    'Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie':
        'Annulla, esci dallo strumento o svuota la selezione – non chiude mai',
    'Strg+W':
        'Ctrl+W',
    'Editor schliessen':
        "Chiudi l'editor",
    'Abgebrochen.':
        'Annullato.',
    'Esc schliesst den Editor nicht – schliessen mit × oder Strg+W.':
        "Esc non chiude l'editor – chiudilo con × o Ctrl+W.",
    'Strg+Z / Strg+Y':
        'Ctrl+Z / Ctrl+Y',
    'Rückgängig / Wiederholen':
        'Annulla / ripeti',
    'Strg+S':
        'Ctrl+S',
    'Projekt speichern':
        'Salva progetto',
    'Strg+E':
        'Ctrl+E',
    'Diese Übersicht ein / aus':
        'Questa panoramica on / off',
    'In der Statistik zeigen':
        'Mostra nelle statistiche',
    'Aufnahme dieser Runde öffnen':
        'Apri la registrazione di questo round',
    'Runde markieren: Rolle, Farming, Killer oder Map korrigieren, löschen – oder Rechtsklick. Doppelklick zeigt die Aufnahme.':
        'Seleziona un round: correggi ruolo, farming, Killer o mappa, elimina – oppure clic destro. Il doppio clic mostra la registrazione.',
    'OBS-Passwort ist auf diesem PC/Benutzerkonto nicht lesbar – bitte neu eingeben.':
        'La password di OBS non può essere letta su questo PC/account utente – inseriscila di nuovo.',
    'Als neues Projekt speichern':
        'Salva come nuovo progetto',
    'Autosave aus':
        'Salvataggio automatico off',
    'Bereich übernehmen':
        "Prendi l'intervallo",
    'Bereich übernommen – Strg+Z stellt das Projekt wieder her.':
        'Intervallo preso – Ctrl+Z riporta il progetto.',
    'Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. Deine Fassung liegt unter Sicherungen und lokal.':
        'Il progetto è stato modificato fuori da Fog Scout o esiste due volte. La tua versione è conservata in Sicherungen e in locale.',
    'Die Aufnahme konnte nicht geprüft werden.':
        'Impossibile controllare la registrazione.',
    'Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz herunterladen.':
        'La registrazione è solo nel cloud – controllarla la scaricherebbe tutta.',
    'Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt ist anders). Es wurde nicht geladen.':
        'La registrazione non corrisponde al progetto salvato (il suo contenuto è diverso). Non è stata caricata.',
    'Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt.':
        'Le clip del progetto erano illeggibili – viene mostrata la clip predefinita.',
    'Die Projektdatei ist unlesbar und wurde nicht geladen.':
        'Il file del progetto è illeggibile e non è stato caricato.',
    'Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist lokal gesichert.':
        'Il file del progetto è stato eliminato o spostato fuori da Fog Scout. Il tuo stato è conservato in locale.',
    'Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.':
        'Il file del progetto è stato rinominato. Il tuo stato è conservato in locale.',
    'Dieses Projekt ist schon in einem anderen Fenster offen – hier wird nichts gespeichert.':
        "Questo progetto è già aperto in un'altra finestra – qui non viene salvato nulla.",
    'Editor-Projekte automatisch speichern':
        "Salva automaticamente i progetti dell'editor",
    'Editor-Projekte nicht gesichert':
        "Progetti dell'editor non messi al sicuro",
    'Editor-Projekte werden noch gesichert …':
        "Messa al sicuro dei progetti dell'editor in corso …",
    'Editor: automatisches Speichern an.':
        'Editor: salvataggio automatico attivo.',
    'Editor: automatisches Speichern aus – Strg+S speichert das Projekt.':
        'Editor: salvataggio automatico disattivato – Ctrl+S salva il progetto.',
    'Eine wählen …':
        'Scegline uno …',
    'Erneut prüfen':
        'Controlla di nuovo',
    'Es gibt ein Projekt zu einer gleichnamigen, aber veränderten Aufnahme.':
        'Esiste un progetto per una registrazione con lo stesso nome che è cambiata.',
    'Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine Clips.':
        "Questa registrazione ha un progetto salvato ({n} clip). Prendere l'intervallo dall'anteprima ({a}–{b}) sostituisce le sue clip.",
    'Gespeichertes Projekt gefunden – die Aufnahme wird geprüft.':
        'Trovato un progetto salvato – la registrazione viene controllata.',
    'Kein Projekt':
        'Nessun progetto',
    'Kein Projekt – Strg+S legt ein neues an.':
        'Nessun progetto – Ctrl+S ne crea uno nuovo.',
    'Keine öffnen':
        'Non aprire nessuno',
    'Laden':
        'Carica',
    'Lokal gesicherter Stand eines fehlenden Projekts gefunden.':
        'Trovato uno stato conservato in locale di un progetto mancante.',
    'Mindestens ein Editor-Stand ist weder im Projekt noch lokal gesichert (Speichern hängt oder der Ordner ist nicht erreichbar). Trotzdem beenden? Die ungesicherten Änderungen gehen dann verloren.':
        "Almeno uno stato dell'editor non è né nel suo progetto né conservato in locale (il salvataggio si blocca o la cartella non è raggiungibile). Uscire comunque? Le modifiche non messe al sicuro andranno perse.",
    'Neu beginnen':
        'Ricomincia',
    'Neuerer Stand aus der lokalen Rettungskopie geladen.':
        'Caricato uno stato più recente dalla copia di salvataggio locale.',
    'Neues Projekt':
        'Nuovo progetto',
    'Nicht laden':
        'Non caricare',
    'Nicht schliessen':
        'Non chiudere',
    'Nicht wiederherstellen':
        'Non ripristinare',
    'Nichts tun':
        'Non fare nulla',
    'Ohne Prüfung laden':
        'Carica senza controllare',
    'Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, gleiche Grösse).':
        'Trovato un progetto di Fog Scout 1.17 o precedente (stesso nome, stessa dimensione).',
    'Projekt aus neuerer Version – wird nicht überschrieben':
        'Progetto di una versione più recente – non sovrascritto',
    'Projekt behalten':
        'Mantieni il progetto',
    'Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen.':
        "Progetto aperto – l'intervallo dall'anteprima non è stato preso.",
    'Projekt nicht gespeichert und keine Rettungskopie möglich: {why}':
        'Progetto non salvato e nessuna copia di salvataggio possibile: {why}',
    'Projekt wiederherstellen':
        'Ripristina il progetto',
    'Projekt wird gespeichert …':
        'Salvataggio del progetto …',
    'Projekt wird gesucht …':
        'Ricerca del progetto …',
    'Prüfen':
        'Controlla',
    'Prüft Aufnahme …':
        'Controllo della registrazione …',
    'Prüft Aufnahme … {p} %':
        'Controllo della registrazione … {p} %',
    'Speichern und schliessen':
        'Salva e chiudi',
    'Trotzdem laden':
        'Carica comunque',
    'Trotzdem schliessen':
        'Chiudi comunque',
    'Ungespeicherte Änderungen von {when} gefunden.':
        'Trovate modifiche non salvate del {when}.',
    'Ungespeicherte Änderungen.':
        'Modifiche non salvate.',
    'Update wartet: Editor-Projekte werden gesichert …':
        "L'aggiornamento attende: messa al sicuro dei progetti dell'editor in corso …",
    'Verwerfen und schliessen':
        'Scarta e chiudi',
    'Wiederherstellen':
        'Ripristina',
    'Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die ganze Aufnahme ist, kann Fog Scout nicht bestätigen.':
        "Questa registrazione ha un progetto mai controllato del tutto. Inizio, fine e dimensione corrispondono; se sia l'intera registrazione, Fog Scout non può confermarlo.",
    'Zuordnung nicht geprüft':
        'Assegnazione non controllata',
    '{n} Projektdateien passen zu dieser Aufnahme – keine wurde geöffnet.':
        '{n} file di progetto corrispondono a questa registrazione – nessuno è stato aperto.',
    '● Änderungen':
        '● Modifiche',
    '⚠ Mehrere Projektdateien – Auswahl nötig':
        '⚠ Più file di progetto – scegline uno',
    '⚠ Nicht gespeichert – {why}':
        '⚠ Non salvato – {why}',
    '⚠ Nicht im Projekt gespeichert – lokal gesichert':
        '⚠ Non salvato nel progetto – conservato in locale',
    '⚠ Projekt ausserhalb geändert':
        "⚠ Progetto modificato dall'esterno",
    '⚠ Projektdatei fehlt – Änderungen nur lokal gesichert':
        '⚠ File di progetto mancante – modifiche conservate solo in locale',
    '⚠ Speichern hängt':
        '⚠ Il salvataggio si blocca',
    '✓ Gespeichert {at}':
        '✓ Salvato {at}',
    'Der grosse Editor speichert sein Projekt von selbst (1,5 s nach einer Änderung, nie während du ziehst) – mit Sicherungen und einer lokalen Kopie, falls die Projektdatei nicht schreibbar ist. Aus: nur Strg+S schreibt das Projekt; dazwischen hält der Editor einen lokalen Wiederherstellungsstand.':
        "Il grande editor salva il suo progetto da solo (1,5 s dopo una modifica, mai mentre trascini) – con backup e una copia locale nel caso il file di progetto non possa essere scritto. Off: solo Ctrl+S scrive il progetto; nel frattempo l'editor conserva uno stato di recupero locale.",
    'Auf alle Clips':
        'A tutte le clip',
    'Bild bei {at} der Aufnahme · {length} s ohne Ton':
        'Immagine a {at} della registrazione · {length} s senza audio',
    'Den Ausschnitt am Anfang des Clips in der Vorschau ziehen – dazwischen fährt die Kamera gleichmässig.':
        "Trascina la cornice all'inizio della clip nell'anteprima – nel mezzo la telecamera si muove in modo uniforme.",
    'Den Ausschnitt am Ende des Clips in der Vorschau ziehen.':
        "Trascina la cornice alla fine della clip nell'anteprima.",
    'Der Clip zeigt wieder das ganze Bild.':
        "La clip mostra di nuovo l'intera immagine.",
    'Effekte':
        'Effetti',
    'Effekte entfernen':
        'Rimuovi effetti',
    'Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start.':
        'Una cornice fissa: inizio e fine uguali – la cornice finale segue quella iniziale.',
    'End-Ausschnitt':
        'Cornice finale',
    'Farbe auf alle {n} Clips übernommen.':
        'Colore applicato a tutte le {n} clip.',
    'Heller oder dunkler – nur dieser Clip.':
        'Più chiaro o più scuro – solo questa clip.',
    'Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen.':
        'Luminosità, contrasto e saturazione di questa clip di nuovo come registrati.',
    'Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton.':
        "Tiene ferma l'immagine alla testina per il tempo impostato (tasto P) – senza audio.",
    'Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.':
        'Colori più intensi o più pallidi, tutto a sinistra bianco e nero – solo questa clip.',
    'Mehr oder weniger Kontrast – nur dieser Clip.':
        'Più o meno contrasto – solo questa clip.',
    'Ohne Bewegung':
        'Nessun movimento',
    'Rückwärts':
        "All'indietro",
    'Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.':
        "All'indietro funziona fino a {n} s per clip – prima dividi questa clip.",
    'Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens {n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).':
        "Riproduce la clip all'indietro, anche l'audio. Per questa registrazione al massimo {n} s per clip (altrimenti ffmpeg richiede troppa memoria).",
    'Standbild am Abspielkopf einfügen':
        'Inserisci un fermo immagine alla testina',
    'Standbild einfügen':
        'Inserisci fermo immagine',
    'Standbild eingefügt: {n} s ohne Ton.':
        'Fermo immagine inserito: {n} s senza audio.',
    'Standbild hier einfügen':
        'Inserisci fermo immagine qui',
    'Standbild – Clip {n} von {total}':
        'Fermo immagine – clip {n} di {total}',
    'Start-Ausschnitt':
        'Cornice iniziale',
    'Wie lange ein Standbild steht – für ein neues, oder für das markierte Standbild.':
        'Quanto dura un fermo immagine – per uno nuovo o per quello selezionato.',
    'Zoom':
        'Zoom',
    'Zoom entfernen':
        'Rimuovi zoom',
    'Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – Esc beendet.':
        "Zoom: trascina la cornice nell'anteprima o tira i suoi angoli per ingrandirla/rimpicciolirla – Esc termina.",
    '{n}  Standbild {length} s':
        '{n}  Fermo immagine {length} s',
    'Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig).':
        'Applica luminosità, contrasto e saturazione di questa clip a tutte le clip della timeline (un passo, Ctrl+Z lo annulla).',
    'Als Short anzeigen':
        'Mostra come short',
    'Beginnt hier':
        'Inizia qui',
    'Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.':
        'Il testo si vede dalla testina per {n} s in fondo allo short.',
    'Der markierte Untertitel beginnt am Abspielkopf.':
        'Il sottotitolo selezionato inizia alla testina.',
    'Der markierte Untertitel endet am Abspielkopf.':
        'Il sottotitolo selezionato finisce alla testina.',
    'Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen.':
        "L'anteprima mostra il video verticale finito con titolo e sottotitoli – disegni e censura sono nell'esportazione, non mostrati qui.",
    'Ein Short ist höchstens {limit} min lang, dieser Schnitt {seconds} s – kürzer schneiden.':
        'Uno short dura al massimo {limit} min, questo montaggio {seconds} s – accorcialo.',
    'Endet hier':
        'Finisce qui',
    'Entfernen':
        'Rimuovi',
    'Entfernt den markierten Untertitel.':
        'Rimuove il sottotitolo selezionato.',
    'Erst den Text des Untertitels eingeben.':
        'Inserisci prima il testo del sottotitolo.',
    'Hochformat 1080×1920 für YouTube Shorts und TikTok, höchstens 3 min':
        'Verticale 1080×1920 per YouTube Shorts e TikTok, al massimo 3 min',
    'Schriftgrösse des Titels.':
        'Dimensione carattere del titolo.',
    'Short (9:16)':
        'Short (9:16)',
    'Short / TikTok (9:16)':
        'Short / TikTok (9:16)',
    'Short 1080×1920, {fps} fps':
        'Short 1080×1920, {fps} fps',
    'Text eingeben, dann „Untertitel am Abspielkopf“':
        'Inserisci il testo, poi «Sottotitolo alla testina»',
    'Titel':
        'Titolo',
    'Titel oben (leer = keiner)':
        'Titolo in alto (vuoto = nessuno)',
    'Unscharfer Hintergrund':
        'Sfondo sfocato',
    'Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der 9:16-Ausschnitt unter Bild) füllt das Hochformat.':
        "Sfondo sfocato: l'intera immagine di gioco al centro, la stessa immagine sfocata sopra e sotto. Ritaglio: il centro (o il ritaglio 9:16 in Immagine) riempie il formato verticale.",
    'Untertitel':
        'Sottotitoli',
    'Untertitel am Abspielkopf':
        'Sottotitolo alla testina',
    'Zuschnitt 9:16':
        'Ritaglio 9:16',
    'gross':
        'grande',
    'klein':
        'piccolo',
    'mittel':
        'medio',
    '⚠ länger als {n} min – so nicht exportierbar':
        '⚠ più lungo di {n} min – non esportabile così',
    '(Datei fehlt – wird nicht exportiert)':
        '(file mancante – non esportato)',
    'Beginnt am Abspielkopf':
        'Inizia alla testina',
    'Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt ihn am meisten. Aus: beide gleich laut wie eingestellt.':
        "L'audio del gioco si abbassa da solo mentre suona la musica – «forte» lo abbassa di più. Off: entrambi al volume impostato.",
    'Der markierte Ton-Clip beginnt am Abspielkopf.':
        'La clip audio selezionata inizia alla testina.',
    'Die Musik wird am Anfang des Clips lauter.':
        "La musica entra in dissolvenza all'inizio della clip.",
    'Die Musik wird zum Ende des Clips leiser.':
        'La musica sfuma verso la fine della clip.',
    'Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im Export läuft die Musik weiter.':
        "L'anteprima riproduce anche la musica – i fermi immagine sono muti nell'anteprima, nell'esportazione la musica continua.",
    'Eigene Tonspur (A2)':
        'Traccia audio propria (A2)',
    'Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die Spur A2 legen – oder die Datei direkt auf A2 ziehen.':
        'Metti un tuo file audio o video (musica, commento) sulla traccia A2 alla testina – oppure trascina il file su A2.',
    'Höchstens {n} Ton-Clips.':
        'Al massimo {n} clip audio.',
    'Kein Ton in {file}.':
        'Nessun audio in {file}.',
    'Keine Ton- oder Videodatei: {file}':
        'Non è un file audio o video: {file}',
    'Lautstärke':
        'Volume',
    'Lautstärke der ganzen Spur A2.':
        "Volume dell'intera traccia A2.",
    'Lautstärke des Spieltons im fertigen Clip.':
        "Volume dell'audio del gioco nella clip finita.",
    'Lautstärke nur dieses Ton-Clips.':
        'Volume solo di questa clip audio.',
    'Lese {file} …':
        'Lettura di {file} …',
    'Musik aus':
        'Uscita musica',
    'Musik ein':
        'Entrata musica',
    'Musik hinzufügen':
        'Aggiungi musica',
    'Musik hinzufügen …':
        'Aggiungi musica …',
    'Musik oder Kommentar hierher ziehen – oder Rechtsklick „Musik hinzufügen …“':
        'Trascina qui musica o commento – oppure clic destro «Aggiungi musica …»',
    'Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt.':
        'Toglie la clip audio selezionata dalla traccia A2 – il file resta.',
    'Noch keine Musik – Spielton wie aufgenommen.':
        'Ancora nessuna musica – audio del gioco come registrato.',
    'Spielton':
        'Audio del gioco',
    'Spielton unter Musik':
        'Gioco sotto la musica',
    'Ton und Video':
        'Audio e video',
    'Ton-Clip entfernen':
        'Rimuovi clip audio',
    'Ton-Clip {file} entfernt – die Datei bleibt.':
        'Clip audio {file} rimossa – il file resta.',
    'leicht':
        'leggero',
    'stark':
        'forte',
    '{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.':
        "{file} è su A2 da {at} – l'audio del gioco si abbassa sotto di essa.",
    '{file}: {start} – {end} der Datei, im Clip ab {at}':
        '{file}: {start} – {end} del file, nella clip da {at}',
    '{n} Ton-Clip(s) auf A2.':
        '{n} clip audio su A2.',
    'Als Montage öffnen …':
        'Apri come montaggio …',
    'Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.':
        "Dimensione diversa ({w}×{h}) – adattata con bordi neri nell'esportazione.",
    'Aufnahme fehlt oder ist nicht lesbar: {file}':
        'Registrazione mancante o illeggibile: {file}',
    'Eine Montage übernimmt keinen Bereich aus der Vorschau.':
        "Un montaggio non prende alcun intervallo dall'anteprima.",
    'Erst wenn das Projekt geladen ist.':
        'Solo quando il progetto è caricato.',
    'Für eine Montage mindestens zwei Videos markieren.':
        'Seleziona almeno due video per un montaggio.',
    'Höchstens {n} Aufnahmen in einer Montage.':
        'Al massimo {n} registrazioni in un montaggio.',
    'Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das Projekt der Runde bleibt, wie es zuletzt gespeichert war.':
        "Ora è un montaggio – viene salvato in Clips → Montagen. Il progetto del round resta com'era all'ultimo salvataggio.",
    'Montage':
        'Montaggio',
    'Montage aus {n} Aufnahmen':
        'Montaggio di {n} registrazioni',
    'Montage nicht zu öffnen – ihre erste Aufnahme fehlt: {file}':
        'Impossibile aprire il montaggio – manca la sua prima registrazione: {file}',
    'Montage {date}':
        'Montaggio {date}',
    'Nicht gefunden: {files} – ihre Clips sind rot, Exportieren geht erst, wenn sie entfernt sind.':
        "Non trovati: {files} – le loro clip sono rosse; l'esportazione funziona una volta rimosse.",
    'Nur lesen':
        'Sola lettura',
    'Trotzdem verwenden':
        'Usa comunque',
    'Video nicht lesbar: {file}':
        'Video illeggibile: {file}',
    '{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.':
        '{file} non è più la stessa registrazione di quando è stato salvato.',
    '{file}: {n} Clip(s) angehängt.':
        '{file}: {n} clip aggiunte.',
    'Audiomediathek':
        'Libreria audio',
    'Audiomediathek im Browser geöffnet – heruntergeladene Titel erscheinen im Abschnitt Ton, sobald du zurück im Editor bist.':
        "Audio Library aperta nel browser – i brani scaricati compaiono nella sezione Audio appena torni nell'editor.",
    'Neu im Download-Ordner – Klick legt sie am Abspielkopf auf A2:':
        'Nuovi nella cartella dei download – un clic lo mette su A2 alla testina:',
    'Öffnet YouTubes Audiomediathek im Browser: kostenlose Musik und Effekte, für Videos freigegeben (keine Content-ID-Ansprüche). Heruntergeladene MP3s erscheinen hier darunter.':
        'Apre la Audio Library di YouTube nel browser: musica ed effetti gratuiti, liberi per i video (nessun reclamo Content ID). Gli MP3 scaricati compaiono qui sotto.',
    'Status, aktuelle Map und deine Runden auf einen Blick':
        'Stato, mappa attuale e i tuoi round in sintesi',
    'Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen':
        'Tutte le mappe callout – guardale, mostrane una a mano, immagini e note personali',
    'Was im Spiel erscheint, wo und wie gross':
        'Cosa compare nel gioco, dove e quanto grande',
    'Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert':
        'I tuoi round, uccisioni e tempi di attesa – salvati solo su questo PC',
    'Runden, Clips und Screenshots – abspielen, schneiden, aufräumen':
        'Round, clip e screenshot – riproduci, taglia, riordina',
    'Server-Regionen wählen und die Verbindung im Blick behalten':
        "Scegli le regioni server e tieni d'occhio la connessione",
    'Alles, was Fog Scout tut – suchen mit Strg+F':
        'Tutto ciò che fa Fog Scout – cerca con Ctrl+F',
    'Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche':
        'Cosa ha fatto il programma – da consultare e per la risoluzione problemi',
    'Übersicht öffnen':
        'Apri la panoramica',
    'Funktionen':
        'Funzioni',
    'aktiv':
        'attivo',
    'wartet auf DBD':
        'in attesa di DBD',
    'nimmt auf':
        'in registrazione',
    'verbunden':
        'connesso',
    'verbindet …':
        'connessione …',
    'startet …':
        'avvio …',
    'Fehler – Details im Log':
        'Errore – dettagli nel log',
    'nur unter Windows':
        'Solo Windows',
    'HWiNFO fehlt':
        'HWiNFO mancante',
    'Mediensteuerung nicht verfügbar':
        'Controllo multimediale non disponibile',
    'Discord nicht erreichbar':
        'Discord non raggiungibile',
    'Anmeldung nötig':
        'Accesso necessario',
    'keine Client-ID':
        'nessun client ID',
    'Suche leeren':
        'Cancella ricerca',
    'Runden · BP/h erst mit Match-Daten':
        'round · BP/h richiede i dati partita',
    'Verbindung prüfen …':
        'Controlla connessione …',
    'Öffnet Einstellungen → Verbindungen: OBS-Verbindung (Port, Passwort) und „Verbindung testen“.':
        'Apre Impostazioni → Connessioni: la connessione OBS (porta, password) e «Prova connessione».',
    '{n} Marken':
        '{n} segni',
    '1 Marke':
        '1 segno',
    'Keine Aufnahme passt zu den Filtern oben.':
        'Nessuna registrazione corrisponde ai filtri sopra.',
    'Kein Clip passt zu den Filtern oben.':
        'Nessuna clip corrisponde ai filtri sopra.',
    'Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.':
        'Nessuna riga – il log è vuoto, oppure la ricerca e le categorie nascondono tutto.',
    'OBS nicht verbunden':
        'OBS non connesso',
    'Kills, Entkommen und Bloodpoints zählen hier ohne Custom Games – die Rolle „Custom Games“ zeigt sie.':
        'Qui uccisioni, fughe e Punti Sangue contano senza partite personalizzate – il ruolo «Partite personalizzate» le mostra.',
    'Keine Runden in dieser Auswahl – „Filter zurücksetzen“ zeigt wieder alle.':
        'Nessun round in questa selezione – «Ripristina filtri» li mostra di nuovo tutti.',
    'In dieser Auswahl ist keine Runde einem Match der Stats-Seite zugeordnet – darum fehlen Kills, Entkommen und Bloodpoints.':
        'Nessun round di questa selezione è collegato a una partita della pagina statistiche – per questo mancano uccisioni, fughe e Punti Sangue.',
    'Kills, Entkommen und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'Uccisioni, fughe e Punti Sangue arrivano dalla pagina statistiche – per questo configura una volta i dati partita.',
    'Nicht gezählt: {n} × Rundenende nicht erkannt (die nächste Map kam, bevor das Ende erkannt wurde). Zuletzt: {map}, {when}.':
        'Non contati: {n} × fine round non rilevata (la mappa successiva è arrivata prima che la fine fosse rilevata). Ultimo: {map}, {when}.',
    '{n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '{n} × fine round non rilevata, ma contata con la durata dalla pagina statistiche.',
    '{n} × Map mitten im Match falsch erkannt (laut Stats-Seite lief da schon ein Match) – nicht gezählt. Zuletzt: {map}, {when}.':
        '{n} × mappa letta male a metà partita (la pagina statistiche aveva già una partita in corso) – non contati. Ultimo: {map}, {when}.',
    'Keine Map passt zu „{text}“. Gesucht wird in Map- und Realm-Namen aller Spielsprachen und in Abkürzungen.':
        'Nessuna mappa corrisponde a «{text}». La ricerca guarda i nomi di mappe e Realm in ogni lingua di gioco e le abbreviazioni.',
    'Leert das Suchfeld und zeigt wieder alle Maps.':
        'Svuota il campo di ricerca e mostra di nuovo tutte le mappe.',
    'Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter „Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) – die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose.':
        "Ogni spunta è un punto in cui Claude aiuta su tuo clic – mai da solo, mai mentre scrivi: la ricerca (riga «Chiedi a Claude»: la tua domanda e i nomi di impostazioni, pagine e azioni), le domande sulle statistiche (conteggi e percentuali), l'editor di clip («Modifica con Claude»: la tua richiesta e il montaggio come numeri, con la sua spunta anche un fermo immagine) e l'editor di immagini (scheda «Claude»: la tua richiesta e l'immagine). Claude si limita a suggerire; nulla viene eseguito finché non lo scegli o confermi con «Applica». Mai inviati: round, mappe, Killer, percorsi, nomi di file, server o il log. Richiede una tua chiave API dalla Anthropic Console («Ottieni chiave API»); l'API si paga con credito, separatamente da un abbonamento Claude («Aggiungi credito», lì si può impostare un limite di spesa) – il programma stima il costo di ogni domanda dalla risposta e lo somma per mese. La chiave è salvata su questo PC con la crittografia di Windows (se non riesce, dura finché non esci) e non finisce mai nel backup, nel log o nella diagnostica.",
    'Zeigt in der Musikkarte, was in Spotify als Nächstes kommt (Position und Anzahl unter Overlay → Musik). Die Windows-Mediensteuerung kennt nur den laufenden Titel, die Liste holt das Programm deshalb von Spotify selbst: Dafür im Developer-Dashboard „Create app“ anlegen (Name frei, API „Web API“), als Redirect URI genau {uri} eintragen, die Client-ID kopieren und hier einfügen, dann „Mit Spotify verbinden“ – der Browser fragt einmal nach der Freigabe. Gelesen wird nur die Warteschlange, nichts gesteuert; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden) und lässt sich hier trennen. Titel kommen nie ins Log.':
        "Mostra sulla scheda musicale cosa viene dopo in Spotify (posizione e numero in Overlay → Musica). I controlli multimediali di Windows conoscono solo il brano attuale, quindi il programma prende l'elenco da Spotify stesso: nella dashboard sviluppatori «Create app» (nome qualsiasi, API «Web API»), inserisci esattamente {uri} come URI di reindirizzamento, copia il Client ID e incollalo qui, poi «Connetti a Spotify» – il browser chiede una volta il tuo consenso. Viene letta solo la coda, nulla viene controllato; il consenso è salvato con la crittografia di Windows su questo PC (se non è disponibile, dura solo finché non esci) e può essere rimosso qui. I titoli non finiscono mai nel log.",
    'Lädt Clips (F8 und Editor) von selbst auf deinen YouTube-Kanal, Runden nur auf Wunsch: Rechtsklick oder „Auf YouTube hochladen“ unter Aufnahmen. Dafür einmal in der Google Cloud Console ein Projekt anlegen, „YouTube Data API v3“ aktivieren, unter „Anmeldedaten“ einen OAuth-Client vom Typ „Desktop-App“ erstellen und den Zustimmungsbildschirm veröffentlichen (sonst läuft die Anmeldung nach 7 Tagen ab); Client-ID und Client-Secret hier einfügen oder die heruntergeladene JSON-Datei laden, dann „Mit YouTube verbinden“ – der Browser fragt einmal nach der Freigabe. Google erlaubt mit dem Standardkontingent etwa sechs Uploads am Tag; was nicht mehr passt, wartet in der Warteschlange bis zum nächsten Tag. Hochgeladen wird nur, wenn du weder in einer Lobby noch in einer Runde bist; die Datei bleibt immer auch auf der Platte. Gesendet werden nur die Videodatei, Titel (Map, Killer, Datum) und Beschreibung – nie Spielernamen; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden). Mit „Uploads in Playlists einsortieren“ kommt jedes Video zusätzlich in eine Playlist deiner Wahl – dafür fragt die Anmeldung die breitere Berechtigung „YouTube-Konto verwalten“ an (einmal neu verbinden).':
        "Carica da sole le clip (F8 ed editor) sul tuo canale YouTube, i round solo su richiesta: clic destro o «Carica su YouTube» in Registrazioni. Per questo crea una volta un progetto nella console Google Cloud, attiva «YouTube Data API v3», crea in «Credenziali» un client OAuth di tipo «App desktop» e pubblica la schermata di consenso (altrimenti l'accesso scade dopo 7 giorni); incolla qui client ID e client secret o carica il file JSON scaricato, poi «Connetti a YouTube» – il browser chiede una volta il tuo consenso. Con la quota predefinita Google consente circa sei caricamenti al giorno; ciò che non ci sta aspetta in coda fino al giorno dopo. I caricamenti avvengono solo quando non sei né in una lobby né in un round; il file resta sempre anche sul disco. Vengono inviati solo il file video, un titolo (mappa, Killer, data) e una descrizione – mai nomi dei giocatori; il consenso è salvato con la crittografia di Windows su questo PC (se non è disponibile, dura solo finché non esci). Con «Ordina i caricamenti in playlist» ogni video va anche in una playlist a tua scelta – per questo l'accesso chiede il permesso più ampio «Gestire il tuo account YouTube» (connettiti ancora una volta).",
    'Liest Client-ID und Client-Secret aus der Datei „client_secret_….json“, die Google nach dem Anlegen des OAuth-Clients zum Herunterladen anbietet („JSON herunterladen“). Die Datei wird nur gelesen und bleibt, wo sie ist; das Secret landet mit der Windows-Verschlüsselung in den Einstellungen (sonst gilt es nur bis zum Beenden).':
        "Legge client ID e client secret dal file «client_secret_….json» che Google offre da scaricare dopo aver creato il client OAuth («Scarica JSON»). Il file viene solo letto e resta dov'è; il secret va nelle impostazioni con la crittografia di Windows (altrimenti dura solo finché non esci).",
    'Öffnet die Google-Anmeldung im Browser (nur Recht „Videos hochladen“). Danach kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe mit der Windows-Verschlüsselung auf diesem PC (sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf einem freien Port.':
        "Apre l'accesso Google nel browser (solo il diritto «caricare video»). Il browser torna poi a 127.0.0.1 e il programma conserva il consenso con la crittografia di Windows su questo PC (altrimenti solo finché non esci). Per farlo ascolta una volta su una porta libera, solo durante l'accesso.",
    'Öffnet die Spotify-Anmeldung im Browser. Nach dem Zustimmen kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe (mit der Windows-Verschlüsselung, nur auf diesem PC – sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf diesem Port.':
        "Apre l'accesso Spotify nel browser. Dopo il tuo consenso, il browser torna a 127.0.0.1 e il programma conserva il consenso (con la crittografia di Windows, solo su questo PC – altrimenti solo finché non esci). Per farlo ascolta una volta su questa porta, solo durante l'accesso.",
    '({how})':
        '({how})',
    'Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird er nicht gespeichert.':
        'Claude: la chiave API dura solo finché non esci – la crittografia di Windows non è disponibile, quindi non viene salvata.',
    'Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu eintragen oder „Key löschen“.':
        'Claude: la chiave salvata non può essere letta su questo PC – inseriscila di nuovo o usa «Elimina chiave».',
    'OBS-Passwort gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'La password di OBS dura solo finché non esci – la crittografia di Windows non è disponibile, quindi non viene salvata.',
    'OBS-Passwort ist nicht verschlüsselt gespeichert – die Windows-Verschlüsselung ist nicht verfügbar.':
        'La password di OBS è salvata senza crittografia – la crittografia di Windows non è disponibile.',
    'Spotify: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'Spotify: connesso – solo finché non esci, la crittografia di Windows non è disponibile.',
    'Unverschlüsselt gespeichert (von früher, die Windows-Verschlüsselung ist nicht verfügbar): {names}.':
        'Salvati senza crittografia (da prima, la crittografia di Windows non è disponibile): {names}.',
    'YouTube: Client-Secret gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'YouTube: il client secret dura solo finché non esci – la crittografia di Windows non è disponibile, quindi non viene salvato.',
    'YouTube: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'YouTube: connesso – solo finché non esci, la crittografia di Windows non è disponibile.',
    'nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar':
        'solo per questa sessione – la crittografia di Windows non è disponibile',
    'unverschlüsselt gespeichert (alt)':
        'salvato senza crittografia (vecchio)',
    'verschlüsselt gespeichert':
        'salvato con crittografia',
    'Befehlspalette':
        'Riquadro comandi',
    'Suchen':
        'Cerca',
    'Vorschläge':
        'Suggerimenti',
    'OBS-Verbindung':
        'Connessione OBS',
    'Port und Passwort von OBS stehen unter Verbindungen → OBS-Verbindung.':
        'Porta e password di OBS sono in Connessioni → Connessione OBS.',
    'Qualität: {word} – {mbps} Mbit/s bei {size}':
        'Qualità: {word} – {mbps} Mbit/s a {size}',
    'Qualität: Einstellungen prüfen':
        'Qualità: controlla le impostazioni',
    'Qualität: gemessen wird während einer Aufnahme':
        'Qualità: misurata durante la registrazione',
    '{words} (letzte Aufnahme)':
        '{words} (ultima registrazione)',
    'gut':
        'buona',
    'knapp':
        'al limite',
    'matschig':
        'impastata',
    'Einstellungen prüfen':
        'controlla le impostazioni',
    'Qualität verbessern …':
        'Migliora qualità …',
    'OBS-Werte zurücksetzen':
        'Ripristina valori OBS',
    'Aufnahmequalität':
        'Qualità di registrazione',
    'In OBS einstellen':
        'Imposta in OBS',
    'Empfohlen (in OBS einzustellen):':
        'Consigliato (imposta in OBS):',
    'Diese Werte lassen sich nur in OBS selbst einstellen – Fog Scout zeigt, wo.':
        'Questi valori si possono impostare solo in OBS stesso – Fog Scout mostra dove.',
    'Einstellen geht erst nach der Aufnahme.':
        'Le impostazioni si possono cambiare solo dopo la registrazione.',
    'Fog Scout stellt in OBS ein (die alten Werte werden gemerkt):':
        'Fog Scout imposta in OBS (i vecchi valori vengono conservati):',
    'Die OBS-Werte von vor „In OBS einstellen“ wiederherstellen?':
        'Ripristinare i valori di OBS di prima di «Imposta in OBS»?',
    'Nichts einzustellen.':
        'Niente da impostare.',
    'OBS nimmt gerade auf – Qualität erst nach der Aufnahme einstellen.':
        'OBS sta registrando – cambia la qualità dopo la registrazione.',
    'In OBS eingestellt – OBS einmal neu starten, damit alle Werte sicher gelten.':
        'Impostato in OBS – riavvia OBS una volta perché ogni valore abbia sicuramente effetto.',
    'OBS-Einstellungen zurückgesetzt.':
        'Impostazioni OBS ripristinate.',
    'OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ ist viel schärfer.':
        'OBS registra con la qualità «uguale alla diretta» o «piccola» – «Qualità indistinguibile» è molto più nitida.',
    'OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.':
        "OBS riduce l'immagine ({base} → {out}) – questo la rende morbida.",
    'OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.':
        'OBS registra a {fps} fotogrammi al secondo – 60 appaiono molto più nitidi in movimento.',
    'Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen.':
        "L'encoder CPU non riesce a stare al passo (fotogrammi saltati) – usa l'encoder della scheda grafica.",
    'Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf CQP 18 stellen (siehe Anleitung).':
        "Il bitrate è troppo basso per questa immagine – imposta il controllo della frequenza dell'encoder su CQP 18 (vedi i passi).",
    'Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf.':
        "Il bitrate basta appena – con CQP 18 l'immagine resta nitida anche nelle scene veloci.",
    'Ausgabeauflösung = Basisauflösung ({size})':
        'Risoluzione di uscita = risoluzione di base ({size})',
    'Bildrate 60':
        'Frequenza fotogrammi 60',
    'Aufnahmequalität „Kaum unterscheidbare Qualität“':
        'Qualità di registrazione «Qualità indistinguibile»',
    'Aufnahme nicht mehr herunterskalieren':
        'Smetti di ridimensionare la registrazione',
    'OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:':
        'OBS → Impostazioni → Uscita (modalità «Semplice») → Registrazione:',
    'Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“':
        'Qualità di registrazione: «Qualità indistinguibile, file di grandi dimensioni»',
    'Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden':
        'Encoder: hardware (NVENC/AMD/QSV) se disponibile',
    'Aufnahmeformat: MKV oder Hybrid-MP4':
        'Formato di registrazione: MKV o MP4 ibrido',
    'Video: Ausgabeauflösung = Basisauflösung, Bildrate 60':
        'Video: risoluzione di uscita = risoluzione di base, frequenza fotogrammi 60',
    'OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:':
        'OBS → Impostazioni → Uscita (modalità «Avanzata») → scheda «Registrazione»:',
    'Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Codificatore video: NVIDIA NVENC H.264 o HEVC (non «Usa il codificatore della diretta»)',
    'Ausgabe neu skalieren: aus':
        "Ridimensiona l'uscita: off",
    'x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast':
        'x264: controllo frequenza CRF, valore 18, preset veryfast',
    'Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)':
        'Controllo frequenza: CQP, livello CQ 18 (HEVC 20)',
    'Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei Durchläufe (Viertelauflösung)':
        'Preset: P5: Slow (good quality), tuning: high quality, multipass: two passes (quarter resolution)',
    'Profil: high (HEVC: main), Keyframe-Intervall: 2 s':
        'Profilo: high (HEVC: main), intervallo fotogrammi chiave: 2 s',
    'Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.':
        'Poi registra un round breve – la scheda mostra il nuovo bitrate.',
    'Was die Aufnahme unscharf macht und wie OBS am besten eingestellt wird – was eine Anfrage setzen kann (Ausgabeauflösung, Bildrate, einfache Aufnahmequalität), stellt „In OBS einstellen“ ein, die alten Werte werden gemerkt.':
        'Cosa rende sfocata la registrazione e come configurare al meglio OBS – ciò che una richiesta può impostare (risoluzione di uscita, frequenza fotogrammi, qualità di registrazione semplice) lo imposta «Imposta in OBS», i vecchi valori vengono conservati.',
    'Stellt die OBS-Werte von vor „In OBS einstellen“ wieder her.':
        'Ripristina i valori di OBS di prima di «Imposta in OBS».',
    'Clips und Editor':
        'Clip ed editor',
    'Erklärung':
        'Spiegazione',
    'Sicherung und Ordner':
        'Backup e cartelle',
    'Wann aufgenommen wird':
        'Quando registrare',
    'Video-Encoder: AMD HW H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Codificatore video: AMD HW H.264 o HEVC (non «Usa il codificatore della diretta»)',
    'Frequenzsteuerung: CQP, QP-Werte 18 (HEVC 20)':
        'Controllo frequenza: CQP, valori QP 18 (HEVC 20)',
    'Voreinstellung: Qualität':
        'Preset: Quality',
    'Video-Encoder: QuickSync H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Codificatore video: QuickSync H.264 o HEVC (non «Usa il codificatore della diretta»)',
    'Frequenzsteuerung: ICQ (oder CQP), Wert 18':
        'Controllo frequenza: ICQ (o CQP), valore 18',
    'Target Usage: TU1 bis TU4 – kleiner = bessere Qualität':
        'Target usage: da TU1 a TU4 – più basso = qualità migliore',
    'Video-Encoder: der Grafikkarten-Encoder (NVENC, AMF oder QuickSync), wenn OBS einen anbietet – sonst x264':
        "Codificatore video: l'encoder della scheda grafica (NVENC, AMF o QuickSync) se OBS ne offre uno – altrimenti x264",
    'Video-Encoder: einen eigenen wählen (nicht „Stream-Encoder verwenden“), am besten den der Grafikkarte, wenn OBS einen anbietet':
        'Codificatore video: scegline uno proprio (non «Usa il codificatore della diretta»), meglio quello della scheda grafica se OBS ne offre uno',
    'Frequenzsteuerung: gleichbleibende Qualität (CQP, CQ, ICQ oder CRF) um 18 statt einer festen niedrigen Bitrate':
        'Controllo frequenza: qualità costante (CQP, CQ, ICQ o CRF) intorno a 18 invece di un bitrate fisso basso',
    'Einschätzung aus Bitrate, Auflösung, Bildrate und Codec – Bildinhalt, Bewegung, Encoder-Voreinstellung und Quelle beeinflussen das Ergebnis.':
        "Una stima da bitrate, risoluzione, frequenza fotogrammi e codec – contenuto dell'immagine, movimento, preset dell'encoder e sorgente cambiano il risultato.",
    'Start und Meldungen':
        'Avvio e notifiche',
    'Fog Scout kann mit Windows starten und still im Infobereich (neben der Uhr) warten, bis DBD läuft. Die Lobby-Meldung sagt dir mit einem Ton, wenn ein Match gefunden wurde.':
        "Fog Scout può avviarsi con Windows e aspettare in silenzio nell'area di notifica (accanto all'orologio) finché DBD non è in esecuzione. La notifica della lobby ti avvisa con un suono quando è stata trovata una partita.",
    'Optional: OBS Studio nimmt jede Runde auf, Fog Scout sagt OBS nur, wann. Ohne OBS einfach „Weiter“.':
        'Facoltativo: OBS Studio registra ogni round, Fog Scout dice solo a OBS quando. Senza OBS basta «Avanti».',
    '1. In OBS: Werkzeuge → WebSocket-Servereinstellungen → „WebSocket-Server aktivieren“ anhaken; unter „Verbindungsinformationen anzeigen“ stehen Port und Passwort.':
        '1. In OBS: Strumenti → Impostazioni server WebSocket → spunta «Abilita server WebSocket»; «Mostra informazioni di connessione» mostra porta e password.',
    '2. Port und Passwort hier eintragen und „Verbindung testen“.':
        '2. Inserisci qui porta e password e fai clic su «Prova connessione».',
    '3. Einen Ordner für die Aufnahmen wählen und die Aufnahmen einschalten.':
        '3. Scegli una cartella per le registrazioni e attiva la registrazione.',
    'Wie scharf OBS aufnimmt, zeigt danach die Karte „Aufnahme“ auf der Seite Aufnahmen – dort auch „Qualität verbessern …“.':
        "Quanto nitido registra OBS lo mostra poi la scheda «Registrazione» nella pagina Registrazioni – lì c'è anche «Migliora qualità …».",
    'Alles hier ist freiwillig und lässt sich später unter Einstellungen → Verbindungen einrichten. Jede Verbindung braucht eine eigene App-ID bzw. einen eigenen Key von dir – „Erklärung“ sagt, wo es sie gibt.':
        'Tutto qui è facoltativo e può essere configurato più tardi in Impostazioni → Connessioni. Ogni connessione richiede un tuo ID app o una tua chiave – «Spiegazione» dice dove ottenerli.',
    'Fog Scout kann anzeigen, mit welchem Spielserver DBD verbunden ist (Region und Ping, auch im Overlay) – dafür fragt Windows einmal nach Administratorrechten.':
        "Fog Scout può mostrare a quale server di gioco è connesso DBD (regione e ping, anche nell'overlay) – per questo Windows chiede una volta i diritti di amministratore.",
    'Auf der Seite Server lässt sich ausserdem festlegen, in welchen Regionen DBD Matches sucht. Das ist freiwillig.':
        'Nella pagina Server puoi anche scegliere in quali regioni DBD cerca partite. È facoltativo.',
    'Serverregionen auswählen …':
        'Scegli regioni server …',
    'Beendet die Einrichtung und öffnet die Seite Server – dort die Regionen anhaken, in denen DBD Matches suchen soll.':
        'Termina la configurazione e apre la pagina Server – spunta lì le regioni in cui DBD deve cercare partite.',
    'Öffnet den Ordner mit Einstellungen, Runden, Log und Sicherungen im Explorer.':
        'Apre in Esplora file la cartella con impostazioni, round, log e backup.',
    'Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an Claude schicken“ einschalten und einen API-Key eintragen.':
        "Off – attiva «Invia a Claude le immagini nell'editor di immagini» in Impostazioni → Connessioni → Claude e inserisci una chiave API.",
    'Ausschnitt ausserhalb des Bildes':
        "ritaglio fuori dall'immagine",
    'Bereich unkenntlich machen ({x} %, {y} %)':
        "Nascondi un'area ({x} %, {y} %)",
    'Bilder im Bild-Editor an Claude schicken':
        "Invia a Claude le immagini nell'editor di immagini",
    'Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        'Le immagini possono mostrare nomi dei giocatori – vanno a Claude solo quando fai clic su «Suggerisci», rimpicciolite e solo in memoria; le aree già censurate restano censurate. Le domande sulle statistiche inviano solo conteggi e percentuali per ruolo, Killer, mappa, regione e ora del giorno – nessun singolo round, nessun nome di giocatore.',
    'Claude hat keine Antwort gegeben.':
        'Claude non ha dato alcuna risposta.',
    'Claude zur Statistik fragen: „{q}“':
        'Chiedi a Claude sulle statistiche: «{q}»',
    'Claude: Key eingetragen, Claude ist überall aus.':
        'Claude: chiave inserita, Claude è disattivato ovunque.',
    'Das Bild hat sich inzwischen geändert – bitte neu vorschlagen.':
        "Nel frattempo l'immagine è cambiata – chiedi di nuovo un suggerimento.",
    'Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude (api.anthropic.com), verkleinert und nur im Speicher.':
        "L'immagine può mostrare nomi dei giocatori – va a Claude (api.anthropic.com) solo con un clic, rimpicciolita e solo in memoria.",
    'Das Bild lässt sich nicht für Claude verkleinern.':
        "Impossibile rimpicciolire l'immagine per Claude.",
    'Das Standbild liess sich nicht lesen – nichts gesendet.':
        'Impossibile leggere il fermo immagine – non è stato inviato nulla.',
    'Die Statistik liess sich nicht zusammenfassen – Details im Log.':
        'Impossibile riassumere le statistiche – dettagli nel log.',
    'Drehung ohne Winkel':
        'rotazione senza angolo',
    'Farbe ohne Werte':
        'colore senza valori',
    'Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %':
        'Colore: luminosità {b} %, contrasto {c} %, saturazione {s} %',
    'In der Suche Statistik-Fragen an Claude stellen':
        'Fai domande a Claude sulle statistiche nella ricerca',
    'Kasten ausserhalb des Bildes':
        "riquadro fuori dall'immagine",
    'Kippen':
        'Capovolgi verticalmente',
    'Noch keine Runden – Claude hätte nichts zum Auswerten.':
        'Ancora nessun round – Claude non avrebbe nulla da guardare.',
    'Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du übernimmst.':
        "Invia a Claude la tua richiesta e l'immagine come appare qui (le aree già censurate restano censurate); nulla cambia prima che tu lo applichi.",
    'Schickt die Frage und Zähler/Quoten deiner Runden an Claude – keine einzelne Runde, keine Namen':
        'Invia a Claude la domanda e conteggi/percentuali dei tuoi round – nessun singolo round, nessun nome',
    'Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        "Invia anche l'immagine alla testina (rimpicciolita, le aree già censurate restano censurate) – così Claude può, ad esempio, censurare i nomi. L'immagine può mostrare nomi dei giocatori.",
    'Spiegeln':
        'Specchia',
    'Spiegeln ohne Richtung':
        'specchiatura senza direzione',
    'Standbild mitsenden':
        'Invia anche un fermo immagine',
    'Standbilder aus Aufnahmen im Clip-Editor an Claude schicken':
        "Invia a Claude fermi immagine dalle registrazioni nell'editor di clip",
    'Um {deg}° drehen':
        'Ruota di {deg}°',
    'Vergisst den Vorschlag; das Bild bleibt, wie es ist.':
        "Dimentica il suggerimento; l'immagine resta com'è.",
    'Zensur nur mit Standbild':
        'censura solo con un fermo immagine',
    'Zensur: {style}':
        'Censura: {style}',
    'Zuschneiden auf {w} × {h} %':
        'Ritaglia a {w} × {h} %',
    'unbekannte Art der Zensur':
        'tipo di censura sconosciuto',
    'unbekannter Schritt':
        'passo sconosciuto',
    'z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller':
        "ad es. pixela i nomi dei giocatori, ritaglia a 16:9, un po' più chiara",
    'zu viele Kästen':
        'troppi riquadri',
    'Zeigt im Bild-Editor den Reiter „Claude“: Du schreibst, was mit dem Bild passieren soll (Namen verpixeln, zuschneiden, heller), und auf „Vorschlagen“ gehen Bitte und Bild verkleinert an Claude. Das Bild kann Spielernamen zeigen; bereits zensierte Bereiche bleiben zensiert.':
        "Mostra la scheda «Claude» nell'editor di immagini: scrivi cosa deve succedere all'immagine (pixelare nomi, ritagliare, schiarire) e con «Suggerisci» la tua richiesta e l'immagine rimpicciolita vanno a Claude. L'immagine può mostrare nomi dei giocatori; le aree già censurate restano censurate.",
    'Erlaubt im grossen Clip-Editor das Häkchen „Standbild mitsenden“: dann geht das Bild an der Abspielposition mit, und Claude kann z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        "Consente la spunta «Invia anche un fermo immagine» nel grande editor di clip: l'immagine alla testina viene allora inviata insieme e Claude può, ad esempio, censurare i nomi. L'immagine può mostrare nomi dei giocatori.",
    'Zeigt in der Suche (Strg+F) die Zeile „Claude zur Statistik fragen“. Gesendet werden deine Frage und Zähler/Quoten deiner Runden je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        'Mostra la riga «Chiedi a Claude sulle statistiche» nella ricerca (Ctrl+F). Vengono inviati la tua domanda e conteggi/percentuali dei tuoi round per ruolo, Killer, mappa, regione e ora del giorno – nessun singolo round, nessun nome di giocatore.',
    'Start: Fenster bereit nach {total} s seit Programmstart (davon {before} s bis Python).':
        "Avvio: finestra pronta {total} s dopo l'avvio del programma (di cui {before} s fino a Python).",
    'Haiku 5.5 – am günstigsten':
        'Haiku 5.5 – il più economico',
    'Opus 5.5 – am genauesten':
        'Opus 5.5 – il più preciso',
    'Sonnet 5.5 – halber Preis':
        'Sonnet 5.5 – metà prezzo',
    'Modell':
        'Modello',
    'Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat {month}. Abgerechnet wird in der Anthropic Console.':
        'Costo (stima a prezzo di listino): questa sessione {session} per {n} richieste, questo mese {month}. La fatturazione è nella Anthropic Console.',
    'Claude: Welcher Build läuft am besten?':
        'Claude: Quale build funziona meglio?',
    'Claude: Woche zusammenfassen':
        'Claude: Riassumi la settimana',
    'Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?':
        'Riassumi la mia settimana rispetto alla precedente: cosa è andato meglio, cosa peggio?',
    'Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?':
        'Quali dei miei perk funzionano meglio – Killer e Sopravvissuto separatamente?',
    'Fog Scout ist abgestürzt':
        'Fog Scout si è bloccato',
    'Fog Scout wurde am {when} unerwartet beendet. „Diagnose kopieren“ legt einen Bericht mit den Stellen des Absturzes in die Zwischenablage – zum Melden auf GitHub oder im Chat. Der Bericht enthält keine Schlüssel, Titel oder Server-Adressen.':
        'Fog Scout si è chiuso in modo imprevisto il {when}. «Copia diagnostica» mette negli appunti un rapporto con i punti del crash – per segnalarlo su GitHub o in una chat. Il rapporto non contiene chiavi, titoli o indirizzi di server.',
    'Claude hat keine Stelle gefunden, die heraussticht.':
        'Claude non ha trovato nessun momento che spicchi.',
    'Claude sieht sich {n} Standbilder an …':
        'Claude sta esaminando {n} fermi immagine …',
    'Highlights finden':
        'Trova momenti salienti',
    'Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu drei Stellen für einen Short. Die Bilder können Spielernamen zeigen.':
        'Invia a Claude piccoli fermi immagine del montaggio (distribuiti uniformemente e ai segni F8, le aree già censurate restano censurate); Claude indica fino a tre momenti per uno short. Le immagini possono mostrare nomi dei giocatori.',
    'Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ ändert den Schnitt.':
        'Suggerisce di tenere solo questa parte – solo «Applica» cambia il montaggio.',
    'Namen beim Zuschauen':
        'Nomi in modalità spettatore',
    'Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und den Namen oben in der Mitte – bei Bedarf verschieben.':
        "Mette riquadri sui nomi come DBD li mostra in modalità spettatore: l'elenco a sinistra, più in alto, e il nome in alto al centro – spostali se serve.",
    'Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        "Mette un riquadro dove DBD mostra i nomi dei Sopravvissuti in partita (in basso a sinistra nell'immagine di gioco) – spostalo se serve.",
    'Aufnahme zeigen':
        'Mostra registrazione',
    'Aufnahme abspielen':
        'Riproduci registrazione',
    'Zu dieser Runde gibt es keine Aufnahme.':
        "Non c'è una registrazione di questo round.",
    'Die Aufnahme dieser Runde ist durch die Filter der Seite Aufnahmen ausgeblendet.':
        'La registrazione di questo round è nascosta dai filtri della pagina Registrazioni.',
    'Sitzungen':
        'Sessioni',
    'Killer/Survivor':
        'Killer/Sopravvissuto',
    '{n} K':
        '{n} K',
    '{n} S':
        '{n} S',
    'Ø Dauer einer Sitzung':
        'Ø durata di una sessione',
    'Ø Runden je Sitzung':
        'Ø round per sessione',
    'Ø Warten':
        'Ø attesa',
    'Eine Sitzung endet nach {n} Minuten ohne Runde. Es gelten die Filter oben – mit einem Rollenfilter zählt eine Sitzung nur die Runden dieser Rolle. Ø Kills, Entkommen und BP laut Stats-Seite. Doppelklick zeigt die Runden der Sitzung unter „Letzte Runden“.':
        'Una sessione finisce dopo {n} minuti senza round. Valgono i filtri sopra – con un filtro ruolo una sessione conta solo i round di quel ruolo. Ø uccisioni, fughe e BP dalla pagina statistiche. Un doppio clic mostra i round della sessione in «Ultimi round».',
    'Blutpunkte-Stand – letzter Wert {per}':
        'Saldo Punti Sangue – ultimo valore {per}',
    'Cap erreicht':
        'Limite raggiunto',
    'Cap in ≈ {n} Runden':
        'Limite tra ≈ {n} round',
    'Cap: {cap}':
        'Limite: {cap}',
    'Noch kein Blutpunkte-Stand gelesen – er kommt aus der Lobby nach der Runde.':
        'Ancora nessun saldo di Punti Sangue letto – arriva dalla lobby dopo il round.',
    '{when}: Stand {bp} BP':
        '{when}: saldo {bp} BP',
    '+{n} Level':
        '+{n} livelli',
    '+{n} P':
        '+{n} P',
    'Eine Zeile oben anklicken, um den Verlauf zu sehen.':
        "Fai clic su una riga sopra per vedere l'andamento.",
    'Keine Matches mit Prestige in dieser Auswahl.':
        'Nessuna partita con prestigio in questa selezione.',
    'Level':
        'Livello',
    'Matches':
        'Partite',
    'Noch kein Prestige in dieser Auswahl – es kommt aus den Match-Daten (Userscript ab Version 3).':
        'Ancora nessun prestigio in questa selezione – arriva dai dati partita (userscript versione 3 o più recente).',
    'Prestige':
        'Prestigio',
    'Prestige und Level deiner Charaktere laut Stats-Seite (ab Userscript Version 3). „Prestige“ und „Level“ = der neueste Stand; „Zuwachs“ und „Matches“ gelten für die Filter oben. Eine Zeile anklicken zeigt darunter den Verlauf dieses Charakters. „Tempo“ = gewonnene Level pro Woche aus den Matches der letzten {days} Tage, „Nächstes P“ = wie lange es bei diesem Tempo bis zur nächsten Stufe dauert. Level steigen nur, wenn du Blutpunkte im Blutnetz ausgibst – die Prognose sagt, was bisher geschah, keine Zusage. „Main“ = dein Charakter mit den meisten Matches je Rolle. „P100“ und „Höchster“ zählen nur Charaktere, die in deinen Match-Daten vorkommen.':
        "Prestigio e livello dei tuoi personaggi dalla pagina statistiche (userscript versione 3 o più recente). «Prestigio» e «Livello» = lo stato più recente; «Guadagno» e «Partite» seguono i filtri sopra. Fai clic su una riga per vedere sotto l'andamento di quel personaggio. «Velocità» = livelli guadagnati a settimana dalle partite degli ultimi {days} giorni, «Prossimo P» = quanto richiede il prossimo grado a quel ritmo. I livelli salgono solo quando spendi Punti Sangue nella Rete Sanguinaria – la previsione dice cosa è successo finora, nessuna promessa. «Main» = il tuo personaggio con più partite per ruolo. «P100» e «Massimo» contano solo i personaggi che compaiono nei tuoi dati partita.",
    'Prestige von {name} {per}':
        'Prestigio di {name} {per}',
    'Zuletzt':
        'Ultima partita',
    'Zuwachs':
        'Guadagno',
    '{when}: Prestige {p} · Level {level}':
        '{when}: prestigio {p} · livello {level}',
    '+{n} weitere':
        '+{n} altri',
    'Charaktere':
        'Personaggi',
    'Höchster':
        'Massimo',
    'Level diese Woche':
        'Livelli questa settimana',
    'Main':
        'Main',
    'Meilenstein: {name} ist jetzt Prestige {p}':
        'Traguardo: {name} ora è prestigio {p}',
    'Nächstes P':
        'Prossimo P',
    'P100 erreicht':
        'P100 raggiunto',
    'Prestige gesamt':
        'Prestigio totale',
    'alle Charaktere':
        'tutti i personaggi',
    'seit Montag':
        'da lunedì',
    '{k} Killer · {s} Survivor':
        '{k} Killer · {s} Sopravvissuto',
    '{name} ist jetzt Prestige {p}':
        '{name} ora è prestigio {p}',
    '{name} · Level {level}':
        '{name} · livello {level}',
    '{n} Level/Woche':
        '{n} livelli/settimana',
    '≈ 1 Tag':
        '≈ 1 giorno',
    '≈ 1 Woche':
        '≈ 1 settimana',
    '≈ {n} Tage':
        '≈ {n} giorni',
    '≈ {n} Wochen':
        '≈ {n} settimane',
    '{n} Charaktere':
        '{n} personaggi',
    'P100':
        'P100',
    '{n}× Killer':
        '{n}× Killer',
    '{n}× Survivor':
        '{n}× Sopravvissuto',
    '{n}× Farming':
        '{n}× farming',
    '{n}× Custom Game':
        '{n}× partita personalizzata',
    '{n}× ohne Rolle':
        '{n}× senza ruolo',
    'Zeigt, was diese Kachel zählt':
        'Mostra cosa conta questo riquadro',
    'Diese Runden sind durch die Filter der Statistik ausgeblendet.':
        'Questi round sono nascosti dai filtri delle statistiche.',
    'Automatisch (zuletzt benutztes Gerät)':
        'Automatico (ultimo dispositivo usato)',
    'Dunkle Fläche hinter den Eingaben':
        'Area scura dietro gli input',
    'EINGABEN':
        'INPUT',
    'Eingaben im Spiel':
        'Input nel gioco',
    'Eingaben im Spiel zeigen (Tasten, Maus, Gamepad)':
        'Mostra gli input nel gioco (tasti, mouse, gamepad)',
    'Gamepad':
        'Gamepad',
    'Gerät':
        'Dispositivo',
    'Tastatur und Maus':
        'Tastiera e mouse',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter den Tasten.':
        "Un'area scura semitrasparente con angoli arrotondati dietro i tasti.",
    'wartet auf eine Runde':
        'in attesa di un round',
    'Eingaben mit der Aufnahme speichern (für den Clip-Editor)':
        "Salva gli input con la registrazione (per l'editor di clip)",
    'Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). Eine offizielle Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.':
        "Fog Scout mostra solo quali di questi tasti sono premuti in questo momento: W, A, S, D, Q, E, R, Space, Shift, Ctrl, i pulsanti del mouse e un gamepad (pulsanti, grilletti, levette). Vengono letti solo durante un round e solo mentre DBD è la finestra attiva – Fog Scout non vede mai ciò che scrivi in altri programmi. Nulla viene registrato nel log o inviato, e nulla va al gioco; con «Salva gli input con la registrazione» i tasti di un round vengono conservati come file accanto alla sua registrazione OBS (per l'editor di clip). Behaviour non ha approvato ufficialmente queste visualizzazioni; non danno alcun vantaggio nel gioco.",
    'Gelesen werden nur W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad – nur während einer Runde und nur, solange DBD vorne ist. Gesendet wird nichts; gespeichert nur mit dem Häkchen oben, als Datei neben der eigenen Aufnahme.':
        'Vengono letti solo W, A, S, D, Q, E, R, Space, Shift, Ctrl, i pulsanti del mouse e un gamepad – solo durante un round e solo mentre DBD è in primo piano. Nulla viene inviato; salvato solo con la casella sopra, come file accanto alla tua registrazione.',
    'Eine Karte im Spiel zeigt, welche Tasten, Maustasten oder Gamepad-Knöpfe du gerade drückst – wie bei Streamern. Gelesen wird nur eine feste Liste von Tasten, nur während einer Runde und nur, solange DBD vorne ist; gesendet wird nichts, gespeichert nur mit „Eingaben mit der Aufnahme speichern“.':
        'Una scheda nel gioco mostra quali tasti, pulsanti del mouse o del gamepad stai premendo in questo momento – come fanno gli streamer. Viene letto solo un elenco fisso di tasti, solo durante un round e solo mentre DBD è in primo piano; nulla viene inviato, salvato solo con «Salva gli input con la registrazione».',
    'Mit OBS-Aufnahmen: die gedrückten Tasten der Runde kommen als kleine Datei neben die Aufnahme – der Clip-Editor zeigt sie als Spur und kann die Karte ins Video einbrennen. Die Datei wird mit der Aufnahme verschoben und gelöscht.':
        "Con le registrazioni OBS: i tasti premuti durante il round finiscono in un piccolo file accanto alla registrazione – l'editor di clip li mostra come traccia e può imprimere la scheda nel video. Il file viene spostato ed eliminato con la registrazione.",
    'Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme speichern“). Clips aus F8 haben keine.':
        'Dal file accanto alla registrazione (Overlay › Input › «Salva gli input con la registrazione»). Le clip F8 non ne hanno.',
    'Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet).':
        "La scheda con i tasti premuti nel round finisce nel video finito – nell'angolo scelto, a tempo con il montaggio (velocità e riproduzione all'indietro comprese).",
    'Dunkle Fläche hinter den Tasten':
        'Area scura dietro i tasti',
    'Ecke':
        'Angolo',
    'Eine halb durchsichtige dunkle Fläche hinter der Karte.':
        "Un'area scura semitrasparente dietro la scheda.",
    'Eingaben im Export zeigen':
        "Mostra gli input nell'esportazione",
    'Höhe der Karte im Verhältnis zur Bildhöhe.':
        "Altezza della scheda rispetto all'altezza dell'immagine.",
    'Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade benutzt wurde.':
        'Quale vista mostra la scheda – automaticamente il dispositivo appena usato.',
    'Wo die Karte im Bild liegt.':
        "Dove sta la scheda nell'immagine.",
    'Claude baut einen Short aus {n} Standbildern …':
        'Claude sta costruendo uno short da {n} fermi immagine …',
    'Clip um Moment':
        'Clip intorno al momento',
    'Der Schnitt hat sich inzwischen geändert – bitte noch einmal.':
        'Nel frattempo il montaggio è cambiato – riprova.',
    'Der Schnitt wird der markierte Moment ({before} s davor bis {after} s danach).':
        'Il montaggio diventa il momento selezionato (da {before} s prima a {after} s dopo).',
    'Die Bilder liessen sich nicht lesen.':
        'Impossibile leggere le immagini.',
    'F8-Marke':
        'Segno F8',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden.':
        'Non possibile ora – termina prima la modifica in corso.',
    'Kein Ladebildschirm am Anfang oder Ende gefunden.':
        "Nessuna schermata di caricamento trovata all'inizio o alla fine.",
    'Kein Leerlauf gefunden.':
        'Nessun tratto inattivo trovato.',
    'Ladebildschirm abschneiden':
        'Taglia la schermata di caricamento',
    'Leerlauf kürzen':
        'Taglia i tempi morti',
    'Momente':
        'Momenti',
    'Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst „Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen.':
        'Invia a Claude fermi immagine nei momenti trovati (da tasti, audio del gioco e segni F8, solo come numeri) e il montaggio; Claude propone uno short completo – intervallo, rallentatore, titolo, sottotitoli. Solo «Applica» cambia il montaggio. Le immagini possono mostrare nomi dei giocatori.',
    'Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war (aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.':
        'Taglia i tratti in cui nulla è stato premuto per almeno {n} s (dagli input della registrazione) – un passo da annullare.',
    'Sehe mir Anfang und Ende an …':
        "Esame dell'inizio e della fine …",
    'Short vorschlagen':
        'Suggerisci uno short',
    'Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.':
        'Esamina i primi e gli ultimi {n} s e taglia via un inizio o una fine neri – un passo da annullare.',
    'laut':
        'rumoroso',
    'viele Tasten':
        'molti tasti',
    '{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z macht es rückgängig.':
        '{n} tratti inattivi tagliati ({seconds} s) – Ctrl+Z lo annulla.',
    '{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – Strg+Z macht es rückgängig.':
        '{n} tratti neri tagliati ({seconds} s) – Ctrl+Z lo annulla.',
    'Anordnen':
        'Disponi',
    'Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · Tab = nächstes Element · Esc = fertig':
        'Disposizione – anche nel gioco: trascina gli elementi · frecce = di precisione (Shift = 10 px) · Tab = elemento successivo · Esc = fatto',
    'Anordnen: alle Elemente mit der Maus ziehen – in der Vorschau und direkt im Spiel. Strg+Mausrad ändert die Grösse, Esc beendet.':
        "Disponi: trascina ogni elemento col mouse – nell'anteprima e direttamente nel gioco. Ctrl+rotellina cambia la dimensione, Esc termina.",
    'Automatisch: im schwarzen Rand neben dem Spielbild bzw. neben dem DBD-Fenster. Frei platzieren: „Anordnen“ oder eine Schnellposition.':
        "Automatico: nel bordo nero accanto all'immagine di gioco o accanto alla finestra di DBD. Per posizionarlo liberamente: «Disponi» o un posto rapido.",
    'CPU, GPU, RAM':
        'CPU, GPU, RAM',
    'Callout-Karte der Map':
        'La mappa callout della mappa',
    'Die Linien in der Vorschau mit „Anordnen“ ziehen – Karte, Systemwerte, Heute und Musik bleiben im Balken dazwischen.':
        "Trascina le linee nell'anteprima con «Disponi» – mappa, valori di sistema, oggi e musica restano tra di esse nella barra.",
    'Ein- oder ausblenden':
        'Mostra o nascondi',
    'Elemente':
        'Elementi',
    'Entsperren: wieder verschiebbar':
        'Sblocca: può essere spostato di nuovo',
    'Fokus':
        'Focus',
    'Frei platzieren: „Anordnen“, eine Schnellposition oder Vorgabe „eigene Position“.':
        "Per posizionarlo liberamente: «Disponi», un posto rapido o l'impostazione «posizione personalizzata».",
    'Gesperrt – erst entsperren':
        'Bloccato – prima sbloccalo',
    'Gilt für alle Elemente':
        'Vale per ogni elemento',
    'Grenzen und Platz':
        'Limiti e spazio',
    'Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen':
        'Linea limite: trascinala fin dove gli elementi nella barra possono arrivare',
    'Grösse und Deckkraft':
        'Dimensione e opacità',
    'Grösse von {name}: Ecke ziehen':
        "Dimensione di {name}: trascina l'angolo",
    'Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, Rechtsklick = Menü. Ende mit „Fertig“ oder Esc.':
        'Un clic su un elemento lo seleziona. Con «Disponi»: trascina un elemento = spostalo (la cornice tratteggiata mostra dove finisce), trascina il suo angolo o Ctrl+rotellina = dimensione, clic destro = menu. Termina con «Fatto» o Esc.',
    'Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel':
        'Un clic seleziona un elemento · «Disponi» attiva lo spostamento – qui e nel gioco',
    'Klick wählt {name}':
        'Un clic seleziona {name}',
    'Layout für {size}':
        'Layout per {size}',
    'Läuft gerade':
        'In riproduzione',
    'Mitte':
        'centro',
    'Nach {where} legen (mit Rand)':
        'Mettilo {where} (con un margine)',
    'Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein).':
        'Posizione e dimensione sono conservate per dimensione della finestra di DBD (scheda Generale).',
    'Runden und Zeit heute':
        'Round e tempo di oggi',
    'Schnellposition':
        'Posto rapido',
    'Sperren':
        'Blocca',
    'Sperren: im Modus „Anordnen“ nicht mehr verschiebbar':
        'Blocca: non viene più spostato in «Disponi»',
    'Stil, Abstand, Grenzen, Discord':
        'Stile, distanza, limiti, Discord',
    'Tasten und Gamepad':
        'Tasti e gamepad',
    'Timer, Bilanz, Server':
        'Timer, record, server',
    'Verhalten':
        'Comportamento',
    'Zeilen':
        'Righe',
    'Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)':
        'Torna al posto automatico (nella barra nera, accanto agli altri)',
    'eigener Platz':
        'posto proprio',
    'eingerastet':
        'agganciato',
    'graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        'linee grigie nelle barre = limiti (off) – trascinarne una li attiva',
    'links Mitte':
        'centro sinistra',
    'oben Mitte':
        'centro in alto',
    'rastet an Mitte, Balken und anderen ein (Alt = frei)':
        'si aggancia al centro, alle barre e agli altri (Alt = libero)',
    'rechts Mitte':
        'centro destra',
    'unten Mitte':
        'centro in basso',
    '{name} entsperrt.':
        '{name} sbloccato.',
    '{name} gesperrt – bleibt beim Anordnen, wo es ist.':
        "{name} bloccato – resta dov'è durante la disposizione.",
    '{name} ist gesperrt – das Schloss in der Liste löst es':
        "{name} è bloccato – il lucchetto nell'elenco lo libera",
    '{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü':
        '{name}: trascina = sposta · angolo o Ctrl+rotellina = dimensione · clic destro = menu',
    'Üblicher Platz':
        'Posto abituale',
    '„Overlay testen“ zeigt die Karte sofort, mit „Anordnen“ ziehst du sie hin.':
        '«Prova overlay» mostra subito la mappa, con «Disponi» la trascini lì.',
    'Nur die Vorschau: Liste und Einstellungen weg, die Navigation schmal – die ganze Fläche zum Anordnen. Esc oder nochmal klicken beendet es.':
        "Solo l'anteprima: elenco e impostazioni via, la navigazione stretta – tutta l'area per disporre. Esc o un altro clic la termina.",
    'Englisch':
        'Inglese',
    'Deutsch':
        'Tedesco',
    'Französisch':
        'Francese',
    'Spanisch':
        'Spagnolo',
    'Spanisch (Mexiko)':
        'Spagnolo (Messico)',
    'Italienisch':
        'Italiano',
    'Polnisch':
        'Polacco',
    'Portugiesisch (Brasilien)':
        'Portoghese (Brasile)',
    'Türkisch':
        'Turco',
    'Spielsprache selbst erkennen und anhaken':
        'Rileva e spunta da solo la lingua del gioco',
    'Spielsprache {lang} erkannt (Banner „{text}“) – automatisch angehakt.':
        'Lingua del gioco {lang} rilevata (banner «{text}») – spuntata automaticamente.',
    'Läuft DBD in einer Sprache, die hier nicht angehakt ist, und passt ein Map-Banner eindeutig zu einer Map in dieser Sprache, hakt Fog Scout sie selbst an – die Karte erscheint dann schon in derselben Runde. Nur am Rundenstart, nie mitten im Match.':
        "Se DBD è in una lingua non spuntata qui e un banner della mappa corrisponde chiaramente a una mappa in quella lingua, Fog Scout la spunta da solo: la mappa compare già nello stesso round. Solo all'inizio del round, mai a partita in corso.",
    'Russisch':
        'Russo',
    'Chinesisch (vereinfacht)':
        'Cinese (semplificato)',
    'Chinesisch (traditionell)':
        'Cinese (tradizionale)',
    'Japanisch':
        'Giapponese',
    'Koreanisch':
        'Coreano',
}
