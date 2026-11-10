"""Korean texts (1.47): the German text of the code is the key, as in i18n_en.EN – a text missing here
shows in English (i18n.table). Made from the English texts; tests/test_i18n.py checks keys and placeholders."""
T = {
    'Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\nKurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden.':
        'Fog Scout가 이미 실행 중이지만 응답하지 않습니다(또는 종료하는 중입니다).\n\n잠시 기다린 후 다시 시작하세요. 그래도 안 되면 작업 관리자의 ‘세부 정보’에서 ‘{exe}’(Fog Scout)를 종료하세요.',
    'Fog Scout konnte nicht neu gestartet werden: Die alte Kopie läuft noch im Hintergrund.\n\nIm Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden und das Programm neu starten.':
        'Fog Scout를 다시 시작할 수 없습니다: 이전 프로그램이 아직 백그라운드에서 실행 중입니다.\n\n작업 관리자의 ‘세부 정보’에서 ‘{exe}’(Fog Scout)를 종료하고 프로그램을 다시 시작하세요.',
    'Start fehlgeschlagen:':
        '시작 실패:',
    'Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt unverändert.':
        '지금까지 Fog Scout를 start.bat으로 사용했습니다:\n{folder}\n\n설정, 라운드, 매치 데이터, 백업, 직접 추가한 맵 이미지를 설치된 버전으로 가져올까요? 이전 폴더는 그대로 유지됩니다.',
    'Übernahme fehlgeschlagen: {error}':
        '가져오기 실패: {error}',
    'Kein Windows: Fenstersuche, Hotkeys und Click-Through sind nur unter Windows aktiv.':
        'Windows가 아닙니다: 창 검색, 단축키, 클릭 통과는 Windows에서만 작동합니다.',
    'Bereit. {n} Maps geladen, Spielsprachen: {langs}.':
        '준비 완료. 맵 {n}개 로드됨, 게임 언어: {langs}.',
    'Bildschirm {w}×{h} ohne schwarze Balken neben dem Spielbild: Systemwerte, „Heute“ und Musik im Spiel sind ausgeschaltet (sie lägen sonst auf dem Spielbild) – einschalten auf der Seite Overlay.':
        '화면 {w}×{h}에 게임 화면 옆 검은 여백이 없습니다: 게임 내 시스템 값, ‘오늘’, 음악이 꺼졌습니다(게임 화면 위에 표시되기 때문). 오버레이 페이지에서 켤 수 있습니다.',
    'Automatisch (Windows-Sprache)':
        '자동(Windows 언어)',
    'Erkennung':
        '인식',
    'Overlay':
        '오버레이',
    'System':
        '시스템',
    'Fehler':
        '오류',
    'automatisch':
        '자동',
    'oben links':
        '왼쪽 위',
    'oben rechts':
        '오른쪽 위',
    'unten links':
        '왼쪽 아래',
    'unten rechts':
        '오른쪽 아래',
    'eigene Position':
        '사용자 지정 위치',
    'Karte ein/aus':
        '맵 켜기/끄기',
    'Layout-Variante':
        '레이아웃 변형',
    'Bildschirm scannen':
        '화면 스캔',
    'Vorherige Map':
        '이전 맵',
    'Nächste Map':
        '다음 맵',
    'Grösser':
        '크게',
    'Kleiner':
        '작게',
    'Mit Maus verschieben':
        '마우스로 이동',
    'Noch keine Map':
        '아직 맵 없음',
    'Karte ausblenden':
        '맵 숨기기',
    'Karte einblenden':
        '맵 표시',
    'Scannen':
        '스캔',
    'Overlay testen':
        '오버레이 테스트',
    'Test beenden':
        '테스트 종료',
    'Bild hinzufügen …':
        '이미지 추가 …',
    'Zuordnen …':
        '지정 …',
    'Server':
        '서버',
    'Einstellungen':
        '설정',
    'Layout {n} von {total}':
        '레이아웃 {n}/{total}',
    '(unsicher)':
        '(불확실)',
    'manuell gewählt':
        '직접 선택함',
    'per Scan gefunden':
        '스캔으로 찾음',
    'Letzte Runde: {time}':
        '마지막 라운드: {time}',
    'Unbekannte Map gelesen: „{text}“':
        '알 수 없는 맵 이름을 읽음: ‘{text}’',
    'Im Menü – Karte pausiert ({map})':
        '메뉴 화면 – 맵 일시 중지({map})',
    'Runde vorbei – wartet auf das nächste Match':
        '라운드 종료 – 다음 매치를 기다리는 중',
    'Karte ausgeblendet ({map})':
        '맵 숨겨짐({map})',
    'Wartet auf DBD':
        'DBD를 기다리는 중',
    'DBD läuft – automatische Erkennung ist aus (Map von Hand wählen)':
        'DBD 실행 중 – 자동 인식이 꺼져 있습니다(맵을 직접 선택하세요)',
    'Wartet auf das nächste Match':
        '다음 매치를 기다리는 중',
    'Simulation – wartet auf das Map-Banner':
        '시뮬레이션 – 맵 배너를 기다리는 중',
    'Im Match: {map}':
        '매치 중: {map}',
    'Karte eingeblendet':
        '맵 표시됨',
    'Kartenbild hinzufügen …':
        '맵 이미지 추가 …',
    'eigenes Bild für eine Map (Hintergrund wird entfernt)':
        '맵에 쓸 직접 만든 이미지(배경이 제거됨)',
    'Eigene Bilder':
        '내 이미지',
    'Position':
        '위치',
    'Zurücksetzen':
        '초기화',
    'Horizontal':
        '가로',
    'Vertikal':
        '세로',
    'Fertig':
        '완료',
    '0 % = links/oben, 100 % = rechts/unten':
        '0% = 왼쪽/위, 100% = 오른쪽/아래',
    'Karte im schwarzen Rand halten':
        '맵을 검은 여백 안에 유지',
    'Darstellung':
        '모양',
    'Grösse':
        '크기',
    'Karte anzeigen':
        '맵 표시',
    'Karte im Overlay eingeblendet.':
        '오버레이에 맵이 표시됩니다.',
    'Karte im Overlay aus – es werden nur Timer, Ort und Ping angezeigt.':
        '오버레이의 맵 꺼짐 – 타이머, 위치, 핑만 표시됩니다.',
    'nichts anzuzeigen':
        '표시할 내용 없음',
    'Aus: Das Overlay zeigt nur Rundentimer, Serverregion und Ping – ohne Karte. Erkennung, Rundenende und Statistik laufen wie gewohnt.':
        '끄기: 오버레이에 맵 없이 라운드 타이머, 서버 지역, 핑만 표시됩니다. 인식, 라운드 종료, 통계는 평소처럼 작동합니다.',
    'Für diese Map zurücksetzen':
        '이 맵 초기화',
    'eigene Grösse {n} % (Hotkeys/Strg+Mausrad)':
        '개별 크기 {n}%(단축키/Ctrl+휠)',
    'gedreht um {deg}°':
        '{deg}° 회전됨',
    'Killer':
        '살인마',
    'Survivor':
        '생존자',
    'Rolle':
        '역할',
    'Rolle: {role}':
        '역할: {role}',
    'Alle Rollen':
        '모든 역할',
    'Custom Game':
        '사용자 지정 게임',
    'Custom Games':
        '사용자 지정 게임',
    'Farming':
        '파밍',
    'Stil':
        '스타일',
    'Original':
        '원본',
    'Dunkel':
        '어둡게',
    'Die Karten mit lila Boden, wie sie mitgeliefert werden – gilt auch im Spiel.':
        '보라색 바닥의 원래 맵 그대로 – 게임 안에서도 적용됩니다.',
    'Klassisch':
        '클래식',
    'Glas-Karten':
        '유리 카드',
    'Chips & Icons':
        '칩 & 아이콘',
    'Minimal Line':
        '미니멀 라인',
    'SYSTEM':
        '시스템',
    'Farming an/aus':
        '파밍 켜기/끄기',
    'Farming-Runden':
        '파밍 라운드',
    'Runden ohne Crossplay als Farming zählen':
        '크로스플레이 없는 라운드를 파밍으로 집계',
    'Alle Runden auf':
        '모든 라운드 켜짐',
    'Farming-Runden zählen in Statistik und Aufnahmen überall mit; das Häkchen „Farming ausblenden“ (bei den Filtern) hält sie heraus, der Reiter Statistik → Farming listet sie immer. Crossplay aus erkennt das Programm an der Weltkugel mit rotem Kreuz neben dem Lobby-Knopf; Runden auf der gewählten Region zählen immer als Farming, auch ältere. Einzelne Runden: „Farming an/aus“ unter „Letzte Runden“.':
        '파밍 라운드는 통계와 녹화 어디에서나 집계됩니다. 필터 옆의 ‘파밍 숨기기’ 상자를 켜면 제외되며, 통계 → 파밍 탭에는 항상 표시됩니다. 크로스플레이 꺼짐은 로비 버튼 옆의 빨간 X 표시가 있는 지구본으로 판단합니다. 선택한 지역의 라운드는 이전 라운드도 포함해 항상 파밍으로 집계됩니다. 개별 라운드: ‘최근 라운드’의 ‘파밍 켜기/끄기’.',
    '{map} ({when}) zählt jetzt als Farming-Runde.':
        '{map}({when})은(는) 이제 파밍 라운드로 집계됩니다.',
    '{map} ({when}) zählt wieder als normale Runde.':
        '{map}({when})은(는) 다시 일반 라운드로 집계됩니다.',
    'Hinweis: Runden auf {region} zählen laut Einstellung weiter als Farming.':
        '참고: {region}의 라운드는 설정에 따라 계속 파밍으로 집계됩니다.',
    'Crossplay war aus – die Runde zählt als Farming-Runde.':
        '크로스플레이가 꺼져 있었습니다 – 이 라운드는 파밍 라운드로 집계됩니다.',
    'Crossplay war aus, die Lobby sah aus wie ein Custom Game – die Runde zählt als Farming-Runde, sobald die Stats-Seite sie als öffentliches Match zeigt.':
        '크로스플레이가 꺼져 있었고 로비가 사용자 지정 게임처럼 보였습니다 – 통계 페이지에 공개 매치로 표시되면 이 라운드는 파밍 라운드로 집계됩니다.',
    '{off} von {n} Blicken mit Kreuz':
        '{n}번 중 {off}번 X 표시 확인',
    'letzter Blick':
        '마지막 확인',
    'Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.':
        '크로스플레이 꺼짐({looks}) – 다음 라운드는 파밍 라운드로 집계됩니다.',
    'Crossplay ist an ({looks}) – keine Farming-Runde.':
        '크로스플레이 켜짐({looks}) – 파밍 라운드 아님.',
    'Als Custom Game erkannt – die Runde zählt nicht als Farming (unter „Letzte Runden“ mit „Farming an/aus“ korrigierbar).':
        '사용자 지정 게임으로 인식됨 – 이 라운드는 파밍으로 집계되지 않습니다(‘최근 라운드’에서 ‘파밍 켜기/끄기’로 수정하세요).',
    'Keine Lobby zur Runde ({why}) – sie zählt nicht als Farming.':
        '이 라운드의 로비 없음({why}) – 파밍으로 집계되지 않습니다.',
    'Lobby zu alt':
        '로비가 너무 오래됨',
    'Lobby nicht gesehen':
        '로비를 보지 못함',
    'Diese Runde als Farming-Runde zählen bzw. wieder als normale Runde – Farming-Runden zählen überall mit, bis „Farming ausblenden“ sie heraushält; der Reiter „Farming“ listet sie immer. Runden auf der Farming-Region (Einstellungen → Match-Daten) bleiben Farming.':
        '이 라운드를 파밍 라운드 또는 다시 일반 라운드로 집계합니다. 파밍 라운드는 ‘파밍 숨기기’로 제외하기 전까지 어디에서나 집계되며, ‘파밍’ 탭에는 항상 표시됩니다. 파밍 지역(설정 → 매치 데이터)의 라운드는 계속 파밍으로 남습니다.',
    'Farming ausblenden':
        '파밍 숨기기',
    'An: Farming-Runden (Crossplay aus, Farming-Region, Farming-Gegner) bleiben aus Statistik, Aufnahmen und Clips draussen – ein Schalter für alle drei. Aus: sie zählen wie jede andere Runde. Der Reiter Statistik → Farming zeigt sie immer.':
        '켜기: 파밍 라운드(크로스플레이 꺼짐, 파밍 지역, 파밍 파트너)를 통계, 녹화, 클립에서 제외합니다 – 세 가지 모두에 적용되는 하나의 스위치입니다. 끄기: 다른 라운드처럼 집계됩니다. 통계 → 파밍 탭에는 항상 표시됩니다.',
    'Zeigt die Lobby die Weltkugel mit rotem Kreuz (Crossplay aus), zählt die nächste Runde als Farming-Runde.':
        '로비에 빨간 X 표시가 있는 지구본(크로스플레이 꺼짐)이 보이면 다음 라운드는 파밍 라운드로 집계됩니다.',
    'Custom Game – keine Wartezeit.':
        '사용자 지정 게임 – 대기 시간 없음.',
    'Suche läuft: {time}':
        '검색 중: {time}',
    'Suche nach einem Match gestartet.':
        '매치 검색을 시작했습니다.',
    'Lobby verlassen – sie zählt für keine Runde.':
        '로비를 나갔습니다 – 어떤 라운드에도 집계되지 않습니다.',
    'Suche abgebrochen.':
        '검색이 취소되었습니다.',
    'Lobby gefunden nach {time}{role}.':
        '{time} 후 로비를 찾았습니다{role}.',
    'Lobby gefunden{role}.':
        '로비를 찾았습니다{role}.',
    'Lobby nur kurz gesehen – Rolle und Crossplay von dort, ohne Wartezeit.':
        '로비가 잠깐만 보였습니다 – 역할과 크로스플레이는 그대로 사용하고 대기 시간은 없습니다.',
    'Wartezeit {time}':
        '{time} 대기',
    'Verbindung in dieser Runde: {n} × Aussetzer, längster {s} s.':
        '이번 라운드 연결: 끊김 {n}회, 최장 {s}초.',
    '{n}× Aussetzer':
        '끊김 {n}회',
    'Ergebnisbildschirm (zweiter Blick): gespielt als {role}.':
        '결과 화면(두 번째 확인): {role}(으)로 플레이했습니다.',
    'Ergebnisbildschirm: gespielt als {role}.':
        '결과 화면: {role}(으)로 플레이했습니다.',
    'Wartezeit':
        '대기 시간',
    'Regionen':
        '지역',
    'Markierte Runde:':
        '선택한 라운드:',
    'Benachrichtigungen':
        '알림',
    'Runde auf {map} nicht gezählt: ihr Ende wurde nicht erkannt.':
        '{map} 라운드는 집계되지 않았습니다: 종료를 인식하지 못했습니다.',
    'Einstellungen exportieren …':
        '설정 내보내기 …',
    'Einstellungen importieren …':
        '설정 가져오기 …',
    'Einstellungen exportieren':
        '설정 내보내기',
    'Einstellungen importieren':
        '설정 가져오기',
    'Export fehlgeschlagen: {error}':
        '내보내기 실패: {error}',
    'Einstellungen gesichert: {path}':
        '설정 저장됨: {path}',
    'Das ist keine Einstellungsdatei von Fog Scout ({error}).':
        'Fog Scout 설정 파일이 아닙니다({error}).',
    'Alle Einstellungen durch die aus der Datei ersetzen? Das Programm startet danach neu.':
        '모든 설정을 파일의 설정으로 바꿀까요? 그 후 프로그램이 다시 시작됩니다.',
    'Einstellungen importiert aus {path}.':
        '{path}에서 설정을 가져왔습니다.',
    'Bitte das Programm jetzt neu starten.':
        '지금 프로그램을 다시 시작하세요.',
    'Speichert alle Einstellungen in eine Datei: Hotkeys, Grösse und Drehung pro Map, eigene Map-Zuordnungen, Overlay, Regionen … Die Statistik (rounds.jsonl) gehört nicht dazu.':
        '모든 설정을 파일에 저장합니다: 단축키, 맵별 크기와 회전, 직접 지정한 맵, 오버레이, 지역 … 통계(rounds.jsonl)는 포함되지 않습니다.',
    'Lädt eine exportierte Einstellungsdatei und startet das Programm neu. Fehlende Werte (ältere Sicherung) bekommen ihren Standard.':
        '내보낸 설정 파일을 불러오고 프로그램을 다시 시작합니다. 없는 값(이전 백업)은 기본값이 됩니다.',
    'Ton und Meldung, wenn eine Lobby gefunden wurde':
        '로비를 찾으면 소리와 알림',
    'Erinnern, wenn der Lobby-Countdown abläuft und READY noch nicht gedrückt ist':
        '로비 카운트다운이 끝나 가는데 아직 READY를 누르지 않았으면 알림',
    'Nur wenn DBD nicht das aktive Fenster ist':
        'DBD가 활성 창이 아닐 때만',
    'Die Meldung erscheint unten rechts über allen Fenstern – auch bei „Nicht stören“ – und nimmt dem aktiven Fenster nicht den Fokus. Klick darauf schliesst sie.':
        '알림은 오른쪽 아래에 모든 창 위로 표시되며(‘방해 금지’ 중에도), 활성 창의 포커스를 빼앗지 않습니다. 클릭하면 닫힙니다.',
    'Meldung testen':
        '테스트 알림',
    'Zeigt die Meldung und spielt den Ton – so siehst du, wo sie erscheint.':
        '알림을 표시하고 소리를 재생합니다 – 어디에 나타나는지 확인할 수 있습니다.',
    'Lobby gefunden':
        '로비를 찾았습니다',
    'nach {time}':
        '{time} 후',
    'READY drücken.':
        'READY를 누르세요.',
    'Lobby startet gleich':
        '곧 로비가 시작됩니다',
    'Noch {n} s – READY ist noch nicht gedrückt.':
        '{n}초 남음 – 아직 READY를 누르지 않았습니다.',
    'Lobby-Countdown läuft ab, READY ist noch nicht gedrückt.':
        '로비 카운트다운이 끝나 가는데 READY를 누르지 않았습니다.',
    'Ø Ping':
        '평균 핑',
    'Spielt einen Hinweiston und zeigt eine Windows-Meldung, sobald DBD eine Lobby gefunden hat – praktisch, wenn du während der Suche etwas anderes machst.':
        'DBD가 로비를 찾는 즉시 소리를 재생하고 Windows 알림을 표시합니다 – 검색 중에 다른 일을 할 때 편리합니다.',
    'Noch einmal melden, wenn der Countdown der Lobby unter 15 s fällt und du READY nicht gedrückt hast.':
        '로비 카운트다운이 15초 아래로 내려갔는데 READY를 누르지 않았으면 다시 알립니다.',
    'Keine Meldung, solange DBD im Vordergrund ist – dann siehst du die Lobby ja selbst.':
        'DBD가 맨 앞에 있을 때는 알림 없음 – 직접 로비를 볼 수 있기 때문입니다.',
    'Bilanz der Sitzung zeigen, wenn DBD beendet wurde':
        'DBD를 닫으면 세션 기록 표시',
    'Etwa 15 s nachdem DBD geschlossen wurde: eine Meldung mit den Runden der Sitzung, der Spielzeit und – mit Match-Daten – Ø Kills, Entkommen und Bloodpoints. Steht auch im Log.':
        'DBD를 닫고 약 15초 후: 세션의 라운드 수, 플레이 시간, 그리고 매치 데이터가 있으면 평균 처치, 탈출, 블러드포인트를 알림으로 표시합니다. 로그에도 기록됩니다.',
    'Sitzung beendet':
        '세션 종료',
    '1 Runde':
        '1라운드',
    '{bp} BP':
        '{bp} BP',
    'Melden, wenn eine Runde keine Blutpunkte gebracht hat (Cap erreicht)':
        '라운드에서 블러드포인트를 얻지 못하면 알림(한도 도달)',
    'Fog Scout liest in der Lobby den Blutpunkte-Stand oben rechts. Ist er nach einer gezählten Runde derselbe wie davor, ist das Cap erreicht (normal 5 Millionen, nach Tome-Belohnungen auch mehr) – die Punkte der Runde sind verfallen. Ton und Meldung kommen auch, wenn DBD im Vordergrund ist; Custom Games zählen nicht.':
        'Fog Scout는 로비 오른쪽 위의 블러드포인트 잔액을 읽습니다. 집계된 라운드 후에도 잔액이 이전과 같으면 한도에 도달한 것입니다(보통 500만, 기록서 보상 후에는 더 많음) – 그 라운드의 포인트는 사라집니다. 소리와 알림은 DBD가 맨 앞에 있을 때도 나옵니다. 사용자 지정 게임은 집계되지 않습니다.',
    'Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte dieser Runde sind verfallen.':
        '블러드포인트 변화 없음: 라운드 전후 모두 {bp} – 한도에 도달해 이번 라운드의 포인트가 사라졌습니다.',
    'Blutpunkte-Cap erreicht':
        '블러드포인트 한도 도달',
    '{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die nächste Runde nichts.':
        '라운드 전후 모두 {bp} BP – 블러드웹에서 사용하세요. 그렇지 않으면 다음 라운드에서도 얻지 못합니다.',
    'Blutpunkte: +{gain} in dieser Runde, Stand {bp}.':
        '블러드포인트: 이번 라운드 +{gain}, 잔액 {bp}.',
    'Blutpunkte: Stand {bp} nach der Runde, vorher {before}.':
        '블러드포인트: 라운드 후 잔액 {bp}, 이전 {before}.',
    'BP-Stand':
        'BP 잔액',
    'Aussetzer':
        '멈춤',
    'Alles sichern (ZIP) …':
        '모두 백업(ZIP) …',
    'Aus Sicherung wiederherstellen (ZIP) …':
        '백업에서 복원(ZIP) …',
    'Aus Sicherung wiederherstellen':
        '백업에서 복원',
    'Führt eine Sicherung von „Alles sichern“ mit den jetzigen Daten zusammen: Runden, Match-Daten, Kartenbilder und Banner, die fehlen, kommen dazu – Vorhandenes bleibt, wie es ist. Zeigt vorher, was dazukommt. Die Einstellungen der Sicherung nur auf eigene Rückfrage.':
        '‘모두 백업’의 백업을 현재 데이터와 합칩니다: 없는 라운드, 매치 데이터, 맵 이미지, 배너가 추가되고 기존 데이터는 그대로 유지됩니다. 먼저 무엇이 추가될지 보여 줍니다. 백업의 설정은 별도로 묻습니다.',
    'Während einer Runde nicht möglich – nach dem Rundenende noch einmal.':
        '라운드 중에는 할 수 없습니다 – 라운드가 끝난 후 다시 시도하세요.',
    'Das ist keine Sicherung von Fog Scout ({error}).':
        'Fog Scout 백업이 아닙니다({error}).',
    '{rounds} Runden, {lost} nicht gezählte Runden, {matches} Matches, {files} Bilder/Banner':
        '라운드 {rounds}개, 집계되지 않은 라운드 {lost}개, 매치 {matches}개, 이미지/배너 {files}개',
    'Alles aus der Sicherung ist schon da – nichts hinzuzufügen.':
        '백업의 모든 항목이 이미 있습니다 – 추가할 것이 없습니다.',
    'Aus der Sicherung hinzufügen: {what}. Schon vorhanden (bleibt, wie es ist): {known}. Vorher kommt eine Kopie der Runden und Match-Daten nach backup/.':
        '백업에서 추가: {what}. 이미 있음(그대로 유지): {known}. 먼저 라운드와 매치 데이터의 사본이 backup/에 저장됩니다.',
    'Zusammenführen':
        '합치기',
    'Wiederherstellen fehlgeschlagen: {error}':
        '복원 실패: {error}',
    'Aus der Sicherung hinzugefügt: {what}.':
        '백업에서 추가됨: {what}.',
    'Einstellungen der Sicherung nicht lesbar: {error}':
        '백업의 설정을 읽을 수 없습니다: {error}',
    'Die Sicherung enthält auch Einstellungen – übernehmen ersetzt die aktuellen.':
        '백업에 설정도 들어 있습니다 – 가져오면 현재 설정이 바뀝니다.',
    'Installation prüfen':
        '설치 확인',
    'Installation wird geprüft …':
        '설치를 확인하는 중 …',
    'Installation prüfen – Fehler: {line}':
        '설치 확인 – 실패: {line}',
    '{n} von {total} Prüfungen fehlgeschlagen – Einzelheiten im Log. Eine Neuinstallation (Setup erneut ausführen) behebt fehlende Dateien meist.':
        '검사 {total}개 중 {n}개 실패 – 자세한 내용은 로그에 있습니다. 다시 설치하면(설치 프로그램 재실행) 보통 누락된 파일이 복구됩니다.',
    'Alle {n} Prüfungen bestanden: {names}.':
        '검사 {n}개 모두 통과: {names}.',
    'Installation prüfen: {text}':
        '설치 확인: {text}',
    'Prüft, ob alles da ist und läuft: Programmdateien, Kartenbilder, Bibliotheken, alle Module, Telemetrie aus, Texterkennung, ffmpeg, Qt – derselbe Selbsttest wie bei jedem Build. Läuft als eigener Prozess, Ergebnis im Log.':
        '모든 것이 있고 작동하는지 확인합니다: 프로그램 파일, 맵 이미지, 라이브러리, 모든 모듈, 텔레메트리 꺼짐, 텍스트 인식, ffmpeg, Qt – 모든 빌드에서 하는 것과 같은 자체 검사입니다. 별도 프로세스로 실행되며 결과는 로그에 기록됩니다.',
    'Alles sichern':
        '모두 백업',
    'Gesichert: {n} Dateien in {path}':
        '백업됨: 파일 {n}개 → {path}',
    'Sichern fehlgeschlagen: {error}':
        '백업 실패: {error}',
    'Packt Runden, Match-Daten, die Einstellungen (ohne Passwörter und PC-eigene Werte), eigene Kartenbilder und den Banner-Korpus in eine ZIP-Datei – zum Aufbewahren oder für einen anderen PC. Aufnahmen und Logs bleiben draussen.':
        '라운드, 매치 데이터, 설정(비밀번호와 이 PC 고유 값 제외), 직접 추가한 맵 이미지, 배너 모음을 하나의 ZIP 파일에 담습니다 – 보관하거나 다른 PC에서 쓸 수 있습니다. 녹화와 로그는 포함되지 않습니다.',
    'Spielmodus':
        '게임 모드',
    'Eigener Charakter':
        '내 캐릭터',
    'Eigene Perks':
        '내 퍼크',
    'JSON (für eigene Auswertungen)':
        'JSON(직접 분석용)',
    'Eine Liste mit einem Objekt je Runde, die Spaltentitel als Schlüssel – für eigene Auswertungen (Python, Tabellen, jq).':
        '라운드마다 객체 하나, 열 제목을 키로 하는 목록 – 직접 분석할 때 사용합니다(Python, 스프레드시트, jq).',
    'Rolle für {map} ({when}) auf {role} geändert.':
        '{map}({when})의 역할이 {role}(으)로 바뀌었습니다.',
    'Rolle konnte nicht gespeichert werden: {error}':
        '역할을 저장할 수 없습니다: {error}',
    'Diese Runde als Killer-Runde zählen (falls die Erkennung falsch lag).':
        '이 라운드를 살인마 라운드로 집계합니다(인식이 틀렸을 때).',
    'Diese Runde als Survivor-Runde zählen (falls die Erkennung falsch lag).':
        '이 라운드를 생존자 라운드로 집계합니다(인식이 틀렸을 때).',
    'Diese Runde als Custom Game zählen – sie fliesst dann nicht in die Wartezeit ein.':
        '이 라운드를 사용자 지정 게임으로 집계합니다 – 대기 시간에서 제외됩니다.',
    'Noch keine Wartezeiten in dieser Auswahl.':
        '이 선택에는 아직 대기 시간이 없습니다.',
    'nach Wochentag':
        '요일별',
    'nach Uhrzeit':
        '시간대별',
    'nach Region':
        '지역별',
    'Wann/Wo':
        '언제/어디서',
    'Ø Wartezeit':
        '평균 대기',
    'Kürzeste':
        '최단',
    'Warten':
        '대기',
    'Uhr':
        '시간',
    'Montag':
        '월요일',
    'Dienstag':
        '화요일',
    'Mittwoch':
        '수요일',
    'Donnerstag':
        '목요일',
    'Freitag':
        '금요일',
    'Samstag':
        '토요일',
    'Sonntag':
        '일요일',
    'Gemessen von „CANCEL“ (Suche läuft) bis zur gefundenen Lobby – nur wenn das Programm die Suche gesehen hat. Custom Games haben keine Wartezeit.':
        '‘CANCEL’(검색 중)부터 로비를 찾을 때까지 측정합니다 – 프로그램이 검색을 본 경우에만. 사용자 지정 게임에는 대기 시간이 없습니다.',
    'Map-Namen oben einfügen (wie bei den mitgelieferten Karten)':
        '맵 이름을 위에 표시(기본 제공 맵처럼)',
    'Das Bild hat oben schon einen Namen – es wird keiner hinzugefügt.':
        '이미지 위에 이미 이름이 있습니다 – 추가하지 않습니다.',
    'Schreibt den Map-Namen weiss mit Schatten über die Karte, im Stil der mitgelieferten Karten. Hat das Bild oben schon einen Namen, passiert nichts. Beim Drehen bleibt der Name aufrecht.':
        '기본 제공 맵 스타일로 맵 위에 그림자가 있는 흰색 맵 이름을 씁니다. 이미지 위에 이미 이름이 있으면 아무것도 하지 않습니다. 맵을 회전해도 이름은 똑바로 유지됩니다.',
    'Drehen':
        '회전',
    'Karte drehen':
        '맵 회전',
    'Etage wechseln':
        '층 전환',
    'Beide Etagen':
        '두 층 모두',
    'Etage {n} von {total}':
        '{n}/{total}층',
    'Diese Map hat nur eine Etage.':
        '이 맵은 층이 하나뿐입니다.',
    'Wechselt die Anzeige bei Karten mit Etagen (Midwich): beide untereinander → unten → oben → beide. Gilt bis zur nächsten Map.':
        '층이 있는 맵(Midwich)의 표시를 전환합니다: 두 층을 위아래로 → 아래층 → 위층 → 두 층. 다음 맵까지 유지됩니다.',
    'Etagen untereinander zeigen':
        '층을 위아래로 표시',
    'An: Karten mit Etagen (Midwich) zeigen alle Etagen untereinander, oben über unten – jede so groß wie eine normale Karte, soweit der Platz reicht. Aus: Sie starten mit der unteren Etage. Der Knopf „Etage“ oder der Hotkey schaltet jederzeit um.':
        '켜기: 층이 있는 맵(Midwich)의 모든 층을 위아래로, 위층을 아래층 위에 표시합니다 – 공간이 허락하는 한 각각 일반 맵 크기로. 끄기: 아래층부터 시작합니다. ‘층’ 버튼이나 단축키로 언제든 전환할 수 있습니다.',
    '{map} um {deg}° gedreht.':
        '{map}이(가) {deg}° 회전되었습니다.',
    'Drehung für {map} entfernt.':
        '{map}의 회전이 제거되었습니다.',
    'Dreht die angezeigte Karte um 90° im Uhrzeigersinn (für jede Map gemerkt). Der Map-Name darüber bleibt aufrecht, die Zahlen in der Karte drehen sich mit.':
        '표시 중인 맵을 시계 방향으로 90° 회전합니다(맵마다 기억됨). 위의 맵 이름은 똑바로 유지되고 맵 안의 숫자는 함께 회전합니다.',
    'Eigene Grösse für {map} entfernt – es gilt wieder der Schieberegler.':
        '{map}의 개별 크기가 제거되었습니다 – 슬라이더가 다시 적용됩니다.',
    'Entfernt eigene Grösse und Drehung der angezeigten Map – danach gilt wieder der Schieberegler für alle Maps.':
        '표시 중인 맵의 개별 크기와 회전을 제거합니다 – 모든 맵에 대한 슬라이더가 다시 적용됩니다.',
    'Deckkraft':
        '불투명도',
    'Nur zeigen, wenn DBD das aktive Fenster ist':
        'DBD가 활성 창일 때만 표시',
    'Map-Namen über der Karte anzeigen':
        '맵 위에 맵 이름 표시',
    'Rundentimer unter der Karte anzeigen':
        '맵 아래에 라운드 타이머 표시',
    'Verbundenen Server unter der Karte':
        '맵 아래에 연결된 서버 표시',
    'Transparenter Rand um die Karte':
        '맵 주위에 투명한 테두리',
    'Map beim Match-Start automatisch erkennen':
        '매치가 시작되면 맵을 자동으로 인식',
    'Overlay ausblenden, sobald ich nicht mehr in der Runde bin':
        '라운드에서 나가면 바로 오버레이 숨기기',
    'erkennt Ergebnisbildschirm, Lobby/Menüs, Ladebildschirm und geschlossenes DBD':
        '결과 화면, 로비/메뉴, 로딩 화면, DBD 종료를 인식합니다',
    'Overlay pausieren, solange ein DBD-Menü offen ist':
        'DBD 메뉴가 열려 있는 동안 오버레이 일시 중지',
    'erkannt am sichtbaren Mauszeiger (ESC-Menü, Ergebnisbildschirm, Lobby)':
        '보이는 마우스 포인터로 인식합니다(ESC 메뉴, 결과 화면, 로비)',
    'Spielsprache (Map-Namen)':
        '게임 언어(맵 이름)',
    'Erweitert':
        '고급',
    'Erweitert (Fehlersuche)':
        '고급(문제 해결)',
    'Technik':
        '기술 정보',
    'Auch erkennen, wenn andere Fenster über DBD liegen':
        '다른 창이 DBD를 가려도 인식',
    'Fensteraufnahme wie bei OBS, nur solange DBD im Hintergrund ist':
        'OBS처럼 창 캡처 – DBD가 백그라운드에 있을 때만',
    'Scans/Sek.':
        '스캔/초',
    'Rundenende-Erkennung: {state}':
        '라운드 종료 인식: {state}',
    'Debug-Bilder speichern':
        '디버그 이미지 저장',
    'Banner jeder Erkennung für „Erkennung prüfen“ sammeln':
        '‘인식 확인’을 위해 인식할 때마다 배너 보관',
    '{n} Banner gesammelt':
        '배너 {n}개 보관됨',
    '1 Banner gesammelt':
        '배너 1개 보관됨',
    'letzte Prüfung: {hits} von {total} erkannt':
        '마지막 확인: {total}개 중 {hits}개 인식',
    'Erkennung prüfen':
        '인식 확인',
    'Korpus exportieren …':
        '모음 내보내기 …',
    'Korpus exportieren':
        '모음 내보내기',
    'Korpus-Ordner öffnen':
        '모음 폴더 열기',
    'Noch keine Banner gesammelt – sie kommen mit jeder erkannten Map.':
        '아직 보관된 배너가 없습니다 – 맵을 인식할 때마다 추가됩니다.',
    'Erkennung prüfen: {n} Banner werden neu gelesen …':
        '인식 확인: 배너 {n}개를 다시 읽는 중 …',
    'Erkennung prüfen fehlgeschlagen: {error}':
        '인식 확인 실패: {error}',
    '{hits} von {total} Bannern wieder erkannt ({seconds} s).':
        '배너 {total}개 중 {hits}개를 다시 인식했습니다({seconds}초).',
    '{n} nicht lesbar.':
        '{n}개 읽을 수 없음.',
    'Erkennung prüfen: {text}':
        '인식 확인: {text}',
    'Erkennung prüfen – {stamp}: erwartet {want}, gelesen „{read}“ → {got}':
        '인식 확인 – {stamp}: 예상 {want}, 읽음 ‘{read}’ → {got}',
    'Die Treffer, die fehlen, stehen im Log.':
        '놓친 배너는 로그에 있습니다.',
    'Korpus exportiert: {n} Dateien nach {path}':
        '모음 내보냄: 파일 {n}개 → {path}',
    'Korpus exportieren fehlgeschlagen: {error}':
        '모음 내보내기 실패: {error}',
    'Speichert bei jeder erkannten Map den Ausschnitt um die Banner-Linie (Name und Realm) im Datenordner unter corpus/, höchstens 300 Stück – die Grundlage für „Erkennung prüfen“. Der Ausschnitt kann den linken HUD-Rand mit Spielernamen zeigen; er bleibt auf diesem PC.':
        '인식한 맵마다 배너 선 주변 부분(이름과 렐름)을 데이터 폴더의 corpus/에 최대 300개까지 보관합니다 – ‘인식 확인’의 기반입니다. 이 부분에는 플레이어 이름이 있는 왼쪽 HUD 가장자리가 보일 수 있으며, 이 PC에만 남습니다.',
    'Liest alle gesammelten Banner mit der Erkennung neu und zählt, wie viele wieder die gespeicherte Map ergeben – nach einem Update oder einer geänderten Spielsprache. Läuft im Hintergrund, Ergebnis im Log.':
        '보관된 모든 배너를 인식 기능으로 다시 읽고 저장된 맵이 다시 나오는 수를 셉니다 – 업데이트 후나 게임 언어를 바꾼 후에 사용합니다. 백그라운드에서 실행되며 결과는 로그에 기록됩니다.',
    'Packt alle gesammelten Banner mit ihren Angaben in eine ZIP-Datei – z. B. um sie für die Tests des Projekts weiterzugeben. Vorher die Bilder ansehen: sie können Spielernamen zeigen.':
        '보관된 모든 배너와 세부 정보를 ZIP 파일에 담습니다 – 예를 들어 프로젝트 테스트에 제공할 때. 먼저 이미지를 확인하세요: 플레이어 이름이 보일 수 있습니다.',
    'Öffnet den Ordner corpus/ im Datenordner.':
        '데이터 폴더의 corpus/ 폴더를 엽니다.',
    'Bildschirm jetzt scannen':
        '지금 화면 스캔',
    'Diagnose kopieren':
        '진단 정보 복사',
    'Verbundener Spielserver':
        '연결된 게임 서버',
    'Serverregionen':
        '서버 지역',
    'DBD sucht Matches nur in den angehakten Regionen (über die Windows-hosts-Datei, das Spiel wird nicht verändert). Nach „Auswahl anwenden“ DBD neu starten.':
        'DBD는 체크한 지역에서만 매치를 찾습니다(Windows hosts 파일을 통해, 게임은 변경되지 않음). ‘선택 적용’ 후 DBD를 다시 시작하세요.',
    'Region':
        '지역',
    'hosts-Datei':
        'hosts 파일',
    'Ping messen':
        '핑 측정',
    'Auswahl anwenden':
        '선택 적용',
    'Alles freigeben':
        '모두 허용',
    'Mit VPN unzuverlässig. Region-Tools sind von BHVR weder erlaubt noch verboten – auf eigene Verantwortung.':
        'VPN 사용 시 정확하지 않습니다. 지역 도구는 BHVR이 허용하지도 금지하지도 않았습니다 – 사용에 따른 책임은 본인에게 있습니다.',
    'Warte auf Windows (Administratorrechte) …':
        'Windows(관리자 권한)를 기다리는 중 …',
    'Aus':
        '끄기',
    'Zeigt Region und Ping des Spielservers, auch im Overlay (braucht Administratorrechte).':
        '게임 서버의 지역과 핑을 오버레이에도 표시합니다(관리자 권한 필요).',
    'DBD läuft mit {w}×{h}, kleiner als 1920×1080: die Erkennung ist unsicherer (vor allem Lobby-Knopf und Killername). Fenster größer ziehen oder „Fenster-Vollbild“ nutzen.':
        'DBD가 1920×1080보다 작은 {w}×{h}로 실행 중입니다: 인식이 덜 정확합니다(특히 로비 버튼과 살인마 이름). 창을 키우거나 ‘창 모드 전체 화면’을 사용하세요.',
    'DBD-Fenster ist schmaler als 16:9 ({w}×{h}): diese Form ist ungetestet, Map- und Rundenende-Erkennung können danebenliegen. Am sichersten: 16:9 oder breiter.':
        'DBD 창이 16:9보다 좁습니다({w}×{h}): 이 비율은 테스트되지 않아 맵 및 라운드 종료 인식이 틀릴 수 있습니다. 가장 안전한 것은 16:9 이상입니다.',
    'Verbunden mit: {server}':
        '연결됨: {server}',
    'pausiert, bis DBD läuft':
        'DBD가 실행될 때까지 일시 중지',
    'Anzeige des Spielservers beendet.':
        '게임 서버 표시가 중지되었습니다.',
    'Spielserver-Anzeige: {error}':
        '게임 서버 표시: {error}',
    'Spielserver-Anzeige läuft (liest nur Paketköpfe, keine Inhalte).':
        '게임 서버 표시 실행 중(패킷 헤더만 읽고 내용은 읽지 않음).',
    'Spielserver-Anzeige pausiert – DBD läuft nicht (startet automatisch mit DBD).':
        '게임 서버 표시 일시 중지 – DBD가 실행 중이 아닙니다(DBD와 함께 다시 시작됨).',
    'Spielserver-Anzeige beendet: {error}':
        '게임 서버 표시 중지됨: {error}',
    ' – nicht in deiner Regionsauswahl':
        ' – 선택한 지역에 없음',
    'Verbunden mit Spielserver: {region}{note}.':
        '게임 서버에 연결됨: {region}{note}.',
    'hosts-Datei nicht lesbar: {error}':
        'hosts 파일을 읽을 수 없습니다: {error}',
    'Aktiv: nur {regions} erlaubt.':
        '활성: {regions}만 허용됨.',
    '(keine)':
        '(없음)',
    'Keine eigene Auswahl aktiv, aber andere Einträge sperren Regionen.':
        '직접 선택한 것은 없지만 다른 항목이 지역을 차단하고 있습니다.',
    'Keine Region gesperrt – DBD wählt selbst.':
        '차단된 지역 없음 – DBD가 직접 선택합니다.',
    'anderen Programmen':
        '다른 프로그램',
    ' Es gibt {n} Einträge von {who} für DBD-Server (werden beim Anwenden ersetzt).':
        ' DBD 서버에 대한 {who}의 항목이 {n}개 있습니다(적용 시 교체됨).',
    'Serverregionen: {text}':
        '서버 지역: {text}',
    'Messe Ping zu den Serverregionen …':
        '서버 지역까지 핑을 측정하는 중 …',
    'Ping fehlgeschlagen: {error}':
        '핑 측정 실패: {error}',
    'Am schnellsten: {list}.':
        '가장 빠름: {list}.',
    'Keine Region hat geantwortet (Internet/Firewall/VPN?).':
        '응답한 지역이 없습니다(인터넷/방화벽/VPN?).',
    'Bitte mindestens eine Region anhaken.':
        '지역을 하나 이상 체크하세요.',
    'Erlaubt bleiben: {names}.\n\nAlle anderen DBD-Serverregionen werden in der Windows-hosts-Datei gesperrt. Windows fragt gleich nach Administratorrechten.':
        '허용: {names}.\n\n다른 모든 DBD 서버 지역은 Windows hosts 파일에서 차단됩니다. Windows가 관리자 권한을 요청합니다.',
    '{n} vorhandene Einträge anderer Programme (z. B. Make Your Choice) für DBD-Server werden dabei entfernt.':
        'DBD 서버에 대한 다른 프로그램(예: Make Your Choice)의 기존 항목 {n}개가 제거됩니다.',
    'Danach DBD neu starten, damit es wirkt.':
        '적용하려면 그 후 DBD를 다시 시작하세요.',
    'Serverregionen anwenden':
        '서버 지역 적용',
    'Nur noch {names} erlaubt':
        '{names}만 허용',
    'Es ist nichts gesperrt.':
        '차단된 것이 없습니다.',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen (auch die von Make Your Choice)?':
        'hosts 파일에서 DBD 서버 지역 차단을 모두 제거할까요(Make Your Choice의 차단 포함)?',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen?':
        'hosts 파일에서 DBD 서버 지역 차단을 모두 제거할까요?',
    'Windows fragt gleich nach Administratorrechten. Danach DBD neu starten.':
        'Windows가 관리자 권한을 요청합니다. 그 후 DBD를 다시 시작하세요.',
    'Serverregionen freigeben':
        '서버 지역 허용',
    'Alle Regionen freigegeben':
        '모든 지역 허용됨',
    'Serverregionen: {text}. DBD neu starten, damit es wirkt.':
        '서버 지역: {text}. 적용하려면 DBD를 다시 시작하세요.',
    '{text}. DBD jetzt neu starten.':
        '{text}. 지금 DBD를 다시 시작하세요.',
    'Keine Änderung nötig.':
        '변경할 필요가 없습니다.',
    'unbekannter Fehler':
        '알 수 없는 오류',
    'Firewall-Regeln von Make Your Choice („Enforced“) gefunden – sie sperren Regionen unabhängig von der hosts-Datei. In Make Your Choice „Revert to Default“ drücken.':
        'Make Your Choice의 방화벽 규칙(‘Enforced’)을 찾았습니다 – hosts 파일과 관계없이 지역을 차단합니다. Make Your Choice에서 ‘Revert to Default’를 누르세요.',
    'Achtung: Firewall-Regeln von Make Your Choice aktiv (siehe Log).':
        '주의: Make Your Choice의 방화벽 규칙이 활성 상태입니다(로그 참조).',
    'Europa':
        '유럽',
    'Amerika':
        '아메리카',
    'Asien':
        '아시아',
    'Ozeanien':
        '오세아니아',
    'frei':
        '허용됨',
    'gesperrt':
        '차단됨',
    'gesperrt (fremd)':
        '차단됨(다른 프로그램)',
    'umgeleitet (fremd)':
        '리디렉션됨(다른 프로그램)',
    'Frankfurt':
        '프랑크푸르트',
    'Irland':
        '아일랜드',
    'London':
        '런던',
    'USA Ost (N. Virginia)':
        '미국 동부(버지니아 북부)',
    'USA Ost (Ohio)':
        '미국 동부(오하이오)',
    'USA West (N. Kalifornien)':
        '미국 서부(캘리포니아 북부)',
    'USA West (Oregon)':
        '미국 서부(오리건)',
    'Kanada (Zentral)':
        '캐나다(중부)',
    'Südamerika (São Paulo)':
        '남아메리카(상파울루)',
    'Tokio':
        '도쿄',
    'Seoul':
        '서울',
    'Mumbai':
        '뭄바이',
    'Singapur':
        '싱가포르',
    'Hongkong':
        '홍콩',
    'Sydney':
        '시드니',
    'Name nicht auflösbar':
        '이름을 확인할 수 없음',
    'Start mit Administratorrechten fehlgeschlagen (Fehler {code}).':
        '관리자 권한으로 시작하지 못했습니다(오류 {code}).',
    'Hilfsprogramm nicht gestartet.':
        '도우미 프로그램이 시작되지 않았습니다.',
    'Das Hilfsprogramm hat kein Ergebnis geliefert (Code {code}).':
        '도우미 프로그램이 결과를 반환하지 않았습니다(코드 {code}).',
    'Zeitüberschreitung beim Schreiben der hosts-Datei.':
        'hosts 파일을 쓰는 중 시간 초과.',
    'Abgebrochen (keine Administratorrechte erteilt).':
        '취소됨(관리자 권한이 부여되지 않음).',
    'Warte auf Match …':
        '매치를 기다리는 중 …',
    'Global':
        '전체',
    'keine Daten vom Mitschnitt':
        '캡처에서 데이터 없음',
    'Nur unter Windows verfügbar.':
        'Windows에서만 사용할 수 있습니다.',
    'Mitschnitt beendet (Code {code}).':
        '캡처 종료(코드 {code}).',
    'Fehler: {error}':
        '오류: {error}',
    'Statistik':
        '통계',
    'Maps':
        '맵',
    'Map':
        '맵',
    'Runden':
        '라운드',
    'Ø Dauer':
        '평균 길이',
    'Letzte Runden':
        '최근 라운드',
    'Gesamter Zeitraum':
        '전체 기간',
    'Heute':
        '오늘',
    'Diese Woche':
        '이번 주',
    'Dieser Monat':
        '이번 달',
    'Dieses Jahr':
        '올해',
    'Alle Regionen':
        '모든 지역',
    'Alle Killer':
        '모든 살인마',
    'Häufigste Map':
        '가장 많이 나온 맵',
    'Der markierte Name (Skin oder neuer Killer) zählt ab jetzt als der gewählte Killer – auch in allen bisherigen Runden.':
        '선택한 이름(스킨 또는 새 살인마)은 이제부터 선택한 살인마로 집계됩니다 – 지난 라운드에도 적용됩니다.',
    'Entfernt alle eigenen Killer-Zuordnungen; die Namen erscheinen wieder so, wie sie gelesen wurden.':
        '직접 지정한 살인마를 모두 제거합니다. 이름은 다시 읽은 그대로 표시됩니다.',
    'Zuordnen':
        '지정',
    'Warte auf Map':
        '맵 대기 중',
    'Solange DBD läuft und keine Karte eingeblendet ist, zeigt das Overlay eine kleine Karte: „Warte auf Map“, darunter Suche/Lobby (z. B. „Suche läuft: 02:13 · Nurse“) oder die letzte Runde. Gilt nicht, wenn du die Karte selbst ausgeblendet hast.':
        'DBD가 실행 중이고 맵이 표시되지 않으면 오버레이에 작은 카드가 표시됩니다: ‘맵 대기 중’, 그 아래에 검색/로비(예: ‘검색 중: 02:13 · Nurse’) 또는 마지막 라운드. 맵을 직접 숨긴 경우에는 표시되지 않습니다.',
    'Ohne Karte: „Warte auf Map“ und Lobby-Status anzeigen':
        '맵이 없으면 ‘맵 대기 중’과 로비 상태 표시',
    'Killer der Runde:':
        '라운드의 살인마:',
    'Killer setzen':
        '살인마 지정',
    'Notiz zum Killer:':
        '살인마 메모:',
    'Um diese Tageszeit ({span} Uhr) am schnellsten: {region} – Wartezeit {wait} (Median), {n} Runden':
        '이 시간대({span}시)에 가장 빠름: {region} – 대기 {wait}(중앙값), {n}라운드',
    'Ø {ping} ms':
        'Ø {ping}ms',
    'danach {region} ({wait})':
        '다음 {region}({wait})',
    'Notiz speichern':
        '메모 저장',
    'Notiz zu {killer} gespeichert.':
        '{killer} 메모가 저장되었습니다.',
    'Notiz zu {killer} gelöscht.':
        '{killer} 메모가 제거되었습니다.',
    'Eigene Notiz zum markierten Killer, z. B. „Lithe, nicht vaulten“. Erscheint im Spiel unter der Map-Notiz, sobald dieser Killer in der Runde ist (eigener Killer oder, als Survivor, der aus der Lobby). Leer speichern löscht sie.':
        '선택한 살인마에 대한 내 메모(예: ‘민첩함 – 창틀 넘지 말 것’). 이 살인마가 라운드에 있으면(내 살인마 또는 생존자일 때 로비의 살인마) 게임에서 맵 메모 아래에 표시됩니다. 비워서 저장하면 제거됩니다.',
    'Killer konnte nicht gespeichert werden: {error}':
        '살인마를 저장할 수 없습니다: {error}',
    'Killer für {map} ({when}) auf {killer} gesetzt.':
        '{map}({when})의 살인마가 {killer}(으)로 지정되었습니다.',
    'Map der Runde:':
        '라운드의 맵:',
    'Setzt die Map nur für die markierten Runden – wenn das Banner falsch gelesen wurde. Statistik, eigener Rekord und die Verknüpfung mit den Match-Daten folgen; die Aufnahme behält ihren Namen.':
        '선택한 라운드에만 맵을 지정합니다 – 배너를 잘못 읽었을 때. 통계, 내 기록, 매치 데이터 연결이 함께 바뀌며, 녹화 파일 이름은 그대로 유지됩니다.',
    'Map setzen':
        '맵 지정',
    'Map konnte nicht gespeichert werden: {error}':
        '맵을 저장할 수 없습니다: {error}',
    'Map der Runde vom {when} auf {map} gesetzt.':
        '{when} 라운드의 맵이 {map}(으)로 지정되었습니다.',
    'Setzt den Killer nur für die markierte Runde und zählt sie als Killer-Runde – z. B. wenn sie fälschlich als Survivor gezählt wurde oder der Name falsch gelesen wurde.':
        '선택한 라운드에만 살인마를 지정하고 살인마 라운드로 집계합니다 – 예를 들어 생존자로 잘못 집계되었거나 이름을 잘못 읽었을 때.',
    'Zuordnungen löschen':
        '지정 삭제',
    '„{name}“ zählt jetzt als {killer}.':
        '‘{name}’은(는) 이제 {killer}(으)로 집계됩니다.',
    'Alle eigenen Killer-Zuordnungen löschen?':
        '직접 지정한 살인마를 모두 삭제할까요?',
    'Killer-Zuordnungen gelöscht.':
        '살인마 지정이 삭제되었습니다.',
    'ohne Region':
        '지역 없음',
    'Anteil':
        '비율',
    'Region nur bekannt, wenn im Tab Server „Verbundener Spielserver“ an war.':
        '지역은 서버 탭에서 ‘연결된 게임 서버’가 켜져 있었을 때만 알 수 있습니다.',
    'Wann':
        '언제',
    'Dauer':
        '길이',
    'Alle Runden löschen …':
        '모든 라운드 삭제 …',
    'Runde löschen':
        '라운드 삭제',
    'Ø {kills} Kills · {n} Runden':
        '평균 {kills}처치 · {n}라운드',
    'Killer: Ø {kills} Kills, {four}× 4K ({n})':
        '살인마: 평균 {kills}처치, 4킬 {four}회({n})',
    'Survivor: {share} entkommen ({n})':
        '생존자: {share} 탈출({n})',
    '{share} entkommen · {n} Runden':
        '{share} 탈출 · {n}라운드',
    'Eigene Bilanz unter dem Timer':
        '타이머 아래에 내 기록',
    'Eigene Notiz unter dem Timer':
        '타이머 아래에 내 메모',
    'Zeigt deine eigene Notiz zur Map unter dem Rundentimer – geschrieben auf der Seite Maps (Map anklicken oder Rechtsklick → „Notiz bearbeiten …“), höchstens vier Zeilen.':
        '라운드 타이머 아래에 이 맵에 대한 내 메모를 표시합니다 – 맵 페이지에서 작성(맵 클릭 또는 오른쪽 클릭 → ‘메모 편집 …’), 최대 네 줄.',
    'Deine Notiz zu dieser Map – wird beim Tippen gespeichert und im Spiel unter dem Timer gezeigt (höchstens vier Zeilen). Leer = keine Notiz.':
        '이 맵에 대한 메모 – 입력하는 동안 저장되고 게임에서 타이머 아래에 표시됩니다(최대 네 줄). 비워 두면 메모 없음.',
    'Eigene Notiz (im Spiel unter dem Timer)':
        '내 메모(게임에서 타이머 아래)',
    'z. B. Shack links vom Main, Gen im Keller …':
        '예: 메인 건물 왼쪽에 판잣집, 지하실에 발전기 …',
    'Notiz bearbeiten …':
        '메모 편집 …',
    'Map-Stile':
        '맵 스타일',
    'Alle auf einmal':
        '한 번에 모두',
    'Kartenstile für {map} werden im Hintergrund erstellt.':
        '{map}의 맵 스타일을 백그라운드에서 만드는 중입니다.',
    'Kartenstil {style} für {map} wird im Hintergrund erstellt.':
        '{map}의 맵 스타일 {style}을(를) 백그라운드에서 만드는 중입니다.',
    'Eigene Notiz':
        '내 메모',
    'Eigene Notiz: {note}':
        '내 메모: {note}',
    'Zeigt unter dem Rundentimer, wie es dir auf dieser Map bisher ging: als Killer Ø Kills, als Survivor den Anteil Escapes – aus den Runden mit Daten der Stats-Seite, ab 3 Runden.':
        '라운드 타이머 아래에 지금까지 이 맵에서의 성적을 표시합니다: 살인마일 때 평균 처치 수, 생존자일 때 탈출 비율 – 통계 페이지 데이터가 있는 라운드 기준, 3라운드부터.',
    'Entfernt die markierte Runde aus der Statistik – z. B. eine Map, die mitten im Match falsch erkannt wurde. Fragt vorher nach.':
        '선택한 라운드를 통계에서 제거합니다 – 예를 들어 매치 도중 맵을 잘못 읽었을 때. 먼저 묻습니다.',
    'Runde {what} aus der Statistik löschen?':
        '{what} 라운드를 통계에서 삭제할까요?',
    'Runde konnte nicht gelöscht werden: {error}':
        '라운드를 삭제할 수 없습니다: {error}',
    'Runde gelöscht: {map} ({when}).':
        '라운드 삭제됨: {map}({when}).',
    'Noch keine Runden gespeichert.':
        '아직 저장된 라운드가 없습니다.',
    'Alle Runden löschen':
        '모든 라운드 삭제',
    'Alle gespeicherten Runden löschen? Vorher wird eine Kopie in {folder}/ angelegt.':
        '저장된 라운드를 모두 삭제할까요? 먼저 사본이 {folder}/에 저장됩니다.',
    'Es sind keine Runden gespeichert.':
        '저장된 라운드가 없습니다.',
    'Die Kopie in {folder}/ konnte nicht angelegt werden – die Runden bleiben gespeichert.':
        '{folder}/에 사본을 만들 수 없습니다 – 라운드는 그대로 저장되어 있습니다.',
    'Nicht angewendet – 1 Änderung. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '적용 안 됨 – 변경 1개. ‘선택 적용’으로 반영한 후 DBD를 다시 시작하세요.',
    'Nicht angewendet – {n} Änderungen. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '적용 안 됨 – 변경 {n}개. ‘선택 적용’으로 반영한 후 DBD를 다시 시작하세요.',
    'Öffnet die markierten Runden bzw. Clips nacheinander im grossen Editor – als eine Montage (mehrere markieren: Strg- oder Umschalt-Klick).':
        '선택한 라운드나 클립을 큰 편집기에서 차례로 하나의 몽타주로 엽니다(여러 개 선택: Ctrl 또는 Shift 클릭).',
    'Ursache: {cause}':
        '원인: {cause}',
    'Keine Region angehakt – für „Auswahl anwenden“ mindestens eine anhaken.':
        '체크한 지역이 없습니다 – ‘선택 적용’을 하려면 하나 이상 체크하세요.',
    'Anwenden':
        '적용',
    'Freigeben':
        '차단 해제',
    'Importieren':
        '가져오기',
    'Markieren':
        '선택',
    'Trotzdem beenden':
        '그래도 종료',
    'Rundenverlauf gelöscht.':
        '라운드 기록이 삭제되었습니다.',
    'Löscht alle gespeicherten Runden (Datei rounds.jsonl) – nach einer Rückfrage, vorher kommt eine Kopie in den Ordner backup.':
        '저장된 모든 라운드(rounds.jsonl 파일)를 삭제합니다 – 확인 후, 먼저 사본이 백업 폴더에 저장됩니다.',
    'Anzeigen:':
        '표시:',
    'Leeren':
        '지우기',
    'Log-Datei öffnen':
        '로그 파일 열기',
    'Sprache und Darstellung':
        '언어 및 모양',
    'Wirkt nach dem nächsten Start des Programms.':
        '다음에 프로그램을 시작할 때 적용됩니다.',
    'Sprache geändert – wirkt nach dem nächsten Start des Programms.':
        '언어가 바뀌었습니다 – 다음에 프로그램을 시작할 때 적용됩니다.',
    'Dark Mode':
        '다크 모드',
    'Hotkeys':
        '단축키',
    'Standard':
        '기본값',
    'Zum Ändern anklicken und die neue Tastenkombination drücken.':
        '클릭해서 바꾼 다음 새 키 조합을 누르세요.',
    'Start und Infobereich':
        '시작 및 알림 영역',
    'Beim Minimieren in den Infobereich':
        '알림 영역으로 최소화',
    'Mit Windows starten':
        'Windows와 함께 시작',
    'Updates':
        '업데이트',
    'Beim Start Updates installieren':
        '시작할 때 업데이트 설치',
    'nur über start.bat bzw. die Desktop-Verknüpfung; eigene Änderungen werden nie überschrieben':
        'start.bat 또는 바탕 화면 바로 가기로 시작할 때만. 직접 수정한 내용은 절대 덮어쓰지 않습니다',
    'Eigene Map-Zuordnungen':
        '직접 지정한 맵',
    'Jetzt nach Updates suchen':
        '지금 업데이트 확인',
    'Aktualisieren und neu starten':
        '업데이트 후 다시 시작',
    'Suche nach Updates …':
        '업데이트를 확인하는 중 …',
    'Beim Start nach Updates suchen':
        '시작할 때 업데이트 확인',
    'Laden und Installieren nur nach deiner Bestätigung; das Setup wird per SHA-256 geprüft':
        '확인한 후에만 다운로드하고 설치합니다. 설치 프로그램은 SHA-256으로 검사합니다',
    'Update-Prüfung fehlgeschlagen: {error}':
        '업데이트 확인 실패: {error}',
    'Kein Update – Version {version} (Build {build}) ist aktuell.':
        '업데이트 없음 – 버전 {version}(빌드 {build})이 최신입니다.',
    'Update verfügbar: {old} → {new} (Build {build}).':
        '업데이트 있음: {old} → {new}(빌드 {build}).',
    'Lade Update …':
        '업데이트를 다운로드하는 중 …',
    'GitHub antwortet gerade nicht (HTTP {code}) – bitte in einigen Minuten erneut versuchen.':
        'GitHub가 지금 응답하지 않습니다(HTTP {code}) – 몇 분 후에 다시 시도하세요.',
    'Keine Antwort von GitHub (Zeitüberschreitung/Verbindung) – bitte später erneut versuchen.':
        'GitHub에서 응답이 없습니다(시간 초과/연결) – 나중에 다시 시도하세요.',
    'GitHub antwortet nicht – neuer Versuch {n} von {total} …':
        'GitHub가 응답하지 않습니다 – 시도 {n}/{total} …',
    'Lade Update … {pct} %':
        '업데이트를 다운로드하는 중 … {pct}%',
    'Update nicht geladen: {error}':
        '업데이트를 다운로드하지 못했습니다: {error}',
    'Update {version} (Build {build}) geladen und geprüft.':
        '업데이트 {version}(빌드 {build})을 다운로드하고 검사했습니다.',
    'Update installieren':
        '업데이트 설치',
    'Fog Scout {version} (Build {build}) ist geladen und per SHA-256 geprüft. Jetzt installieren? Das Programm schliesst sich und startet danach neu.':
        'Fog Scout {version}(빌드 {build})을 다운로드하고 SHA-256으로 검사했습니다. 지금 설치할까요? 프로그램이 종료된 후 다시 시작됩니다.',
    'Installieren':
        '설치',
    'Update gesperrt: eine Runde läuft oder ein Clip wird gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '업데이트 차단됨: 라운드가 진행 중이거나 클립을 저장하는 중입니다. 끝난 후 ‘업데이트 후 다시 시작’을 다시 클릭하세요.',
    'Programm schliesst sich und installiert das Update …':
        '프로그램을 종료하고 업데이트를 설치합니다 …',
    'Das Update wurde nicht gestartet: Die Setup-Datei hat sich seit dem Download verändert oder fehlt. Bitte das Update noch einmal laden.':
        '업데이트가 시작되지 않았습니다: 다운로드 후 설치 파일이 바뀌었거나 없습니다. 업데이트를 다시 다운로드하세요.',
    'Das Update wurde nicht gestartet: Die Setup-Datei liess sich nicht sicher bereitstellen ({error}). Bitte das Update noch einmal laden.':
        '업데이트가 시작되지 않았습니다: 설치 파일을 안전하게 배치할 수 없습니다({error}). 업데이트를 다시 다운로드하세요.',
    'Das Setup konnte nicht gestartet werden (Abfrage nach Administratorrechten abgebrochen?). Erneut versuchen oder das Setup selbst starten:\n{path}':
        '설치 프로그램을 시작할 수 없습니다(관리자 확인을 취소했나요?). 다시 시도하거나 설치 프로그램을 직접 시작하세요:\n{path}',
    'Neustart nicht möglich: {error}':
        '다시 시작할 수 없습니다: {error}',
    'Nur unter Windows: bitte das Programm über start.bat neu starten.':
        'Windows 전용: start.bat으로 프로그램을 다시 시작하세요.',
    'Programm startet neu und installiert das Update …':
        '프로그램을 다시 시작하고 업데이트를 설치합니다 …',
    'Fragt GitHub, ob es eine neue Version gibt (nur bei diesem Klick). Installiert wird erst mit „Aktualisieren und neu starten“.':
        'GitHub에 새 버전이 있는지 묻습니다(이 클릭 때만). ‘업데이트 후 다시 시작’을 눌러야만 설치됩니다.',
    'Beendet das Programm und startet es über start.bat neu – dabei wird das Update installiert. Die installierte Version lädt das Setup, prüft es per SHA-256 und fragt vor dem Installieren.':
        '프로그램을 종료하고 start.bat으로 다시 시작합니다 – 이때 업데이트가 설치됩니다. 설치된 버전은 설치 프로그램을 다운로드해 SHA-256으로 검사하고 설치 전에 묻습니다.',
    'Fragt nach jedem Start einmal GitHub, ob es ein neues Release gibt. Geladen und installiert wird nur nach deinem Klick und einer Rückfrage.':
        '시작할 때마다 한 번 GitHub에 새 릴리스가 있는지 묻습니다. 다운로드와 설치는 클릭하고 확인한 후에만 진행됩니다.',
    'Alle löschen':
        '모두 삭제',
    'Datenordner öffnen':
        '데이터 폴더 열기',
    'Karten-Ordner öffnen':
        '맵 폴더 열기',
    'liest nur Bildschirmpixel, sendet keine Eingaben ans Spiel.':
        '화면 픽셀만 읽고 게임에 입력을 보내지 않습니다.',
    'Inoffizielles Fan-Tool, nicht von Behaviour Interactive genehmigt – Nutzung auf eigene Gefahr (siehe LICENSE).':
        'Behaviour Interactive가 승인하지 않은 비공식 팬 도구입니다 – 사용에 따른 책임은 본인에게 있습니다(LICENSE 참조).',
    'Kartenbilder: Lethia (hens333.com/callouts, mit Erlaubnis von Hens) · Map-Namen: Luca Fontanot (DBD Map Overlay).':
        '맵 이미지: Lethia(hens333.com/callouts, Hens의 허락을 받음) · 맵 이름: Luca Fontanot(DBD Map Overlay).',
    'Keine. Unbekannte Map-Namen lassen sich nach dem Match im Hauptfenster zuordnen.':
        '없음. 알 수 없는 맵 이름은 매치 후 메인 창에서 지정할 수 있습니다.',
    'Eigene Zuordnungen':
        '직접 지정',
    'Alle eigenen Map-Zuordnungen löschen?':
        '직접 지정한 맵을 모두 삭제할까요?',
    'Eigene Map-Zuordnungen gelöscht.':
        '직접 지정한 맵이 삭제되었습니다.',
    'Spielsprachen: {langs}':
        '게임 언어: {langs}',
    'Änderbar, wenn das Programm über die Desktop-Verknüpfung gestartet wurde (verknuepfung_erstellen.bat einmal ausführen).':
        '바탕 화면 바로 가기로 프로그램을 시작했을 때 바꿀 수 있습니다(verknuepfung_erstellen.bat을 한 번 실행).',
    'Wird eingerichtet …':
        '설정하는 중 …',
    'Startet ab jetzt mit Windows im Infobereich.':
        '이제부터 Windows와 함께 알림 영역에서 시작합니다.',
    'Startet nicht mehr mit Windows.':
        '더 이상 Windows와 함께 시작하지 않습니다.',
    'Startet ab jetzt mit Windows im Infobereich (abschaltbar unter Einstellungen → Start und Infobereich).':
        '이제부터 Windows와 함께 알림 영역에서 시작합니다(설정 → 시작 및 알림 영역에서 끌 수 있음).',
    'Autostart mit Windows fehlgeschlagen: {error}':
        'Windows와 함께 시작하도록 설정할 수 없습니다: {error}',
    'Fehlgeschlagen: {error}':
        '실패: {error}',
    'Nur unter Windows.':
        'Windows 전용.',
    'Tipp: Fog Scout über die Verknüpfung im Startmenü starten – dann läuft es ohne Windows-Abfrage mit den nötigen Rechten.':
        '팁: 시작 메뉴의 바로 가기로 Fog Scout를 시작하세요 – 그러면 Windows 확인 창 없이 필요한 권한으로 실행됩니다.',
    'Änderbar, wenn das Programm über die Verknüpfung im Startmenü gestartet wurde.':
        '시작 메뉴의 바로 가기로 프로그램을 시작했을 때 바꿀 수 있습니다.',
    'Tipp: Einmal als Administrator starten (Rechtsklick auf start.bat → „Als Administrator ausführen“) – dann richtet das Programm die Desktop-Verknüpfung ein, die künftig ohne Windows-Abfrage startet.':
        '팁: 한 번 관리자로 시작하세요(start.bat 오른쪽 클릭 → ‘관리자 권한으로 실행’) – 그러면 프로그램이 바탕 화면 바로 가기를 만들고, 이후에는 Windows 확인 창 없이 시작됩니다.',
    'Desktop-Verknüpfung eingerichtet/aktualisiert: startet ab jetzt ohne Windows-Abfrage.':
        '바탕 화면 바로 가기를 설정/업데이트했습니다: 이제부터 Windows 확인 창 없이 시작됩니다.',
    'Einrichtung der Verknüpfung fehlgeschlagen: {error}':
        '바로 가기 설정 실패: {error}',
    'Verknüpfung erstellt: {path}':
        '바로 가기 생성됨: {path}',
    'Aufgabe konnte nicht angelegt werden: {error}':
        '예약된 작업을 만들 수 없습니다: {error}',
    'Verknüpfung konnte nicht angelegt werden: {error}':
        '바로 가기를 만들 수 없습니다: {error}',
    '(Autostart nicht erneuert: {error})':
        '(자동 시작이 갱신되지 않음: {error})',
    'Symbol im Infobereich nicht verfügbar ({error}) – Minimieren wie gewohnt.':
        '알림 영역 아이콘을 사용할 수 없습니다({error}) – 최소화는 평소처럼 작동합니다.',
    'Öffnen nur unter Windows: {path}':
        '열기는 Windows에서만 작동합니다: {path}',
    'Kann {path} nicht öffnen: {error}':
        '{path}을(를) 열 수 없습니다: {error}',
    'Fenster öffnen':
        '창 열기',
    'Beenden':
        '종료',
    'Hotkey: {keys}':
        '단축키: {keys}',
    'Hotkey {keys} ({action}) nicht verfügbar: {why}.':
        '단축키 {keys}({action})을(를) 사용할 수 없습니다: {why}.',
    '{n} Hotkey(s) nicht verfügbar – siehe Log.':
        '단축키 {n}개를 사용할 수 없습니다 – 로그 참조.',
    '– aus –':
        '– 꺼짐 –',
    'Tasten drücken …':
        '키를 누르세요 …',
    'Neue Kombination drücken – Esc bricht ab, Entf schaltet den Hotkey aus.':
        '새 조합을 누르세요 – Esc는 취소, Delete는 단축키를 끕니다.',
    '{keys} ist schon „{action}“ – andere wählen.':
        '{keys}은(는) 이미 ‘{action}’에 사용 중입니다 – 다른 키를 선택하세요.',
    'aus':
        '꺼짐',
    'an':
        '켜짐',
    'Hotkey {action}: {keys}.':
        '단축키 {action}: {keys}.',
    'Standard-Hotkeys wiederhergestellt.':
        '기본 단축키가 복원되었습니다.',
    'Strg':
        'Ctrl',
    'Taste „{key}“ geht nicht als Hotkey':
        '‘{key}’ 키는 단축키로 사용할 수 없습니다',
    'Bitte mit Strg und/oder Alt kombinieren':
        'Ctrl 및/또는 Alt와 함께 사용하세요',
    'schon von einem anderen Programm belegt':
        '이미 다른 프로그램에서 사용 중',
    'Für „{map}“ gibt es kein Bild.':
        '‘{map}’의 이미지가 없습니다.',
    'Bild konnte nicht geladen werden: {path} ({error})':
        '이미지를 불러올 수 없습니다: {path}({error})',
    'Map gewählt: {map}':
        '맵 선택됨: {map}',
    'Noch keine Map gewählt.':
        '아직 선택한 맵이 없습니다.',
    'Overlay eingeblendet.':
        '오버레이 표시됨.',
    'Overlay ausgeblendet.':
        '오버레이 숨겨짐.',
    '„{map}“ hat nur ein Layout.':
        '‘{map}’에는 레이아웃이 하나뿐입니다.',
    'Layout manuell gewechselt':
        '레이아웃을 직접 바꿈',
    'Scanne den Bildschirm nach Map- oder Realm-Namen …':
        '화면에서 맵 또는 렐름 이름을 스캔하는 중 …',
    'Testanzeige':
        '테스트 표시',
    'Test: Overlay 10 s lang an seiner normalen Position, mit Systemwerten, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – nochmal drücken beendet den Test.':
        '테스트: 시스템 값, ‘오늘’, 음악과 함께(아무것도 없으면 예시 값) 오버레이를 평소 위치에 10초 동안 표시합니다 – 다시 누르면 테스트가 끝납니다.',
    'Links':
        '왼쪽',
    'Mittig':
        '가운데',
    'Rechts':
        '오른쪽',
    'Im Balken':
        '여백 안',
    'Abstand':
        '간격',
    'Zeile CPU (Temperatur, Last)':
        'CPU 행(온도, 부하)',
    'Zeile GPU (Temperatur, Last)':
        'GPU 행(온도, 부하)',
    'Zeile Hotspot / GPU-Speicher (HWiNFO)':
        '핫스팟 / GPU 메모리 행(HWiNFO)',
    'Zeile VRAM':
        'VRAM 행',
    'Zeile RAM':
        'RAM 행',
    'Zeile in den Systemwerten an/aus. Die Warnungen „CPU/GPU DROSSELT“ erscheinen immer.':
        '시스템 값의 행 켜기/끄기. ‘CPU/GPU THROTTLED’ 경고는 항상 표시됩니다.',
    'Zeile in den Systemwerten an/aus – Hotspot und Memory Junction kommen nur mit HWiNFO.':
        '시스템 값의 행 켜기/끄기 – 핫스팟과 메모리 정션은 HWiNFO가 있을 때만 표시됩니다.',
    'Zeile in den Systemwerten an/aus.':
        '시스템 값의 행 켜기/끄기.',
    'Test beendet.':
        '테스트가 끝났습니다.',
    'Diagnose in die Zwischenablage kopiert (auch als diagnose.txt gespeichert).':
        '진단 정보를 클립보드에 복사했습니다(diagnose.txt로도 저장됨).',
    'Alle Elemente mit der Maus ziehen (im Spiel oder in der Vorschau): Karte, Infos, Systemwerte, Heute, Eingaben, Musik. Rechtsklick auf ein Element = Menü (Ausblenden, Position zurücksetzen, Sperren), Strg+Mausrad = Grösse. Danach „Fertig“ oder Hotkey.':
        '모든 요소를 마우스로 끌어 옮기세요(게임 또는 미리 보기에서): 맵, 정보, 시스템 값, 오늘, 입력, 음악. 요소를 오른쪽 클릭 = 메뉴(숨기기, 위치 초기화, 잠금), Ctrl+마우스 휠 = 크기. 그다음 ‘완료’ 또는 단축키.',
    '{name} wieder an seinem üblichen Platz.':
        '{name}이(가) 원래 위치로 돌아갔습니다.',
    'Karte':
        '맵',
    'Systemwerte':
        '시스템 값',
    'Musik':
        '음악',
    'Eingaben':
        '입력',
    'Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = Grösse, Rechtsklick = Menü':
        '이동 켜짐 – 끌기(맞춤, Alt = 자유), 화살표 키 = 미세 조정, 모서리/Ctrl+휠 = 크기, 오른쪽 클릭 = 메뉴',
    'Position zurücksetzen':
        '위치 초기화',
    'Rückgängig':
        '실행 취소',
    'Karte darf grösser als der Balken werden':
        '맵이 여백보다 커질 수 있음',
    'Karte füllt den Balken aus':
        '맵이 여백을 채움',
    'Erlaubt jede Kartengrösse: Ist die Karte breiter als der schwarze Balken, bleibt sie an dessen Aussenrand und ragt ins Spielbild. Aus: Die Karte wird nie breiter als der Balken (auf 3440×1440 etwa 31 % der Bildhöhe).':
        '맵 크기 제한을 없앱니다: 맵이 검은 여백보다 넓으면 여백의 바깥쪽 가장자리에 붙은 채 게임 화면 안으로 들어갑니다. 끄기: 맵이 여백보다 넓어지지 않습니다(3440×1440에서 높이의 약 31%).',
    'Die Karte wird so gross, dass sie den schwarzen Balken von links bis rechts ausfüllt (bis auf den Abstand zum Rand); der Grössen-Regler gilt dann nicht. Eine hohe Karte stoppt an der Bildhöhe.':
        '맵이 검은 여백을 왼쪽에서 오른쪽까지 채울 때까지 커집니다(가장자리와의 간격 제외). 이때 크기 슬라이더는 적용되지 않습니다. 세로로 긴 맵은 화면 높이에서 멈춥니다.',
    'Nimmt die letzte Änderung an Position oder Grösse zurück (Karte, Systemwerte, Musik) – auch mit Strg+Z auf dieser Seite. Ein ganzes Ziehen zählt als ein Schritt.':
        '마지막 위치 또는 크기 변경(맵, 시스템 값, 음악)을 되돌립니다 – 이 페이지에서 Ctrl+Z로도 가능합니다. 한 번 끌기는 한 단계로 계산됩니다.',
    'Merkt Position und Grösse aller Elemente getrennt für jede Grösse des DBD-Fensters (z. B. Vollbild 3440×1440 und ein kleineres Fenster) und lädt sie automatisch, sobald DBD in dieser Grösse läuft.':
        'DBD 창 크기마다(예: 전체 화면 3440×1440과 더 작은 창) 모든 요소의 위치와 크기를 따로 기억하고, DBD가 그 크기로 실행되면 자동으로 불러옵니다.',
    'Nichts rückgängig zu machen.':
        '되돌릴 것이 없습니다.',
    'Position/Grösse rückgängig gemacht.':
        '위치/크기를 되돌렸습니다.',
    'Position und Grösse je DBD-Fenstergrösse merken':
        'DBD 창 크기별로 위치와 크기 기억',
    'DBD-Fenster {size}: Layout für diese Grösse geladen.':
        'DBD 창 {size}: 이 크기의 레이아웃을 불러왔습니다.',
    'DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.':
        'DBD 창 {size}: 새 크기 – 이제부터 이 크기의 레이아웃을 기억합니다.',
    'Aktuell: Layout für {size} · {n} Grössen gemerkt':
        '현재: {size}의 레이아웃 · 크기 {n}개 기억됨',
    'Position zurückgesetzt (automatisch).':
        '위치가 초기화되었습니다(자동).',
    'keine Map':
        '맵 없음',
    'ausgeblendet':
        '숨겨짐',
    'Menü offen':
        '메뉴 열림',
    'aktives Fenster ist {window}':
        '활성 창: {window}',
    'DBD-Fenster {w}×{h}':
        'DBD 창 {w}×{h}',
    'Bildschirm':
        '화면',
    'Overlay sichtbar bei {pos} über {src}.':
        '오버레이가 {src} 위 {pos}에 표시됩니다.',
    'Overlay pausiert: {reason}.':
        '오버레이 일시 중지: {reason}.',
    '{text} – Details in fogscout.log':
        '{text} – 자세한 내용은 fogscout.log',
    '{text} ({n}× seit {since}) – Details in fogscout.log':
        '{text}({since} 이후 {n}회) – 자세한 내용은 fogscout.log',
    'Erkennung neu gestartet ({n}/{total})':
        '인식 다시 시작됨({n}/{total})',
    'Map-Banner gefunden, lese …':
        '맵 배너를 찾았습니다. 읽는 중 …',
    'automatisch erkannt ({p})':
        '자동 인식됨({p})',
    'Layout {n} ({p})':
        '레이아웃 {n}({p})',
    'Rundentimer gestartet.':
        '라운드 타이머가 시작되었습니다.',
    'Rundentimer gestoppt: {time}.':
        '라운드 타이머 중지: {time}.',
    'Erkannt: {map} – gelesen „{name}“ / „{realm}“':
        '인식됨: {map} – ‘{name}’ / ‘{realm}’ 읽음',
    'Layout unsicher – falls falsch: Layout-Knopf oder {keys}.':
        '레이아웃 불확실 – 틀렸다면: 레이아웃 버튼 또는 {keys}.',
    'Mitten in der Runde „{name}“ / „{realm}“ gelesen (am ehesten {map}) – ignoriert: Map-Banner gibt es nur am Rundenstart, und die Lesung war nicht eindeutig.':
        '라운드 도중 ‘{name}’ / ‘{realm}’을(를) 읽었습니다(가장 가까운 맵: {map}) – 무시됨: 맵 배너는 라운드 시작 때만 나타나며, 읽은 결과가 명확하지 않았습니다.',
    'Banner gesehen, aber keine bekannte Map: „{text}“. Map manuell wählen oder mit „Zuordnen …“ dauerhaft zuordnen.':
        '배너는 보였지만 알려진 맵이 아닙니다: ‘{text}’. 맵을 직접 선택하거나 ‘지정 …’으로 영구히 지정하세요.',
    'Runde vorbei ({reason}) – Overlay ausgeblendet.':
        '라운드 종료({reason}) – 오버레이 숨겨짐.',
    'Runde vorbei ({reason}).':
        '라운드 종료({reason}).',
    'Menü offen (Mauszeiger sichtbar) – Overlay pausiert.':
        '메뉴 열림(마우스 포인터 보임) – 오버레이 일시 중지.',
    'Zurück im Spiel – Overlay wieder sichtbar.':
        '게임으로 돌아옴 – 오버레이가 다시 표시됩니다.',
    'Die Erkennung ist abgestürzt – Details in fogscout.log':
        '인식 기능이 중단되었습니다 – 자세한 내용은 fogscout.log',
    'Die Erkennung ist abgestürzt:':
        '인식 기능이 중단되었습니다:',
    'Die Erkennung ist abgestürzt – bitte Fog Scout neu starten.':
        '인식 기능이 중단되었습니다 – Fog Scout를 다시 시작하세요.',
    'Nichts gefunden':
        '찾은 것 없음',
    'Runde gilt jetzt für {map} (vorher {old}).':
        '이제 이 라운드는 {map}(으)로 집계됩니다(이전: {old}).',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen. Bis zum Neustart wird nichts gespeichert.':
        'settings.json을 읽을 수 없습니다({error}) – 기본값을 불러왔습니다. 다시 시작할 때까지 아무것도 저장되지 않습니다.',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen, die alte Datei liegt als settings.json.broken daneben.':
        'settings.json을 읽을 수 없습니다({error}) – 기본값을 불러왔고, 이전 파일은 settings.json.broken으로 보관했습니다.',
    'Scan fehlgeschlagen: {error}':
        '스캔 실패: {error}',
    'per Scan gefunden: „{text}“':
        '스캔으로 찾음: ‘{text}’',
    'Scan ({s} s): {map}':
        '스캔({s}초): {map}',
    'Realm „{realm}“ hat nur diese Map':
        '렐름 ‘{realm}’에는 이 맵만 있습니다',
    'Scan: Realm „{realm}“ gefunden – bitte Map in der Liste wählen.':
        '스캔: 렐름 ‘{realm}’을(를) 찾았습니다 – 목록에서 맵을 선택하세요.',
    'Scan ({s} s): kein Map- oder Realm-Name auf dem Bildschirm.':
        '스캔({s}초): 화면에 맵 또는 렐름 이름이 없습니다.',
    'Ergebnisbildschirm':
        '결과 화면',
    'Lobby/Menü':
        '로비/메뉴',
    'Ladebildschirm':
        '로딩 화면',
    'Clip wird geladen …':
        '클립을 불러오는 중 …',
    'Vorschaubild und Zeitleiste kommen aus der Aufnahme.':
        '미리 보기 이미지와 타임라인을 녹화에서 읽습니다.',
    '{n} von {total} Bildern':
        '이미지 {n}/{total}',
    'Lädt länger als erwartet – das Fenster ist trotzdem bedienbar.':
        '예상보다 오래 걸립니다 – 창은 그래도 작동합니다.',
    'DBD wurde geschlossen':
        'DBD가 닫혔습니다',
    'Menü/Lobby (Mauszeiger lange sichtbar)':
        '메뉴/로비(마우스 포인터가 오래 보임)',
    'keine Map angezeigt':
        '표시된 맵 없음',
    'Runde vorbei ({reason})':
        '라운드 종료({reason})',
    'wartet, bis du im Match bist (Map manuell gewählt)':
        '매치에 들어갈 때까지 대기 중(맵을 직접 선택함)',
    'Menü offen – Overlay pausiert':
        '메뉴 열림 – 오버레이 일시 중지',
    'im Match':
        '매치 중',
    'Ausblenden nach der Runde aus':
        '라운드 후 숨기기 꺼짐',
    'Mauszeiger-Hinweis aus':
        '마우스 포인터 신호 꺼짐',
    'Mauszeiger-Hinweis ab dem nächsten Map-Banner':
        '다음 맵 배너부터 마우스 포인터 신호 사용',
    'Mauszeiger: –':
        '마우스 포인터: –',
    'Mauszeiger sichtbar':
        '마우스 포인터 보임',
    'Mauszeiger verborgen':
        '마우스 포인터 숨겨짐',
    'aus (Einstellung)':
        '꺼짐(설정)',
    'Runde vorbei – wartet auf die nächste Map':
        '라운드 종료 – 다음 맵을 기다리는 중',
    'Automatische Erkennung ist aus':
        '자동 인식이 꺼져 있습니다',
    'DBD ist minimiert':
        'DBD가 최소화되어 있습니다',
    'DBD gefunden ({w}×{h}) – warte auf Map-Banner':
        'DBD를 찾았습니다({w}×{h}) – 맵 배너를 기다리는 중',
    'DBD nicht gefunden – Erkennung startet, sobald DBD läuft':
        'DBD를 찾을 수 없습니다 – DBD가 실행되면 인식이 시작됩니다',
    'Bildschirmaufnahme fehlgeschlagen: {error}':
        '화면 캡처 실패: {error}',
    'Aufnahme ist schwarz – DBD im Modus „Fenster-Vollbild“ betreiben':
        '캡처가 검은색입니다 – DBD를 ‘창 모드 전체 화면’으로 실행하세요',
    'Fensteraufnahme nicht möglich, nutze Bildschirmaufnahme ({error})':
        '창 캡처를 할 수 없어 화면 캡처를 사용합니다({error})',
    'DBD im Hintergrund – Fensteraufnahme aktiv: die Map wird auch erkannt, wenn andere Fenster darüber liegen.':
        'DBD가 백그라운드에 있음 – 창 캡처 활성: 다른 창이 가려도 맵을 인식합니다.',
    'Rundenende-Erkennung für die gewählte Map ist jetzt aktiv.':
        '선택한 맵의 라운드 종료 인식이 이제 활성화되었습니다.',
    'Mauszeiger war beim Map-Banner sichtbar – Menü-Erkennung per Mauszeiger ist für diese Runde aus.':
        '맵 배너 때 마우스 포인터가 보였습니다 – 이번 라운드에는 마우스 포인터로 메뉴를 인식하지 않습니다.',
    'Map zuordnen':
        '맵 지정',
    'Gelesen: „{text}“':
        '읽음: ‘{text}’',
    'Welche Map war das? Der Name wird künftig automatisch erkannt.':
        '어떤 맵이었나요? 이제부터 이 이름을 자동으로 인식합니다.',
    'Bitte eine Map auswählen.':
        '맵을 선택하세요.',
    'Abbrechen':
        '취소',
    '„{text}“ wird jetzt als {map} erkannt (eigene Zuordnung).':
        '‘{text}’은(는) 이제 {map}(으)로 인식됩니다(직접 지정).',
    'zugeordnet: „{text}“':
        '지정됨: ‘{text}’',
    'Der gelesene Text ist zu kurz.':
        '읽은 텍스트가 너무 짧습니다.',
    'Unbekannte Map.':
        '알 수 없는 맵입니다.',
    '„{text}“ ist schon der Name von {map}.':
        '‘{text}’은(는) 이미 {map}의 이름입니다.',
    'Kartenbild hinzufügen':
        '맵 이미지 추가',
    'eigenes Bild':
        '내 이미지',
    'Kartenbild gespeichert: {path}':
        '맵 이미지 저장됨: {path}',
    'Eigenes Kartenbild für {map} gespeichert: {path}':
        '{map}의 내 맵 이미지 저장됨: {path}',
    'wird ab jetzt automatisch erkannt.':
        '이제부터 자동으로 인식됩니다.',
    'Eigenes Kartenbild für {map} gelöscht – das mitgelieferte gilt wieder.':
        '{map}의 내 맵 이미지가 삭제되었습니다 – 기본 제공 이미지가 다시 사용됩니다.',
    'Bitte den Namen der Map eingeben.':
        '맵 이름을 입력하세요.',
    '„{name}“ gibt es schon ({map}) – dann „Bild einer vorhandenen Map ersetzen“ wählen.':
        '‘{name}’은(는) 이미 있습니다({map}) – 대신 ‘기존 맵의 이미지 교체’를 선택하세요.',
    'Noch kein Bild gewählt (PNG, JPG, WebP, GIF)':
        '아직 선택한 이미지가 없습니다(PNG, JPG, WebP, GIF)',
    'Für welche Map?':
        '어떤 맵에 사용하나요?',
    'Ergebnis':
        '결과',
    'Eigenes Bild löschen':
        '내 이미지 삭제',
    'Speichern':
        '저장',
    'Bilder':
        '이미지',
    'Kartenbild wählen':
        '맵 이미지 선택',
    'Für diese Map lässt sich kein Bild speichern.':
        '이 맵에는 이미지를 저장할 수 없습니다.',
    'Erst ein Bild wählen.':
        '먼저 이미지를 선택하세요.',
    'Das ist kein lesbares Bild: {error}':
        '읽을 수 있는 이미지가 아닙니다: {error}',
    'Bild konnte nicht verarbeitet werden: {error}':
        '이미지를 처리할 수 없습니다: {error}',
    'Speichern fehlgeschlagen: {error}':
        '저장 실패: {error}',
    'Eigenes Bild für „{map}“ löschen?':
        '‘{map}’의 내 이미지를 삭제할까요?',
    'Löschen fehlgeschlagen: {error}':
        '삭제 실패: {error}',
    'Bild wählen …':
        '이미지 선택 …',
    'Bild einer vorhandenen Map ersetzen':
        '기존 맵의 이미지 교체',
    'Neue Map (fehlt im Programm)':
        '새 맵(프로그램에 없음)',
    'Name':
        '이름',
    'Name so, wie er im Map-Banner steht – dann wird die Map automatisch erkannt.':
        '맵 배너에 표시되는 이름 – 그러면 맵이 자동으로 인식됩니다.',
    'Hintergrund entfernen (Dunkelblau und Graulila der Community-Karten) und Rand abschneiden':
        '배경(커뮤니티 맵의 짙은 파란색과 회보라색)을 제거하고 테두리를 잘라냄',
    'Ordner öffnen':
        '폴더 열기',
    'Animiertes GIF: wird unverändert übernommen.':
        '움직이는 GIF: 그대로 사용됩니다.',
    'Wird gestartet …':
        '시작하는 중 …',
    'Version {version}':
        '버전 {version}',
    'Lade Maps …':
        '맵을 불러오는 중 …',
    'Bereite Overlay vor …':
        '오버레이를 준비하는 중 …',
    'Baue Oberfläche …':
        '인터페이스를 만드는 중 …',
    'Starte Erkennung …':
        '인식 기능을 시작하는 중 …',
    'Öffne Fenster …':
        '창을 여는 중 …',
    'Fog Scout ist bereit.':
        'Fog Scout가 준비되었습니다.',
    'Automatische Erkennung':
        '자동 인식',
    'Aufnahmen mit OBS':
        'OBS로 녹화',
    'Lobby-Meldung':
        '로비 알림',
    'Spielserver anzeigen':
        '게임 서버 표시',
    'Systemwerte im Spiel':
        '게임 내 시스템 값',
    '„Heute“ im Spiel':
        '게임 내 ‘오늘’',
    'Musik im Spiel':
        '게임 내 음악',
    'Discord-Status':
        'Discord 상태',
    'Spotify „Als nächstes“':
        'Spotify ‘다음 곡’',
    'YouTube-Upload':
        'YouTube 업로드',
    '{name} eingeschaltet.':
        '{name} 켜짐.',
    '{name} ausgeschaltet.':
        '{name} 꺼짐.',
    'Erkennt die Map beim Match-Start am Banner und blendet die Karte ein. Aus: nur noch von Hand (Scannen, Map wählen). Dasselbe Häkchen steht unter Einstellungen → Erkennung.':
        '매치가 시작되면 배너에서 맵을 읽고 맵을 표시합니다. 끄기: 직접만(스캔, 맵 선택). 같은 상자가 설정 → 인식에도 있습니다.',
    'OBS nimmt jede Runde auf: Start beim Map-Banner, Stopp beim Rundenende. Aus: keine neue Aufnahme und keine F8-Clips – eine laufende Aufnahme endet normal mit der Runde. Alles Weitere unter Einstellungen → Aufnahmen.':
        'OBS가 모든 라운드를 녹화합니다: 맵 배너에서 시작, 라운드 종료 시 중지. 끄기: 새 녹화와 F8 클립 없음 – 진행 중인 녹화는 평소처럼 라운드와 함께 끝납니다. 나머지는 모두 설정 → 녹화에 있습니다.',
    'Ton und Hinweisfenster, sobald DBD eine Lobby gefunden hat. Die Erinnerung beim Countdown und „nur wenn DBD nicht vorne ist“ bleiben unter Einstellungen → Erkennung → Benachrichtigungen.':
        'DBD가 로비를 찾으면 바로 소리와 알림 창. 카운트다운 알림과 ‘DBD가 맨 앞에 없을 때만’은 설정 → 인식 → 알림에 있습니다.',
    'Zeigt Region und Ping des verbundenen Spielservers – auf der Seite Server, im Overlay und in der Statistik. Einschalten fragt Windows einmal nach Administratorrechten; gelesen werden nur Paketköpfe, nie Inhalte.':
        '연결된 게임 서버의 지역과 핑을 서버 페이지, 오버레이, 통계에 표시합니다. 켤 때 Windows가 한 번 관리자 권한을 요청합니다. 패킷 헤더만 읽고 내용은 절대 읽지 않습니다.',
    'Die Karte mit CPU-/GPU-Temperatur, Last und Speicher im schwarzen Balken. Einschalten bringt sie an die Position, an der sie zuletzt stand; Position und Zeilen unter Overlay → Systemwerte.':
        '검은 여백에 CPU/GPU 온도, 부하, 메모리를 표시하는 카드. 켜면 마지막 위치에 다시 표시됩니다. 위치와 행은 오버레이 → 시스템 값에 있습니다.',
    'Die Karte „Heute“ im Spiel: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit. Position unter Overlay → Heute.':
        '게임 내 ‘오늘’ 카드: 라운드, 플레이 시간, 평균 처치/탈출, 시계. 위치는 오버레이 → 오늘에 있습니다.',
    'Die Musikkarte „Läuft gerade“ im Spiel (Titel, Interpret, Cover aus der Windows-Mediensteuerung). Position und Aussehen unter Overlay → Musik.':
        '게임 내 ‘지금 재생 중’ 음악 카드(Windows 미디어 컨트롤의 제목, 아티스트, 커버). 위치와 모양은 오버레이 → 음악에 있습니다.',
    'Rich Presence: Map, Rolle und Rundenzeit in deinem Discord-Status. Application-ID und Einzelheiten unter Einstellungen → Verbindungen → Discord.':
        'Rich Presence: Discord 상태에 맵, 역할, 라운드 시간을 표시합니다. 애플리케이션 ID와 세부 설정은 설정 → 연결 → Discord에 있습니다.',
    'Die Liste „Als nächstes“ aus Spotify in der Musikkarte. Client-ID und Anmeldung unter Einstellungen → Verbindungen → Spotify.':
        '음악 카드에 Spotify의 ‘다음 곡’ 목록을 표시합니다. 클라이언트 ID와 로그인은 설정 → 연결 → Spotify에 있습니다.',
    'Neue Clips (F8, Editor) gehen von selbst auf YouTube. Aus: nichts Neues wird eingereiht – was schon in der Warteschlange steht, lädt fertig; Runden lädst du weiter per Rechtsklick hoch. Einstellungen → Verbindungen → YouTube.':
        '새 클립(F8, 편집기)이 자동으로 YouTube에 올라갑니다. 끄기: 새로 대기열에 넣지 않습니다 – 이미 대기열에 있는 것은 끝까지 올라가며, 라운드는 계속 오른쪽 클릭으로 업로드할 수 있습니다. 설정 → 연결 → YouTube.',
    'Werkzeuge für die Fehlersuche ein- oder ausklappen: Live-Zustand der Rundenende-Erkennung, Debug-Bilder, Bildschirm scannen.':
        '문제 해결 도구 표시 또는 숨기기: 라운드 종료 인식의 실시간 상태, 디버그 이미지, 화면 스캔.',
    'Klicken und die neue Tastenkombination drücken: Strg/Alt + Taste, oder eine Taste allein (F1–F12, Numpad, Pause, Rollen, Einfg, Pos1, Ende, Bild↑/↓ – die gilt nur, solange DBD vorne ist). Esc bricht ab, Entf schaltet den Hotkey aus.':
        '클릭하고 새 키 조합을 누르세요: Ctrl/Alt + 키, 또는 단일 키(F1–F12, 숫자 키패드, Pause, Scroll Lock, Insert, Home, End, Page Up/Down – DBD가 맨 앞에 있을 때만 작동). Esc는 취소, Delete는 단축키를 끕니다.',
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
        'DBD가 맨 앞에 있을 때만 작동합니다 – DBD 자체는 더 이상 {keys}을(를) 받지 않습니다(DBD에서 할당되지 않았나요?).',
    'Map-Namen in dieser Spielsprache erkennen. Nur die Sprachen anhaken, in denen du spielst – weniger Sprachen, weniger Verwechslungen.':
        '이 게임 언어로 된 맵 이름을 인식합니다. 플레이하는 언어만 체크하세요 – 언어가 적을수록 혼동이 줄어듭니다.',
    'Meldungen der Art „{category}“ im Log anzeigen.':
        '로그에 ‘{category}’ 메시지 표시.',
    'Karte ausblenden (die automatische Erkennung läuft weiter).':
        '맵 숨기기(자동 인식은 계속 실행됨).',
    'Karte wieder einblenden.':
        '맵을 다시 표시합니다.',
    'Die Erkennung war beim Layout nicht sicher – stimmt es nicht, hier weiterschalten.':
        '인식 기능이 레이아웃을 확신하지 못했습니다 – 틀렸다면 여기서 전환하세요.',
    'Wechselt zum nächsten Layout dieser Map (z. B. Coal Tower ↔ Coal Tower II). Die Layouts ab II gibt es seit Patch 8.6.0 nur noch in Custom Games.':
        '이 맵의 다음 레이아웃으로 전환합니다(예: Coal Tower ↔ Coal Tower II). 패치 8.6.0부터 II 이후의 레이아웃은 사용자 지정 게임에만 있습니다.',
    'Test sofort beenden.':
        '지금 테스트를 끝냅니다.',
    'Zeigt 10 s lang alles, was das Overlay im Match zeigt – Karte, Systemwerte, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – an den eingestellten Stellen, auch ohne DBD. Nochmal drücken beendet den Test.':
        '오버레이가 매치에서 보여 주는 모든 것 – 맵, 시스템 값, ‘오늘’, 음악(아무것도 없으면 예시 값) – 을 DBD 없이도 제자리에 10초 동안 표시합니다. 다시 누르면 테스트가 끝납니다.',
    'Verschieben beenden.':
        '이동을 멈춥니다.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen – falls die automatische Erkennung das Banner verpasst hat.':
        '화면 전체에서 맵 또는 렐름 이름을 바로 찾습니다 – 자동 인식이 배너를 놓쳤을 때.',
    'Eigenes Kartenbild für diese unbekannte Map anlegen – Name und Realm sind schon eingetragen, der Hintergrund wird automatisch entfernt.':
        '이 알 수 없는 맵의 이미지를 직접 만듭니다 – 이름과 렐름은 이미 채워져 있고 배경은 자동으로 제거됩니다.',
    'Der gelesene Name gehört zu einer vorhandenen Map (z. B. anders geschrieben)? Einmal zuordnen – danach wird er automatisch erkannt.':
        '읽은 이름이 기존 맵의 것인가요(예: 다른 철자)? 한 번 지정하면 이후에는 자동으로 인식됩니다.',
    'Hinweis ausblenden.':
        '이 안내를 숨깁니다.',
    'Eigenes Bild für eine Map wählen: vorhandenes Bild ersetzen oder neue Map anlegen. Rand und Hintergrund werden automatisch entfernt.':
        '맵에 쓸 이미지를 직접 선택합니다: 기존 이미지를 교체하거나 새 맵을 만듭니다. 테두리와 배경은 자동으로 제거됩니다.',
    'Position wieder auf „automatisch“ stellen (auf Ultrawide im linken schwarzen Rand).':
        '위치를 ‘자동’으로 되돌립니다(울트라와이드에서는 왼쪽 검은 여백).',
    'Auf breiten Monitoren bleibt die Karte im schwarzen Balken, in dem sie liegt, und wird bei Bedarf verkleinert. Mitten über dem Spiel platziert gilt keine Begrenzung. Ohne schwarze Balken neben dem Spielbild (16:9, z. B. 1920×1080) sind die Balken-Optionen ausgegraut.':
        '와이드 모니터에서 맵은 들어 있는 검은 여백 안에 머물며 필요하면 작아집니다. 게임 화면 가운데 위에 두면 제한이 없습니다. 게임 화면 옆에 검은 여백이 없으면(16:9, 예: 1920×1080) 여백 옵션이 회색으로 표시됩니다.',
    'Karte ausblenden, solange ein anderes Fenster (Browser, Discord …) im Vordergrund ist.':
        '다른 창(브라우저, Discord …)이 맨 앞에 있는 동안 맵을 숨깁니다.',
    'Zusätzliche Namenszeile über der Karte – die meisten Kartenbilder tragen den Namen schon selbst.':
        '맵 위의 추가 이름 줄 – 대부분의 맵 이미지에는 이미 이름이 표시되어 있습니다.',
    'Zeit seit dem Einblenden der Karte, gross unter der Karte.':
        '맵이 나타난 후 경과 시간을 맵 아래에 크게 표시합니다.',
    'Region und Ping des Spielservers unter der Karte. Braucht „Verbundener Spielserver“ im Tab Server.':
        '게임 서버의 지역과 핑을 맵 아래에 표시합니다. 서버 탭의 ‘연결된 게임 서버’가 필요합니다.',
    'Aus: Karte liegt auf einem dunklen Rechteck – besser lesbar über hellen Spielszenen.':
        '끄기: 맵이 어두운 사각형 위에 표시됩니다 – 밝은 게임 장면에서 읽기 쉽습니다.',
    'Liest das Map-Banner am Match-Anfang und blendet die passende Karte ein. Aus: Map nur von Hand wählen.':
        '매치가 시작될 때 맵 배너를 읽고 해당 맵을 표시합니다. 끄기: 맵을 직접만 선택합니다.',
    'Blendet die Karte nach der Runde aus (Ergebnisbildschirm, Lobby, Ladebildschirm, DBD beendet).':
        '라운드 후 맵을 숨깁니다(결과 화면, 로비, 로딩 화면, DBD 닫힘).',
    'Karte verschwindet, solange der Mauszeiger im Spiel sichtbar ist (ESC-Menü), und kommt danach wieder.':
        '게임에서 마우스 포인터가 보이는 동안(ESC 메뉴) 맵이 사라졌다가 그 후 다시 나타납니다.',
    'Fensteraufnahme wie bei OBS: erkennt das Banner auch, wenn DBD verdeckt ist. Nur solange DBD im Hintergrund ist.':
        'OBS처럼 창 캡처: DBD가 가려져도 배너를 인식합니다. DBD가 백그라운드에 있을 때만.',
    'Speichert gelesene Banner und verkleinerte Bilder der Runde im Ordner debug/ – nur zur Fehlersuche, kostet Speicherplatz.':
        '읽은 배너와 라운드의 작은 이미지를 debug/ 폴더에 저장합니다 – 문제 해결용으로만, 디스크 공간을 차지합니다.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen.':
        '화면 전체에서 맵 또는 렐름 이름을 바로 찾습니다.',
    'Kopiert technische Infos (Fenster, Overlay, letzte Rundenende-Prüfungen) in die Zwischenablage – zum Weitergeben bei Problemen.':
        '기술 정보(창, 오버레이, 최근 라운드 종료 검사)를 클립보드에 복사합니다 – 문제가 생겼을 때 전달용.',
    'Misst den Ping zu allen AWS-Regionen (UDP-Beacon von Amazon GameLift).':
        '모든 AWS 지역까지의 핑을 측정합니다(Amazon GameLift의 UDP 비컨).',
    'Nur die angehakten Regionen erlauben – trägt die übrigen in die Windows-hosts-Datei ein (fragt nach Administratorrechten).':
        '체크한 지역만 허용합니다 – 나머지는 Windows hosts 파일에 추가됩니다(관리자 권한 요청).',
    'Entfernt die Einträge des Programms aus der hosts-Datei – alle Regionen wieder erlaubt.':
        'hosts 파일에서 프로그램의 항목을 제거합니다 – 모든 지역이 다시 허용됩니다.',
    'Log-Anzeige leeren (die Log-Datei bleibt).':
        '로그 보기를 지웁니다(로그 파일은 유지).',
    'Öffnet fogscout.log mit allen Details.':
        '모든 세부 정보가 담긴 fogscout.log를 엽니다.',
    'Dunkle oder helle Darstellung des Steuerfensters.':
        '제어 창의 어두운 또는 밝은 모양.',
    'Alle Hotkeys auf die Voreinstellung zurücksetzen.':
        '모든 단축키를 기본값으로 되돌립니다.',
    'Minimieren versteckt das Fenster im Infobereich; Doppelklick auf das Symbol holt es zurück.':
        '최소화하면 창이 알림 영역에 숨겨집니다. 아이콘을 더블 클릭하면 다시 나타납니다.',
    'Startet das Programm bei der Anmeldung im Infobereich. Nur als Administrator änderbar.':
        '로그인할 때 알림 영역에서 프로그램을 시작합니다. 관리자만 바꿀 수 있습니다.',
    'Holt beim Start über die Verknüpfung den neuen Stand von GitHub. Eigene Änderungen werden nie überschrieben.':
        '바로 가기로 시작할 때 GitHub에서 최신 버전을 가져옵니다. 직접 수정한 내용은 절대 덮어쓰지 않습니다.',
    'Alle eigenen Map-Zuordnungen löschen (die Namen werden dann wieder als unbekannt gemeldet).':
        '직접 지정한 맵을 모두 삭제합니다(이름은 다시 알 수 없음으로 보고됨).',
    'Öffnet den Ordner mit den mitgelieferten Kartenbildern.':
        '기본 제공 맵 이미지가 있는 폴더를 엽니다.',
    'PNG, JPG, WebP oder GIF auswählen – zum Beispiel ein Original mit Hintergrund.':
        'PNG, JPG, WebP 또는 GIF를 선택하세요 – 예를 들어 배경이 있는 원본.',
    'Dein Bild ersetzt das mitgelieferte Bild dieser Map (bzw. dieses Layouts). Löschen stellt das Original wieder her.':
        '내 이미지가 이 맵(또는 이 레이아웃)의 기본 제공 이미지를 대체합니다. 삭제하면 원본이 복원됩니다.',
    'Legt eine neue Map an. Sie wird erkannt, wenn der Name so geschrieben ist wie im Map-Banner.':
        '새 맵을 만듭니다. 이름을 맵 배너와 같게 쓰면 인식됩니다.',
    'Öffnet den Ordner user_maps mit deinen eigenen Kartenbildern.':
        '내 맵 이미지가 있는 user_maps 폴더를 엽니다.',
    'Löscht dein Bild für die gewählte Map – danach gilt wieder das mitgelieferte.':
        '선택한 맵의 내 이미지를 삭제합니다 – 기본 제공 이미지가 다시 사용됩니다.',
    'Bild umwandeln und speichern; die Karte wird sofort angezeigt.':
        '이미지를 변환하고 저장합니다. 맵이 바로 표시됩니다.',
    'Schliessen, ohne etwas zu ändern.':
        '아무것도 바꾸지 않고 닫습니다.',
    'Macht Dunkelblau (#282a42) und Graulila (#535781) der Community-Karten transparent, schneidet den gleichfarbigen Rand ab und bringt das Bild auf 1280 px Höhe.':
        '커뮤니티 맵의 짙은 파란색(#282a42)과 회보라색(#535781)을 투명하게 하고, 같은 색의 테두리를 잘라내고, 이미지를 높이 1280px로 조정합니다.',
    '? unsicher – {keys} = falsch':
        '? 불확실 – {keys} = 틀림',
    'Falsch erkannt':
        '잘못된 맵',
    'Stimmt':
        '맞음',
    'Unsicher erkannt: {map} (gelesen „{name}“)':
        '불확실한 인식: {map}(‘{name}’ 읽음)',
    'Unsicher erkannt: {map} – gelesen „{name}“, Passung {fit}. Falls falsch: {keys} oder „Falsch erkannt“.':
        '불확실한 인식: {map} – ‘{name}’ 읽음, 일치도 {fit}. 틀렸다면: {keys} 또는 ‘잘못된 맵’.',
    '{map} bestätigt.':
        '{map} 확인됨.',
    'Nichts zu verwerfen: keine automatisch erkannte Map eingeblendet.':
        '버릴 것이 없습니다: 자동 인식된 맵이 표시되어 있지 않습니다.',
    'Verworfen: {map} – die Runde wird nicht gezählt.':
        '버림: {map} – 이 라운드는 집계되지 않습니다.',
    'Die erkannte Map stimmt nicht: Karte ausblenden, Timer zurücksetzen, die Runde wird nicht gezählt. Geht auch im Spiel mit dem Hotkey (Standard Strg+Alt+X).':
        '인식된 맵이 틀렸습니다: 맵을 숨기고 타이머를 초기화하며 라운드는 집계되지 않습니다. 게임에서 단축키(기본 Ctrl+Alt+X)로도 가능합니다.',
    'Die Map stimmt – Hinweis „unsicher“ ausblenden.':
        '맵이 맞습니다 – ‘불확실’ 표시를 숨깁니다.',
    'als falsch verworfen':
        '틀린 것으로 버림',
    'Ping {ms} ms':
        '핑 {ms}ms',
    'Ø Kills':
        '평균 처치',
    '4K':
        '4K',
    'Entkommen':
        '탈출',
    'entkommen':
        '탈출',
    'tot':
        '사망',
    'aufgegeben':
        '포기',
    'verlassen':
        '나감',
    'Stats-Seite öffnen, wenn DBD beendet wird':
        'DBD를 닫으면 통계 페이지 열기',
    'Userscript kopieren':
        '유저스크립트 복사',
    'Stats-Seite öffnen':
        '통계 페이지 열기',
    '⚠ Unbekannter Status auf der Stats-Seite: {list} – zählt nicht. Bitte melden („Diagnose kopieren“).':
        '⚠ 통계 페이지의 알 수 없는 상태: {list} – 집계되지 않음. 알려 주세요(‘진단 정보 복사’).',
    '⚠ Lücke: zwischen {start} und {end} fehlen vielleicht Matches – die Seite zeigt nur die letzten 30. Seite öfter öffnen.':
        '⚠ 빈틈: {start}에서 {end} 사이의 매치가 빠졌을 수 있습니다 – 페이지는 최근 30개만 보여 줍니다. 페이지를 더 자주 여세요.',
    '⚠ {n}× andere Map als erkannt, zuletzt {when}: erkannt {ours}, laut Seite {theirs}.':
        '⚠ 인식과 다른 맵 {n}회, 마지막 {when}: 인식 {ours}, 페이지 {theirs}.',
    '⚠ Das Userscript ist veraltet (Version {old}, aktuell {new}) – „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '⚠ 유저스크립트가 오래되었습니다(버전 {old}, 최신 {new}) – ‘유저스크립트 복사’를 누르고 Tampermonkey에서 교체하세요.',
    'Stats-Seite konnte nicht geöffnet werden: {error}':
        '통계 페이지를 열 수 없습니다: {error}',
    'DBD beendet – Stats-Seite geöffnet; das Userscript speichert die Matches.':
        'DBD 닫힘 – 통계 페이지를 열었습니다. 유저스크립트가 매치를 저장합니다.',
    'Userscript nicht gefunden: {error}':
        '유저스크립트를 찾을 수 없습니다: {error}',
    'Userscript in die Zwischenablage kopiert. In Tampermonkey: „Neues Skript erstellen“ → alles ersetzen (Strg+A, Strg+V) → Speichern. Danach stats.deadbydaylight.com öffnen und anmelden.':
        '유저스크립트를 클립보드에 복사했습니다. Tampermonkey에서: ‘새 스크립트 만들기’ → 모두 교체(Ctrl+A, Ctrl+V) → 저장. 그다음 stats.deadbydaylight.com을 열고 로그인하세요.',
    'Offizielle Match-Daten: {n} Matches gelesen, {new} neu – Datei gelöscht.':
        '공식 매치 데이터: 매치 {n}개 읽음, 새 매치 {new}개 – 파일 삭제됨.',
    'Offizielle Match-Daten: zwischen {start} und {end} fehlen vielleicht Matches (die Seite zeigt nur die letzten 30).':
        '공식 매치 데이터: {start}에서 {end} 사이의 매치가 빠졌을 수 있습니다(페이지는 최근 30개만 보여 줌).',
    '{name} gelesen, aber nicht gelöscht: {error}':
        '{name}을(를) 읽었지만 삭제하지 못했습니다: {error}',
    '{name} ist keine Match-Datei von Fog Scout – bleibt liegen.':
        '{name}은(는) Fog Scout 매치 파일이 아닙니다 – 그대로 둡니다.',
    'Unbekannter Status auf der Stats-Seite: „{status}“ – zählt nicht für Kills/Escapes. Bitte melden.':
        '통계 페이지의 알 수 없는 상태: ‘{status}’ – 처치/탈출에 집계되지 않습니다. 알려 주세요.',
    'Schliesst du DBD nach mindestens einer Runde, öffnet das Programm stats.deadbydaylight.com im Browser. Das Userscript speichert dann die letzten 30 Matches, das Programm liest sie ein und löscht die Datei. Nie während DBD läuft.':
        '라운드를 한 번 이상 한 후 DBD를 닫으면 프로그램이 브라우저에서 stats.deadbydaylight.com을 엽니다. 유저스크립트가 최근 30개 매치를 저장하고, 프로그램이 이를 읽은 후 파일을 삭제합니다. DBD 실행 중에는 절대 열지 않습니다.',
    'Kopiert das Userscript in die Zwischenablage. In Tampermonkey „Neues Skript erstellen“, alles ersetzen und speichern. Es liest nur die Match-Liste, die die Seite selbst lädt – keine Konto- oder Login-Daten – und schickt nichts irgendwohin.':
        '유저스크립트를 클립보드에 복사합니다. Tampermonkey에서 ‘새 스크립트 만들기’, 모두 교체하고 저장하세요. 페이지가 직접 불러오는 매치 목록만 읽으며 – 계정이나 로그인 데이터는 읽지 않음 – 어디에도 아무것도 보내지 않습니다.',
    'Öffnet stats.deadbydaylight.com jetzt. Mit installiertem Userscript kommen die Matches gleich danach an.':
        '지금 stats.deadbydaylight.com을 엽니다. 유저스크립트가 설치되어 있으면 매치가 바로 들어옵니다.',
    'Vom Programm erkannt: {seen} von {n} ({share})':
        '프로그램이 인식함: {n}개 중 {seen}개({share})',
    'Nicht erkannt (oder das Programm lief nicht): {list}':
        '인식하지 못함(또는 프로그램이 실행 중이 아니었음): {list}',
    'Rundenende erkannt: Median {off} gegenüber dem Ende laut Seite ({n} Runden; + = später)':
        '라운드 종료 인식: 페이지의 종료 시각 대비 중앙값 {off}({n}라운드, + = 더 늦음)',
    '{n} Mio.':
        '{n}M',
    'Ø BP':
        '평균 BP',
    '✓ {n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '✓ 라운드 종료를 {n}회 인식하지 못했지만 통계 페이지의 길이로 집계했습니다.',
    'Runden vom Map-Banner bis zum Rundenende (ab 1 min), nur lokal gespeichert. Kills, Escapes und Bloodpoints laut stats.deadbydaylight.com, sobald eine Runde dort zugeordnet ist.':
        '맵 배너부터 라운드 종료까지의 라운드(1분 이상), 로컬에만 저장됩니다. 처치, 탈출, 블러드포인트는 라운드가 stats.deadbydaylight.com의 매치와 연결되면 그곳에서 가져옵니다.',
    '{n}× Abandon':
        '포기 {n}회',
    'Ein Skin oder neuer Killer steht unter seinem eigenen Namen? Zeile markieren, Killer wählen, „Zuordnen“ – gilt auch rückwirkend.':
        '의상이나 새 살인마가 자체 이름으로 표시되나요? 행을 선택하고 살인마를 고른 후 ‘지정’ – 지난 라운드에도 적용됩니다.',
    'Abgleich mit der Stats-Seite':
        '통계 페이지와 비교',
    'Noch keine offiziellen Daten.':
        '아직 공식 데이터가 없습니다.',
    'Neu seit {version}':
        '{version} 이후 새로운 기능',
    'sofort':
        '즉시',
    'HWiNFO läuft nicht: CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen.':
        'HWiNFO가 실행 중이 아닙니다: CPU 온도, CPU 전력, 코어, FPS가 없습니다.',
    'Systemwerte: HWiNFO läuft nicht – CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen in dieser Runde.':
        '시스템 값: HWiNFO가 실행 중이 아닙니다 – 이번 라운드에는 CPU 온도, CPU 전력, 코어, FPS가 없습니다.',
    'Vorwoche {value}':
        '지난주 {value}',
    '{n} Pkt.':
        '{n}점',
    'Montag bis jetzt gegenüber der Vorwoche (Mo–So); Custom und Farming zählen nicht.':
        '월요일부터 지금까지를 지난주(월–일)와 비교합니다. 사용자 지정 게임과 파밍은 집계되지 않습니다.',
    'Sicherung: {files} nach {folder}/ kopiert (die letzten {n} Stände bleiben).':
        '백업: {files}을(를) {folder}/에 복사했습니다(최근 사본 {n}개 보관).',
    '{n} Dateien, zuletzt {day}':
        '파일 {n}개, 최신 {day}',
    '1 Datei, zuletzt {day}':
        '파일 1개, 최신 {day}',
    'behalten (nie aufgeräumt)':
        '보관됨(정리되지 않음)',
    'wartet auf den YouTube-Upload':
        'YouTube 업로드 대기 중',
    'auf YouTube':
        'YouTube에 있음',
    'Karte im Spiel':
        '게임 내 맵',
    'OBS läuft nicht, oder sein WebSocket-Server ist aus':
        'OBS가 실행 중이 아니거나 WebSocket 서버가 꺼져 있습니다',
    'OBS antwortet nicht':
        'OBS가 응답하지 않습니다',
    'OBS hat die Verbindung getrennt':
        'OBS가 연결을 닫았습니다',
    'noch keine':
        '아직 없음',
    'Tägliche Kopie von rounds.jsonl und official.jsonl nach {folder}/ (nur bei Änderungen, die letzten {n} Stände je Datei; vor „Alle Runden löschen“ eine zusätzliche): {state}':
        'rounds.jsonl과 official.jsonl을 매일 {folder}/에 복사합니다(변경이 있을 때만, 파일마다 최근 사본 {n}개, ‘모든 라운드 삭제’ 전에 하나 더): {state}',
    'Verstanden':
        '확인',
    'Aus HISTORY.md (Deutsch), die neuesten zuerst.':
        'HISTORY.md(독일어)에서, 최신순.',
    'Blendet die Karte „Neu seit …“ aus, bis die nächste neue Version kommt.':
        '다음 새 버전이 나올 때까지 ‘… 이후 새로운 기능’ 카드를 숨깁니다.',
    'Offizielle Match-Daten':
        '공식 매치 데이터',
    'Einmal einrichten: Tampermonkey im Browser installieren, „Userscript kopieren“ und dort als neues Skript einfügen und speichern, auf stats.deadbydaylight.com anmelden. Chrome/Edge: in den Details der Erweiterung „Allow User Scripts“ einschalten, sonst läuft kein Skript. Beim Öffnen der Seite speichert das Skript neue Matches (die letzten 30) im Download-Ordner; das Programm liest die Datei und löscht sie. Es geht dafür selbst nicht ins Internet.':
        '한 번 설정: 브라우저에 Tampermonkey를 설치하고, ‘유저스크립트 복사’ 후 거기에 새 스크립트로 붙여 넣어 저장하고, stats.deadbydaylight.com에 로그인하세요. Chrome/Edge: 확장 프로그램 세부 정보에서 ‘사용자 스크립트 허용’을 켜야 스크립트가 실행됩니다. 페이지가 열리면 스크립트가 새 매치(최근 30개)를 다운로드 폴더에 저장하고, 프로그램이 파일을 읽은 후 삭제합니다. 이를 위해 프로그램이 직접 인터넷에 접속하지는 않습니다.',
    'Alle Matches neu speichern':
        '모든 매치 다시 저장',
    'Öffnet die Stats-Seite so, dass das Userscript ihre letzten 30 Matches noch einmal speichert, auch wenn keines neu ist – nach einer Neuinstallation oder wenn die Datei verloren ging.':
        '새 매치가 없어도 유저스크립트가 최근 30개 매치를 한 번 더 저장하도록 통계 페이지를 엽니다 – 새로 설치한 후나 파일을 잃어버렸을 때.',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) speichert ihre letzten 30 Matches noch einmal, auch wenn keines neu ist; das Programm übernimmt sie gleich – bekannte zählen nur einmal. Kommt keine Datei: in der Console des Browsers (F12) steht, ob das Skript läuft. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '브라우저에서 통계 페이지가 열립니다. 유저스크립트(버전 {n} 이상)는 새 매치가 없어도 최근 30개 매치를 한 번 더 저장하고, 프로그램이 바로 가져옵니다 – 이미 아는 매치는 한 번만 집계됩니다. 파일이 오지 않으면: 브라우저 콘솔(F12)에서 스크립트가 실행되는지 알 수 있습니다. 이전 유저스크립트: 먼저 ‘유저스크립트 복사’를 누르고 Tampermonkey에서 교체하세요.',
    'Verlauf':
        '추세',
    'Nur Runden, die einem Match auf der Stats-Seite zugeordnet sind. Die Maus über einer Säule zeigt Wert und Anzahl der Runden.':
        '통계 페이지의 매치와 연결된 라운드만. 막대에 마우스를 올리면 값과 라운드 수가 표시됩니다.',
    'Killer – Ø Kills {per}':
        '살인마 – 평균 처치 {per}',
    'Survivor – entkommen {per}':
        '생존자 – 탈출 {per}',
    'pro Stunde':
        '시간당',
    'pro Tag':
        '일별',
    'pro Woche':
        '주별',
    'KW {n}':
        '{n}주',
    '{when}: Ø {kills} Kills · {n} Runden':
        '{when}: 평균 {kills}처치 · {n}라운드',
    '{when}: {share} entkommen · {n} Runden':
        '{when}: {share} 탈출 · {n}라운드',
    'Keine Killer-Runden mit offiziellen Daten in dieser Auswahl.':
        '이 선택에는 공식 데이터가 있는 살인마 라운드가 없습니다.',
    'Keine Survivor-Runden mit offiziellen Daten in dieser Auswahl.':
        '이 선택에는 공식 데이터가 있는 생존자 라운드가 없습니다.',
    'Ø {kills} Kills':
        '평균 {kills}처치',
    '{share} entkommen':
        '{share} 탈출',
    'Meldung, wenn Match-Daten eingelesen und gelöscht wurden':
        '매치 데이터를 읽고 삭제하면 알림',
    'Zeigt unten rechts kurz, wie viele Matches gelesen wurden und dass die Datei gelöscht ist – nicht, solange DBD im Vordergrund ist. Im Log steht es immer.':
        '매치를 몇 개 읽었는지와 파일이 삭제되었음을 오른쪽 아래에 잠깐 표시합니다 – DBD가 맨 앞에 있을 때는 표시하지 않습니다. 로그에는 항상 기록됩니다.',
    '{n} Matches gelesen, davon {new} neu. Die Datei wurde gelöscht.':
        '매치 {n}개를 읽었고 그중 {new}개가 새 매치입니다. 파일이 삭제되었습니다.',
    '{name} wurde gelesen, konnte aber nicht gelöscht werden – Details im Log.':
        '{name}을(를) 읽었지만 삭제할 수 없습니다 – 자세한 내용은 로그에 있습니다.',
    'Links oben (über der Karte)':
        '왼쪽 위(맵 위)',
    'Rechts oben':
        '오른쪽 위',
    'GPU: {name}':
        'GPU: {name}',
    'GPU: keine NVIDIA-Karte gefunden':
        'GPU: NVIDIA 카드를 찾을 수 없음',
    'CPU-Temperatur: aus HWiNFO':
        'CPU 온도: HWiNFO에서',
    'Systemwerte (CPU/GPU-Temperatur, Auslastung, VRAM, RAM)':
        '시스템 값(CPU/GPU 온도, 부하, VRAM, RAM)',
    'nach Map':
        '맵별',
    'nach Killer':
        '살인마별',
    'GPU Ø °C':
        'GPU 평균 °C',
    'GPU max':
        'GPU 최대',
    'CPU Ø °C':
        'CPU 평균 °C',
    'CPU max':
        'CPU 최대',
    'GPU Ø Last':
        'GPU 평균 부하',
    'Ø Watt':
        '평균 와트',
    'Noch keine Systemwerte in dieser Auswahl (Tab Overlay → Systemwerte einschalten).':
        '이 선택에는 아직 시스템 값이 없습니다(오버레이 탭 → 시스템 값 켜기).',
    'GPU DROSSELT (TEMP.)':
        'GPU 스로틀링(온도)',
    'GPU DROSSELT (HW)':
        'GPU 스로틀링(HW)',
    'Hotspot max {v} °C':
        '핫스팟 최대 {v}°C',
    'Hotspot max':
        '핫스팟 최대',
    'GPU-Temperatur – Ø {per}':
        'GPU 온도 – 평균 {per}',
    'Noch keine GPU-Temperaturen in dieser Auswahl.':
        '이 선택에는 아직 GPU 온도가 없습니다.',
    '{when}: Ø {avg} °C · max {max} °C · {n} Runden':
        '{when}: 평균 {avg}°C · 최대 {max}°C · {n}라운드',
    'Werte der Systemwerte-Anzeige (Tab Overlay) während der Runden – nur Runden, in denen sie eingeschaltet war. CPU-Temperatur nur mit HWiNFO. „Wann/Wo“ zeigt, auf welchen Maps oder zu welcher Tageszeit der PC am heißesten läuft. „Gedrosselt“: Sekunden, in denen die GPU wegen Temperatur oder Hardware langsamer lief (nur NVIDIA). „–“: in diesen Runden nicht erfasst – CPU-Temperatur, -Leistung, Kerne und FPS gibt es nur, solange HWiNFO läuft, und jeder Wert braucht mindestens 10 Sekunden Messwerte in der Runde.':
        '라운드 동안의 시스템 값 표시(오버레이 탭) 값 – 표시가 켜져 있던 라운드만. CPU 온도는 HWiNFO가 있을 때만. ‘언제/어디서’는 어떤 맵이나 시간대에 PC가 가장 뜨거운지 보여 줍니다. ‘스로틀링’: 온도나 하드웨어 때문에 GPU가 느려진 초(NVIDIA만). ‘–’: 해당 라운드에 기록되지 않음 – CPU 온도, 전력, 코어, FPS는 HWiNFO가 실행 중일 때만 있으며, 모든 값은 라운드에서 최소 10초의 측정이 필요합니다.',
    'Eigene Position (mit der Maus verschieben)':
        '사용자 지정 위치(마우스로 끌기)',
    'SYSTEMWERTE':
        '시스템 값',
    'Direkt über der Karte (wandert mit)':
        '맵 바로 위(맵과 함께 이동)',
    'Schriftgrösse':
        '글꼴 크기',
    'Übersicht':
        '개요',
    'Aktuelle Map':
        '현재 맵',
    'Rundenzeit':
        '라운드 시간',
    'Ping':
        '핑',
    'läuft':
        '진행 중',
    'letzte Runde':
        '마지막 라운드',
    'startet':
        '시작 중',
    '4K: {n} von {total}':
        '4K: {total}회 중 {n}회',
    '{n} Survivor-Runden':
        '생존자 라운드 {n}회',
    '{n} normal':
        '일반 {n}회',
    '{n} Farming-Runden · Ø {bp} BP':
        '파밍 라운드 {n}회 · 평균 {bp} BP',
    'Spielzeit heute: {time}':
        '오늘 플레이: {time}',
    'Systemwerte sind aus (Tab Overlay → Systemwerte).':
        '시스템 값이 꺼져 있습니다(오버레이 탭 → 시스템 값).',
    'Systemwerte gibt es nur unter Windows.':
        '시스템 값은 Windows에서만 사용할 수 있습니다.',
    'Erscheinen, sobald DBD läuft.':
        'DBD가 실행되면 바로 표시됩니다.',
    'OK':
        '확인',
    '4 Kills · leer = weniger als {n} Runden':
        '4킬 · 비어 있음 = {n}라운드 미만',
    'Killer × Map – Ø Kills laut Stats-Seite':
        '살인마 × 맵 – 통계 페이지 기준 평균 처치',
    'Maps – am häufigsten gespielt':
        '맵 – 가장 많이 플레이함',
    'Median {time}':
        '중앙값 {time}',
    'Noch keine Killer-Runde mit Ergebnis von der Stats-Seite.':
        '아직 통계 페이지 결과가 있는 살인마 라운드가 없습니다.',
    'keine Killer-Runden mit Stats-Daten':
        '통계 데이터가 있는 살인마 라운드 없음',
    'keine Survivor-Runden mit Stats-Daten':
        '통계 데이터가 있는 생존자 라운드 없음',
    '{map} · {killer}: Ø {kills} Kills ({n} Runden)':
        '{map} · {killer}: 평균 {kills}처치({n}라운드)',
    '{n} Matches':
        '매치 {n}개',
    '{time} gespielt':
        '{time} 플레이',
    'Ø Bloodpoints':
        '평균 블러드포인트',
    'Ø Rundendauer':
        '평균 라운드 길이',
    'Anzeigen':
        '표시',
    'Kartenbild nicht lesbar: {error}':
        '맵 이미지를 읽을 수 없습니다: {error}',
    'Keine Map gewählt':
        '선택한 맵 없음',
    'Blendet die gewählte Map jetzt als Overlay ein – die Erkennung übernimmt beim nächsten Match wieder.':
        '선택한 맵을 지금 오버레이에 표시합니다 – 다음 매치에서 다시 인식 기능이 맡습니다.',
    'Ziehen, um den Kasten zu verschieben':
        '끌어서 이 상자 이동',
    'Anordnung zurücksetzen':
        '배치 초기화',
    'Die Kästen der Seiten lassen sich am Griff rechts im Titel verschieben.':
        '페이지의 상자는 제목 오른쪽의 손잡이로 옮길 수 있습니다.',
    'Stellt die Kästen auf allen Seiten, die Reiter-Reihen (Statistik, Overlay) und die Navigation links wieder in die ursprüngliche Reihenfolge.':
        '모든 페이지의 상자, 탭 행(통계, 오버레이), 왼쪽 탐색을 원래 순서로 되돌립니다.',
    'Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der du Dead by Daylight spielst (mehrere gehen).':
        '매치가 시작되면 프로그램이 이미지에서 맵 이름을 읽습니다. Dead by Daylight를 플레이하는 언어를 체크하세요(여러 개도 됩니다).',
    'Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.':
        '매치가 시작되면 맵이 자동으로 나타나고 라운드 후에 사라집니다. ‘자동’은 게임 화면 옆 검은 여백(울트라와이드) 또는 DBD 창 옆에 표시합니다.',
    'Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle Tasten findest du später unter Einstellungen.':
        '가장 중요한 키 – 클릭해서 바꾼 다음 새 조합을 누르세요. 모든 키는 나중에 설정에 있습니다.',
    'Einrichtung starten':
        '설정 시작',
    'Öffnet noch einmal die Einrichtung vom ersten Start: Spielsprache, Overlay-Position und die wichtigsten Tasten.':
        '처음 시작할 때의 설정을 다시 엽니다: 게임 언어, 오버레이 위치, 가장 중요한 키.',
    'Suchen (Strg+F)':
        '검색(Ctrl+F)',
    'Strg+F':
        'Ctrl+F',
    'Suchen: Einstellung, Seite, Map, Aktion, Runde …':
        '검색: 설정, 페이지, 맵, 동작, 라운드 …',
    'Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst':
        '화살표 키로 선택 · Enter로 열기 · Ctrl+Enter로 게임 또는 녹화에서 열기 · Esc로 닫기',
    'Aktionen':
        '동작',
    'Seiten':
        '페이지',
    'Vorschlag von Claude':
        'Claude 제안',
    'Enter':
        'Enter',
    'Strg+Enter':
        'Ctrl+Enter',
    'Claude fragen: „{q}“':
        'Claude에게 묻기: ‘{q}’',
    'Schickt nur die Frage und die Namen der Einstellungen an Claude':
        '질문과 설정 이름만 Claude에게 보냅니다',
    'Claude denkt nach …':
        'Claude가 생각하는 중 …',
    'Claude hat nichts Passendes gefunden.':
        'Claude가 맞는 것을 찾지 못했습니다.',
    'Claude hat die Frage abgelehnt.':
        'Claude가 질문을 거절했습니다.',
    'Claude hat unverständlich geantwortet.':
        'Claude의 답변을 읽을 수 없습니다.',
    'Claude ist nicht erreichbar – keine Internetverbindung?':
        'Claude에 연결할 수 없습니다 – 인터넷 연결이 없나요?',
    'Claude: Zu viele Anfragen – gleich noch einmal versuchen.':
        'Claude: 요청이 너무 많습니다 – 잠시 후 다시 시도하세요.',
    'Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen.':
        'API 키 없음 – 설정 → 연결 → Claude에서 입력하세요.',
    'Zeigt im grossen Clip-Editor den Abschnitt „Mit Claude bearbeiten“: Du schreibst, was mit dem Schnitt passieren soll, Claude schlägt Schritte vor, du übernimmst oder verwirfst sie. Gesendet werden nur deine Bitte und der Schnitt als Zahlen – kein Bild, kein Dateiname. Braucht einen eigenen API-Key.':
        '큰 클립 편집기에 ‘Claude로 편집’ 섹션을 표시합니다: 편집에 원하는 내용을 쓰면 Claude가 단계를 제안하고, 적용하거나 버릴 수 있습니다. 요청과 숫자로 된 편집 정보만 전송됩니다 – 이미지나 파일 이름은 보내지 않습니다. 본인의 API 키가 필요합니다.',
    'Claude':
        'Claude',
    'Im Clip-Editor Claude nutzen':
        '클립 편집기에서 Claude 사용',
    'Mit Claude bearbeiten':
        'Claude로 편집',
    'z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short':
        '예: 처음 10초 삭제, 0:40부터 2배속, 쇼츠로',
    'Vorschlagen':
        '제안',
    'Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst.':
        '요청과 숫자로 된 편집 정보(시간, 속도, 페이드 – 이미지와 파일 이름 없음)를 Claude에게 보냅니다. 적용하기 전에는 아무것도 바뀌지 않습니다.',
    'Übernehmen':
        '적용',
    'Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z).':
        '제안된 단계를 실행합니다 – 한 번에 실행 취소(Ctrl+Z) 가능.',
    'Verwerfen':
        '버리기',
    'Vergisst den Vorschlag; der Schnitt bleibt, wie er ist.':
        '제안을 버립니다. 편집은 그대로 유지됩니다.',
    'Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude nutzen“ einschalten und einen API-Key eintragen.':
        '꺼짐 – 설정 → 연결 → Claude에서 ‘클립 편집기에서 Claude 사용’을 켜고 API 키를 입력하세요.',
    'Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen.':
        '그사이에 편집이 바뀌었습니다 – 다시 제안을 요청하세요.',
    'Claude hat keinen passenden Schritt gefunden.':
        'Claude가 맞는 단계를 찾지 못했습니다.',
    'Übernommen – Strg+Z macht es rückgängig.':
        '적용됨 – Ctrl+Z로 되돌릴 수 있습니다.',
    'übersprungen: {why}':
        '건너뜀: {why}',
    'unbekannte Aktion':
        '알 수 없는 동작',
    'Zeiten fehlen':
        '시간 없음',
    'Bereich zu kurz oder ausserhalb':
        '범위가 너무 짧거나 벗어남',
    'Tempo nicht erlaubt':
        '제공되지 않는 속도',
    '{a}–{b} mit Tempo {f}×':
        '{a}–{b} {f}× 속도',
    'würde alles entfernen':
        '모두 제거하게 됨',
    '{a}–{b} herausgeschnitten':
        '{a}–{b} 잘라냄',
    'nur {a}–{b} behalten':
        '{a}–{b}만 남김',
    'Stelle ausserhalb':
        '시점이 범위를 벗어남',
    'Schnitt bei {a}':
        '{a}에서 분할',
    'keine Änderung':
        '변경 없음',
    'Blende ungültig':
        '제공되지 않는 페이드',
    'Standbild: Dauer ungültig':
        '정지 화면: 허용되지 않는 길이',
    'Untertitel zu kurz':
        '자막이 너무 짧음',
    '{n} weitere Schritte nicht ausgeführt (höchstens {max})':
        '단계 {n}개는 더 실행하지 않음(최대 {max}개)',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen.':
        '지금은 할 수 없습니다 – 현재 편집을 먼저 마친 후 적용하세요.',
    'Standbild bei {a} für {s} s':
        '{a}에서 {s}초 정지 화면',
    'Blende ohne Dauer':
        '길이 없는 페이드',
    'Blenden: ein {i} s, aus {o} s':
        '페이드: 인 {i}초, 아웃 {o}초',
    'Export-Art unbekannt':
        '알 수 없는 내보내기 형식',
    'Export-Art: {m}':
        '내보내기 형식: {m}',
    'nur bei Export-Art Short':
        '쇼츠 내보내기 형식에서만',
    'Text fehlt':
        '텍스트 없음',
    'Short-Titel „{t}“':
        '쇼츠 제목 ‘{t}’',
    'Untertitel: Zeiten fehlen':
        '자막: 시간 없음',
    'zu viele Untertitel':
        '자막이 너무 많음',
    'Untertitel {a}–{b}':
        '자막 {a}–{b}',
    'Claude: Der API-Key wird nicht angenommen – unter Einstellungen → Verbindungen prüfen („API-Key holen“ öffnet die Anthropic Console).':
        'Claude: API 키가 받아들여지지 않습니다 – 설정 → 연결에서 확인하세요(‘API 키 받기’는 Anthropic Console을 엽니다).',
    'Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen → Verbindungen → „Guthaben aufladen“.':
        'Claude: API 계정에 크레딧이 남아 있지 않습니다 – 설정 → 연결 → ‘크레딧 추가’.',
    'API-Key holen':
        'API 키 받기',
    'Guthaben aufladen':
        '크레딧 추가',
    'Öffnet die Seite „API keys“ der Anthropic Console im Browser (platform.claude.com). Dort einen Key anlegen und hier einfügen – er beginnt mit sk-ant-.':
        '브라우저에서 Anthropic Console의 ‘API keys’ 페이지(platform.claude.com)를 엽니다. 거기서 키를 만들어 여기에 붙여 넣으세요 – sk-ant-로 시작합니다.',
    'Öffnet die Seite „Billing“ der Anthropic Console im Browser. Die API wird getrennt von einem Claude-Abo im Voraus bezahlt; dort lässt sich auch ein monatliches Ausgabenlimit setzen.':
        '브라우저에서 Anthropic Console의 ‘Billing’ 페이지를 엽니다. API는 Claude 구독과 별도로 선불로 결제하며, 거기서 월 지출 한도도 설정할 수 있습니다.',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude fragen“. Erst wenn du sie wählst, gehen deine Frage und die Namen der Einstellungen, Seiten und Aktionen an Claude (api.anthropic.com) – nie Runden, Maps oder Spieldaten. Braucht einen eigenen API-Key.':
        '검색(Ctrl+F)에 ‘Claude에게 묻기’ 행을 표시합니다. 그 행을 선택할 때만 질문과 설정, 페이지, 동작의 이름이 Claude(api.anthropic.com)에게 전송됩니다 – 라운드, 맵, 게임 데이터는 절대 보내지 않습니다. 본인의 API 키가 필요합니다.',
    'Schickt eine kleine Probefrage an Claude und sagt, ob der API-Key angenommen wird (kostet einen kleinen Betrag deines API-Guthabens).':
        'Claude에게 작은 테스트 질문을 보내 API 키가 받아들여지는지 알려 줍니다(API 크레딧이 약간 사용됨).',
    'Entfernt den API-Key von diesem PC; die Suche fragt Claude dann nicht mehr.':
        '이 PC에서 API 키를 제거합니다. 그러면 검색이 더 이상 Claude에게 묻지 않습니다.',
    'In der Suche Claude fragen können':
        '검색에서 Claude에게 묻기',
    'API-Key':
        'API 키',
    'Key prüfen':
        '키 확인',
    'Key löschen':
        '키 삭제',
    'Claude: Key funktioniert.':
        'Claude: 키가 작동합니다.',
    'Claude: prüfe den Key …':
        'Claude: 키를 확인하는 중 …',
    'Claude: kein API-Key eingetragen.':
        'Claude: 입력한 API 키가 없습니다.',
    'Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-).':
        'Claude: API 키처럼 보이지 않습니다(sk-ant-로 시작해야 함).',
    'Claude: Key eingetragen.':
        'Claude: 키가 입력되었습니다.',
    'Schritt {n} von {total}':
        '{n}/{total}단계',
    'Sprache':
        '언어',
    'Sprache dieses Programms:':
        '이 프로그램의 언어:',
    'Weiter':
        '다음',
    'Zurück':
        '뒤로',
    'Überspringen':
        '건너뛰기',
    'Einrichtung: {step}':
        '설정: {step}',
    'Aufgeteilt':
        '세부 항목',
    'CPU-Temperatur':
        'CPU 온도',
    'GPU gedrosselt':
        'GPU 스로틀링',
    'GPU-Leistung':
        'GPU 전력',
    'GPU-Speicher':
        'GPU 메모리',
    'GPU-Temperatur':
        'GPU 온도',
    'Hotspot':
        '핫스팟',
    'Höchstwert':
        '최고',
    'Höchstwerte':
        '최고 값',
    'RAM':
        'RAM',
    'Runden, zusammen {time}':
        '라운드, 총 {time}',
    'VRAM':
        'VRAM',
    'Wert':
        '값',
    '{n} von {total}':
        '{n}/{total}',
    'Ø CPU-Temperatur':
        '평균 CPU 온도',
    'Ø GPU-Last':
        '평균 GPU 부하',
    'Ø GPU-Leistung':
        '평균 GPU 전력',
    'Ø GPU-Temperatur':
        '평균 GPU 온도',
    'über {n} Runden':
        '{n}라운드 기준',
    'Bilanz: Ø 2,8 Kills · 12 Runden':
        '기록: 평균 2.8처치 · 12라운드',
    'Infos und Schrift (Name, Timer, Bilanz, Server)':
        '정보와 텍스트(이름, 타이머, 기록, 서버)',
    'Eigenes Element unter der Karte':
        '맵 아래의 별도 요소',
    'Eigenes Element über der Karte':
        '맵 위의 별도 요소',
    'Eigenes Element, eigene Position':
        '별도 요소, 별도 위치',
    'Mit der Karte verbunden, unten':
        '맵에 붙임, 아래',
    'Mit der Karte verbunden, oben':
        '맵에 붙임, 위',
    'Infos':
        '정보',
    'INFOS':
        '정보',
    'Infos (Timer, Bilanz, Server)':
        '정보(타이머, 기록, 서버)',
    'In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine Sofort-Clips (F8) und keinen Vorlauf.':
        'OBS의 리플레이 버퍼가 켜져 있지 않습니다 – OBS: 설정 → 출력 → 리플레이 버퍼 → ‘리플레이 버퍼 사용’을 켜고 적용하세요. 없으면 즉석 클립(F8)과 사전 녹화가 없습니다.',
    'Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)':
        'OBS에서 리플레이 버퍼가 켜져 있지 않음(설정 → 출력 → 리플레이 버퍼)',
    'Karten im selben Balken gleich breit':
        '같은 여백의 카드를 같은 너비로',
    'Zu einer Spalte zusammenführen':
        '한 열로 합치기',
    'Die Karten, die im selben schwarzen Balken stehen, werden so breit gezeichnet wie die breiteste von ihnen – untereinander ergeben sie eine Spalte mit bündigen Rändern.':
        '같은 검은 여백에 있는 카드들을 그중 가장 넓은 카드 너비로 그립니다 – 위아래로 쌓으면 가장자리가 맞는 하나의 열이 됩니다.',
    'Heute unter die Systemwerte, die Musik unter Heute, alle gleich breit – eine Spalte im Balken der Systemwerte. Rückgängig mit Strg+Z.':
        '오늘은 시스템 값 아래, 음악은 오늘 아래, 모두 같은 너비로 – 시스템 값 여백에 하나의 열. Ctrl+Z로 되돌립니다.',
    'Cover':
        '커버',
    'Discord-Overlay freihalten':
        'Discord 오버레이 영역 비우기',
    'Karte, Infos, Systemwerte, Heute und Musik weichen den Stellen aus, an denen Discords Overlay seine Widgets zeigt (in der Vorschau schraffiert). Das Programm liest nichts aus Discord – die Flächen sind fest.':
        '맵, 정보, 시스템 값, 오늘, 음악이 Discord 오버레이가 위젯을 표시하는 곳(미리 보기에서 빗금)을 피합니다. 프로그램은 Discord에서 아무것도 읽지 않습니다 – 영역은 고정되어 있습니다.',
    'Wie der Stil':
        '스타일에 따름',
    'Rund':
        '둥글게',
    'Eckig':
        '사각형',
    '{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr (der schwarze Balken ist voll).':
        '{what}은(는) 여기서 최대 크기입니다 – {cap}%부터는 슬라이더가 아무것도 바꾸지 않습니다(검은 여백이 꽉 참).',
    'Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).':
        '‘맵이 여백보다 커질 수 있음’을 켜면 더 커집니다(그러면 게임 화면 안으로 들어감).',
    'Spielbild':
        '게임 화면',
    'Map-Name':
        '맵 이름',
    'Farbthema':
        '색상 테마',
    'Gold (Standard)':
        '골드(기본)',
    'Blutrot':
        '핏빛 빨강',
    'Eisblau':
        '얼음 파랑',
    'Giftgrün':
        '독성 초록',
    'Lila':
        '보라',
    '„Heute“: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit':
        '‘오늘’: 라운드, 플레이 시간, 평균 처치/탈출, 시계',
    'Eine eigene Karte, solange eine Map im Match zu sehen ist: wie viele Runden du heute gespielt hast, wie lange, Ø Kills bzw. Entkommen laut Stats-Seite und die Uhrzeit. Position darunter, Grösse über den Grössenregler („Heute“ wählen).':
        '매치에서 맵이 화면에 있는 동안 표시되는 별도 카드: 오늘 플레이한 라운드 수, 플레이 시간, 통계 페이지 기준 평균 처치 또는 탈출, 현재 시각. 위치는 아래, 크기는 크기 슬라이더로(‘오늘’ 선택).',
    'Dunkle Fläche hinter „Heute“':
        '‘오늘’ 뒤 어두운 영역',
    'Vorlage':
        '프리셋',
    'Vorlage anwenden':
        '프리셋 적용',
    'Alles links':
        '모두 왼쪽',
    'Alles rechts':
        '모두 오른쪽',
    'Verteilt: Karte links, Werte rechts':
        '분산: 맵은 왼쪽, 값은 오른쪽',
    'Vorlage „{name}“ angewendet.':
        '프리셋 ‘{name}’ 적용됨.',
    'Setzt Karte, Systemwerte, „Heute“ und Musik auf einmal auf die gewählte Anordnung. „Rückgängig“ holt die vorherige zurück.':
        '맵, 시스템 값, ‘오늘’, 음악을 선택한 배치로 한 번에 옮깁니다. ‘실행 취소’로 이전 배치를 되돌립니다.',
    'Weich ein- und ausblenden':
        '부드럽게 나타나고 사라지기',
    'In kleinen DBD-Fenstern ausblenden':
        '작은 DBD 창에서는 숨기기',
    'Läuft DBD in einem kleinen Fenster (Bild kleiner als 1920×1080 oder schmaler als 16:9), zeigt das Programm im Spiel nichts – wie der Hauptschalter. Map-Erkennung, Statistik und OBS-Aufnahmen laufen weiter. Wird das Fenster wieder gross, erscheint das Overlay von selbst.':
        'DBD가 작은 창(1920×1080보다 작거나 16:9보다 좁은 화면)에서 실행되면 프로그램은 마스터 스위치처럼 게임에 아무것도 표시하지 않습니다. 맵 인식, 통계, OBS 녹화는 계속됩니다. 창이 다시 커지면 오버레이가 자동으로 돌아옵니다.',
    'Kleines DBD-Fenster ({w}×{h}) – Overlay ausgeblendet, Runden werden weiter gezählt und aufgenommen.':
        '작은 DBD 창({w}×{h}) – 오버레이 숨겨짐, 라운드는 계속 집계되고 녹화됩니다.',
    'Update gesperrt: eine Runde läuft. Nach dem Rundenende noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '업데이트 잠김: 라운드가 진행 중입니다. 라운드가 끝난 후 ‘업데이트 후 다시 시작’을 다시 클릭하세요.',
    'Alle Farming-Runden der Auswahl (Zeitraum, Region, Map, Modus) – unabhängig vom Rollen-Filter und von „Farming ausblenden“. Farming = Crossplay war in der Lobby aus (oder die eingestellte Farming-Region); korrigieren unter „Letzte Runden“ mit „Farming an/aus“. Aufnahmen liegen im Unterordner „Farming“ des Aufnahmeordners. Wartezeit „sofort“: die Lobby war voll, bevor eine Suchzeit messbar war. Server nur, wenn „Verbunden mit“ auf der Seite Server läuft.':
        '선택(기간, 지역, 맵, 모드)의 모든 파밍 라운드 – 역할 필터와 ‘파밍 숨기기’와 관계없이. 파밍 = 로비에서 크로스플레이가 꺼져 있었음(또는 설정한 파밍 지역). ‘최근 라운드’에서 ‘파밍 켜기/끄기’로 수정하세요. 녹화는 녹화 폴더의 ‘Farming’ 하위 폴더에 있습니다. 대기 ‘즉시’: 검색 시간을 측정하기 전에 로비가 찼습니다. 서버는 서버 페이지에서 ‘연결됨’이 실행 중일 때만.',
    'Keine Farming-Runden in dieser Auswahl.':
        '이 선택에는 파밍 라운드가 없습니다.',
    '{n} als Killer · {m} als Survivor':
        '살인마 {n}회 · 생존자 {m}회',
    'Spielzeit':
        '플레이 시간',
    'vom Map-Banner bis zum Rundenende':
        '맵 배너부터 라운드 종료까지',
    'BP':
        'BP',
    '{n} gespeicherte Matches haben ein Loadout, aber keines davon ist in dieser Auswahl. Custom Games zählen nur mit dem Rollen-Filter „Custom Games“, Farming-Runden nicht mit „Farming ausblenden“, Matches ohne erkannte Runde gar nicht.':
        '저장된 매치 {n}개에 로드아웃이 있지만 이 선택에는 하나도 없습니다. 사용자 지정 게임은 역할 필터 ‘사용자 지정 게임’에서만, 파밍 라운드는 ‘파밍 숨기기’가 켜져 있으면 집계되지 않으며, 인식된 라운드가 없는 매치는 전혀 집계되지 않습니다.',
    'DBD-Fenster wieder gross genug – Overlay wieder an.':
        'DBD 창이 다시 충분히 커졌습니다 – 오버레이가 다시 켜졌습니다.',
    'Overlay anzeigen':
        '오버레이 표시',
    'Hauptschalter: aus = das Programm zeigt im Spiel nichts (Karte, Systemwerte, Heute, Musik). Erkennung, Statistik und Aufnahmen laufen weiter. Auch als Knopf in der Übersicht.':
        '마스터 스위치: 끄기 = 프로그램이 게임에 아무것도 표시하지 않습니다(맵, 시스템 값, 오늘, 음악). 인식, 통계, 녹화는 계속됩니다. 개요에도 버튼이 있습니다.',
    'Overlay eingeschaltet.':
        '오버레이가 켜졌습니다.',
    'Overlay ausgeschaltet – die Erkennung läuft weiter.':
        '오버레이가 꺼졌습니다 – 인식은 계속됩니다.',
    'Overlay ausschalten':
        '오버레이 끄기',
    'Overlay einschalten':
        '오버레이 켜기',
    'Blendet alles aus, was das Programm im Spiel zeigt – Karte, Systemwerte, Heute, Musik. Die Erkennung, Statistik und Aufnahmen laufen weiter.':
        '프로그램이 게임에 표시하는 모든 것을 숨깁니다 – 맵, 시스템 값, 오늘, 음악. 인식, 통계, 녹화는 계속됩니다.',
    'Zeigt das Overlay im Spiel wieder an.':
        '게임에 오버레이를 다시 표시합니다.',
    'Karte, Systemwerte und „Heute“ blenden in einer Drittelsekunde ein und aus, statt hart zu erscheinen. Die Musik hat ihr eigenes Häkchen.':
        '맵, 시스템 값, ‘오늘’이 갑자기 나타나지 않고 1/3초 동안 부드럽게 나타나고 사라집니다. 음악에는 별도 체크 상자가 있습니다.',
    'Unter „Heute“':
        '‘오늘’ 아래',
    'Unter der Musik':
        '음악 아래',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter „Heute“.':
        '‘오늘’ 뒤에 모서리가 둥근 반투명 어두운 영역.',
    'HEUTE':
        '오늘',
    'ENTKOMMEN ':
        '탈출 ',
    'HEUTE ':
        '오늘 ',
    'UHR ':
        '시간 ',
    '{n} RUNDEN · {time}':
        '{n}라운드 · {time}',
    'Ø KILLS ':
        '평균 처치 ',
    'NORMAL ':
        '일반 ',
    'FARMING ':
        '파밍 ',
    'BP/H ':
        'BP/시 ',
    'OLED-Schwarz':
        'OLED 블랙',
    'Hintergründe in echtem Schwarz statt Dunkelgrau – passt zu OLED-Bildschirmen und geht mit jeder Akzentfarbe. Im hellen Modus ohne Wirkung.':
        '배경을 짙은 회색 대신 완전한 검은색으로 – OLED 화면에 어울리며 모든 강조 색상과 맞습니다. 라이트 모드에서는 효과가 없습니다.',
    'Eigene Farbe':
        '사용자 지정 색상',
    'Eigene Farbe …':
        '사용자 지정 색상 …',
    'Beliebige Farbe wählen – das Programm passt die Helligkeit an, bis alles lesbar ist.':
        '원하는 색상을 고르세요 – 프로그램이 모든 것을 읽을 수 있을 때까지 밝기를 조정합니다.',
    '„Läuft gerade“: Titel, Interpret und Cover':
        '‘지금 재생 중’: 제목, 아티스트, 커버',
    'Liest Titel und Interpret aus der Windows-Mediensteuerung (dieselbe Liste wie beim Lautstärkeregler von Windows) – nur Anzeige, das Programm steuert nichts und speichert nichts.':
        'Windows 미디어 컨트롤(Windows 볼륨 플라이아웃과 같은 목록)에서 제목과 아티스트를 읽습니다 – 표시만 하며, 프로그램은 아무것도 제어하거나 저장하지 않습니다.',
    'Unter den Systemwerten':
        '시스템 값 아래',
    'Rechts unten im Balken':
        '여백 오른쪽 아래',
    'Links unten im Balken':
        '여백 왼쪽 아래',
    'MUSIK':
        '음악',
    'läuft gerade':
        '지금 재생 중',
    'Albumcover zeigen':
        '앨범 커버 표시',
    'Auch Videos zeigen (YouTube, Twitch …) – aus: nur Musik':
        '동영상도 표시(YouTube, Twitch …) – 끄기: 음악만',
    'Die Mediensteuerung meldet auch Videos aus dem Browser. An: ein Video erscheint als „▶ Titel“ mit dem Kanal darunter. Aus: die Karte zeigt nur Musik. Unterschieden wird am Album: Musikdienste melden eins, ein Video nicht.':
        '미디어 컨트롤은 브라우저 동영상도 알려 줍니다. 켜기: 동영상이 ‘▶ 제목’으로, 아래에 채널이 표시됩니다. 끄기: 카드에 음악만 표시됩니다. 앨범으로 구분합니다: 음악 서비스는 앨범을 알려 주고 동영상은 그렇지 않습니다.',
    'Balken in der Farbe des Covers':
        '커버 색상의 진행 막대',
    'Dunkle Fläche hinter Karte und Infos':
        '맵과 정보 줄 뒤 어두운 영역',
    'Dunkle Fläche hinter den Systemwerten':
        '시스템 값 뒤 어두운 영역',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Karte, Timer und Infozeilen (auch hinter „Warte auf Map“) – gut lesbar über hellen Stellen im Spiel.':
        '맵, 타이머, 정보 줄 뒤(‘맵 대기 중’ 뒤에도) 모서리가 둥근 반투명 어두운 영역 – 게임의 밝은 부분 위에서도 읽기 쉽습니다.',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Systemwerten und „Heute“.':
        '시스템 값과 ‘오늘’ 뒤에 모서리가 둥근 반투명 어두운 영역.',
    'Restzeit statt Länge (−1:46)':
        '길이 대신 남은 시간(−1:46)',
    'Dunkle Fläche hinter der Musikkarte':
        '음악 카드 뒤 어두운 영역',
    'Weich ein- und ausblenden (auch beim nächsten Lied)':
        '부드럽게 나타나고 사라지기(다음 곡에서도)',
    'Der Fortschrittsbalken nimmt die Hauptfarbe des Albumcovers an, wie bei Spotify. Graue Cover: weiss.':
        '진행 막대가 Spotify처럼 앨범 커버의 주요 색상을 따릅니다. 회색 커버: 흰색.',
    'Rechts neben dem Balken steht, wie lange das Lied noch läuft, statt seiner Gesamtlänge.':
        '막대 오른쪽에 곡의 전체 길이 대신 남은 시간을 표시합니다.',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Cover und Text – gut lesbar, wenn die Karte über hellen Stellen im Spiel liegt.':
        '커버와 텍스트 뒤에 모서리가 둥근 반투명 어두운 영역 – 카드가 게임의 밝은 부분 위에 있을 때 읽기 쉽습니다.',
    'Die Musikkarte blendet in einer Drittelsekunde ein und aus, statt hart zu erscheinen – auch wenn ein neues Lied beginnt.':
        '음악 카드가 갑자기 나타나지 않고 1/3초 동안 부드럽게 나타나고 사라집니다 – 새 곡이 시작될 때도.',
    'Das Bild zum Lied links neben Titel und Interpret – Windows liefert es mit; es bleibt nur im Speicher.':
        '제목과 아티스트 왼쪽에 곡의 이미지 – Windows가 제공하며 메모리에만 남습니다.',
    'Gross – Cover oben, Titel darunter':
        '크게 – 위에 커버, 아래에 제목',
    'Kompakt – Cover links':
        '작게 – 왼쪽에 커버',
    'Fortschritt des Lieds zeigen':
        '곡 진행 상황 표시',
    'Unter Titel und Künstler: wie weit das Lied ist, mit Balken und Länge – wie in Spotify.':
        '제목과 아티스트 아래에 곡이 얼마나 진행되었는지 막대와 길이로 표시합니다 – Spotify처럼.',
    'KARTE · Strg+Mausrad = Grösse':
        '맵 · Ctrl+휠 = 크기',
    'Ziehst: {name}':
        '끄는 중: {name}',
    'Unter der Maus: {name}':
        '마우스 아래: {name}',
    'Kartenstil':
        '맵 스타일',
    'Kartenstil: {style}.':
        '맵 스타일: {style}.',
    'Map wählen …':
        '맵 선택 …',
    'Zur Seite Maps: eine Map von Hand anzeigen (Doppelklick oder „Anzeigen“). Beim nächsten Match übernimmt die automatische Erkennung wieder.':
        '맵 페이지로: 맵을 직접 표시합니다(더블 클릭 또는 ‘표시’). 다음 매치에서 다시 자동 인식이 맡습니다.',
    'Erscheint automatisch, sobald im Match das Map-Banner kommt – oder von Hand über „Map wählen“.':
        '매치에서 맵 배너가 나오면 자동으로 나타납니다 – 또는 ‘맵 선택’으로 직접.',
    'Wann zeigen':
        '표시 시점',
    'Alle Maps':
        '모든 맵',
    'Zuletzt gespielt':
        '최근 플레이',
    'Suchen: Name, Realm, Abkürzung …':
        '검색: 이름, 렐름, 약어 …',
    'Klick oder Enter = groß ansehen · Doppelklick oder Strg+Enter = jetzt anzeigen. Die Erkennung übernimmt beim nächsten Match wieder.':
        '클릭 또는 Enter = 크게 보기 · 더블 클릭 또는 Ctrl+Enter = 지금 표시. 다음 매치에서 다시 인식 기능이 맡습니다.',
    'Zurück zu den Karten des Realms (Esc).':
        '렐름의 맵으로 돌아가기(Esc).',
    'Allgemein':
        '일반',
    'Alle Einstellungen zurücksetzen':
        '모든 설정 초기화',
    'Alle Einstellungen auf die Auslieferung zurücksetzen? Runden, Match-Daten und eigene Bilder bleiben. Das Programm startet danach neu.':
        '모든 설정을 처음 상태로 되돌릴까요? 라운드, 매치 데이터, 내 이미지는 유지됩니다. 그 후 프로그램이 다시 시작됩니다.',
    'Alle Einstellungen zurückgesetzt.':
        '모든 설정이 초기화되었습니다.',
    'Standard wiederherstellen':
        '기본값 복원',
    'Ausschalten':
        '끄기',
    '{free} von {total} Regionen freigegeben':
        '지역 {total}개 중 {free}개 허용됨',
    'DBD läuft gerade – die Änderung gilt erst nach einem Neustart von DBD.':
        'DBD 실행 중 – 변경 사항은 DBD를 다시 시작한 후에 적용됩니다.',
    'Suchen …':
        '검색 …',
    'Setzt jede Einstellung auf die Auslieferung zurück (Overlay, Hotkeys, Erkennung, Server-Auswahl im Programm …). Runden, Match-Daten und eigene Bilder bleiben; das Programm startet danach neu. Vorher sichern: „Einstellungen exportieren“.':
        '모든 설정을 처음 상태로 되돌립니다(오버레이, 단축키, 인식, 프로그램의 지역 선택 …). 라운드, 매치 데이터, 내 이미지는 유지되며 그 후 프로그램이 다시 시작됩니다. 먼저 백업하세요: ‘설정 내보내기’.',
    'Grösse {pct} %':
        '크기 {pct}%',
    'Eigene Einstellungen dieser Map: {what}':
        '이 맵의 개별 설정: {what}',
    'Eigene Grösse und Drehung zurücksetzen':
        '개별 크기와 회전 초기화',
    'Kartenbild ersetzen …':
        '맵 이미지 교체 …',
    'Im schwarzen Rand, solange die Karte im Match zu sehen ist. GPU-Werte von NVIDIA (Treiber), CPU-Temperatur nur mit HWiNFO („Shared Memory Support“ an) – kein eigener Treiber.':
        '매치에서 맵이 화면에 있는 동안 검은 여백에 표시됩니다. GPU 값은 NVIDIA(드라이버)에서, CPU 온도는 HWiNFO(‘Shared Memory Support’ 켜기)가 있을 때만 – 자체 드라이버는 없습니다.',
    'Standard (wie ausgeliefert)':
        '표준(처음 상태)',
    'Fenster {size}':
        '창 {size}',
    'alle Fenstergrössen':
        '모든 창 크기',
    'Gilt für: {window}':
        '적용 대상: {window}',
    'Gilt für: {maps} · {window}':
        '적용 대상: {maps} · {window}',
    'nur {map}':
        '{map}만',
    'alle Maps (keine Map eingeblendet)':
        '모든 맵(화면에 맵 없음)',
    'Letzte 7 Tage':
        '최근 7일',
    'Letzte 30 Tage':
        '최근 30일',
    'Rolle/Killer':
        '역할/살인마',
    'Weitere 100 Runden anzeigen':
        '라운드 100개 더 보기',
    'Runden exportieren':
        '라운드 내보내기',
    '{n} Runden exportiert: {path}':
        '라운드 {n}개 내보냄: {path}',
    'Median':
        '중앙값',
    '{n} Runden':
        '{n}라운드',
    'Längste':
        '최장',
    'Die Liste zeigt die neuesten 100 Runden der Auswahl; jeder Klick hängt 100 ältere an.':
        '목록에는 선택의 최신 라운드 100개가 표시되며, 클릭할 때마다 이전 라운드 100개가 추가됩니다.',
    'Server-Tab öffnen':
        '서버 탭 열기',
    'Match-Daten einrichten …':
        '매치 데이터 설정 …',
    'Einrichten …':
        '설정 …',
    'Noch keine Runden heute':
        '오늘은 아직 라운드 없음',
    'Stats-Seite':
        '통계 페이지',
    'nicht eingerichtet':
        '설정 안 됨',
    'Match-Daten':
        '매치 데이터',
    'Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → Match-Daten → Offizielle Match-Daten).':
        '라운드의 처치, 탈출, 블러드포인트는 stats.deadbydaylight.com에서 가져옵니다 – 프로그램이 아니라 브라우저가 불러옵니다. 나중에 설정할 수도 있습니다(설정 → 매치 데이터 → 공식 매치 데이터).',
    'Zur Seite Server: dort „Spielserver anzeigen“ anhaken – Region und Ping stehen dann hier und im Overlay.':
        '서버 페이지로: 거기서 ‘게임 서버 표시’를 체크하세요 – 그러면 지역과 핑이 여기와 오버레이에 표시됩니다.',
    'Zu Einstellungen → Match-Daten → Offizielle Match-Daten: einmal das Userscript in den Browser, danach zählen Kills, Entkommen und Bloodpoints in der Statistik.':
        '설정 → 매치 데이터 → 공식 매치 데이터로: 유저스크립트를 브라우저에 한 번 넣으면 처치, 탈출, 블러드포인트가 통계에 집계됩니다.',
    'CPU DROSSELT (TEMP.)':
        'CPU 스로틀링(온도)',
    'CPU gedr.':
        'CPU 스로틀',
    'GPU gedr.':
        'GPU 스로틀',
    'CPU gedrosselt':
        'CPU 스로틀링',
    'CPU Ø W':
        'CPU 평균 W',
    'CPU-Leistung':
        'CPU 전력',
    'Kern Ø %':
        '코어 평균 %',
    'Ø CPU-Leistung':
        '평균 CPU 전력',
    'Ø stärkster CPU-Kern':
        '가장 바쁜 CPU 코어 평균',
    'Niedrigstes FPS-Tief':
        '최저 FPS low',
    'Ø FPS':
        '평균 FPS',
    'Ø FPS-Tief':
        '평균 FPS low',
    'FPS Ø':
        'FPS 평균',
    'FPS Tief':
        'FPS low',
    'Klick: sortieren · Rechtsklick: Spalten ein-/ausblenden':
        '클릭: 정렬 · 오른쪽 클릭: 열 표시/숨기기',
    'Alle Spalten zeigen':
        '모든 열 표시',
    'Exportieren …':
        '내보내기 …',
    'Zeitraum':
        '기간',
    'Von':
        '시작',
    'Bis':
        '끝',
    'TT.MM.JJJJ HH:MM – auch nur ein Datum (ganzer Tag) oder nur eine Uhrzeit (heute); leer = offen.':
        'DD.MM.YYYY HH:MM – 날짜만(하루 전체) 또는 시간만(오늘)도 됩니다. 비워 두면 제한 없음.',
    'Gestern':
        '어제',
    'Alles':
        '전체',
    'Eigener Zeitraum':
        '사용자 지정 기간',
    'Filter':
        '필터',
    'Custom Games einschliessen':
        '사용자 지정 게임 포함',
    'Farming-Runden einschliessen':
        '파밍 라운드 포함',
    'Spalten':
        '열',
    'Start':
        '시작',
    'Realm':
        '렐름',
    'Ping (ms)':
        '핑(ms)',
    'Kills':
        '처치',
    'Normal':
        '일반',
    'ja':
        '예',
    'nein':
        '아니요',
    'CSV-Datei (Excel)':
        'CSV 파일(Excel)',
    'Textliste (eine Zeile je Runde)':
        '텍스트 목록(라운드당 한 줄)',
    '{n} Runden, {m} Spalten':
        '라운드 {n}개, 열 {m}개',
    'Zeitangabe nicht lesbar: „{text}“ – Format TT.MM.JJJJ HH:MM.':
        '시간 ‘{text}’을(를) 읽을 수 없습니다 – 형식 DD.MM.YYYY HH:MM.',
    'Nichts zu kopieren – keine Runde passt, oder keine Spalte gewählt.':
        '복사할 것이 없습니다 – 일치하는 라운드가 없거나 선택한 열이 없습니다.',
    'Nichts zu speichern – keine Runde passt, oder keine Spalte gewählt.':
        '저장할 것이 없습니다 – 일치하는 라운드가 없거나 선택한 열이 없습니다.',
    'In Zwischenablage kopieren':
        '클립보드에 복사',
    'Als Datei speichern …':
        '파일로 저장 …',
    'Schliessen':
        '닫기',
    '{n} Runden in die Zwischenablage kopiert.':
        '라운드 {n}개를 클립보드에 복사했습니다.',
    'Spalte „{name}“ mit ausgeben.':
        '‘{name}’ 열을 포함합니다.',
    'Öffnet das Export-Fenster: Zeitraum (auch von–bis), Rolle, Killer, Map, Region, Spalten nach Wahl – als CSV für Excel oder als Textliste in die Zwischenablage. Die Filter der Statistik sind vorbelegt.':
        '내보내기 창을 엽니다: 기간(시작–끝도 가능), 역할, 살인마, 맵, 지역, 원하는 열 – Excel용 CSV 또는 클립보드용 텍스트 목록. 통계의 필터가 미리 설정됩니다.',
    'Kopiert die Runden in der gewählten Form (CSV oder Textliste) in die Zwischenablage – zum Einfügen in Discord, Excel oder einen Editor.':
        '선택한 형식(CSV 또는 텍스트 목록)으로 라운드를 클립보드에 복사합니다 – Discord, Excel, 편집기에 붙여 넣을 수 있습니다.',
    'Speichert die Runden als Datei: CSV (Semikolon, UTF-8 mit BOM – Excel öffnet sie direkt) oder Textliste (.txt).':
        '라운드를 파일로 저장합니다: CSV(세미콜론, BOM 포함 UTF-8 – Excel에서 바로 열림) 또는 텍스트 목록(.txt).',
    'Schliesst das Fenster.':
        '창을 닫습니다.',
    'Aus: Custom Games (eigene Lobbys, Bots) bleiben draussen.':
        '끄기: 사용자 지정 게임(직접 만든 로비, 봇)은 제외됩니다.',
    'Aus: Farming-Runden (Crossplay aus bzw. Farming-Region) bleiben draussen.':
        '끄기: 파밍 라운드(크로스플레이 꺼짐 또는 파밍 지역)는 제외됩니다.',
    'Eine Zeile je Runde, Spalten durch Semikolon getrennt, mit Kopfzeile.':
        '라운드당 한 줄, 열은 세미콜론으로 구분, 머리글 줄 포함.',
    'Eine Zeile je Runde, die gewählten Spalten mit „ · “ getrennt, ohne Kopfzeile – zum Einfügen in einen Chat.':
        '라운드당 한 줄, 선택한 열은 ‘ · ’로 구분, 머리글 없음 – 채팅에 붙여 넣기용.',
    'Verbindungen':
        '연결',
    'Ton':
        '소리',
    'Aufräumen':
        '정리',
    'Jede Runde mit OBS aufnehmen':
        'OBS로 모든 라운드 녹화',
    'Port':
        '포트',
    'Passwort':
        '비밀번호',
    'Verbindung testen':
        '연결 테스트',
    'Aufnahmeordner wählen …':
        '녹화 폴더 선택 …',
    '(kein Ordner gewählt)':
        '(선택한 폴더 없음)',
    'Platz für Aufnahmen':
        '녹화 공간',
    'Ganze Platte (Älteste weg, wenn sie voll wird)':
        '드라이브 전체(가득 차면 가장 오래된 것부터 삭제)',
    'Vorlauf aus dem OBS-Wiederholungspuffer sichern':
        'OBS 리플레이 버퍼로 사전 녹화 유지',
    'OBS nimmt auf, das Programm sagt nur wann: Start beim Map-Banner, Stopp beim erkannten Rundenende, Datei nach Datum, Map und Killer benannt. Dafür in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server einschalten und Port und Passwort unter Verbindungen → OBS-Verbindung eintragen; Verbindung nur auf diesem PC (127.0.0.1). Empfohlen: Aufnahmeformat MKV oder Hybrid-MP4 (bleibt bei Abbruch lesbar), Fenster- oder Bildschirmaufnahme statt Spielaufnahme. Der Ordner wird über sein Laufwerk gemerkt – ist die Platte nicht angeschlossen, wird nicht aufgenommen.':
        '녹화는 OBS가 하고 프로그램은 시점만 알려 줍니다: 맵 배너에서 시작, 인식된 라운드 종료에서 중지, 파일 이름은 날짜, 맵, 살인마. OBS에서 도구 → WebSocket 서버 설정에서 서버를 켜고, 연결 → OBS 연결에 포트와 비밀번호를 입력하세요. 연결은 이 PC 안에서만 이루어집니다(127.0.0.1). 권장: 녹화 형식 MKV 또는 하이브리드 MP4(충돌 후에도 읽을 수 있음), 게임 캡처보다 창 캡처나 디스플레이 캡처. 폴더는 드라이브 기준으로 기억됩니다 – 드라이브를 분리하면 아무것도 녹화되지 않습니다.',
    'Ordner für die Aufnahmen (z. B. auf der externen Platte)':
        '녹화 폴더(예: 외장 드라이브)',
    'Aufnahmeordner: {path}':
        '녹화 폴더: {path}',
    'Verbinde mit OBS …':
        'OBS에 연결하는 중 …',
    'Aufnahme: {text}':
        '녹화: {text}',
    'Aufnahme gespeichert: {file}':
        '녹화 저장됨: {file}',
    'Aufnahmen gelöscht (Platz): {n}':
        '녹화 삭제됨(공간): {n}',
    'OBS hat die Verbindung geschlossen':
        'OBS가 연결을 닫았습니다',
    'OBS antwortet nicht auf die Anfrage {kind}':
        'OBS가 {kind} 요청에 응답하지 않습니다',
    'OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})':
        'OBS에 연결할 수 없습니다 – OBS가 WebSocket 서버를 켠 채로 실행 중인가요? ({error})',
    'Keine Antwort von obs-websocket':
        'obs-websocket에서 응답 없음',
    'Kein obs-websocket auf diesem Port':
        '이 포트에 obs-websocket 없음',
    'Falsche WebSocket-Antwort':
        '잘못된 WebSocket 응답',
    'Unerwartete Begrüssung von OBS':
        'OBS의 예기치 않은 인사 메시지',
    'OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)':
        'OBS가 비밀번호를 요구합니다(OBS: 도구 → WebSocket 서버 설정)',
    'OBS hat die Anmeldung abgelehnt – Passwort falsch?':
        'OBS가 로그인을 거부했습니다 – 비밀번호가 틀렸나요?',
    'OBS {version} verbunden':
        'OBS {version} 연결됨',
    'nimmt gerade auf':
        '녹화 중',
    'bereit':
        '준비됨',
    'Wiederholungspuffer läuft':
        '리플레이 버퍼 실행 중',
    'Wiederholungspuffer aus (kein Vorlauf)':
        '리플레이 버퍼 꺼짐(사전 녹화 없음)',
    'Ordner: {folder}':
        '폴더: {folder}',
    'Ordner/Laufwerk nicht gefunden':
        '폴더/드라이브를 찾을 수 없음',
    'Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen':
        '녹화 드라이브가 연결되지 않음 – 이 라운드는 녹화되지 않습니다',
    'Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen':
        '녹화 드라이브가 거의 가득 참 – 이 라운드는 녹화되지 않습니다',
    'OBS nimmt schon auf (von Hand?) – nichts gestartet':
        'OBS가 이미 녹화 중입니다(직접 시작?) – 아무것도 시작하지 않았습니다',
    'Nimmt die Runde auf':
        '라운드 녹화 중',
    'OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet':
        'OBS가 파일 이름을 알려 주지 않았습니다 – 녹화가 연결되지 않음',
    "Aufnahme liegt in OBS' eigenem Ordner: {path}":
        '녹화가 OBS 자체 폴더에 있습니다: {path}',
    'Gespeichert: {file}':
        '저장됨: {file}',
    'Das Programm startet die OBS-Aufnahme beim Map-Banner und stoppt sie beim erkannten Rundenende (obs-websocket, nur auf diesem PC). OBS muss laufen.':
        '프로그램은 맵 배너에서 OBS 녹화를 시작하고 인식된 라운드 종료에서 중지합니다(obs-websocket, 이 PC 안에서만). OBS가 실행 중이어야 합니다.',
    'Verbindet sich einmal mit OBS und zeigt Version, Aufnahmezustand, Wiederholungspuffer und ob der Aufnahmeordner erreichbar ist.':
        'OBS에 한 번 연결해 버전, 녹화 여부, 리플레이 버퍼, 녹화 폴더에 접근할 수 있는지 보여 줍니다.',
    'Ordner, in den OBS die Runden legt – z. B. auf der externen Platte. Gemerkt wird das Laufwerk, nicht der Buchstabe: bekommt die Platte einen anderen, findet das Programm den Ordner trotzdem.':
        'OBS가 라운드를 저장하는 폴더 – 예: 외장 드라이브. 드라이브 문자가 아니라 드라이브 자체를 기억합니다: 드라이브 문자가 바뀌어도 프로그램은 폴더를 찾습니다.',
    'Läuft in OBS der Wiederholungspuffer, wird er beim Map-Banner gespeichert – der Anfang (Spawn) fehlt dann nicht, aber die Datei enthält auch Lobby und Ladebildschirm. Seit 1.5.5 standardmässig aus (Wunsch des Nutzers: nur die Runde). Die Datei liegt als „(Vorlauf)“ neben der Runde.':
        'OBS 리플레이 버퍼가 실행 중이면 맵 배너에서 저장됩니다 – 그러면 시작(스폰) 부분이 빠지지 않지만 파일에 로비와 로딩 화면도 들어갑니다. 1.5.5부터 기본값은 꺼짐입니다(사용자 요청: 라운드만). 파일은 라운드 옆에 ‘(Vorlauf)’로 저장됩니다.',
    'Wiederholungspuffer mit DBD starten und stoppen':
        'DBD와 함께 리플레이 버퍼 시작/중지',
    'Nur das DBD-Fenster aufnehmen':
        'DBD 창만 녹화',
    'Dafür die OBS-Spielaufnahme verwenden':
        '이를 위해 OBS 게임 캡처 사용',
    'Statt der Fensteraufnahme legt das Programm in OBS eine Spielaufnahme „Fog Scout – DBD-Spiel“ an und blendet die Fensteraufnahme aus. Die Spielaufnahme braucht etwas weniger Leistung; OBS hängt sich dafür mit seinem Anti-Cheat-kompatiblen Hook ins Spiel – das macht OBS, nicht dieses Programm. Ihr eigener Ton bleibt aus, der Spielton kommt weiter über die Tonquelle „Fog Scout – DBD“. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“.':
        '창 캡처 대신 프로그램이 OBS에 게임 캡처 ‘Fog Scout – DBD-Spiel’을 만들고 창 캡처를 숨깁니다. 게임 캡처는 성능을 조금 덜 씁니다. 이를 위해 OBS가 안티 치트 호환 후킹으로 게임에 연결합니다 – 이 프로그램이 아니라 OBS가 하는 일입니다. 게임 캡처 자체 소리는 꺼져 있고, 게임 소리는 계속 오디오 소스 ‘Fog Scout – DBD’로 들어옵니다. ‘DBD 창만 녹화’와 함께일 때만.',
    'Bildquelle {name} über {over} gelegt':
        '이미지 소스 {name}을(를) {over} 위에 배치함',
    'Bildquelle angelegt: {name} (Szene „{scene}“)':
        '이미지 소스 생성됨: {name}(장면 ‘{scene}’)',
    'Bildquelle in der Szene „{scene}“ ausgeblendet: {name}':
        '장면 ‘{scene}’에서 이미지 소스 숨겨짐: {name}',
    'Bildquelle zur Szene „{scene}“ hinzugefügt: {name}':
        '장면 ‘{scene}’에 이미지 소스 추가됨: {name}',
    'Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        '장면 ‘{scene}’에서 이미지 소스 다시 표시됨: {name}',
    'Bildquelle {name} zeigt jetzt {exe}':
        '이미지 소스 {name}이(가) 이제 {exe}을(를) 표시합니다',
    'DBD-Fenster in OBS nicht eingerichtet: {error}':
        'OBS에서 DBD 창이 설정되지 않았습니다: {error}',
    'OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin keine Sofort-Clips (F8) und kein Vorlauf.':
        'OBS가 리플레이 버퍼를 시작하지 못했습니다(OBS가 출력 오류를 보고함, 대부분 인코더 – 자세한 내용은 OBS 로그). 프로그램은 다음 DBD 시작 때만 다시 시도합니다. 그때까지 즉석 클립(F8)과 사전 녹화가 없습니다.',
    'Das Programm legt in OBS eine Fensteraufnahme „Fog Scout – DBD-Fenster“ an (oben in der laufenden Szene, auf die Leinwand eingepasst) und stellt sie auf Steam, Epic oder Store um. Aufgenommen wird dann nur das Spiel – ohne Discord, Benachrichtigungen und ohne das Overlay dieses Programms. OBS nimmt dabei über Windows auf; die Spielaufnahme gibt es als Häkchen darunter. Aus: die Quelle wird nur ausgeblendet, deine eigene Bildschirmaufnahme bleibt unangetastet.':
        '프로그램이 OBS에 창 캡처 ‘Fog Scout – DBD-Fenster’를 만들고(송출 중인 장면 맨 위, 캔버스에 맞춤) Steam, Epic 또는 Store로 전환합니다. 그러면 게임만 녹화됩니다 – Discord, 알림, 이 프로그램의 오버레이 없이. 여기서 OBS는 Windows를 통해 캡처합니다. 게임 캡처는 아래 상자입니다. 끄기: 소스는 숨겨질 뿐이며 사용자의 디스플레이 캡처는 그대로 둡니다.',
    'Das Programm startet den Wiederholungspuffer in OBS, sobald DBD läuft, und stoppt ihn, wenn DBD zu ist – so kostet er ausserhalb des Spiels nichts und du musst nicht daran denken.':
        'DBD가 실행되면 바로 OBS 리플레이 버퍼를 시작하고 DBD를 닫으면 중지합니다 – 게임 밖에서는 자원을 쓰지 않고 신경 쓸 필요도 없습니다.',
    'Nachlauf nach dem Rundenende':
        '라운드 종료 후 추가 녹화',
    'Overlay mit in die Aufnahme':
        '녹화에 오버레이 포함',
    'Die Fensteraufnahme enthält das Overlay dieses Programms nicht (eigene Fenster). Mit Häkchen schreibt das Programm das sichtbare Overlay – Karte, Infos, Systemwerte, Heute, Musik – als Bild in seinen Cache-Ordner und legt in OBS eine Bildquelle „Fog Scout – Overlay“ darauf an, genau dort, wo das Overlay über dem DBD-Fenster liegt. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“; bei einer Bildschirmaufnahme ist das Overlay ohnehin im Bild. Aus: die Quelle wird nur ausgeblendet.':
        '창 캡처에는 이 프로그램의 오버레이(별도 창)가 들어가지 않습니다. 체크하면 프로그램이 보이는 오버레이 – 맵, 줄, 시스템 값, 오늘, 음악 – 를 캐시 폴더에 이미지로 쓰고, OBS에서 오버레이가 DBD 창 위에 놓인 바로 그 위치에 이미지 소스 ‘Fog Scout – Overlay’를 만듭니다. ‘DBD 창만 녹화’와 함께일 때만. 디스플레이 캡처에는 오버레이가 어차피 보입니다. 끄기: 소스는 숨겨질 뿐입니다.',
    'Overlay in OBS nicht eingerichtet: {error}':
        'OBS에서 오버레이가 설정되지 않았습니다: {error}',
    '{n} s':
        '{n}초',
    'keiner':
        '없음',
    'Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen.':
        '녹화 드라이브가 연결되지 않음 – 라운드가 녹화되지 않습니다.',
    'OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})':
        'OBS가 실행 중이 아님 – 라운드가 녹화되지 않습니다. ({error})',
    'OBS bereit – Runden werden aufgenommen':
        'OBS 준비됨 – 라운드가 녹화됩니다',
    'Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).':
        '녹화가 손상된 것 같습니다({why}): {file} – OBS 설정(인코더, 드라이브)을 확인하세요.',
    'Aufnahme':
        '녹화',
    'Vorlauf und Runde zu einer Datei zusammenfügen':
        '사전 녹화와 라운드를 하나의 파일로 합치기',
    'Nach der Runde hängt ffmpeg den Vorlauf vorne an die Aufnahme – ohne Neukodierung, in Sekunden. Seit 1.5.5 standardmässig aus: Am PC des Nutzers lief der Rundenteil der zusammengefügten Datei zu schnell. Klappt es nicht, bleiben beide Dateien liegen.':
        '라운드 후 ffmpeg가 사전 녹화를 녹화 앞에 붙입니다 – 재인코딩 없이 몇 초면 끝납니다. 1.5.5부터 기본값은 꺼짐: 사용자의 PC에서 합친 파일의 라운드 부분이 너무 빠르게 재생되었습니다. 실패하면 두 파일이 모두 남습니다.',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start; bis dahin bleibt der Vorlauf eine eigene Datei.':
        'ffmpeg가 없습니다(imageio-ffmpeg 패키지) – start.bat이 다음 시작 때 설치합니다. 그때까지 사전 녹화는 별도 파일로 남습니다.',
    'Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben':
        '저장됨: {file} – 사전 녹화는 합쳐지지 않고 옆에 별도 파일로 있습니다',
    'Clip-Marke setzen':
        '클립 표시 설정',
    'Clip-Marke {n} bei {pos} gesetzt.':
        '클립 표시 {n}을(를) {pos}에 설정했습니다.',
    'Keine Aufnahme läuft – keine Clip-Marke gesetzt.':
        '진행 중인 녹화가 없습니다 – 클립 표시를 설정하지 않았습니다.',
    'Aufnahmen':
        '녹화',
    'Aufnahmen einrichten …':
        '녹화 설정 …',
    'Öffnet die Einstellungen für die Aufnahmen mit OBS (Ordner, Verbindung).':
        'OBS 녹화 설정(폴더, 연결)을 엽니다.',
    'Platte nicht angeschlossen':
        '드라이브가 연결되지 않음',
    'kein Ordner gewählt':
        '선택한 폴더 없음',
    'Platz wird gemessen …':
        '공간을 측정하는 중 …',
    '{n} mit Marke':
        '표시 있음 {n}개',
    'älteste {date}':
        '가장 오래됨 {date}',
    '{size} frei':
        '{size} 남음',
    '1 Aufnahme':
        '녹화 1개',
    '{n} Aufnahmen':
        '녹화 {n}개',
    'Abspielen':
        '재생',
    'Alle Aufnahmen':
        '모든 녹화',
    'Aufnahme fehlt: {file}':
        '녹화 없음: {file}',
    'Aufnahme gelöscht: {file}':
        '녹화 삭제됨: {file}',
    'Aufnahme löschen':
        '녹화 삭제',
    'Aufnahme nicht gelöscht ({error}): {file}':
        '녹화가 삭제되지 않았습니다({error}): {file}',
    'Aufnahme wird behalten: {file}':
        '녹화를 보관합니다: {file}',
    'Aufnahme wird nicht mehr behalten: {file}':
        '녹화를 더 이상 보관하지 않습니다: {file}',
    'Aufnahme-Laufwerk nicht angeschlossen.':
        '녹화 드라이브가 연결되지 않았습니다.',
    'Aufnahmeordner öffnen':
        '녹화 폴더 열기',
    'Behalten':
        '보관',
    'Beschädigt':
        '손상됨',
    'Datei':
        '파일',
    'Einschalten unter Einstellungen → Aufnahmen.':
        '설정 → 녹화에서 켜세요.',
    'Im Explorer zeigen':
        '탐색기에서 보기',
    'Keine Marken – F8 während der Runde setzt eine.':
        '표시 없음 – 라운드 중 F8을 누르면 설정됩니다.',
    'Marken: {list}':
        '표시: {list}',
    'Mit Marke':
        '표시 있음',
    'Nicht mehr behalten':
        '보관 해제',
    'Noch kein Aufnahmeordner gewählt.':
        '아직 선택한 녹화 폴더가 없습니다.',
    'fehlt':
        '없음',
    '{file} von der Platte löschen?':
        '드라이브에서 {file}을(를) 삭제할까요?',
    'Spielt die markierte Aufnahme im Standard-Videoplayer ab.':
        '선택한 녹화를 기본 동영상 플레이어로 재생합니다.',
    'Öffnet den Explorer mit der markierten Datei.':
        '선택한 파일이 선택된 상태로 탐색기를 엽니다.',
    'Eine behaltene Aufnahme wird nie fürs Aufräumen gelöscht, wenn die Platte Platz braucht. Nochmal drücken hebt es auf.':
        '보관한 녹화는 드라이브 공간이 필요할 때 정리 기능이 절대 삭제하지 않습니다. 다시 누르면 되돌립니다.',
    'Löscht die markierte Aufnahme (und ihren Vorlauf) von der Platte – nach Rückfrage.':
        '선택한 녹화(와 사전 녹화)를 확인 후 드라이브에서 삭제합니다.',
    'Öffnet den Aufnahmeordner im Explorer.':
        '탐색기에서 녹화 폴더를 엽니다.',
    'Farming-Runden im Unterordner „Farming“ ablegen':
        '파밍 라운드를 ‘Farming’ 하위 폴더에 저장',
    'Runden, die das Programm als Farming erkennt (Crossplay aus oder die Farming-Region), landen im Unterordner „Farming“ des Aufnahmeordners statt zwischen den normalen Runden. Clips gehen immer in den Ordner „Clips“.':
        '프로그램이 파밍으로 인식한 라운드(크로스플레이 꺼짐 또는 파밍 지역)는 일반 라운드와 섞이지 않고 녹화 폴더의 ‘Farming’ 하위 폴더에 저장됩니다. 클립은 항상 ‘Clips’ 폴더에 저장됩니다.',
    'Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in debug/lobby).':
        '크로스플레이 표시를 읽을 수 없음 – 이 라운드는 파밍으로 집계되지 않습니다(debug/lobby에 잘라낸 이미지).',
    'Rolle für {n} Runden auf {role} geändert.':
        '라운드 {n}개의 역할이 {role}(으)로 바뀌었습니다.',
    '{n} Runden aus der Statistik löschen?':
        '라운드 {n}개를 통계에서 삭제할까요?',
    '{n} Runden gelöscht.':
        '라운드 {n}개가 삭제되었습니다.',
    '{n} Runden zählen jetzt als Farming-Runden.':
        '라운드 {n}개가 이제 파밍 라운드로 집계됩니다.',
    '{n} Runden zählen wieder als normale Runden.':
        '라운드 {n}개가 다시 일반 라운드로 집계됩니다.',
    'Clip bearbeiten …':
        '클립 편집 …',
    'Öffnet den Clip-Editor für die markierte Aufnahme: Vorschau, Zeitleiste mit Marken, Start/Ende setzen, Ausschnitt als MP4 in den Ordner „Clips“ speichern.':
        '선택한 녹화의 클립 편집기를 엽니다: 미리 보기, 표시가 있는 타임라인, 시작/끝 설정, 편집 결과를 MP4로 ‘Clips’ 폴더에 저장.',
    'Clip bearbeiten – {name}':
        '클립 편집 – {name}',
    'Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)':
        '빠르게(키프레임 기준, 시작이 몇 초 일찍일 수 있음)',
    'Genau (Bild neu kodiert, dauert etwas)':
        '정확하게(화면 재인코딩, 시간이 조금 걸림)',
    '5 Sekunden vor (Shift+→)':
        '5초 앞으로(Shift+→)',
    '5 Sekunden zurück (Shift+←)':
        '5초 뒤로(Shift+←)',
    '▶ Abspielen':
        '▶ 재생',
    '⏸ Pause':
        '⏸ 일시 정지',
    'Abspielen / Pause (Leertaste)':
        '재생 / 일시 정지(스페이스 바)',
    'Start setzen':
        '시작 설정',
    'Ende setzen':
        '끝 설정',
    'Der Clip beginnt am Abspielkopf (Taste I).':
        '클립이 재생 헤드에서 시작합니다(I 키).',
    'Der Clip endet am Abspielkopf (Taste O).':
        '클립이 재생 헤드에서 끝납니다(O 키).',
    'Zur Marke ▸':
        '표시로 ▸',
    'Marken (F8)':
        '표시(F8)',
    'Clip um Marke':
        '표시 주변 클립',
    'Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der nächsten am Abspielkopf) und endet {after} s danach.':
        '클립이 선택한 표시(선택하지 않으면 재생 헤드에서 가장 가까운 표시) {before}초 전에 시작해 {after}초 후에 끝납니다.',
    'Springt zur nächsten F8-Marke (Taste M).':
        '다음 F8 표시로 이동합니다(M 키).',
    'Clip: {start} – {end} ({length} s)':
        '클립: {start} – {end}({length}초)',
    'Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows).':
        '미리 보기와 함께 녹화의 소리를 재생합니다(Windows).',
    'Ton im Clip':
        '클립의 소리',
    'Abspielkopf hierher':
        '재생 헤드를 여기로',
    'Als Custom Game':
        '사용자 지정 게임으로',
    'Als Killer-Runde':
        '살인마 라운드로',
    'Als Survivor-Runde':
        '생존자 라운드로',
    'Ausblenden':
        '숨기기',
    'Bild':
        '이미지',
    'Clip beginnt hier':
        '여기서 클립 시작',
    'Clip endet hier':
        '여기서 클립 끝',
    'Dunkle Fläche dahinter':
        '뒤에 어두운 영역',
    'Grösse zurücksetzen':
        '크기 초기화',
    'Standbild gespeichert: {file}':
        '정지 이미지 저장됨: {file}',
    'Standbild hier speichern':
        '여기서 정지 이미지 저장',
    'Standbild nicht gespeichert.':
        '정지 이미지가 저장되지 않았습니다.',
    '{n} Runden löschen':
        '라운드 {n}개 삭제',
    'Grosser Editor …':
        '큰 편집기 …',
    'Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle und allen Tasten.':
        '클립을 별도 창에서 엽니다 – 가리기, 소리 소스별 음량, 모든 단축키 포함.',
    'Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton.':
        'Discord 음성 채팅 – OBS 트랙 3. 끄기 = 클립에 Discord 소리 없음.',
    'Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird).':
        '마이크 – OBS 트랙 4(OBS가 녹음할 때만).',
    'Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen).':
        '클립에서 이 소스의 음량(100% = 녹음된 그대로).',
    'Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen).':
        '오디오 트랙이 하나뿐입니다 – 믹싱하려면 OBS가 트랙 1–4로 녹화해야 합니다(설정 → 녹화).',
    'ohne Ton':
        '소리 없음',
    'Ton neu gemischt':
        '소리 다시 믹싱됨',
    'Clip speichern':
        '클립 저장',
    'Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen.':
        '편집 결과를 MP4로 녹화 옆 ‘Clips’ 폴더에 씁니다.',
    'Clips-Ordner öffnen':
        '클립 폴더 열기',
    'Öffnet den Ordner „Clips“ im Explorer.':
        '탐색기에서 ‘Clips’ 폴더를 엽니다.',
    'Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau.':
        '파일을 읽을 수 없거나 ffmpeg가 없습니다 – 미리 보기 없음.',
    'Clips-Ordner nicht anlegbar: {error}':
        '클립 폴더를 만들 수 없습니다: {error}',
    'Schreibe {file} …':
        '{file} 쓰는 중 …',
    'Clip gespeichert: {file}':
        '클립 저장됨: {file}',
    'Clip nicht gespeichert: {why}':
        '클립이 저장되지 않았습니다: {why}',
    '(Sofort-Clip)':
        '(즉석 클립)',
    'Aufnahme schon am Ladebildschirm starten':
        '로딩 화면에서 녹화 시작',
    'Aufnahme-Laufwerk nicht angeschlossen':
        '녹화 드라이브가 연결되지 않음',
    'Clip':
        '클립',
    'DBD':
        'DBD',
    'Discord':
        'Discord',
    'F8 speichert die letzten Sekunden als Sofort-Clip':
        'F8로 마지막 몇 초를 즉석 클립으로 저장',
    'Kein Sofort-Clip: {why}':
        '즉석 클립 없음: {why}',
    'Ladebildschirm vorbei – das Match beginnt.':
        '로딩 화면 끝 – 매치가 시작됩니다.',
    'Mikrofon':
        '마이크',
    'Spiel':
        '게임',
    'Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner':
        '녹화 중 – 로딩 화면이 끝난 후부터, 맵 배너를 기다리는 중',
    'Nimmt die Runde auf (seit dem Ladebildschirm)':
        '라운드 녹화 중(로딩 화면부터)',
    'OBS hat den Puffer nicht gespeichert':
        'OBS가 버퍼를 저장하지 않았습니다',
    'Sofort-Clip gespeichert ({n} s): {file}':
        '즉석 클립 저장됨({n}초): {file}',
    'Ton in OBS einstellen, sobald DBD startet:':
        'DBD가 시작되면 바로 OBS의 소리 설정:',
    'Ton in OBS nicht eingestellt: {error}':
        'OBS의 소리가 설정되지 않았습니다: {error}',
    'OBS bereit – Runden werden aufgenommen. {problem}':
        'OBS 준비됨 – 라운드가 녹화됩니다. {problem}',
    'Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)':
        '클립 편집기에서 소리를 믹싱하려면 OBS에서: 설정 → 출력 → 출력 방식 ‘고급’ → 녹화 탭 → 오디오 트랙 1–5 체크(1 전체, 2 게임, 3 Discord, 4 마이크, 5 배경)',
    'Jede Tonquelle auf eine eigene OBS-Tonspur':
        '각 소리 소스를 별도 OBS 트랙에',
    'Dafür in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken. Das Programm prüft das beim DBD-Start und meldet es im Kasten „Aufnahmen mit OBS“; es ändert nichts am OBS-Profil.':
        '이를 위해 OBS에서: 설정 → 출력 → 출력 방식 ‘고급’ → 녹화 탭 → 오디오 트랙 1–5 체크. 프로그램은 DBD가 시작될 때 이를 확인해 ‘OBS로 녹화’ 카드에 알려 주며, OBS 프로필은 바꾸지 않습니다.',
    'Sofort-Clip (F8) mit Ton von:':
        '즉석 클립(F8)에 포함할 소리:',
    'Wie bei Medal: Das Programm weist in OBS jede Tonquelle der Spur 1 (alles – spielt in jedem Player) und ihrer eigenen Spur zu: nur DBD 2, Discord 3, Mikrofon 4, alle anderen Tonquellen in OBS (z. B. Spotify, Browser) 5 = Hintergrund. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt deshalb nur auf Spur 1. Im Clip-Editor schaltest du jede Quelle an oder aus und regelst ihre Lautstärke; beim Speichern mischt ffmpeg sie zusammen. OBS schreibt die Spuren nur im Ausgabemodus „Erweitert“ mit Audiospur 1 bis 5 angehakt (MKV oder MP4, nicht FLV); das Programm prüft das beim DBD-Start und meldet es, ändert aber nichts am OBS-Profil. Aus = Spuren bleiben, wie sie in OBS stehen.':
        'Medal처럼: 프로그램이 OBS의 모든 소리 소스를 트랙 1(전체 – 어떤 플레이어에서도 재생)과 각자의 트랙에 할당합니다: DBD만 2, Discord 3, 마이크 4, OBS의 다른 모든 소리 소스(예: Spotify, 브라우저) 5 = 배경. Windows 데스크톱 소리에는 DBD와 Discord도 들어 있으므로 트랙 1에만 둡니다. 클립 편집기에서 각 소스를 켜고 끄고 음량을 설정하며, 저장할 때 ffmpeg가 믹싱합니다. OBS는 출력 방식 ‘고급’에서 오디오 트랙 1–5를 체크했을 때만 트랙을 씁니다(MKV 또는 MP4, FLV 제외). 프로그램은 DBD가 시작될 때 이를 확인해 알려 주지만 OBS 프로필은 바꾸지 않습니다. 끄기 = 트랙은 OBS에서 설정한 그대로.',
    'Nur der Ton von DBD im Sofort-Clip.':
        '즉석 클립에 DBD의 소리만.',
    'Ton von Discord (Sprachchat) in der Aufnahme bzw. im Sofort-Clip.':
        '녹화 또는 즉석 클립에 Discord(음성 채팅)의 소리.',
    'Dein Mikrofon – die Quelle „Mikrofon/AUX“ in OBS bzw. seine Spur im Sofort-Clip.':
        '마이크 – OBS의 ‘마이크/보조’ 소스, 또는 즉석 클립의 해당 트랙.',
    'Hintergrund':
        '배경',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.':
        'OBS에 자체 소리 소스가 있는 다른 프로그램(예: Spotify, 브라우저) – OBS 트랙 5. Windows 데스크톱 소리에는 DBD와 Discord도 들어 있어 트랙 1에만 있습니다.',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) im Sofort-Clip – OBS-Spur 5.':
        '즉석 클립에 OBS에 자체 소리 소스가 있는 다른 프로그램(예: Spotify, 브라우저)의 소리 – OBS 트랙 5.',
    'Tonquelle angelegt: {name}':
        '소리 소스 생성됨: {name}',
    'Farming-Aufnahmen löschen nach':
        '파밍 녹화 삭제 기간',
    'nie':
        '안 함',
    '{n} Tagen':
        '{n}일',
    'Alte Farming-Aufnahmen gelöscht (älter als {days} Tage): {n}':
        '오래된 파밍 녹화 삭제됨({days}일보다 오래됨): {n}',
    '{name} – keine Quelle':
        '{name} – 소스 없음',
    '{name} – in OBS aus':
        '{name} – OBS에서 꺼짐',
    'In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf Spur 5.':
        '이 녹화에는 OBS 배경 소스가 없었습니다. Spotify, 브라우저 등은 OBS에서 프로그램마다 애플리케이션 오디오 캡처를 추가하세요 – 프로그램이 트랙 5에 배치합니다.',
    'Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen ausgeschaltet.':
        '이 녹화를 할 때 설정 → 녹화에서 이 소리 소스가 꺼져 있었습니다.',
    'Tonquelle {name} hört jetzt auf {exe}':
        '소리 소스 {name}이(가) 이제 {exe}을(를) 듣습니다',
    'Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}':
        '게임/Discord/마이크 대신 트랙 5(배경)에: {names}',
    'Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.':
        '녹화 전체에서 트랙 {n}에 아무 소리도 들리지 않습니다.',
    'Tonquelle zur Szene „{scene}“ hinzugefügt: {name}':
        '장면 ‘{scene}’에 소리 소스 추가됨: {name}',
    'Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        '장면 ‘{scene}’에서 소리 소스 다시 표시됨: {name}',
    '{name} (Spur {n})':
        '{name}(트랙 {n})',
    'Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.':
        '이 녹화에서 무음: {names} – OBS가 아무것도 녹음하지 않았습니다. OBS에서 확인하세요: 녹화 중인 장면에 소스가 있는지, 음소거되지 않았는지, 트랙이 체크되었는지.',
    '{name} – still':
        '{name} – 무음',
    'Nur der Ton von Dead by Daylight – OBS-Spur 2.':
        'Dead by Daylight의 소리만 – OBS 트랙 2.',
    'Unbekannte Map':
        '알 수 없는 맵',
    'Wiederholungspuffer in OBS läuft nicht':
        'OBS 리플레이 버퍼가 실행 중이 아닙니다',
    'Übriger Desktop-Ton':
        '기타 데스크톱 소리',
    'Das Map-Banner kommt erst einige Sekunden nach dem Spawn. Mit diesem Häkchen startet OBS schon, wenn der Ladebildschirm nach der Lobby endet – ohne Lobby, mit Spawn. Das Banner benennt die Aufnahme danach. Kommt 3 Minuten lang kein Banner, endet die Aufnahme und heisst „Unbekannte Map“.':
        '맵 배너는 스폰 몇 초 후에 나옵니다. 이 상자를 켜면 로비 다음 로딩 화면이 끝나는 즉시 OBS가 시작합니다 – 로비 없이, 스폰 포함. 녹화 이름은 나중에 배너로 정해집니다. 3분 동안 배너가 없으면 녹화가 끝나고 ‘알 수 없는 맵’이라는 이름이 붙습니다.',
    'F8 sichert den Wiederholungspuffer von OBS und legt die letzten Sekunden als MP4 in den Ordner „Clips“ – Bild ohne Neukodierung, in Sekunden. Spur 1 ist die unten gewählte Tonmischung (spielt überall), dahinter liegen die Einzelspuren des Puffers für den Clip-Editor. Der Wiederholungspuffer muss in OBS eingerichtet sein. Die Marke in der Rundenaufnahme setzt F8 weiterhin.':
        'F8은 OBS 리플레이 버퍼를 저장하고 마지막 몇 초를 MP4로 ‘Clips’ 폴더에 넣습니다 – 화면은 재인코딩 없이, 몇 초면 끝납니다. 트랙 1은 아래에서 선택한 소리 믹스(어디서나 재생)이고, 그 뒤에 클립 편집기용 버퍼 자체 트랙이 있습니다. OBS에서 리플레이 버퍼를 설정해야 합니다. F8은 라운드 녹화에 표시도 설정합니다.',
    'Das Programm legt in der aktuellen OBS-Szene je eine Anwendungs-Audioaufnahme für DBD und Discord an (einmalig) und schaltet die Tonquellen wie gewählt stumm oder laut – beim Start von DBD und bei jeder Änderung hier, auch mitten in der Runde. Aufnehmen tut OBS, das Programm fasst DBD nicht an. Braucht OBS 28 oder neuer.':
        '프로그램이 현재 OBS 장면에 DBD와 Discord용 애플리케이션 오디오 캡처를 하나씩 만들고(한 번), 선택에 따라 소리 소스를 음소거하거나 해제합니다 – DBD가 시작될 때와 여기서 바꿀 때마다, 라운드 중에도. 캡처는 OBS가 하며 프로그램은 DBD를 건드리지 않습니다. OBS 28 이상이 필요합니다.',
    'Ton des Spiels in der Aufnahme.':
        '녹화에 게임 소리.',
    'Alles andere, was am PC zu hören ist (Musik, Browser, Systemtöne) – die Quelle „Desktop-Audio“ in OBS.':
        'PC에서 들리는 나머지 모든 소리(음악, 브라우저, 시스템 소리) – OBS의 ‘데스크톱 오디오’ 소스.',
    'Als Farming markieren':
        '파밍으로 표시',
    'Grund':
        '이유',
    'Ist Farming':
        '파밍임',
    'Kein Farming':
        '파밍 아님',
    'Alle als Farming':
        '모두 파밍으로',
    'Alle ignorieren':
        '모두 무시',
    'Custom Game, laut Stats-Seite öffentlich':
        '사용자 지정 게임, 통계 페이지에서는 공개',
    'kurze Serie, gleicher Gegner':
        '짧은 연속 라운드, 같은 상대',
    '{n} Runden bleiben normale Runden (kein Farming).':
        '라운드 {n}개는 일반 라운드로 남습니다(파밍 아님).',
    'Markiert alle Runden der Liste als Farming-Runden (mit Rückfrage) – wie „Ist Farming“ für jede.':
        '목록의 모든 라운드를 파밍 라운드로 표시합니다(먼저 묻습니다) – 각각 ‘파밍임’을 누르는 것과 같습니다.',
    'Keine der Runden der Liste mehr vorschlagen – sie bleiben, wie sie sind.':
        '목록의 어떤 라운드도 다시 제안하지 않습니다 – 그대로 유지됩니다.',
    'Die markierten Runden der Liste sind Farming-Runden (und kein Custom Game mehr); ihre Aufnahmen wandern in den Ordner „Farming“. Zurück: „Farming an/aus“ unter „Letzte Runden“.':
        '목록에서 선택한 라운드는 파밍 라운드입니다(더 이상 사용자 지정 게임 아님). 녹화는 ‘Farming’ 폴더로 옮겨집니다. 되돌리기: ‘최근 라운드’의 ‘파밍 켜기/끄기’.',
    'Die markierten Runden der Liste sind normale Runden – sie bleiben, wie sie sind, und werden nie wieder vorgeschlagen.':
        '목록에서 선택한 라운드는 일반 라운드입니다 – 그대로 유지되며 다시 제안되지 않습니다.',
    'Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB.':
        'Discord: Nitro 없이 10MB, Nitro Basic 50MB, Nitro 500MB.',
    'Format':
        '형식',
    'Für Discord (passt unter die Zielgrösse)':
        'Discord용(목표 크기 이하로 맞춤)',
    'Gespeichert: {file} ({mb} MB)':
        '저장됨: {file}({mb}MB)',
    'Ignorieren':
        '무시',
    'Runden nicht geändert: {error}':
        '라운드가 바뀌지 않았습니다: {error}',
    'Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück.':
        '클립 부분만 재생한 후 시작 지점으로 돌아갑니다.',
    'Zeigt den zuletzt gespeicherten Clip im Explorer.':
        '마지막으로 저장한 클립을 탐색기에서 보여 줍니다.',
    '{n} Runden als Farming markiert.':
        '라운드 {n}개를 파밍으로 표시했습니다.',
    '{n} Runden als Farming-Runden markieren?':
        '라운드 {n}개를 파밍 라운드로 표시할까요?',
    '{n} Runden sehen nach Farming aus: {reasons}. Zuletzt: {map}, {when}.':
        '라운드 {n}개가 파밍처럼 보입니다: {reasons}. 최근: {map}, {when}.',
    '{n} als Custom Game gespeichert, laut Stats-Seite aber öffentliche Matches (vor 1.5.5 so erkannt)':
        '사용자 지정 게임으로 저장되었지만 통계 페이지에서는 공개 매치 {n}개(1.5.5 이전에 그렇게 읽음)',
    '{n} kurze Runden (bis 3 min) hintereinander gegen denselben Charakter':
        '같은 캐릭터를 상대로 연속된 짧은 라운드(최대 3분) {n}개',
    'Farming?':
        '파밍?',
    'Runden sehen nach Farming aus':
        '파밍처럼 보이는 라운드',
    'Farming prüfen …':
        '파밍 확인 …',
    'Öffnet die Statistik-Übersicht mit der Zeile, die sagt, warum diese Runden nach Farming aussehen – dort markieren oder ignorieren.':
        '이 라운드들이 왜 파밍처럼 보이는지 설명하는 줄과 함께 통계 개요를 엽니다 – 거기서 표시하거나 무시하세요.',
    'etwa {mb} MB':
        '약 {mb}MB',
    'wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB':
        '{h}p {fps}fps, ≈ {kbps}kbit/s, {mb}MB 이하가 됩니다',
    '≤ {n} MB':
        '≤ {n}MB',
    '▶ Clip ansehen':
        '▶ 클립 보기',
    'Markiert alle genannten Runden als Farming-Runden (und nicht mehr als Custom Game); ihre Aufnahmen wandern in den Ordner „Farming“. Einzeln zurück: „Farming an/aus“ unter „Letzte Runden“.':
        '이 라운드를 모두 파밍 라운드로 표시합니다(더 이상 사용자 지정 게임 아님). 녹화는 ‘Farming’ 폴더로 옮겨집니다. 하나씩 되돌리기: ‘최근 라운드’의 ‘파밍 켜기/끄기’.',
    'Diese Runden nicht mehr vorschlagen – sie bleiben, wie sie sind.':
        '이 라운드를 다시 제안하지 않습니다 – 그대로 유지됩니다.',
    'Alle':
        '전체',
    'BP/h':
        'BP/시',
    'BP/h mit Wartezeit':
        '대기 포함 BP/시',
    'Bloodpoints':
        '블러드포인트',
    'Bloodpoints laut Stats-Seite. BP/h = je Stunde im Match; mit Wartezeit = je Stunde aus Match und Suche zusammen. Was das Farmen allein bringt, steht im Reiter „Farming“; „Farming ausblenden“ rechnet hier ohne Farming-Runden.':
        '통계 페이지의 블러드포인트. BP/시 = 매치 시간당. 대기 포함 = 매치와 검색을 합친 시간당. 파밍만으로 얻은 것은 ‘파밍’ 탭에 있으며, ‘파밍 숨기기’를 켜면 여기서 파밍 라운드가 제외됩니다.',
    'Bloodpoints pro Stunde':
        '시간당 블러드포인트',
    'Summe':
        '합계',
    'mit Wartezeit {bp}':
        '대기 포함 {bp}',
    'Rekorde':
        '기록',
    'Serien zählen Runden mit Ergebnis laut Stats-Seite in zeitlicher Reihenfolge – „aktuell“ ist die Serie der neuesten Runden der Auswahl. Beste Woche ab {n} Runden mit Ergebnis. Eine Sitzung endet nach 45 Minuten ohne Runde.':
        '연속 기록은 통계 페이지 결과가 있는 라운드를 시간 순서로 셉니다 – ‘현재’는 선택한 범위의 최신 라운드들의 연속 기록입니다. 최고의 주는 결과가 있는 라운드 {n}개부터. 세션은 라운드 없이 45분이 지나면 끝납니다.',
    'Noch keine Runden in dieser Auswahl.':
        '이 선택에는 아직 라운드가 없습니다.',
    'aktuell {n}':
        '현재 {n}',
    'zuletzt {date}':
        '마지막 {date}',
    '4K-Serie':
        '4K 연속',
    'Ø {kills} Kills · {n} Runden als {killer}':
        'Ø {kills}처치 · {killer}(으)로 {n}라운드',
    '{share} entkommen · {n} Runden gegen {killer}':
        '{share} 탈출 · {killer} 상대로 {n}라운드',
    '4K-Serie {n}':
        '4K 연속 {n}',
    'Entkommen-Serie {n}':
        '탈출 연속 {n}',
    'Entkommen-Serie':
        '탈출 연속',
    'Beste Woche als Killer':
        '살인마 최고의 주',
    'ab {date} · {n} Runden':
        '{date}부터 · {n}라운드',
    'ab {n} Killer-Runden in einer Woche':
        '한 주에 살인마 라운드 {n}개부터',
    'Beste Woche als Survivor':
        '생존자 최고의 주',
    'ab {n} Survivor-Runden in einer Woche':
        '한 주에 생존자 라운드 {n}개부터',
    'Meiste Runden an einem Tag':
        '하루 최다 라운드',
    'Längste Sitzung':
        '최장 세션',
    'Längste Runde':
        '최장 라운드',
    'Spielstatus in Discord anzeigen (Rich Presence)':
        'Discord에 게임 상태 표시(Rich Presence)',
    'Application-ID':
        '애플리케이션 ID',
    'Discord testen':
        'Discord 테스트',
    'Developer-Portal öffnen':
        '개발자 포털 열기',
    'Killer in Discord anzeigen':
        'Discord에 살인마 표시',
    'Auch Lobby, Suche und Menü anzeigen':
        '로비, 검색, 메뉴도 표시',
    'Zeigt in deinem Discord-Status, was gerade läuft: „Nurse auf Coal Tower“ mit Rundenzeit, in der Lobby „Sucht ein Match“. Discord braucht dafür eine Application-ID: im Developer-Portal „New Application“ anlegen (als Name z. B. „Dead by Daylight“ – so steht es im Status), die Application-ID kopieren und hier eintragen. Das Programm spricht nur mit dem Discord-Client auf diesem PC (lokale Pipe), ohne ID wird nichts gesendet; Discord erfährt nur Map, Rolle, Killer und die Startzeit.':
        '지금 무엇을 하는지 Discord 상태에 표시합니다: 라운드 시간과 함께 ‘Nurse on Coal Tower’, 로비에서는 ‘매치 검색 중’. 이를 위해 Discord는 애플리케이션 ID가 필요합니다: 개발자 포털에서 ‘New Application’을 만들고(이름은 예를 들어 ‘Dead by Daylight’ – 상태에 표시되는 이름), 애플리케이션 ID를 복사해 여기에 입력하세요. 프로그램은 이 PC의 Discord 클라이언트와만 통신합니다(로컬 파이프). ID가 없으면 아무것도 보내지 않으며, Discord가 아는 것은 맵, 역할, 살인마, 시작 시각뿐입니다.',
    'Verbinde mit Discord …':
        'Discord에 연결하는 중 …',
    'Discord nicht gefunden – läuft es?':
        'Discord를 찾을 수 없습니다 – 실행 중인가요?',
    'Killer · {killer}':
        '살인마 · {killer}',
    'Im Match':
        '매치 중',
    'Sucht ein Match':
        '매치 검색 중',
    'In der Lobby':
        '로비에 있음',
    'Bereit machen':
        '준비 중',
    'Im Menü':
        '메뉴에 있음',
    'Discord: aus':
        'Discord: 꺼짐',
    'Discord: Fehler – {error}':
        'Discord: 오류 – {error}',
    'Application-ID fehlt – im Developer-Portal anlegen und hier eintragen.':
        '애플리케이션 ID 없음 – 개발자 포털에서 만들어 여기에 입력하세요.',
    'Ungültige Application-ID ({error})':
        '잘못된 애플리케이션 ID({error})',
    'Discord: verbunden':
        'Discord: 연결됨',
    'Als Killer steht dein Killer im Status („Killer · The Nurse“); aus = nur „Killer“.':
        '살인마일 때 상태에 내 살인마가 표시됩니다(‘살인마 · The Nurse’). 끄기 = ‘살인마’만.',
    'Aus = der Status erscheint nur während einer Runde; sonst auch „Sucht ein Match“, „In der Lobby“ und „Im Menü“, solange DBD läuft.':
        '끄기 = 상태가 라운드 중에만 표시됩니다. 켜기 = DBD 실행 중 ‘매치 검색 중’, ‘로비에 있음’, ‘메뉴에 있음’도 표시됩니다.',
    'Dein Discord-Status zeigt Map, Rolle, Killer und die Rundenzeit (in der Lobby: Suche/Lobby). Braucht eine Application-ID aus dem Discord-Developer-Portal; das Programm spricht nur mit dem Discord-Client auf diesem PC.':
        'Discord 상태에 맵, 역할, 살인마, 라운드 시간(로비에서는 검색/로비)을 표시합니다. Discord 개발자 포털의 애플리케이션 ID가 필요합니다. 프로그램은 이 PC의 Discord 클라이언트와만 통신합니다.',
    'Verbindet sich einmal mit dem laufenden Discord und zeigt, ob die Application-ID angenommen wird.':
        '실행 중인 Discord에 한 번 연결해 애플리케이션 ID가 받아들여지는지 보여 줍니다.',
    'Öffnet discord.com/developers im Browser: „New Application“ anlegen (Name z. B. „Dead by Daylight“), die Application-ID kopieren und links eintragen.':
        '브라우저에서 discord.com/developers를 엽니다: ‘New Application’을 만들고(이름 예: ‘Dead by Daylight’), 애플리케이션 ID를 복사해 왼쪽에 입력하세요.',
    'Ø pro Runde':
        '라운드당 평균',
    'BP/h im Match':
        '매치 중 BP/시',
    'Spielzeit laut Stats-Seite':
        '통계 페이지 기준 플레이 시간',
    'Match und Suche zusammen':
        '매치와 검색 합산',
    'Beste Runde':
        '최고 라운드',
    'Ø BP als Killer':
        '살인마 평균 BP',
    'Ø BP als Survivor':
        '생존자 평균 BP',
    '{when}: Ø {bp} BP · {n} Runden · Summe {sum}':
        '{when}: 평균 {bp} BP · {n}라운드 · 합계 {sum}',
    'Ø Bloodpoints pro Runde {per}':
        '라운드당 평균 블러드포인트 {per}',
    'Keine Runden mit Bloodpoints in dieser Auswahl.':
        '이 선택에는 블러드포인트가 있는 라운드가 없습니다.',
    'Verpixelt':
        '픽셀화',
    'Verwischt':
        '흐리게',
    'Schwarz':
        '검은색',
    'Zensieren':
        '가리기',
    'Beim Speichern anwenden':
        '저장할 때 적용',
    'Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das Bild neu kodiert, auch im Format „Schnell“).':
        '저장된 클립에서 상자 부분이 가려집니다(이를 위해 ‘빠르게’ 형식에서도 화면이 재인코딩됨).',
    'Kasten zeichnen':
        '상자 그리기',
    'Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug.':
        '화면에서 영역을 끌어 지정하세요. 상자는 옮길 수 있고 오른쪽 아래 모서리로 크기를 바꿀 수 있습니다. 다시 누르면 도구가 끝납니다.',
    'Namen links unten':
        '왼쪽 아래 이름',
    'Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        'DBD가 생존자 이름을 표시하는 곳(게임 화면 왼쪽 아래)에 상자를 놓습니다 – 필요하면 옮기세요.',
    'Kasten entfernen':
        '상자 제거',
    'Entfernt den markierten Kasten (Taste Entf).':
        '선택한 상자를 제거합니다(Del 키).',
    'Alle entfernen':
        '모두 제거',
    'Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ lässt dich einen aufziehen.':
        '아직 상자가 없습니다. ‘왼쪽 아래 이름’은 생존자 이름 위에 상자를 놓고, ‘상자 그리기’로 직접 끌어 만들 수 있습니다.',
    '{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.':
        '상자 {n}개 – 끌기 = 이동, 오른쪽 아래 모서리 = 크기, 클릭 = 선택.',
    '{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.':
        '상자 {n}개 기억됨 – 다음 클립에도 적용됩니다.',
    'mit Zensur neu kodiert (wie „Genau“)':
        '가리기를 위해 재인코딩됨(‘정확하게’처럼)',
    'Retusche (aus der Umgebung übermalt)':
        '리터치(주변으로 덧칠)',
    'Spotify':
        'Spotify',
    '„Als nächstes“ aus Spotify in der Musikkarte zeigen':
        '음악 카드에 Spotify의 ‘다음 곡’ 표시',
    'Client-ID':
        '클라이언트 ID',
    'Developer-Dashboard öffnen':
        '개발자 대시보드 열기',
    'Mit Spotify verbinden':
        'Spotify에 연결',
    'Spotify-Verbindung trennen':
        'Spotify 연결 해제',
    'Spotify: öffne die Anmeldung im Browser …':
        'Spotify: 브라우저에서 로그인을 여는 중 …',
    'YouTube':
        'YouTube',
    'Privat':
        '비공개',
    'Nicht gelistet':
        '일부 공개',
    'Öffentlich':
        '공개',
    'Client-Secret':
        '클라이언트 보안 비밀',
    'Sichtbarkeit':
        '공개 범위',
    'Clips automatisch auf YouTube hochladen':
        '클립을 YouTube에 자동 업로드',
    'Google Cloud Console öffnen':
        'Google Cloud 콘솔 열기',
    'Client-Datei laden …':
        '클라이언트 파일 불러오기 …',
    'Client-Datei laden':
        '클라이언트 파일 불러오기',
    'Client-Datei von Google laden':
        'Google 클라이언트 파일 불러오기',
    'Das ist keine Client-Datei von Google ({error}).':
        'Google 클라이언트 파일이 아닙니다({error}).',
    'YouTube: Client-ID und Client-Secret aus {file} übernommen – jetzt „Mit YouTube verbinden“ klicken.':
        'YouTube: {file}에서 클라이언트 ID와 클라이언트 보안 비밀을 가져왔습니다 – 이제 ‘YouTube에 연결’을 클릭하세요.',
    'YouTube: Client-Daten aus {file} übernommen.':
        'YouTube: {file}에서 클라이언트 데이터를 가져왔습니다.',
    'Datei zu gross':
        '파일이 너무 큼',
    'nicht lesbar: {error}':
        '읽을 수 없음: {error}',
    'kein JSON: {error}':
        'JSON이 아님: {error}',
    'kein JSON-Objekt':
        'JSON 객체가 아님',
    'OAuth-Client vom Typ „Webanwendung“ – in der Cloud Console einen vom Typ „Desktop-App“ anlegen':
        '‘웹 애플리케이션’ 유형의 OAuth 클라이언트 – Cloud 콘솔에서 ‘데스크톱 앱’ 유형으로 만드세요',
    'kein Abschnitt „installed“':
        '‘installed’ 섹션 없음',
    'Client-ID fehlt oder endet nicht auf .apps.googleusercontent.com':
        '클라이언트 ID가 없거나 .apps.googleusercontent.com으로 끝나지 않음',
    'Client-Secret fehlt':
        '클라이언트 보안 비밀 없음',
    'Mit YouTube verbinden':
        'YouTube에 연결',
    'YouTube-Verbindung trennen':
        'YouTube 연결 해제',
    'Auf YouTube hochladen':
        'YouTube에 업로드',
    'YouTube-Link kopieren':
        'YouTube 링크 복사',
    'Auf YouTube öffnen':
        'YouTube에서 열기',
    'YouTube: Client-ID (…apps.googleusercontent.com) und Client-Secret eintragen.':
        'YouTube: 클라이언트 ID(…apps.googleusercontent.com)와 클라이언트 보안 비밀을 입력하세요.',
    'YouTube: öffne die Anmeldung im Browser …':
        'YouTube: 브라우저에서 로그인을 여는 중 …',
    'Hochgeladen: {file}':
        '업로드됨: {file}',
    'YouTube: nicht hochgeladen – {file}: {why}':
        'YouTube: 업로드되지 않음 – {file}: {why}',
    'YouTube: in die Warteschlange – {file}':
        'YouTube: 대기열에 추가됨 – {file}',
    'YouTube-Link kopiert: {url}':
        'YouTube 링크 복사됨: {url}',
    'Clip: {what}':
        '클립: {what}',
    'Dauer {d}':
        '길이 {d}',
    'Aufgenommen mit Fog Scout':
        'Fog Scout로 녹화함',
    'keine Upload-Sitzung erhalten':
        '업로드 세션을 받지 못함',
    'Antwort ohne Video-ID':
        '동영상 ID가 없는 응답',
    'nicht angemeldet':
        '로그인되지 않음',
    'Datei nicht gefunden':
        '파일을 찾을 수 없음',
    'Aufnahmeordner nicht da':
        '녹화 폴더 없음',
    'YouTube: aus':
        'YouTube: 꺼짐',
    'YouTube: nicht verbunden – „Mit YouTube verbinden“ klicken.':
        'YouTube: 연결되지 않음 – ‘YouTube에 연결’을 클릭하세요.',
    'Mit YouTube verbunden – du kannst dieses Fenster schliessen.':
        'YouTube에 연결되었습니다 – 이 창을 닫아도 됩니다.',
    'Google hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Google이 로그인을 거부했습니다 – 이 창을 닫아도 됩니다.',
    'YouTube: Anmeldung nicht möglich – {error}':
        'YouTube: 로그인할 수 없음 – {error}',
    'YouTube: Browser nicht geöffnet – {error}':
        'YouTube: 브라우저가 열리지 않음 – {error}',
    'YouTube: Anmeldung abgelehnt ({error})':
        'YouTube: 로그인 거부됨({error})',
    'YouTube: Google gab kein dauerhaftes Token – in der Cloud Console den OAuth-Client als „Desktop“ anlegen und den Zustimmungsbildschirm veröffentlichen.':
        'YouTube: Google이 영구 토큰을 주지 않았습니다 – Cloud 콘솔에서 OAuth 클라이언트를 ‘데스크톱 앱’으로 만들고 동의 화면을 게시하세요.',
    'YouTube: verbunden':
        'YouTube: 연결됨',
    'YouTube: Anmeldung abgelaufen – noch einmal „Mit YouTube verbinden“ klicken.':
        'YouTube: 로그인 만료 – ‘YouTube에 연결’을 한 번 더 클릭하세요.',
    'YouTube: {n} in der Warteschlange – wartet, bis Lobby und Runde vorbei sind':
        'YouTube: {n}개 대기 중 – 로비와 라운드가 끝날 때까지 대기',
    'YouTube: {n} in der Warteschlange – Tageskontingent aufgebraucht, weiter ab {when}':
        'YouTube: {n}개 대기 중 – 일일 할당량 소진, {when}에 계속',
    'YouTube: lädt {file} hoch ({pct} %)':
        'YouTube: {file} 업로드 중({pct}%)',
    'YouTube: hochgeladen – {file}':
        'YouTube: 업로드됨 – {file}',
    'YouTube: {error} – neuer Versuch in {s} s':
        'YouTube: {error} – {s}초 후 다시 시도',
    'YouTube: {n} in der Warteschlange – {why}':
        'YouTube: {n}개 대기 중 – {why}',
    'Uploads in Playlists einsortieren':
        '업로드를 재생목록으로 분류',
    'Playlists laden':
        '재생목록 불러오기',
    'Clips in':
        '클립 저장 위치',
    'Runden in':
        '라운드 저장 위치',
    'YouTube: lade Playlists …':
        'YouTube: 재생목록을 불러오는 중 …',
    'YouTube: zuerst „Uploads in Playlists einsortieren“ anhaken.':
        'YouTube: 먼저 ‘업로드를 재생목록으로 분류’를 체크하세요.',
    'YouTube: {n} Playlists geladen – im Kasten auswählen':
        'YouTube: 재생목록 {n}개를 불러왔습니다 – 상자에서 고르세요',
    'YouTube: keine Playlists auf dem Kanal – zuerst auf YouTube eine anlegen':
        'YouTube: 채널에 재생목록이 없습니다 – 먼저 YouTube에서 만드세요',
    'YouTube: Playlists nicht geladen – {why}':
        'YouTube: 재생목록을 불러오지 못함 – {why}',
    'YouTube: {file} in Playlist „{name}“ einsortiert':
        'YouTube: {file}을(를) 재생목록 ‘{name}’에 추가함',
    'YouTube: {file} hochgeladen, aber nicht in die Playlist – {why}':
        'YouTube: {file}은(는) 업로드되었지만 재생목록에는 추가되지 않음 – {why}',
    'Berechtigung fehlt – noch einmal „Mit YouTube verbinden“ klicken':
        '권한 없음 – ‘YouTube에 연결’을 한 번 더 클릭하세요',
    'YouTube: verbunden – für Playlists einmal neu „Mit YouTube verbinden“ klicken.':
        'YouTube: 연결됨 – 재생목록을 쓰려면 ‘YouTube에 연결’을 한 번 더 클릭하세요.',
    'Nach dem Upload kommt jedes Video in die gewählte Playlist – für Clips und Runden getrennt wählbar, beide dürfen dieselbe sein. Braucht bei Google die Berechtigung „YouTube-Konto verwalten“ statt nur „Videos hochladen“: nach dem Anhaken einmal neu „Mit YouTube verbinden“. Das Programm nutzt davon nur Playlists auflisten und Video einsortieren (50 Einheiten je Video; es bleiben sechs Uploads am Tag).':
        '업로드 후 모든 동영상이 선택한 재생목록에 들어갑니다 – 클립과 라운드를 따로, 둘이 같아도 됩니다. ‘동영상 업로드’ 대신 Google의 ‘YouTube 계정 관리’ 권한이 필요합니다: 체크한 후 ‘YouTube에 연결’을 한 번 더 클릭하세요. 프로그램은 이 권한을 재생목록 나열과 동영상 추가에만 씁니다(동영상당 50단위, 하루 업로드 6개는 그대로 가능).',
    'Holt die Liste deiner Playlists von YouTube (1 Einheit) in die beiden Auswahlfelder. Neue Playlists legst du auf YouTube an und lädst die Liste danach neu.':
        'YouTube에서 재생목록 목록을 가져와(1단위) 두 선택 상자에 넣습니다. 새 재생목록은 YouTube에서 만든 후 목록을 다시 불러오세요.',
    'YouTube: Fehler – {error}':
        'YouTube: 오류 – {error}',
    'Jeder neue Clip (F8 und aus dem Editor) kommt in die Warteschlange und geht auf deinen Kanal, sobald du weder in einer Lobby noch in einer Runde bist – mit der Sichtbarkeit rechts, Standard privat. Runden lädst du nur auf Wunsch hoch (Rechtsklick unter Aufnahmen). Google erlaubt etwa sechs Uploads am Tag, der Rest wartet bis zum nächsten Tag. Die Datei bleibt auf der Platte.':
        '새 클립(F8과 편집기에서)은 모두 대기열에 들어가며, 로비나 라운드 중이 아닐 때 바로 채널에 올라갑니다 – 공개 범위는 오른쪽 설정, 기본값은 비공개. 라운드는 요청할 때만 업로드됩니다(녹화에서 오른쪽 클릭). Google은 하루 약 6개의 업로드를 허용하며, 나머지는 다음 날까지 기다립니다. 파일은 디스크에 남습니다.',
    'Öffnet die Anmeldedaten der Google Cloud Console im Browser: Projekt anlegen, „YouTube Data API v3“ aktivieren, OAuth-Client „Desktop-App“ erstellen, Client-ID und -Secret hier einfügen.':
        '브라우저에서 Google Cloud 콘솔의 사용자 인증 정보 페이지를 엽니다: 프로젝트를 만들고, ‘YouTube Data API v3’를 사용 설정하고, OAuth 클라이언트 ‘데스크톱 앱’을 만든 후 클라이언트 ID와 보안 비밀을 여기에 붙여 넣으세요.',
    'Vergisst die Google-Freigabe auf diesem PC; die Warteschlange wartet, bis du dich neu verbindest. In deinem Google-Konto unter Sicherheit → Drittanbieter-Apps lässt sich der Zugriff ebenfalls entfernen.':
        '이 PC에서 Google 동의를 삭제합니다. 대기열은 다시 연결할 때까지 기다립니다. Google 계정의 보안 → 서드 파티 앱에서도 액세스를 제거할 수 있습니다.',
    'Die markierte Datei in die YouTube-Warteschlange (Sichtbarkeit wie in den Einstellungen, Standard privat). Hochgeladen wird, sobald du weder in einer Lobby noch in einer Runde bist und das Tageskontingent reicht; der Link erscheint danach im Rechtsklick-Menü.':
        '선택한 파일을 YouTube 대기열에 넣습니다(공개 범위는 설정대로, 기본값은 비공개). 로비나 라운드 중이 아니고 일일 할당량이 허락하면 바로 업로드되며, 그 후 오른쪽 클릭 메뉴에 링크가 나타납니다.',
    'Spotify: Client-ID sieht falsch aus – erwartet werden 32 Zeichen aus 0–9 und a–f (Dashboard → deine App → Settings → Basic Information → Client ID).':
        'Spotify: 클라이언트 ID가 잘못된 것 같습니다 – 0–9와 a–f로 된 32자여야 합니다(대시보드 → 내 앱 → Settings → Basic Information → Client ID).',
    'ALS NÄCHSTES':
        '다음 곡',
    'Unter dem Lied':
        '곡 아래',
    'Rechts neben dem Lied':
        '곡 오른쪽',
    'Als nächstes':
        '다음 곡',
    'Anzahl Titel':
        '표시할 곡 수',
    'Die Liste kommt aus Spotify – einrichten unter Einstellungen → Verbindungen → Spotify.':
        '목록은 Spotify에서 가져옵니다 – 설정 → 연결 → Spotify에서 설정하세요.',
    'Spotify: aus':
        'Spotify: 꺼짐',
    'Spotify: Client-ID fehlt – im Developer-Dashboard anlegen und hier eintragen.':
        'Spotify: 클라이언트 ID 없음 – 개발자 대시보드에서 만들어 여기에 입력하세요.',
    'Spotify: nicht verbunden – „Mit Spotify verbinden“ klicken.':
        'Spotify: 연결되지 않음 – ‘Spotify에 연결’을 클릭하세요.',
    'Spotify: Anmeldung im Browser offen – dort bei Spotify anmelden und zustimmen …':
        'Spotify: 브라우저에 로그인이 열렸습니다 – 거기서 Spotify에 로그인하고 동의하세요 …',
    'Spotify: Port {port} ist belegt – Anmeldung nicht möglich.':
        'Spotify: 포트 {port}이(가) 사용 중입니다 – 로그인할 수 없습니다.',
    'Spotify: Browser konnte nicht geöffnet werden ({error})':
        'Spotify: 브라우저를 열 수 없습니다({error})',
    'Spotify: Anmeldung fehlgeschlagen ({error})':
        'Spotify: 로그인 실패({error})',
    'Spotify: Anmeldung abgelehnt ({error})':
        'Spotify: 로그인 거부됨({error})',
    'Spotify: keine Antwort vom Browser – Anmeldung abgebrochen.':
        'Spotify: 브라우저에서 응답 없음 – 로그인이 취소되었습니다.',
    'Spotify: verbunden':
        'Spotify: 연결됨',
    'Spotify: Anmeldung abgelaufen – bitte neu verbinden.':
        'Spotify: 로그인 만료 – 다시 연결하세요.',
    'Spotify: kein Zugriff ({error}) – ist dein Spotify-Konto in der Developer-App unter „User Management“ eingetragen?':
        'Spotify: 액세스 없음({error}) – Spotify 계정이 개발자 앱의 ‘User Management’에 등록되어 있나요?',
    'Spotify: Fehler – {error}':
        'Spotify: 오류 – {error}',
    'Spotify: Kontingent der Developer-App aufgebraucht – „Als nächstes“ pausiert bis {time}.':
        'Spotify: 개발자 앱의 할당량이 소진되었습니다 – {time}까지 ‘다음 곡’이 일시 중지됩니다.',
    'keine Antwort mit Token':
        '토큰이 있는 응답 없음',
    'Mit Spotify verbunden – du kannst dieses Fenster schliessen.':
        'Spotify에 연결되었습니다 – 이 창을 닫아도 됩니다.',
    'Spotify hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Spotify가 로그인을 거부했습니다 – 이 창을 닫아도 됩니다.',
    'Die nächsten Titel deiner Spotify-Warteschlange unter oder neben dem laufenden Lied. Braucht eine eigene App im Spotify-Developer-Dashboard (Client-ID) und einmal die Anmeldung im Browser; nur solange Spotify spielt.':
        '현재 곡 아래나 옆에 Spotify 대기열의 다음 곡들을 표시합니다. Spotify 개발자 대시보드에 직접 만든 앱(클라이언트 ID)과 브라우저에서 한 번의 로그인이 필요합니다. Spotify가 재생 중일 때만.',
    'Öffnet developer.spotify.com/dashboard im Browser: „Create app“, Redirect URI wie unten angegeben eintragen, die Client-ID kopieren und links einfügen.':
        '브라우저에서 developer.spotify.com/dashboard를 엽니다: ‘Create app’, 아래에 표시된 리디렉션 URI를 입력하고, 클라이언트 ID를 복사해 왼쪽에 붙여 넣으세요.',
    'Vergisst die Spotify-Freigabe auf diesem PC; die Liste verschwindet. In Spotify selbst lässt sich die App unter Konto → Apps ebenfalls entfernen.':
        '이 PC에서 Spotify 동의를 삭제합니다. 목록이 사라집니다. Spotify 자체에서도 계정 → 앱에서 앱을 제거할 수 있습니다.',
    'Alle Arten':
        '모든 종류',
    'Art':
        '종류',
    'Clip abspielen':
        '클립 재생',
    'Clip im Editor öffnen …':
        '편집기에서 클립 열기 …',
    'Im Editor öffnen …':
        '편집기에서 열기 …',
    'Datei kopieren (zum Einfügen)':
        '파일 복사(붙여 넣기용)',
    'Zur Runde springen':
        '라운드로 이동',
    'Farming-Runde':
        '파밍 라운드',
    'Datei fehlt: {file}':
        '파일 없음: {file}',
    '{file} kopiert – mit Strg+V z. B. in Discord einfügen.':
        '{file} 복사됨 – Ctrl+V로 붙여 넣으세요(예: Discord에서).',
    'Die Aufnahme dieser Runde gibt es nicht mehr.':
        '이 라운드의 녹화가 없습니다.',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start.':
        'ffmpeg 없음(imageio-ffmpeg 패키지) – start.bat이 다음 시작 때 설치합니다.',
    'Öffnet den markierten Clip (auch Sofort-Clips von F8) im Clip-Editor: kürzen, zensieren, Ton mischen. Gespeichert wird ein neuer Clip, der alte bleibt.':
        '선택한 클립(F8 즉석 클립 포함)을 클립 편집기에서 엽니다: 자르기, 가리기, 소리 믹싱. 새 클립으로 저장하며 기존 클립은 유지됩니다.',
    'Clip fehlt: {file}':
        '클립 없음: {file}',
    'Keine Videodatei: {file}':
        '동영상 파일이 아닙니다: {file}',
    'Clip gelöscht: {file}':
        '클립 삭제됨: {file}',
    'Clip im Explorer zeigen':
        '탐색기에서 클립 보기',
    'Clip löschen':
        '클립 삭제',
    'Clip nicht gelöscht ({error}): {file}':
        '클립이 삭제되지 않았습니다({error}): {file}',
    'Kein Aufnahmeordner – die Clips liegen in seinem Ordner „Clips“.':
        '녹화 폴더 없음 – 클립은 녹화 폴더의 ‘Clips’ 폴더에 보관됩니다.',
    'Länge':
        '길이',
    'Noch keine Clips – „Clip bearbeiten …“ bei einer Runde oder F8 im Spiel.':
        '아직 클립 없음 – 라운드에서 ‘클립 편집 …’ 또는 게임에서 F8.',
    'Sofort-Clip':
        '즉석 클립',
    'Sofort-Clips (F8)':
        '즉석 클립(F8)',
    'Standbild':
        '정지 화면',
    'Standbilder':
        '정지 화면',
    '{n} von {total} Clips':
        '클립 {total}개 중 {n}개',
    'Spielt den markierten Clip im Standard-Player von Windows ab.':
        '선택한 클립을 Windows 기본 플레이어로 재생합니다.',
    'Öffnet den Explorer mit dem markierten Clip.':
        '선택한 클립으로 탐색기를 엽니다.',
    'Löscht den markierten Clip von der Platte – nach Rückfrage. Nur Dateien, die das Programm selbst angelegt hat.':
        '선택한 클립을 확인 후 드라이브에서 삭제합니다. 프로그램이 직접 만든 파일만.',
    'Öffnet den Ordner „Clips“ neben den Aufnahmen im Explorer.':
        '녹화 옆의 ‘Clips’ 폴더를 탐색기에서 엽니다.',
    'Clips':
        '클립',
    'Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '여백의 회색 선 = 경계(꺼짐) – 끌면 켜집니다',
    'mit kurzer Meldung':
        '짧은 알림과 함께',
    'Clip wird gespeichert …':
        '클립 저장 중 …',
    'Die letzten {n} s aus dem Puffer von OBS':
        'OBS 버퍼의 마지막 {n}초',
    'Clip gespeichert ✓':
        '클립 저장됨 ✓',
    '{n} s · im Tab Aufnahmen → Clips':
        '{n}초 · 녹화 → 클립 탭에 있음',
    'Kein Clip':
        '클립 없음',
    'Zeigt beim Sofort-Clip (F8) unten rechts ein kleines Hinweisfenster – „Clip wird gespeichert …“ und danach „Clip gespeichert“ bzw. warum nicht. Auch im Spiel, ohne Ton; nimmt nie den Fokus.':
        '즉석 클립(F8)에 대해 오른쪽 아래에 작은 알림 창을 표시합니다 – ‘클립 저장 중 …’ 다음에 ‘클립 저장됨’ 또는 실패 이유. 게임 중에도 소리 없이 표시되며 포커스를 빼앗지 않습니다.',
    'Grenzen oben und unten in den schwarzen Balken':
        '검은 여백 위아래 경계',
    'Grenzen zurücksetzen':
        '경계 초기화',
    'Links und rechts gleich':
        '왼쪽과 오른쪽 동일하게',
    'In jedem schwarzen Balken (links und rechts) eine Linie oben und eine unten: Karte, Systemwerte, Heute und Musik bleiben dazwischen – z. B. frei für eine FPS-Anzeige oder Benachrichtigungen. Die Karte wird bei Bedarf kleiner.':
        '각 검은 여백(왼쪽과 오른쪽)의 위와 아래에 선 하나씩: 맵, 시스템 값, 오늘, 음악은 그 사이에 머뭅니다 – 예를 들어 FPS 카운터나 알림을 위한 공간을 남길 때. 필요하면 맵이 작아집니다.',
    'Eine Linie ziehen bewegt die gleiche Linie im anderen Balken mit.':
        '선을 끌면 다른 여백의 같은 선도 함께 움직입니다.',
    'Setzt alle vier Linien auf 8 % vom Rand zurück.':
        '네 선을 모두 가장자리에서 8% 위치로 되돌립니다.',
    'Dunkelgrauer Boden mit hellem Rand – gilt auch im Spiel.':
        '밝은 테두리가 있는 짙은 회색 바닥 – 게임 안에서도.',
    'Dunkelgrauer Boden – die Form der Map bleibt auf dem schwarzen Balken sichtbar. Gilt auch im Spiel.':
        '짙은 회색 바닥 – 검은 여백에서 맵 모양이 보입니다. 게임 안에서도.',
    'Dunkles Lila mit lila Rand, erinnert an die Originalfarbe – gilt auch im Spiel.':
        '라일락 테두리가 있는 짙은 라일락 – 원래 색에 가까움. 게임 안에서도.',
    'Durchsichtiger Boden mit dunklem Rand – gilt auch im Spiel.':
        '어두운 테두리가 있는 투명한 바닥 – 게임 안에서도.',
    'Grau':
        '회색',
    'Grau mit Rand':
        '테두리 있는 회색',
    'Lila dunkel':
        '짙은 라일락',
    'Lila transparent':
        '반투명 라일락',
    'Lila Boden, halb durchsichtig – gilt auch im Spiel.':
        '반투명 라일락 바닥 – 게임 안에서도.',
    'Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe unsichtbar.':
        '중요: DBD의 설정 → 그래픽에서 화면 모드 ‘창 모드 전체 화면’을 선택하세요. 전용 전체 화면에서는 Windows가 게임 위에 창을 표시할 수 없어 맵이 보이지 않습니다.',
    'Ungültiger Servername im Auftrag: {name}':
        '작업에 잘못된 서버 이름: {name}',
    'Die hosts-Datei wurde direkt nach dem Schreiben wieder verändert (Virenschutz oder ein anderes Programm?).':
        '쓴 직후 hosts 파일이 다시 바뀌었습니다(백신 또는 다른 프로그램?).',
    'Keine Schreibrechte auf die hosts-Datei (Administratorrechte?).':
        'hosts 파일을 쓸 권한이 없습니다(관리자 권한?).',
    'Aufbau der Match-Daten speichern':
        '매치 데이터 구조 저장',
    'Öffnet die Stats-Seite so, dass das Userscript einmal den Aufbau ihrer Match-Daten im Download-Ordner speichert: nur Feldnamen und Arten, keine Werte. Damit lässt sich entscheiden, welche Daten das Programm zusätzlich auswerten könnte.':
        '유저스크립트가 매치 데이터의 구조를 다운로드 폴더에 한 번 저장하도록 통계 페이지를 엽니다: 필드 이름과 형식만, 값은 없음. 이를 통해 프로그램이 어떤 데이터를 더 쓸 수 있는지 알 수 있습니다.',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) legt danach „{file}“ in den Download-Ordner: nur die Namen und Arten der Felder, die die Seite liefert – keine Werte, keine Namen, keine IDs. Das Programm liest diese Datei nicht; du kannst sie weitergeben, um zu entscheiden, welche Felder zusätzlich übernommen werden sollen. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '브라우저에서 통계 페이지가 열립니다. 그러면 유저스크립트(버전 {n} 이상)가 ‘{file}’을(를) 다운로드 폴더에 저장합니다: 페이지가 보내는 필드의 이름과 종류만 – 값, 이름, ID는 없음. 프로그램은 이 파일을 읽지 않습니다. 어떤 필드를 더 가져올지 결정하도록 이 파일을 전달할 수 있습니다. 이전 유저스크립트: 먼저 ‘유저스크립트 복사’를 누르고 Tampermonkey에서 교체하세요.',
    'Gegner':
        '상대',
    'Charakter':
        '캐릭터',
    'Begegnungen':
        '대면',
    'Geopfert':
        '희생됨',
    'Getötet':
        '처치됨',
    'Aufgegeben':
        '포기함',
    'Laut Stats-Seite: als Killer die Survivor gegen dich und wie ihr Match endete, als Survivor der Killer und wie dein Match endete. „Getötet“ = vom Killer direkt getötet (z. B. Mori), „Aufgegeben“ schließt verlassene Matches ein. „Ø Kills ohne Aufgaben“ zählt nur Matches, in denen kein Survivor aufgab oder ging. „Farming“ = Begegnungen in Farming-Runden, die „Begegnungen“ nicht zählen.':
        '통계 페이지 기준: 살인마일 때는 상대한 생존자와 그들의 매치 결과, 생존자일 때는 살인마와 내 매치 결과. ‘처치됨’ = 살인마가 직접 처치(예: 메멘토 모리), ‘포기함’에는 나간 매치도 포함됩니다. ‘깨끗한 Ø 처치’는 포기하거나 나간 생존자가 없는 매치만 셉니다. ‘파밍’ = 파밍 라운드에서의 대면으로, ‘대면’에서는 제외됩니다.',
    'Noch keine Runden mit Daten der Stats-Seite in dieser Auswahl.':
        '이 선택에는 아직 통계 페이지 데이터가 있는 라운드가 없습니다.',
    'Schnellste 4K':
        '가장 빠른 4K',
    '{n} von {total} Runden':
        '{total}라운드 중 {n}라운드',
    '{n} Survivor':
        '생존자 {n}명',
    'Ø Kills ohne Aufgaben':
        '깨끗한 Ø 처치',
    'OBS mit DBD starten, falls es noch nicht läuft':
        'OBS가 실행 중이 아니면 DBD와 함께 시작',
    'Startet DBD und ist OBS nicht erreichbar, startet das Programm OBS einmal minimiert im Infobereich – nur, wenn kein OBS-Fenster offen ist. OBS bleibt offen, wenn DBD beendet wird. OBS läuft dann mit denselben Rechten wie das Programm (Administrator).':
        'DBD가 시작될 때 OBS에 연결할 수 없으면 프로그램이 OBS를 한 번 알림 영역으로 최소화해 시작합니다 – 열린 OBS 창이 없을 때만. DBD를 닫아도 OBS는 열려 있습니다. 이때 OBS는 프로그램과 같은 권한(관리자)으로 실행됩니다.',
    'OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS를 시작했지만 연결할 수 없습니다 – OBS의 도구 → WebSocket 서버 설정에서 서버를 켜고 포트/비밀번호를 확인하세요. ({error})',
    'OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio).':
        'OBS를 찾을 수 없습니다 – OBS를 직접 시작하세요(Program Files\\obs-studio에서 찾았음).',
    'OBS konnte nicht gestartet werden: {error}':
        'OBS를 시작할 수 없습니다: {error}',
    'OBS wird gestartet …':
        'OBS를 시작하는 중 …',
    'OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS가 열려 있지만 연결할 수 없습니다 – OBS의 도구 → WebSocket 서버 설정에서 서버를 켜고 포트/비밀번호를 확인하세요. ({error})',
    'Builds':
        '빌드',
    'Build (4 Perks)':
        '빌드(퍼크 4개)',
    'Perk':
        '퍼크',
    'Add-on':
        '애드온',
    'Opfergabe':
        '공물',
    'Kraft/Item':
        '능력/아이템',
    'ohne':
        '제외 시',
    'Dein Loadout laut Stats-Seite (ab Userscript Version 3). „Ergebnis“ = als Killer Ø Kills, als Survivor Anteil entkommen; „ohne“ = dasselbe in deinen Runden derselben Rolle ohne diesen Eintrag. Builds ab {n} Runden. Embleme: Ø Stufe von keins (0) bis Iri (4); „voll“ = Kategorie mit {max} Punkten.':
        '통계 페이지의 내 로드아웃(유저스크립트 버전 3 이상). ‘결과’ = 살인마일 때 Ø 처치, 생존자일 때 탈출 비율. ‘제외 시’ = 같은 역할의 라운드 중 이 항목이 없는 라운드의 같은 값. 빌드는 {n}라운드부터. 엠블럼: 없음(0)부터 무지개(4)까지 Ø 등급, ‘가득’ = 카테고리 {max}점.',
    'Event-Modus':
        '이벤트 모드',
    'keins':
        '없음',
    'Bronze':
        '브론즈',
    'Silber':
        '실버',
    'Gold':
        '골드',
    'Iri':
        '무지개',
    'Emblem':
        '엠블럼',
    'Ø Stufe':
        'Ø 등급',
    'Punktekategorie':
        '점수 카테고리',
    'Ø Punkte':
        'Ø 점수',
    'voll':
        '가득',
    'Killer-Wertung: {list}':
        '살인마 평가: {list}',
    'Noch keine Matches mit Loadout in dieser Auswahl – die Stats-Seite liefert es ab Userscript Version 3 (Einstellungen → Match-Daten → Offizielle Match-Daten → „Userscript kopieren“).':
        '이 선택에는 아직 로드아웃이 있는 매치가 없습니다 – 통계 페이지는 유저스크립트 버전 3부터 이를 보냅니다(설정 → 매치 데이터 → 공식 매치 데이터 → ‘유저스크립트 복사’).',
    'Alle Modi':
        '모든 모드',
    '„{name}“ nicht mehr als Farming-Gegner':
        '‘{name}’을(를) 더 이상 파밍 파트너로 두지 않음',
    '„{name}“ als Farming-Gegner (Runden mit diesem Charakter zählen als Farming)':
        '‘{name}’을(를) 파밍 파트너로(이 캐릭터와의 라운드는 파밍으로 집계)',
    '„{name}“ gilt jetzt als Farming-Gegner – {n} Runden zählen als Farming (auch ältere; Aufnahmen bleiben, wo sie sind).':
        '‘{name}’은(는) 이제 파밍 파트너로 집계됩니다 – 라운드 {n}개가 파밍으로 집계됩니다(이전 라운드 포함, 녹화는 그대로 유지).',
    '„{name}“ gilt nicht mehr als Farming-Gegner.':
        '‘{name}’은(는) 더 이상 파밍 파트너로 집계되지 않습니다.',
    'Farming-Gegner (Rechtsklick auf einen Charakter im Reiter „Gegner“): {names}':
        '파밍 파트너(‘상대’ 탭에서 캐릭터를 오른쪽 클릭): {names}',
    'Gegner & Builds':
        '상대 & 빌드',
    'Maps, Server & PC':
        '맵, 서버 & PC',
    'Bloodpoints & Farming':
        '블러드포인트 & 파밍',
    'Aufnahme markieren: abspielen, Clip schneiden, behalten, löschen – oder Rechtsklick.':
        '녹화를 선택하세요: 재생, 클립 자르기, 보관, 삭제 – 또는 오른쪽 클릭.',
    'Clip markieren: abspielen, im Editor öffnen, löschen – oder Rechtsklick.':
        '클립을 선택하세요: 재생, 편집기에서 열기, 삭제 – 또는 오른쪽 클릭.',
    'Filter{count}':
        '필터{count}',
    'Filter zurücksetzen':
        '필터 초기화',
    'Alle Filter der Statistik zurück auf „alle“ – Zeitraum, Rolle, Region, Killer, Map, Modus und „Farming ausblenden“.':
        '통계의 모든 필터를 ‘전체’로 되돌립니다 – 기간, 역할, 지역, 살인마, 맵, 모드, ‘파밍 숨기기’.',
    'Region, Killer, Map, Modus und „Farming ausblenden“ ein- oder ausklappen. Die Zahl sagt, wie viele davon gerade filtern.':
        '지역, 살인마, 맵, 모드, ‘파밍 숨기기’를 표시하거나 숨깁니다. 숫자는 지금 그중 몇 개가 필터링 중인지 나타냅니다.',
    'Noch keine Runden gespeichert':
        '아직 저장된 라운드 없음',
    'Eine Runde zählt vom Map-Banner bis zum Rundenende (ab 1 Minute) und erscheint hier von selbst. Kills, Escapes und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        '라운드는 맵 배너부터 라운드 종료까지(1분 이상) 집계되며 여기에 자동으로 나타납니다. 처치, 탈출, 블러드포인트는 통계 페이지에서 가져옵니다 – 이를 위해 매치 데이터를 한 번 설정하세요.',
    'Noch keine Aufnahmen – OBS nimmt ab dem nächsten Map-Banner auf. Runden erscheinen hier, Clips (F8 oder aus dem Editor) im Reiter „Clips“.':
        '아직 녹화 없음 – OBS는 다음 맵 배너부터 녹화합니다. 라운드는 여기에, 클립(F8 또는 편집기에서)은 ‘클립’ 탭에 표시됩니다.',
    'Runden pro Tag – letzte {n} Tage':
        '일별 라운드 – 최근 {n}일',
    '{when}: {n} Runden ({k} Killer, {s} Survivor)':
        '{when}: {n}라운드(살인마 {k}, 생존자 {s})',
    '1 s ab Abspielkopf':
        '재생 헤드부터 1초',
    '10 s ab Abspielkopf':
        '재생 헤드부터 10초',
    '100 % = unverändert.':
        '100% = 변경 없음.',
    '3 s ab Abspielkopf':
        '재생 헤드부터 3초',
    '5 s ab Abspielkopf':
        '재생 헤드부터 5초',
    '9:16 (Hochformat)':
        '9:16(세로)',
    'Alle Bilder':
        '모든 이미지',
    'Alle Zeichnungen entfernen':
        '모든 그림 제거',
    'Alles zurücksetzen':
        '모두 초기화',
    'Anderen Ordner …':
        '다른 폴더 …',
    'Aufgenommen (F12)':
        '촬영(F12)',
    'Ausschnitt':
        '자르기',
    'Ausschnitt {w}×{h}':
        '자르기 {w}×{h}',
    'Bearbeitet':
        '편집됨',
    'Bearbeitete Bilder öffnen':
        '편집한 이미지 열기',
    'Bild bearbeiten – {name}':
        '이미지 편집 – {name}',
    'Bild bearbeiten …':
        '이미지 편집 …',
    'Bild gespeichert: {file}':
        '이미지 저장됨: {file}',
    'Bild im Explorer zeigen':
        '탐색기에서 이미지 보기',
    'Bild nicht gespeichert: {error}':
        '이미지가 저장되지 않았습니다: {error}',
    'Speichert …':
        '저장하는 중 …',
    'Bild nicht lesbar: {error}':
        '이미지를 읽을 수 없습니다: {error}',
    'Bild speichern':
        '이미지 저장',
    'Der Clip beginnt aus Schwarz und mit leisem Ton.':
        '클립이 검은 화면에서 시작하며 소리가 커집니다.',
    'Der Clip endet in Schwarz, der Ton wird leiser.':
        '클립이 검은 화면으로 끝나며 소리가 작아집니다.',
    'Dick':
        '굵게',
    'Dünn':
        '가늘게',
    'Eigener Ordner':
        '내 폴더',
    'Eigener Ordner nicht gefunden: {path}':
        '내 폴더를 찾을 수 없습니다: {path}',
    'Einblenden':
        '페이드 인',
    'Entfernt den markierten Kasten (Entf).':
        '선택한 상자를 제거합니다(Del).',
    'Entfernt die markierte Zeichnung (Entf).':
        '선택한 그림을 제거합니다(Del).',
    'Farbe':
        '색상',
    'Farbe zurücksetzen':
        '색상 초기화',
    'Frei':
        '자유',
    'Freihand':
        '자유 곡선',
    'GIF (ohne Ton, für Chats)':
        'GIF(소리 없음, 채팅용)',
    'GIF {h}p, {fps} Bilder/s, ohne Ton':
        'GIF {h}p, 초당 {fps}프레임, 소리 없음',
    'Helligkeit':
        '밝기',
    'Helligkeit, Kontrast und Sättigung auf 100 %.':
        '밝기, 대비, 채도를 100%로 되돌립니다.',
    'Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats).':
        'GIF의 높이 – 작을수록 파일이 작아집니다(Discord, 채팅).',
    'Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern.':
        '화면에서 읽을 수 없게 만들 영역을 끌어 지정하세요 – 이름, 채팅, 친구 목록. 상자는 옮길 수 있고 오른쪽 아래 모서리로 크기를 바꿀 수 있습니다.',
    'Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt sie, Entf löscht sie.':
        '화면에서 끌어 그리세요(텍스트: 클릭). 그림을 클릭하면 선택, 끌면 이동, Del로 제거합니다.',
    'Immer':
        '항상',
    'In Zwischenablage':
        '클립보드로',
    'In die Zwischenablage kopiert – in Discord mit Strg+V einfügen.':
        '클립보드에 복사했습니다 – Discord에서 Ctrl+V로 붙여 넣으세요.',
    'Ohne schwarze Ränder':
        '검은 테두리 없음',
    'Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das Spielbild, „Kein Ausschnitt“ das ganze Bild.':
        '녹화에 검은 테두리가 있습니다: ‘검은 테두리 없음’은 게임 화면만, ‘자르지 않음’은 화면 전체를 저장합니다.',
    'Kein Ausschnitt':
        '자르지 않음',
    'Kein Screenshot-Ordner von Steam für DBD gefunden – noch kein F12-Screenshot, oder Steam speichert woanders („Anderen Ordner …“).':
        'DBD의 Steam 스크린샷 폴더를 찾을 수 없습니다 – 아직 F12 스크린샷이 없거나 Steam이 다른 곳에 저장합니다(‘다른 폴더 …’).',
    'Kontrast':
        '대비',
    'Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C).':
        '편집한 이미지를 복사합니다 – Discord에서 Ctrl+V로 붙여 넣으세요(Ctrl+C).',
    'Kreis':
        '타원',
    'Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen':
        'Space 재생 · ←/→ 1초 · Shift 5초 · Ctrl 1프레임 · I/O 시작/끝 · A 구간 · M 표시 · Home/End 처음/끝 · Del 상자/그림 제거 · Esc 닫기',
    'Letzten Schritt zurücknehmen (Strg+Z).':
        '마지막 단계를 실행 취소합니다(Ctrl+Z).',
    'Linie':
        '선',
    'Links und rechts tauschen.':
        '왼쪽과 오른쪽을 바꿉니다.',
    'Mittel':
        '보통',
    'Oben und unten tauschen.':
        '위와 아래를 바꿉니다.',
    'Ordner mit deinen Screenshots':
        '스크린샷 폴더',
    'Ordner nicht anlegbar: {error}':
        '폴더를 만들 수 없습니다: {error}',
    'PNG: verlustfrei · JPG: kleinere Datei.':
        'PNG: 무손실 · JPG: 더 작은 파일.',
    'Pfeil':
        '화살표',
    'Rahmen':
        '상자',
    'Rahmen bearbeiten':
        '프레임 편집',
    'Rahmen im Bild ziehen, verschieben, an den Ecken ändern.':
        '화면에서 프레임을 끌어 지정하고, 옮기고, 모서리로 바꾸세요.',
    'Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. Nochmal drücken beendet das Werkzeug.':
        '미리 보기에서 프레임을 옮기거나 모서리를 끌어 크기를 바꾸세요. 다시 누르면 도구가 끝납니다.',
    'Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen.':
        '화면에서 영역을 잘라냅니다 – YouTube Shorts와 TikTok용 9:16, Instagram용 1:1. 미리 보기에서 프레임을 옮기고 모서리를 끄세요.',
    'Screenshots':
        '스크린샷',
    'Sehr dick':
        '매우 굵게',
    'Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den Ecken ziehen.':
        '자르기의 화면 비율. 화면에서 프레임을 옮기고 모서리를 끄세요.',
    'Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im Screenshot-Ordner von Steam) bleibt unverändert (Strg+S).':
        '편집한 사본을 Fog Scout 폴더에 저장합니다 – 원본(예: Steam 스크린샷 폴더)은 그대로 유지됩니다(Ctrl+S).',
    'Steam (F12)':
        'Steam(F12)',
    'Steam-Ordner verwenden':
        'Steam 폴더 사용',
    'Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf Markiertes löschen · Esc schliessen':
        'Ctrl+Z 실행 취소 · Ctrl+Y 다시 실행 · Ctrl+C 복사 · Ctrl+S 저장 · Del 선택 항목 제거 · Esc 닫기',
    'Strichstärke bzw. Textgrösse.':
        '선 굵기 또는 텍스트 크기.',
    'Sättigung':
        '채도',
    'Tempo':
        '속도',
    'Text':
        '텍스트',
    'Text für das Text-Werkzeug':
        '텍스트 도구용 텍스트',
    'Um 90° gegen den Uhrzeigersinn drehen.':
        '시계 반대 방향으로 90° 회전합니다.',
    'Um 90° im Uhrzeigersinn drehen.':
        '시계 방향으로 90° 회전합니다.',
    'Verwirft alle Änderungen – das Original bleibt ohnehin unverändert.':
        '모든 변경을 버립니다 – 원본은 어차피 그대로 유지됩니다.',
    'Wie der Bereich unkenntlich wird.':
        '영역을 읽을 수 없게 만드는 방식.',
    'Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des Abspielkopfs. Gilt für neue und für die markierte Zeichnung.':
        '그림이 클립에 표시되는 시간 – 재생 헤드부터. 새 그림과 선택한 그림에 적용됩니다.',
    'Zeichnen':
        '그리기',
    'Zeichnung entfernen':
        '그림 제거',
    'Zeigt das zuletzt gespeicherte Bild im Explorer.':
        '마지막으로 저장한 이미지를 탐색기에서 보여 줍니다.',
    'Zurückgenommenen Schritt wiederholen (Strg+Y).':
        '실행 취소한 단계를 다시 실행합니다(Ctrl+Y).',
    'Zuschneiden':
        '자르기',
    'neu kodiert (wie „Genau“)':
        '재인코딩됨(‘정확하게’처럼)',
    'normal':
        '보통',
    '{n} Abschnitt(e), {length} s':
        '구간 {n}개, {length}초',
    '{w} × {h} Pixel · Original bleibt unverändert':
        '{w} × {h}픽셀 · 원본은 그대로 유지',
    '↶ Rückgängig':
        '↶ 실행 취소',
    '↷ Wiederholen':
        '↷ 다시 실행',
    '⇅ Kippen':
        '⇅ 상하 반전',
    '⇆ Spiegeln':
        '⇆ 좌우 반전',
    '⟲ Links drehen':
        '⟲ 왼쪽으로 회전',
    '⟳ Rechts drehen':
        '⟳ 오른쪽으로 회전',
    'Öffnet das markierte Bild im Bild-Editor: zuschneiden, drehen, Pfeile und Text, zensieren, Farbe – gespeichert wird eine Kopie, das Original bleibt.':
        '선택한 이미지를 이미지 편집기에서 엽니다: 자르기, 회전, 화살표와 텍스트, 가리기, 색상 – 사본이 저장되고 원본은 유지됩니다.',
    'Zeigt die Bilddatei im Explorer.':
        '탐색기에서 이미지 파일을 보여 줍니다.',
    'Öffnet den Ordner mit den bearbeiteten Bildern (Screenshots neben den Aufnahmen bzw. Bilder/Fog Scout).':
        '편집한 이미지가 있는 폴더를 엽니다(녹화 옆의 Screenshots 또는 사진/Fog Scout).',
    'Bilder aus einem eigenen Ordner zeigen – z. B. wenn Steam die Screenshots unkomprimiert in einen anderen Ordner speichert.':
        '직접 지정한 폴더의 이미지를 표시합니다 – 예를 들어 Steam이 압축하지 않은 스크린샷을 다른 폴더에 저장할 때.',
    'Wieder die Screenshots aus Steams Ordner für DBD zeigen (F12 im Spiel).':
        'Steam의 DBD 폴더의 스크린샷을 다시 표시합니다(게임에서 F12).',
    'Bild anklicken: bearbeiten (zuschneiden, zeichnen, zensieren), im Explorer zeigen – Doppelklick öffnet den Editor.':
        '이미지를 클릭하세요: 편집(자르기, 그리기, 가리기), 탐색기에서 보기 – 더블 클릭하면 편집기가 열립니다.',
    'F12 im Spiel ist Steams Screenshot-Taste; das Programm liest Steams Ordner nur. Bearbeitete Bilder sind Kopien im Ordner „Screenshots“ neben den Aufnahmen.':
        '게임의 F12는 Steam의 스크린샷 키입니다. 프로그램은 Steam 폴더를 읽기만 합니다. 편집한 이미지는 녹화 옆 ‘Screenshots’ 폴더의 사본입니다.',
    '1 Bild':
        '이미지 1개',
    '{n} Bilder':
        '이미지 {n}개',
    '★ behalten (nie aufgeräumt) · ⚑ Marken (F8 in der Runde) · ▶ auf YouTube · Rechtsklick auf die Spaltenköpfe: Spalten ein-/ausblenden':
        '★ 보관됨(정리되지 않음) · ⚑ 표시(라운드 중 F8) · ▶ YouTube에 있음 · 머리글 오른쪽 클릭: 열 표시/숨기기',
    'Clips aus dem Editor, Sofort-Clips (F8) und Standbilder, mit ihrer Runde · ▶ auf YouTube · gelöscht werden nur Dateien, die das Programm selbst angelegt hat':
        '편집기의 클립, 즉석 클립(F8), 정지 화면과 해당 라운드 · ▶ YouTube에 있음 · 프로그램이 직접 만든 파일만 삭제됩니다',
    'Status':
        '상태',
    'Schnell (ohne Neukodieren)':
        '빠르게(재인코딩 없음)',
    'Genau (neu kodiert)':
        '정확하게(재인코딩)',
    'Für Discord (Zielgrösse)':
        'Discord용(목표 크기)',
    'GIF (ohne Ton)':
        'GIF(소리 없음)',
    'Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als Video speichern.':
        'GIF는 최대 {limit}초인데 이 클립은 {seconds}초입니다 – 더 짧게 자르거나 동영상으로 저장하세요.',
    'beim Beenden abgebrochen':
        '프로그램이 종료되어 중지됨',
    'Update gesperrt: ein Clip wird noch gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '업데이트 잠김: 아직 클립을 저장하는 중입니다. 끝난 후 ‘업데이트 후 다시 시작’을 다시 클릭하세요.',
    '(gerade {n})':
        '(현재 {n})',
    'Aufnahme gestartet':
        '녹화 시작됨',
    'Aufnahme läuft weiter':
        '녹화 재개됨',
    'Aufnahme läuft weiter.':
        '녹화가 재개되었습니다.',
    'Aufnahme pausieren/weiter':
        '녹화 일시 정지/재개',
    'Aufnahme pausiert':
        '녹화 일시 정지됨',
    'Aufnahme pausiert.':
        '녹화가 일시 정지되었습니다.',
    'Aufnahme starten':
        '녹화 시작',
    'Aufnahme starten/stoppen':
        '녹화 시작/중지',
    'Aufnahme stoppen':
        '녹화 중지',
    'Aufnahme von Hand gestartet.':
        '녹화를 직접 시작했습니다.',
    'Aufnahme wird beendet …':
        '녹화를 중지하는 중 …',
    'Aufnahme-Laufwerk fast voll – Aufnahme beendet':
        '녹화 드라이브가 거의 가득 참 – 녹화가 중지되었습니다',
    'Aufnahme-Laufwerk fast voll – nichts gestartet':
        '녹화 드라이브가 거의 가득 참 – 아무것도 시작하지 않았습니다',
    'Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet':
        '녹화 드라이브가 연결되지 않음 – 아무것도 시작하지 않았습니다',
    'Aufnahmen sind aus.':
        '녹화가 꺼져 있습니다.',
    'Ausgewogen':
        '균형',
    'Automatisch':
        '자동',
    'Bereit':
        '준비됨',
    'Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert.':
        '클립의 화면 높이 – 녹화보다 작으면 축소하며, 확대는 하지 않습니다.',
    'CPU (x264/x265)':
        'CPU(x264/x265)',
    'Clip speichern (F8)':
        '클립 저장(F8)',
    "Der Sofort-Clip (F8) ist auf {clip} s eingestellt, OBS' Wiederholungspuffer hält nur {buf} s – in OBS: Einstellungen → Ausgabe → Wiederholungspuffer → Maximale Wiederholungszeit.":
        '즉석 클립(F8)은 {clip}초로 설정되어 있지만 OBS 리플레이 버퍼는 {buf}초만 담습니다 – OBS에서: 설정 → 출력 → 리플레이 버퍼 → 최대 리플레이 시간.',
    'Die Datei erscheint im Tab Aufnahmen':
        '파일은 녹화 탭에 나타납니다',
    'Es läuft schon eine Aufnahme':
        '이미 녹화가 진행 중입니다',
    'H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel kleiner, braucht aber einen neueren Player.':
        'H.264는 어디서나 재생됩니다. HEVC(H.265)는 같은 품질에서 약 1/3 작지만 최신 플레이어가 필요합니다.',
    'Hoch':
        '높음',
    'Kein Aufnahmeordner gewählt – Einstellungen → Aufnahmen.':
        '선택한 녹화 폴더 없음 – 설정 → 녹화.',
    'Keine Aufnahme':
        '녹화 없음',
    'Keine Aufnahme läuft':
        '진행 중인 녹화 없음',
    'Keine Aufnahme läuft.':
        '진행 중인 녹화가 없습니다.',
    'Kodiere {file} … ({how}, dauert etwas)':
        '{file} 인코딩 중 … ({how}, 시간이 조금 걸림)',
    'Kodierung':
        '인코딩',
    'Marke setzen':
        '표시 설정',
    'Nimmt auf':
        '녹화 중',
    'Nimmt auf (von Hand gestartet)':
        '녹화 중(직접 시작)',
    'Nimmt die Runde in der laufenden Aufnahme auf':
        '진행 중인 녹화 안에서 라운드 녹화 중',
    'OBS lässt Bilder aus ({n} von {total}, Kodierer überlastet) – in OBS Voreinstellung oder Auflösung senken.':
        'OBS가 프레임을 건너뛰고 있습니다({total}개 중 {n}개, 인코더 과부하) – OBS에서 프리셋이나 해상도를 낮추세요.',
    'OBS nicht erreichbar':
        'OBS에 연결할 수 없음',
    'OBS starten, WebSocket-Server einschalten, Port/Passwort prüfen (Einstellungen → Verbindungen → OBS-Verbindung → Verbindung testen). {why}':
        'OBS를 시작하고 WebSocket 서버를 켜고 포트/비밀번호를 확인하세요(설정 → 연결 → OBS 연결 → 연결 테스트). {why}',
    'OBS verpasst Bilder beim Rendern ({n} von {total}, Grafikkarte ausgelastet).':
        'OBS가 렌더링 중 프레임을 놓치고 있습니다({total}개 중 {n}개, 그래픽 카드 사용량 높음).',
    'Pause':
        '일시 정지',
    'Pausiert':
        '일시 정지됨',
    'Schnell':
        '빠르게',
    'Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. Hoch: grösser, nahe am Original.':
        '빠르게: 더 작고 빠르지만 눈에 띄게 흐림. 균형: 이전과 같음. 높음: 더 크고 원본에 가까움.',
    'Stoppen mit demselben Hotkey oder im Tab Aufnahmen':
        '같은 단축키나 녹화 탭에서 중지하세요',
    'Warte auf OBS …':
        'OBS를 기다리는 중 …',
    'Wie aufgenommen':
        '녹화 그대로',
    'Wiederholungspuffer aus':
        '리플레이 버퍼 꺼짐',
    'Wiederholungspuffer in OBS nicht aktiviert':
        'OBS에서 리플레이 버퍼가 켜져 있지 않음',
    'Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; „Automatisch“ nimmt die erste, die geht.':
        '클립을 인코딩하는 장치: 그래픽 카드(NVENC, AMF, Quick Sync – 여기서 ffmpeg가 실제로 쓸 수 있을 때만)는 프로세서에 거의 부담을 주지 않습니다. ‘자동’은 처음으로 작동하는 것을 사용합니다.',
    'letzter Clip {file} (vor {age})':
        '마지막 클립 {file}({age} 전)',
    'Fortsetzen':
        '재개',
    'von Hand gestartet':
        '직접 시작함',
    'von OBS selbst gestartet':
        'OBS에서 직접 시작함',
    'Beendet die laufende Aufnahme jetzt (bei einer Runde ohne Nachlauf) und legt sie in den Aufnahmeordner.':
        '진행 중인 녹화를 지금 중지하고(라운드 종료 후 추가 녹화 없이) 녹화 폴더에 정리합니다.',
    'Hält die laufende Aufnahme an (OBS pausiert); „Fortsetzen“ setzt sie in derselben Datei fort. Marken bleiben an ihrer Stelle.':
        '진행 중인 녹화를 일시 정지합니다(OBS가 일시 정지). ‘재개’를 누르면 같은 파일에 이어서 녹화합니다. 표시는 위치를 유지합니다.',
    'Merkt diesen Moment in der laufenden Aufnahme (⚑) – der Clip-Editor springt später dorthin. Ohne Sofort-Clip.':
        '진행 중인 녹화에 이 순간을 기록합니다(⚑) – 나중에 클립 편집기가 여기로 이동합니다. 즉석 클립은 만들지 않습니다.',
    'Setzt die pausierte Aufnahme fort.':
        '일시 정지된 녹화를 이어서 합니다.',
    'Startet jetzt eine OBS-Aufnahme von Hand – auch ausserhalb einer Runde. Sie läuft, bis du sie stoppst oder DBD beendet wird; ein Map-Banner benennt sie. Hotkey einstellbar.':
        '지금 OBS 녹화를 직접 시작합니다 – 라운드 밖에서도. 중지하거나 DBD를 닫을 때까지 계속되며, 맵 배너가 이름을 정합니다. 단축키 설정 가능.',
    'Wie F8: speichert die letzten Sekunden aus dem OBS-Wiederholungspuffer als Sofort-Clip (Länge unter Einstellungen → Aufnahmen) und setzt eine Marke, falls eine Aufnahme läuft.':
        'F8처럼: OBS 리플레이 버퍼의 마지막 몇 초를 즉석 클립으로 저장하고(길이는 설정 → 녹화), 녹화가 진행 중이면 표시를 설정합니다.',
    '1 Eintrag':
        '항목 1개',
    '{n} Einträge':
        '항목 {n}개',
    '5 Sekunden vor (Shift+→).':
        '5초 앞으로(Shift+→).',
    '5 Sekunden zurück (Shift+←).':
        '5초 뒤로(Shift+←).',
    'Auf der Zeitleiste öffnen':
        '타임라인에서 열기',
    'Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s':
        '녹화 {start} – {end} · 타임라인 {at}부터 · {length}초',
    'Auswahl':
        '선택',
    'Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).':
        '영역 흐리게 – 이름, 채팅, 친구 목록(X).',
    'Bibliothek':
        '라이브러리',
    'Bibliothek ein-/ausblenden.':
        '라이브러리 표시/숨기기.',
    'Bildausschnitt – den Rahmen in der Vorschau ziehen (C).':
        '자르기 – 뷰어에서 프레임을 끄세요(C).',
    'Clip entfernt – die Aufnahme bleibt, wie sie ist.':
        '클립 제거됨 – 녹화는 그대로 유지됩니다.',
    'Clip geteilt – jetzt {n} Clips.':
        '클립 분할됨 – 이제 클립 {n}개.',
    'Clip {n} von {total}':
        '클립 {n}/{total}',
    'Clips auf der Zeitleiste wählen, verschieben und trimmen (V).':
        '타임라인에서 클립을 선택, 이동, 트리밍합니다(V).',
    'Den ganzen Schnitt einpassen (Strg+0).':
        '편집 전체를 맞춤(Ctrl+0).',
    'Der Clip unter dem Abspielkopf beginnt hier (Taste I).':
        '재생 헤드 아래 클립이 여기서 시작합니다(I 키).',
    'Der Clip unter dem Abspielkopf endet hier (Taste O).':
        '재생 헤드 아래 클립이 여기서 끝납니다(O 키).',
    'Diese Aufnahme ist schon auf der Zeitleiste.':
        '이 녹화는 이미 타임라인에 있습니다.',
    'Ein Bild vor (Strg+→); → eine Sekunde.':
        '한 프레임 앞으로(Ctrl+→). →는 1초.',
    'Ein Bild zurück (Strg+←); ← eine Sekunde.':
        '한 프레임 뒤로(Ctrl+←). ←는 1초.',
    'Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt.':
        '선택한 클립을 타임라인에서 제거합니다(Del) – 녹화는 유지됩니다.',
    'Export':
        '내보내기',
    'Exportieren':
        '내보내기',
    'Fog Scout · Editor':
        'Fog Scout · 편집기',
    'Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze.':
        '여기서는 분할할 것이 없습니다 – 재생 헤드가 클립 가장자리에 있습니다.',
    'Hier teilen':
        '여기서 분할',
    'Inspector':
        '인스펙터',
    'Inspector ein-/ausblenden.':
        '인스펙터 표시/숨기기.',
    'Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine andere Videodatei.':
        '녹화 없음 – OBS 녹화와 클립이 여기에 나타나며, ‘가져오기’로 다른 동영상 파일을 불러올 수 있습니다.',
    'Keine Clips auf der Zeitleiste.':
        '타임라인에 클립이 없습니다.',
    'Kürzeste zuerst':
        '짧은 순',
    'Lautstärke der Vorschau (nicht des Clips).':
        '미리 보기의 음량(클립의 음량 아님).',
    '? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export':
        '? 모든 단축키 · Space 재생 · ←/→ 1초 · Shift 5초 · Ctrl 또는 ,/. 1프레임 · I/O 클립 시작/끝 · S 분할 · Del 삭제 · Ctrl+Z/Y 실행 취소/다시 실행 · F 전체 화면 · Ctrl+S 프로젝트 · Ctrl+E 내보내기',
    'Längste zuerst':
        '긴 순',
    'Löschen':
        '삭제',
    'Name A–Z':
        '이름 A–Z',
    'Name des Projekts – auch der Name des exportierten Clips.':
        '프로젝트 이름 – 내보낸 클립의 이름이기도 합니다.',
    'Neueste zuerst':
        '최신 순',
    'Pause (Leertaste)':
        '일시 정지(Space)',
    'Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D).':
        '화면에 화살표, 상자, 자유 곡선, 텍스트를 그립니다(D).',
    'Projekt':
        '프로젝트',
    'Projekt geladen: {name}':
        '프로젝트 불러옴: {name}',
    'Projekt gespeichert: {file}':
        '프로젝트 저장됨: {file}',
    'Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten.':
        '프로젝트 저장(Ctrl+S) – 이 녹화의 편집, 자르기, 그림, 가리기, 내보내기 설정을 저장해 나중에 이어서 작업합니다.',
    'Runde':
        '라운드',
    'Rückgängig (Strg+Z).':
        '실행 취소(Ctrl+Z).',
    'Rückgängig.':
        '실행 취소됨.',
    'Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen (Strg+E) – Format und Kodierung im Inspector unter Export.':
        '편집 결과를 녹화 옆 ‘Clips’ 폴더에 클립으로 씁니다(Ctrl+E) – 형식과 인코딩은 인스펙터의 내보내기에서.',
    'Sichtbar':
        '표시',
    'Sortierung der Bibliothek.':
        '라이브러리 정렬 순서.',
    'Spielt den ganzen Schnitt von vorn ab und springt danach zurück.':
        '편집 전체를 처음부터 재생한 후 다시 돌아갑니다.',
    'Standbild am Abspielkopf als PNG neben den Clips speichern.':
        '재생 헤드 위치의 정지 화면을 클립 옆에 PNG로 저장합니다.',
    'Stärke':
        '강도',
    'Teilen':
        '분할',
    'Teilt den Clip unter dem Abspielkopf in zwei (Taste S).':
        '재생 헤드 아래 클립을 둘로 나눕니다(S 키).',
    'Ton der Vorschau an/aus (Windows).':
        '미리 보기 소리 켜기/끄기(Windows).',
    'Videodatei importieren':
        '동영상 파일 가져오기',
    'Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie eine Aufnahme öffnen.':
        '동영상 파일을 가져옵니다 – 라이브러리에 나타나며 녹화처럼 열립니다.',
    'Videos':
        '동영상',
    'Vollbild – nur die Vorschau (F, Esc beendet).':
        '전체 화면 – 뷰어만(F, Esc로 종료).',
    'Wiederholen (Strg+Y).':
        '다시 실행(Ctrl+Y).',
    'Wiederholt.':
        '다시 실행됨.',
    'Zeitleiste':
        '타임라인',
    'Zeitleiste ein-/ausblenden.':
        '타임라인 표시/숨기기.',
    'Zeitleiste einpassen':
        '타임라인 맞춤',
    'Zeitleiste herauszoomen (−, Strg+Mausrad).':
        '타임라인 축소(−, Ctrl+휠).',
    'Zeitleiste hineinzoomen (+, Strg+Mausrad).':
        '타임라인 확대(+, Ctrl+휠).',
    'Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit.':
        '선택한 클립의 슬로 모션 또는 빨리 감기. 소리도 따라갑니다.',
    'Zum Anfang (Pos1).':
        '처음으로(Home).',
    'Zum Ende (Ende).':
        '끝으로(End).',
    '{at} liegt in keinem Clip der Zeitleiste.':
        '{at}은(는) 타임라인의 어떤 클립에도 없습니다.',
    '{n} Clip(s) · {length} s':
        '클립 {n}개 · {length}초',
    'Älteste zuerst':
        '오래된 순',
    'Öffnen aus der Bibliothek ist hier nicht verfügbar.':
        '여기서는 라이브러리에서 열 수 없습니다.',
    'Fehler in {step} – siehe Log.':
        '{step} 오류 – 로그를 참조하세요.',
    'Strg+{n}':
        'Ctrl+{n}',
    'Tastenkürzel':
        '단축키',
    'Schliessen (? oder Esc)':
        '닫기(? 또는 Esc)',
    'Wiedergabe':
        '재생',
    'Werkzeuge':
        '도구',
    'Leertaste':
        'Space',
    'Abspielen / Anhalten':
        '재생 / 일시 정지',
    '1 Sekunde zurück / vor':
        '1초 뒤로 / 앞으로',
    'Shift+← / →':
        'Shift+← / →',
    '5 Sekunden zurück / vor':
        '5초 뒤로 / 앞으로',
    'Strg+← / →  ·  , / .':
        'Ctrl+← / →  ·  , / .',
    '1 Bild zurück / vor':
        '1프레임 뒤로 / 앞으로',
    'Pos1 / Ende':
        'Home / End',
    'Zum Anfang / zum Schluss':
        '처음으로 / 끝으로',
    'Zur nächsten Marke':
        '다음 표시로',
    'Untertitel {a}–{b}.':
        '자막 {a}–{b}.',
    '{file} wartet – {n} Export(e) davor.':
        '{file} 대기 중 – 앞에 내보내기 {n}개.',
    'Kodiere {file} …':
        '{file} 인코딩 중 …',
    'Titel & Vorschaubild':
        '제목 & 썸네일',
    'Claude fragt: {question}':
        'Claude의 질문: {question}',
    'Deine Antwort …':
        '답변 …',
    'Name der Vorlage':
        '템플릿 이름',
    'Als Vorlage speichern':
        '템플릿으로 저장',
    'Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen.':
        '방금 한 단계들(가리기 상자 제외)을 템플릿으로 보관합니다 – 시간은 처음 또는 끝 기준이므로 다른 길이에도 맞습니다.',
    'Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, kostenlos; erst „Übernehmen“ ändert den Schnitt.':
        '이 편집에 템플릿의 단계를 제안합니다 – Claude 없이, 무료. ‘적용’을 눌러야 편집이 바뀝니다.',
    'Vorlage löschen':
        '템플릿 삭제',
    'Entfernt die gewählte Vorlage.':
        '선택한 템플릿을 제거합니다.',
    'Bitte einen Namen für die Vorlage eingeben.':
        '템플릿 이름을 입력하세요.',
    'Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu).':
        '템플릿으로 쓸 수 있는 것이 없습니다(가리기 상자는 포함되지 않음).',
    'Vorlage „{name}“ gespeichert.':
        '템플릿 ‘{name}’ 저장됨.',
    'Vorlage „{name}“':
        '템플릿 ‘{name}’',
    'Vorlage „{name}“ gelöscht.':
        '템플릿 ‘{name}’ 삭제됨.',
    'Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts wird hochgeladen.':
        '‘내보내기 확인’과 같은 정지 화면 8개를 Claude에게 보냅니다. Claude가 가장 좋은 썸네일을 고르고 제목을 제안합니다. 제목은 직접 가져가고 썸네일은 ‘Clips’에 이미지로만 저장됩니다 – 아무것도 업로드되지 않습니다.',
    'Claude sucht unter {n} Standbildern ein Vorschaubild …':
        'Claude가 정지 화면 {n}개 중에서 썸네일을 고르는 중 …',
    'Als Short-Titel: „{title}“':
        '쇼츠 제목으로: ‘{title}’',
    'Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für YouTube kopierst du ihn selbst.':
        '이 제목을 쇼츠 제목으로 사용합니다(한 번에 실행 취소 가능). YouTube에는 직접 복사하세요.',
    'Vorschaubild bei {at} speichern':
        '{at}의 썸네일 저장',
    'Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im Export, mit dem Titel. Hochgeladen wird nichts.':
        '이 정지 화면을 원래 크기의 PNG로 ‘Clips’에 저장합니다 – 내보내기처럼 가려지고 제목 포함. 아무것도 업로드되지 않습니다.',
    'Short-Titel übernommen.':
        '쇼츠 제목을 사용했습니다.',
    'Vorschaubild':
        '썸네일',
    'Export prüfen':
        '내보내기 확인',
    'Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf einen Fund springt hin und schlägt einen Zensurkasten vor.':
        '완성된 편집의 정지 화면 8개(내보내기처럼 잘리고 가린 영역은 가려짐)를 Claude에게 보냅니다. Claude가 아직 읽을 수 있는 이름이나 채팅, 그 밖에 이대로 공유하면 안 되는 것을 알려 줍니다. 결과를 클릭하면 그 위치로 이동하고 가리기 상자를 제안합니다.',
    'Claude prüft {n} Standbilder des fertigen Schnitts …':
        'Claude가 완성된 편집의 정지 화면 {n}개를 확인하는 중 …',
    'Claude hat nichts gefunden, das so nicht geteilt werden sollte.':
        'Claude가 이대로 공유하면 안 되는 것을 찾지 못했습니다.',
    'Springt hin und schlägt einen Zensurkasten für diese Stelle vor.':
        '그 위치로 이동하고 이 지점에 가리기 상자를 제안합니다.',
    'Springt hin.':
        '그 위치로 이동합니다.',
    'Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.':
        '{at}에 제안 – ‘제안 적용’을 누르면 그 지점을 가립니다.',
    'Name lesbar':
        '이름이 보임',
    'Chat lesbar':
        '채팅이 보임',
    'Auffällig':
        '눈에 띔',
    'Text finden':
        '텍스트 찾기',
    'Sucht auf dem Bild am Abspielkopf nach Text (Namen, Chat) – auf diesem PC, nichts wird gesendet. Die Fundstellen erscheinen nummeriert.':
        '재생 헤드 위치의 화면에서 텍스트(이름, 채팅)를 찾습니다 – 이 PC에서만, 아무것도 전송되지 않습니다. 찾은 것은 번호가 붙어 표시됩니다.',
    'Vorschläge übernehmen':
        '제안 적용',
    'Macht aus den nummerierten Fundstellen Zensurkästen (ein Schritt zum Rückgängigmachen).':
        '번호가 붙은 결과를 가리기 상자로 바꿉니다(한 번에 실행 취소 가능).',
    'Vorschläge verwerfen':
        '제안 버리기',
    'Claude: nur Namen':
        'Claude: 이름만',
    'Schickt das Standbild (zensierte Bereiche bleiben zensiert) mit den nummerierten Fundstellen an Claude; Claude nennt nur die Nummern, die Namen oder Chat zeigen – die übrigen Vorschläge fallen weg.':
        '정지 화면(가린 영역은 가려진 채로)과 번호가 붙은 결과를 Claude에게 보냅니다. Claude는 이름이나 채팅이 보이는 번호만 알려 주고, 나머지 제안은 사라집니다.',
    'Die Texterkennung ist in dieser Installation nicht vorhanden.':
        '이 설치에서는 텍스트 인식을 사용할 수 없습니다.',
    'Suche Text im Bild …':
        '화면에서 텍스트를 찾는 중 …',
    'Das Bild liess sich nicht nach Text durchsuchen.':
        '화면에서 텍스트를 찾을 수 없었습니다.',
    'Kein Text gefunden, der nicht schon verdeckt ist.':
        '아직 가려지지 않은 텍스트를 찾지 못했습니다.',
    '{n} Textstellen gefunden – „Vorschläge übernehmen“ verdeckt sie.':
        '텍스트 위치 {n}곳 찾음 – ‘제안 적용’을 누르면 가려집니다.',
    '{n} Kästen gesetzt.':
        '상자 {n}개 설정됨.',
    'Claude sieht sich {n} Fundstellen an …':
        'Claude가 결과 {n}개를 보는 중 …',
    'Claude hält keine Fundstelle für einen Namen oder Chat.':
        'Claude는 결과 중 이름이나 채팅이 없다고 판단했습니다.',
    '{n} Fundstellen zeigen laut Claude Namen oder Chat.':
        'Claude에 따르면 결과 {n}개에 이름이나 채팅이 보입니다.',
    'Kasten ab hier':
        '여기부터 상자',
    'Kasten bis hier':
        '여기까지 상자',
    'Kasten immer':
        '항상 상자',
    'Der markierte Kasten gilt erst ab dem Bild am Abspielkopf – z. B. wenn ein Name erst später erscheint.':
        '선택한 상자는 재생 헤드 위치의 화면부터만 적용됩니다 – 예를 들어 이름이 나중에야 나타날 때.',
    'Der markierte Kasten gilt nur bis zum Bild am Abspielkopf.':
        '선택한 상자는 재생 헤드 위치의 화면까지만 적용됩니다.',
    'Der markierte Kasten gilt wieder für die ganze Aufnahme.':
        '선택한 상자가 다시 녹화 전체에 적용됩니다.',
    'Kasten {n} gilt von {a} bis {b} der Aufnahme.':
        '상자 {n}은(는) 녹화의 {a}부터 {b}까지 적용됩니다.',
    'Kasten {n} gilt für die ganze Aufnahme.':
        '상자 {n}은(는) 녹화 전체에 적용됩니다.',
    'Am Anfang der Aufnahme gibt es kein „bis hier“.':
        '녹화 시작 지점에는 ‘여기까지’가 없습니다.',
    '{n} davon nur zeitweise.':
        '그중 {n}개는 일정 시간만.',
    'Zurückspringen / Anhalten / Abspielen – L mehrmals: ×2, ×4':
        '뒤로 / 정지 / 재생 – L을 다시 누르면 ×2, ×4',
    'Vollbild an / aus':
        '전체 화면 켜기 / 끄기',
    'Clip beginnt / endet am Abspielkopf':
        '재생 헤드에서 클립 시작 / 끝',
    'S oder Strg+B':
        'S 또는 Ctrl+B',
    'Clip am Abspielkopf teilen':
        '재생 헤드에서 클립 분할',
    'Entf':
        'Del',
    'Markierten Clip löschen':
        '선택한 클립 삭제',
    'Hinein- / herauszoomen':
        '확대 / 축소',
    'Strg+0':
        'Ctrl+0',
    'Ganze Zeitleiste zeigen':
        '타임라인 전체 보기',
    'Auswählen':
        '선택',
    'Bildausschnitt':
        '자르기',
    'Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie':
        '취소, 도구 종료 또는 선택 해제 – 절대 닫지 않음',
    'Strg+W':
        'Ctrl+W',
    'Editor schliessen':
        '편집기 닫기',
    'Abgebrochen.':
        '취소됨.',
    'Esc schliesst den Editor nicht – schliessen mit × oder Strg+W.':
        'Esc로는 편집기가 닫히지 않습니다 – × 또는 Ctrl+W로 닫으세요.',
    'Strg+Z / Strg+Y':
        'Ctrl+Z / Ctrl+Y',
    'Rückgängig / Wiederholen':
        '실행 취소 / 다시 실행',
    'Strg+S':
        'Ctrl+S',
    'Projekt speichern':
        '프로젝트 저장',
    'Strg+E':
        'Ctrl+E',
    'Diese Übersicht ein / aus':
        '이 개요 켜기 / 끄기',
    'In der Statistik zeigen':
        '통계에서 보기',
    'Aufnahme dieser Runde öffnen':
        '이 라운드의 녹화 열기',
    'Runde markieren: Rolle, Farming, Killer oder Map korrigieren, löschen – oder Rechtsklick. Doppelklick zeigt die Aufnahme.':
        '라운드를 선택하세요: 역할, 파밍, 살인마, 맵 수정, 삭제 – 또는 오른쪽 클릭. 더블 클릭하면 녹화가 표시됩니다.',
    'OBS-Passwort ist auf diesem PC/Benutzerkonto nicht lesbar – bitte neu eingeben.':
        '이 PC/사용자 계정에서는 OBS 비밀번호를 읽을 수 없습니다 – 다시 입력하세요.',
    'Als neues Projekt speichern':
        '새 프로젝트로 저장',
    'Autosave aus':
        '자동 저장 꺼짐',
    'Bereich übernehmen':
        '범위 가져오기',
    'Bereich übernommen – Strg+Z stellt das Projekt wieder her.':
        '범위를 가져왔습니다 – Ctrl+Z로 프로젝트를 되돌릴 수 있습니다.',
    'Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. Deine Fassung liegt unter Sicherungen und lokal.':
        '프로젝트가 Fog Scout 밖에서 바뀌었거나 두 개 있습니다. 내 버전은 Sicherungen과 로컬에 보관됩니다.',
    'Die Aufnahme konnte nicht geprüft werden.':
        '녹화를 확인할 수 없습니다.',
    'Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz herunterladen.':
        '녹화가 클라우드에만 있습니다 – 확인하려면 전체를 다운로드해야 합니다.',
    'Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt ist anders). Es wurde nicht geladen.':
        '녹화가 저장된 프로젝트와 맞지 않습니다(내용이 다름). 불러오지 않았습니다.',
    'Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt.':
        '프로젝트의 클립을 읽을 수 없어 기본 클립을 표시합니다.',
    'Die Projektdatei ist unlesbar und wurde nicht geladen.':
        '프로젝트 파일을 읽을 수 없어 불러오지 않았습니다.',
    'Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist lokal gesichert.':
        '프로젝트 파일이 Fog Scout 밖에서 삭제되거나 이동되었습니다. 현재 상태는 로컬에 보관됩니다.',
    'Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.':
        '프로젝트 파일 이름이 바뀌었습니다. 현재 상태는 로컬에 보관됩니다.',
    'Dieses Projekt ist schon in einem anderen Fenster offen – hier wird nichts gespeichert.':
        '이 프로젝트는 이미 다른 창에서 열려 있습니다 – 여기서는 아무것도 저장되지 않습니다.',
    'Editor-Projekte automatisch speichern':
        '편집기 프로젝트 자동 저장',
    'Editor-Projekte nicht gesichert':
        '편집기 프로젝트가 보존되지 않음',
    'Editor-Projekte werden noch gesichert …':
        '편집기 프로젝트를 아직 보존하는 중 …',
    'Editor: automatisches Speichern an.':
        '편집기: 자동 저장 켜짐.',
    'Editor: automatisches Speichern aus – Strg+S speichert das Projekt.':
        '편집기: 자동 저장 꺼짐 – Ctrl+S로 프로젝트를 저장합니다.',
    'Eine wählen …':
        '하나를 선택하세요 …',
    'Erneut prüfen':
        '다시 확인',
    'Es gibt ein Projekt zu einer gleichnamigen, aber veränderten Aufnahme.':
        '같은 이름의 녹화에 대한 프로젝트가 있는데, 녹화가 바뀌었습니다.',
    'Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine Clips.':
        '이 녹화에는 저장된 프로젝트가 있습니다(클립 {n}개). 미리 보기의 범위({a}–{b})를 가져오면 프로젝트의 클립이 바뀝니다.',
    'Gespeichertes Projekt gefunden – die Aufnahme wird geprüft.':
        '저장된 프로젝트를 찾았습니다 – 녹화를 확인하는 중입니다.',
    'Kein Projekt':
        '프로젝트 없음',
    'Kein Projekt – Strg+S legt ein neues an.':
        '프로젝트 없음 – Ctrl+S로 새로 만듭니다.',
    'Keine öffnen':
        '아무것도 열지 않음',
    'Laden':
        '불러오기',
    'Lokal gesicherter Stand eines fehlenden Projekts gefunden.':
        '없어진 프로젝트의 로컬 보관 상태를 찾았습니다.',
    'Mindestens ein Editor-Stand ist weder im Projekt noch lokal gesichert (Speichern hängt oder der Ordner ist nicht erreichbar). Trotzdem beenden? Die ungesicherten Änderungen gehen dann verloren.':
        '편집기 상태 중 하나 이상이 프로젝트에도 로컬에도 보관되지 않았습니다(저장이 멈췄거나 폴더에 접근할 수 없음). 그래도 종료할까요? 보존되지 않은 변경 사항은 사라집니다.',
    'Neu beginnen':
        '새로 시작',
    'Neuerer Stand aus der lokalen Rettungskopie geladen.':
        '로컬 복구 사본에서 더 새로운 상태를 불러왔습니다.',
    'Neues Projekt':
        '새 프로젝트',
    'Nicht laden':
        '불러오지 않음',
    'Nicht schliessen':
        '닫지 않음',
    'Nicht wiederherstellen':
        '복원하지 않음',
    'Nichts tun':
        '아무것도 하지 않음',
    'Ohne Prüfung laden':
        '확인 없이 불러오기',
    'Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, gleiche Grösse).':
        'Fog Scout 1.17 이하의 프로젝트를 찾았습니다(같은 이름, 같은 크기).',
    'Projekt aus neuerer Version – wird nicht überschrieben':
        '더 새로운 버전의 프로젝트 – 덮어쓰지 않음',
    'Projekt behalten':
        '프로젝트 유지',
    'Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen.':
        '프로젝트를 열었습니다 – 미리 보기의 범위는 가져오지 않았습니다.',
    'Projekt nicht gespeichert und keine Rettungskopie möglich: {why}':
        '프로젝트가 저장되지 않았고 복구 사본도 만들 수 없습니다: {why}',
    'Projekt wiederherstellen':
        '프로젝트 복원',
    'Projekt wird gespeichert …':
        '프로젝트를 저장하는 중 …',
    'Projekt wird gesucht …':
        '프로젝트를 찾는 중 …',
    'Prüfen':
        '확인',
    'Prüft Aufnahme …':
        '녹화를 확인하는 중 …',
    'Prüft Aufnahme … {p} %':
        '녹화를 확인하는 중 … {p}%',
    'Speichern und schliessen':
        '저장하고 닫기',
    'Trotzdem laden':
        '그래도 불러오기',
    'Trotzdem schliessen':
        '그래도 닫기',
    'Ungespeicherte Änderungen von {when} gefunden.':
        '{when}의 저장되지 않은 변경 사항을 찾았습니다.',
    'Ungespeicherte Änderungen.':
        '저장되지 않은 변경 사항.',
    'Update wartet: Editor-Projekte werden gesichert …':
        '업데이트 대기 중: 편집기 프로젝트를 보존하는 중 …',
    'Verwerfen und schliessen':
        '버리고 닫기',
    'Wiederherstellen':
        '복원',
    'Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die ganze Aufnahme ist, kann Fog Scout nicht bestätigen.':
        '이 녹화에는 완전히 확인된 적 없는 프로젝트가 있습니다. 시작, 끝, 크기는 맞지만 녹화 전체인지는 Fog Scout가 확인할 수 없습니다.',
    'Zuordnung nicht geprüft':
        '연결이 확인되지 않음',
    '{n} Projektdateien passen zu dieser Aufnahme – keine wurde geöffnet.':
        '이 녹화와 맞는 프로젝트 파일이 {n}개 있습니다 – 아무것도 열지 않았습니다.',
    '● Änderungen':
        '● 변경 사항',
    '⚠ Mehrere Projektdateien – Auswahl nötig':
        '⚠ 프로젝트 파일 여러 개 – 하나를 선택하세요',
    '⚠ Nicht gespeichert – {why}':
        '⚠ 저장되지 않음 – {why}',
    '⚠ Nicht im Projekt gespeichert – lokal gesichert':
        '⚠ 프로젝트에 저장되지 않음 – 로컬에 보관됨',
    '⚠ Projekt ausserhalb geändert':
        '⚠ 프로젝트가 외부에서 바뀜',
    '⚠ Projektdatei fehlt – Änderungen nur lokal gesichert':
        '⚠ 프로젝트 파일 없음 – 변경 사항은 로컬에만 보관됨',
    '⚠ Speichern hängt':
        '⚠ 저장이 멈춤',
    '✓ Gespeichert {at}':
        '✓ {at}에 저장됨',
    'Der grosse Editor speichert sein Projekt von selbst (1,5 s nach einer Änderung, nie während du ziehst) – mit Sicherungen und einer lokalen Kopie, falls die Projektdatei nicht schreibbar ist. Aus: nur Strg+S schreibt das Projekt; dazwischen hält der Editor einen lokalen Wiederherstellungsstand.':
        '큰 편집기는 프로젝트를 자동으로 저장합니다(변경 후 1.5초, 끄는 동안에는 저장하지 않음) – 백업과 함께, 프로젝트 파일을 쓸 수 없을 때를 대비한 로컬 사본도 만듭니다. 끄기: Ctrl+S로만 프로젝트를 씁니다. 그사이 편집기는 로컬 복구 상태를 유지합니다.',
    'Auf alle Clips':
        '모든 클립에',
    'Bild bei {at} der Aufnahme · {length} s ohne Ton':
        '녹화의 {at} 화면 · 소리 없이 {length}초',
    'Den Ausschnitt am Anfang des Clips in der Vorschau ziehen – dazwischen fährt die Kamera gleichmässig.':
        '미리 보기에서 클립 시작 지점의 프레임을 끄세요 – 그 사이에는 카메라가 고르게 움직입니다.',
    'Den Ausschnitt am Ende des Clips in der Vorschau ziehen.':
        '미리 보기에서 클립 끝 지점의 프레임을 끄세요.',
    'Der Clip zeigt wieder das ganze Bild.':
        '클립이 다시 화면 전체를 표시합니다.',
    'Effekte':
        '효과',
    'Effekte entfernen':
        '효과 제거',
    'Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start.':
        '고정 프레임: 시작과 끝이 같음 – 끝 프레임이 시작을 따릅니다.',
    'End-Ausschnitt':
        '끝 프레임',
    'Farbe auf alle {n} Clips übernommen.':
        '색상을 클립 {n}개 모두에 적용했습니다.',
    'Heller oder dunkler – nur dieser Clip.':
        '더 밝게 또는 어둡게 – 이 클립만.',
    'Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen.':
        '이 클립의 밝기, 대비, 채도를 녹화된 그대로 되돌립니다.',
    'Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton.':
        '재생 헤드 위치의 화면을 설정한 시간 동안 멈춰 보여 줍니다(P 키) – 소리 없이.',
    'Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.':
        '더 진하거나 연한 색상, 맨 왼쪽은 흑백 – 이 클립만.',
    'Mehr oder weniger Kontrast – nur dieser Clip.':
        '대비를 높이거나 낮춥니다 – 이 클립만.',
    'Ohne Bewegung':
        '움직임 없음',
    'Rückwärts':
        '역재생',
    'Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.':
        '역재생은 클립당 최대 {n}초까지 가능합니다 – 먼저 이 클립을 분할하세요.',
    'Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens {n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).':
        '클립을 소리까지 거꾸로 재생합니다. 이 녹화에서는 클립당 최대 {n}초(그 이상은 ffmpeg가 메모리를 너무 많이 씀).',
    'Standbild am Abspielkopf einfügen':
        '재생 헤드에 정지 화면 삽입',
    'Standbild einfügen':
        '정지 화면 삽입',
    'Standbild eingefügt: {n} s ohne Ton.':
        '정지 화면 삽입됨: 소리 없이 {n}초.',
    'Standbild hier einfügen':
        '여기에 정지 화면 삽입',
    'Standbild – Clip {n} von {total}':
        '정지 화면 – 클립 {n}/{total}',
    'Start-Ausschnitt':
        '시작 프레임',
    'Wie lange ein Standbild steht – für ein neues, oder für das markierte Standbild.':
        '정지 화면이 유지되는 시간 – 새 정지 화면 또는 선택한 정지 화면에 적용.',
    'Zoom':
        '확대',
    'Zoom entfernen':
        '확대 제거',
    'Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – Esc beendet.':
        '확대: 미리 보기에서 프레임을 끌거나 모서리를 당겨 크기를 바꾸세요 – Esc로 종료.',
    '{n}  Standbild {length} s':
        '{n}  정지 화면 {length}초',
    'Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig).':
        '이 클립의 밝기, 대비, 채도를 타임라인의 모든 클립에 적용합니다(한 단계, Ctrl+Z로 되돌림).',
    'Als Short anzeigen':
        '쇼츠로 보기',
    'Beginnt hier':
        '여기서 시작',
    'Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.':
        '텍스트가 재생 헤드부터 {n}초 동안 쇼츠 아래쪽에 표시됩니다.',
    'Der markierte Untertitel beginnt am Abspielkopf.':
        '선택한 자막이 재생 헤드에서 시작합니다.',
    'Der markierte Untertitel endet am Abspielkopf.':
        '선택한 자막이 재생 헤드에서 끝납니다.',
    'Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen.':
        '미리 보기는 제목과 자막이 들어간 완성된 세로 동영상을 보여 줍니다 – 그림과 가리기는 내보내기에 들어가며 여기에는 표시되지 않습니다.',
    'Ein Short ist höchstens {limit} min lang, dieser Schnitt {seconds} s – kürzer schneiden.':
        '쇼츠는 최대 {limit}분인데 이 편집은 {seconds}초입니다 – 더 짧게 자르세요.',
    'Endet hier':
        '여기서 끝',
    'Entfernen':
        '제거',
    'Entfernt den markierten Untertitel.':
        '선택한 자막을 제거합니다.',
    'Erst den Text des Untertitels eingeben.':
        '먼저 자막 텍스트를 입력하세요.',
    'Hochformat 1080×1920 für YouTube Shorts und TikTok, höchstens 3 min':
        'YouTube Shorts와 TikTok용 세로 1080×1920, 최대 3분',
    'Schriftgrösse des Titels.':
        '제목의 글꼴 크기.',
    'Short (9:16)':
        '쇼츠(9:16)',
    'Short / TikTok (9:16)':
        '쇼츠 / TikTok(9:16)',
    'Short 1080×1920, {fps} fps':
        '쇼츠 1080×1920, {fps}fps',
    'Text eingeben, dann „Untertitel am Abspielkopf“':
        '텍스트를 입력한 다음 ‘재생 헤드에 자막’',
    'Titel':
        '제목',
    'Titel oben (leer = keiner)':
        '위쪽 제목(비워 두면 없음)',
    'Unscharfer Hintergrund':
        '흐린 배경',
    'Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der 9:16-Ausschnitt unter Bild) füllt das Hochformat.':
        '흐린 배경: 가운데에 게임 화면 전체, 위아래에 같은 화면을 흐리게. 자르기: 가운데(또는 이미지의 9:16 자르기)가 세로 화면을 채웁니다.',
    'Untertitel':
        '자막',
    'Untertitel am Abspielkopf':
        '재생 헤드에 자막',
    'Zuschnitt 9:16':
        '9:16 자르기',
    'gross':
        '크게',
    'klein':
        '작게',
    'mittel':
        '보통',
    '⚠ länger als {n} min – so nicht exportierbar':
        '⚠ {n}분보다 김 – 이대로는 내보낼 수 없습니다',
    '(Datei fehlt – wird nicht exportiert)':
        '(파일 없음 – 내보내지 않음)',
    'Beginnt am Abspielkopf':
        '재생 헤드에서 시작',
    'Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt ihn am meisten. Aus: beide gleich laut wie eingestellt.':
        '음악이 재생되는 동안 게임 소리가 자동으로 작아집니다 – ‘강하게’가 가장 많이 줄입니다. 끄기: 둘 다 설정한 음량 그대로.',
    'Der markierte Ton-Clip beginnt am Abspielkopf.':
        '선택한 오디오 클립이 재생 헤드에서 시작합니다.',
    'Die Musik wird am Anfang des Clips lauter.':
        '클립 시작 부분에서 음악이 페이드 인됩니다.',
    'Die Musik wird zum Ende des Clips leiser.':
        '클립 끝으로 갈수록 음악이 페이드 아웃됩니다.',
    'Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im Export läuft die Musik weiter.':
        '미리 보기에서도 음악이 재생됩니다 – 정지 화면은 미리 보기에서는 무음이지만 내보내기에서는 음악이 계속 재생됩니다.',
    'Eigene Tonspur (A2)':
        '내 오디오 트랙(A2)',
    'Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die Spur A2 legen – oder die Datei direkt auf A2 ziehen.':
        '직접 준비한 오디오 또는 동영상 파일(음악, 해설)을 재생 헤드 위치의 A2 트랙에 넣습니다 – 또는 파일을 A2로 끌어 놓으세요.',
    'Höchstens {n} Ton-Clips.':
        '오디오 클립은 최대 {n}개.',
    'Kein Ton in {file}.':
        '{file}에 소리가 없습니다.',
    'Keine Ton- oder Videodatei: {file}':
        '오디오 또는 동영상 파일이 아닙니다: {file}',
    'Lautstärke':
        '음량',
    'Lautstärke der ganzen Spur A2.':
        'A2 트랙 전체의 음량.',
    'Lautstärke des Spieltons im fertigen Clip.':
        '완성된 클립에서 게임 소리의 음량.',
    'Lautstärke nur dieses Ton-Clips.':
        '이 오디오 클립만의 음량.',
    'Lese {file} …':
        '{file} 읽는 중 …',
    'Musik aus':
        '음악 아웃',
    'Musik ein':
        '음악 인',
    'Musik hinzufügen':
        '음악 추가',
    'Musik hinzufügen …':
        '음악 추가 …',
    'Musik oder Kommentar hierher ziehen – oder Rechtsklick „Musik hinzufügen …“':
        '음악이나 해설을 여기로 끌어 놓으세요 – 또는 오른쪽 클릭 ‘음악 추가 …’',
    'Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt.':
        '선택한 오디오 클립을 A2 트랙에서 뺍니다 – 파일은 유지됩니다.',
    'Noch keine Musik – Spielton wie aufgenommen.':
        '아직 음악 없음 – 게임 소리는 녹음된 그대로.',
    'Spielton':
        '게임 소리',
    'Spielton unter Musik':
        '음악 아래 게임 소리',
    'Ton und Video':
        '오디오 및 동영상',
    'Ton-Clip entfernen':
        '오디오 클립 제거',
    'Ton-Clip {file} entfernt – die Datei bleibt.':
        '오디오 클립 {file} 제거됨 – 파일은 유지됩니다.',
    'leicht':
        '약하게',
    'stark':
        '강하게',
    '{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.':
        '{file}이(가) {at}부터 A2에 있습니다 – 그 아래에서 게임 소리가 작아집니다.',
    '{file}: {start} – {end} der Datei, im Clip ab {at}':
        '{file}: 파일의 {start} – {end}, 클립에서는 {at}부터',
    '{n} Ton-Clip(s) auf A2.':
        'A2에 오디오 클립 {n}개.',
    'Als Montage öffnen …':
        '몽타주로 열기 …',
    'Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.':
        '크기가 다릅니다({w}×{h}) – 내보낼 때 검은 테두리로 맞춥니다.',
    'Aufnahme fehlt oder ist nicht lesbar: {file}':
        '녹화가 없거나 읽을 수 없습니다: {file}',
    'Eine Montage übernimmt keinen Bereich aus der Vorschau.':
        '몽타주는 미리 보기의 범위를 가져오지 않습니다.',
    'Erst wenn das Projekt geladen ist.':
        '프로젝트를 불러온 후에만 가능합니다.',
    'Für eine Montage mindestens zwei Videos markieren.':
        '몽타주를 만들려면 동영상을 두 개 이상 선택하세요.',
    'Höchstens {n} Aufnahmen in einer Montage.':
        '몽타주에는 녹화를 최대 {n}개까지 넣을 수 있습니다.',
    'Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das Projekt der Runde bleibt, wie es zuletzt gespeichert war.':
        '이제 몽타주입니다 – 클립 → Montagen에 저장됩니다. 라운드의 프로젝트는 마지막으로 저장한 그대로 유지됩니다.',
    'Montage':
        '몽타주',
    'Montage aus {n} Aufnahmen':
        '녹화 {n}개의 몽타주',
    'Montage nicht zu öffnen – ihre erste Aufnahme fehlt: {file}':
        '몽타주를 열 수 없습니다 – 첫 번째 녹화가 없습니다: {file}',
    'Montage {date}':
        '몽타주 {date}',
    'Nicht gefunden: {files} – ihre Clips sind rot, Exportieren geht erst, wenn sie entfernt sind.':
        '찾을 수 없음: {files} – 해당 클립은 빨간색으로 표시되며, 제거하면 내보낼 수 있습니다.',
    'Nur lesen':
        '읽기 전용',
    'Trotzdem verwenden':
        '그래도 사용',
    'Video nicht lesbar: {file}':
        '동영상을 읽을 수 없습니다: {file}',
    '{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.':
        '{file}은(는) 저장할 때와 같은 녹화가 아닙니다.',
    '{file}: {n} Clip(s) angehängt.':
        '{file}: 클립 {n}개 추가됨.',
    'Audiomediathek':
        '오디오 보관함',
    'Audiomediathek im Browser geöffnet – heruntergeladene Titel erscheinen im Abschnitt Ton, sobald du zurück im Editor bist.':
        '브라우저에서 오디오 보관함을 열었습니다 – 다운로드한 트랙은 편집기로 돌아오면 소리 섹션에 나타납니다.',
    'Neu im Download-Ordner – Klick legt sie am Abspielkopf auf A2:':
        '다운로드 폴더에 새로 있음 – 클릭하면 재생 헤드 위치의 A2에 넣습니다:',
    'Öffnet YouTubes Audiomediathek im Browser: kostenlose Musik und Effekte, für Videos freigegeben (keine Content-ID-Ansprüche). Heruntergeladene MP3s erscheinen hier darunter.':
        '브라우저에서 YouTube 오디오 보관함을 엽니다: 동영상에 써도 되는 무료 음악과 효과음(Content ID 소유권 주장 없음). 다운로드한 MP3는 아래에 나타납니다.',
    'Status, aktuelle Map und deine Runden auf einen Blick':
        '상태, 현재 맵, 내 라운드를 한눈에',
    'Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen':
        '모든 콜아웃 맵 – 보기, 직접 표시, 내 이미지와 메모',
    'Was im Spiel erscheint, wo und wie gross':
        '게임에 무엇을, 어디에, 얼마나 크게 표시할지',
    'Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert':
        '내 라운드, 처치, 대기 시간 – 이 PC에만 저장',
    'Runden, Clips und Screenshots – abspielen, schneiden, aufräumen':
        '라운드, 클립, 스크린샷 – 재생, 자르기, 정리',
    'Server-Regionen wählen und die Verbindung im Blick behalten':
        '서버 지역을 선택하고 연결을 지켜보기',
    'Alles, was Fog Scout tut – suchen mit Strg+F':
        'Fog Scout가 하는 모든 것 – Ctrl+F로 검색',
    'Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche':
        '프로그램이 한 일 – 확인 및 문제 해결용',
    'Übersicht öffnen':
        '개요 열기',
    'Funktionen':
        '기능',
    'aktiv':
        '활성',
    'wartet auf DBD':
        'DBD를 기다리는 중',
    'nimmt auf':
        '녹화 중',
    'verbunden':
        '연결됨',
    'verbindet …':
        '연결하는 중 …',
    'startet …':
        '시작하는 중 …',
    'Fehler – Details im Log':
        '오류 – 자세한 내용은 로그에',
    'nur unter Windows':
        'Windows 전용',
    'HWiNFO fehlt':
        'HWiNFO 없음',
    'Mediensteuerung nicht verfügbar':
        '미디어 컨트롤을 사용할 수 없음',
    'Discord nicht erreichbar':
        'Discord에 연결할 수 없음',
    'Anmeldung nötig':
        '로그인 필요',
    'keine Client-ID':
        '클라이언트 ID 없음',
    'Suche leeren':
        '검색 지우기',
    'Runden · BP/h erst mit Match-Daten':
        '라운드 · BP/시는 매치 데이터가 필요합니다',
    'Verbindung prüfen …':
        '연결 확인 …',
    'Öffnet Einstellungen → Verbindungen: OBS-Verbindung (Port, Passwort) und „Verbindung testen“.':
        '설정 → 연결을 엽니다: OBS 연결(포트, 비밀번호)과 ‘연결 테스트’.',
    '{n} Marken':
        '표시 {n}개',
    '1 Marke':
        '표시 1개',
    'Keine Aufnahme passt zu den Filtern oben.':
        '위 필터와 일치하는 녹화가 없습니다.',
    'Kein Clip passt zu den Filtern oben.':
        '위 필터와 일치하는 클립이 없습니다.',
    'Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.':
        '표시할 줄 없음 – 로그가 비어 있거나 검색과 카테고리가 모두 숨기고 있습니다.',
    'OBS nicht verbunden':
        'OBS 연결 안 됨',
    'Kills, Entkommen und Bloodpoints zählen hier ohne Custom Games – die Rolle „Custom Games“ zeigt sie.':
        '여기서 처치, 탈출, 블러드포인트는 사용자 지정 게임을 빼고 집계됩니다 – 역할 ‘사용자 지정 게임’에서 볼 수 있습니다.',
    'Keine Runden in dieser Auswahl – „Filter zurücksetzen“ zeigt wieder alle.':
        '이 선택에는 라운드가 없습니다 – ‘필터 초기화’를 누르면 모두 다시 표시됩니다.',
    'In dieser Auswahl ist keine Runde einem Match der Stats-Seite zugeordnet – darum fehlen Kills, Entkommen und Bloodpoints.':
        '이 선택의 어떤 라운드도 통계 페이지의 매치와 연결되어 있지 않습니다 – 그래서 처치, 탈출, 블러드포인트가 없습니다.',
    'Kills, Entkommen und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        '처치, 탈출, 블러드포인트는 통계 페이지에서 가져옵니다 – 이를 위해 매치 데이터를 한 번 설정하세요.',
    'Nicht gezählt: {n} × Rundenende nicht erkannt (die nächste Map kam, bevor das Ende erkannt wurde). Zuletzt: {map}, {when}.':
        '집계되지 않음: 라운드 종료 인식 실패 {n}회(종료를 인식하기 전에 다음 맵이 나옴). 마지막: {map}, {when}.',
    '{n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '라운드 종료를 {n}회 인식하지 못했지만 통계 페이지의 길이로 집계했습니다.',
    '{n} × Map mitten im Match falsch erkannt (laut Stats-Seite lief da schon ein Match) – nicht gezählt. Zuletzt: {map}, {when}.':
        '매치 도중 맵을 잘못 읽음 {n}회(통계 페이지에 이미 진행 중인 매치가 있었음) – 집계되지 않음. 마지막: {map}, {when}.',
    'Keine Map passt zu „{text}“. Gesucht wird in Map- und Realm-Namen aller Spielsprachen und in Abkürzungen.':
        '‘{text}’와(과) 일치하는 맵이 없습니다. 검색은 모든 게임 언어의 맵 및 렐름 이름과 약어를 찾습니다.',
    'Leert das Suchfeld und zeigt wieder alle Maps.':
        '검색 필드를 지우고 모든 맵을 다시 표시합니다.',
    'Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter „Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) – die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose.':
        '각 체크는 클릭했을 때 Claude가 돕는 곳 하나입니다 – 스스로 하거나 입력 중에 하는 일은 절대 없습니다: 검색(‘Claude에게 묻기’ 행: 질문과 설정, 페이지, 동작의 이름), 통계 질문(개수와 비율), 클립 편집기(‘Claude로 편집’: 요청과 숫자로 된 편집 정보, 해당 체크 시 정지 화면도), 이미지 편집기(‘Claude’ 탭: 요청과 이미지). Claude는 제안만 하며, 선택하거나 ‘적용’으로 확인하기 전에는 아무것도 실행되지 않습니다. 절대 보내지 않는 것: 라운드, 맵, 살인마, 경로, 파일 이름, 서버, 로그. Anthropic Console의 본인 API 키가 필요합니다(‘API 키 받기’). API는 Claude 구독과 별도로 크레딧에서 결제됩니다(‘크레딧 추가’, 거기서 지출 한도 설정 가능) – 프로그램은 응답으로 질문마다 비용을 추정해 월별로 합산합니다. 키는 Windows 암호화로 이 PC에 저장되며(실패하면 종료할 때까지만 유지), 백업, 로그, 진단에는 절대 들어가지 않습니다.',
    'Zeigt in der Musikkarte, was in Spotify als Nächstes kommt (Position und Anzahl unter Overlay → Musik). Die Windows-Mediensteuerung kennt nur den laufenden Titel, die Liste holt das Programm deshalb von Spotify selbst: Dafür im Developer-Dashboard „Create app“ anlegen (Name frei, API „Web API“), als Redirect URI genau {uri} eintragen, die Client-ID kopieren und hier einfügen, dann „Mit Spotify verbinden“ – der Browser fragt einmal nach der Freigabe. Gelesen wird nur die Warteschlange, nichts gesteuert; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden) und lässt sich hier trennen. Titel kommen nie ins Log.':
        '음악 카드에 Spotify에서 다음에 나올 곡을 표시합니다(위치와 개수는 오버레이 → 음악). Windows 미디어 컨트롤은 현재 곡만 알기 때문에 프로그램이 Spotify에서 직접 목록을 가져옵니다: 개발자 대시보드에서 ‘Create app’(이름 자유, API ‘Web API’), 리디렉션 URI에 정확히 {uri}를 입력하고, 클라이언트 ID를 복사해 여기에 붙여 넣은 후 ‘Spotify에 연결’ – 브라우저가 한 번 동의를 요청합니다. 대기열만 읽고 아무것도 제어하지 않습니다. 동의는 이 PC에 Windows 암호화로 저장되며(사용할 수 없으면 종료할 때까지만 유지) 여기서 제거할 수 있습니다. 곡 제목은 절대 로그에 기록되지 않습니다.',
    'Lädt Clips (F8 und Editor) von selbst auf deinen YouTube-Kanal, Runden nur auf Wunsch: Rechtsklick oder „Auf YouTube hochladen“ unter Aufnahmen. Dafür einmal in der Google Cloud Console ein Projekt anlegen, „YouTube Data API v3“ aktivieren, unter „Anmeldedaten“ einen OAuth-Client vom Typ „Desktop-App“ erstellen und den Zustimmungsbildschirm veröffentlichen (sonst läuft die Anmeldung nach 7 Tagen ab); Client-ID und Client-Secret hier einfügen oder die heruntergeladene JSON-Datei laden, dann „Mit YouTube verbinden“ – der Browser fragt einmal nach der Freigabe. Google erlaubt mit dem Standardkontingent etwa sechs Uploads am Tag; was nicht mehr passt, wartet in der Warteschlange bis zum nächsten Tag. Hochgeladen wird nur, wenn du weder in einer Lobby noch in einer Runde bist; die Datei bleibt immer auch auf der Platte. Gesendet werden nur die Videodatei, Titel (Map, Killer, Datum) und Beschreibung – nie Spielernamen; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden). Mit „Uploads in Playlists einsortieren“ kommt jedes Video zusätzlich in eine Playlist deiner Wahl – dafür fragt die Anmeldung die breitere Berechtigung „YouTube-Konto verwalten“ an (einmal neu verbinden).':
        '클립(F8과 편집기)은 자동으로, 라운드는 요청할 때만 YouTube 채널에 업로드합니다: 녹화에서 오른쪽 클릭 또는 ‘YouTube에 업로드’. 이를 위해 Google Cloud 콘솔에서 한 번 프로젝트를 만들고, ‘YouTube Data API v3’를 사용 설정하고, ‘사용자 인증 정보’에서 ‘데스크톱 앱’ 유형의 OAuth 클라이언트를 만들고 동의 화면을 게시하세요(그렇지 않으면 7일 후 로그인이 만료됨). 클라이언트 ID와 클라이언트 보안 비밀을 여기에 붙여 넣거나 다운로드한 JSON 파일을 불러온 후 ‘YouTube에 연결’ – 브라우저가 한 번 동의를 요청합니다. 기본 할당량으로 Google은 하루 약 6개의 업로드를 허용하며, 넘치는 것은 다음 날까지 대기열에서 기다립니다. 업로드는 로비나 라운드 중이 아닐 때만 진행되며, 파일은 항상 디스크에도 남습니다. 동영상 파일, 제목(맵, 살인마, 날짜), 설명만 전송되며 플레이어 이름은 절대 보내지 않습니다. 동의는 이 PC에 Windows 암호화로 저장됩니다(사용할 수 없으면 종료할 때까지만 유지). ‘업로드를 재생목록으로 분류’를 켜면 모든 동영상이 원하는 재생목록에도 들어갑니다 – 이를 위해 로그인 시 더 넓은 권한 ‘YouTube 계정 관리’를 요청합니다(한 번 더 연결).',
    'Liest Client-ID und Client-Secret aus der Datei „client_secret_….json“, die Google nach dem Anlegen des OAuth-Clients zum Herunterladen anbietet („JSON herunterladen“). Die Datei wird nur gelesen und bleibt, wo sie ist; das Secret landet mit der Windows-Verschlüsselung in den Einstellungen (sonst gilt es nur bis zum Beenden).':
        'OAuth 클라이언트를 만든 후 Google이 다운로드로 제공하는 ‘client_secret_….json’ 파일(‘JSON 다운로드’)에서 클라이언트 ID와 클라이언트 보안 비밀을 읽습니다. 파일은 읽기만 하고 그대로 둡니다. 보안 비밀은 Windows 암호화로 설정에 저장됩니다(그렇지 않으면 종료할 때까지만 유지).',
    'Öffnet die Google-Anmeldung im Browser (nur Recht „Videos hochladen“). Danach kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe mit der Windows-Verschlüsselung auf diesem PC (sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf einem freien Port.':
        '브라우저에서 Google 로그인을 엽니다(‘동영상 업로드’ 권한만). 그 후 브라우저가 127.0.0.1로 돌아오고, 프로그램은 동의를 이 PC에 Windows 암호화로 보관합니다(그렇지 않으면 종료할 때까지만). 이를 위해 로그인 중에만 빈 포트에서 한 번 수신합니다.',
    'Öffnet die Spotify-Anmeldung im Browser. Nach dem Zustimmen kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe (mit der Windows-Verschlüsselung, nur auf diesem PC – sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf diesem Port.':
        '브라우저에서 Spotify 로그인을 엽니다. 동의하면 브라우저가 127.0.0.1로 돌아오고 프로그램이 동의를 보관합니다(Windows 암호화로 이 PC에만 – 그렇지 않으면 종료할 때까지만). 이를 위해 로그인 중에만 이 포트에서 한 번 수신합니다.',
    '({how})':
        '({how})',
    'Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird er nicht gespeichert.':
        'Claude: API 키는 종료할 때까지만 유지됩니다 – Windows 암호화를 사용할 수 없어 저장되지 않습니다.',
    'Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu eintragen oder „Key löschen“.':
        'Claude: 저장된 키를 이 PC에서 읽을 수 없습니다 – 다시 입력하거나 ‘키 삭제’를 사용하세요.',
    'OBS-Passwort gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'OBS 비밀번호는 종료할 때까지만 유지됩니다 – Windows 암호화를 사용할 수 없어 저장되지 않습니다.',
    'OBS-Passwort ist nicht verschlüsselt gespeichert – die Windows-Verschlüsselung ist nicht verfügbar.':
        'OBS 비밀번호가 암호화되지 않은 채 저장되어 있습니다 – Windows 암호화를 사용할 수 없습니다.',
    'Spotify: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'Spotify: 연결됨 – 종료할 때까지만, Windows 암호화를 사용할 수 없습니다.',
    'Unverschlüsselt gespeichert (von früher, die Windows-Verschlüsselung ist nicht verfügbar): {names}.':
        '암호화되지 않은 채 저장됨(이전 것, Windows 암호화를 사용할 수 없음): {names}.',
    'YouTube: Client-Secret gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'YouTube: 클라이언트 보안 비밀은 종료할 때까지만 유지됩니다 – Windows 암호화를 사용할 수 없어 저장되지 않습니다.',
    'YouTube: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'YouTube: 연결됨 – 종료할 때까지만, Windows 암호화를 사용할 수 없습니다.',
    'nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar':
        '이 세션에서만 – Windows 암호화를 사용할 수 없습니다',
    'unverschlüsselt gespeichert (alt)':
        '암호화되지 않은 채 저장됨(이전)',
    'verschlüsselt gespeichert':
        '암호화되어 저장됨',
    'Befehlspalette':
        '명령 팔레트',
    'Suchen':
        '검색',
    'Vorschläge':
        '제안',
    'OBS-Verbindung':
        'OBS 연결',
    'Port und Passwort von OBS stehen unter Verbindungen → OBS-Verbindung.':
        'OBS 포트와 비밀번호는 연결 → OBS 연결에 있습니다.',
    'Qualität: {word} – {mbps} Mbit/s bei {size}':
        '품질: {word} – {size}에서 {mbps}Mbit/s',
    'Qualität: Einstellungen prüfen':
        '품질: 설정을 확인하세요',
    'Qualität: gemessen wird während einer Aufnahme':
        '품질: 녹화 중 측정됨',
    '{words} (letzte Aufnahme)':
        '{words}(마지막 녹화)',
    'gut':
        '좋음',
    'knapp':
        '경계선',
    'matschig':
        '뭉개짐',
    'Einstellungen prüfen':
        '설정을 확인하세요',
    'Qualität verbessern …':
        '품질 개선 …',
    'OBS-Werte zurücksetzen':
        'OBS 값 복원',
    'Aufnahmequalität':
        '녹화 품질',
    'In OBS einstellen':
        'OBS에 설정',
    'Empfohlen (in OBS einzustellen):':
        '권장(OBS에 설정):',
    'Diese Werte lassen sich nur in OBS selbst einstellen – Fog Scout zeigt, wo.':
        '이 값은 OBS 자체에서만 설정할 수 있습니다 – Fog Scout가 위치를 알려 줍니다.',
    'Einstellen geht erst nach der Aufnahme.':
        '설정은 녹화가 끝난 후에만 바꿀 수 있습니다.',
    'Fog Scout stellt in OBS ein (die alten Werte werden gemerkt):':
        'Fog Scout가 OBS에 설정하는 값(이전 값은 보관됨):',
    'Die OBS-Werte von vor „In OBS einstellen“ wiederherstellen?':
        '‘OBS에 설정’ 이전의 OBS 값을 복원할까요?',
    'Nichts einzustellen.':
        '설정할 것이 없습니다.',
    'OBS nimmt gerade auf – Qualität erst nach der Aufnahme einstellen.':
        'OBS가 녹화 중입니다 – 녹화가 끝난 후 품질을 바꾸세요.',
    'In OBS eingestellt – OBS einmal neu starten, damit alle Werte sicher gelten.':
        'OBS에 설정됨 – 모든 값이 확실히 적용되도록 OBS를 한 번 다시 시작하세요.',
    'OBS-Einstellungen zurückgesetzt.':
        'OBS 설정이 복원되었습니다.',
    'OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ ist viel schärfer.':
        'OBS가 ‘방송과 같음’ 또는 ‘작음’ 품질로 녹화합니다 – ‘구별할 수 없는 품질’이 훨씬 선명합니다.',
    'OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.':
        'OBS가 화면을 축소합니다({base} → {out}) – 그래서 흐려집니다.',
    'OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.':
        'OBS가 초당 {fps}프레임으로 녹화합니다 – 60이면 움직임이 훨씬 선명합니다.',
    'Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen.':
        'CPU 인코더가 따라가지 못합니다(프레임 건너뜀) – 그래픽 카드의 인코더를 사용하세요.',
    'Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf CQP 18 stellen (siehe Anleitung).':
        '이 화면에 비해 비트레이트가 너무 낮습니다 – 인코더의 속도 제어를 CQP 18로 설정하세요(단계 참조).',
    'Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf.':
        '비트레이트가 겨우 충분합니다 – CQP 18이면 빠른 장면에서도 화면이 선명하게 유지됩니다.',
    'Ausgabeauflösung = Basisauflösung ({size})':
        '출력 해상도 = 기본 해상도({size})',
    'Bildrate 60':
        '프레임 레이트 60',
    'Aufnahmequalität „Kaum unterscheidbare Qualität“':
        '녹화 품질 ‘구별할 수 없는 품질’',
    'Aufnahme nicht mehr herunterskalieren':
        '녹화 크기 조정 중지',
    'OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:':
        'OBS → 설정 → 출력(방식 ‘단순’) → 녹화:',
    'Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“':
        '녹화 품질: ‘구별할 수 없는 품질, 큰 파일 크기’',
    'Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden':
        '인코더: 가능하면 하드웨어(NVENC/AMD/QSV)',
    'Aufnahmeformat: MKV oder Hybrid-MP4':
        '녹화 형식: MKV 또는 하이브리드 MP4',
    'Video: Ausgabeauflösung = Basisauflösung, Bildrate 60':
        '비디오: 출력 해상도 = 기본 해상도, 프레임 레이트 60',
    'OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:':
        'OBS → 설정 → 출력(방식 ‘고급’) → ‘녹화’ 탭:',
    'Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '비디오 인코더: NVIDIA NVENC H.264 또는 HEVC(‘방송 인코더 사용’ 아님)',
    'Ausgabe neu skalieren: aus':
        '출력 크기 조정: 끄기',
    'x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast':
        'x264: 속도 제어 CRF, 값 18, 프리셋 veryfast',
    'Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)':
        '속도 제어: CQP, CQ 수준 18(HEVC 20)',
    'Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei Durchläufe (Viertelauflösung)':
        '프리셋: P5: Slow(좋은 품질), 튜닝: 고품질, 멀티패스: 2패스(1/4 해상도)',
    'Profil: high (HEVC: main), Keyframe-Intervall: 2 s':
        '프로필: high(HEVC: main), 키프레임 간격: 2초',
    'Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.':
        '그다음 짧은 라운드를 녹화하세요 – 카드에 새 비트레이트가 표시됩니다.',
    'Was die Aufnahme unscharf macht und wie OBS am besten eingestellt wird – was eine Anfrage setzen kann (Ausgabeauflösung, Bildrate, einfache Aufnahmequalität), stellt „In OBS einstellen“ ein, die alten Werte werden gemerkt.':
        '녹화가 흐려지는 원인과 OBS를 가장 잘 설정하는 방법 – 요청으로 설정할 수 있는 것(출력 해상도, 프레임 레이트, 단순 녹화 품질)은 ‘OBS에 설정’이 설정하며, 이전 값은 보관됩니다.',
    'Stellt die OBS-Werte von vor „In OBS einstellen“ wieder her.':
        '‘OBS에 설정’ 이전의 OBS 값을 복원합니다.',
    'Clips und Editor':
        '클립 및 편집기',
    'Erklärung':
        '설명',
    'Sicherung und Ordner':
        '백업 및 폴더',
    'Wann aufgenommen wird':
        '녹화 시점',
    'Video-Encoder: AMD HW H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '비디오 인코더: AMD HW H.264 또는 HEVC(‘방송 인코더 사용’ 아님)',
    'Frequenzsteuerung: CQP, QP-Werte 18 (HEVC 20)':
        '속도 제어: CQP, QP 값 18(HEVC 20)',
    'Voreinstellung: Qualität':
        '프리셋: Quality',
    'Video-Encoder: QuickSync H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '비디오 인코더: QuickSync H.264 또는 HEVC(‘방송 인코더 사용’ 아님)',
    'Frequenzsteuerung: ICQ (oder CQP), Wert 18':
        '속도 제어: ICQ(또는 CQP), 값 18',
    'Target Usage: TU1 bis TU4 – kleiner = bessere Qualität':
        'Target usage: TU1–TU4 – 낮을수록 품질이 좋음',
    'Video-Encoder: der Grafikkarten-Encoder (NVENC, AMF oder QuickSync), wenn OBS einen anbietet – sonst x264':
        '비디오 인코더: OBS가 제공하면 그래픽 카드의 인코더(NVENC, AMF 또는 QuickSync) – 아니면 x264',
    'Video-Encoder: einen eigenen wählen (nicht „Stream-Encoder verwenden“), am besten den der Grafikkarte, wenn OBS einen anbietet':
        '비디오 인코더: 별도 인코더 선택(‘방송 인코더 사용’ 아님), OBS가 제공하면 그래픽 카드의 것이 가장 좋음',
    'Frequenzsteuerung: gleichbleibende Qualität (CQP, CQ, ICQ oder CRF) um 18 statt einer festen niedrigen Bitrate':
        '속도 제어: 낮은 고정 비트레이트 대신 18 정도의 일정 품질(CQP, CQ, ICQ 또는 CRF)',
    'Einschätzung aus Bitrate, Auflösung, Bildrate und Codec – Bildinhalt, Bewegung, Encoder-Voreinstellung und Quelle beeinflussen das Ergebnis.':
        '비트레이트, 해상도, 프레임 레이트, 코덱으로 추정한 값입니다 – 화면 내용, 움직임, 인코더 프리셋, 소스에 따라 결과가 달라집니다.',
    'Start und Meldungen':
        '시작 및 알림',
    'Fog Scout kann mit Windows starten und still im Infobereich (neben der Uhr) warten, bis DBD läuft. Die Lobby-Meldung sagt dir mit einem Ton, wenn ein Match gefunden wurde.':
        'Fog Scout는 Windows와 함께 시작해 DBD가 실행될 때까지 알림 영역(시계 옆)에서 조용히 기다릴 수 있습니다. 로비 알림은 매치를 찾으면 소리로 알려 줍니다.',
    'Optional: OBS Studio nimmt jede Runde auf, Fog Scout sagt OBS nur, wann. Ohne OBS einfach „Weiter“.':
        '선택 사항: OBS Studio가 모든 라운드를 녹화하며, Fog Scout는 OBS에 시점만 알려 줍니다. OBS가 없으면 그냥 ‘다음’.',
    '1. In OBS: Werkzeuge → WebSocket-Servereinstellungen → „WebSocket-Server aktivieren“ anhaken; unter „Verbindungsinformationen anzeigen“ stehen Port und Passwort.':
        '1. OBS에서: 도구 → WebSocket 서버 설정 → ‘WebSocket 서버 사용’ 체크. ‘연결 정보 표시’에서 포트와 비밀번호를 볼 수 있습니다.',
    '2. Port und Passwort hier eintragen und „Verbindung testen“.':
        '2. 여기에 포트와 비밀번호를 입력하고 ‘연결 테스트’를 클릭하세요.',
    '3. Einen Ordner für die Aufnahmen wählen und die Aufnahmen einschalten.':
        '3. 녹화 폴더를 선택하고 녹화를 켜세요.',
    'Wie scharf OBS aufnimmt, zeigt danach die Karte „Aufnahme“ auf der Seite Aufnahmen – dort auch „Qualität verbessern …“.':
        'OBS가 얼마나 선명하게 녹화하는지는 나중에 녹화 페이지의 ‘녹화’ 카드에 표시됩니다 – 거기에 ‘품질 개선 …’도 있습니다.',
    'Alles hier ist freiwillig und lässt sich später unter Einstellungen → Verbindungen einrichten. Jede Verbindung braucht eine eigene App-ID bzw. einen eigenen Key von dir – „Erklärung“ sagt, wo es sie gibt.':
        '여기 있는 것은 모두 선택 사항이며 나중에 설정 → 연결에서 설정할 수 있습니다. 각 연결에는 직접 받은 앱 ID나 키가 필요합니다 – 어디서 받는지는 ‘설명’에 있습니다.',
    'Fog Scout kann anzeigen, mit welchem Spielserver DBD verbunden ist (Region und Ping, auch im Overlay) – dafür fragt Windows einmal nach Administratorrechten.':
        'Fog Scout는 DBD가 연결된 게임 서버(지역과 핑, 오버레이에도)를 표시할 수 있습니다 – 이를 위해 Windows가 한 번 관리자 권한을 요청합니다.',
    'Auf der Seite Server lässt sich ausserdem festlegen, in welchen Regionen DBD Matches sucht. Das ist freiwillig.':
        '서버 페이지에서 DBD가 매치를 찾을 지역도 선택할 수 있습니다. 선택 사항입니다.',
    'Serverregionen auswählen …':
        '서버 지역 선택 …',
    'Beendet die Einrichtung und öffnet die Seite Server – dort die Regionen anhaken, in denen DBD Matches suchen soll.':
        '설정을 마치고 서버 페이지를 엽니다 – 거기서 DBD가 매치를 찾을 지역을 체크하세요.',
    'Öffnet den Ordner mit Einstellungen, Runden, Log und Sicherungen im Explorer.':
        '설정, 라운드, 로그, 백업이 있는 폴더를 탐색기에서 엽니다.',
    'Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an Claude schicken“ einschalten und einen API-Key eintragen.':
        '꺼짐 – 설정 → 연결 → Claude에서 ‘이미지 편집기의 이미지를 Claude에게 보내기’를 켜고 API 키를 입력하세요.',
    'Ausschnitt ausserhalb des Bildes':
        '이미지 밖의 자르기',
    'Bereich unkenntlich machen ({x} %, {y} %)':
        '영역 가리기({x}%, {y}%)',
    'Bilder im Bild-Editor an Claude schicken':
        '이미지 편집기의 이미지를 Claude에게 보내기',
    'Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '이미지에 플레이어 이름이 보일 수 있습니다 – ‘제안’을 클릭할 때만, 축소된 채 메모리에서만 Claude에게 갑니다. 이미 가린 영역은 가려진 채로 유지됩니다. 통계 질문은 역할, 살인마, 맵, 지역, 시간대별 개수와 비율만 보냅니다 – 개별 라운드나 플레이어 이름은 보내지 않습니다.',
    'Claude hat keine Antwort gegeben.':
        'Claude가 답변하지 않았습니다.',
    'Claude zur Statistik fragen: „{q}“':
        '통계에 대해 Claude에게 묻기: ‘{q}’',
    'Claude: Key eingetragen, Claude ist überall aus.':
        'Claude: 키가 입력되었지만 Claude는 모든 곳에서 꺼져 있습니다.',
    'Das Bild hat sich inzwischen geändert – bitte neu vorschlagen.':
        '그사이에 이미지가 바뀌었습니다 – 다시 제안을 요청하세요.',
    'Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude (api.anthropic.com), verkleinert und nur im Speicher.':
        '이미지에 플레이어 이름이 보일 수 있습니다 – 클릭할 때만, 축소된 채 메모리에서만 Claude(api.anthropic.com)에게 갑니다.',
    'Das Bild lässt sich nicht für Claude verkleinern.':
        'Claude용으로 이미지를 축소할 수 없습니다.',
    'Das Standbild liess sich nicht lesen – nichts gesendet.':
        '정지 화면을 읽을 수 없습니다 – 아무것도 보내지 않았습니다.',
    'Die Statistik liess sich nicht zusammenfassen – Details im Log.':
        '통계를 요약할 수 없습니다 – 자세한 내용은 로그에 있습니다.',
    'Drehung ohne Winkel':
        '각도 없는 회전',
    'Farbe ohne Werte':
        '값 없는 색상',
    'Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %':
        '색상: 밝기 {b}%, 대비 {c}%, 채도 {s}%',
    'In der Suche Statistik-Fragen an Claude stellen':
        '검색에서 Claude에게 통계 질문하기',
    'Kasten ausserhalb des Bildes':
        '이미지 밖의 상자',
    'Kippen':
        '상하 반전',
    'Noch keine Runden – Claude hätte nichts zum Auswerten.':
        '아직 라운드가 없습니다 – Claude가 볼 것이 없습니다.',
    'Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du übernimmst.':
        '요청과 여기 보이는 이미지(이미 가린 영역은 가려진 채로)를 Claude에게 보냅니다. 적용하기 전에는 아무것도 바뀌지 않습니다.',
    'Schickt die Frage und Zähler/Quoten deiner Runden an Claude – keine einzelne Runde, keine Namen':
        '질문과 내 라운드의 개수/비율을 Claude에게 보냅니다 – 개별 라운드와 이름은 보내지 않음',
    'Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '재생 헤드 위치의 이미지도 함께 보냅니다(축소, 이미 가린 영역은 가려진 채로) – 그러면 Claude가 예를 들어 이름을 가릴 수 있습니다. 이미지에 플레이어 이름이 보일 수 있습니다.',
    'Spiegeln':
        '좌우 반전',
    'Spiegeln ohne Richtung':
        '방향 없는 반전',
    'Standbild mitsenden':
        '정지 화면 함께 보내기',
    'Standbilder aus Aufnahmen im Clip-Editor an Claude schicken':
        '클립 편집기에서 녹화의 정지 화면을 Claude에게 보내기',
    'Um {deg}° drehen':
        '{deg}° 회전',
    'Vergisst den Vorschlag; das Bild bleibt, wie es ist.':
        '제안을 버립니다. 이미지는 그대로 유지됩니다.',
    'Zensur nur mit Standbild':
        '가리기는 정지 화면이 있을 때만',
    'Zensur: {style}':
        '가리기: {style}',
    'Zuschneiden auf {w} × {h} %':
        '{w} × {h}%로 자르기',
    'unbekannte Art der Zensur':
        '알 수 없는 가리기 방식',
    'unbekannter Schritt':
        '알 수 없는 단계',
    'z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller':
        '예: 플레이어 이름 픽셀화, 16:9로 자르기, 조금 더 밝게',
    'zu viele Kästen':
        '상자가 너무 많음',
    'Zeigt im Bild-Editor den Reiter „Claude“: Du schreibst, was mit dem Bild passieren soll (Namen verpixeln, zuschneiden, heller), und auf „Vorschlagen“ gehen Bitte und Bild verkleinert an Claude. Das Bild kann Spielernamen zeigen; bereits zensierte Bereiche bleiben zensiert.':
        '이미지 편집기에 ‘Claude’ 탭을 표시합니다: 이미지에 원하는 작업(이름 픽셀화, 자르기, 밝게)을 쓰고 ‘제안’을 누르면 요청과 축소된 이미지가 Claude에게 갑니다. 이미지에 플레이어 이름이 보일 수 있으며, 이미 가린 영역은 가려진 채로 유지됩니다.',
    'Erlaubt im grossen Clip-Editor das Häkchen „Standbild mitsenden“: dann geht das Bild an der Abspielposition mit, und Claude kann z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '큰 클립 편집기에서 ‘정지 화면 함께 보내기’ 체크를 허용합니다: 그러면 재생 헤드 위치의 이미지가 함께 가며, Claude가 예를 들어 이름을 가릴 수 있습니다. 이미지에 플레이어 이름이 보일 수 있습니다.',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude zur Statistik fragen“. Gesendet werden deine Frage und Zähler/Quoten deiner Runden je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '검색(Ctrl+F)에 ‘통계에 대해 Claude에게 묻기’ 행을 표시합니다. 질문과 역할, 살인마, 맵, 지역, 시간대별 내 라운드의 개수/비율이 전송됩니다 – 개별 라운드나 플레이어 이름은 보내지 않습니다.',
    'Start: Fenster bereit nach {total} s seit Programmstart (davon {before} s bis Python).':
        '시작: 프로그램 시작 {total}초 후 창 준비됨(그중 Python까지 {before}초).',
    'Haiku 5.5 – am günstigsten':
        'Haiku 5.5 – 가장 저렴',
    'Opus 5.5 – am genauesten':
        'Opus 5.5 – 가장 정확',
    'Sonnet 5.5 – halber Preis':
        'Sonnet 5.5 – 절반 가격',
    'Modell':
        '모델',
    'Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat {month}. Abgerechnet wird in der Anthropic Console.':
        '비용(정가 기준 추정): 이번 세션 요청 {n}개에 {session}, 이번 달 {month}. 결제는 Anthropic Console에서 이루어집니다.',
    'Claude: Welcher Build läuft am besten?':
        'Claude: 어떤 빌드가 가장 좋나요?',
    'Claude: Woche zusammenfassen':
        'Claude: 이번 주 요약',
    'Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?':
        '이번 주를 지난주와 비교해 요약해 줘: 무엇이 더 좋아졌고 무엇이 더 나빠졌어?',
    'Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?':
        '내 퍼크 중 어떤 것이 가장 효과가 좋아? 살인마와 생존자를 따로 알려 줘.',
    'Fog Scout ist abgestürzt':
        'Fog Scout가 중단되었습니다',
    'Fog Scout wurde am {when} unerwartet beendet. „Diagnose kopieren“ legt einen Bericht mit den Stellen des Absturzes in die Zwischenablage – zum Melden auf GitHub oder im Chat. Der Bericht enthält keine Schlüssel, Titel oder Server-Adressen.':
        'Fog Scout가 {when}에 예기치 않게 종료되었습니다. ‘진단 정보 복사’를 누르면 중단 위치가 담긴 보고서가 클립보드에 복사됩니다 – GitHub나 채팅에서 알릴 때 쓰세요. 보고서에는 키, 곡 제목, 서버 주소가 들어 있지 않습니다.',
    'Claude hat keine Stelle gefunden, die heraussticht.':
        'Claude가 눈에 띄는 순간을 찾지 못했습니다.',
    'Claude sieht sich {n} Standbilder an …':
        'Claude가 정지 화면 {n}개를 보는 중 …',
    'Highlights finden':
        '하이라이트 찾기',
    'Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu drei Stellen für einen Short. Die Bilder können Spielernamen zeigen.':
        '편집의 작은 정지 화면(고르게 분포 및 F8 표시 위치, 이미 가린 영역은 가려진 채로)을 Claude에게 보냅니다. Claude가 쇼츠용 순간을 최대 세 개 알려 줍니다. 이미지에 플레이어 이름이 보일 수 있습니다.',
    'Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ ändert den Schnitt.':
        '이 부분만 남기도록 제안합니다 – ‘적용’을 눌러야 편집이 바뀝니다.',
    'Namen beim Zuschauen':
        '관전 중 이름',
    'Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und den Namen oben in der Mitte – bei Bedarf verschieben.':
        '관전 중 DBD가 이름을 표시하는 곳에 상자를 놓습니다: 왼쪽의 더 위쪽 목록과 위쪽 가운데의 이름 – 필요하면 옮기세요.',
    'Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        '매치에서 DBD가 생존자 이름을 표시하는 곳(게임 화면 왼쪽 아래)에 상자를 놓습니다 – 필요하면 옮기세요.',
    'Aufnahme zeigen':
        '녹화 보기',
    'Aufnahme abspielen':
        '녹화 재생',
    'Zu dieser Runde gibt es keine Aufnahme.':
        '이 라운드의 녹화가 없습니다.',
    'Die Aufnahme dieser Runde ist durch die Filter der Seite Aufnahmen ausgeblendet.':
        '이 라운드의 녹화가 녹화 페이지의 필터로 숨겨져 있습니다.',
    'Sitzungen':
        '세션',
    'Killer/Survivor':
        '살인마/생존자',
    '{n} K':
        '{n} K',
    '{n} S':
        '{n} S',
    'Ø Dauer einer Sitzung':
        '세션 Ø 길이',
    'Ø Runden je Sitzung':
        '세션당 Ø 라운드',
    'Ø Warten':
        'Ø 대기',
    'Eine Sitzung endet nach {n} Minuten ohne Runde. Es gelten die Filter oben – mit einem Rollenfilter zählt eine Sitzung nur die Runden dieser Rolle. Ø Kills, Entkommen und BP laut Stats-Seite. Doppelklick zeigt die Runden der Sitzung unter „Letzte Runden“.':
        '세션은 라운드 없이 {n}분이 지나면 끝납니다. 위의 필터가 적용됩니다 – 역할 필터가 있으면 세션에는 그 역할의 라운드만 집계됩니다. Ø 처치, 탈출, BP는 통계 페이지 기준. 더블 클릭하면 ‘최근 라운드’에 세션의 라운드가 표시됩니다.',
    'Blutpunkte-Stand – letzter Wert {per}':
        '블러드포인트 잔액 – 마지막 값 {per}',
    'Cap erreicht':
        '한도 도달',
    'Cap in ≈ {n} Runden':
        '약 {n}라운드 후 한도',
    'Cap: {cap}':
        '한도: {cap}',
    'Noch kein Blutpunkte-Stand gelesen – er kommt aus der Lobby nach der Runde.':
        '아직 읽은 블러드포인트 잔액이 없습니다 – 라운드 후 로비에서 가져옵니다.',
    '{when}: Stand {bp} BP':
        '{when}: 잔액 {bp} BP',
    '+{n} Level':
        '+{n}레벨',
    '+{n} P':
        '+{n} P',
    'Eine Zeile oben anklicken, um den Verlauf zu sehen.':
        '위에서 행을 클릭하면 추세를 볼 수 있습니다.',
    'Keine Matches mit Prestige in dieser Auswahl.':
        '이 선택에는 프레스티지가 있는 매치가 없습니다.',
    'Level':
        '레벨',
    'Matches':
        '매치',
    'Noch kein Prestige in dieser Auswahl – es kommt aus den Match-Daten (Userscript ab Version 3).':
        '이 선택에는 아직 프레스티지가 없습니다 – 매치 데이터(유저스크립트 버전 3 이상)에서 가져옵니다.',
    'Prestige':
        '프레스티지',
    'Prestige und Level deiner Charaktere laut Stats-Seite (ab Userscript Version 3). „Prestige“ und „Level“ = der neueste Stand; „Zuwachs“ und „Matches“ gelten für die Filter oben. Eine Zeile anklicken zeigt darunter den Verlauf dieses Charakters. „Tempo“ = gewonnene Level pro Woche aus den Matches der letzten {days} Tage, „Nächstes P“ = wie lange es bei diesem Tempo bis zur nächsten Stufe dauert. Level steigen nur, wenn du Blutpunkte im Blutnetz ausgibst – die Prognose sagt, was bisher geschah, keine Zusage. „Main“ = dein Charakter mit den meisten Matches je Rolle. „P100“ und „Höchster“ zählen nur Charaktere, die in deinen Match-Daten vorkommen.':
        '통계 페이지의 내 캐릭터 프레스티지와 레벨(유저스크립트 버전 3 이상). ‘프레스티지’와 ‘레벨’ = 최신 상태. ‘상승’과 ‘매치’는 위의 필터를 따릅니다. 행을 클릭하면 아래에 해당 캐릭터의 추세가 표시됩니다. ‘속도’ = 최근 {days}일 동안의 매치에서 주당 오른 레벨, ‘다음 P’ = 그 속도로 다음 등급까지 걸리는 시간. 레벨은 블러드웹에서 블러드포인트를 쓸 때만 오릅니다 – 예측은 지금까지의 기록일 뿐 보장이 아닙니다. ‘메인’ = 역할별로 매치가 가장 많은 캐릭터. ‘P100’과 ‘최고’는 매치 데이터에 나오는 캐릭터만 셉니다.',
    'Prestige von {name} {per}':
        '{name}의 프레스티지 {per}',
    'Zuletzt':
        '마지막 플레이',
    'Zuwachs':
        '상승',
    '{when}: Prestige {p} · Level {level}':
        '{when}: 프레스티지 {p} · 레벨 {level}',
    '+{n} weitere':
        '+{n}개 더',
    'Charaktere':
        '캐릭터',
    'Höchster':
        '최고',
    'Level diese Woche':
        '이번 주 레벨',
    'Main':
        '메인',
    'Meilenstein: {name} ist jetzt Prestige {p}':
        '달성: {name}이(가) 이제 프레스티지 {p}입니다',
    'Nächstes P':
        '다음 P',
    'P100 erreicht':
        'P100 달성',
    'Prestige gesamt':
        '프레스티지 합계',
    'alle Charaktere':
        '모든 캐릭터',
    'seit Montag':
        '월요일부터',
    '{k} Killer · {s} Survivor':
        '살인마 {k} · 생존자 {s}',
    '{name} ist jetzt Prestige {p}':
        '{name}이(가) 이제 프레스티지 {p}입니다',
    '{name} · Level {level}':
        '{name} · 레벨 {level}',
    '{n} Level/Woche':
        '주당 {n}레벨',
    '≈ 1 Tag':
        '≈ 1일',
    '≈ 1 Woche':
        '≈ 1주',
    '≈ {n} Tage':
        '≈ {n}일',
    '≈ {n} Wochen':
        '≈ {n}주',
    '{n} Charaktere':
        '캐릭터 {n}명',
    'P100':
        'P100',
    '{n}× Killer':
        '살인마 {n}회',
    '{n}× Survivor':
        '생존자 {n}회',
    '{n}× Farming':
        '파밍 {n}회',
    '{n}× Custom Game':
        '사용자 지정 게임 {n}회',
    '{n}× ohne Rolle':
        '역할 없음 {n}회',
    'Zeigt, was diese Kachel zählt':
        '이 타일이 무엇을 세는지 보여 줍니다',
    'Diese Runden sind durch die Filter der Statistik ausgeblendet.':
        '이 라운드들은 통계 필터로 숨겨져 있습니다.',
    'Automatisch (zuletzt benutztes Gerät)':
        '자동(마지막으로 사용한 장치)',
    'Dunkle Fläche hinter den Eingaben':
        '입력 뒤 어두운 영역',
    'EINGABEN':
        '입력',
    'Eingaben im Spiel':
        '게임 내 입력',
    'Eingaben im Spiel zeigen (Tasten, Maus, Gamepad)':
        '게임에 입력 표시(키, 마우스, 게임패드)',
    'Gamepad':
        '게임패드',
    'Gerät':
        '장치',
    'Tastatur und Maus':
        '키보드와 마우스',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter den Tasten.':
        '키 뒤에 모서리가 둥근 반투명 어두운 영역.',
    'wartet auf eine Runde':
        '라운드를 기다리는 중',
    'Eingaben mit der Aufnahme speichern (für den Clip-Editor)':
        '녹화와 함께 입력 저장(클립 편집기용)',
    'Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). Eine offizielle Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.':
        'Fog Scout는 다음 키 중 지금 눌린 것만 표시합니다: W, A, S, D, Q, E, R, Space, Shift, Ctrl, 마우스 버튼, 게임패드(버튼, 트리거, 스틱). 라운드 중에만, DBD가 활성 창일 때만 읽습니다 – Fog Scout는 다른 프로그램에서 입력하는 내용을 절대 보지 않습니다. 이 중 어떤 것도 기록하거나 전송하지 않고 게임에 아무것도 보내지 않습니다. ‘녹화와 함께 입력 저장’을 켜면 라운드의 키가 OBS 녹화 옆에 파일로 보관됩니다(클립 편집기용). Behaviour가 이런 표시를 공식적으로 승인한 적은 없으며, 게임에서 이점을 주지 않습니다.',
    'Gelesen werden nur W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad – nur während einer Runde und nur, solange DBD vorne ist. Gesendet wird nichts; gespeichert nur mit dem Häkchen oben, als Datei neben der eigenen Aufnahme.':
        'W, A, S, D, Q, E, R, Space, Shift, Ctrl, 마우스 버튼, 게임패드만 읽습니다 – 라운드 중에만, DBD가 맨 앞에 있을 때만. 아무것도 전송하지 않으며, 위 상자를 켰을 때만 내 녹화 옆에 파일로 저장합니다.',
    'Eine Karte im Spiel zeigt, welche Tasten, Maustasten oder Gamepad-Knöpfe du gerade drückst – wie bei Streamern. Gelesen wird nur eine feste Liste von Tasten, nur während einer Runde und nur, solange DBD vorne ist; gesendet wird nichts, gespeichert nur mit „Eingaben mit der Aufnahme speichern“.':
        '게임 안의 카드가 지금 누르고 있는 키, 마우스 버튼, 게임패드 버튼을 보여 줍니다 – 스트리머들처럼. 정해진 키 목록만, 라운드 중에만, DBD가 맨 앞에 있을 때만 읽습니다. 아무것도 전송하지 않으며, ‘녹화와 함께 입력 저장’을 켰을 때만 저장합니다.',
    'Mit OBS-Aufnahmen: die gedrückten Tasten der Runde kommen als kleine Datei neben die Aufnahme – der Clip-Editor zeigt sie als Spur und kann die Karte ins Video einbrennen. Die Datei wird mit der Aufnahme verschoben und gelöscht.':
        'OBS 녹화 시: 라운드 중 누른 키가 녹화 옆의 작은 파일에 저장됩니다 – 클립 편집기는 이를 트랙으로 보여 주고 카드를 동영상에 넣을 수 있습니다. 파일은 녹화와 함께 이동하고 삭제됩니다.',
    'Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme speichern“). Clips aus F8 haben keine.':
        '녹화 옆의 파일에서(오버레이 › 입력 › ‘녹화와 함께 입력 저장’). F8 클립에는 없습니다.',
    'Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet).':
        '라운드 중 누른 키를 보여 주는 카드가 완성된 동영상에 들어갑니다 – 선택한 모서리에, 편집에 맞춰(속도와 역재생 포함).',
    'Dunkle Fläche hinter den Tasten':
        '키 뒤 어두운 영역',
    'Ecke':
        '모서리',
    'Eine halb durchsichtige dunkle Fläche hinter der Karte.':
        '카드 뒤의 반투명 어두운 영역.',
    'Eingaben im Export zeigen':
        '내보내기에 입력 표시',
    'Höhe der Karte im Verhältnis zur Bildhöhe.':
        '화면 높이에 대한 카드의 높이.',
    'Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade benutzt wurde.':
        '카드가 보여 줄 장치 – 자동이면 방금 사용한 장치.',
    'Wo die Karte im Bild liegt.':
        '화면에서 카드의 위치.',
    'Claude baut einen Short aus {n} Standbildern …':
        'Claude가 정지 화면 {n}개로 쇼츠를 만드는 중 …',
    'Clip um Moment':
        '순간 주변 클립',
    'Der Schnitt hat sich inzwischen geändert – bitte noch einmal.':
        '그사이에 편집이 바뀌었습니다 – 다시 시도하세요.',
    'Der Schnitt wird der markierte Moment ({before} s davor bis {after} s danach).':
        '편집이 선택한 순간({before}초 전부터 {after}초 후까지)이 됩니다.',
    'Die Bilder liessen sich nicht lesen.':
        '이미지를 읽을 수 없습니다.',
    'F8-Marke':
        'F8 표시',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden.':
        '지금은 할 수 없습니다 – 현재 편집을 먼저 마치세요.',
    'Kein Ladebildschirm am Anfang oder Ende gefunden.':
        '시작이나 끝에서 로딩 화면을 찾지 못했습니다.',
    'Kein Leerlauf gefunden.':
        '아무 입력 없는 구간을 찾지 못했습니다.',
    'Ladebildschirm abschneiden':
        '로딩 화면 잘라내기',
    'Leerlauf kürzen':
        '입력 없는 시간 줄이기',
    'Momente':
        '순간',
    'Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst „Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen.':
        '찾은 순간(키, 게임 소리, F8 표시에서 – 숫자로만)의 정지 화면과 편집 정보를 Claude에게 보냅니다. Claude가 쇼츠 전체 – 범위, 슬로 모션, 제목, 자막 – 를 제안합니다. ‘적용’을 눌러야 편집이 바뀝니다. 이미지에 플레이어 이름이 보일 수 있습니다.',
    'Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war (aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.':
        '{n}초 이상 아무 키도 누르지 않은 구간을 잘라냅니다(녹화의 입력 기준) – 한 번에 실행 취소 가능.',
    'Sehe mir Anfang und Ende an …':
        '시작과 끝을 확인하는 중 …',
    'Short vorschlagen':
        '쇼츠 제안',
    'Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.':
        '처음과 마지막 {n}초를 보고 검은 시작이나 끝을 잘라냅니다 – 한 번에 실행 취소 가능.',
    'laut':
        '소리 큼',
    'viele Tasten':
        '많은 키',
    '{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z macht es rückgängig.':
        '입력 없는 구간 {n}개 줄임({seconds}초) – Ctrl+Z로 되돌립니다.',
    '{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – Strg+Z macht es rückgängig.':
        '검은 구간 {n}개 잘라냄({seconds}초) – Ctrl+Z로 되돌립니다.',
    'Anordnen':
        '배치',
    'Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · Tab = nächstes Element · Esc = fertig':
        '배치 중 – 게임에서도: 요소 끌기 · 화살표 키 = 미세 조정(Shift = 10px) · Tab = 다음 요소 · Esc = 완료',
    'Anordnen: alle Elemente mit der Maus ziehen – in der Vorschau und direkt im Spiel. Strg+Mausrad ändert die Grösse, Esc beendet.':
        '배치: 모든 요소를 마우스로 끌어 옮기세요 – 미리 보기에서도, 게임에서 바로도. Ctrl+휠로 크기를 바꾸고 Esc로 끝냅니다.',
    'Automatisch: im schwarzen Rand neben dem Spielbild bzw. neben dem DBD-Fenster. Frei platzieren: „Anordnen“ oder eine Schnellposition.':
        '자동: 게임 화면 옆 또는 DBD 창 옆의 검은 여백에. 자유롭게 배치하려면: ‘배치’ 또는 빠른 위치.',
    'CPU, GPU, RAM':
        'CPU, GPU, RAM',
    'Callout-Karte der Map':
        '맵의 콜아웃 맵',
    'Die Linien in der Vorschau mit „Anordnen“ ziehen – Karte, Systemwerte, Heute und Musik bleiben im Balken dazwischen.':
        '‘배치’로 미리 보기에서 선을 끄세요 – 맵, 시스템 값, 오늘, 음악은 여백 안에서 그 사이에 머뭅니다.',
    'Ein- oder ausblenden':
        '표시 또는 숨기기',
    'Elemente':
        '요소',
    'Entsperren: wieder verschiebbar':
        '잠금 해제: 다시 옮길 수 있음',
    'Fokus':
        '포커스',
    'Frei platzieren: „Anordnen“, eine Schnellposition oder Vorgabe „eigene Position“.':
        '자유롭게 배치하려면: ‘배치’, 빠른 위치 또는 ‘사용자 지정 위치’ 설정.',
    'Gesperrt – erst entsperren':
        '잠김 – 먼저 잠금을 해제하세요',
    'Gilt für alle Elemente':
        '모든 요소에 적용',
    'Grenzen und Platz':
        '경계와 공간',
    'Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen':
        '경계선: 여백 안의 요소가 닿을 수 있는 곳까지 끄세요',
    'Grösse und Deckkraft':
        '크기와 불투명도',
    'Grösse von {name}: Ecke ziehen':
        '{name}의 크기: 모서리를 끄세요',
    'Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, Rechtsklick = Menü. Ende mit „Fertig“ oder Esc.':
        '요소를 클릭하면 선택됩니다. ‘배치’에서: 요소 끌기 = 이동(점선 프레임이 놓일 위치를 표시), 모서리 끌기 또는 Ctrl+휠 = 크기, 오른쪽 클릭 = 메뉴. ‘완료’ 또는 Esc로 끝냅니다.',
    'Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel':
        '클릭으로 요소 선택 · ‘배치’로 이동 켜기 – 여기와 게임에서',
    'Klick wählt {name}':
        '클릭하면 {name} 선택',
    'Layout für {size}':
        '{size}의 레이아웃',
    'Läuft gerade':
        '지금 재생 중',
    'Mitte':
        '가운데',
    'Nach {where} legen (mit Rand)':
        '{where}에 배치(여백 포함)',
    'Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein).':
        '위치와 크기는 DBD 창 크기별로 보관됩니다(일반 탭).',
    'Runden und Zeit heute':
        '오늘의 라운드와 시간',
    'Schnellposition':
        '빠른 위치',
    'Sperren':
        '잠금',
    'Sperren: im Modus „Anordnen“ nicht mehr verschiebbar':
        '잠금: ‘배치’에서 더 이상 옮겨지지 않음',
    'Stil, Abstand, Grenzen, Discord':
        '스타일, 간격, 경계, Discord',
    'Tasten und Gamepad':
        '키와 게임패드',
    'Timer, Bilanz, Server':
        '타이머, 기록, 서버',
    'Verhalten':
        '동작',
    'Zeilen':
        '행',
    'Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)':
        '자동 위치로 돌아가기(검은 여백, 다른 요소 옆)',
    'eigener Platz':
        '사용자 지정 위치',
    'eingerastet':
        '맞춰짐',
    'graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '여백의 회색 선 = 경계(꺼짐) – 끌면 켜집니다',
    'links Mitte':
        '왼쪽 가운데',
    'oben Mitte':
        '위쪽 가운데',
    'rastet an Mitte, Balken und anderen ein (Alt = frei)':
        '가운데, 여백, 다른 요소에 맞춰짐(Alt = 자유)',
    'rechts Mitte':
        '오른쪽 가운데',
    'unten Mitte':
        '아래쪽 가운데',
    '{name} entsperrt.':
        '{name} 잠금 해제됨.',
    '{name} gesperrt – bleibt beim Anordnen, wo es ist.':
        '{name} 잠김 – 배치 중에도 그 자리에 머뭅니다.',
    '{name} ist gesperrt – das Schloss in der Liste löst es':
        '{name}이(가) 잠겨 있습니다 – 목록의 자물쇠로 해제하세요',
    '{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü':
        '{name}: 끌기 = 이동 · 모서리 또는 Ctrl+휠 = 크기 · 오른쪽 클릭 = 메뉴',
    'Üblicher Platz':
        '기본 위치',
    '„Overlay testen“ zeigt die Karte sofort, mit „Anordnen“ ziehst du sie hin.':
        '‘오버레이 테스트’는 맵을 바로 보여 주며, ‘배치’로 그 위치에 끌어 놓을 수 있습니다.',
    'Nur die Vorschau: Liste und Einstellungen weg, die Navigation schmal – die ganze Fläche zum Anordnen. Esc oder nochmal klicken beendet es.':
        '미리 보기만: 목록과 설정을 치우고 탐색을 좁게 – 전체 영역을 배치에 사용합니다. Esc 또는 다른 클릭으로 끝냅니다.',
    'Englisch':
        '영어',
    'Deutsch':
        '독일어',
    'Französisch':
        '프랑스어',
    'Spanisch':
        '스페인어',
    'Spanisch (Mexiko)':
        '스페인어(멕시코)',
    'Italienisch':
        '이탈리아어',
    'Polnisch':
        '폴란드어',
    'Portugiesisch (Brasilien)':
        '포르투갈어(브라질)',
    'Türkisch':
        '튀르키예어',
    'Spielsprache selbst erkennen und anhaken':
        '게임 언어를 자동으로 감지해 선택',
    'Spielsprache {lang} erkannt (Banner „{text}“) – automatisch angehakt.':
        "게임 언어 {lang} 감지됨(배너 '{text}') – 자동으로 선택했습니다.",
    'Läuft DBD in einer Sprache, die hier nicht angehakt ist, und passt ein Map-Banner eindeutig zu einer Map in dieser Sprache, hakt Fog Scout sie selbst an – die Karte erscheint dann schon in derselben Runde. Nur am Rundenstart, nie mitten im Match.':
        'DBD가 여기서 선택하지 않은 언어로 실행 중이고 맵 배너가 그 언어의 맵과 명확히 일치하면 Fog Scout가 해당 언어를 자동으로 선택합니다. 맵은 같은 라운드에서 바로 표시됩니다. 라운드 시작 시에만 작동하며 매치 도중에는 작동하지 않습니다.',
}
