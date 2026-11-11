"""Russian texts (1.47): the German text of the code is the key, as in i18n_en.EN – a text missing here
shows in English (i18n.table). Made from the English texts; tests/test_i18n.py checks keys and placeholders."""
T = {
    'Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\nKurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden.':
        'Fog Scout уже запущен, но не отвечает (или как раз закрывается).\n\nПодождите немного и запустите снова. Если не поможет: завершите «{exe}» (Fog Scout) в Диспетчере задач на вкладке «Подробности».',
    'Fog Scout konnte nicht neu gestartet werden: Die alte Kopie läuft noch im Hintergrund.\n\nIm Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden und das Programm neu starten.':
        'Не удалось перезапустить Fog Scout: старая копия ещё работает в фоне.\n\nЗавершите «{exe}» (Fog Scout) в Диспетчере задач на вкладке «Подробности» и запустите программу снова.',
    'Start fehlgeschlagen:':
        'Ошибка запуска:',
    'Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt unverändert.':
        'До сих пор Fog Scout запускался через start.bat:\n{folder}\n\nПеренести настройки, раунды, данные матчей, резервные копии и свои изображения карт в установленную версию? Старая папка останется без изменений.',
    'Übernahme fehlgeschlagen: {error}':
        'Перенос не удался: {error}',
    'Kein Windows: Fenstersuche, Hotkeys und Click-Through sind nur unter Windows aktiv.':
        'Не Windows: поиск окна, горячие клавиши и прозрачность для кликов работают только в Windows.',
    'Bereit. {n} Maps geladen, Spielsprachen: {langs}.':
        'Готово. Загружено карт: {n}, языки игры: {langs}.',
    'Bildschirm {w}×{h} ohne schwarze Balken neben dem Spielbild: Systemwerte, „Heute“ und Musik im Spiel sind ausgeschaltet (sie lägen sonst auf dem Spielbild) – einschalten auf der Seite Overlay.':
        'Экран {w}×{h} без чёрных полос рядом с картинкой игры: системные данные, «Сегодня» и музыка в игре выключены (иначе они лежали бы на картинке игры) — включите их на странице «Оверлей».',
    'Automatisch (Windows-Sprache)':
        'Автоматически (язык Windows)',
    'Erkennung':
        'Распознавание',
    'Overlay':
        'Оверлей',
    'System':
        'Система',
    'Fehler':
        'Ошибка',
    'automatisch':
        'автоматически',
    'oben links':
        'вверху слева',
    'oben rechts':
        'вверху справа',
    'unten links':
        'внизу слева',
    'unten rechts':
        'внизу справа',
    'eigene Position':
        'своя позиция',
    'Karte ein/aus':
        'Карта вкл./выкл.',
    'Layout-Variante':
        'Вариант раскладки',
    'Bildschirm scannen':
        'Сканировать экран',
    'Vorherige Map':
        'Предыдущая карта',
    'Nächste Map':
        'Следующая карта',
    'Grösser':
        'Крупнее',
    'Kleiner':
        'Мельче',
    'Mit Maus verschieben':
        'Двигать мышью',
    'Noch keine Map':
        'Карты ещё нет',
    'Karte ausblenden':
        'Скрыть карту',
    'Karte einblenden':
        'Показать карту',
    'Scannen':
        'Сканировать',
    'Overlay testen':
        'Тест оверлея',
    'Test beenden':
        'Завершить тест',
    'Bild hinzufügen …':
        'Добавить изображение…',
    'Zuordnen …':
        'Назначить…',
    'Server':
        'Сервер',
    'Einstellungen':
        'Настройки',
    'Layout {n} von {total}':
        'Раскладка {n} из {total}',
    '(unsicher)':
        '(неуверенно)',
    'manuell gewählt':
        'выбрано вручную',
    'per Scan gefunden':
        'найдено сканированием',
    'Letzte Runde: {time}':
        'Последний раунд: {time}',
    'Unbekannte Map gelesen: „{text}“':
        'Прочитана неизвестная карта: «{text}»',
    'Im Menü – Karte pausiert ({map})':
        'В меню — карта на паузе ({map})',
    'Runde vorbei – wartet auf das nächste Match':
        'Раунд окончен — ожидание следующего матча',
    'Karte ausgeblendet ({map})':
        'Карта скрыта ({map})',
    'Wartet auf DBD':
        'Ожидание DBD',
    'DBD läuft – automatische Erkennung ist aus (Map von Hand wählen)':
        'DBD запущена — автоматическое распознавание выключено (выберите карту вручную)',
    'Wartet auf das nächste Match':
        'Ожидание следующего матча',
    'Simulation – wartet auf das Map-Banner':
        'Симуляция — ожидание баннера карты',
    'Im Match: {map}':
        'В матче: {map}',
    'Karte eingeblendet':
        'Карта показана',
    'Kartenbild hinzufügen …':
        'Добавить изображение карты…',
    'eigenes Bild für eine Map (Hintergrund wird entfernt)':
        'своё изображение для карты (фон удаляется)',
    'Eigene Bilder':
        'Свои изображения',
    'Position':
        'Позиция',
    'Zurücksetzen':
        'Сбросить',
    'Horizontal':
        'По горизонтали',
    'Vertikal':
        'По вертикали',
    'Fertig':
        'Готово',
    '0 % = links/oben, 100 % = rechts/unten':
        '0 % = слева/сверху, 100 % = справа/снизу',
    'Karte im schwarzen Rand halten':
        'Держать карту в чёрной полосе',
    'Darstellung':
        'Внешний вид',
    'Grösse':
        'Размер',
    'Karte anzeigen':
        'Показывать карту',
    'Karte im Overlay eingeblendet.':
        'Карта показана в оверлее.',
    'Karte im Overlay aus – es werden nur Timer, Ort und Ping angezeigt.':
        'Карта в оверлее выключена — показываются только таймер, место и пинг.',
    'nichts anzuzeigen':
        'нечего показывать',
    'Aus: Das Overlay zeigt nur Rundentimer, Serverregion und Ping – ohne Karte. Erkennung, Rundenende und Statistik laufen wie gewohnt.':
        'Выкл.: оверлей показывает только таймер раунда, регион сервера и пинг — без карты. Распознавание, конец раунда и статистика работают как обычно.',
    'Für diese Map zurücksetzen':
        'Сбросить для этой карты',
    'eigene Grösse {n} % (Hotkeys/Strg+Mausrad)':
        'свой размер {n} % (горячие клавиши/Ctrl+колесо)',
    'gedreht um {deg}°':
        'повёрнуто на {deg}°',
    'Killer':
        'Убийца',
    'Survivor':
        'Выживший',
    'Rolle':
        'Роль',
    'Rolle: {role}':
        'Роль: {role}',
    'Alle Rollen':
        'Все роли',
    'Custom Game':
        'Своя игра',
    'Custom Games':
        'Свои игры',
    'Farming':
        'Фарм',
    'Stil':
        'Стиль',
    'Original':
        'Оригинал',
    'Dunkel':
        'Тёмный',
    'Die Karten mit lila Boden, wie sie mitgeliefert werden – gilt auch im Spiel.':
        'Карты с фиолетовым полом, как в поставке — действует и в игре.',
    'Klassisch':
        'Классика',
    'Glas-Karten':
        'Стеклянные карточки',
    'Chips & Icons':
        'Чипы и значки',
    'Minimal Line':
        'Минимальная линия',
    'SYSTEM':
        'СИСТЕМА',
    'Farming an/aus':
        'Фарм вкл./выкл.',
    'Farming-Runden':
        'Фарм-раунды',
    'Runden ohne Crossplay als Farming zählen':
        'Считать раунды без кроссплея фармом',
    'Alle Runden auf':
        'Все раунды на',
    'Farming-Runden zählen in Statistik und Aufnahmen überall mit; das Häkchen „Farming ausblenden“ (bei den Filtern) hält sie heraus, der Reiter Statistik → Farming listet sie immer. Crossplay aus erkennt das Programm an der Weltkugel mit rotem Kreuz neben dem Lobby-Knopf; Runden auf der gewählten Region zählen immer als Farming, auch ältere. Einzelne Runden: „Farming an/aus“ unter „Letzte Runden“.':
        'Фарм-раунды учитываются везде в статистике и записях; флажок «Скрыть фарм» (рядом с фильтрами) исключает их, вкладка «Статистика → Фарм» всегда их показывает. Выключенный кроссплей считывается по глобусу с красным крестом рядом с кнопкой лобби; раунды в выбранном регионе всегда считаются фармом, в том числе старые. Отдельные раунды: «Фарм вкл./выкл.» в «Последних раундах».',
    '{map} ({when}) zählt jetzt als Farming-Runde.':
        '{map} ({when}) теперь считается фарм-раундом.',
    '{map} ({when}) zählt wieder als normale Runde.':
        '{map} ({when}) снова считается обычным раундом.',
    'Hinweis: Runden auf {region} zählen laut Einstellung weiter als Farming.':
        'Примечание: раунды в регионе {region} по настройке по-прежнему считаются фармом.',
    'Crossplay war aus – die Runde zählt als Farming-Runde.':
        'Кроссплей был выключен — раунд считается фарм-раундом.',
    'Crossplay war aus, die Lobby sah aus wie ein Custom Game – die Runde zählt als Farming-Runde, sobald die Stats-Seite sie als öffentliches Match zeigt.':
        'Кроссплей был выключен, лобби выглядело как своя игра — раунд будет считаться фарм-раундом, как только страница статистики покажет его как публичный матч.',
    '{off} von {n} Blicken mit Kreuz':
        'с крестом: {off} из {n} проверок',
    'letzter Blick':
        'последняя проверка',
    'Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.':
        'Кроссплей выключен ({looks}) — следующий раунд считается фарм-раундом.',
    'Crossplay ist an ({looks}) – keine Farming-Runde.':
        'Кроссплей включён ({looks}) — не фарм-раунд.',
    'Als Custom Game erkannt – die Runde zählt nicht als Farming (unter „Letzte Runden“ mit „Farming an/aus“ korrigierbar).':
        'Распознано как своя игра — раунд не считается фармом (исправить можно в «Последних раундах» кнопкой «Фарм вкл./выкл.»).',
    'Keine Lobby zur Runde ({why}) – sie zählt nicht als Farming.':
        'Нет лобби для этого раунда ({why}) — он не считается фармом.',
    'Lobby zu alt':
        'лобби слишком старое',
    'Lobby nicht gesehen':
        'лобби не замечено',
    'Diese Runde als Farming-Runde zählen bzw. wieder als normale Runde – Farming-Runden zählen überall mit, bis „Farming ausblenden“ sie heraushält; der Reiter „Farming“ listet sie immer. Runden auf der Farming-Region (Einstellungen → Match-Daten) bleiben Farming.':
        'Считать этот раунд фарм-раундом или снова обычным — фарм-раунды учитываются везде, пока «Скрыть фарм» их не исключит; вкладка «Фарм» всегда их показывает. Раунды в регионе фарма (Настройки → Данные матчей) остаются фармом.',
    'Farming ausblenden':
        'Скрыть фарм',
    'An: Farming-Runden (Crossplay aus, Farming-Region, Farming-Gegner) bleiben aus Statistik, Aufnahmen und Clips draussen – ein Schalter für alle drei. Aus: sie zählen wie jede andere Runde. Der Reiter Statistik → Farming zeigt sie immer.':
        'Вкл.: фарм-раунды (кроссплей выключен, регион фарма, партнёры по фарму) не попадают в статистику, записи и клипы — один переключатель для всех трёх. Выкл.: они учитываются как любой другой раунд. Вкладка «Статистика → Фарм» всегда их показывает.',
    'Zeigt die Lobby die Weltkugel mit rotem Kreuz (Crossplay aus), zählt die nächste Runde als Farming-Runde.':
        'Если в лобби виден глобус с красным крестом (кроссплей выключен), следующий раунд считается фарм-раундом.',
    'Custom Game – keine Wartezeit.':
        'Своя игра — без ожидания.',
    'Suche läuft: {time}':
        'Поиск: {time}',
    'Suche nach einem Match gestartet.':
        'Начат поиск матча.',
    'Lobby verlassen – sie zählt für keine Runde.':
        'Лобби покинуто — оно не относится ни к одному раунду.',
    'Suche abgebrochen.':
        'Поиск отменён.',
    'Lobby gefunden nach {time}{role}.':
        'Лобби найдено через {time}{role}.',
    'Lobby gefunden{role}.':
        'Лобби найдено{role}.',
    'Lobby nur kurz gesehen – Rolle und Crossplay von dort, ohne Wartezeit.':
        'Лобби было видно лишь мельком — роль и кроссплей взяты оттуда, без времени ожидания.',
    'Wartezeit {time}':
        'ожидание {time}',
    'Verbindung in dieser Runde: {n} × Aussetzer, längster {s} s.':
        'Связь в этом раунде: обрывов — {n}, самый долгий {s} с.',
    '{n}× Aussetzer':
        'обрывов: {n}×',
    'Ergebnisbildschirm (zweiter Blick): gespielt als {role}.':
        'Экран результатов (вторая проверка): сыграно за {role}.',
    'Ergebnisbildschirm: gespielt als {role}.':
        'Экран результатов: сыграно за {role}.',
    'Wartezeit':
        'Время ожидания',
    'Regionen':
        'Регионы',
    'Markierte Runde:':
        'Выбранный раунд:',
    'Benachrichtigungen':
        'Уведомления',
    'Runde auf {map} nicht gezählt: ihr Ende wurde nicht erkannt.':
        'Раунд на карте {map} не засчитан: его конец не распознан.',
    'Einstellungen exportieren …':
        'Экспорт настроек…',
    'Einstellungen importieren …':
        'Импорт настроек…',
    'Einstellungen exportieren':
        'Экспорт настроек',
    'Einstellungen importieren':
        'Импорт настроек',
    'Export fehlgeschlagen: {error}':
        'Ошибка экспорта: {error}',
    'Einstellungen gesichert: {path}':
        'Настройки сохранены: {path}',
    'Das ist keine Einstellungsdatei von Fog Scout ({error}).':
        'Это не файл настроек Fog Scout ({error}).',
    'Alle Einstellungen durch die aus der Datei ersetzen? Das Programm startet danach neu.':
        'Заменить все настройки настройками из файла? После этого программа перезапустится.',
    'Einstellungen importiert aus {path}.':
        'Настройки импортированы из {path}.',
    'Bitte das Programm jetzt neu starten.':
        'Перезапустите программу.',
    'Speichert alle Einstellungen in eine Datei: Hotkeys, Grösse und Drehung pro Map, eigene Map-Zuordnungen, Overlay, Regionen … Die Statistik (rounds.jsonl) gehört nicht dazu.':
        'Сохраняет все настройки в файл: горячие клавиши, размер и поворот для каждой карты, свои назначения карт, оверлей, регионы… Статистика (rounds.jsonl) сюда не входит.',
    'Lädt eine exportierte Einstellungsdatei und startet das Programm neu. Fehlende Werte (ältere Sicherung) bekommen ihren Standard.':
        'Загружает экспортированный файл настроек и перезапускает программу. Отсутствующие значения (старая копия) получают значения по умолчанию.',
    'Ton und Meldung, wenn eine Lobby gefunden wurde':
        'Звук и уведомление, когда лобби найдено',
    'Erinnern, wenn der Lobby-Countdown abläuft und READY noch nicht gedrückt ist':
        'Напомнить, если отсчёт лобби истекает, а READY ещё не нажато',
    'Nur wenn DBD nicht das aktive Fenster ist':
        'Только если DBD не активное окно',
    'Die Meldung erscheint unten rechts über allen Fenstern – auch bei „Nicht stören“ – und nimmt dem aktiven Fenster nicht den Fokus. Klick darauf schliesst sie.':
        'Уведомление появляется внизу справа поверх всех окон — даже в режиме «Не беспокоить» — и не забирает фокус у активного окна. Щелчок закрывает его.',
    'Meldung testen':
        'Тест уведомления',
    'Zeigt die Meldung und spielt den Ton – so siehst du, wo sie erscheint.':
        'Показывает уведомление и проигрывает звук — так вы увидите, где оно появляется.',
    'Lobby gefunden':
        'Лобби найдено',
    'nach {time}':
        'через {time}',
    'READY drücken.':
        'Нажмите READY.',
    'Lobby startet gleich':
        'Лобби скоро начнётся',
    'Noch {n} s – READY ist noch nicht gedrückt.':
        'Осталось {n} с — READY ещё не нажато.',
    'Lobby-Countdown läuft ab, READY ist noch nicht gedrückt.':
        'Отсчёт лобби истекает, READY не нажато.',
    'Ø Ping':
        'Ср. пинг',
    'Spielt einen Hinweiston und zeigt eine Windows-Meldung, sobald DBD eine Lobby gefunden hat – praktisch, wenn du während der Suche etwas anderes machst.':
        'Проигрывает звук и показывает уведомление Windows, как только DBD нашла лобби — удобно, если во время поиска вы заняты чем-то другим.',
    'Noch einmal melden, wenn der Countdown der Lobby unter 15 s fällt und du READY nicht gedrückt hast.':
        'Напомнить ещё раз, когда отсчёт лобби опустится ниже 15 с, а вы не нажали READY.',
    'Keine Meldung, solange DBD im Vordergrund ist – dann siehst du die Lobby ja selbst.':
        'Без уведомления, пока DBD на переднем плане — тогда вы и сами видите лобби.',
    'Bilanz der Sitzung zeigen, wenn DBD beendet wurde':
        'Показывать итоги сессии после закрытия DBD',
    'Etwa 15 s nachdem DBD geschlossen wurde: eine Meldung mit den Runden der Sitzung, der Spielzeit und – mit Match-Daten – Ø Kills, Entkommen und Bloodpoints. Steht auch im Log.':
        'Примерно через 15 с после закрытия DBD: уведомление с раундами сессии, временем игры и — при наличии данных матчей — средними убийствами, побегами и очками крови. Также в журнале.',
    'Sitzung beendet':
        'Сессия завершена',
    '1 Runde':
        '1 раунд',
    '{bp} BP':
        '{bp} BP',
    'Melden, wenn eine Runde keine Blutpunkte gebracht hat (Cap erreicht)':
        'Сообщать, если раунд не принёс очков крови (лимит достигнут)',
    'Fog Scout liest in der Lobby den Blutpunkte-Stand oben rechts. Ist er nach einer gezählten Runde derselbe wie davor, ist das Cap erreicht (normal 5 Millionen, nach Tome-Belohnungen auch mehr) – die Punkte der Runde sind verfallen. Ton und Meldung kommen auch, wenn DBD im Vordergrund ist; Custom Games zählen nicht.':
        'Fog Scout считывает баланс очков крови в лобби вверху справа. Если после засчитанного раунда он такой же, как до него, лимит достигнут (обычно 5 миллионов, больше после наград из архивов) — очки за раунд потеряны. Звук и уведомление приходят и тогда, когда DBD на переднем плане; свои игры не учитываются.',
    'Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte dieser Runde sind verfallen.':
        'Очки крови не изменились: {bp} до и после раунда — лимит достигнут, очки этого раунда потеряны.',
    'Blutpunkte-Cap erreicht':
        'Достигнут лимит очков крови',
    '{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die nächste Runde nichts.':
        '{bp} BP до и после раунда — потратьте их в паутине крови, иначе и следующий раунд ничего не принесёт.',
    'Blutpunkte: +{gain} in dieser Runde, Stand {bp}.':
        'Очки крови: +{gain} за этот раунд, баланс {bp}.',
    'Blutpunkte: Stand {bp} nach der Runde, vorher {before}.':
        'Очки крови: баланс {bp} после раунда, до него {before}.',
    'BP-Stand':
        'Баланс BP',
    'Aussetzer':
        'Обрывы',
    'Alles sichern (ZIP) …':
        'Сохранить всё (ZIP)…',
    'Aus Sicherung wiederherstellen (ZIP) …':
        'Восстановить из копии (ZIP)…',
    'Aus Sicherung wiederherstellen':
        'Восстановить из копии',
    'Führt eine Sicherung von „Alles sichern“ mit den jetzigen Daten zusammen: Runden, Match-Daten, Kartenbilder und Banner, die fehlen, kommen dazu – Vorhandenes bleibt, wie es ist. Zeigt vorher, was dazukommt. Die Einstellungen der Sicherung nur auf eigene Rückfrage.':
        'Объединяет копию из «Сохранить всё» с текущими данными: недостающие раунды, данные матчей, изображения карт и баннеры добавляются — то, что уже есть, остаётся как есть. Сначала показывает, что будет добавлено. Настройки из копии — только по отдельному вопросу.',
    'Während einer Runde nicht möglich – nach dem Rundenende noch einmal.':
        'Во время раунда невозможно — повторите после его окончания.',
    'Das ist keine Sicherung von Fog Scout ({error}).':
        'Это не резервная копия Fog Scout ({error}).',
    '{rounds} Runden, {lost} nicht gezählte Runden, {matches} Matches, {files} Bilder/Banner':
        'Раунды: {rounds}, не засчитанные раунды: {lost}, матчи: {matches}, изображения/баннеры: {files}',
    'Alles aus der Sicherung ist schon da – nichts hinzuzufügen.':
        'Всё из копии уже есть — добавлять нечего.',
    'Aus der Sicherung hinzufügen: {what}. Schon vorhanden (bleibt, wie es ist): {known}. Vorher kommt eine Kopie der Runden und Match-Daten nach backup/.':
        'Добавить из копии: {what}. Уже есть (останется как есть): {known}. Сначала копия раундов и данных матчей сохраняется в backup/.',
    'Zusammenführen':
        'Объединить',
    'Wiederherstellen fehlgeschlagen: {error}':
        'Ошибка восстановления: {error}',
    'Aus der Sicherung hinzugefügt: {what}.':
        'Добавлено из копии: {what}.',
    'Einstellungen der Sicherung nicht lesbar: {error}':
        'Не удаётся прочитать настройки из копии: {error}',
    'Die Sicherung enthält auch Einstellungen – übernehmen ersetzt die aktuellen.':
        'Копия содержит и настройки — их применение заменит текущие.',
    'Installation prüfen':
        'Проверить установку',
    'Installation wird geprüft …':
        'Проверка установки…',
    'Installation prüfen – Fehler: {line}':
        'Проверка установки — сбой: {line}',
    '{n} von {total} Prüfungen fehlgeschlagen – Einzelheiten im Log. Eine Neuinstallation (Setup erneut ausführen) behebt fehlende Dateien meist.':
        'Не пройдено проверок: {n} из {total} — подробности в журнале. Переустановка (повторный запуск установщика) обычно восстанавливает недостающие файлы.',
    'Alle {n} Prüfungen bestanden: {names}.':
        'Все проверки ({n}) пройдены: {names}.',
    'Installation prüfen: {text}':
        'Проверка установки: {text}',
    'Prüft, ob alles da ist und läuft: Programmdateien, Kartenbilder, Bibliotheken, alle Module, Telemetrie aus, Texterkennung, ffmpeg, Qt – derselbe Selbsttest wie bei jedem Build. Läuft als eigener Prozess, Ergebnis im Log.':
        'Проверяет, что всё на месте и работает: файлы программы, изображения карт, библиотеки, каждый модуль, отключённая телеметрия, распознавание текста, ffmpeg, Qt — та же самопроверка, что и при каждой сборке. Выполняется отдельным процессом, результат в журнале.',
    'Alles sichern':
        'Сохранить всё',
    'Gesichert: {n} Dateien in {path}':
        'Сохранено: файлов — {n}, в {path}',
    'Sichern fehlgeschlagen: {error}':
        'Ошибка сохранения: {error}',
    'Packt Runden, Match-Daten, die Einstellungen (ohne Passwörter und PC-eigene Werte), eigene Kartenbilder und den Banner-Korpus in eine ZIP-Datei – zum Aufbewahren oder für einen anderen PC. Aufnahmen und Logs bleiben draussen.':
        'Упаковывает раунды, данные матчей, настройки (без паролей и значений, привязанных к этому ПК), свои изображения карт и корпус баннеров в один ZIP-файл — для хранения или для другого ПК. Записи и журналы не входят.',
    'Spielmodus':
        'Режим игры',
    'Eigener Charakter':
        'Свой персонаж',
    'Eigene Perks':
        'Свои навыки',
    'JSON (für eigene Auswertungen)':
        'JSON (для своего анализа)',
    'Eine Liste mit einem Objekt je Runde, die Spaltentitel als Schlüssel – für eigene Auswertungen (Python, Tabellen, jq).':
        'Список с одним объектом на раунд, заголовки столбцов — ключи; для своего анализа (Python, таблицы, jq).',
    'Rolle für {map} ({when}) auf {role} geändert.':
        'Роль для {map} ({when}) изменена на {role}.',
    'Rolle konnte nicht gespeichert werden: {error}':
        'Не удалось сохранить роль: {error}',
    'Diese Runde als Killer-Runde zählen (falls die Erkennung falsch lag).':
        'Считать этот раунд раундом за убийцу (если распознавание ошиблось).',
    'Diese Runde als Survivor-Runde zählen (falls die Erkennung falsch lag).':
        'Считать этот раунд раундом за выжившего (если распознавание ошиблось).',
    'Diese Runde als Custom Game zählen – sie fliesst dann nicht in die Wartezeit ein.':
        'Считать этот раунд своей игрой — тогда он не учитывается во времени ожидания.',
    'Noch keine Wartezeiten in dieser Auswahl.':
        'В этой выборке пока нет времени ожидания.',
    'nach Wochentag':
        'по дням недели',
    'nach Uhrzeit':
        'по времени суток',
    'nach Region':
        'по регионам',
    'Wann/Wo':
        'Когда/где',
    'Ø Wartezeit':
        'Ср. ожидание',
    'Kürzeste':
        'Кратчайшее',
    'Warten':
        'Ожидание',
    'Uhr':
        'ч',
    'Montag':
        'Понедельник',
    'Dienstag':
        'Вторник',
    'Mittwoch':
        'Среда',
    'Donnerstag':
        'Четверг',
    'Freitag':
        'Пятница',
    'Samstag':
        'Суббота',
    'Sonntag':
        'Воскресенье',
    'Gemessen von „CANCEL“ (Suche läuft) bis zur gefundenen Lobby – nur wenn das Programm die Suche gesehen hat. Custom Games haben keine Wartezeit.':
        'Измеряется от «CANCEL» (идёт поиск) до найденного лобби — только если программа видела поиск. У своих игр нет времени ожидания.',
    'Map-Namen oben einfügen (wie bei den mitgelieferten Karten)':
        'Добавить название карты сверху (как у встроенных карт)',
    'Das Bild hat oben schon einen Namen – es wird keiner hinzugefügt.':
        'На изображении уже есть название сверху — новое не добавляется.',
    'Schreibt den Map-Namen weiss mit Schatten über die Karte, im Stil der mitgelieferten Karten. Hat das Bild oben schon einen Namen, passiert nichts. Beim Drehen bleibt der Name aufrecht.':
        'Пишет название карты белым с тенью над картой, в стиле встроенных карт. Если название сверху уже есть, ничего не происходит. При повороте карты название остаётся горизонтальным.',
    'Drehen':
        'Повернуть',
    'Karte drehen':
        'Повернуть карту',
    'Etage wechseln':
        'Сменить этаж',
    'Beide Etagen':
        'Оба этажа',
    'Etage {n} von {total}':
        'Этаж {n} из {total}',
    'Diese Map hat nur eine Etage.':
        'У этой карты только один этаж.',
    'Wechselt die Anzeige bei Karten mit Etagen (Midwich): beide untereinander → unten → oben → beide. Gilt bis zur nächsten Map.':
        'Переключает, что показывают карты с этажами (Midwich): оба друг под другом → нижний → верхний → оба. Действует до следующей карты.',
    'Etagen untereinander zeigen':
        'Показывать этажи друг под другом',
    'An: Karten mit Etagen (Midwich) zeigen alle Etagen untereinander, oben über unten – jede so groß wie eine normale Karte, soweit der Platz reicht. Aus: Sie starten mit der unteren Etage. Der Knopf „Etage“ oder der Hotkey schaltet jederzeit um.':
        'Вкл.: карты с этажами (Midwich) показывают все этажи друг под другом, верхний над нижним — каждый размером с обычную карту, насколько хватает места. Выкл.: начинают с нижнего этажа. Кнопка «Этаж» или горячая клавиша переключают в любой момент.',
    '{map} um {deg}° gedreht.':
        '{map} повёрнута на {deg}°.',
    'Drehung für {map} entfernt.':
        'Поворот для {map} удалён.',
    'Dreht die angezeigte Karte um 90° im Uhrzeigersinn (für jede Map gemerkt). Der Map-Name darüber bleibt aufrecht, die Zahlen in der Karte drehen sich mit.':
        'Поворачивает показанную карту на 90° по часовой стрелке (запоминается для каждой карты). Название карты над ней остаётся горизонтальным, цифры внутри карты поворачиваются вместе с ней.',
    'Eigene Grösse für {map} entfernt – es gilt wieder der Schieberegler.':
        'Свой размер для {map} удалён — снова действует ползунок.',
    'Entfernt eigene Grösse und Drehung der angezeigten Map – danach gilt wieder der Schieberegler für alle Maps.':
        'Удаляет свой размер и поворот показанной карты — снова действует ползунок для всех карт.',
    'Deckkraft':
        'Непрозрачность',
    'Nur zeigen, wenn DBD das aktive Fenster ist':
        'Показывать только когда DBD — активное окно',
    'Map-Namen über der Karte anzeigen':
        'Название карты над картой',
    'Rundentimer unter der Karte anzeigen':
        'Таймер раунда под картой',
    'Verbundenen Server unter der Karte':
        'Подключённый сервер под картой',
    'Transparenter Rand um die Karte':
        'Прозрачный край вокруг карты',
    'Map beim Match-Start automatisch erkennen':
        'Распознавать карту автоматически при начале матча',
    'Overlay ausblenden, sobald ich nicht mehr in der Runde bin':
        'Скрывать оверлей, как только я вышел из раунда',
    'erkennt Ergebnisbildschirm, Lobby/Menüs, Ladebildschirm und geschlossenes DBD':
        'распознаёт экран результатов, лобби/меню, экран загрузки и закрытие DBD',
    'Overlay pausieren, solange ein DBD-Menü offen ist':
        'Ставить оверлей на паузу, пока открыто меню DBD',
    'erkannt am sichtbaren Mauszeiger (ESC-Menü, Ergebnisbildschirm, Lobby)':
        'распознаётся по видимому указателю мыши (меню ESC, экран результатов, лобби)',
    'Spielsprache (Map-Namen)':
        'Язык игры (названия карт)',
    'Erweitert':
        'Дополнительно',
    'Erweitert (Fehlersuche)':
        'Дополнительно (поиск неполадок)',
    'Technik':
        'Технические',
    'Auch erkennen, wenn andere Fenster über DBD liegen':
        'Распознавать и тогда, когда DBD закрыта другими окнами',
    'Fensteraufnahme wie bei OBS, nur solange DBD im Hintergrund ist':
        'захват окна как в OBS, только пока DBD в фоне',
    'Scans/Sek.':
        'Сканов/с',
    'Rundenende-Erkennung: {state}':
        'Распознавание конца раунда: {state}',
    'Debug-Bilder speichern':
        'Сохранять отладочные изображения',
    'Banner jeder Erkennung für „Erkennung prüfen“ sammeln':
        'Сохранять баннер каждого распознавания для «Проверить распознавание»',
    '{n} Banner gesammelt':
        'Сохранено баннеров: {n}',
    '1 Banner gesammelt':
        'Сохранён 1 баннер',
    'letzte Prüfung: {hits} von {total} erkannt':
        'последняя проверка: распознано {hits} из {total}',
    'Erkennung prüfen':
        'Проверить распознавание',
    'Korpus exportieren …':
        'Экспорт корпуса…',
    'Korpus exportieren':
        'Экспорт корпуса',
    'Korpus-Ordner öffnen':
        'Открыть папку корпуса',
    'Noch keine Banner gesammelt – sie kommen mit jeder erkannten Map.':
        'Баннеров пока нет — они появляются с каждой распознанной картой.',
    'Erkennung prüfen: {n} Banner werden neu gelesen …':
        'Проверка распознавания: повторное чтение баннеров ({n})…',
    'Erkennung prüfen fehlgeschlagen: {error}':
        'Ошибка проверки распознавания: {error}',
    '{hits} von {total} Bannern wieder erkannt ({seconds} s).':
        'Снова распознано баннеров: {hits} из {total} ({seconds} с).',
    '{n} nicht lesbar.':
        'Нечитаемых: {n}.',
    'Erkennung prüfen: {text}':
        'Проверка распознавания: {text}',
    'Erkennung prüfen – {stamp}: erwartet {want}, gelesen „{read}“ → {got}':
        'Проверка распознавания — {stamp}: ожидалось {want}, прочитано «{read}» → {got}',
    'Die Treffer, die fehlen, stehen im Log.':
        'Нераспознанные баннеры указаны в журнале.',
    'Korpus exportiert: {n} Dateien nach {path}':
        'Корпус экспортирован: файлов — {n}, в {path}',
    'Korpus exportieren fehlgeschlagen: {error}':
        'Ошибка экспорта корпуса: {error}',
    'Speichert bei jeder erkannten Map den Ausschnitt um die Banner-Linie (Name und Realm) im Datenordner unter corpus/, höchstens 300 Stück – die Grundlage für „Erkennung prüfen“. Der Ausschnitt kann den linken HUD-Rand mit Spielernamen zeigen; er bleibt auf diesem PC.':
        'Сохраняет для каждой распознанной карты фрагмент вокруг линии баннера (название и мир) в папке данных в corpus/, не более 300 — основа для «Проверить распознавание». Фрагмент может показывать левый край HUD с именами игроков; он остаётся на этом ПК.',
    'Liest alle gesammelten Banner mit der Erkennung neu und zählt, wie viele wieder die gespeicherte Map ergeben – nach einem Update oder einer geänderten Spielsprache. Läuft im Hintergrund, Ergebnis im Log.':
        'Заново читает все сохранённые баннеры и считает, сколько из них снова дают сохранённую карту — после обновления или смены языка игры. Работает в фоне, результат в журнале.',
    'Packt alle gesammelten Banner mit ihren Angaben in eine ZIP-Datei – z. B. um sie für die Tests des Projekts weiterzugeben. Vorher die Bilder ansehen: sie können Spielernamen zeigen.':
        'Упаковывает все сохранённые баннеры со сведениями в ZIP-файл — например, чтобы передать их в тесты проекта. Сначала просмотрите изображения: на них могут быть имена игроков.',
    'Öffnet den Ordner corpus/ im Datenordner.':
        'Открывает папку corpus/ в папке данных.',
    'Bildschirm jetzt scannen':
        'Сканировать экран сейчас',
    'Diagnose kopieren':
        'Копировать диагностику',
    'Verbundener Spielserver':
        'Подключённый игровой сервер',
    'Serverregionen':
        'Регионы серверов',
    'DBD sucht Matches nur in den angehakten Regionen (über die Windows-hosts-Datei, das Spiel wird nicht verändert). Nach „Auswahl anwenden“ DBD neu starten.':
        'DBD ищет матчи только в отмеченных регионах (через файл hosts Windows, игра не изменяется). После «Применить выбор» перезапустите DBD.',
    'Region':
        'Регион',
    'hosts-Datei':
        'файл hosts',
    'Ping messen':
        'Измерить пинг',
    'Auswahl anwenden':
        'Применить выбор',
    'Alles freigeben':
        'Разрешить все',
    'Mit VPN unzuverlässig. Region-Tools sind von BHVR weder erlaubt noch verboten – auf eigene Verantwortung.':
        'С VPN ненадёжно. Инструменты выбора региона BHVR не разрешает и не запрещает — на ваш страх и риск.',
    'Warte auf Windows (Administratorrechte) …':
        'Ожидание Windows (права администратора)…',
    'Aus':
        'Выкл.',
    'Zeigt Region und Ping des Spielservers, auch im Overlay (braucht Administratorrechte).':
        'Показывает регион и пинг игрового сервера, в том числе в оверлее (нужны права администратора).',
    'DBD läuft mit {w}×{h}, kleiner als 1920×1080: die Erkennung ist unsicherer (vor allem Lobby-Knopf und Killername). Fenster größer ziehen oder „Fenster-Vollbild“ nutzen.':
        'DBD работает в {w}×{h}, меньше 1920×1080: распознавание менее надёжно (прежде всего кнопка лобби и имя убийцы). Увеличьте окно или используйте «Оконный полноэкранный».',
    'DBD-Fenster ist schmaler als 16:9 ({w}×{h}): diese Form ist ungetestet, Map- und Rundenende-Erkennung können danebenliegen. Am sichersten: 16:9 oder breiter.':
        'Окно DBD уже, чем 16:9 ({w}×{h}): такая форма не проверялась, распознавание карты и конца раунда может ошибаться. Надёжнее всего: 16:9 или шире.',
    'Verbunden mit: {server}':
        'Подключено к: {server}',
    'pausiert, bis DBD läuft':
        'пауза до запуска DBD',
    'Anzeige des Spielservers beendet.':
        'Показ игрового сервера остановлен.',
    'Spielserver-Anzeige: {error}':
        'Показ игрового сервера: {error}',
    'Spielserver-Anzeige läuft (liest nur Paketköpfe, keine Inhalte).':
        'Показ игрового сервера работает (читаются только заголовки пакетов, без содержимого).',
    'Spielserver-Anzeige pausiert – DBD läuft nicht (startet automatisch mit DBD).':
        'Показ игрового сервера на паузе — DBD не запущена (снова начнётся с DBD).',
    'Spielserver-Anzeige beendet: {error}':
        'Показ игрового сервера остановлен: {error}',
    ' – nicht in deiner Regionsauswahl':
        ' — не в выбранных вами регионах',
    'Verbunden mit Spielserver: {region}{note}.':
        'Подключено к игровому серверу: {region}{note}.',
    'hosts-Datei nicht lesbar: {error}':
        'Файл hosts не читается: {error}',
    'Aktiv: nur {regions} erlaubt.':
        'Активно: разрешены только {regions}.',
    '(keine)':
        '(нет)',
    'Keine eigene Auswahl aktiv, aber andere Einträge sperren Regionen.':
        'Своего выбора нет, но другие записи блокируют регионы.',
    'Keine Region gesperrt – DBD wählt selbst.':
        'Ни один регион не заблокирован — DBD выбирает сама.',
    'anderen Programmen':
        'других программ',
    ' Es gibt {n} Einträge von {who} für DBD-Server (werden beim Anwenden ersetzt).':
        ' Есть записи ({n}) от {who} для серверов DBD (при применении будут заменены).',
    'Serverregionen: {text}':
        'Регионы серверов: {text}',
    'Messe Ping zu den Serverregionen …':
        'Измерение пинга до регионов серверов…',
    'Ping fehlgeschlagen: {error}':
        'Ошибка пинга: {error}',
    'Am schnellsten: {list}.':
        'Быстрее всего: {list}.',
    'Keine Region hat geantwortet (Internet/Firewall/VPN?).':
        'Ни один регион не ответил (интернет/брандмауэр/VPN?).',
    'Bitte mindestens eine Region anhaken.':
        'Отметьте хотя бы один регион.',
    'Erlaubt bleiben: {names}.\n\nAlle anderen DBD-Serverregionen werden in der Windows-hosts-Datei gesperrt. Windows fragt gleich nach Administratorrechten.':
        'Разрешены: {names}.\n\nВсе остальные регионы серверов DBD блокируются в файле hosts Windows. Windows запросит права администратора.',
    '{n} vorhandene Einträge anderer Programme (z. B. Make Your Choice) für DBD-Server werden dabei entfernt.':
        'Существующие записи других программ (например, Make Your Choice) для серверов DBD будут удалены: {n}.',
    'Danach DBD neu starten, damit es wirkt.':
        'Затем перезапустите DBD, чтобы изменения вступили в силу.',
    'Serverregionen anwenden':
        'Применить регионы серверов',
    'Nur noch {names} erlaubt':
        'Разрешены только {names}',
    'Es ist nichts gesperrt.':
        'Ничего не заблокировано.',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen (auch die von Make Your Choice)?':
        'Удалить из файла hosts все блокировки регионов серверов DBD (включая блокировки Make Your Choice)?',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen?':
        'Удалить из файла hosts все блокировки регионов серверов DBD?',
    'Windows fragt gleich nach Administratorrechten. Danach DBD neu starten.':
        'Windows запросит права администратора. Затем перезапустите DBD.',
    'Serverregionen freigeben':
        'Разрешить регионы серверов',
    'Alle Regionen freigegeben':
        'Все регионы разрешены',
    'Serverregionen: {text}. DBD neu starten, damit es wirkt.':
        'Регионы серверов: {text}. Перезапустите DBD, чтобы изменения вступили в силу.',
    '{text}. DBD jetzt neu starten.':
        '{text}. Перезапустите DBD сейчас.',
    'Keine Änderung nötig.':
        'Изменений не требуется.',
    'unbekannter Fehler':
        'неизвестная ошибка',
    'Firewall-Regeln von Make Your Choice („Enforced“) gefunden – sie sperren Regionen unabhängig von der hosts-Datei. In Make Your Choice „Revert to Default“ drücken.':
        'Найдены правила брандмауэра Make Your Choice («Enforced») — они блокируют регионы независимо от файла hosts. Нажмите «Revert to Default» в Make Your Choice.',
    'Achtung: Firewall-Regeln von Make Your Choice aktiv (siehe Log).':
        'Внимание: активны правила брандмауэра Make Your Choice (см. журнал).',
    'Europa':
        'Европа',
    'Amerika':
        'Америка',
    'Asien':
        'Азия',
    'Ozeanien':
        'Океания',
    'frei':
        'разрешён',
    'gesperrt':
        'заблокирован',
    'gesperrt (fremd)':
        'заблокирован (другая программа)',
    'umgeleitet (fremd)':
        'перенаправлен (другая программа)',
    'Frankfurt':
        'Франкфурт',
    'Irland':
        'Ирландия',
    'London':
        'Лондон',
    'USA Ost (N. Virginia)':
        'США Восток (Сев. Вирджиния)',
    'USA Ost (Ohio)':
        'США Восток (Огайо)',
    'USA West (N. Kalifornien)':
        'США Запад (Сев. Калифорния)',
    'USA West (Oregon)':
        'США Запад (Орегон)',
    'Kanada (Zentral)':
        'Канада (Центр)',
    'Südamerika (São Paulo)':
        'Южная Америка (Сан-Паулу)',
    'Tokio':
        'Токио',
    'Seoul':
        'Сеул',
    'Mumbai':
        'Мумбаи',
    'Singapur':
        'Сингапур',
    'Hongkong':
        'Гонконг',
    'Sydney':
        'Сидней',
    'Name nicht auflösbar':
        'имя не удаётся разрешить',
    'Start mit Administratorrechten fehlgeschlagen (Fehler {code}).':
        'Не удалось запустить с правами администратора (ошибка {code}).',
    'Hilfsprogramm nicht gestartet.':
        'Вспомогательная программа не запущена.',
    'Das Hilfsprogramm hat kein Ergebnis geliefert (Code {code}).':
        'Вспомогательная программа не вернула результат (код {code}).',
    'Zeitüberschreitung beim Schreiben der hosts-Datei.':
        'Тайм-аут при записи файла hosts.',
    'Abgebrochen (keine Administratorrechte erteilt).':
        'Отменено (права администратора не предоставлены).',
    'Warte auf Match …':
        'Ожидание матча…',
    'Global':
        'Глобально',
    'keine Daten vom Mitschnitt':
        'нет данных от захвата',
    'Nur unter Windows verfügbar.':
        'Доступно только в Windows.',
    'Mitschnitt beendet (Code {code}).':
        'Захват завершён (код {code}).',
    'Fehler: {error}':
        'Ошибка: {error}',
    'Statistik':
        'Статистика',
    'Log':
        'Журнал',
    'Maps':
        'Карты',
    'Map':
        'Карта',
    'Runden':
        'Раунды',
    'Ø Dauer':
        'Ср. длительность',
    'Letzte Runden':
        'Последние раунды',
    'Gesamter Zeitraum':
        'За всё время',
    'Heute':
        'Сегодня',
    'Diese Woche':
        'Эта неделя',
    'Dieser Monat':
        'Этот месяц',
    'Dieses Jahr':
        'Этот год',
    'Alle Regionen':
        'Все регионы',
    'Alle Killer':
        'Все убийцы',
    'Häufigste Map':
        'Самая частая карта',
    'Der markierte Name (Skin oder neuer Killer) zählt ab jetzt als der gewählte Killer – auch in allen bisherigen Runden.':
        'Выбранное имя (облик или новый убийца) отныне считается выбранным убийцей — и во всех прошлых раундах.',
    'Entfernt alle eigenen Killer-Zuordnungen; die Namen erscheinen wieder so, wie sie gelesen wurden.':
        'Удаляет все свои назначения убийц; имена снова показываются так, как были прочитаны.',
    'Zuordnen':
        'Назначить',
    'Warte auf Map':
        'Ожидание карты',
    'Solange DBD läuft und keine Karte eingeblendet ist, zeigt das Overlay eine kleine Karte: „Warte auf Map“, darunter Suche/Lobby (z. B. „Suche läuft: 02:13 · Nurse“) oder die letzte Runde. Gilt nicht, wenn du die Karte selbst ausgeblendet hast.':
        'Пока DBD работает и карта не показана, оверлей показывает маленькую карточку: «Ожидание карты», под ней поиск/лобби (например, «Поиск: 02:13 · Nurse») или последний раунд. Не тогда, когда вы сами скрыли карту.',
    'Ohne Karte: „Warte auf Map“ und Lobby-Status anzeigen':
        'Без карты: показывать «Ожидание карты» и состояние лобби',
    'Killer der Runde:':
        'Убийца раунда:',
    'Killer setzen':
        'Задать убийцу',
    'Notiz zum Killer:':
        'Заметка об убийце:',
    'Um diese Tageszeit ({span} Uhr) am schnellsten: {region} – Wartezeit {wait} (Median), {n} Runden':
        'Быстрее всего в это время суток ({span} ч): {region} — ожидание {wait} (медиана), раунды: {n}',
    'Ø {ping} ms':
        'Ср. {ping} мс',
    'danach {region} ({wait})':
        'затем {region} ({wait})',
    'Notiz speichern':
        'Сохранить заметку',
    'Notiz zu {killer} gespeichert.':
        'Заметка о {killer} сохранена.',
    'Notiz zu {killer} gelöscht.':
        'Заметка о {killer} удалена.',
    'Eigene Notiz zum markierten Killer, z. B. „Lithe, nicht vaulten“. Erscheint im Spiel unter der Map-Notiz, sobald dieser Killer in der Runde ist (eigener Killer oder, als Survivor, der aus der Lobby). Leer speichern löscht sie.':
        'Своя заметка о выбранном убийце, например «Ловкий, не перепрыгивать». Показывается в игре под заметкой карты, как только этот убийца в раунде (ваш убийца или, если вы выживший, тот, что из лобби). Сохранение пустой заметки удаляет её.',
    'Killer konnte nicht gespeichert werden: {error}':
        'Не удалось сохранить убийцу: {error}',
    'Killer für {map} ({when}) auf {killer} gesetzt.':
        'Убийца для {map} ({when}) задан: {killer}.',
    'Map der Runde:':
        'Карта раунда:',
    'Setzt die Map nur für die markierten Runden – wenn das Banner falsch gelesen wurde. Statistik, eigener Rekord und die Verknüpfung mit den Match-Daten folgen; die Aufnahme behält ihren Namen.':
        'Задаёт карту только для выбранных раундов — если баннер прочитан неверно. Статистика, свои итоги и связь с данными матчей следуют за ней; запись сохраняет своё имя.',
    'Map setzen':
        'Задать карту',
    'Map konnte nicht gespeichert werden: {error}':
        'Не удалось сохранить карту: {error}',
    'Map der Runde vom {when} auf {map} gesetzt.':
        'Карта раунда от {when} задана: {map}.',
    'Setzt den Killer nur für die markierte Runde und zählt sie als Killer-Runde – z. B. wenn sie fälschlich als Survivor gezählt wurde oder der Name falsch gelesen wurde.':
        'Задаёт убийцу только для выбранного раунда и считает его раундом за убийцу — например, если он ошибочно засчитан как раунд за выжившего или имя прочитано неверно.',
    'Zuordnungen löschen':
        'Удалить назначения',
    '„{name}“ zählt jetzt als {killer}.':
        '«{name}» теперь считается как {killer}.',
    'Alle eigenen Killer-Zuordnungen löschen?':
        'Удалить все свои назначения убийц?',
    'Killer-Zuordnungen gelöscht.':
        'Назначения убийц удалены.',
    'ohne Region':
        'нет региона',
    'Anteil':
        'Доля',
    'Region nur bekannt, wenn im Tab Server „Verbundener Spielserver“ an war.':
        'Регион известен, только если на вкладке «Сервер» был включён «Подключённый игровой сервер».',
    'Wann':
        'Когда',
    'Dauer':
        'Длительность',
    'Alle Runden löschen …':
        'Удалить все раунды…',
    'Runde löschen':
        'Удалить раунд',
    'Ø {kills} Kills · {n} Runden':
        'Ср. {kills} убийств · раунды: {n}',
    'Killer: Ø {kills} Kills, {four}× 4K ({n})':
        'Убийца: ср. {kills} убийств, 4K: {four}× ({n})',
    'Survivor: {share} entkommen ({n})':
        'Выживший: сбежал в {share} ({n})',
    '{share} entkommen · {n} Runden':
        'побеги: {share} · раунды: {n}',
    'Eigene Bilanz unter dem Timer':
        'Свои итоги под таймером',
    'Eigene Notiz unter dem Timer':
        'Своя заметка под таймером',
    'Zeigt deine eigene Notiz zur Map unter dem Rundentimer – geschrieben auf der Seite Maps (Map anklicken oder Rechtsklick → „Notiz bearbeiten …“), höchstens vier Zeilen.':
        'Показывает вашу заметку о карте под таймером раунда — пишется на странице «Карты» (щёлкните карту или правой кнопкой → «Изменить заметку…»), не более четырёх строк.',
    'Deine Notiz zu dieser Map – wird beim Tippen gespeichert und im Spiel unter dem Timer gezeigt (höchstens vier Zeilen). Leer = keine Notiz.':
        'Ваша заметка об этой карте — сохраняется по мере ввода и показывается в игре под таймером (не более четырёх строк). Пусто = без заметки.',
    'Eigene Notiz (im Spiel unter dem Timer)':
        'Своя заметка (в игре под таймером)',
    'z. B. Shack links vom Main, Gen im Keller …':
        'например, хижина слева от главного здания, генератор в подвале…',
    'Notiz bearbeiten …':
        'Изменить заметку…',
    'Map-Stile':
        'Стили карт',
    'Alle auf einmal':
        'Все сразу',
    'Kartenstile für {map} werden im Hintergrund erstellt.':
        'Стили карты {map} создаются в фоне.',
    'Kartenstil {style} für {map} wird im Hintergrund erstellt.':
        'Стиль {style} карты {map} создаётся в фоне.',
    'Eigene Notiz':
        'Своя заметка',
    'Eigene Notiz: {note}':
        'Своя заметка: {note}',
    'Zeigt unter dem Rundentimer, wie es dir auf dieser Map bisher ging: als Killer Ø Kills, als Survivor den Anteil Escapes – aus den Runden mit Daten der Stats-Seite, ab 3 Runden.':
        'Показывает под таймером раунда ваши успехи на этой карте: средние убийства за убийцу, долю побегов за выжившего — по раундам с данными страницы статистики, начиная с 3 раундов.',
    'Entfernt die markierte Runde aus der Statistik – z. B. eine Map, die mitten im Match falsch erkannt wurde. Fragt vorher nach.':
        'Удаляет выбранный раунд из статистики — например, если карта прочитана неверно посреди матча. Сначала спрашивает.',
    'Runde {what} aus der Statistik löschen?':
        'Удалить раунд {what} из статистики?',
    'Runde konnte nicht gelöscht werden: {error}':
        'Не удалось удалить раунд: {error}',
    'Runde gelöscht: {map} ({when}).':
        'Раунд удалён: {map} ({when}).',
    'Noch keine Runden gespeichert.':
        'Сохранённых раундов пока нет.',
    'Alle Runden löschen':
        'Удалить все раунды',
    'Alle gespeicherten Runden löschen? Vorher wird eine Kopie in {folder}/ angelegt.':
        'Удалить все сохранённые раунды? Сначала копия сохраняется в {folder}/.',
    'Es sind keine Runden gespeichert.':
        'Сохранённых раундов нет.',
    'Die Kopie in {folder}/ konnte nicht angelegt werden – die Runden bleiben gespeichert.':
        'Не удалось создать копию в {folder}/ — раунды остаются сохранёнными.',
    'Nicht angewendet – 1 Änderung. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        'Не применено — 1 изменение. «Применить выбор» применит его; затем перезапустите DBD.',
    'Nicht angewendet – {n} Änderungen. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        'Не применено — изменений: {n}. «Применить выбор» применит их; затем перезапустите DBD.',
    'Öffnet die markierten Runden bzw. Clips nacheinander im grossen Editor – als eine Montage (mehrere markieren: Strg- oder Umschalt-Klick).':
        'Открывает выбранные раунды или клипы друг за другом в большом редакторе — как один монтаж (выбрать несколько: Ctrl или Shift + щелчок).',
    'Ursache: {cause}':
        'Причина: {cause}',
    'Keine Region angehakt – für „Auswahl anwenden“ mindestens eine anhaken.':
        'Ни один регион не отмечен — отметьте хотя бы один для «Применить выбор».',
    'Anwenden':
        'Применить',
    'Freigeben':
        'Разблокировать',
    'Importieren':
        'Импорт',
    'Markieren':
        'Отметить',
    'Trotzdem beenden':
        'Всё равно выйти',
    'Rundenverlauf gelöscht.':
        'История раундов удалена.',
    'Löscht alle gespeicherten Runden (Datei rounds.jsonl) – nach einer Rückfrage, vorher kommt eine Kopie in den Ordner backup.':
        'Удаляет все сохранённые раунды (файл rounds.jsonl) — после вопроса; сначала копия сохраняется в папку резервных копий.',
    'Anzeigen:':
        'Показать:',
    'Leeren':
        'Очистить',
    'Log-Datei öffnen':
        'Открыть файл журнала',
    'Sprache und Darstellung':
        'Язык и внешний вид',
    'Wirkt nach dem nächsten Start des Programms.':
        'Вступит в силу при следующем запуске программы.',
    'Sprache geändert – wirkt nach dem nächsten Start des Programms.':
        'Язык изменён — вступит в силу при следующем запуске программы.',
    'Dark Mode':
        'Тёмный режим',
    'Hotkeys':
        'Горячие клавиши',
    'Standard':
        'По умолчанию',
    'Zum Ändern anklicken und die neue Tastenkombination drücken.':
        'Щёлкните, чтобы изменить, затем нажмите новое сочетание клавиш.',
    'Start und Infobereich':
        'Запуск и область уведомлений',
    'Beim Minimieren in den Infobereich':
        'Сворачивать в область уведомлений',
    'Mit Windows starten':
        'Запускать вместе с Windows',
    'Updates':
        'Обновления',
    'Beim Start Updates installieren':
        'Устанавливать обновления при запуске',
    'nur über start.bat bzw. die Desktop-Verknüpfung; eigene Änderungen werden nie überschrieben':
        'только через start.bat или ярлык на рабочем столе; ваши изменения никогда не перезаписываются',
    'Eigene Map-Zuordnungen':
        'Свои назначения карт',
    'Jetzt nach Updates suchen':
        'Проверить обновления',
    'Aktualisieren und neu starten':
        'Обновить и перезапустить',
    'Suche nach Updates …':
        'Проверка обновлений…',
    'Beim Start nach Updates suchen':
        'Проверять обновления при запуске',
    'Laden und Installieren nur nach deiner Bestätigung; das Setup wird per SHA-256 geprüft':
        'загружается и устанавливается только после вашего подтверждения; установщик проверяется по SHA-256',
    'Update-Prüfung fehlgeschlagen: {error}':
        'Ошибка проверки обновлений: {error}',
    'Kein Update – Version {version} (Build {build}) ist aktuell.':
        'Обновлений нет — версия {version} (сборка {build}) актуальна.',
    'Update verfügbar: {old} → {new} (Build {build}).':
        'Доступно обновление: {old} → {new} (сборка {build}).',
    'Lade Update …':
        'Загрузка обновления…',
    'GitHub antwortet gerade nicht (HTTP {code}) – bitte in einigen Minuten erneut versuchen.':
        'GitHub сейчас не отвечает (HTTP {code}) — повторите через несколько минут.',
    'Keine Antwort von GitHub (Zeitüberschreitung/Verbindung) – bitte später erneut versuchen.':
        'Нет ответа от GitHub (тайм-аут/соединение) — повторите позже.',
    'GitHub antwortet nicht – neuer Versuch {n} von {total} …':
        'GitHub не отвечает — попытка {n} из {total}…',
    'Lade Update … {pct} %':
        'Загрузка обновления… {pct} %',
    'Update nicht geladen: {error}':
        'Обновление не загружено: {error}',
    'Update {version} (Build {build}) geladen und geprüft.':
        'Обновление {version} (сборка {build}) загружено и проверено.',
    'Update installieren':
        'Установить обновление',
    'Fog Scout {version} (Build {build}) ist geladen und per SHA-256 geprüft. Jetzt installieren? Das Programm schliesst sich und startet danach neu.':
        'Fog Scout {version} (сборка {build}) загружен и проверен по SHA-256. Установить сейчас? Программа закроется и затем запустится снова.',
    'Installieren':
        'Установить',
    'Update gesperrt: eine Runde läuft oder ein Clip wird gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Обновление заблокировано: идёт раунд или сохраняется клип. Потом снова нажмите «Обновить и перезапустить».',
    'Programm schliesst sich und installiert das Update …':
        'Программа закрывается и устанавливает обновление…',
    'Das Update wurde nicht gestartet: Die Setup-Datei hat sich seit dem Download verändert oder fehlt. Bitte das Update noch einmal laden.':
        'Обновление не запущено: файл установщика изменился после загрузки или отсутствует. Загрузите обновление ещё раз.',
    'Das Update wurde nicht gestartet: Die Setup-Datei liess sich nicht sicher bereitstellen ({error}). Bitte das Update noch einmal laden.':
        'Обновление не запущено: файл установщика не удалось безопасно разместить ({error}). Загрузите обновление снова.',
    'Das Setup konnte nicht gestartet werden (Abfrage nach Administratorrechten abgebrochen?). Erneut versuchen oder das Setup selbst starten:\n{path}':
        'Не удалось запустить установщик (запрос администратора отменён?). Повторите или запустите установщик сами:\n{path}',
    'Neustart nicht möglich: {error}':
        'Перезапуск невозможен: {error}',
    'Nur unter Windows: bitte das Programm über start.bat neu starten.':
        'Только Windows: перезапустите программу через start.bat.',
    'Programm startet neu und installiert das Update …':
        'Программа перезапускается и устанавливает обновление…',
    'Fragt GitHub, ob es eine neue Version gibt (nur bei diesem Klick). Installiert wird erst mit „Aktualisieren und neu starten“.':
        'Спрашивает GitHub, есть ли новая версия (только по этому щелчку). Устанавливается она только кнопкой «Обновить и перезапустить».',
    'Beendet das Programm und startet es über start.bat neu – dabei wird das Update installiert. Die installierte Version lädt das Setup, prüft es per SHA-256 und fragt vor dem Installieren.':
        'Закрывает программу и снова запускает её через start.bat — который устанавливает обновление. Установленная версия загружает установщик, проверяет его по SHA-256 и спрашивает перед установкой.',
    'Fragt nach jedem Start einmal GitHub, ob es ein neues Release gibt. Geladen und installiert wird nur nach deinem Klick und einer Rückfrage.':
        'После каждого запуска один раз спрашивает GitHub, есть ли новый выпуск. Загрузка и установка — только после вашего щелчка и подтверждения.',
    'Alle löschen':
        'Удалить все',
    'Datenordner öffnen':
        'Открыть папку данных',
    'Karten-Ordner öffnen':
        'Открыть папку карт',
    'liest nur Bildschirmpixel, sendet keine Eingaben ans Spiel.':
        'читает только пиксели экрана, не отправляет в игру никакого ввода.',
    'Inoffizielles Fan-Tool, nicht von Behaviour Interactive genehmigt – Nutzung auf eigene Gefahr (siehe LICENSE).':
        'Неофициальный фанатский инструмент, не одобрен Behaviour Interactive — используйте на свой риск (см. LICENSE).',
    'Kartenbilder: Lethia (hens333.com/callouts, mit Erlaubnis von Hens) · Map-Namen: Luca Fontanot (DBD Map Overlay).':
        'Изображения карт: Lethia (hens333.com/callouts, с разрешения Hens) · названия карт: Luca Fontanot (DBD Map Overlay).',
    'Keine. Unbekannte Map-Namen lassen sich nach dem Match im Hauptfenster zuordnen.':
        'Нет. Неизвестные названия карт можно назначить в главном окне после матча.',
    'Eigene Zuordnungen':
        'Свои назначения',
    'Alle eigenen Map-Zuordnungen löschen?':
        'Удалить все свои назначения карт?',
    'Eigene Map-Zuordnungen gelöscht.':
        'Свои назначения карт удалены.',
    'Spielsprachen: {langs}':
        'Языки игры: {langs}',
    'Änderbar, wenn das Programm über die Desktop-Verknüpfung gestartet wurde (verknuepfung_erstellen.bat einmal ausführen).':
        'Можно изменить, если программа запущена через ярлык на рабочем столе (один раз запустите verknuepfung_erstellen.bat).',
    'Wird eingerichtet …':
        'Настройка…',
    'Startet ab jetzt mit Windows im Infobereich.':
        'Отныне запускается вместе с Windows в области уведомлений.',
    'Startet nicht mehr mit Windows.':
        'Больше не запускается вместе с Windows.',
    'Startet ab jetzt mit Windows im Infobereich (abschaltbar unter Einstellungen → Start und Infobereich).':
        'Отныне запускается вместе с Windows в области уведомлений (отключается в «Настройки → Запуск и область уведомлений»).',
    'Autostart mit Windows fehlgeschlagen: {error}':
        'Не удалось настроить запуск вместе с Windows: {error}',
    'Fehlgeschlagen: {error}':
        'Ошибка: {error}',
    'Nur unter Windows.':
        'Только Windows.',
    'Tipp: Fog Scout über die Verknüpfung im Startmenü starten – dann läuft es ohne Windows-Abfrage mit den nötigen Rechten.':
        'Совет: запускайте Fog Scout ярлыком из меню «Пуск» — тогда он работает с нужными правами, без запроса Windows.',
    'Änderbar, wenn das Programm über die Verknüpfung im Startmenü gestartet wurde.':
        'Можно изменить, если программа запущена ярлыком из меню «Пуск».',
    'Tipp: Einmal als Administrator starten (Rechtsklick auf start.bat → „Als Administrator ausführen“) – dann richtet das Programm die Desktop-Verknüpfung ein, die künftig ohne Windows-Abfrage startet.':
        'Совет: один раз запустите от имени администратора (правой кнопкой по start.bat → «Запуск от имени администратора») — программа создаст ярлык на рабочем столе, который в дальнейшем запускает её без запроса Windows.',
    'Desktop-Verknüpfung eingerichtet/aktualisiert: startet ab jetzt ohne Windows-Abfrage.':
        'Ярлык на рабочем столе создан/обновлён: отныне запуск без запроса Windows.',
    'Einrichtung der Verknüpfung fehlgeschlagen: {error}':
        'Не удалось создать ярлык: {error}',
    'Verknüpfung erstellt: {path}':
        'Ярлык создан: {path}',
    'Aufgabe konnte nicht angelegt werden: {error}':
        'Не удалось создать задачу планировщика: {error}',
    'Verknüpfung konnte nicht angelegt werden: {error}':
        'Не удалось создать ярлык: {error}',
    '(Autostart nicht erneuert: {error})':
        '(автозапуск не обновлён: {error})',
    'Symbol im Infobereich nicht verfügbar ({error}) – Minimieren wie gewohnt.':
        'Значок в области уведомлений недоступен ({error}) — сворачивание работает как обычно.',
    'Öffnen nur unter Windows: {path}':
        'Открытие работает только в Windows: {path}',
    'Kann {path} nicht öffnen: {error}':
        'Не удаётся открыть {path}: {error}',
    'Fenster öffnen':
        'Открыть окно',
    'Beenden':
        'Выход',
    'Hotkey: {keys}':
        'Горячая клавиша: {keys}',
    'Hotkey {keys} ({action}) nicht verfügbar: {why}.':
        'Горячая клавиша {keys} ({action}) недоступна: {why}.',
    '{n} Hotkey(s) nicht verfügbar – siehe Log.':
        'Недоступно горячих клавиш: {n} — см. журнал.',
    '– aus –':
        '– выкл. –',
    'Tasten drücken …':
        'Нажмите клавиши…',
    'Neue Kombination drücken – Esc bricht ab, Entf schaltet den Hotkey aus.':
        'Нажмите новое сочетание — Esc отменяет, Delete отключает горячую клавишу.',
    '{keys} ist schon „{action}“ – andere wählen.':
        '{keys} уже занято: «{action}» — выберите другое.',
    'aus':
        'выкл.',
    'an':
        'вкл.',
    'Hotkey {action}: {keys}.':
        'Горячая клавиша «{action}»: {keys}.',
    'Standard-Hotkeys wiederhergestellt.':
        'Горячие клавиши по умолчанию восстановлены.',
    'Strg':
        'Ctrl',
    'Taste „{key}“ geht nicht als Hotkey':
        'Клавишу «{key}» нельзя использовать как горячую',
    'Bitte mit Strg und/oder Alt kombinieren':
        'Сочетайте с Ctrl и/или Alt',
    'schon von einem anderen Programm belegt':
        'уже используется другой программой',
    'Für „{map}“ gibt es kein Bild.':
        'Для «{map}» нет изображения.',
    'Bild konnte nicht geladen werden: {path} ({error})':
        'Не удалось загрузить изображение: {path} ({error})',
    'Map gewählt: {map}':
        'Выбрана карта: {map}',
    'Noch keine Map gewählt.':
        'Карта ещё не выбрана.',
    'Overlay eingeblendet.':
        'Оверлей показан.',
    'Overlay ausgeblendet.':
        'Оверлей скрыт.',
    '„{map}“ hat nur ein Layout.':
        'У «{map}» только одна раскладка.',
    'Layout manuell gewechselt':
        'раскладка изменена вручную',
    'Scanne den Bildschirm nach Map- oder Realm-Namen …':
        'Поиск названий карт или миров на экране…',
    'Testanzeige':
        'тестовый показ',
    'Test: Overlay 10 s lang an seiner normalen Position, mit Systemwerten, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – nochmal drücken beendet den Test.':
        'Тест: оверлей на 10 с в обычном месте, с системными данными, «Сегодня» и музыкой (примерные значения, если данных нет) — нажмите снова, чтобы завершить тест.',
    'Links':
        'Слева',
    'Mittig':
        'По центру',
    'Rechts':
        'Справа',
    'Im Balken':
        'В полосе',
    'Abstand':
        'Отступ',
    'Zeile CPU (Temperatur, Last)':
        'Строка CPU (температура, нагрузка)',
    'Zeile GPU (Temperatur, Last)':
        'Строка GPU (температура, нагрузка)',
    'Zeile Hotspot / GPU-Speicher (HWiNFO)':
        'Строка хотспот / память GPU (HWiNFO)',
    'Zeile VRAM':
        'Строка VRAM',
    'Zeile RAM':
        'Строка RAM',
    'Zeile in den Systemwerten an/aus. Die Warnungen „CPU/GPU DROSSELT“ erscheinen immer.':
        'Строка системных данных вкл./выкл. Предупреждения «ТРОТТЛИНГ CPU/GPU» показываются всегда.',
    'Zeile in den Systemwerten an/aus – Hotspot und Memory Junction kommen nur mit HWiNFO.':
        'Строка системных данных вкл./выкл. — хотспот и температура памяти доступны только с HWiNFO.',
    'Zeile in den Systemwerten an/aus.':
        'Строка системных данных вкл./выкл.',
    'Test beendet.':
        'Тест завершён.',
    'Diagnose in die Zwischenablage kopiert (auch als diagnose.txt gespeichert).':
        'Диагностика скопирована в буфер обмена (также сохранена как diagnose.txt).',
    'Alle Elemente mit der Maus ziehen (im Spiel oder in der Vorschau): Karte, Infos, Systemwerte, Heute, Eingaben, Musik. Rechtsklick auf ein Element = Menü (Ausblenden, Position zurücksetzen, Sperren), Strg+Mausrad = Grösse. Danach „Fertig“ oder Hotkey.':
        'Перетаскивайте любой элемент мышью (в игре или в предпросмотре): карта, сведения, системные данные, «Сегодня», ввод, музыка. Правый щелчок по элементу = меню (скрыть, сбросить позицию, закрепить), Ctrl+колесо мыши = размер. Затем «Готово» или горячая клавиша.',
    '{name} wieder an seinem üblichen Platz.':
        '{name} снова на обычном месте.',
    'Karte':
        'Карта',
    'Systemwerte':
        'Системные данные',
    'Musik':
        'Музыка',
    'Eingaben':
        'Ввод',
    'Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = Grösse, Rechtsklick = Menü':
        'Перемещение включено — тяните (с привязкой, Alt = свободно), стрелки = точно, угол/Ctrl+колесо = размер, правый щелчок = меню',
    'Position zurücksetzen':
        'Сбросить позицию',
    'Rückgängig':
        'Отменить',
    'Karte darf grösser als der Balken werden':
        'Карта может быть больше полосы',
    'Karte füllt den Balken aus':
        'Карта заполняет полосу',
    'Erlaubt jede Kartengrösse: Ist die Karte breiter als der schwarze Balken, bleibt sie an dessen Aussenrand und ragt ins Spielbild. Aus: Die Karte wird nie breiter als der Balken (auf 3440×1440 etwa 31 % der Bildhöhe).':
        'Разрешает любой размер карты: если карта шире чёрной полосы, она остаётся у внешнего края полосы и заходит на картинку игры. Выкл.: карта никогда не шире полосы (около 31 % высоты при 3440×1440).',
    'Die Karte wird so gross, dass sie den schwarzen Balken von links bis rechts ausfüllt (bis auf den Abstand zum Rand); der Grössen-Regler gilt dann nicht. Eine hohe Karte stoppt an der Bildhöhe.':
        'Карта растёт, пока не заполнит чёрную полосу слева направо (кроме отступа от края); ползунок размера тогда не действует. Высокая карта останавливается на высоте картинки.',
    'Nimmt die letzte Änderung an Position oder Grösse zurück (Karte, Systemwerte, Musik) – auch mit Strg+Z auf dieser Seite. Ein ganzes Ziehen zählt als ein Schritt.':
        'Отменяет последнее изменение места или размера (карта, системные данные, музыка) — на этой странице также Ctrl+Z. Всё перетаскивание считается одним шагом.',
    'Merkt Position und Grösse aller Elemente getrennt für jede Grösse des DBD-Fensters (z. B. Vollbild 3440×1440 und ein kleineres Fenster) und lädt sie automatisch, sobald DBD in dieser Grösse läuft.':
        'Запоминает место и размер каждого элемента отдельно для каждого размера окна DBD (например, полный экран 3440×1440 и меньшее окно) и сам загружает их, как только DBD работает в этом размере.',
    'Nichts rückgängig zu machen.':
        'Нечего отменять.',
    'Position/Grösse rückgängig gemacht.':
        'Место/размер отменены.',
    'Position und Grösse je DBD-Fenstergrösse merken':
        'Запоминать место и размер для каждого размера окна DBD',
    'DBD-Fenster {size}: Layout für diese Grösse geladen.':
        'Окно DBD {size}: загружена раскладка для этого размера.',
    'DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.':
        'Окно DBD {size}: новый размер — отныне раскладка запоминается для него.',
    'Aktuell: Layout für {size} · {n} Grössen gemerkt':
        'Сейчас: раскладка для {size} · запомнено размеров: {n}',
    'Position zurückgesetzt (automatisch).':
        'Позиция сброшена (автоматически).',
    'keine Map':
        'нет карты',
    'ausgeblendet':
        'скрыто',
    'Menü offen':
        'открыто меню',
    'aktives Fenster ist {window}':
        'активное окно — {window}',
    'DBD-Fenster {w}×{h}':
        'Окно DBD {w}×{h}',
    'Bildschirm':
        'экран',
    'Overlay sichtbar bei {pos} über {src}.':
        'Оверлей виден в {pos} поверх {src}.',
    'Overlay pausiert: {reason}.':
        'Оверлей на паузе: {reason}.',
    '{text} – Details in fogscout.log':
        '{text} — подробности в fogscout.log',
    '{text} ({n}× seit {since}) – Details in fogscout.log':
        '{text} ({n}× с {since}) — подробности в fogscout.log',
    'Erkennung neu gestartet ({n}/{total})':
        'Распознавание перезапущено ({n}/{total})',
    'Map-Banner gefunden, lese …':
        'Баннер карты найден, чтение…',
    'automatisch erkannt ({p})':
        'распознано автоматически ({p})',
    'Layout {n} ({p})':
        'Раскладка {n} ({p})',
    'Rundentimer gestartet.':
        'Таймер раунда запущен.',
    'Rundentimer gestoppt: {time}.':
        'Таймер раунда остановлен: {time}.',
    'Erkannt: {map} – gelesen „{name}“ / „{realm}“':
        'Распознано: {map} — прочитано «{name}» / «{realm}»',
    'Layout unsicher – falls falsch: Layout-Knopf oder {keys}.':
        'Раскладка неуверенная — если неверно: кнопка раскладки или {keys}.',
    'Mitten in der Runde „{name}“ / „{realm}“ gelesen (am ehesten {map}) – ignoriert: Map-Banner gibt es nur am Rundenstart, und die Lesung war nicht eindeutig.':
        'Посреди раунда прочитано «{name}» / «{realm}» (ближе всего: {map}) — пропущено: баннеры карт появляются только в начале раунда, а чтение было неоднозначным.',
    'Banner gesehen, aber keine bekannte Map: „{text}“. Map manuell wählen oder mit „Zuordnen …“ dauerhaft zuordnen.':
        'Баннер виден, но карта неизвестна: «{text}». Выберите карту вручную или назначьте её навсегда через «Назначить…».',
    'Runde vorbei ({reason}) – Overlay ausgeblendet.':
        'Раунд окончен ({reason}) — оверлей скрыт.',
    'Runde vorbei ({reason}).':
        'Раунд окончен ({reason}).',
    'Menü offen (Mauszeiger sichtbar) – Overlay pausiert.':
        'Открыто меню (виден указатель мыши) — оверлей на паузе.',
    'Zurück im Spiel – Overlay wieder sichtbar.':
        'Снова в игре — оверлей снова виден.',
    'Die Erkennung ist abgestürzt – Details in fogscout.log':
        'Распознавание аварийно завершилось — подробности в fogscout.log',
    'Die Erkennung ist abgestürzt:':
        'Распознавание аварийно завершилось:',
    'Die Erkennung ist abgestürzt – bitte Fog Scout neu starten.':
        'Распознавание аварийно завершилось — перезапустите Fog Scout.',
    'Nichts gefunden':
        'Ничего не найдено',
    'Runde gilt jetzt für {map} (vorher {old}).':
        'Раунд теперь засчитан для {map} (раньше: {old}).',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen. Bis zum Neustart wird nichts gespeichert.':
        'Не удалось прочитать settings.json ({error}) — загружены значения по умолчанию. До перезапуска ничего не сохраняется.',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen, die alte Datei liegt als settings.json.broken daneben.':
        'Не удалось прочитать settings.json ({error}) — загружены значения по умолчанию, старый файл сохранён как settings.json.broken.',
    'Scan fehlgeschlagen: {error}':
        'Ошибка сканирования: {error}',
    'per Scan gefunden: „{text}“':
        'найдено сканированием: «{text}»',
    'Scan ({s} s): {map}':
        'Сканирование ({s} с): {map}',
    'Realm „{realm}“ hat nur diese Map':
        'В мире «{realm}» только эта карта',
    'Scan: Realm „{realm}“ gefunden – bitte Map in der Liste wählen.':
        'Сканирование: найден мир «{realm}» — выберите карту в списке.',
    'Scan ({s} s): kein Map- oder Realm-Name auf dem Bildschirm.':
        'Сканирование ({s} с): на экране нет названия карты или мира.',
    'Ergebnisbildschirm':
        'экран результатов',
    'Lobby/Menü':
        'лобби/меню',
    'Ladebildschirm':
        'экран загрузки',
    'Clip wird geladen …':
        'Загрузка клипа…',
    'Vorschaubild und Zeitleiste kommen aus der Aufnahme.':
        'Изображение предпросмотра и шкала времени читаются из записи.',
    '{n} von {total} Bildern':
        'Кадров: {n} из {total}',
    'Lädt länger als erwartet – das Fenster ist trotzdem bedienbar.':
        'Дольше, чем ожидалось — окно всё равно работает.',
    'DBD wurde geschlossen':
        'DBD закрыта',
    'Menü/Lobby (Mauszeiger lange sichtbar)':
        'меню/лобби (указатель мыши долго виден)',
    'keine Map angezeigt':
        'карта не показана',
    'Runde vorbei ({reason})':
        'раунд окончен ({reason})',
    'wartet, bis du im Match bist (Map manuell gewählt)':
        'ожидание, пока вы не окажетесь в матче (карта выбрана вручную)',
    'Menü offen – Overlay pausiert':
        'открыто меню — оверлей на паузе',
    'im Match':
        'в матче',
    'Ausblenden nach der Runde aus':
        'скрытие после раунда выключено',
    'Mauszeiger-Hinweis aus':
        'признак указателя мыши выключен',
    'Mauszeiger-Hinweis ab dem nächsten Map-Banner':
        'признак указателя мыши — со следующего баннера карты',
    'Mauszeiger: –':
        'указатель мыши: –',
    'Mauszeiger sichtbar':
        'указатель мыши виден',
    'Mauszeiger verborgen':
        'указатель мыши скрыт',
    'aus (Einstellung)':
        'выкл. (настройка)',
    'Runde vorbei – wartet auf die nächste Map':
        'раунд окончен — ожидание следующей карты',
    'Automatische Erkennung ist aus':
        'Автоматическое распознавание выключено',
    'DBD ist minimiert':
        'DBD свёрнута',
    'DBD gefunden ({w}×{h}) – warte auf Map-Banner':
        'DBD найдена ({w}×{h}) — ожидание баннера карты',
    'DBD nicht gefunden – Erkennung startet, sobald DBD läuft':
        'DBD не найдена — распознавание начнётся, когда DBD запустится',
    'Bildschirmaufnahme fehlgeschlagen: {error}':
        'Ошибка захвата экрана: {error}',
    'Aufnahme ist schwarz – DBD im Modus „Fenster-Vollbild“ betreiben':
        'Захват чёрный — запускайте DBD в режиме «Оконный полноэкранный»',
    'Fensteraufnahme nicht möglich, nutze Bildschirmaufnahme ({error})':
        'Захват окна невозможен, используется захват экрана ({error})',
    'DBD im Hintergrund – Fensteraufnahme aktiv: die Map wird auch erkannt, wenn andere Fenster darüber liegen.':
        'DBD в фоне — активен захват окна: карта распознаётся, даже если её закрывают другие окна.',
    'Rundenende-Erkennung für die gewählte Map ist jetzt aktiv.':
        'Распознавание конца раунда для выбранной карты теперь активно.',
    'Mauszeiger war beim Map-Banner sichtbar – Menü-Erkennung per Mauszeiger ist für diese Runde aus.':
        'При баннере карты был виден указатель мыши — распознавание меню по указателю в этом раунде выключено.',
    'Map zuordnen':
        'Назначить карту',
    'Gelesen: „{text}“':
        'Прочитано: «{text}»',
    'Welche Map war das? Der Name wird künftig automatisch erkannt.':
        'Какая это была карта? Отныне название будет распознаваться автоматически.',
    'Bitte eine Map auswählen.':
        'Выберите карту.',
    'Abbrechen':
        'Отмена',
    '„{text}“ wird jetzt als {map} erkannt (eigene Zuordnung).':
        '«{text}» теперь распознаётся как {map} (своё назначение).',
    'zugeordnet: „{text}“':
        'назначено: «{text}»',
    'Der gelesene Text ist zu kurz.':
        'Прочитанный текст слишком короткий.',
    'Unbekannte Map.':
        'Неизвестная карта.',
    '„{text}“ ist schon der Name von {map}.':
        '«{text}» уже является названием {map}.',
    'Kartenbild hinzufügen':
        'Добавить изображение карты',
    'eigenes Bild':
        'своё изображение',
    'Kartenbild gespeichert: {path}':
        'Изображение карты сохранено: {path}',
    'Eigenes Kartenbild für {map} gespeichert: {path}':
        'Своё изображение карты {map} сохранено: {path}',
    'wird ab jetzt automatisch erkannt.':
        'отныне распознаётся автоматически.',
    'Eigenes Kartenbild für {map} gelöscht – das mitgelieferte gilt wieder.':
        'Своё изображение карты {map} удалено — снова используется встроенное.',
    'Bitte den Namen der Map eingeben.':
        'Введите название карты.',
    '„{name}“ gibt es schon ({map}) – dann „Bild einer vorhandenen Map ersetzen“ wählen.':
        '«{name}» уже существует ({map}) — выберите вместо этого «Заменить изображение существующей карты».',
    'Noch kein Bild gewählt (PNG, JPG, WebP, GIF)':
        'Изображение ещё не выбрано (PNG, JPG, WebP, GIF)',
    'Für welche Map?':
        'Для какой карты?',
    'Ergebnis':
        'Результат',
    'Eigenes Bild löschen':
        'Удалить своё изображение',
    'Speichern':
        'Сохранить',
    'Bilder':
        'Изображения',
    'Kartenbild wählen':
        'Выбрать изображение карты',
    'Für diese Map lässt sich kein Bild speichern.':
        'Для этой карты нельзя сохранить изображение.',
    'Erst ein Bild wählen.':
        'Сначала выберите изображение.',
    'Das ist kein lesbares Bild: {error}':
        'Это не читаемое изображение: {error}',
    'Bild konnte nicht verarbeitet werden: {error}':
        'Не удалось обработать изображение: {error}',
    'Speichern fehlgeschlagen: {error}':
        'Ошибка сохранения: {error}',
    'Eigenes Bild für „{map}“ löschen?':
        'Удалить своё изображение для «{map}»?',
    'Löschen fehlgeschlagen: {error}':
        'Ошибка удаления: {error}',
    'Bild wählen …':
        'Выбрать изображение…',
    'Bild einer vorhandenen Map ersetzen':
        'Заменить изображение существующей карты',
    'Neue Map (fehlt im Programm)':
        'Новая карта (нет в программе)',
    'Name':
        'Название',
    'Name so, wie er im Map-Banner steht – dann wird die Map automatisch erkannt.':
        'Название, как на баннере карты, — тогда карта распознаётся автоматически.',
    'Hintergrund entfernen (Dunkelblau und Graulila der Community-Karten) und Rand abschneiden':
        'Удалить фон (тёмно-синий и серо-фиолетовый у карт сообщества) и обрезать рамку',
    'Ordner öffnen':
        'Открыть папку',
    'Animiertes GIF: wird unverändert übernommen.':
        'Анимированный GIF: используется без изменений.',
    'Wird gestartet …':
        'Запуск…',
    'Version {version}':
        'Версия {version}',
    'Lade Maps …':
        'Загрузка карт…',
    'Bereite Overlay vor …':
        'Подготовка оверлея…',
    'Baue Oberfläche …':
        'Построение интерфейса…',
    'Starte Erkennung …':
        'Запуск распознавания…',
    'Öffne Fenster …':
        'Открытие окна…',
    'Fog Scout ist bereit.':
        'Fog Scout готов.',
    'Automatische Erkennung':
        'Автоматическое распознавание',
    'Aufnahmen mit OBS':
        'Запись с OBS',
    'Lobby-Meldung':
        'Уведомление о лобби',
    'Spielserver anzeigen':
        'Показывать игровой сервер',
    'Systemwerte im Spiel':
        'Системные данные в игре',
    '„Heute“ im Spiel':
        '«Сегодня» в игре',
    'Musik im Spiel':
        'Музыка в игре',
    'Discord-Status':
        'Статус Discord',
    'Spotify „Als nächstes“':
        'Spotify «Далее»',
    'YouTube-Upload':
        'Загрузка на YouTube',
    '{name} eingeschaltet.':
        '{name}: включено.',
    '{name} ausgeschaltet.':
        '{name}: выключено.',
    'Erkennt die Map beim Match-Start am Banner und blendet die Karte ein. Aus: nur noch von Hand (Scannen, Map wählen). Dasselbe Häkchen steht unter Einstellungen → Erkennung.':
        'Считывает карту с баннера при начале матча и показывает её. Выкл.: только вручную (сканирование, выбор карты). Тот же флажок есть в «Настройки → Распознавание».',
    'OBS nimmt jede Runde auf: Start beim Map-Banner, Stopp beim Rundenende. Aus: keine neue Aufnahme und keine F8-Clips – eine laufende Aufnahme endet normal mit der Runde. Alles Weitere unter Einstellungen → Aufnahmen.':
        'OBS записывает каждый раунд: старт при баннере карты, стоп в конце раунда. Выкл.: никаких новых записей и клипов F8 — идущая запись заканчивается с раундом как обычно. Всё остальное в «Настройки → Записи».',
    'Ton und Hinweisfenster, sobald DBD eine Lobby gefunden hat. Die Erinnerung beim Countdown und „nur wenn DBD nicht vorne ist“ bleiben unter Einstellungen → Erkennung → Benachrichtigungen.':
        'Звук и окно уведомления, как только DBD нашла лобби. Напоминание об отсчёте и «только когда DBD не на переднем плане» остаются в «Настройки → Распознавание → Уведомления».',
    'Zeigt Region und Ping des verbundenen Spielservers – auf der Seite Server, im Overlay und in der Statistik. Einschalten fragt Windows einmal nach Administratorrechten; gelesen werden nur Paketköpfe, nie Inhalte.':
        'Показывает регион и пинг подключённого игрового сервера — на странице «Сервер», в оверлее и в статистике. При включении один раз запрашивает у Windows права администратора; читаются только заголовки пакетов, никогда не содержимое.',
    'Die Karte mit CPU-/GPU-Temperatur, Last und Speicher im schwarzen Balken. Einschalten bringt sie an die Position, an der sie zuletzt stand; Position und Zeilen unter Overlay → Systemwerte.':
        'Карточка с температурой, нагрузкой и памятью CPU/GPU в чёрной полосе. При включении возвращается туда, где была в последний раз; позиция и строки — в «Оверлей → Системные данные».',
    'Die Karte „Heute“ im Spiel: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit. Position unter Overlay → Heute.':
        'Карточка «Сегодня» в игре: раунды, время игры, ср. убийства/побеги, часы. Позиция — в «Оверлей → Сегодня».',
    'Die Musikkarte „Läuft gerade“ im Spiel (Titel, Interpret, Cover aus der Windows-Mediensteuerung). Position und Aussehen unter Overlay → Musik.':
        'Музыкальная карточка «Сейчас играет» в игре (название, исполнитель, обложка из медиаэлементов Windows). Позиция и вид — в «Оверлей → Музыка».',
    'Rich Presence: Map, Rolle und Rundenzeit in deinem Discord-Status. Application-ID und Einzelheiten unter Einstellungen → Verbindungen → Discord.':
        'Rich Presence: карта, роль и время раунда в вашем статусе Discord. Application ID и подробности — в «Настройки → Подключения → Discord».',
    'Die Liste „Als nächstes“ aus Spotify in der Musikkarte. Client-ID und Anmeldung unter Einstellungen → Verbindungen → Spotify.':
        'Список «Далее» из Spotify на музыкальной карточке. Client ID и вход — в «Настройки → Подключения → Spotify».',
    'Neue Clips (F8, Editor) gehen von selbst auf YouTube. Aus: nichts Neues wird eingereiht – was schon in der Warteschlange steht, lädt fertig; Runden lädst du weiter per Rechtsklick hoch. Einstellungen → Verbindungen → YouTube.':
        'Новые клипы (F8, редактор) сами загружаются на YouTube. Выкл.: в очередь ничего нового не добавляется — то, что уже в очереди, догружается; раунды по-прежнему загружаются через правый щелчок. «Настройки → Подключения → YouTube».',
    'Werkzeuge für die Fehlersuche ein- oder ausklappen: Live-Zustand der Rundenende-Erkennung, Debug-Bilder, Bildschirm scannen.':
        'Показать или скрыть инструменты поиска неполадок: текущее состояние распознавания конца раунда, отладочные изображения, сканирование экрана.',
    'Klicken und die neue Tastenkombination drücken: Strg/Alt + Taste, oder eine Taste allein (F1–F12, Numpad, Pause, Rollen, Einfg, Pos1, Ende, Bild↑/↓ – die gilt nur, solange DBD vorne ist). Esc bricht ab, Entf schaltet den Hotkey aus.':
        'Щёлкните и нажмите новое сочетание: Ctrl/Alt + клавиша или одна клавиша (F1–F12, цифровой блок, Pause, Scroll Lock, Insert, Home, End, Page Up/Down — работает только когда DBD на переднем плане). Esc отменяет, Delete отключает горячую клавишу.',
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
        'Работает только когда DBD на переднем плане — сама DBD больше не получает {keys} (не назначено в DBD?).',
    'Map-Namen in dieser Spielsprache erkennen. Nur die Sprachen anhaken, in denen du spielst – weniger Sprachen, weniger Verwechslungen.':
        'Распознавать названия карт на этом языке игры. Отмечайте только языки, на которых играете — меньше языков, меньше путаницы.',
    'Meldungen der Art „{category}“ im Log anzeigen.':
        'Показывать в журнале сообщения «{category}».',
    'Karte ausblenden (die automatische Erkennung läuft weiter).':
        'Скрыть карту (автоматическое распознавание продолжает работать).',
    'Karte wieder einblenden.':
        'Снова показать карту.',
    'Die Erkennung war beim Layout nicht sicher – stimmt es nicht, hier weiterschalten.':
        'Распознавание не было уверено в раскладке — если она неверна, переключите здесь.',
    'Wechselt zum nächsten Layout dieser Map (z. B. Coal Tower ↔ Coal Tower II). Die Layouts ab II gibt es seit Patch 8.6.0 nur noch in Custom Games.':
        'Переключает на следующую раскладку этой карты (например, Coal Tower ↔ Coal Tower II). С патча 8.6.0 раскладки начиная со II существуют только в своих играх.',
    'Test sofort beenden.':
        'Завершить тест сейчас.',
    'Zeigt 10 s lang alles, was das Overlay im Match zeigt – Karte, Systemwerte, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – an den eingestellten Stellen, auch ohne DBD. Nochmal drücken beendet den Test.':
        'Показывает на 10 с всё, что оверлей показывает в матче — карту, системные данные, «Сегодня» и музыку (примерные значения, если данных нет) — на своих местах, даже без DBD. Нажмите снова, чтобы завершить тест.',
    'Verschieben beenden.':
        'Прекратить перемещение.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen – falls die automatische Erkennung das Banner verpasst hat.':
        'Сразу ищет на всём экране название карты или мира — на случай, если автоматическое распознавание пропустило баннер.',
    'Eigenes Kartenbild für diese unbekannte Map anlegen – Name und Realm sind schon eingetragen, der Hintergrund wird automatisch entfernt.':
        'Создать своё изображение для этой неизвестной карты — название и мир уже заполнены, фон удаляется автоматически.',
    'Der gelesene Name gehört zu einer vorhandenen Map (z. B. anders geschrieben)? Einmal zuordnen – danach wird er automatisch erkannt.':
        'Прочитанное название относится к существующей карте (например, написано иначе)? Назначьте его один раз — после этого оно распознаётся автоматически.',
    'Hinweis ausblenden.':
        'Скрыть это уведомление.',
    'Eigenes Bild für eine Map wählen: vorhandenes Bild ersetzen oder neue Map anlegen. Rand und Hintergrund werden automatisch entfernt.':
        'Выберите своё изображение для карты: замените существующее или создайте новую карту. Рамка и фон удаляются автоматически.',
    'Position wieder auf „automatisch“ stellen (auf Ultrawide im linken schwarzen Rand).':
        'Вернуть позицию на «автоматически» (на ультрашироком мониторе — в левой чёрной полосе).',
    'Auf breiten Monitoren bleibt die Karte im schwarzen Balken, in dem sie liegt, und wird bei Bedarf verkleinert. Mitten über dem Spiel platziert gilt keine Begrenzung. Ohne schwarze Balken neben dem Spielbild (16:9, z. B. 1920×1080) sind die Balken-Optionen ausgegraut.':
        'На широких мониторах карта остаётся внутри своей чёрной полосы и при необходимости уменьшается. Если она размещена над серединой игры, ограничений нет. Без чёрных полос рядом с картинкой игры (16:9, например 1920×1080) варианты полосы недоступны.',
    'Karte ausblenden, solange ein anderes Fenster (Browser, Discord …) im Vordergrund ist.':
        'Скрывать карту, пока на переднем плане другое окно (браузер, Discord…).',
    'Zusätzliche Namenszeile über der Karte – die meisten Kartenbilder tragen den Namen schon selbst.':
        'Дополнительная строка с названием над картой — большинство изображений карт уже сами показывают название.',
    'Zeit seit dem Einblenden der Karte, gross unter der Karte.':
        'Время с появления карты, крупно под картой.',
    'Region und Ping des Spielservers unter der Karte. Braucht „Verbundener Spielserver“ im Tab Server.':
        'Регион и пинг игрового сервера под картой. Нужен «Подключённый игровой сервер» на вкладке «Сервер».',
    'Aus: Karte liegt auf einem dunklen Rechteck – besser lesbar über hellen Spielszenen.':
        'Выкл.: карта лежит на тёмном прямоугольнике — легче читать на ярких сценах игры.',
    'Liest das Map-Banner am Match-Anfang und blendet die passende Karte ein. Aus: Map nur von Hand wählen.':
        'Считывает баннер карты в начале матча и показывает подходящую карту. Выкл.: карта выбирается только вручную.',
    'Blendet die Karte nach der Runde aus (Ergebnisbildschirm, Lobby, Ladebildschirm, DBD beendet).':
        'Скрывает карту после раунда (экран результатов, лобби, экран загрузки, DBD закрыта).',
    'Karte verschwindet, solange der Mauszeiger im Spiel sichtbar ist (ESC-Menü), und kommt danach wieder.':
        'Карта исчезает, пока в игре виден указатель мыши (меню ESC), и потом возвращается.',
    'Fensteraufnahme wie bei OBS: erkennt das Banner auch, wenn DBD verdeckt ist. Nur solange DBD im Hintergrund ist.':
        'Захват окна как в OBS: распознаёт баннер, даже когда DBD закрыта. Только пока DBD в фоне.',
    'Speichert gelesene Banner und verkleinerte Bilder der Runde im Ordner debug/ – nur zur Fehlersuche, kostet Speicherplatz.':
        'Сохраняет прочитанные баннеры и маленькие изображения раунда в папку debug/ — только для поиска неполадок, занимает место на диске.',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen.':
        'Сразу ищет на всём экране название карты или мира.',
    'Kopiert technische Infos (Fenster, Overlay, letzte Rundenende-Prüfungen) in die Zwischenablage – zum Weitergeben bei Problemen.':
        'Копирует технические сведения (окно, оверлей, последние проверки конца раунда) в буфер обмена — чтобы передать, если что-то пошло не так.',
    'Misst den Ping zu allen AWS-Regionen (UDP-Beacon von Amazon GameLift).':
        'Измеряет пинг до всех регионов AWS (UDP-маяк Amazon GameLift).',
    'Nur die angehakten Regionen erlauben – trägt die übrigen in die Windows-hosts-Datei ein (fragt nach Administratorrechten).':
        'Разрешить только отмеченные регионы — остальные добавляются в файл hosts Windows (запрашивает права администратора).',
    'Entfernt die Einträge des Programms aus der hosts-Datei – alle Regionen wieder erlaubt.':
        'Удаляет записи программы из файла hosts — все регионы снова разрешены.',
    'Log-Anzeige leeren (die Log-Datei bleibt).':
        'Очистить окно журнала (файл журнала остаётся).',
    'Öffnet fogscout.log mit allen Details.':
        'Открывает fogscout.log со всеми подробностями.',
    'Dunkle oder helle Darstellung des Steuerfensters.':
        'Тёмный или светлый вид окна управления.',
    'Alle Hotkeys auf die Voreinstellung zurücksetzen.':
        'Сбросить все горячие клавиши на значения по умолчанию.',
    'Minimieren versteckt das Fenster im Infobereich; Doppelklick auf das Symbol holt es zurück.':
        'При сворачивании окно прячется в область уведомлений; двойной щелчок по значку возвращает его.',
    'Startet das Programm bei der Anmeldung im Infobereich. Nur als Administrator änderbar.':
        'Запускает программу в области уведомлений при входе в систему. Изменить можно только от имени администратора.',
    'Holt beim Start über die Verknüpfung den neuen Stand von GitHub. Eigene Änderungen werden nie überschrieben.':
        'При запуске через ярлык загружает новейшую версию с GitHub. Ваши изменения никогда не перезаписываются.',
    'Alle eigenen Map-Zuordnungen löschen (die Namen werden dann wieder als unbekannt gemeldet).':
        'Удалить все свои назначения карт (названия снова будут сообщаться как неизвестные).',
    'Öffnet den Ordner mit den mitgelieferten Kartenbildern.':
        'Открывает папку со встроенными изображениями карт.',
    'PNG, JPG, WebP oder GIF auswählen – zum Beispiel ein Original mit Hintergrund.':
        'Выберите PNG, JPG, WebP или GIF — например, оригинал с фоном.',
    'Dein Bild ersetzt das mitgelieferte Bild dieser Map (bzw. dieses Layouts). Löschen stellt das Original wieder her.':
        'Ваше изображение заменяет встроенное изображение этой карты (или этой раскладки). Удаление восстанавливает оригинал.',
    'Legt eine neue Map an. Sie wird erkannt, wenn der Name so geschrieben ist wie im Map-Banner.':
        'Создаёт новую карту. Она распознаётся, если название написано как на баннере карты.',
    'Öffnet den Ordner user_maps mit deinen eigenen Kartenbildern.':
        'Открывает папку user_maps со своими изображениями карт.',
    'Löscht dein Bild für die gewählte Map – danach gilt wieder das mitgelieferte.':
        'Удаляет ваше изображение для выбранной карты — снова используется встроенное.',
    'Bild umwandeln und speichern; die Karte wird sofort angezeigt.':
        'Преобразовать и сохранить изображение; карта сразу показывается.',
    'Schliessen, ohne etwas zu ändern.':
        'Закрыть без изменений.',
    'Macht Dunkelblau (#282a42) und Graulila (#535781) der Community-Karten transparent, schneidet den gleichfarbigen Rand ab und bringt das Bild auf 1280 px Höhe.':
        'Делает тёмно-синий (#282a42) и серо-фиолетовый (#535781) цвета карт сообщества прозрачными, обрезает рамку того же цвета и масштабирует изображение до высоты 1280 px.',
    '? unsicher – {keys} = falsch':
        '? неуверенно — {keys} = неверно',
    'Falsch erkannt':
        'Не та карта',
    'Stimmt':
        'Верно',
    'Unsicher erkannt: {map} (gelesen „{name}“)':
        'Неуверенное распознавание: {map} (прочитано «{name}»)',
    'Unsicher erkannt: {map} – gelesen „{name}“, Passung {fit}. Falls falsch: {keys} oder „Falsch erkannt“.':
        'Неуверенное распознавание: {map} — прочитано «{name}», совпадение {fit}. Если неверно: {keys} или «Не та карта».',
    '{map} bestätigt.':
        '{map} подтверждена.',
    'Nichts zu verwerfen: keine automatisch erkannte Map eingeblendet.':
        'Нечего отбрасывать: нет показанной автоматически распознанной карты.',
    'Verworfen: {map} – die Runde wird nicht gezählt.':
        'Отброшено: {map} — раунд не засчитывается.',
    'Die erkannte Map stimmt nicht: Karte ausblenden, Timer zurücksetzen, die Runde wird nicht gezählt. Geht auch im Spiel mit dem Hotkey (Standard Strg+Alt+X).':
        'Распознанная карта неверна: скрыть карту, сбросить таймер, раунд не засчитывается. Работает и в игре горячей клавишей (по умолчанию Ctrl+Alt+X).',
    'Die Map stimmt – Hinweis „unsicher“ ausblenden.':
        'Карта верна — скрыть пометку «неуверенно».',
    'als falsch verworfen':
        'отброшено как неверное',
    'Ping {ms} ms':
        'пинг {ms} мс',
    'Ø Kills':
        'Ср. убийства',
    '4K':
        '4K',
    'Entkommen':
        'Побеги',
    'entkommen':
        'сбежал',
    'tot':
        'погиб',
    'aufgegeben':
        'сдался',
    'verlassen':
        'вышел',
    'Stats-Seite öffnen, wenn DBD beendet wird':
        'Открывать страницу статистики после закрытия DBD',
    'Userscript kopieren':
        'Копировать юзерскрипт',
    'Stats-Seite öffnen':
        'Открыть страницу статистики',
    '⚠ Unbekannter Status auf der Stats-Seite: {list} – zählt nicht. Bitte melden („Diagnose kopieren“).':
        '⚠ Неизвестный статус на странице статистики: {list} — не учитывается. Сообщите об этом («Копировать диагностику»).',
    '⚠ Lücke: zwischen {start} und {end} fehlen vielleicht Matches – die Seite zeigt nur die letzten 30. Seite öfter öffnen.':
        '⚠ Пропуск: матчи между {start} и {end} могут отсутствовать — страница показывает только последние 30. Открывайте её чаще.',
    '⚠ {n}× andere Map als erkannt, zuletzt {when}: erkannt {ours}, laut Seite {theirs}.':
        '⚠ {n}× карта не совпала с распознанной, последний раз {when}: распознано {ours}, страница говорит {theirs}.',
    '⚠ Das Userscript ist veraltet (Version {old}, aktuell {new}) – „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '⚠ Юзерскрипт устарел (версия {old}, актуальная {new}) — «Копировать юзерскрипт» и замените его в Tampermonkey.',
    'Stats-Seite konnte nicht geöffnet werden: {error}':
        'Не удалось открыть страницу статистики: {error}',
    'DBD beendet – Stats-Seite geöffnet; das Userscript speichert die Matches.':
        'DBD закрыта — страница статистики открыта; юзерскрипт сохраняет матчи.',
    'Userscript nicht gefunden: {error}':
        'Юзерскрипт не найден: {error}',
    'Userscript in die Zwischenablage kopiert. In Tampermonkey: „Neues Skript erstellen“ → alles ersetzen (Strg+A, Strg+V) → Speichern. Danach stats.deadbydaylight.com öffnen und anmelden.':
        'Юзерскрипт скопирован в буфер обмена. В Tampermonkey: «Создать новый скрипт» → заменить всё (Ctrl+A, Ctrl+V) → Сохранить. Затем откройте stats.deadbydaylight.com и войдите.',
    'Offizielle Match-Daten: {n} Matches gelesen, {new} neu – Datei gelöscht.':
        'Официальные данные матчей: прочитано матчей — {n}, новых — {new}; файл удалён.',
    'Offizielle Match-Daten: zwischen {start} und {end} fehlen vielleicht Matches (die Seite zeigt nur die letzten 30).':
        'Официальные данные матчей: матчи между {start} и {end} могут отсутствовать (страница показывает только последние 30).',
    '{name} gelesen, aber nicht gelöscht: {error}':
        '{name} прочитан, но не удалён: {error}',
    '{name} ist keine Match-Datei von Fog Scout – bleibt liegen.':
        '{name} — не файл матчей Fog Scout; оставлен как есть.',
    'Unbekannter Status auf der Stats-Seite: „{status}“ – zählt nicht für Kills/Escapes. Bitte melden.':
        'Неизвестный статус на странице статистики: «{status}» — не учитывается в убийствах/побегах. Сообщите об этом.',
    'Schliesst du DBD nach mindestens einer Runde, öffnet das Programm stats.deadbydaylight.com im Browser. Das Userscript speichert dann die letzten 30 Matches, das Programm liest sie ein und löscht die Datei. Nie während DBD läuft.':
        'Когда вы закрываете DBD хотя бы после одного раунда, программа открывает stats.deadbydaylight.com в браузере. Юзерскрипт сохраняет последние 30 матчей; программа читает их и удаляет файл. Никогда — пока DBD запущена.',
    'Kopiert das Userscript in die Zwischenablage. In Tampermonkey „Neues Skript erstellen“, alles ersetzen und speichern. Es liest nur die Match-Liste, die die Seite selbst lädt – keine Konto- oder Login-Daten – und schickt nichts irgendwohin.':
        'Копирует юзерскрипт в буфер обмена. В Tampermonkey «Создать новый скрипт», заменить всё и сохранить. Он читает только список матчей, который страница загружает сама — без данных аккаунта и входа — и никуда ничего не отправляет.',
    'Öffnet stats.deadbydaylight.com jetzt. Mit installiertem Userscript kommen die Matches gleich danach an.':
        'Открывает stats.deadbydaylight.com сейчас. С установленным юзерскриптом матчи появятся сразу после этого.',
    'Vom Programm erkannt: {seen} von {n} ({share})':
        'Распознано программой: {seen} из {n} ({share})',
    'Nicht erkannt (oder das Programm lief nicht): {list}':
        'Не распознано (или программа не работала): {list}',
    'Rundenende erkannt: Median {off} gegenüber dem Ende laut Seite ({n} Runden; + = später)':
        'Конец раунда распознан: медиана {off} относительно конца на странице (раунды: {n}; + = позже)',
    '{n} Mio.':
        '{n} млн',
    'Ø BP':
        'Ср. BP',
    '✓ {n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '✓ {n} × конец раунда не распознан, но засчитан с длительностью со страницы статистики.',
    'Runden vom Map-Banner bis zum Rundenende (ab 1 min), nur lokal gespeichert. Kills, Escapes und Bloodpoints laut stats.deadbydaylight.com, sobald eine Runde dort zugeordnet ist.':
        'Раунды от баннера карты до конца раунда (от 1 мин), хранятся только локально. Убийства, побеги и очки крови — со stats.deadbydaylight.com, как только раунд связан там с матчем.',
    '{n}× Abandon':
        'сдач: {n}×',
    'Ein Skin oder neuer Killer steht unter seinem eigenen Namen? Zeile markieren, Killer wählen, „Zuordnen“ – gilt auch rückwirkend.':
        'Наряд или новый убийца показан под своим именем? Выберите строку, укажите убийцу, «Назначить» — действует и для прошлых раундов.',
    'Abgleich mit der Stats-Seite':
        'Сверка со страницей статистики',
    'Noch keine offiziellen Daten.':
        'Официальных данных пока нет.',
    'Neu seit {version}':
        'Новое с версии {version}',
    'sofort':
        'сразу',
    'HWiNFO läuft nicht: CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen.':
        'HWiNFO не запущен: нет температуры CPU, мощности CPU, ядер и FPS.',
    'Systemwerte: HWiNFO läuft nicht – CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen in dieser Runde.':
        'Системные данные: HWiNFO не запущен — в этом раунде нет температуры CPU, мощности CPU, ядер и FPS.',
    'Vorwoche {value}':
        'прошлая неделя: {value}',
    '{n} Pkt.':
        '{n} п.',
    'Montag bis jetzt gegenüber der Vorwoche (Mo–So); Custom und Farming zählen nicht.':
        'С понедельника до сейчас против прошлой недели (пн–вс); свои игры и фарм не учитываются.',
    'Sicherung: {files} nach {folder}/ kopiert (die letzten {n} Stände bleiben).':
        'Резервная копия: {files} скопировано в {folder}/ (хранятся последние {n} копий).',
    '{n} Dateien, zuletzt {day}':
        'Файлов: {n}, последний {day}',
    '1 Datei, zuletzt {day}':
        '1 файл, последний {day}',
    'behalten (nie aufgeräumt)':
        'сохранено (никогда не удаляется)',
    'wartet auf den YouTube-Upload':
        'ожидает загрузки на YouTube',
    'auf YouTube':
        'на YouTube',
    'Karte im Spiel':
        'Карта в игре',
    'OBS läuft nicht, oder sein WebSocket-Server ist aus':
        'OBS не запущен или его WebSocket-сервер выключен',
    'OBS antwortet nicht':
        'OBS не отвечает',
    'OBS hat die Verbindung getrennt':
        'OBS закрыл соединение',
    'noch keine':
        'пока нет',
    'Tägliche Kopie von rounds.jsonl und official.jsonl nach {folder}/ (nur bei Änderungen, die letzten {n} Stände je Datei; vor „Alle Runden löschen“ eine zusätzliche): {state}':
        'Ежедневная копия rounds.jsonl и official.jsonl в {folder}/ (только при изменениях, последние {n} копий каждого файла; ещё одна перед «Удалить все раунды»): {state}',
    'Verstanden':
        'Понятно',
    'Aus HISTORY.md (Deutsch), die neuesten zuerst.':
        'Из HISTORY.md (на немецком), новое сверху.',
    'Blendet die Karte „Neu seit …“ aus, bis die nächste neue Version kommt.':
        'Скрывает карточку «Новое с…» до выхода следующей новой версии.',
    'Offizielle Match-Daten':
        'Официальные данные матчей',
    'Einmal einrichten: Tampermonkey im Browser installieren, „Userscript kopieren“ und dort als neues Skript einfügen und speichern, auf stats.deadbydaylight.com anmelden. Chrome/Edge: in den Details der Erweiterung „Allow User Scripts“ einschalten, sonst läuft kein Skript. Beim Öffnen der Seite speichert das Skript neue Matches (die letzten 30) im Download-Ordner; das Programm liest die Datei und löscht sie. Es geht dafür selbst nicht ins Internet.':
        'Настройка один раз: установите Tampermonkey в браузере, «Копировать юзерскрипт», вставьте его туда как новый скрипт и сохраните, войдите на stats.deadbydaylight.com. Chrome/Edge: включите «Разрешить пользовательские скрипты» в сведениях о расширении, иначе ни один скрипт не работает. Когда страница открывается, скрипт сохраняет новые матчи (последние 30) в папку загрузок; программа читает файл и удаляет его. Сама программа для этого в интернет не выходит.',
    'Alle Matches neu speichern':
        'Сохранить все матчи заново',
    'Öffnet die Stats-Seite so, dass das Userscript ihre letzten 30 Matches noch einmal speichert, auch wenn keines neu ist – nach einer Neuinstallation oder wenn die Datei verloren ging.':
        'Открывает страницу статистики, чтобы юзерскрипт ещё раз сохранил последние 30 матчей, хотя новых нет — после новой установки или если файл потерялся.',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) speichert ihre letzten 30 Matches noch einmal, auch wenn keines neu ist; das Programm übernimmt sie gleich – bekannte zählen nur einmal. Kommt keine Datei: in der Console des Browsers (F12) steht, ob das Skript läuft. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        'Страница статистики открывается в браузере. Юзерскрипт (версия {n} или новее) ещё раз сохраняет последние 30 матчей, хотя новых нет; программа сразу их забирает — известные учитываются один раз. Если файл не появился: консоль браузера (F12) покажет, работает ли скрипт. Старые юзерскрипты: сначала «Копировать юзерскрипт» и замените его в Tampermonkey.',
    'Verlauf':
        'Тренд',
    'Nur Runden, die einem Match auf der Stats-Seite zugeordnet sind. Die Maus über einer Säule zeigt Wert und Anzahl der Runden.':
        'Только раунды, связанные с матчем на странице статистики. Наведите на столбец, чтобы увидеть его значение и число раундов.',
    'Killer – Ø Kills {per}':
        'Убийца — ср. убийства {per}',
    'Survivor – entkommen {per}':
        'Выживший — побеги {per}',
    'pro Stunde':
        'в час',
    'pro Tag':
        'в день',
    'pro Woche':
        'в неделю',
    'KW {n}':
        'Н{n}',
    '{when}: Ø {kills} Kills · {n} Runden':
        '{when}: ср. {kills} убийств · раунды: {n}',
    '{when}: {share} entkommen · {n} Runden':
        '{when}: побеги {share} · раунды: {n}',
    'Keine Killer-Runden mit offiziellen Daten in dieser Auswahl.':
        'В этой выборке нет раундов за убийцу с официальными данными.',
    'Keine Survivor-Runden mit offiziellen Daten in dieser Auswahl.':
        'В этой выборке нет раундов за выжившего с официальными данными.',
    'Ø {kills} Kills':
        'ср. {kills} убийств',
    '{share} entkommen':
        'побеги: {share}',
    'Meldung, wenn Match-Daten eingelesen und gelöscht wurden':
        'Сообщать, когда данные матчей прочитаны и удалены',
    'Zeigt unten rechts kurz, wie viele Matches gelesen wurden und dass die Datei gelöscht ist – nicht, solange DBD im Vordergrund ist. Im Log steht es immer.':
        'Ненадолго показывает внизу справа, сколько матчей прочитано и что файл удалён — не пока DBD на переднем плане. В журнале это есть всегда.',
    '{n} Matches gelesen, davon {new} neu. Die Datei wurde gelöscht.':
        'Прочитано матчей: {n}, из них новых: {new}. Файл удалён.',
    '{name} wurde gelesen, konnte aber nicht gelöscht werden – Details im Log.':
        '{name} прочитан, но не удалось его удалить — подробности в журнале.',
    'Links oben (über der Karte)':
        'Вверху слева (над картой)',
    'Rechts oben':
        'Вверху справа',
    'GPU: {name}':
        'GPU: {name}',
    'GPU: keine NVIDIA-Karte gefunden':
        'GPU: видеокарта NVIDIA не найдена',
    'CPU-Temperatur: aus HWiNFO':
        'Температура CPU: из HWiNFO',
    'Systemwerte (CPU/GPU-Temperatur, Auslastung, VRAM, RAM)':
        'Системные данные (температура и нагрузка CPU/GPU, VRAM, RAM)',
    'nach Map':
        'по картам',
    'nach Killer':
        'по убийцам',
    'GPU Ø °C':
        'GPU ср. °C',
    'GPU max':
        'GPU макс.',
    'CPU Ø °C':
        'CPU ср. °C',
    'CPU max':
        'CPU макс.',
    'GPU Ø Last':
        'GPU ср. нагрузка',
    'Ø Watt':
        'Ср. ватт',
    'Noch keine Systemwerte in dieser Auswahl (Tab Overlay → Systemwerte einschalten).':
        'В этой выборке пока нет системных данных (вкладка «Оверлей» → включить системные данные).',
    'GPU DROSSELT (TEMP.)':
        'ТРОТТЛИНГ GPU (ТЕМП.)',
    'GPU DROSSELT (HW)':
        'ТРОТТЛИНГ GPU (HW)',
    'Hotspot max {v} °C':
        'хотспот макс. {v} °C',
    'Hotspot max':
        'Хотспот макс.',
    'GPU-Temperatur – Ø {per}':
        'Температура GPU — среднее {per}',
    'Noch keine GPU-Temperaturen in dieser Auswahl.':
        'В этой выборке пока нет температур GPU.',
    '{when}: Ø {avg} °C · max {max} °C · {n} Runden':
        '{when}: ср. {avg} °C · макс. {max} °C · раунды: {n}',
    'Werte der Systemwerte-Anzeige (Tab Overlay) während der Runden – nur Runden, in denen sie eingeschaltet war. CPU-Temperatur nur mit HWiNFO. „Wann/Wo“ zeigt, auf welchen Maps oder zu welcher Tageszeit der PC am heißesten läuft. „Gedrosselt“: Sekunden, in denen die GPU wegen Temperatur oder Hardware langsamer lief (nur NVIDIA). „–“: in diesen Runden nicht erfasst – CPU-Temperatur, -Leistung, Kerne und FPS gibt es nur, solange HWiNFO läuft, und jeder Wert braucht mindestens 10 Sekunden Messwerte in der Runde.':
        'Значения показа системных данных (вкладка «Оверлей») во время раундов — только раунды, в которых он был включён. Температура CPU только с HWiNFO. «Когда/где» показывает, на каких картах или в какое время суток ПК греется сильнее всего. «Троттлинг»: секунды, в которые GPU работал медленнее из-за температуры или оборудования (только NVIDIA). «–»: в этих раундах не записано — температура CPU, мощность, ядра и FPS есть только при работающем HWiNFO, и каждому значению нужно не менее 10 секунд измерений в раунде.',
    'Eigene Position (mit der Maus verschieben)':
        'Своя позиция (тянуть мышью)',
    'SYSTEMWERTE':
        'СИСТЕМНЫЕ ДАННЫЕ',
    'Direkt über der Karte (wandert mit)':
        'Прямо над картой (движется вместе с ней)',
    'Schriftgrösse':
        'Размер шрифта',
    'Übersicht':
        'Обзор',
    'Aktuelle Map':
        'Текущая карта',
    'Rundenzeit':
        'Время раунда',
    'Ping':
        'Пинг',
    'läuft':
        'идёт',
    'letzte Runde':
        'последний раунд',
    'startet':
        'запуск',
    '4K: {n} von {total}':
        '4K: {n} из {total}',
    '{n} Survivor-Runden':
        'Раунды за выжившего: {n}',
    '{n} normal':
        'обычных: {n}',
    '{n} Farming-Runden · Ø {bp} BP':
        'Фарм-раунды: {n} · ср. {bp} BP',
    'Spielzeit heute: {time}':
        'Сыграно сегодня: {time}',
    'Systemwerte sind aus (Tab Overlay → Systemwerte).':
        'Системные данные выключены (вкладка «Оверлей» → «Системные данные»).',
    'Systemwerte gibt es nur unter Windows.':
        'Системные данные доступны только в Windows.',
    'Erscheinen, sobald DBD läuft.':
        'Появятся, как только DBD запустится.',
    'OK':
        'OK',
    '4 Kills · leer = weniger als {n} Runden':
        '4 убийства · пусто = меньше {n} раундов',
    'Killer × Map – Ø Kills laut Stats-Seite':
        'Убийца × карта — ср. убийства со страницы статистики',
    'Maps – am häufigsten gespielt':
        'Карты — чаще всего',
    'Median {time}':
        'медиана {time}',
    'Noch keine Killer-Runde mit Ergebnis von der Stats-Seite.':
        'Пока нет раундов за убийцу с результатом со страницы статистики.',
    'keine Killer-Runden mit Stats-Daten':
        'нет раундов за убийцу с данными статистики',
    'keine Survivor-Runden mit Stats-Daten':
        'нет раундов за выжившего с данными статистики',
    '{map} · {killer}: Ø {kills} Kills ({n} Runden)':
        '{map} · {killer}: ср. {kills} убийств (раунды: {n})',
    '{n} Matches':
        'Матчи: {n}',
    '{time} gespielt':
        'Сыграно: {time}',
    'Ø Bloodpoints':
        'Ср. очки крови',
    'Ø Rundendauer':
        'Ср. длительность раунда',
    'Anzeigen':
        'Показать',
    'Kartenbild nicht lesbar: {error}':
        'Изображение карты не читается: {error}',
    'Keine Map gewählt':
        'Карта не выбрана',
    'Blendet die gewählte Map jetzt als Overlay ein – die Erkennung übernimmt beim nächsten Match wieder.':
        'Показывает выбранную карту в оверлее сейчас — со следующего матча снова работает распознавание.',
    'Ziehen, um den Kasten zu verschieben':
        'Тяните, чтобы переместить этот блок',
    'Anordnung zurücksetzen':
        'Сбросить расположение',
    'Die Kästen der Seiten lassen sich am Griff rechts im Titel verschieben.':
        'Блоки страниц можно перемещать за ручку справа от заголовка.',
    'Stellt die Kästen auf allen Seiten, die Reiter-Reihen (Statistik, Overlay) und die Navigation links wieder in die ursprüngliche Reihenfolge.':
        'Возвращает блоки всех страниц, ряды вкладок (Статистика, Оверлей) и навигацию слева в исходный порядок.',
    'Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der du Dead by Daylight spielst (mehrere gehen).':
        'Программа читает название карты с изображения при начале матча. Отметьте язык, на котором вы играете в Dead by Daylight (можно несколько).',
    'Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.':
        'Карта появляется сама при начале матча и исчезает после раунда. «автоматически» помещает её в чёрную полосу рядом с картинкой игры (ультраширокий монитор) или рядом с окном DBD.',
    'Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle Tasten findest du später unter Einstellungen.':
        'Самые важные клавиши — щёлкните, чтобы изменить, затем нажмите новое сочетание. Все клавиши потом есть в «Настройки».',
    'Einrichtung starten':
        'Начать настройку',
    'Öffnet noch einmal die Einrichtung vom ersten Start: Spielsprache, Overlay-Position und die wichtigsten Tasten.':
        'Снова открывает настройку первого запуска: язык игры, позиция оверлея и самые важные клавиши.',
    'Suchen (Strg+F)':
        'Поиск (Ctrl+F)',
    'Strg+F':
        'Ctrl+F',
    'Suchen: Einstellung, Seite, Map, Aktion, Runde …':
        'Поиск: настройка, страница, карта, действие, раунд…',
    'Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst':
        'Стрелки — выбор · Enter — открыть · Ctrl+Enter — в игре или в записи · Esc — закрыть',
    'Aktionen':
        'Действия',
    'Seiten':
        'Страницы',
    'Vorschlag von Claude':
        'Предложено Claude',
    'Enter':
        'Enter',
    'Strg+Enter':
        'Ctrl+Enter',
    'Claude fragen: „{q}“':
        'Спросить Claude: «{q}»',
    'Schickt nur die Frage und die Namen der Einstellungen an Claude':
        'Отправляет Claude только вопрос и названия настроек',
    'Claude denkt nach …':
        'Claude думает…',
    'Claude hat nichts Passendes gefunden.':
        'Claude не нашёл ничего подходящего.',
    'Claude hat die Frage abgelehnt.':
        'Claude отклонил вопрос.',
    'Claude hat unverständlich geantwortet.':
        'Ответ Claude не удалось прочитать.',
    'Claude ist nicht erreichbar – keine Internetverbindung?':
        'Claude недоступен — нет подключения к интернету?',
    'Claude: Zu viele Anfragen – gleich noch einmal versuchen.':
        'Claude: слишком много запросов — повторите чуть позже.',
    'Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen.':
        'Нет ключа API — введите его в «Настройки → Подключения → Claude».',
    'Zeigt im grossen Clip-Editor den Abschnitt „Mit Claude bearbeiten“: Du schreibst, was mit dem Schnitt passieren soll, Claude schlägt Schritte vor, du übernimmst oder verwirfst sie. Gesendet werden nur deine Bitte und der Schnitt als Zahlen – kein Bild, kein Dateiname. Braucht einen eigenen API-Key.':
        'Показывает раздел «Правка с Claude» в большом редакторе клипов: вы пишете, что сделать с монтажом, Claude предлагает шаги, вы применяете или отбрасываете их. Отправляются только ваше пожелание и монтаж в виде чисел — без изображения, без имени файла. Нужен свой ключ API.',
    'Claude':
        'Claude',
    'Im Clip-Editor Claude nutzen':
        'Claude в редакторе клипов',
    'Mit Claude bearbeiten':
        'Правка с Claude',
    'z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short':
        'например, убрать первые 10 с, двойная скорость с 0:40, как Short',
    'Vorschlagen':
        'Предложить',
    'Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst.':
        'Отправляет Claude ваше пожелание и монтаж в виде чисел (время, скорость, переходы — без изображения, без имени файла); ничего не меняется, пока вы не примените.',
    'Übernehmen':
        'Применить',
    'Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z).':
        'Выполняет предложенные шаги — отменяется одним шагом (Ctrl+Z).',
    'Verwerfen':
        'Отбросить',
    'Vergisst den Vorschlag; der Schnitt bleibt, wie er ist.':
        'Забывает предложение; монтаж остаётся как есть.',
    'Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude nutzen“ einschalten und einen API-Key eintragen.':
        'Выкл. — включите «Claude в редакторе клипов» в «Настройки → Подключения → Claude» и введите ключ API.',
    'Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen.':
        'Монтаж тем временем изменился — запросите предложение заново.',
    'Claude hat keinen passenden Schritt gefunden.':
        'Claude не нашёл подходящего шага.',
    'Übernommen – Strg+Z macht es rückgängig.':
        'Применено — Ctrl+Z отменяет.',
    'übersprungen: {why}':
        'пропущено: {why}',
    'unbekannte Aktion':
        'неизвестное действие',
    'Zeiten fehlen':
        'нет времени',
    'Bereich zu kurz oder ausserhalb':
        'диапазон слишком короткий или вне клипа',
    'Tempo nicht erlaubt':
        'скорость недоступна',
    '{a}–{b} mit Tempo {f}×':
        '{a}–{b} со скоростью {f}×',
    'würde alles entfernen':
        'удалило бы всё',
    '{a}–{b} herausgeschnitten':
        '{a}–{b} вырезано',
    'nur {a}–{b} behalten':
        'оставлено только {a}–{b}',
    'Stelle ausserhalb':
        'момент вне клипа',
    'Schnitt bei {a}':
        'разрезано в {a}',
    'keine Änderung':
        'без изменений',
    'Blende ungültig':
        'переход недоступен',
    'Standbild: Dauer ungültig':
        'стоп-кадр: недопустимая длительность',
    'Untertitel zu kurz':
        'субтитр слишком короткий',
    '{n} weitere Schritte nicht ausgeführt (höchstens {max})':
        'ещё шагов не выполнено: {n} (не более {max})',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen.':
        'Сейчас невозможно — сначала завершите текущую правку, затем примените.',
    'Standbild bei {a} für {s} s':
        'стоп-кадр в {a} на {s} с',
    'Blende ohne Dauer':
        'переход без длительности',
    'Blenden: ein {i} s, aus {o} s':
        'переходы: появление {i} с, исчезание {o} с',
    'Export-Art unbekannt':
        'неизвестный тип экспорта',
    'Export-Art: {m}':
        'тип экспорта: {m}',
    'nur bei Export-Art Short':
        'только с типом экспорта Short',
    'Text fehlt':
        'нет текста',
    'Short-Titel „{t}“':
        'заголовок Short «{t}»',
    'Untertitel: Zeiten fehlen':
        'субтитр: нет времени',
    'zu viele Untertitel':
        'слишком много субтитров',
    'Untertitel {a}–{b}':
        'субтитр {a}–{b}',
    'Claude: Der API-Key wird nicht angenommen – unter Einstellungen → Verbindungen prüfen („API-Key holen“ öffnet die Anthropic Console).':
        'Claude: ключ API не принят — проверьте его в «Настройки → Подключения» («Получить ключ API» открывает Anthropic Console).',
    'Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen → Verbindungen → „Guthaben aufladen“.':
        'Claude: на API-аккаунте закончились средства — «Настройки → Подключения → Пополнить баланс».',
    'API-Key holen':
        'Получить ключ API',
    'Guthaben aufladen':
        'Пополнить баланс',
    'Öffnet die Seite „API keys“ der Anthropic Console im Browser (platform.claude.com). Dort einen Key anlegen und hier einfügen – er beginnt mit sk-ant-.':
        'Открывает страницу «API keys» в Anthropic Console в браузере (platform.claude.com). Создайте там ключ и вставьте его сюда — он начинается с sk-ant-.',
    'Öffnet die Seite „Billing“ der Anthropic Console im Browser. Die API wird getrennt von einem Claude-Abo im Voraus bezahlt; dort lässt sich auch ein monatliches Ausgabenlimit setzen.':
        'Открывает страницу «Billing» в Anthropic Console в браузере. API оплачивается заранее, отдельно от подписки Claude; там же можно задать месячный лимит расходов.',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude fragen“. Erst wenn du sie wählst, gehen deine Frage und die Namen der Einstellungen, Seiten und Aktionen an Claude (api.anthropic.com) – nie Runden, Maps oder Spieldaten. Braucht einen eigenen API-Key.':
        'Показывает строку «Спросить Claude» в поиске (Ctrl+F). Только когда вы её выбираете, ваш вопрос и названия настроек, страниц и действий отправляются Claude (api.anthropic.com) — никогда не раунды, карты или данные игры. Нужен свой ключ API.',
    'Schickt eine kleine Probefrage an Claude und sagt, ob der API-Key angenommen wird (kostet einen kleinen Betrag deines API-Guthabens).':
        'Отправляет Claude маленький тестовый вопрос и сообщает, принят ли ключ API (стоит немного средств с вашего баланса API).',
    'Entfernt den API-Key von diesem PC; die Suche fragt Claude dann nicht mehr.':
        'Удаляет ключ API с этого ПК; после этого поиск больше не спрашивает Claude.',
    'In der Suche Claude fragen können':
        'Разрешить поиску спрашивать Claude',
    'API-Key':
        'Ключ API',
    'Key prüfen':
        'Проверить ключ',
    'Key löschen':
        'Удалить ключ',
    'Claude: Key funktioniert.':
        'Claude: ключ работает.',
    'Claude: prüfe den Key …':
        'Claude: проверка ключа…',
    'Claude: kein API-Key eingetragen.':
        'Claude: ключ API не введён.',
    'Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-).':
        'Claude: это не похоже на ключ API (он начинается с sk-ant-).',
    'Claude: Key eingetragen.':
        'Claude: ключ введён.',
    'Schritt {n} von {total}':
        'Шаг {n} из {total}',
    'Sprache':
        'Язык',
    'Sprache dieses Programms:':
        'Язык этой программы:',
    'Weiter':
        'Далее',
    'Zurück':
        'Назад',
    'Überspringen':
        'Пропустить',
    'Einrichtung: {step}':
        'Настройка: {step}',
    'Aufgeteilt':
        'Подробно',
    'CPU-Temperatur':
        'Температура CPU',
    'GPU gedrosselt':
        'Троттлинг GPU',
    'GPU-Leistung':
        'Мощность GPU',
    'GPU-Speicher':
        'Память GPU',
    'GPU-Temperatur':
        'Температура GPU',
    'Hotspot':
        'Хотспот',
    'Höchstwert':
        'Максимум',
    'Höchstwerte':
        'Максимальные значения',
    'RAM':
        'RAM',
    'Runden, zusammen {time}':
        'раунды, всего {time}',
    'VRAM':
        'VRAM',
    'Wert':
        'Значение',
    '{n} von {total}':
        '{n} из {total}',
    'Ø CPU-Temperatur':
        'Ср. температура CPU',
    'Ø GPU-Last':
        'Ср. нагрузка GPU',
    'Ø GPU-Leistung':
        'Ср. мощность GPU',
    'Ø GPU-Temperatur':
        'Ср. температура GPU',
    'über {n} Runden':
        'по раундам: {n}',
    'Bilanz: Ø 2,8 Kills · 12 Runden':
        'Итоги: ср. 2,8 убийства · 12 раундов',
    'Infos und Schrift (Name, Timer, Bilanz, Server)':
        'Сведения и текст (название, таймер, итоги, сервер)',
    'Eigenes Element unter der Karte':
        'Отдельный элемент под картой',
    'Eigenes Element über der Karte':
        'Отдельный элемент над картой',
    'Eigenes Element, eigene Position':
        'Отдельный элемент, своя позиция',
    'Mit der Karte verbunden, unten':
        'Вместе с картой, снизу',
    'Mit der Karte verbunden, oben':
        'Вместе с картой, сверху',
    'Infos':
        'Сведения',
    'INFOS':
        'СВЕДЕНИЯ',
    'Infos (Timer, Bilanz, Server)':
        'Сведения (таймер, итоги, сервер)',
    'In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine Sofort-Clips (F8) und keinen Vorlauf.':
        'Буфер повтора OBS не включён — OBS: Настройки → Вывод → Буфер повтора → «Включить буфер повтора» и применить. Без него нет мгновенных клипов (F8) и предзаписи.',
    'Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)':
        'Буфер повтора в OBS не включён (Настройки → Вывод → Буфер повтора)',
    'Karten im selben Balken gleich breit':
        'Карточки в одной полосе одной ширины',
    'Zu einer Spalte zusammenführen':
        'Объединить в один столбец',
    'Die Karten, die im selben schwarzen Balken stehen, werden so breit gezeichnet wie die breiteste von ihnen – untereinander ergeben sie eine Spalte mit bündigen Rändern.':
        'Карточки в одной чёрной полосе рисуются шириной с самую широкую из них — друг под другом они образуют столбец с ровными краями.',
    'Heute unter die Systemwerte, die Musik unter Heute, alle gleich breit – eine Spalte im Balken der Systemwerte. Rückgängig mit Strg+Z.':
        '«Сегодня» под системными данными, музыка под «Сегодня», всё одной ширины — один столбец в полосе системных данных. Отмена — Ctrl+Z.',
    'Cover':
        'Обложка',
    'Discord-Overlay freihalten':
        'Не занимать место оверлея Discord',
    'Karte, Infos, Systemwerte, Heute und Musik weichen den Stellen aus, an denen Discords Overlay seine Widgets zeigt (in der Vorschau schraffiert). Das Programm liest nichts aus Discord – die Flächen sind fest.':
        'Карта, сведения, системные данные, «Сегодня» и музыка держатся в стороне от мест, где оверлей Discord показывает свои виджеты (заштрихованы в предпросмотре). Программа ничего не читает из Discord — области фиксированы.',
    'Wie der Stil':
        'Как у стиля',
    'Rund':
        'Круглая',
    'Eckig':
        'Квадратная',
    '{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr (der schwarze Balken ist voll).':
        '{what} здесь уже максимального размера — с {cap} % ползунок ничего не меняет (чёрная полоса заполнена).',
    'Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).':
        'Больше — с «Карта может быть больше полосы» (тогда она заходит на картинку игры).',
    'Spielbild':
        'Картинка игры',
    'Map-Name':
        'Название карты',
    'Farbthema':
        'Цветовая тема',
    'Gold (Standard)':
        'Золото (по умолчанию)',
    'Blutrot':
        'Кроваво-красная',
    'Eisblau':
        'Ледяная синяя',
    'Giftgrün':
        'Ядовито-зелёная',
    'Lila':
        'Фиолетовая',
    '„Heute“: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit':
        '«Сегодня»: раунды, время игры, ср. убийства/побеги, часы',
    'Eine eigene Karte, solange eine Map im Match zu sehen ist: wie viele Runden du heute gespielt hast, wie lange, Ø Kills bzw. Entkommen laut Stats-Seite und die Uhrzeit. Position darunter, Grösse über den Grössenregler („Heute“ wählen).':
        'Отдельная карточка, пока в матче на экране карта: сколько раундов вы сыграли сегодня, как долго, ср. убийства или побеги со страницы статистики и время суток. Позиция — ниже, размер — ползунком размера (выберите «Сегодня»).',
    'Dunkle Fläche hinter „Heute“':
        'Тёмный фон за «Сегодня»',
    'Vorlage':
        'Шаблон',
    'Vorlage anwenden':
        'Применить шаблон',
    'Alles links':
        'Всё слева',
    'Alles rechts':
        'Всё справа',
    'Verteilt: Karte links, Werte rechts':
        'Раздельно: карта слева, данные справа',
    'Vorlage „{name}“ angewendet.':
        'Шаблон «{name}» применён.',
    'Setzt Karte, Systemwerte, „Heute“ und Musik auf einmal auf die gewählte Anordnung. „Rückgängig“ holt die vorherige zurück.':
        'Сразу расставляет карту, системные данные, «Сегодня» и музыку по выбранной схеме. «Отменить» возвращает предыдущую.',
    'Weich ein- und ausblenden':
        'Плавное появление и исчезание',
    'In kleinen DBD-Fenstern ausblenden':
        'Скрывать в маленьких окнах DBD',
    'Läuft DBD in einem kleinen Fenster (Bild kleiner als 1920×1080 oder schmaler als 16:9), zeigt das Programm im Spiel nichts – wie der Hauptschalter. Map-Erkennung, Statistik und OBS-Aufnahmen laufen weiter. Wird das Fenster wieder gross, erscheint das Overlay von selbst.':
        'Если DBD работает в маленьком окне (картинка меньше 1920×1080 или уже, чем 16:9), программа ничего не показывает в игре — как главный переключатель. Распознавание карты, статистика и записи OBS продолжаются. Когда окно снова большое, оверлей возвращается сам.',
    'Kleines DBD-Fenster ({w}×{h}) – Overlay ausgeblendet, Runden werden weiter gezählt und aufgenommen.':
        'Маленькое окно DBD ({w}×{h}) — оверлей скрыт, раунды по-прежнему считаются и записываются.',
    'Update gesperrt: eine Runde läuft. Nach dem Rundenende noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Обновление заблокировано: идёт раунд. После окончания раунда снова нажмите «Обновить и перезапустить».',
    'Alle Farming-Runden der Auswahl (Zeitraum, Region, Map, Modus) – unabhängig vom Rollen-Filter und von „Farming ausblenden“. Farming = Crossplay war in der Lobby aus (oder die eingestellte Farming-Region); korrigieren unter „Letzte Runden“ mit „Farming an/aus“. Aufnahmen liegen im Unterordner „Farming“ des Aufnahmeordners. Wartezeit „sofort“: die Lobby war voll, bevor eine Suchzeit messbar war. Server nur, wenn „Verbunden mit“ auf der Seite Server läuft.':
        'Все фарм-раунды выборки (период, регион, карта, режим) — независимо от фильтра роли и «Скрыть фарм». Фарм = в лобби был выключен кроссплей (или заданный вами регион фарма); исправить можно в «Последних раундах» кнопкой «Фарм вкл./выкл.». Записи лежат в подпапке «Farming» папки записей. Ожидание «сразу»: лобби заполнилось раньше, чем удалось измерить время поиска. Сервер — только пока на странице «Сервер» работает «Подключено к».',
    'Keine Farming-Runden in dieser Auswahl.':
        'В этой выборке нет фарм-раундов.',
    '{n} als Killer · {m} als Survivor':
        'за убийцу: {n} · за выжившего: {m}',
    'Spielzeit':
        'Время игры',
    'vom Map-Banner bis zum Rundenende':
        'от баннера карты до конца раунда',
    'BP':
        'BP',
    '{n} gespeicherte Matches haben ein Loadout, aber keines davon ist in dieser Auswahl. Custom Games zählen nur mit dem Rollen-Filter „Custom Games“, Farming-Runden nicht mit „Farming ausblenden“, Matches ohne erkannte Runde gar nicht.':
        'У сохранённых матчей ({n}) есть снаряжение, но ни один из них не входит в эту выборку. Свои игры учитываются только с фильтром роли «Свои игры», фарм-раунды — не со «Скрыть фарм», матчи без распознанного раунда — вообще нет.',
    'DBD-Fenster wieder gross genug – Overlay wieder an.':
        'Окно DBD снова достаточно большое — оверлей снова включён.',
    'Overlay anzeigen':
        'Показывать оверлей',
    'Hauptschalter: aus = das Programm zeigt im Spiel nichts (Karte, Systemwerte, Heute, Musik). Erkennung, Statistik und Aufnahmen laufen weiter. Auch als Knopf in der Übersicht.':
        'Главный переключатель: выкл. = программа ничего не показывает в игре (карта, системные данные, «Сегодня», музыка). Распознавание, статистика и записи продолжаются. Также кнопка на странице «Обзор».',
    'Overlay eingeschaltet.':
        'Оверлей включён.',
    'Overlay ausgeschaltet – die Erkennung läuft weiter.':
        'Оверлей выключен — распознавание продолжается.',
    'Overlay ausschalten':
        'Выключить оверлей',
    'Overlay einschalten':
        'Включить оверлей',
    'Blendet alles aus, was das Programm im Spiel zeigt – Karte, Systemwerte, Heute, Musik. Die Erkennung, Statistik und Aufnahmen laufen weiter.':
        'Скрывает всё, что программа показывает в игре — карту, системные данные, «Сегодня», музыку. Распознавание, статистика и записи продолжаются.',
    'Zeigt das Overlay im Spiel wieder an.':
        'Снова показывает оверлей в игре.',
    'Karte, Systemwerte und „Heute“ blenden in einer Drittelsekunde ein und aus, statt hart zu erscheinen. Die Musik hat ihr eigenes Häkchen.':
        'Карта, системные данные и «Сегодня» появляются и исчезают за треть секунды, а не выскакивают. У музыки свой флажок.',
    'Unter „Heute“':
        'Под «Сегодня»',
    'Unter der Musik':
        'Под музыкой',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter „Heute“.':
        'Полупрозрачный тёмный фон со скруглёнными углами за «Сегодня».',
    'HEUTE':
        'СЕГОДНЯ',
    'ENTKOMMEN ':
        'ПОБЕГИ ',
    'HEUTE ':
        'СЕГОДНЯ ',
    'UHR ':
        'ВРЕМЯ ',
    '{n} RUNDEN · {time}':
        'РАУНДЫ: {n} · {time}',
    'Ø KILLS ':
        'СР. УБИЙСТВА ',
    'NORMAL ':
        'ОБЫЧНЫЕ ',
    'FARMING ':
        'ФАРМ ',
    'BP/H ':
        'BP/Ч ',
    'OLED-Schwarz':
        'OLED-чёрный',
    'Hintergründe in echtem Schwarz statt Dunkelgrau – passt zu OLED-Bildschirmen und geht mit jeder Akzentfarbe. Im hellen Modus ohne Wirkung.':
        'Фоны истинно чёрные вместо тёмно-серых — подходит для OLED-экранов и сочетается с любым акцентным цветом. В светлом режиме не действует.',
    'Eigene Farbe':
        'Свой цвет',
    'Eigene Farbe …':
        'Свой цвет…',
    'Beliebige Farbe wählen – das Programm passt die Helligkeit an, bis alles lesbar ist.':
        'Выберите любой цвет — программа подстроит его яркость, чтобы всё читалось.',
    '„Läuft gerade“: Titel, Interpret und Cover':
        '«Сейчас играет»: название, исполнитель и обложка',
    'Liest Titel und Interpret aus der Windows-Mediensteuerung (dieselbe Liste wie beim Lautstärkeregler von Windows) – nur Anzeige, das Programm steuert nichts und speichert nichts.':
        'Читает название и исполнителя из медиаэлементов Windows (тот же список, что во всплывающем окне громкости Windows) — только показ, программа ничем не управляет и ничего не сохраняет.',
    'Unter den Systemwerten':
        'Под системными данными',
    'Rechts unten im Balken':
        'Внизу справа в полосе',
    'Links unten im Balken':
        'Внизу слева в полосе',
    'MUSIK':
        'МУЗЫКА',
    'läuft gerade':
        'сейчас играет',
    'Albumcover zeigen':
        'Показывать обложку альбома',
    'Auch Videos zeigen (YouTube, Twitch …) – aus: nur Musik':
        'Показывать и видео (YouTube, Twitch…) — выкл.: только музыка',
    'Die Mediensteuerung meldet auch Videos aus dem Browser. An: ein Video erscheint als „▶ Titel“ mit dem Kanal darunter. Aus: die Karte zeigt nur Musik. Unterschieden wird am Album: Musikdienste melden eins, ein Video nicht.':
        'Медиаэлементы сообщают и о видео в браузере. Вкл.: видео показывается как «▶ Название» с каналом ниже. Выкл.: карточка показывает только музыку. Различаются по альбому: музыкальные сервисы его сообщают, видео — нет.',
    'Balken in der Farbe des Covers':
        'Полоса цвета обложки',
    'Dunkle Fläche hinter Karte und Infos':
        'Тёмный фон за картой и её строками',
    'Dunkle Fläche hinter den Systemwerten':
        'Тёмный фон за системными данными',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Karte, Timer und Infozeilen (auch hinter „Warte auf Map“) – gut lesbar über hellen Stellen im Spiel.':
        'Полупрозрачный тёмный фон со скруглёнными углами за картой, таймером и строками сведений (и за «Ожидание карты») — легко читать поверх ярких мест игры.',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Systemwerten und „Heute“.':
        'Полупрозрачный тёмный фон со скруглёнными углами за системными данными и «Сегодня».',
    'Restzeit statt Länge (−1:46)':
        'Оставшееся время вместо длительности (−1:46)',
    'Dunkle Fläche hinter der Musikkarte':
        'Тёмный фон за музыкальной карточкой',
    'Weich ein- und ausblenden (auch beim nächsten Lied)':
        'Плавное появление и исчезание (и при следующей песне)',
    'Der Fortschrittsbalken nimmt die Hauptfarbe des Albumcovers an, wie bei Spotify. Graue Cover: weiss.':
        'Полоса прогресса принимает основной цвет обложки альбома, как в Spotify. Серые обложки — белый.',
    'Rechts neben dem Balken steht, wie lange das Lied noch läuft, statt seiner Gesamtlänge.':
        'Справа от полосы: сколько ещё играет песня, вместо её общей длительности.',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Cover und Text – gut lesbar, wenn die Karte über hellen Stellen im Spiel liegt.':
        'Полупрозрачный тёмный фон со скруглёнными углами за обложкой и текстом — легко читать, когда карточка лежит поверх ярких мест игры.',
    'Die Musikkarte blendet in einer Drittelsekunde ein und aus, statt hart zu erscheinen – auch wenn ein neues Lied beginnt.':
        'Музыкальная карточка появляется и исчезает за треть секунды, а не выскакивает — и когда начинается новая песня.',
    'Das Bild zum Lied links neben Titel und Interpret – Windows liefert es mit; es bleibt nur im Speicher.':
        'Изображение песни слева от названия и исполнителя — его предоставляет Windows; оно хранится только в памяти.',
    'Gross – Cover oben, Titel darunter':
        'Большая — обложка сверху, название под ней',
    'Kompakt – Cover links':
        'Компактная — обложка слева',
    'Fortschritt des Lieds zeigen':
        'Показывать прогресс песни',
    'Unter Titel und Künstler: wie weit das Lied ist, mit Balken und Länge – wie in Spotify.':
        'Под названием и исполнителем: насколько проиграна песня, с полосой и длительностью — как в Spotify.',
    'KARTE · Strg+Mausrad = Grösse':
        'КАРТА · Ctrl+колесо = размер',
    'Ziehst: {name}':
        'Перетаскивание: {name}',
    'Unter der Maus: {name}':
        'Под мышью: {name}',
    'Kartenstil':
        'Стиль карты',
    'Kartenstil: {style}.':
        'Стиль карты: {style}.',
    'Map wählen …':
        'Выбрать карту…',
    'Zur Seite Maps: eine Map von Hand anzeigen (Doppelklick oder „Anzeigen“). Beim nächsten Match übernimmt die automatische Erkennung wieder.':
        'На страницу «Карты»: показать карту вручную (двойной щелчок или «Показать»). Со следующего матча снова работает автоматическое распознавание.',
    'Erscheint automatisch, sobald im Match das Map-Banner kommt – oder von Hand über „Map wählen“.':
        'Появляется сама, как только в матче появляется баннер карты — или вручную через «Выбрать карту».',
    'Wann zeigen':
        'Когда показывать',
    'Alle Maps':
        'Все карты',
    'Zuletzt gespielt':
        'Последние сыгранные',
    'Suchen: Name, Realm, Abkürzung …':
        'Поиск: название, мир, сокращение…',
    'Klick oder Enter = groß ansehen · Doppelklick oder Strg+Enter = jetzt anzeigen. Die Erkennung übernimmt beim nächsten Match wieder.':
        'Щелчок или Enter = посмотреть крупно · двойной щелчок или Ctrl+Enter = показать сейчас. Со следующего матча снова работает распознавание.',
    'Zurück zu den Karten des Realms (Esc).':
        'Назад к картам мира (Esc).',
    'Allgemein':
        'Общие',
    'Alle Einstellungen zurücksetzen':
        'Сбросить все настройки',
    'Alle Einstellungen auf die Auslieferung zurücksetzen? Runden, Match-Daten und eigene Bilder bleiben. Das Programm startet danach neu.':
        'Вернуть все настройки к исходному состоянию? Раунды, данные матчей и свои изображения сохранятся. После этого программа перезапустится.',
    'Alle Einstellungen zurückgesetzt.':
        'Все настройки сброшены.',
    'Standard wiederherstellen':
        'Вернуть по умолчанию',
    'Ausschalten':
        'Выключить',
    '{free} von {total} Regionen freigegeben':
        'Разрешено регионов: {free} из {total}',
    'DBD läuft gerade – die Änderung gilt erst nach einem Neustart von DBD.':
        'DBD запущена — изменение вступит в силу только после перезапуска DBD.',
    'Suchen …':
        'Поиск…',
    'Setzt jede Einstellung auf die Auslieferung zurück (Overlay, Hotkeys, Erkennung, Server-Auswahl im Programm …). Runden, Match-Daten und eigene Bilder bleiben; das Programm startet danach neu. Vorher sichern: „Einstellungen exportieren“.':
        'Возвращает все настройки к исходному состоянию (оверлей, горячие клавиши, распознавание, выбор регионов в программе…). Раунды, данные матчей и свои изображения сохраняются; программа затем перезапускается. Сначала сделайте копию: «Экспорт настроек».',
    'Grösse {pct} %':
        'размер {pct} %',
    'Eigene Einstellungen dieser Map: {what}':
        'Свои настройки этой карты: {what}',
    'Eigene Grösse und Drehung zurücksetzen':
        'Сбросить свой размер и поворот',
    'Kartenbild ersetzen …':
        'Заменить изображение карты…',
    'Im schwarzen Rand, solange die Karte im Match zu sehen ist. GPU-Werte von NVIDIA (Treiber), CPU-Temperatur nur mit HWiNFO („Shared Memory Support“ an) – kein eigener Treiber.':
        'В чёрной полосе, пока в матче на экране карта. Данные GPU — от NVIDIA (драйвер), температура CPU только с HWiNFO (включена «Shared Memory Support») — без собственного драйвера.',
    'Standard (wie ausgeliefert)':
        'Стандарт (как в поставке)',
    'Fenster {size}':
        'окно {size}',
    'alle Fenstergrössen':
        'все размеры окна',
    'Gilt für: {window}':
        'Действует для: {window}',
    'Gilt für: {maps} · {window}':
        'Действует для: {maps} · {window}',
    'nur {map}':
        'только {map}',
    'alle Maps (keine Map eingeblendet)':
        'все карты (карта не показана)',
    'Letzte 7 Tage':
        'Последние 7 дней',
    'Letzte 30 Tage':
        'Последние 30 дней',
    'Rolle/Killer':
        'Роль/убийца',
    'Weitere 100 Runden anzeigen':
        'Показать ещё 100 раундов',
    'Runden exportieren':
        'Экспорт раундов',
    '{n} Runden exportiert: {path}':
        'Экспортировано раундов: {n} — {path}',
    'Median':
        'Медиана',
    '{n} Runden':
        'Раунды: {n}',
    'Längste':
        'Самое долгое',
    'Die Liste zeigt die neuesten 100 Runden der Auswahl; jeder Klick hängt 100 ältere an.':
        'Список показывает 100 самых новых раундов выборки; каждый щелчок добавляет ещё 100 более старых.',
    'Server-Tab öffnen':
        'Открыть вкладку «Сервер»',
    'Match-Daten einrichten …':
        'Настроить данные матчей…',
    'Einrichten …':
        'Настроить…',
    'Noch keine Runden heute':
        'Сегодня раундов ещё нет',
    'Stats-Seite':
        'Страница статистики',
    'nicht eingerichtet':
        'не настроено',
    'Match-Daten':
        'Данные матчей',
    'Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → Match-Daten → Offizielle Match-Daten).':
        'Убийства, побеги и очки крови ваших раундов берутся со stats.deadbydaylight.com — их загружает ваш браузер, а не программа. Можно настроить и позже (Настройки → Данные матчей → Официальные данные матчей).',
    'Zur Seite Server: dort „Spielserver anzeigen“ anhaken – Region und Ping stehen dann hier und im Overlay.':
        'На страницу «Сервер»: отметьте там «Показывать игровой сервер» — тогда регион и пинг появятся здесь и в оверлее.',
    'Zu Einstellungen → Match-Daten → Offizielle Match-Daten: einmal das Userscript in den Browser, danach zählen Kills, Entkommen und Bloodpoints in der Statistik.':
        'В «Настройки → Данные матчей → Официальные данные матчей»: один раз установите юзерскрипт в браузер, и убийства, побеги и очки крови будут учитываться в статистике.',
    'CPU DROSSELT (TEMP.)':
        'ТРОТТЛИНГ CPU (ТЕМП.)',
    'CPU gedr.':
        'Тротт. CPU',
    'GPU gedr.':
        'Тротт. GPU',
    'CPU gedrosselt':
        'Троттлинг CPU',
    'CPU Ø W':
        'CPU ср. Вт',
    'CPU-Leistung':
        'Мощность CPU',
    'Kern Ø %':
        'Ядро ср. %',
    'Ø CPU-Leistung':
        'Ср. мощность CPU',
    'Ø stärkster CPU-Kern':
        'Ср. самое загруженное ядро CPU',
    'Niedrigstes FPS-Tief':
        'Наименьший мин. FPS',
    'Ø FPS':
        'Ср. FPS',
    'Ø FPS-Tief':
        'Ср. мин. FPS',
    'FPS Ø':
        'FPS ср.',
    'FPS Tief':
        'Мин. FPS',
    'Klick: sortieren · Rechtsklick: Spalten ein-/ausblenden':
        'Щелчок: сортировка · правый щелчок: показать/скрыть столбцы',
    'Alle Spalten zeigen':
        'Показать все столбцы',
    'Exportieren …':
        'Экспорт…',
    'Zeitraum':
        'Период',
    'Von':
        'С',
    'Bis':
        'По',
    'TT.MM.JJJJ HH:MM – auch nur ein Datum (ganzer Tag) oder nur eine Uhrzeit (heute); leer = offen.':
        'ДД.ММ.ГГГГ ЧЧ:ММ — подойдёт и только дата (весь день) или только время (сегодня); пусто = без ограничения.',
    'Gestern':
        'Вчера',
    'Alles':
        'Всё',
    'Eigener Zeitraum':
        'Свой период',
    'Filter':
        'Фильтры',
    'Custom Games einschliessen':
        'Включать свои игры',
    'Farming-Runden einschliessen':
        'Включать фарм-раунды',
    'Spalten':
        'Столбцы',
    'Start':
        'Начало',
    'Realm':
        'Мир',
    'Ping (ms)':
        'Пинг (мс)',
    'Kills':
        'Убийства',
    'Normal':
        'Обычный',
    'ja':
        'да',
    'nein':
        'нет',
    'CSV-Datei (Excel)':
        'CSV-файл (Excel)',
    'Textliste (eine Zeile je Runde)':
        'Текстовый список (строка на раунд)',
    '{n} Runden, {m} Spalten':
        'Раунды: {n}, столбцы: {m}',
    'Zeitangabe nicht lesbar: „{text}“ – Format TT.MM.JJJJ HH:MM.':
        'Не удаётся прочитать время «{text}» — формат ДД.ММ.ГГГГ ЧЧ:ММ.',
    'Nichts zu kopieren – keine Runde passt, oder keine Spalte gewählt.':
        'Нечего копировать — нет подходящих раундов или не выбран ни один столбец.',
    'Nichts zu speichern – keine Runde passt, oder keine Spalte gewählt.':
        'Нечего сохранять — нет подходящих раундов или не выбран ни один столбец.',
    'In Zwischenablage kopieren':
        'Копировать в буфер обмена',
    'Als Datei speichern …':
        'Сохранить в файл…',
    'Schliessen':
        'Закрыть',
    '{n} Runden in die Zwischenablage kopiert.':
        'Скопировано в буфер обмена раундов: {n}.',
    'Spalte „{name}“ mit ausgeben.':
        'Включить столбец «{name}».',
    'Öffnet das Export-Fenster: Zeitraum (auch von–bis), Rolle, Killer, Map, Region, Spalten nach Wahl – als CSV für Excel oder als Textliste in die Zwischenablage. Die Filter der Statistik sind vorbelegt.':
        'Открывает окно экспорта: период (в том числе с–по), роль, убийца, карта, регион, столбцы на выбор — как CSV для Excel или как текстовый список в буфер обмена. Фильтры статистики подставлены заранее.',
    'Kopiert die Runden in der gewählten Form (CSV oder Textliste) in die Zwischenablage – zum Einfügen in Discord, Excel oder einen Editor.':
        'Копирует раунды в выбранном виде (CSV или текстовый список) в буфер обмена — чтобы вставить в Discord, Excel или редактор.',
    'Speichert die Runden als Datei: CSV (Semikolon, UTF-8 mit BOM – Excel öffnet sie direkt) oder Textliste (.txt).':
        'Сохраняет раунды в файл: CSV (точка с запятой, UTF-8 с BOM — Excel открывает напрямую) или текстовый список (.txt).',
    'Schliesst das Fenster.':
        'Закрывает окно.',
    'Aus: Custom Games (eigene Lobbys, Bots) bleiben draussen.':
        'Выкл.: свои игры (свои лобби, боты) не включаются.',
    'Aus: Farming-Runden (Crossplay aus bzw. Farming-Region) bleiben draussen.':
        'Выкл.: фарм-раунды (кроссплей выключен или регион фарма) не включаются.',
    'Eine Zeile je Runde, Spalten durch Semikolon getrennt, mit Kopfzeile.':
        'Строка на раунд, столбцы через точку с запятой, со строкой заголовка.',
    'Eine Zeile je Runde, die gewählten Spalten mit „ · “ getrennt, ohne Kopfzeile – zum Einfügen in einen Chat.':
        'Строка на раунд, выбранные столбцы через « · », без заголовка — чтобы вставить в чат.',
    'Verbindungen':
        'Подключения',
    'Ton':
        'Звук',
    'Aufräumen':
        'Очистка',
    'Jede Runde mit OBS aufnehmen':
        'Записывать каждый раунд с OBS',
    'Port':
        'Порт',
    'Passwort':
        'Пароль',
    'Verbindung testen':
        'Проверить подключение',
    'Aufnahmeordner wählen …':
        'Выбрать папку записей…',
    '(kein Ordner gewählt)':
        '(папка не выбрана)',
    'Platz für Aufnahmen':
        'Место для записей',
    'Ganze Platte (Älteste weg, wenn sie voll wird)':
        'Весь диск (старые удаляются при заполнении)',
    'Vorlauf aus dem OBS-Wiederholungspuffer sichern':
        'Сохранять предзапись из буфера повтора OBS',
    'OBS nimmt auf, das Programm sagt nur wann: Start beim Map-Banner, Stopp beim erkannten Rundenende, Datei nach Datum, Map und Killer benannt. Dafür in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server einschalten und Port und Passwort unter Verbindungen → OBS-Verbindung eintragen; Verbindung nur auf diesem PC (127.0.0.1). Empfohlen: Aufnahmeformat MKV oder Hybrid-MP4 (bleibt bei Abbruch lesbar), Fenster- oder Bildschirmaufnahme statt Spielaufnahme. Der Ordner wird über sein Laufwerk gemerkt – ist die Platte nicht angeschlossen, wird nicht aufgenommen.':
        'Записывает OBS, программа только говорит когда: старт при баннере карты, стоп при распознанном конце раунда, файл называется по дате, карте и убийце. В OBS включите сервер в «Сервис → Настройки сервера WebSocket» и введите порт и пароль в «Подключения → Подключение к OBS»; соединение остаётся на этом ПК (127.0.0.1). Рекомендуется: формат записи MKV или гибридный MP4 (остаётся читаемым после сбоя), захват окна или экрана, а не захват игры. Папка запоминается по диску — если диск отключён, ничего не записывается.',
    'Ordner für die Aufnahmen (z. B. auf der externen Platte)':
        'Папка для записей (например, на внешнем диске)',
    'Aufnahmeordner: {path}':
        'Папка записей: {path}',
    'Verbinde mit OBS …':
        'Подключение к OBS…',
    'Aufnahme: {text}':
        'Запись: {text}',
    'Aufnahme gespeichert: {file}':
        'Запись сохранена: {file}',
    'Aufnahmen gelöscht (Platz): {n}':
        'Удалено записей (место): {n}',
    'OBS hat die Verbindung geschlossen':
        'OBS закрыл соединение',
    'OBS antwortet nicht auf die Anfrage {kind}':
        'OBS не отвечает на запрос {kind}',
    'OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})':
        'OBS недоступен — запущен ли OBS с включённым сервером WebSocket? ({error})',
    'Keine Antwort von obs-websocket':
        'Нет ответа от obs-websocket',
    'Kein obs-websocket auf diesem Port':
        'На этом порту нет obs-websocket',
    'Falsche WebSocket-Antwort':
        'Неверный ответ WebSocket',
    'Unerwartete Begrüssung von OBS':
        'Неожиданное приветствие от OBS',
    'OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)':
        'OBS требует пароль (OBS: Сервис → Настройки сервера WebSocket)',
    'OBS hat die Anmeldung abgelehnt – Passwort falsch?':
        'OBS отклонил вход — неверный пароль?',
    'OBS {version} verbunden':
        'OBS {version} подключён',
    'nimmt gerade auf':
        'идёт запись',
    'bereit':
        'готов',
    'Wiederholungspuffer läuft':
        'буфер повтора работает',
    'Wiederholungspuffer aus (kein Vorlauf)':
        'буфер повтора выключен (без предзаписи)',
    'Ordner: {folder}':
        'Папка: {folder}',
    'Ordner/Laufwerk nicht gefunden':
        'папка/диск не найдены',
    'Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen':
        'Диск для записей не подключён — раунд не записывается',
    'Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen':
        'Диск для записей почти заполнен — раунд не записывается',
    'OBS nimmt schon auf (von Hand?) – nichts gestartet':
        'OBS уже записывает (вручную?) — ничего не запущено',
    'Nimmt die Runde auf':
        'Запись раунда',
    'OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet':
        'OBS не сообщил имя файла — запись не привязана',
    "Aufnahme liegt in OBS' eigenem Ordner: {path}":
        'Запись в собственной папке OBS: {path}',
    'Gespeichert: {file}':
        'Сохранено: {file}',
    'Das Programm startet die OBS-Aufnahme beim Map-Banner und stoppt sie beim erkannten Rundenende (obs-websocket, nur auf diesem PC). OBS muss laufen.':
        'Программа запускает запись OBS при баннере карты и останавливает её при распознанном конце раунда (obs-websocket, только на этом ПК). OBS должен быть запущен.',
    'Verbindet sich einmal mit OBS und zeigt Version, Aufnahmezustand, Wiederholungspuffer und ob der Aufnahmeordner erreichbar ist.':
        'Один раз подключается к OBS и показывает его версию, идёт ли запись, буфер повтора и доступна ли папка записей.',
    'Ordner, in den OBS die Runden legt – z. B. auf der externen Platte. Gemerkt wird das Laufwerk, nicht der Buchstabe: bekommt die Platte einen anderen, findet das Programm den Ordner trotzdem.':
        'Папка, куда OBS кладёт раунды — например, на внешнем диске. Запоминается диск, а не его буква: если у диска сменится буква, программа всё равно найдёт папку.',
    'Läuft in OBS der Wiederholungspuffer, wird er beim Map-Banner gespeichert – der Anfang (Spawn) fehlt dann nicht, aber die Datei enthält auch Lobby und Ladebildschirm. Seit 1.5.5 standardmässig aus (Wunsch des Nutzers: nur die Runde). Die Datei liegt als „(Vorlauf)“ neben der Runde.':
        'Если буфер повтора OBS работает, он сохраняется при баннере карты — тогда начало (появление) не теряется, но файл содержит и лобби, и экран загрузки. По умолчанию выключено с версии 1.5.5 (пожелание пользователя: только раунд). Файл лежит рядом с раундом как «(Vorlauf)».',
    'Wiederholungspuffer mit DBD starten und stoppen':
        'Запускать и останавливать буфер повтора вместе с DBD',
    'Nur das DBD-Fenster aufnehmen':
        'Записывать только окно DBD',
    'Dafür die OBS-Spielaufnahme verwenden':
        'Использовать для этого захват игры OBS',
    'Statt der Fensteraufnahme legt das Programm in OBS eine Spielaufnahme „Fog Scout – DBD-Spiel“ an und blendet die Fensteraufnahme aus. Die Spielaufnahme braucht etwas weniger Leistung; OBS hängt sich dafür mit seinem Anti-Cheat-kompatiblen Hook ins Spiel – das macht OBS, nicht dieses Programm. Ihr eigener Ton bleibt aus, der Spielton kommt weiter über die Tonquelle „Fog Scout – DBD“. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“.':
        'Вместо захвата окна программа создаёт в OBS захват игры «Fog Scout – DBD-Spiel» и скрывает захват окна. Захвату игры нужно чуть меньше ресурсов; для него OBS подключается к игре своим совместимым с античитом хуком — это делает OBS, а не эта программа. Его собственный звук остаётся выключенным, звук игры по-прежнему идёт через источник звука «Fog Scout – DBD». Только вместе с «Записывать только окно DBD».',
    'Bildquelle {name} über {over} gelegt':
        'Источник изображения {name} размещён над {over}',
    'Bildquelle angelegt: {name} (Szene „{scene}“)':
        'Источник изображения создан: {name} (сцена «{scene}»)',
    'Bildquelle in der Szene „{scene}“ ausgeblendet: {name}':
        'Источник изображения скрыт в сцене «{scene}»: {name}',
    'Bildquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'Источник изображения добавлен в сцену «{scene}»: {name}',
    'Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'Источник изображения снова показан в сцене «{scene}»: {name}',
    'Bildquelle {name} zeigt jetzt {exe}':
        'Источник изображения {name} теперь показывает {exe}',
    'DBD-Fenster in OBS nicht eingerichtet: {error}':
        'Окно DBD не настроено в OBS: {error}',
    'OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin keine Sofort-Clips (F8) und kein Vorlauf.':
        'OBS не смог запустить буфер повтора (OBS сообщает об ошибке вывода, чаще всего кодировщика — подробности в журнале OBS). Программа повторит попытку только при следующем запуске DBD; до тех пор нет мгновенных клипов (F8) и предзаписи.',
    'Das Programm legt in OBS eine Fensteraufnahme „Fog Scout – DBD-Fenster“ an (oben in der laufenden Szene, auf die Leinwand eingepasst) und stellt sie auf Steam, Epic oder Store um. Aufgenommen wird dann nur das Spiel – ohne Discord, Benachrichtigungen und ohne das Overlay dieses Programms. OBS nimmt dabei über Windows auf; die Spielaufnahme gibt es als Häkchen darunter. Aus: die Quelle wird nur ausgeblendet, deine eigene Bildschirmaufnahme bleibt unangetastet.':
        'Программа создаёт в OBS захват окна «Fog Scout – DBD-Fenster» (поверх транслируемой сцены, вписанный в холст) и переключает его на Steam, Epic или Store. Тогда записывается только игра — без Discord, уведомлений и без оверлея этой программы. OBS захватывает здесь через Windows; захват игры — флажок ниже. Выкл.: источник только скрывается, ваш собственный захват экрана остаётся нетронутым.',
    'Das Programm startet den Wiederholungspuffer in OBS, sobald DBD läuft, und stoppt ihn, wenn DBD zu ist – so kostet er ausserhalb des Spiels nichts und du musst nicht daran denken.':
        'Программа запускает буфер повтора OBS, как только запускается DBD, и останавливает его, когда DBD закрывается — так он ничего не стоит вне игры, и о нём не нужно помнить.',
    'Nachlauf nach dem Rundenende':
        'Хвост после конца раунда',
    'Overlay mit in die Aufnahme':
        'Оверлей в запись',
    'Die Fensteraufnahme enthält das Overlay dieses Programms nicht (eigene Fenster). Mit Häkchen schreibt das Programm das sichtbare Overlay – Karte, Infos, Systemwerte, Heute, Musik – als Bild in seinen Cache-Ordner und legt in OBS eine Bildquelle „Fog Scout – Overlay“ darauf an, genau dort, wo das Overlay über dem DBD-Fenster liegt. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“; bei einer Bildschirmaufnahme ist das Overlay ohnehin im Bild. Aus: die Quelle wird nur ausgeblendet.':
        'Захват окна не содержит оверлей этой программы (это её собственные окна). Если флажок стоит, программа записывает видимый оверлей — карту, строки, системные данные, «Сегодня», музыку — как изображение в свою папку кэша и создаёт на его основе в OBS источник изображения «Fog Scout – Overlay» точно там, где оверлей лежит над окном DBD. Только вместе с «Записывать только окно DBD»; захват экрана и так показывает оверлей. Выкл.: источник только скрывается.',
    'Overlay in OBS nicht eingerichtet: {error}':
        'Оверлей не настроен в OBS: {error}',
    '{n} s':
        '{n} с',
    'keiner':
        'нет',
    'Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen.':
        'Диск для записей не подключён — раунды не записываются.',
    'OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})':
        'OBS не запущен — раунды не записываются. ({error})',
    'OBS bereit – Runden werden aufgenommen':
        'OBS готов — раунды записываются',
    'Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).':
        'Запись выглядит повреждённой ({why}): {file} — проверьте настройки OBS (кодировщик, диск).',
    'Aufnahme':
        'Запись',
    'Vorlauf und Runde zu einer Datei zusammenfügen':
        'Склеивать предзапись и раунд в один файл',
    'Nach der Runde hängt ffmpeg den Vorlauf vorne an die Aufnahme – ohne Neukodierung, in Sekunden. Seit 1.5.5 standardmässig aus: Am PC des Nutzers lief der Rundenteil der zusammengefügten Datei zu schnell. Klappt es nicht, bleiben beide Dateien liegen.':
        'После раунда ffmpeg ставит предзапись перед записью — без перекодирования, секунды работы. По умолчанию выключено с версии 1.5.5: на ПК пользователя часть раунда в склеенном файле проигрывалась слишком быстро. Если не получится, остаются оба файла.',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start; bis dahin bleibt der Vorlauf eine eigene Datei.':
        'Нет ffmpeg (пакет imageio-ffmpeg) — start.bat установит его при следующем запуске; до тех пор предзапись остаётся отдельным файлом.',
    'Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben':
        'Сохранено: {file} — предзапись не склеена, лежит рядом отдельным файлом',
    'Clip-Marke setzen':
        'Поставить метку клипа',
    'Clip-Marke {n} bei {pos} gesetzt.':
        'Метка клипа {n} поставлена в {pos}.',
    'Keine Aufnahme läuft – keine Clip-Marke gesetzt.':
        'Запись не идёт — метка клипа не поставлена.',
    'Aufnahmen':
        'Записи',
    'Aufnahmen einrichten …':
        'Настроить записи…',
    'Öffnet die Einstellungen für die Aufnahmen mit OBS (Ordner, Verbindung).':
        'Открывает настройки записи с OBS (папка, подключение).',
    'Platte nicht angeschlossen':
        'диск не подключён',
    'kein Ordner gewählt':
        'папка не выбрана',
    'Platz wird gemessen …':
        'измерение места…',
    '{n} mit Marke':
        'с меткой: {n}',
    'älteste {date}':
        'самая старая {date}',
    '{size} frei':
        'свободно {size}',
    '1 Aufnahme':
        '1 запись',
    '{n} Aufnahmen':
        'Записи: {n}',
    'Abspielen':
        'Воспроизвести',
    'Alle Aufnahmen':
        'Все записи',
    'Aufnahme fehlt: {file}':
        'Запись отсутствует: {file}',
    'Aufnahme gelöscht: {file}':
        'Запись удалена: {file}',
    'Aufnahme löschen':
        'Удалить запись',
    'Aufnahme nicht gelöscht ({error}): {file}':
        'Запись не удалена ({error}): {file}',
    'Aufnahme wird behalten: {file}':
        'Запись сохраняется навсегда: {file}',
    'Aufnahme wird nicht mehr behalten: {file}':
        'Запись больше не сохраняется навсегда: {file}',
    'Aufnahme-Laufwerk nicht angeschlossen.':
        'Диск для записей не подключён.',
    'Aufnahmeordner öffnen':
        'Открыть папку записей',
    'Behalten':
        'Сохранять',
    'Beschädigt':
        'Повреждена',
    'Datei':
        'Файл',
    'Einschalten unter Einstellungen → Aufnahmen.':
        'Включите в «Настройки → Записи».',
    'Im Explorer zeigen':
        'Показать в проводнике',
    'Keine Marken – F8 während der Runde setzt eine.':
        'Меток нет — F8 во время раунда ставит метку.',
    'Marken: {list}':
        'Метки: {list}',
    'Mit Marke':
        'С меткой',
    'Nicht mehr behalten':
        'Не сохранять',
    'Noch kein Aufnahmeordner gewählt.':
        'Папка записей ещё не выбрана.',
    'fehlt':
        'отсутствует',
    '{file} von der Platte löschen?':
        'Удалить {file} с диска?',
    'Spielt die markierte Aufnahme im Standard-Videoplayer ab.':
        'Воспроизводит выбранную запись в видеоплеере по умолчанию.',
    'Öffnet den Explorer mit der markierten Datei.':
        'Открывает проводник с выделенным выбранным файлом.',
    'Eine behaltene Aufnahme wird nie fürs Aufräumen gelöscht, wenn die Platte Platz braucht. Nochmal drücken hebt es auf.':
        'Сохраняемая запись никогда не удаляется очисткой, когда диску нужно место. Нажмите снова, чтобы отменить.',
    'Löscht die markierte Aufnahme (und ihren Vorlauf) von der Platte – nach Rückfrage.':
        'Удаляет выбранную запись (и её предзапись) с диска — после подтверждения.',
    'Öffnet den Aufnahmeordner im Explorer.':
        'Открывает папку записей в проводнике.',
    'Farming-Runden im Unterordner „Farming“ ablegen':
        'Класть фарм-раунды в подпапку «Farming»',
    'Runden, die das Programm als Farming erkennt (Crossplay aus oder die Farming-Region), landen im Unterordner „Farming“ des Aufnahmeordners statt zwischen den normalen Runden. Clips gehen immer in den Ordner „Clips“.':
        'Раунды, которые программа распознаёт как фарм (кроссплей выключен или регион фарма), попадают в подпапку «Farming» папки записей, а не к обычным раундам. Клипы всегда попадают в папку «Clips».',
    'Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in debug/lobby).':
        'Индикатор кроссплея не читается — раунд не считается фармом (фрагмент в debug/lobby).',
    'Rolle für {n} Runden auf {role} geändert.':
        'Роль раундов ({n}) изменена на {role}.',
    '{n} Runden aus der Statistik löschen?':
        'Удалить раунды ({n}) из статистики?',
    '{n} Runden gelöscht.':
        'Удалено раундов: {n}.',
    '{n} Runden zählen jetzt als Farming-Runden.':
        'Раунды ({n}) теперь считаются фарм-раундами.',
    '{n} Runden zählen wieder als normale Runden.':
        'Раунды ({n}) снова считаются обычными.',
    'Clip bearbeiten …':
        'Изменить клип…',
    'Öffnet den Clip-Editor für die markierte Aufnahme: Vorschau, Zeitleiste mit Marken, Start/Ende setzen, Ausschnitt als MP4 in den Ordner „Clips“ speichern.':
        'Открывает редактор клипов для выбранной записи: предпросмотр, шкала времени с метками, задать начало/конец, сохранить отрезок как MP4 в папку «Clips».',
    'Clip bearbeiten – {name}':
        'Изменить клип — {name}',
    'Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)':
        'Быстро (по ключевым кадрам, начало может быть на несколько секунд раньше)',
    'Genau (Bild neu kodiert, dauert etwas)':
        'Точно (изображение перекодируется, занимает время)',
    '5 Sekunden vor (Shift+→)':
        '5 секунд вперёд (Shift+→)',
    '5 Sekunden zurück (Shift+←)':
        '5 секунд назад (Shift+←)',
    '▶ Abspielen':
        '▶ Воспроизвести',
    '⏸ Pause':
        '⏸ Пауза',
    'Abspielen / Pause (Leertaste)':
        'Воспроизведение / пауза (пробел)',
    'Start setzen':
        'Задать начало',
    'Ende setzen':
        'Задать конец',
    'Der Clip beginnt am Abspielkopf (Taste I).':
        'Клип начинается с позиции воспроизведения (клавиша I).',
    'Der Clip endet am Abspielkopf (Taste O).':
        'Клип заканчивается на позиции воспроизведения (клавиша O).',
    'Zur Marke ▸':
        'К метке ▸',
    'Marken (F8)':
        'Метки (F8)',
    'Clip um Marke':
        'Клип вокруг метки',
    'Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der nächsten am Abspielkopf) und endet {after} s danach.':
        'Клип начинается за {before} с до выбранной метки (если не выбрана — ближайшей к позиции воспроизведения) и заканчивается через {after} с после неё.',
    'Springt zur nächsten F8-Marke (Taste M).':
        'Переходит к следующей метке F8 (клавиша M).',
    'Clip: {start} – {end} ({length} s)':
        'Клип: {start} – {end} ({length} с)',
    'Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows).':
        'Воспроизводить звук записи вместе с предпросмотром (Windows).',
    'Ton im Clip':
        'Звук в клипе',
    'Abspielkopf hierher':
        'Позиция воспроизведения сюда',
    'Als Custom Game':
        'Как своя игра',
    'Als Killer-Runde':
        'Как раунд за убийцу',
    'Als Survivor-Runde':
        'Как раунд за выжившего',
    'Ausblenden':
        'Скрыть',
    'Bild':
        'Изображение',
    'Clip beginnt hier':
        'Клип начинается здесь',
    'Clip endet hier':
        'Клип заканчивается здесь',
    'Dunkle Fläche dahinter':
        'Тёмный фон за ним',
    'Grösse zurücksetzen':
        'Сбросить размер',
    'Standbild gespeichert: {file}':
        'Стоп-кадр сохранён: {file}',
    'Standbild hier speichern':
        'Сохранить стоп-кадр здесь',
    'Standbild nicht gespeichert.':
        'Стоп-кадр не сохранён.',
    '{n} Runden löschen':
        'Удалить раунды: {n}',
    'Grosser Editor …':
        'Большой редактор…',
    'Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle und allen Tasten.':
        'Открывает клип в отдельном окне — с цензурой, уровнем для каждого источника звука и всеми клавишами.',
    'Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton.':
        'Голосовой чат Discord — дорожка OBS 3. Выкл. = в клипе нет звука Discord.',
    'Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird).':
        'Ваш микрофон — дорожка OBS 4 (только если OBS его записывает).',
    'Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen).':
        'Уровень этого источника в клипе (100 % = как записано).',
    'Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen).':
        'Одна аудиодорожка — для микширования OBS должен записывать дорожки 1–4 (Настройки → Записи).',
    'ohne Ton':
        'без звука',
    'Ton neu gemischt':
        'звук перемикширован',
    'Clip speichern':
        'Сохранить клип',
    'Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen.':
        'Записывает отрезок как MP4 в папку «Clips» рядом с записями.',
    'Clips-Ordner öffnen':
        'Открыть папку клипов',
    'Öffnet den Ordner „Clips“ im Explorer.':
        'Открывает папку «Clips» в проводнике.',
    'Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau.':
        'Файл не читается или нет ffmpeg — без предпросмотра.',
    'Clips-Ordner nicht anlegbar: {error}':
        'Не удаётся создать папку клипов: {error}',
    'Schreibe {file} …':
        'Запись {file}…',
    'Clip gespeichert: {file}':
        'Клип сохранён: {file}',
    'Clip nicht gespeichert: {why}':
        'Клип не сохранён: {why}',
    '(Sofort-Clip)':
        '(мгновенный клип)',
    'Aufnahme schon am Ladebildschirm starten':
        'Начинать запись на экране загрузки',
    'Aufnahme-Laufwerk nicht angeschlossen':
        'Диск для записей не подключён',
    'Clip':
        'Клип',
    'DBD':
        'DBD',
    'Discord':
        'Discord',
    'F8 speichert die letzten Sekunden als Sofort-Clip':
        'F8 сохраняет последние секунды как мгновенный клип',
    'Kein Sofort-Clip: {why}':
        'Нет мгновенного клипа: {why}',
    'Ladebildschirm vorbei – das Match beginnt.':
        'Экран загрузки окончен — матч начинается.',
    'Mikrofon':
        'Микрофон',
    'Spiel':
        'Игра',
    'Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner':
        'Запись — с конца экрана загрузки, ожидание баннера карты',
    'Nimmt die Runde auf (seit dem Ladebildschirm)':
        'Запись раунда (с экрана загрузки)',
    'OBS hat den Puffer nicht gespeichert':
        'OBS не сохранил буфер',
    'Sofort-Clip gespeichert ({n} s): {file}':
        'Мгновенный клип сохранён ({n} с): {file}',
    'Ton in OBS einstellen, sobald DBD startet:':
        'Настроить звук в OBS, как только запускается DBD:',
    'Ton in OBS nicht eingestellt: {error}':
        'Звук в OBS не настроен: {error}',
    'OBS bereit – Runden werden aufgenommen. {problem}':
        'OBS готов — раунды записываются. {problem}',
    'Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)':
        'Для микширования звука в редакторе клипов в OBS: Настройки → Вывод → Режим вывода «Расширенный» → вкладка «Запись» → отметьте аудиодорожки 1–5 (1 всё, 2 игра, 3 Discord, 4 микрофон, 5 фон)',
    'Jede Tonquelle auf eine eigene OBS-Tonspur':
        'Каждый источник звука на своей дорожке OBS',
    'Dafür in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken. Das Programm prüft das beim DBD-Start und meldet es im Kasten „Aufnahmen mit OBS“; es ändert nichts am OBS-Profil.':
        'Для этого в OBS: Настройки → Вывод → Режим вывода «Расширенный» → вкладка «Запись» → отметьте аудиодорожки 1–5. Программа проверяет это при запуске DBD и сообщает в карточке «Запись с OBS»; в профиле OBS она ничего не меняет.',
    'Sofort-Clip (F8) mit Ton von:':
        'Мгновенный клип (F8) со звуком из:',
    'Wie bei Medal: Das Programm weist in OBS jede Tonquelle der Spur 1 (alles – spielt in jedem Player) und ihrer eigenen Spur zu: nur DBD 2, Discord 3, Mikrofon 4, alle anderen Tonquellen in OBS (z. B. Spotify, Browser) 5 = Hintergrund. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt deshalb nur auf Spur 1. Im Clip-Editor schaltest du jede Quelle an oder aus und regelst ihre Lautstärke; beim Speichern mischt ffmpeg sie zusammen. OBS schreibt die Spuren nur im Ausgabemodus „Erweitert“ mit Audiospur 1 bis 5 angehakt (MKV oder MP4, nicht FLV); das Programm prüft das beim DBD-Start und meldet es, ändert aber nichts am OBS-Profil. Aus = Spuren bleiben, wie sie in OBS stehen.':
        'Как в Medal: программа назначает каждый источник звука в OBS на дорожку 1 (всё — играет в любом плеере) и на свою дорожку: только DBD — 2, Discord — 3, микрофон — 4, любой другой источник звука в OBS (например, Spotify, браузер) — 5 = фон. Звук рабочего стола Windows содержит и DBD, и Discord, поэтому он только на дорожке 1. В редакторе клипов вы включаете или выключаете каждый источник и задаёте его уровень; ffmpeg сводит их при сохранении. OBS записывает дорожки только в режиме вывода «Расширенный» с отмеченными аудиодорожками 1–5 (MKV или MP4, не FLV); программа проверяет это при запуске DBD и сообщает, но ничего не меняет в профиле OBS. Выкл. = дорожки остаются как настроены в OBS.',
    'Nur der Ton von DBD im Sofort-Clip.':
        'Только звук DBD в мгновенном клипе.',
    'Ton von Discord (Sprachchat) in der Aufnahme bzw. im Sofort-Clip.':
        'Звук Discord (голосовой чат) в записи или мгновенном клипе.',
    'Dein Mikrofon – die Quelle „Mikrofon/AUX“ in OBS bzw. seine Spur im Sofort-Clip.':
        'Ваш микрофон — источник «Mic/Aux» в OBS или его дорожка в мгновенном клипе.',
    'Hintergrund':
        'Фон',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.':
        'Другие программы со своим источником звука в OBS (например, Spotify, браузер) — дорожка OBS 5. Звук рабочего стола Windows содержит и DBD, и Discord и находится только на дорожке 1.',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) im Sofort-Clip – OBS-Spur 5.':
        'Другие программы со своим источником звука в OBS (например, Spotify, браузер) в мгновенном клипе — дорожка OBS 5.',
    'Tonquelle angelegt: {name}':
        'Источник звука создан: {name}',
    'Farming-Aufnahmen löschen nach':
        'Удалять фарм-записи через',
    'nie':
        'никогда',
    '{n} Tagen':
        '{n} дн.',
    'Alte Farming-Aufnahmen gelöscht (älter als {days} Tage): {n}':
        'Удалены старые фарм-записи (старше {days} дн.): {n}',
    '{name} – keine Quelle':
        '{name} — нет источника',
    '{name} – in OBS aus':
        '{name} — выключен в OBS',
    'In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf Spur 5.':
        'У OBS не было фонового источника для этой записи. Для Spotify, браузера и т. п. добавьте в OBS захват звука приложения для каждой программы — программа поместит его на дорожку 5.',
    'Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen ausgeschaltet.':
        'Этот источник звука был выключен в «Настройки → Записи», когда шла эта запись.',
    'Tonquelle {name} hört jetzt auf {exe}':
        'Источник звука {name} теперь слушает {exe}',
    'Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}':
        'На дорожке 5 (фон), а не с игрой/Discord/микрофоном: {names}',
    'Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.':
        'На дорожке {n} за всю запись ничего не слышно.',
    'Tonquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'Источник звука добавлен в сцену «{scene}»: {name}',
    'Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'Источник звука снова показан в сцене «{scene}»: {name}',
    '{name} (Spur {n})':
        '{name} (дорожка {n})',
    'Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.':
        'Тишина в этой записи: {names} — OBS ничего там не записал. Проверьте в OBS: источник в записываемой сцене, звук не отключён, дорожка отмечена.',
    '{name} – still':
        '{name} — тишина',
    'Nur der Ton von Dead by Daylight – OBS-Spur 2.':
        'Только звук Dead by Daylight — дорожка OBS 2.',
    'Unbekannte Map':
        'Неизвестная карта',
    'Wiederholungspuffer in OBS läuft nicht':
        'Буфер повтора OBS не работает',
    'Übriger Desktop-Ton':
        'Прочий звук рабочего стола',
    'Das Map-Banner kommt erst einige Sekunden nach dem Spawn. Mit diesem Häkchen startet OBS schon, wenn der Ladebildschirm nach der Lobby endet – ohne Lobby, mit Spawn. Das Banner benennt die Aufnahme danach. Kommt 3 Minuten lang kein Banner, endet die Aufnahme und heisst „Unbekannte Map“.':
        'Баннер карты появляется через несколько секунд после появления в игре. С этим флажком OBS начинает запись, как только заканчивается экран загрузки после лобби — без лобби, с появлением. Баннер потом даёт записи имя. Если баннера нет 3 минуты, запись заканчивается и называется «Неизвестная карта».',
    'F8 sichert den Wiederholungspuffer von OBS und legt die letzten Sekunden als MP4 in den Ordner „Clips“ – Bild ohne Neukodierung, in Sekunden. Spur 1 ist die unten gewählte Tonmischung (spielt überall), dahinter liegen die Einzelspuren des Puffers für den Clip-Editor. Der Wiederholungspuffer muss in OBS eingerichtet sein. Die Marke in der Rundenaufnahme setzt F8 weiterhin.':
        'F8 сохраняет буфер повтора OBS и кладёт его последние секунды как MP4 в папку «Clips» — изображение без перекодирования, секунды работы. Дорожка 1 — выбранное ниже сведение звука (играет везде), за ней идут собственные дорожки буфера для редактора клипов. Буфер повтора нужно настроить в OBS. F8 по-прежнему ставит метку в записи раунда.',
    'Das Programm legt in der aktuellen OBS-Szene je eine Anwendungs-Audioaufnahme für DBD und Discord an (einmalig) und schaltet die Tonquellen wie gewählt stumm oder laut – beim Start von DBD und bei jeder Änderung hier, auch mitten in der Runde. Aufnehmen tut OBS, das Programm fasst DBD nicht an. Braucht OBS 28 oder neuer.':
        'Программа создаёт в текущей сцене OBS по одному захвату звука приложения для DBD и Discord (один раз) и включает или отключает звук источников по выбору — при запуске DBD и при каждом изменении здесь, в том числе посреди раунда. Захват выполняет OBS, программа DBD не трогает. Нужен OBS 28 или новее.',
    'Ton des Spiels in der Aufnahme.':
        'Звук игры в записи.',
    'Alles andere, was am PC zu hören ist (Musik, Browser, Systemtöne) – die Quelle „Desktop-Audio“ in OBS.':
        'Всё остальное, что вы слышите на ПК (музыка, браузер, системные звуки) — источник OBS «Звук рабочего стола».',
    'Als Farming markieren':
        'Отметить как фарм',
    'Grund':
        'Причина',
    'Ist Farming':
        'Это фарм',
    'Kein Farming':
        'Не фарм',
    'Alle als Farming':
        'Всё как фарм',
    'Alle ignorieren':
        'Игнорировать все',
    'Custom Game, laut Stats-Seite öffentlich':
        'Своя игра, публичная на странице статистики',
    'kurze Serie, gleicher Gegner':
        'короткая серия, тот же противник',
    '{n} Runden bleiben normale Runden (kein Farming).':
        'Раунды ({n}) остаются обычными (не фарм).',
    'Markiert alle Runden der Liste als Farming-Runden (mit Rückfrage) – wie „Ist Farming“ für jede.':
        'Отмечает каждый раунд списка как фарм-раунд (сначала спрашивает) — как «Это фарм» для каждого.',
    'Keine der Runden der Liste mehr vorschlagen – sie bleiben, wie sie sind.':
        'Больше никогда не предлагать раунды из списка — они остаются как есть.',
    'Die markierten Runden der Liste sind Farming-Runden (und kein Custom Game mehr); ihre Aufnahmen wandern in den Ordner „Farming“. Zurück: „Farming an/aus“ unter „Letzte Runden“.':
        'Выбранные раунды списка — фарм-раунды (и больше не свои игры); их записи переносятся в папку «Farming». Вернуть: «Фарм вкл./выкл.» в «Последних раундах».',
    'Die markierten Runden der Liste sind normale Runden – sie bleiben, wie sie sind, und werden nie wieder vorgeschlagen.':
        'Выбранные раунды списка — обычные раунды; они остаются как есть и больше никогда не предлагаются.',
    'Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB.':
        'Discord: 10 МБ без Nitro, Nitro Basic 50 МБ, Nitro 500 МБ.',
    'Format':
        'Формат',
    'Für Discord (passt unter die Zielgrösse)':
        'Для Discord (влезает в целевой размер)',
    'Gespeichert: {file} ({mb} MB)':
        'Сохранено: {file} ({mb} МБ)',
    'Ignorieren':
        'Игнорировать',
    'Runden nicht geändert: {error}':
        'Раунды не изменены: {error}',
    'Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück.':
        'Воспроизводит ровно клип и затем возвращается к его началу.',
    'Zeigt den zuletzt gespeicherten Clip im Explorer.':
        'Показывает последний сохранённый клип в проводнике.',
    '{n} Runden als Farming markiert.':
        'Отмечено как фарм раундов: {n}.',
    '{n} Runden als Farming-Runden markieren?':
        'Отметить раунды ({n}) как фарм-раунды?',
    '{n} Runden sehen nach Farming aus: {reasons}. Zuletzt: {map}, {when}.':
        'Раунды ({n}) похожи на фарм: {reasons}. Последний: {map}, {when}.',
    '{n} als Custom Game gespeichert, laut Stats-Seite aber öffentliche Matches (vor 1.5.5 so erkannt)':
        '{n} сохранены как свои игры, но на странице статистики это публичные матчи (так читалось до версии 1.5.5)',
    '{n} kurze Runden (bis 3 min) hintereinander gegen denselben Charakter':
        '{n} коротких раундов (до 3 мин) подряд против одного персонажа',
    'Farming?':
        'Фарм?',
    'Runden sehen nach Farming aus':
        'раунды похожи на фарм',
    'Farming prüfen …':
        'Проверить фарм…',
    'Öffnet die Statistik-Übersicht mit der Zeile, die sagt, warum diese Runden nach Farming aussehen – dort markieren oder ignorieren.':
        'Открывает обзор статистики со строкой, объясняющей, почему эти раунды похожи на фарм — отметьте или проигнорируйте их там.',
    'etwa {mb} MB':
        'около {mb} МБ',
    'wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB':
        'станет {h}p {fps} fps, ≈ {kbps} кбит/с, меньше {mb} МБ',
    '≤ {n} MB':
        '≤ {n} МБ',
    '▶ Clip ansehen':
        '▶ Смотреть клип',
    'Markiert alle genannten Runden als Farming-Runden (und nicht mehr als Custom Game); ihre Aufnahmen wandern in den Ordner „Farming“. Einzeln zurück: „Farming an/aus“ unter „Letzte Runden“.':
        'Отмечает все эти раунды как фарм-раунды (больше не свои игры); их записи переносятся в папку «Farming». Вернуть по одному: «Фарм вкл./выкл.» в «Последних раундах».',
    'Diese Runden nicht mehr vorschlagen – sie bleiben, wie sie sind.':
        'Больше не предлагать эти раунды — они остаются как есть.',
    'Alle':
        'Все',
    'BP/h':
        'BP/ч',
    'BP/h mit Wartezeit':
        'BP/ч с ожиданием',
    'Bloodpoints':
        'Очки крови',
    'Bloodpoints laut Stats-Seite. BP/h = je Stunde im Match; mit Wartezeit = je Stunde aus Match und Suche zusammen. Was das Farmen allein bringt, steht im Reiter „Farming“; „Farming ausblenden“ rechnet hier ohne Farming-Runden.':
        'Очки крови со страницы статистики. BP/ч = в час в матче; с ожиданием = в час матча и поиска вместе. Сколько приносит один фарм — на вкладке «Фарм»; «Скрыть фарм» исключает здесь фарм-раунды.',
    'Bloodpoints pro Stunde':
        'Очки крови в час',
    'Summe':
        'Всего',
    'mit Wartezeit {bp}':
        'с ожиданием {bp}',
    'Rekorde':
        'Рекорды',
    'Serien zählen Runden mit Ergebnis laut Stats-Seite in zeitlicher Reihenfolge – „aktuell“ ist die Serie der neuesten Runden der Auswahl. Beste Woche ab {n} Runden mit Ergebnis. Eine Sitzung endet nach 45 Minuten ohne Runde.':
        'Серии считают раунды с результатом со страницы статистики по порядку времени — «текущая» — это серия самых новых раундов выборки. Лучшая неделя — от {n} раундов с результатом. Сессия заканчивается после 45 минут без раунда.',
    'Noch keine Runden in dieser Auswahl.':
        'В этой выборке пока нет раундов.',
    'aktuell {n}':
        'текущая {n}',
    'zuletzt {date}':
        'последний раз {date}',
    '4K-Serie':
        'Серия 4K',
    'Ø {kills} Kills · {n} Runden als {killer}':
        'Ср. {kills} убийств · раунды за {killer}: {n}',
    '{share} entkommen · {n} Runden gegen {killer}':
        'побеги {share} · раунды против {killer}: {n}',
    '4K-Serie {n}':
        'Серия 4K: {n}',
    'Entkommen-Serie {n}':
        'Серия побегов: {n}',
    'Entkommen-Serie':
        'Серия побегов',
    'Beste Woche als Killer':
        'Лучшая неделя за убийцу',
    'ab {date} · {n} Runden':
        'с {date} · раунды: {n}',
    'ab {n} Killer-Runden in einer Woche':
        'от {n} раундов за убийцу за неделю',
    'Beste Woche als Survivor':
        'Лучшая неделя за выжившего',
    'ab {n} Survivor-Runden in einer Woche':
        'от {n} раундов за выжившего за неделю',
    'Meiste Runden an einem Tag':
        'Больше всего раундов за день',
    'Längste Sitzung':
        'Самая долгая сессия',
    'Längste Runde':
        'Самый долгий раунд',
    'Spielstatus in Discord anzeigen (Rich Presence)':
        'Показывать статус игры в Discord (Rich Presence)',
    'Application-ID':
        'Application ID',
    'Discord testen':
        'Проверить Discord',
    'Developer-Portal öffnen':
        'Открыть портал разработчика',
    'Killer in Discord anzeigen':
        'Показывать убийцу в Discord',
    'Auch Lobby, Suche und Menü anzeigen':
        'Показывать также лобби, поиск и меню',
    'Zeigt in deinem Discord-Status, was gerade läuft: „Nurse auf Coal Tower“ mit Rundenzeit, in der Lobby „Sucht ein Match“. Discord braucht dafür eine Application-ID: im Developer-Portal „New Application“ anlegen (als Name z. B. „Dead by Daylight“ – so steht es im Status), die Application-ID kopieren und hier eintragen. Das Programm spricht nur mit dem Discord-Client auf diesem PC (lokale Pipe), ohne ID wird nichts gesendet; Discord erfährt nur Map, Rolle, Killer und die Startzeit.':
        'Показывает в вашем статусе Discord, что происходит: «Nurse on Coal Tower» со временем раунда, в лобби — «Поиск матча». Для этого Discord нужен Application ID: создайте «New Application» на портале разработчика (назовите, например, «Dead by Daylight» — это и покажет статус), скопируйте его Application ID и введите здесь. Программа общается только с клиентом Discord на этом ПК (локальный канал); без ID ничего не отправляется; Discord узнаёт только карту, роль, убийцу и время начала.',
    'Verbinde mit Discord …':
        'Подключение к Discord…',
    'Discord nicht gefunden – läuft es?':
        'Discord не найден — он запущен?',
    'Killer · {killer}':
        'Убийца · {killer}',
    'Im Match':
        'В матче',
    'Sucht ein Match':
        'Поиск матча',
    'In der Lobby':
        'В лобби',
    'Bereit machen':
        'Подготовка',
    'Im Menü':
        'В меню',
    'Discord: aus':
        'Discord: выкл.',
    'Discord: Fehler – {error}':
        'Discord: ошибка — {error}',
    'Application-ID fehlt – im Developer-Portal anlegen und hier eintragen.':
        'Нет Application ID — создайте его на портале разработчика и введите здесь.',
    'Ungültige Application-ID ({error})':
        'Неверный Application ID ({error})',
    'Discord: verbunden':
        'Discord: подключено',
    'Als Killer steht dein Killer im Status („Killer · The Nurse“); aus = nur „Killer“.':
        'За убийцу в статусе ваш убийца («Убийца · The Nurse»); выкл. = просто «Убийца».',
    'Aus = der Status erscheint nur während einer Runde; sonst auch „Sucht ein Match“, „In der Lobby“ und „Im Menü“, solange DBD läuft.':
        'Выкл. = статус появляется только во время раунда; иначе пока работает DBD — также «Поиск матча», «В лобби» и «В меню».',
    'Dein Discord-Status zeigt Map, Rolle, Killer und die Rundenzeit (in der Lobby: Suche/Lobby). Braucht eine Application-ID aus dem Discord-Developer-Portal; das Programm spricht nur mit dem Discord-Client auf diesem PC.':
        'Ваш статус Discord показывает карту, роль, убийцу и время раунда (в лобби: поиск/лобби). Нужен Application ID с портала разработчика Discord; программа общается только с клиентом Discord на этом ПК.',
    'Verbindet sich einmal mit dem laufenden Discord und zeigt, ob die Application-ID angenommen wird.':
        'Один раз подключается к запущенному Discord и показывает, принят ли Application ID.',
    'Öffnet discord.com/developers im Browser: „New Application“ anlegen (Name z. B. „Dead by Daylight“), die Application-ID kopieren und links eintragen.':
        'Открывает discord.com/developers в браузере: создайте «New Application» (название, например, «Dead by Daylight»), скопируйте его Application ID и введите слева.',
    'Ø pro Runde':
        'ср. за раунд',
    'BP/h im Match':
        'BP/ч в матче',
    'Spielzeit laut Stats-Seite':
        'время игры со страницы статистики',
    'Match und Suche zusammen':
        'матч и поиск вместе',
    'Beste Runde':
        'Лучший раунд',
    'Ø BP als Killer':
        'ср. BP за убийцу',
    'Ø BP als Survivor':
        'ср. BP за выжившего',
    '{when}: Ø {bp} BP · {n} Runden · Summe {sum}':
        '{when}: ср. {bp} BP · раунды: {n} · всего {sum}',
    'Ø Bloodpoints pro Runde {per}':
        'Ср. очки крови за раунд {per}',
    'Keine Runden mit Bloodpoints in dieser Auswahl.':
        'В этой выборке нет раундов с очками крови.',
    'Verpixelt':
        'Пикселизация',
    'Verwischt':
        'Размытие',
    'Schwarz':
        'Чёрный',
    'Zensieren':
        'Цензура',
    'Beim Speichern anwenden':
        'Применять при сохранении',
    'Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das Bild neu kodiert, auch im Format „Schnell“).':
        'Области скрываются в сохранённом клипе (для этого изображение перекодируется, даже в формате «Быстро»).',
    'Kasten zeichnen':
        'Нарисовать область',
    'Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug.':
        'Выделите область на изображении; области можно перемещать и менять их размер за правый нижний угол. Нажмите снова, чтобы завершить инструмент.',
    'Namen links unten':
        'Имена внизу слева',
    'Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        'Ставит область туда, где DBD показывает имена выживших (внизу слева на картинке игры) — при необходимости сдвиньте её.',
    'Kasten entfernen':
        'Удалить область',
    'Entfernt den markierten Kasten (Taste Entf).':
        'Удаляет выбранную область (клавиша Del).',
    'Alle entfernen':
        'Удалить все',
    'Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ lässt dich einen aufziehen.':
        'Областей пока нет. «Имена внизу слева» ставит одну на имена выживших, «Нарисовать область» позволяет выделить её самим.',
    '{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.':
        'Областей: {n} — тянуть = переместить, правый нижний угол = размер, щелчок = выбрать.',
    '{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.':
        'Запомнено областей: {n} — они действуют и для следующего клипа.',
    'mit Zensur neu kodiert (wie „Genau“)':
        'перекодировано для цензуры (как «Точно»)',
    'Retusche (aus der Umgebung übermalt)':
        'Ретушь (закрашивается по окружению)',
    'Spotify':
        'Spotify',
    '„Als nächstes“ aus Spotify in der Musikkarte zeigen':
        'Показывать «Далее» из Spotify на музыкальной карточке',
    'Client-ID':
        'Client ID',
    'Developer-Dashboard öffnen':
        'Открыть панель разработчика',
    'Mit Spotify verbinden':
        'Подключить Spotify',
    'Spotify-Verbindung trennen':
        'Отключить Spotify',
    'Spotify: öffne die Anmeldung im Browser …':
        'Spotify: открытие входа в браузере…',
    'YouTube':
        'YouTube',
    'Privat':
        'Частный',
    'Nicht gelistet':
        'По ссылке',
    'Öffentlich':
        'Открытый',
    'Client-Secret':
        'Client secret',
    'Sichtbarkeit':
        'Доступ',
    'Clips automatisch auf YouTube hochladen':
        'Автоматически загружать клипы на YouTube',
    'Google Cloud Console öffnen':
        'Открыть консоль Google Cloud',
    'Client-Datei laden …':
        'Загрузить файл клиента…',
    'Client-Datei laden':
        'Загрузить файл клиента',
    'Client-Datei von Google laden':
        'Загрузите файл клиента от Google',
    'Das ist keine Client-Datei von Google ({error}).':
        'Это не файл клиента от Google ({error}).',
    'YouTube: Client-ID und Client-Secret aus {file} übernommen – jetzt „Mit YouTube verbinden“ klicken.':
        'YouTube: Client ID и client secret взяты из {file} — теперь нажмите «Подключить YouTube».',
    'YouTube: Client-Daten aus {file} übernommen.':
        'YouTube: данные клиента взяты из {file}.',
    'Datei zu gross':
        'файл слишком большой',
    'nicht lesbar: {error}':
        'не читается: {error}',
    'kein JSON: {error}':
        'не JSON: {error}',
    'kein JSON-Objekt':
        'не объект JSON',
    'OAuth-Client vom Typ „Webanwendung“ – in der Cloud Console einen vom Typ „Desktop-App“ anlegen':
        'OAuth-клиент типа «Web application» — создайте в консоли Cloud клиент типа «Desktop app»',
    'kein Abschnitt „installed“':
        'нет раздела «installed»',
    'Client-ID fehlt oder endet nicht auf .apps.googleusercontent.com':
        'Client ID отсутствует или не заканчивается на .apps.googleusercontent.com',
    'Client-Secret fehlt':
        'нет client secret',
    'Mit YouTube verbinden':
        'Подключить YouTube',
    'YouTube-Verbindung trennen':
        'Отключить YouTube',
    'Auf YouTube hochladen':
        'Загрузить на YouTube',
    'YouTube-Link kopieren':
        'Копировать ссылку YouTube',
    'Auf YouTube öffnen':
        'Открыть на YouTube',
    'YouTube: Client-ID (…apps.googleusercontent.com) und Client-Secret eintragen.':
        'YouTube: введите Client ID (…apps.googleusercontent.com) и client secret.',
    'YouTube: öffne die Anmeldung im Browser …':
        'YouTube: открытие входа в браузере…',
    'Hochgeladen: {file}':
        'Загружено: {file}',
    'YouTube: nicht hochgeladen – {file}: {why}':
        'YouTube: не загружено — {file}: {why}',
    'YouTube: in die Warteschlange – {file}':
        'YouTube: в очереди — {file}',
    'YouTube-Link kopiert: {url}':
        'Ссылка YouTube скопирована: {url}',
    'Clip: {what}':
        'Клип: {what}',
    'Dauer {d}':
        'Длительность {d}',
    'Aufgenommen mit Fog Scout':
        'Записано с Fog Scout',
    'keine Upload-Sitzung erhalten':
        'сеанс загрузки не получен',
    'Antwort ohne Video-ID':
        'ответ без ID видео',
    'nicht angemeldet':
        'вход не выполнен',
    'Datei nicht gefunden':
        'файл не найден',
    'Aufnahmeordner nicht da':
        'папки записей нет',
    'YouTube: aus':
        'YouTube: выкл.',
    'YouTube: nicht verbunden – „Mit YouTube verbinden“ klicken.':
        'YouTube: не подключено — нажмите «Подключить YouTube».',
    'Mit YouTube verbunden – du kannst dieses Fenster schliessen.':
        'Подключено к YouTube — это окно можно закрыть.',
    'Google hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Google отклонил вход — это окно можно закрыть.',
    'YouTube: Anmeldung nicht möglich – {error}':
        'YouTube: вход невозможен — {error}',
    'YouTube: Browser nicht geöffnet – {error}':
        'YouTube: браузер не открылся — {error}',
    'YouTube: Anmeldung abgelehnt ({error})':
        'YouTube: вход отклонён ({error})',
    'YouTube: Google gab kein dauerhaftes Token – in der Cloud Console den OAuth-Client als „Desktop“ anlegen und den Zustimmungsbildschirm veröffentlichen.':
        'YouTube: Google не выдал постоянный токен — создайте OAuth-клиент как «Desktop app» в консоли Cloud и опубликуйте экран согласия.',
    'YouTube: verbunden':
        'YouTube: подключено',
    'YouTube: Anmeldung abgelaufen – noch einmal „Mit YouTube verbinden“ klicken.':
        'YouTube: вход истёк — нажмите «Подключить YouTube» ещё раз.',
    'YouTube: {n} in der Warteschlange – wartet, bis Lobby und Runde vorbei sind':
        'YouTube: в очереди {n} — ожидание, пока не закончатся лобби и раунд',
    'YouTube: {n} in der Warteschlange – Tageskontingent aufgebraucht, weiter ab {when}':
        'YouTube: в очереди {n} — дневная квота исчерпана, продолжение в {when}',
    'YouTube: lädt {file} hoch ({pct} %)':
        'YouTube: загрузка {file} ({pct} %)',
    'YouTube: hochgeladen – {file}':
        'YouTube: загружено — {file}',
    'YouTube: {error} – neuer Versuch in {s} s':
        'YouTube: {error} — повтор через {s} с',
    'YouTube: {n} in der Warteschlange – {why}':
        'YouTube: в очереди {n} — {why}',
    'Uploads in Playlists einsortieren':
        'Распределять загрузки по плейлистам',
    'Playlists laden':
        'Загрузить плейлисты',
    'Clips in':
        'Клипы в',
    'Runden in':
        'Раунды в',
    'YouTube: lade Playlists …':
        'YouTube: загрузка плейлистов…',
    'YouTube: zuerst „Uploads in Playlists einsortieren“ anhaken.':
        'YouTube: сначала отметьте «Распределять загрузки по плейлистам».',
    'YouTube: {n} Playlists geladen – im Kasten auswählen':
        'YouTube: загружено плейлистов: {n} — выберите их в списке',
    'YouTube: keine Playlists auf dem Kanal – zuerst auf YouTube eine anlegen':
        'YouTube: на канале нет плейлистов — сначала создайте плейлист на YouTube',
    'YouTube: Playlists nicht geladen – {why}':
        'YouTube: плейлисты не загружены — {why}',
    'YouTube: {file} in Playlist „{name}“ einsortiert':
        'YouTube: {file} добавлен в плейлист «{name}»',
    'YouTube: {file} hochgeladen, aber nicht in die Playlist – {why}':
        'YouTube: {file} загружен, но не в плейлист — {why}',
    'Berechtigung fehlt – noch einmal „Mit YouTube verbinden“ klicken':
        'нет разрешения — нажмите «Подключить YouTube» ещё раз',
    'YouTube: verbunden – für Playlists einmal neu „Mit YouTube verbinden“ klicken.':
        'YouTube: подключено — для плейлистов нажмите «Подключить YouTube» ещё раз.',
    'Nach dem Upload kommt jedes Video in die gewählte Playlist – für Clips und Runden getrennt wählbar, beide dürfen dieselbe sein. Braucht bei Google die Berechtigung „YouTube-Konto verwalten“ statt nur „Videos hochladen“: nach dem Anhaken einmal neu „Mit YouTube verbinden“. Das Programm nutzt davon nur Playlists auflisten und Video einsortieren (50 Einheiten je Video; es bleiben sechs Uploads am Tag).':
        'После загрузки каждое видео попадает в выбранный плейлист — отдельно для клипов и раундов, оба могут совпадать. Нужно разрешение Google «Управление аккаунтом YouTube» вместо только «Загрузка видео»: после отметки ещё раз нажмите «Подключить YouTube». Программа использует его только для списка плейлистов и добавления видео (50 единиц на видео; остаётся шесть загрузок в день).',
    'Holt die Liste deiner Playlists von YouTube (1 Einheit) in die beiden Auswahlfelder. Neue Playlists legst du auf YouTube an und lädst die Liste danach neu.':
        'Загружает с YouTube список ваших плейлистов (1 единица) в оба списка выбора. Новые плейлисты создайте на YouTube, затем загрузите список снова.',
    'YouTube: Fehler – {error}':
        'YouTube: ошибка — {error}',
    'Jeder neue Clip (F8 und aus dem Editor) kommt in die Warteschlange und geht auf deinen Kanal, sobald du weder in einer Lobby noch in einer Runde bist – mit der Sichtbarkeit rechts, Standard privat. Runden lädst du nur auf Wunsch hoch (Rechtsklick unter Aufnahmen). Google erlaubt etwa sechs Uploads am Tag, der Rest wartet bis zum nächsten Tag. Die Datei bleibt auf der Platte.':
        'Каждый новый клип (F8 и из редактора) встаёт в очередь и загружается на ваш канал, как только вы не в лобби и не в раунде — с доступом, выбранным справа, по умолчанию частным. Раунды загружаются только по запросу (правый щелчок в «Записи»). Google разрешает около шести загрузок в день, остальное ждёт следующего дня. Файл остаётся на диске.',
    'Öffnet die Anmeldedaten der Google Cloud Console im Browser: Projekt anlegen, „YouTube Data API v3“ aktivieren, OAuth-Client „Desktop-App“ erstellen, Client-ID und -Secret hier einfügen.':
        'Открывает страницу учётных данных консоли Google Cloud в браузере: создайте проект, включите «YouTube Data API v3», создайте OAuth-клиент «Desktop app», вставьте сюда Client ID и secret.',
    'Vergisst die Google-Freigabe auf diesem PC; die Warteschlange wartet, bis du dich neu verbindest. In deinem Google-Konto unter Sicherheit → Drittanbieter-Apps lässt sich der Zugriff ebenfalls entfernen.':
        'Забывает согласие Google на этом ПК; очередь ждёт, пока вы снова не подключитесь. В аккаунте Google в разделе «Безопасность → Сторонние приложения» доступ тоже можно удалить.',
    'Die markierte Datei in die YouTube-Warteschlange (Sichtbarkeit wie in den Einstellungen, Standard privat). Hochgeladen wird, sobald du weder in einer Lobby noch in einer Runde bist und das Tageskontingent reicht; der Link erscheint danach im Rechtsklick-Menü.':
        'Ставит выбранный файл в очередь YouTube (доступ — как в настройках, по умолчанию частный). Загружается, как только вы не в лобби и не в раунде и позволяет дневная квота; затем ссылка появляется в меню правого щелчка.',
    'Spotify: Client-ID sieht falsch aus – erwartet werden 32 Zeichen aus 0–9 und a–f (Dashboard → deine App → Settings → Basic Information → Client ID).':
        'Spotify: Client ID выглядит неверным — ожидается 32 символа из 0–9 и a–f (панель → ваше приложение → Settings → Basic Information → Client ID).',
    'ALS NÄCHSTES':
        'ДАЛЕЕ',
    'Unter dem Lied':
        'Под песней',
    'Rechts neben dem Lied':
        'Справа от песни',
    'Als nächstes':
        'Далее',
    'Anzahl Titel':
        'Показывать треков',
    'Die Liste kommt aus Spotify – einrichten unter Einstellungen → Verbindungen → Spotify.':
        'Список берётся из Spotify — настройте его в «Настройки → Подключения → Spotify».',
    'Spotify: aus':
        'Spotify: выкл.',
    'Spotify: Client-ID fehlt – im Developer-Dashboard anlegen und hier eintragen.':
        'Spotify: нет Client ID — создайте его в панели разработчика и введите здесь.',
    'Spotify: nicht verbunden – „Mit Spotify verbinden“ klicken.':
        'Spotify: не подключено — нажмите «Подключить Spotify».',
    'Spotify: Anmeldung im Browser offen – dort bei Spotify anmelden und zustimmen …':
        'Spotify: вход открыт в браузере — войдите там в Spotify и дайте согласие…',
    'Spotify: Port {port} ist belegt – Anmeldung nicht möglich.':
        'Spotify: порт {port} занят — вход невозможен.',
    'Spotify: Browser konnte nicht geöffnet werden ({error})':
        'Spotify: не удалось открыть браузер ({error})',
    'Spotify: Anmeldung fehlgeschlagen ({error})':
        'Spotify: ошибка входа ({error})',
    'Spotify: Anmeldung abgelehnt ({error})':
        'Spotify: вход отклонён ({error})',
    'Spotify: keine Antwort vom Browser – Anmeldung abgebrochen.':
        'Spotify: нет ответа от браузера — вход отменён.',
    'Spotify: verbunden':
        'Spotify: подключено',
    'Spotify: Anmeldung abgelaufen – bitte neu verbinden.':
        'Spotify: вход истёк — подключитесь снова.',
    'Spotify: kein Zugriff ({error}) – ist dein Spotify-Konto in der Developer-App unter „User Management“ eingetragen?':
        'Spotify: нет доступа ({error}) — указан ли ваш аккаунт Spotify в приложении разработчика в «User Management»?',
    'Spotify: Fehler – {error}':
        'Spotify: ошибка — {error}',
    'Spotify: Kontingent der Developer-App aufgebraucht – „Als nächstes“ pausiert bis {time}.':
        'Spotify: квота приложения разработчика исчерпана — «Далее» на паузе до {time}.',
    'keine Antwort mit Token':
        'нет ответа с токеном',
    'Mit Spotify verbunden – du kannst dieses Fenster schliessen.':
        'Подключено к Spotify — это окно можно закрыть.',
    'Spotify hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Spotify отклонил вход — это окно можно закрыть.',
    'Die nächsten Titel deiner Spotify-Warteschlange unter oder neben dem laufenden Lied. Braucht eine eigene App im Spotify-Developer-Dashboard (Client-ID) und einmal die Anmeldung im Browser; nur solange Spotify spielt.':
        'Следующие треки вашей очереди Spotify под текущей песней или рядом с ней. Нужно своё приложение в панели разработчика Spotify (Client ID) и один вход в браузере; только пока играет Spotify.',
    'Öffnet developer.spotify.com/dashboard im Browser: „Create app“, Redirect URI wie unten angegeben eintragen, die Client-ID kopieren und links einfügen.':
        'Открывает developer.spotify.com/dashboard в браузере: «Create app», введите указанный ниже redirect URI, скопируйте Client ID и вставьте слева.',
    'Vergisst die Spotify-Freigabe auf diesem PC; die Liste verschwindet. In Spotify selbst lässt sich die App unter Konto → Apps ebenfalls entfernen.':
        'Забывает согласие Spotify на этом ПК; список исчезает. В самом Spotify приложение тоже можно удалить в «Аккаунт → Приложения».',
    'Alle Arten':
        'Все виды',
    'Art':
        'Вид',
    'Clip abspielen':
        'Воспроизвести клип',
    'Clip im Editor öffnen …':
        'Открыть клип в редакторе…',
    'Im Editor öffnen …':
        'Открыть в редакторе…',
    'Datei kopieren (zum Einfügen)':
        'Копировать файл (для вставки)',
    'Zur Runde springen':
        'Перейти к раунду',
    'Farming-Runde':
        'Фарм-раунд',
    'Datei fehlt: {file}':
        'Файл отсутствует: {file}',
    '{file} kopiert – mit Strg+V z. B. in Discord einfügen.':
        '{file} скопирован — вставьте его через Ctrl+V, например в Discord.',
    'Die Aufnahme dieser Runde gibt es nicht mehr.':
        'Записи этого раунда больше нет.',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start.':
        'Нет ffmpeg (пакет imageio-ffmpeg) — start.bat установит его при следующем запуске.',
    'Öffnet den markierten Clip (auch Sofort-Clips von F8) im Clip-Editor: kürzen, zensieren, Ton mischen. Gespeichert wird ein neuer Clip, der alte bleibt.':
        'Открывает выбранный клип (в том числе мгновенные клипы F8) в редакторе клипов: обрезать, зацензурить, свести звук. Сохраняется новый клип, старый остаётся.',
    'Clip fehlt: {file}':
        'Клип отсутствует: {file}',
    'Keine Videodatei: {file}':
        'Не видеофайл: {file}',
    'Clip gelöscht: {file}':
        'Клип удалён: {file}',
    'Clip im Explorer zeigen':
        'Показать клип в проводнике',
    'Clip löschen':
        'Удалить клип',
    'Clip nicht gelöscht ({error}): {file}':
        'Клип не удалён ({error}): {file}',
    'Kein Aufnahmeordner – die Clips liegen in seinem Ordner „Clips“.':
        'Нет папки записей — клипы хранятся в её папке «Clips».',
    'Länge':
        'Длительность',
    'Noch keine Clips – „Clip bearbeiten …“ bei einer Runde oder F8 im Spiel.':
        'Клипов пока нет — «Изменить клип…» у раунда или F8 в игре.',
    'Sofort-Clip':
        'Мгновенный клип',
    'Sofort-Clips (F8)':
        'Мгновенные клипы (F8)',
    'Standbild':
        'Кадр',
    'Standbilder':
        'Кадры',
    '{n} von {total} Clips':
        'Клипы: {n} из {total}',
    'Spielt den markierten Clip im Standard-Player von Windows ab.':
        'Воспроизводит выбранный клип в плеере Windows по умолчанию.',
    'Öffnet den Explorer mit dem markierten Clip.':
        'Открывает проводник с выбранным клипом.',
    'Löscht den markierten Clip von der Platte – nach Rückfrage. Nur Dateien, die das Programm selbst angelegt hat.':
        'Удаляет выбранный клип с диска — после вопроса. Только файлы, созданные самой программой.',
    'Öffnet den Ordner „Clips“ neben den Aufnahmen im Explorer.':
        'Открывает в проводнике папку «Clips» рядом с записями.',
    'Clips':
        'Клипы',
    'Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        'Серые линии в полосах = границы (выкл.) — потяните одну, чтобы включить их',
    'mit kurzer Meldung':
        'с коротким уведомлением',
    'Clip wird gespeichert …':
        'Сохранение клипа…',
    'Die letzten {n} s aus dem Puffer von OBS':
        'Последние {n} с из буфера OBS',
    'Clip gespeichert ✓':
        'Клип сохранён ✓',
    '{n} s · im Tab Aufnahmen → Clips':
        '{n} с · на вкладке «Записи → Клипы»',
    'Kein Clip':
        'Нет клипа',
    'Zeigt beim Sofort-Clip (F8) unten rechts ein kleines Hinweisfenster – „Clip wird gespeichert …“ und danach „Clip gespeichert“ bzw. warum nicht. Auch im Spiel, ohne Ton; nimmt nie den Fokus.':
        'Показывает маленькое окно уведомления внизу справа для мгновенного клипа (F8) — «Сохранение клипа…», а затем «Клип сохранён» или почему нет. И в игре, без звука; никогда не забирает фокус.',
    'Grenzen oben und unten in den schwarzen Balken':
        'Границы сверху и снизу чёрных полос',
    'Grenzen zurücksetzen':
        'Сбросить границы',
    'Links und rechts gleich':
        'Слева и справа одинаково',
    'In jedem schwarzen Balken (links und rechts) eine Linie oben und eine unten: Karte, Systemwerte, Heute und Musik bleiben dazwischen – z. B. frei für eine FPS-Anzeige oder Benachrichtigungen. Die Karte wird bei Bedarf kleiner.':
        'Линия сверху и линия снизу в каждой чёрной полосе (слева и справа): карта, системные данные, «Сегодня» и музыка остаются между ними — например, чтобы оставить место для счётчика FPS или уведомлений. При необходимости карта уменьшается.',
    'Eine Linie ziehen bewegt die gleiche Linie im anderen Balken mit.':
        'Перетаскивание линии сдвигает ту же линию в другой полосе.',
    'Setzt alle vier Linien auf 8 % vom Rand zurück.':
        'Возвращает все четыре линии на 8 % от края.',
    'Dunkelgrauer Boden mit hellem Rand – gilt auch im Spiel.':
        'Тёмно-серый пол со светлым краем — и в игре.',
    'Dunkelgrauer Boden – die Form der Map bleibt auf dem schwarzen Balken sichtbar. Gilt auch im Spiel.':
        'Тёмно-серый пол — форма карты остаётся видна на чёрной полосе. И в игре.',
    'Dunkles Lila mit lila Rand, erinnert an die Originalfarbe – gilt auch im Spiel.':
        'Тёмно-сиреневый с сиреневым краем, близко к исходному цвету — и в игре.',
    'Durchsichtiger Boden mit dunklem Rand – gilt auch im Spiel.':
        'Прозрачный пол с тёмным краем — и в игре.',
    'Grau':
        'Серый',
    'Grau mit Rand':
        'Серый с краем',
    'Lila dunkel':
        'Тёмно-сиреневый',
    'Lila transparent':
        'Сиреневый прозрачный',
    'Lila Boden, halb durchsichtig – gilt auch im Spiel.':
        'Сиреневый пол, полупрозрачный — и в игре.',
    'Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe unsichtbar.':
        'Важно: в DBD в «Настройки → Графика» выберите режим отображения «Оконный полноэкранный». В эксклюзивном полноэкранном режиме Windows не может показать окно поверх игры — карта останется невидимой.',
    'Ungültiger Servername im Auftrag: {name}':
        'Неверное имя сервера в задании: {name}',
    'Die hosts-Datei wurde direkt nach dem Schreiben wieder verändert (Virenschutz oder ein anderes Programm?).':
        'Файл hosts снова изменился сразу после записи (антивирус или другая программа?).',
    'Keine Schreibrechte auf die hosts-Datei (Administratorrechte?).':
        'Нет разрешения на запись файла hosts (права администратора?).',
    'Aufbau der Match-Daten speichern':
        'Сохранить структуру данных матчей',
    'Öffnet die Stats-Seite so, dass das Userscript einmal den Aufbau ihrer Match-Daten im Download-Ordner speichert: nur Feldnamen und Arten, keine Werte. Damit lässt sich entscheiden, welche Daten das Programm zusätzlich auswerten könnte.':
        'Открывает страницу статистики, чтобы юзерскрипт один раз сохранил структуру своих данных матчей в папку загрузок: только имена и типы полей, без значений. Это показывает, какие ещё данные программа могла бы использовать.',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) legt danach „{file}“ in den Download-Ordner: nur die Namen und Arten der Felder, die die Seite liefert – keine Werte, keine Namen, keine IDs. Das Programm liest diese Datei nicht; du kannst sie weitergeben, um zu entscheiden, welche Felder zusätzlich übernommen werden sollen. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        'Страница статистики открывается в браузере. Затем юзерскрипт (версия {n} или новее) кладёт «{file}» в папку загрузок: только имена и виды полей, которые отправляет страница — без значений, без имён, без ID. Программа этот файл не читает; вы можете передать его, чтобы решить, какие ещё поля стоит брать. Старые юзерскрипты: сначала «Копировать юзерскрипт» и замените его в Tampermonkey.',
    'Gegner':
        'Противники',
    'Charakter':
        'Персонаж',
    'Begegnungen':
        'Встречи',
    'Geopfert':
        'Принесён в жертву',
    'Getötet':
        'Убит',
    'Aufgegeben':
        'Сдался',
    'Laut Stats-Seite: als Killer die Survivor gegen dich und wie ihr Match endete, als Survivor der Killer und wie dein Match endete. „Getötet“ = vom Killer direkt getötet (z. B. Mori), „Aufgegeben“ schließt verlassene Matches ein. „Ø Kills ohne Aufgaben“ zählt nur Matches, in denen kein Survivor aufgab oder ging. „Farming“ = Begegnungen in Farming-Runden, die „Begegnungen“ nicht zählen.':
        'Со страницы статистики: за убийцу — выжившие против вас и чем закончился их матч, за выжившего — убийца и чем закончился ваш матч. «Убит» = убит убийцей напрямую (например, мори), «Сдался» включает покинутые матчи. «Чистые ср. убийства» учитывают только матчи, в которых ни один выживший не сдался и не вышел. «Фарм» = встречи в фарм-раундах, которые «Встречи» не учитывают.',
    'Noch keine Runden mit Daten der Stats-Seite in dieser Auswahl.':
        'В этой выборке пока нет раундов с данными страницы статистики.',
    'Schnellste 4K':
        'Самый быстрый 4K',
    '{n} von {total} Runden':
        'Раунды: {n} из {total}',
    '{n} Survivor':
        'Выжившие: {n}',
    'Ø Kills ohne Aufgaben':
        'Чистые ср. убийства',
    'OBS mit DBD starten, falls es noch nicht läuft':
        'Запускать OBS вместе с DBD, если он ещё не запущен',
    'Startet DBD und ist OBS nicht erreichbar, startet das Programm OBS einmal minimiert im Infobereich – nur, wenn kein OBS-Fenster offen ist. OBS bleibt offen, wenn DBD beendet wird. OBS läuft dann mit denselben Rechten wie das Programm (Administrator).':
        'Когда DBD запускается, а OBS недоступен, программа один раз запускает OBS свёрнутым в область уведомлений — только если не открыто ни одно окно OBS. OBS остаётся открытым после закрытия DBD. OBS тогда работает с теми же правами, что и программа (администратор).',
    'OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS запущен, но недоступен — в OBS в «Сервис → Настройки сервера WebSocket» включите сервер и проверьте порт/пароль. ({error})',
    'OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio).':
        'OBS не найден — запустите OBS сами (поиск в Program Files\\obs-studio).',
    'OBS konnte nicht gestartet werden: {error}':
        'Не удалось запустить OBS: {error}',
    'OBS wird gestartet …':
        'Запуск OBS…',
    'OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS открыт, но недоступен — в OBS в «Сервис → Настройки сервера WebSocket» включите сервер и проверьте порт/пароль. ({error})',
    'Builds':
        'Сборки',
    'Build (4 Perks)':
        'Сборка (4 навыка)',
    'Perk':
        'Навык',
    'Add-on':
        'Улучшение',
    'Opfergabe':
        'Подношение',
    'Kraft/Item':
        'Способность/предмет',
    'ohne':
        'без',
    'Dein Loadout laut Stats-Seite (ab Userscript Version 3). „Ergebnis“ = als Killer Ø Kills, als Survivor Anteil entkommen; „ohne“ = dasselbe in deinen Runden derselben Rolle ohne diesen Eintrag. Builds ab {n} Runden. Embleme: Ø Stufe von keins (0) bis Iri (4); „voll“ = Kategorie mit {max} Punkten.':
        'Ваше снаряжение со страницы статистики (юзерскрипт версии 3 или новее). «Результат» = за убийцу ср. убийства, за выжившего доля побегов; «без» = то же в ваших раундах этой роли без этой позиции. Сборки — от {n} раундов. Эмблемы: ср. уровень от нет (0) до радужной (4); «полная» = категория на {max} очков.',
    'Event-Modus':
        'Режим события',
    'keins':
        'нет',
    'Bronze':
        'Бронза',
    'Silber':
        'Серебро',
    'Gold':
        'Золото',
    'Iri':
        'Радужная',
    'Emblem':
        'Эмблема',
    'Ø Stufe':
        'Ср. уровень',
    'Punktekategorie':
        'Категория очков',
    'Ø Punkte':
        'Ср. очки',
    'voll':
        'полная',
    'Killer-Wertung: {list}':
        'Рейтинг убийц: {list}',
    'Noch keine Matches mit Loadout in dieser Auswahl – die Stats-Seite liefert es ab Userscript Version 3 (Einstellungen → Match-Daten → Offizielle Match-Daten → „Userscript kopieren“).':
        'В этой выборке пока нет матчей со снаряжением — страница статистики передаёт его с юзерскрипта версии 3 (Настройки → Данные матчей → Официальные данные матчей → «Копировать юзерскрипт»).',
    'Alle Modi':
        'Все режимы',
    '„{name}“ nicht mehr als Farming-Gegner':
        '«{name}» больше не партнёр по фарму',
    '„{name}“ als Farming-Gegner (Runden mit diesem Charakter zählen als Farming)':
        '«{name}» как партнёр по фарму (раунды с этим персонажем считаются фармом)',
    '„{name}“ gilt jetzt als Farming-Gegner – {n} Runden zählen als Farming (auch ältere; Aufnahmen bleiben, wo sie sind).':
        '«{name}» теперь считается партнёром по фарму — раунды ({n}) считаются фармом (в том числе старые; записи остаются на месте).',
    '„{name}“ gilt nicht mehr als Farming-Gegner.':
        '«{name}» больше не считается партнёром по фарму.',
    'Farming-Gegner (Rechtsklick auf einen Charakter im Reiter „Gegner“): {names}':
        'Партнёры по фарму (правый щелчок по персонажу на вкладке «Противники»): {names}',
    'Gegner & Builds':
        'Противники и сборки',
    'Maps, Server & PC':
        'Карты, серверы и ПК',
    'Bloodpoints & Farming':
        'Очки крови и фарм',
    'Aufnahme markieren: abspielen, Clip schneiden, behalten, löschen – oder Rechtsklick.':
        'Выберите запись: воспроизвести, вырезать клип, сохранить, удалить — или правый щелчок.',
    'Clip markieren: abspielen, im Editor öffnen, löschen – oder Rechtsklick.':
        'Выберите клип: воспроизвести, открыть в редакторе, удалить — или правый щелчок.',
    'Filter{count}':
        'Фильтры{count}',
    'Filter zurücksetzen':
        'Сбросить фильтры',
    'Alle Filter der Statistik zurück auf „alle“ – Zeitraum, Rolle, Region, Killer, Map, Modus und „Farming ausblenden“.':
        'Все фильтры статистики обратно на «все» — период, роль, регион, убийца, карта, режим и «Скрыть фарм».',
    'Region, Killer, Map, Modus und „Farming ausblenden“ ein- oder ausklappen. Die Zahl sagt, wie viele davon gerade filtern.':
        'Показать или скрыть регион, убийцу, карту, режим и «Скрыть фарм». Число показывает, сколько из них сейчас фильтрует.',
    'Noch keine Runden gespeichert':
        'Сохранённых раундов пока нет',
    'Eine Runde zählt vom Map-Banner bis zum Rundenende (ab 1 Minute) und erscheint hier von selbst. Kills, Escapes und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'Раунд считается от баннера карты до конца раунда (от 1 минуты) и появляется здесь сам. Убийства, побеги и очки крови берутся со страницы статистики — для этого один раз настройте данные матчей.',
    'Noch keine Aufnahmen – OBS nimmt ab dem nächsten Map-Banner auf. Runden erscheinen hier, Clips (F8 oder aus dem Editor) im Reiter „Clips“.':
        'Записей пока нет — OBS записывает начиная со следующего баннера карты. Раунды появляются здесь, клипы (F8 или из редактора) — на вкладке «Клипы».',
    'Runden pro Tag – letzte {n} Tage':
        'Раунды в день — последние {n} дн.',
    '{when}: {n} Runden ({k} Killer, {s} Survivor)':
        '{when}: раунды: {n} (убийца {k}, выживший {s})',
    '1 s ab Abspielkopf':
        '1 с от позиции воспроизведения',
    '10 s ab Abspielkopf':
        '10 с от позиции воспроизведения',
    '100 % = unverändert.':
        '100 % = без изменений.',
    '3 s ab Abspielkopf':
        '3 с от позиции воспроизведения',
    '5 s ab Abspielkopf':
        '5 с от позиции воспроизведения',
    '9:16 (Hochformat)':
        '9:16 (вертикально)',
    'Alle Bilder':
        'Все изображения',
    'Alle Zeichnungen entfernen':
        'Удалить все рисунки',
    'Alles zurücksetzen':
        'Сбросить всё',
    'Anderen Ordner …':
        'Другая папка…',
    'Aufgenommen (F12)':
        'Снятые (F12)',
    'Ausschnitt':
        'Обрезка',
    'Ausschnitt {w}×{h}':
        'обрезка {w}×{h}',
    'Bearbeitet':
        'Отредактированные',
    'Bearbeitete Bilder öffnen':
        'Открыть отредактированные',
    'Bild bearbeiten – {name}':
        'Изменить изображение — {name}',
    'Bild bearbeiten …':
        'Изменить изображение…',
    'Bild gespeichert: {file}':
        'Изображение сохранено: {file}',
    'Bild im Explorer zeigen':
        'Показать изображение в проводнике',
    'Bild nicht gespeichert: {error}':
        'Изображение не сохранено: {error}',
    'Speichert …':
        'Сохранение…',
    'Bild nicht lesbar: {error}':
        'Изображение не читается: {error}',
    'Bild speichern':
        'Сохранить изображение',
    'Der Clip beginnt aus Schwarz und mit leisem Ton.':
        'Клип начинается из чёрного, звук нарастает.',
    'Der Clip endet in Schwarz, der Ton wird leiser.':
        'Клип уходит в чёрное, звук затухает.',
    'Dick':
        'Толстая',
    'Dünn':
        'Тонкая',
    'Eigener Ordner':
        'Своя папка',
    'Eigener Ordner nicht gefunden: {path}':
        'Своя папка не найдена: {path}',
    'Einblenden':
        'Появление',
    'Entfernt den markierten Kasten (Entf).':
        'Удаляет выбранную область (Del).',
    'Entfernt die markierte Zeichnung (Entf).':
        'Удаляет выбранный рисунок (Del).',
    'Farbe':
        'Цвет',
    'Farbe zurücksetzen':
        'Сбросить цвет',
    'Frei':
        'Свободно',
    'Freihand':
        'От руки',
    'GIF (ohne Ton, für Chats)':
        'GIF (без звука, для чатов)',
    'GIF {h}p, {fps} Bilder/s, ohne Ton':
        'GIF {h}p, {fps} кадров/с, без звука',
    'Helligkeit':
        'Яркость',
    'Helligkeit, Kontrast und Sättigung auf 100 %.':
        'Яркость, контраст и насыщенность обратно на 100 %.',
    'Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats).':
        'Высота GIF — меньше = меньше файл (Discord, чаты).',
    'Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern.':
        'Выделите на изображении область, которая станет нечитаемой — имена, чат, список друзей. Области можно перемещать и менять их размер за правый нижний угол.',
    'Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt sie, Entf löscht sie.':
        'Рисуйте на изображении (текст: щелчок). Щелчок по рисунку выбирает его, перетаскивание перемещает, Del удаляет.',
    'Immer':
        'Всегда',
    'In Zwischenablage':
        'В буфер обмена',
    'In die Zwischenablage kopiert – in Discord mit Strg+V einfügen.':
        'Скопировано в буфер обмена — вставьте в Discord через Ctrl+V.',
    'Ohne schwarze Ränder':
        'Без чёрных полос',
    'Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das Spielbild, „Kein Ausschnitt“ das ganze Bild.':
        'У записи есть чёрные полосы: «Без чёрных полос» сохраняет только картинку игры, «Без обрезки» — всё изображение.',
    'Kein Ausschnitt':
        'Без обрезки',
    'Kein Screenshot-Ordner von Steam für DBD gefunden – noch kein F12-Screenshot, oder Steam speichert woanders („Anderen Ordner …“).':
        'Папка скриншотов Steam для DBD не найдена — скриншотов F12 ещё нет, или Steam сохраняет их в другое место («Другая папка…»).',
    'Kontrast':
        'Контраст',
    'Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C).':
        'Копирует отредактированное изображение — вставьте в Discord через Ctrl+V (Ctrl+C).',
    'Kreis':
        'Эллипс',
    'Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen':
        'Пробел — воспр. · ←/→ 1 с · Shift 5 с · Ctrl 1 кадр · I/O начало/конец · A часть · M метка · Home/End начало/конец · Del удаляет область/рисунок · Esc закрыть',
    'Letzten Schritt zurücknehmen (Strg+Z).':
        'Отменить последний шаг (Ctrl+Z).',
    'Linie':
        'Линия',
    'Links und rechts tauschen.':
        'Поменять местами лево и право.',
    'Mittel':
        'Средняя',
    'Oben und unten tauschen.':
        'Поменять местами верх и низ.',
    'Ordner mit deinen Screenshots':
        'Папка с вашими скриншотами',
    'Ordner nicht anlegbar: {error}':
        'Не удаётся создать папку: {error}',
    'PNG: verlustfrei · JPG: kleinere Datei.':
        'PNG: без потерь · JPG: файл меньше.',
    'Pfeil':
        'Стрелка',
    'Rahmen':
        'Прямоугольник',
    'Rahmen bearbeiten':
        'Изменить рамку',
    'Rahmen im Bild ziehen, verschieben, an den Ecken ändern.':
        'Растяните рамку на изображении, перемещайте её, меняйте за углы.',
    'Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. Nochmal drücken beendet das Werkzeug.':
        'Перемещайте рамку в предпросмотре или тяните её углы, чтобы увеличить/уменьшить. Нажмите снова, чтобы завершить инструмент.',
    'Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen.':
        'Вырезает область из изображения — 9:16 для YouTube Shorts и TikTok, 1:1 для Instagram. Перемещайте рамку в предпросмотре и тяните её углы.',
    'Screenshots':
        'Скриншоты',
    'Sehr dick':
        'Очень толстая',
    'Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den Ecken ziehen.':
        'Соотношение сторон обрезки; перемещайте рамку на изображении и тяните её углы.',
    'Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im Screenshot-Ordner von Steam) bleibt unverändert (Strg+S).':
        'Сохраняет отредактированную копию в папке Fog Scout — оригинал (например, в папке скриншотов Steam) остаётся как есть (Ctrl+S).',
    'Steam (F12)':
        'Steam (F12)',
    'Steam-Ordner verwenden':
        'Использовать папку Steam',
    'Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf Markiertes löschen · Esc schliessen':
        'Ctrl+Z отменить · Ctrl+Y повторить · Ctrl+C копировать · Ctrl+S сохранить · Del удаляет выбранное · Esc закрыть',
    'Strichstärke bzw. Textgrösse.':
        'Толщина линии или размер текста.',
    'Sättigung':
        'Насыщенность',
    'Tempo':
        'Темп',
    'Text':
        'Текст',
    'Text für das Text-Werkzeug':
        'Текст для инструмента «Текст»',
    'Um 90° gegen den Uhrzeigersinn drehen.':
        'Повернуть на 90° против часовой стрелки.',
    'Um 90° im Uhrzeigersinn drehen.':
        'Повернуть на 90° по часовой стрелке.',
    'Verwirft alle Änderungen – das Original bleibt ohnehin unverändert.':
        'Отбрасывает все изменения — оригинал в любом случае остаётся как есть.',
    'Wie der Bereich unkenntlich wird.':
        'Как область делается нечитаемой.',
    'Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des Abspielkopfs. Gilt für neue und für die markierte Zeichnung.':
        'Как долго рисунок виден в клипе — начиная с позиции воспроизведения. Для новых рисунков и выбранного.',
    'Zeichnen':
        'Рисовать',
    'Zeichnung entfernen':
        'Удалить рисунок',
    'Zeigt das zuletzt gespeicherte Bild im Explorer.':
        'Показывает последнее сохранённое изображение в проводнике.',
    'Zurückgenommenen Schritt wiederholen (Strg+Y).':
        'Повторить отменённый шаг (Ctrl+Y).',
    'Zuschneiden':
        'Обрезать',
    'neu kodiert (wie „Genau“)':
        'перекодировано (как «Точно»)',
    'normal':
        'обычный',
    '{n} Abschnitt(e), {length} s':
        'Частей: {n}, {length} с',
    '{w} × {h} Pixel · Original bleibt unverändert':
        '{w} × {h} пикселей · оригинал остаётся как есть',
    '↶ Rückgängig':
        '↶ Отменить',
    '↷ Wiederholen':
        '↷ Повторить',
    '⇅ Kippen':
        '⇅ Отразить',
    '⇆ Spiegeln':
        '⇆ Зеркально',
    '⟲ Links drehen':
        '⟲ Повернуть влево',
    '⟳ Rechts drehen':
        '⟳ Повернуть вправо',
    'Öffnet das markierte Bild im Bild-Editor: zuschneiden, drehen, Pfeile und Text, zensieren, Farbe – gespeichert wird eine Kopie, das Original bleibt.':
        'Открывает выбранное изображение в редакторе изображений: обрезка, поворот, стрелки и текст, цензура, цвет — сохраняется копия, оригинал остаётся.',
    'Zeigt die Bilddatei im Explorer.':
        'Показывает файл изображения в проводнике.',
    'Öffnet den Ordner mit den bearbeiteten Bildern (Screenshots neben den Aufnahmen bzw. Bilder/Fog Scout).':
        'Открывает папку с отредактированными изображениями (Screenshots рядом с записями или Изображения/Fog Scout).',
    'Bilder aus einem eigenen Ordner zeigen – z. B. wenn Steam die Screenshots unkomprimiert in einen anderen Ordner speichert.':
        'Показывать изображения из своей папки — например, если Steam сохраняет несжатые скриншоты в другую папку.',
    'Wieder die Screenshots aus Steams Ordner für DBD zeigen (F12 im Spiel).':
        'Снова показывать скриншоты из папки DBD в Steam (F12 в игре).',
    'Bild anklicken: bearbeiten (zuschneiden, zeichnen, zensieren), im Explorer zeigen – Doppelklick öffnet den Editor.':
        'Щёлкните изображение: изменить (обрезать, рисовать, зацензурить), показать в проводнике — двойной щелчок открывает редактор.',
    'F12 im Spiel ist Steams Screenshot-Taste; das Programm liest Steams Ordner nur. Bearbeitete Bilder sind Kopien im Ordner „Screenshots“ neben den Aufnahmen.':
        'F12 в игре — клавиша скриншотов Steam; программа только читает папку Steam. Отредактированные изображения — копии в папке «Screenshots» рядом с записями.',
    '1 Bild':
        '1 изображение',
    '{n} Bilder':
        'Изображения: {n}',
    '★ behalten (nie aufgeräumt) · ⚑ Marken (F8 in der Runde) · ▶ auf YouTube · Rechtsklick auf die Spaltenköpfe: Spalten ein-/ausblenden':
        '★ сохраняется (никогда не удаляется) · ⚑ метки (F8 в раунде) · ▶ на YouTube · правый щелчок по заголовкам: показать/скрыть столбцы',
    'Clips aus dem Editor, Sofort-Clips (F8) und Standbilder, mit ihrer Runde · ▶ auf YouTube · gelöscht werden nur Dateien, die das Programm selbst angelegt hat':
        'Клипы из редактора, мгновенные клипы (F8) и кадры с их раундом · ▶ на YouTube · удаляются только файлы, созданные самой программой',
    'Status':
        'Статус',
    'Schnell (ohne Neukodieren)':
        'Быстро (без перекодирования)',
    'Genau (neu kodiert)':
        'Точно (с перекодированием)',
    'Für Discord (Zielgrösse)':
        'Для Discord (целевой размер)',
    'GIF (ohne Ton)':
        'GIF (без звука)',
    'Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als Video speichern.':
        'GIF длится не более {limit} с, этот клип — {seconds} с: сократите его или сохраните как видео.',
    'beim Beenden abgebrochen':
        'остановлено при выходе из программы',
    'Update gesperrt: ein Clip wird noch gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'Обновление заблокировано: клип ещё сохраняется. Потом снова нажмите «Обновить и перезапустить».',
    '(gerade {n})':
        '(сейчас {n})',
    'Aufnahme gestartet':
        'Запись начата',
    'Aufnahme läuft weiter':
        'Запись возобновлена',
    'Aufnahme läuft weiter.':
        'Запись возобновлена.',
    'Aufnahme pausieren/weiter':
        'Пауза/продолжение записи',
    'Aufnahme pausiert':
        'Запись на паузе',
    'Aufnahme pausiert.':
        'Запись на паузе.',
    'Aufnahme starten':
        'Начать запись',
    'Aufnahme starten/stoppen':
        'Начать/остановить запись',
    'Aufnahme stoppen':
        'Остановить запись',
    'Aufnahme von Hand gestartet.':
        'Запись начата вручную.',
    'Aufnahme wird beendet …':
        'Остановка записи…',
    'Aufnahme-Laufwerk fast voll – Aufnahme beendet':
        'Диск для записей почти заполнен — запись остановлена',
    'Aufnahme-Laufwerk fast voll – nichts gestartet':
        'Диск для записей почти заполнен — ничего не запущено',
    'Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet':
        'Диск для записей не подключён — ничего не запущено',
    'Aufnahmen sind aus.':
        'Записи выключены.',
    'Ausgewogen':
        'Сбалансированно',
    'Automatisch':
        'Автоматически',
    'Bereit':
        'Готово',
    'Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert.':
        'Высота изображения клипа — если меньше записи, изображение уменьшается, но никогда не увеличивается.',
    'CPU (x264/x265)':
        'CPU (x264/x265)',
    'Clip speichern (F8)':
        'Сохранить клип (F8)',
    "Der Sofort-Clip (F8) ist auf {clip} s eingestellt, OBS' Wiederholungspuffer hält nur {buf} s – in OBS: Einstellungen → Ausgabe → Wiederholungspuffer → Maximale Wiederholungszeit.":
        'Мгновенный клип (F8) задан на {clip} с, но буфер повтора OBS хранит только {buf} с — в OBS: Настройки → Вывод → Буфер повтора → Максимальное время повтора.',
    'Die Datei erscheint im Tab Aufnahmen':
        'Файл появится на вкладке «Записи»',
    'Es läuft schon eine Aufnahme':
        'Запись уже идёт',
    'H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel kleiner, braucht aber einen neueren Player.':
        'H.264 воспроизводится везде; HEVC (H.265) примерно на треть меньше при том же качестве, но нужен более новый плеер.',
    'Hoch':
        'Высокое',
    'Kein Aufnahmeordner gewählt – Einstellungen → Aufnahmen.':
        'Папка записей не выбрана — «Настройки → Записи».',
    'Keine Aufnahme':
        'Нет записи',
    'Keine Aufnahme läuft':
        'Запись не идёт',
    'Keine Aufnahme läuft.':
        'Запись не идёт.',
    'Kodiere {file} … ({how}, dauert etwas)':
        'Кодирование {file}… ({how}, занимает время)',
    'Kodierung':
        'Кодирование',
    'Marke setzen':
        'Поставить метку',
    'Nimmt auf':
        'Идёт запись',
    'Nimmt auf (von Hand gestartet)':
        'Идёт запись (начата вручную)',
    'Nimmt die Runde in der laufenden Aufnahme auf':
        'Запись раунда внутри идущей записи',
    'OBS lässt Bilder aus ({n} von {total}, Kodierer überlastet) – in OBS Voreinstellung oder Auflösung senken.':
        'OBS пропускает кадры ({n} из {total}, кодировщик перегружен) — понизьте предустановку или разрешение в OBS.',
    'OBS nicht erreichbar':
        'OBS недоступен',
    'OBS starten, WebSocket-Server einschalten, Port/Passwort prüfen (Einstellungen → Verbindungen → OBS-Verbindung → Verbindung testen). {why}':
        'Запустите OBS, включите его сервер WebSocket, проверьте порт/пароль (Настройки → Подключения → Подключение к OBS → Проверить подключение). {why}',
    'OBS verpasst Bilder beim Rendern ({n} von {total}, Grafikkarte ausgelastet).':
        'OBS теряет кадры при рендеринге ({n} из {total}, видеокарта занята).',
    'Pause':
        'Пауза',
    'Pausiert':
        'На паузе',
    'Schnell':
        'Быстро',
    'Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. Hoch: grösser, nahe am Original.':
        'Быстро: меньше и быстрее, заметно мягче. Сбалансированно: как раньше. Высокое: больше, близко к оригиналу.',
    'Stoppen mit demselben Hotkey oder im Tab Aufnahmen':
        'Остановить — той же горячей клавишей или на вкладке «Записи»',
    'Warte auf OBS …':
        'Ожидание OBS…',
    'Wie aufgenommen':
        'Как записано',
    'Wiederholungspuffer aus':
        'Буфер повтора выключен',
    'Wiederholungspuffer in OBS nicht aktiviert':
        'Буфер повтора в OBS не включён',
    'Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; „Automatisch“ nimmt die erste, die geht.':
        'Чем кодируется клип: видеокарта (NVENC, AMF, Quick Sync — только если ffmpeg действительно может её здесь использовать) почти не нагружает процессор; «Автоматически» берёт первый работающий вариант.',
    'letzter Clip {file} (vor {age})':
        'последний клип {file} ({age} назад)',
    'Fortsetzen':
        'Продолжить',
    'von Hand gestartet':
        'начата вручную',
    'von OBS selbst gestartet':
        'начата в самом OBS',
    'Beendet die laufende Aufnahme jetzt (bei einer Runde ohne Nachlauf) und legt sie in den Aufnahmeordner.':
        'Сразу останавливает идущую запись (раунд без хвоста) и кладёт её в папку записей.',
    'Hält die laufende Aufnahme an (OBS pausiert); „Fortsetzen“ setzt sie in derselben Datei fort. Marken bleiben an ihrer Stelle.':
        'Ставит идущую запись на паузу (OBS приостанавливает); «Продолжить» продолжает её в том же файле. Метки сохраняют своё место.',
    'Merkt diesen Moment in der laufenden Aufnahme (⚑) – der Clip-Editor springt später dorthin. Ohne Sofort-Clip.':
        'Отмечает этот момент в идущей записи (⚑) — редактор клипов потом переходит туда. Без мгновенного клипа.',
    'Setzt die pausierte Aufnahme fort.':
        'Продолжает приостановленную запись.',
    'Startet jetzt eine OBS-Aufnahme von Hand – auch ausserhalb einer Runde. Sie läuft, bis du sie stoppst oder DBD beendet wird; ein Map-Banner benennt sie. Hotkey einstellbar.':
        'Сразу начинает запись OBS вручную — и вне раунда. Она идёт, пока вы её не остановите или не закроется DBD; баннер карты даёт ей имя. Горячая клавиша настраивается.',
    'Wie F8: speichert die letzten Sekunden aus dem OBS-Wiederholungspuffer als Sofort-Clip (Länge unter Einstellungen → Aufnahmen) und setzt eine Marke, falls eine Aufnahme läuft.':
        'Как F8: сохраняет последние секунды буфера повтора OBS как мгновенный клип (длительность — в «Настройки → Записи») и ставит метку, если идёт запись.',
    '1 Eintrag':
        '1 запись',
    '{n} Einträge':
        'Записи: {n}',
    '5 Sekunden vor (Shift+→).':
        '5 секунд вперёд (Shift+→).',
    '5 Sekunden zurück (Shift+←).':
        '5 секунд назад (Shift+←).',
    'Auf der Zeitleiste öffnen':
        'Открыть на шкале времени',
    'Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s':
        'Запись {start} – {end} · на шкале времени с {at} · {length} с',
    'Auswahl':
        'Выбор',
    'Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).':
        'Размыть области — имена, чат, список друзей (X).',
    'Bibliothek':
        'Библиотека',
    'Bibliothek ein-/ausblenden.':
        'Показать/скрыть библиотеку.',
    'Bildausschnitt – den Rahmen in der Vorschau ziehen (C).':
        'Обрезка — тяните рамку в окне просмотра (C).',
    'Clip entfernt – die Aufnahme bleibt, wie sie ist.':
        'Клип удалён — запись остаётся как есть.',
    'Clip geteilt – jetzt {n} Clips.':
        'Клип разрезан — теперь клипов: {n}.',
    'Clip {n} von {total}':
        'Клип {n} из {total}',
    'Clips auf der Zeitleiste wählen, verschieben und trimmen (V).':
        'Выбирать, перемещать и обрезать клипы на шкале времени (V).',
    'Den ganzen Schnitt einpassen (Strg+0).':
        'Вместить весь монтаж (Ctrl+0).',
    'Der Clip unter dem Abspielkopf beginnt hier (Taste I).':
        'Клип под позицией воспроизведения начинается здесь (клавиша I).',
    'Der Clip unter dem Abspielkopf endet hier (Taste O).':
        'Клип под позицией воспроизведения заканчивается здесь (клавиша O).',
    'Diese Aufnahme ist schon auf der Zeitleiste.':
        'Эта запись уже на шкале времени.',
    'Ein Bild vor (Strg+→); → eine Sekunde.':
        'На кадр вперёд (Ctrl+→); → на секунду.',
    'Ein Bild zurück (Strg+←); ← eine Sekunde.':
        'На кадр назад (Ctrl+←); ← на секунду.',
    'Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt.':
        'Удаляет выбранный клип со шкалы времени (Del) — запись остаётся.',
    'Export':
        'Экспорт',
    'Exportieren':
        'Экспорт',
    'Fog Scout · Editor':
        'Fog Scout · Редактор',
    'Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze.':
        'Здесь нечего разрезать — позиция воспроизведения на краю клипа.',
    'Hier teilen':
        'Разрезать здесь',
    'Inspector':
        'Инспектор',
    'Inspector ein-/ausblenden.':
        'Показать/скрыть инспектор.',
    'Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine andere Videodatei.':
        'Записей нет — записи OBS и клипы появляются здесь, «Импорт» добавляет другой видеофайл.',
    'Keine Clips auf der Zeitleiste.':
        'На шкале времени нет клипов.',
    'Kürzeste zuerst':
        'Сначала короткие',
    'Lautstärke der Vorschau (nicht des Clips).':
        'Громкость предпросмотра (не клипа).',
    '? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export':
        '? все сочетания · Пробел воспр. · ←/→ 1 с · Shift 5 с · Ctrl или ,/. 1 кадр · I/O клип начинается/заканчивается здесь · S разрезать · Del удалить · Ctrl+Z/Y отменить/повторить · F полный экран · Ctrl+S проект · Ctrl+E экспорт',
    'Längste zuerst':
        'Сначала длинные',
    'Löschen':
        'Удалить',
    'Name A–Z':
        'Имя А–Я',
    'Name des Projekts – auch der Name des exportierten Clips.':
        'Название проекта — оно же имя экспортированного клипа.',
    'Neueste zuerst':
        'Сначала новые',
    'Pause (Leertaste)':
        'Пауза (пробел)',
    'Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D).':
        'Рисовать на изображении стрелки, прямоугольники, от руки и текст (D).',
    'Projekt':
        'Проект',
    'Projekt geladen: {name}':
        'Проект загружен: {name}',
    'Projekt gespeichert: {file}':
        'Проект сохранён: {file}',
    'Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten.':
        'Сохранить проект (Ctrl+S) — монтаж, обрезку, рисунки, цензуру и настройки экспорта этой записи, чтобы продолжить позже.',
    'Runde':
        'Раунд',
    'Rückgängig (Strg+Z).':
        'Отменить (Ctrl+Z).',
    'Rückgängig.':
        'Отменено.',
    'Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen (Strg+E) – Format und Kodierung im Inspector unter Export.':
        'Записывает монтаж как клип в папку «Clips» рядом с записями (Ctrl+E) — формат и кодирование в инспекторе в разделе «Экспорт».',
    'Sichtbar':
        'Видимость',
    'Sortierung der Bibliothek.':
        'Порядок библиотеки.',
    'Spielt den ganzen Schnitt von vorn ab und springt danach zurück.':
        'Воспроизводит весь монтаж с начала и затем возвращается назад.',
    'Standbild am Abspielkopf als PNG neben den Clips speichern.':
        'Сохранить кадр на позиции воспроизведения как PNG рядом с клипами.',
    'Stärke':
        'Толщина',
    'Teilen':
        'Разрезать',
    'Teilt den Clip unter dem Abspielkopf in zwei (Taste S).':
        'Разрезает клип под позицией воспроизведения на два (клавиша S).',
    'Ton der Vorschau an/aus (Windows).':
        'Звук предпросмотра вкл./выкл. (Windows).',
    'Videodatei importieren':
        'Импорт видеофайла',
    'Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie eine Aufnahme öffnen.':
        'Импортировать видеофайл — он появится в библиотеке и открывается как запись.',
    'Videos':
        'Видео',
    'Vollbild – nur die Vorschau (F, Esc beendet).':
        'Полный экран — только окно просмотра (F, Esc завершает).',
    'Wiederholen (Strg+Y).':
        'Повторить (Ctrl+Y).',
    'Wiederholt.':
        'Повторено.',
    'Zeitleiste':
        'Шкала времени',
    'Zeitleiste ein-/ausblenden.':
        'Показать/скрыть шкалу времени.',
    'Zeitleiste einpassen':
        'Вместить шкалу',
    'Zeitleiste herauszoomen (−, Strg+Mausrad).':
        'Уменьшить масштаб шкалы времени (−, Ctrl+колесо).',
    'Zeitleiste hineinzoomen (+, Strg+Mausrad).':
        'Увеличить масштаб шкалы времени (+, Ctrl+колесо).',
    'Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit.':
        'Замедление или ускорение для выбранного клипа. Звук следует за ним.',
    'Zum Anfang (Pos1).':
        'В начало (Home).',
    'Zum Ende (Ende).':
        'В конец (End).',
    '{at} liegt in keinem Clip der Zeitleiste.':
        '{at} не попадает ни в один клип шкалы времени.',
    '{n} Clip(s) · {length} s':
        'Клипов: {n} · {length} с',
    'Älteste zuerst':
        'Сначала старые',
    'Öffnen aus der Bibliothek ist hier nicht verfügbar.':
        'Открытие из библиотеки здесь недоступно.',
    'Fehler in {step} – siehe Log.':
        'Ошибка в {step} — см. журнал.',
    'Strg+{n}':
        'Ctrl+{n}',
    'Tastenkürzel':
        'Сочетания клавиш',
    'Schliessen (? oder Esc)':
        'Закрыть (? или Esc)',
    'Wiedergabe':
        'Воспроизведение',
    'Werkzeuge':
        'Инструменты',
    'Leertaste':
        'Пробел',
    'Abspielen / Anhalten':
        'Воспроизведение / пауза',
    '1 Sekunde zurück / vor':
        'На 1 секунду назад / вперёд',
    'Shift+← / →':
        'Shift+← / →',
    '5 Sekunden zurück / vor':
        'На 5 секунд назад / вперёд',
    'Strg+← / →  ·  , / .':
        'Ctrl+← / →  ·  , / .',
    '1 Bild zurück / vor':
        'На 1 кадр назад / вперёд',
    'Pos1 / Ende':
        'Home / End',
    'Zum Anfang / zum Schluss':
        'В начало / в конец',
    'Zur nächsten Marke':
        'К следующей метке',
    'Untertitel {a}–{b}.':
        'Субтитр {a}–{b}.',
    '{file} wartet – {n} Export(e) davor.':
        '{file} ждёт — перед ним экспортов: {n}.',
    'Kodiere {file} …':
        'Кодирование {file}…',
    'Titel & Vorschaubild':
        'Заголовок и миниатюра',
    'Claude fragt: {question}':
        'Claude спрашивает: {question}',
    'Deine Antwort …':
        'Ваш ответ…',
    'Name der Vorlage':
        'Название шаблона',
    'Als Vorlage speichern':
        'Сохранить как шаблон',
    'Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen.':
        'Сохраняет только что выполненные шаги (без областей цензуры) как шаблон — время от начала или от конца, чтобы они подходили и к другим длительностям.',
    'Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, kostenlos; erst „Übernehmen“ ändert den Schnitt.':
        'Предлагает шаги шаблона для этого монтажа — без Claude, бесплатно; монтаж меняет только «Применить».',
    'Vorlage löschen':
        'Удалить шаблон',
    'Entfernt die gewählte Vorlage.':
        'Удаляет выбранный шаблон.',
    'Bitte einen Namen für die Vorlage eingeben.':
        'Введите название шаблона.',
    'Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu).':
        'Нет ничего, что годится для шаблона (области цензуры в него не входят).',
    'Vorlage „{name}“ gespeichert.':
        'Шаблон «{name}» сохранён.',
    'Vorlage „{name}“':
        'Шаблон «{name}»',
    'Vorlage „{name}“ gelöscht.':
        'Шаблон «{name}» удалён.',
    'Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts wird hochgeladen.':
        'Отправляет Claude те же восемь кадров, что и «Проверить экспорт»; Claude выбирает лучшую миниатюру и предлагает заголовок. Заголовок вы берёте сами, миниатюра только сохраняется как изображение в «Clips» — ничего не загружается.',
    'Claude sucht unter {n} Standbildern ein Vorschaubild …':
        'Claude выбирает миниатюру среди кадров ({n})…',
    'Als Short-Titel: „{title}“':
        'Как заголовок Short: «{title}»',
    'Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für YouTube kopierst du ihn selbst.':
        'Берёт заголовок как заголовок Short (один шаг отмены). Для YouTube скопируйте его сами.',
    'Vorschaubild bei {at} speichern':
        'Сохранить миниатюру в {at}',
    'Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im Export, mit dem Titel. Hochgeladen wird nichts.':
        'Сохраняет этот кадр в полном размере как PNG в «Clips» — с цензурой, как в экспорте, и с заголовком. Ничего не загружается.',
    'Short-Titel übernommen.':
        'Заголовок Short принят.',
    'Vorschaubild':
        'Миниатюра',
    'Export prüfen':
        'Проверить экспорт',
    'Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf einen Fund springt hin und schlägt einen Zensurkasten vor.':
        'Отправляет Claude восемь кадров готового монтажа (обрезанных как в экспорте, с применённой цензурой); Claude сообщает о ещё читаемых именах или чате и обо всём прочем, чем не стоит так делиться. Щелчок по находке переходит туда и предлагает область цензуры.',
    'Claude prüft {n} Standbilder des fertigen Schnitts …':
        'Claude проверяет кадры готового монтажа ({n})…',
    'Claude hat nichts gefunden, das so nicht geteilt werden sollte.':
        'Claude не нашёл ничего, чем не стоит так делиться.',
    'Springt hin und schlägt einen Zensurkasten für diese Stelle vor.':
        'Переходит туда и предлагает область цензуры для этого места.',
    'Springt hin.':
        'Переходит туда.',
    'Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.':
        'Предложение в {at} — «Принять предложения» скрывает это место.',
    'Name lesbar':
        'Читается имя',
    'Chat lesbar':
        'Читается чат',
    'Auffällig':
        'Бросается в глаза',
    'Text finden':
        'Найти текст',
    'Sucht auf dem Bild am Abspielkopf nach Text (Namen, Chat) – auf diesem PC, nichts wird gesendet. Die Fundstellen erscheinen nummeriert.':
        'Ищет текст (имена, чат) на изображении в позиции воспроизведения — на этом ПК, ничего не отправляется. Находки появляются пронумерованными.',
    'Vorschläge übernehmen':
        'Принять предложения',
    'Macht aus den nummerierten Fundstellen Zensurkästen (ein Schritt zum Rückgängigmachen).':
        'Превращает пронумерованные находки в области цензуры (один шаг отмены).',
    'Vorschläge verwerfen':
        'Отбросить предложения',
    'Claude: nur Namen':
        'Claude: только имена',
    'Schickt das Standbild (zensierte Bereiche bleiben zensiert) mit den nummerierten Fundstellen an Claude; Claude nennt nur die Nummern, die Namen oder Chat zeigen – die übrigen Vorschläge fallen weg.':
        'Отправляет Claude кадр (зацензуренные области остаются зацензуренными) с пронумерованными находками; Claude называет только номера, на которых имена или чат — остальные предложения убираются.',
    'Die Texterkennung ist in dieser Installation nicht vorhanden.':
        'Распознавание текста недоступно в этой установке.',
    'Suche Text im Bild …':
        'Поиск текста на изображении…',
    'Das Bild liess sich nicht nach Text durchsuchen.':
        'Не удалось найти текст на изображении.',
    'Kein Text gefunden, der nicht schon verdeckt ist.':
        'Не найдено текста, который ещё не скрыт.',
    '{n} Textstellen gefunden – „Vorschläge übernehmen“ verdeckt sie.':
        'Найдено мест с текстом: {n} — «Принять предложения» скрывает их.',
    '{n} Kästen gesetzt.':
        'Поставлено областей: {n}.',
    'Claude sieht sich {n} Fundstellen an …':
        'Claude смотрит находки ({n})…',
    'Claude hält keine Fundstelle für einen Namen oder Chat.':
        'Claude считает, что ни одна находка не является именем или чатом.',
    '{n} Fundstellen zeigen laut Claude Namen oder Chat.':
        'По словам Claude, находок с именами или чатом: {n}.',
    'Kasten ab hier':
        'Область отсюда',
    'Kasten bis hier':
        'Область до сюда',
    'Kasten immer':
        'Область всегда',
    'Der markierte Kasten gilt erst ab dem Bild am Abspielkopf – z. B. wenn ein Name erst später erscheint.':
        'Выбранная область действует только с изображения в позиции воспроизведения — например, если имя появляется только позже.',
    'Der markierte Kasten gilt nur bis zum Bild am Abspielkopf.':
        'Выбранная область действует только до изображения в позиции воспроизведения.',
    'Der markierte Kasten gilt wieder für die ganze Aufnahme.':
        'Выбранная область снова действует для всей записи.',
    'Kasten {n} gilt von {a} bis {b} der Aufnahme.':
        'Область {n} действует с {a} по {b} записи.',
    'Kasten {n} gilt für die ganze Aufnahme.':
        'Область {n} действует для всей записи.',
    'Am Anfang der Aufnahme gibt es kein „bis hier“.':
        'В начале записи нет «до сюда».',
    '{n} davon nur zeitweise.':
        'Из них только на время: {n}.',
    'Zurückspringen / Anhalten / Abspielen – L mehrmals: ×2, ×4':
        'Назад / стоп / воспроизведение — ещё раз L: ×2, ×4',
    'Vollbild an / aus':
        'Полный экран вкл./выкл.',
    'Clip beginnt / endet am Abspielkopf':
        'Клип начинается / заканчивается на позиции воспроизведения',
    'S oder Strg+B':
        'S или Ctrl+B',
    'Clip am Abspielkopf teilen':
        'Разрезать клип на позиции воспроизведения',
    'Entf':
        'Del',
    'Markierten Clip löschen':
        'Удалить выбранный клип',
    'Hinein- / herauszoomen':
        'Приблизить / отдалить',
    'Strg+0':
        'Ctrl+0',
    'Ganze Zeitleiste zeigen':
        'Показать всю шкалу времени',
    'Auswählen':
        'Выбор',
    'Bildausschnitt':
        'Обрезка',
    'Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie':
        'Отменить, выйти из инструмента или снять выделение — никогда не закрывает',
    'Strg+W':
        'Ctrl+W',
    'Editor schliessen':
        'Закрыть редактор',
    'Abgebrochen.':
        'Отменено.',
    'Esc schliesst den Editor nicht – schliessen mit × oder Strg+W.':
        'Esc не закрывает редактор — закройте его через × или Ctrl+W.',
    'Strg+Z / Strg+Y':
        'Ctrl+Z / Ctrl+Y',
    'Rückgängig / Wiederholen':
        'Отменить / повторить',
    'Strg+S':
        'Ctrl+S',
    'Projekt speichern':
        'Сохранить проект',
    'Strg+E':
        'Ctrl+E',
    'Diese Übersicht ein / aus':
        'Этот обзор вкл./выкл.',
    'In der Statistik zeigen':
        'Показать в статистике',
    'Aufnahme dieser Runde öffnen':
        'Открыть запись этого раунда',
    'Runde markieren: Rolle, Farming, Killer oder Map korrigieren, löschen – oder Rechtsklick. Doppelklick zeigt die Aufnahme.':
        'Выберите раунд: исправить роль, фарм, убийцу или карту, удалить — или правый щелчок. Двойной щелчок показывает запись.',
    'OBS-Passwort ist auf diesem PC/Benutzerkonto nicht lesbar – bitte neu eingeben.':
        'Пароль OBS не удаётся прочитать на этом ПК/в этой учётной записи — введите его снова.',
    'Als neues Projekt speichern':
        'Сохранить как новый проект',
    'Autosave aus':
        'Автосохранение выкл.',
    'Bereich übernehmen':
        'Взять диапазон',
    'Bereich übernommen – Strg+Z stellt das Projekt wieder her.':
        'Диапазон взят — Ctrl+Z возвращает проект.',
    'Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. Deine Fassung liegt unter Sicherungen und lokal.':
        'Проект был изменён вне Fog Scout или существует дважды. Ваша версия сохранена в Sicherungen и локально.',
    'Die Aufnahme konnte nicht geprüft werden.':
        'Не удалось проверить запись.',
    'Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz herunterladen.':
        'Запись есть только в облаке — для проверки пришлось бы скачать её целиком.',
    'Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt ist anders). Es wurde nicht geladen.':
        'Запись не совпадает с сохранённым проектом (у неё другое содержимое). Она не загружена.',
    'Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt.':
        'Клипы проекта не читаются — показан клип по умолчанию.',
    'Die Projektdatei ist unlesbar und wurde nicht geladen.':
        'Файл проекта не читается и не загружен.',
    'Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist lokal gesichert.':
        'Файл проекта удалён или перемещён вне Fog Scout. Ваше состояние сохранено локально.',
    'Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.':
        'Файл проекта переименован. Ваше состояние сохранено локально.',
    'Dieses Projekt ist schon in einem anderen Fenster offen – hier wird nichts gespeichert.':
        'Этот проект уже открыт в другом окне — здесь ничего не сохраняется.',
    'Editor-Projekte automatisch speichern':
        'Автоматически сохранять проекты редактора',
    'Editor-Projekte nicht gesichert':
        'Проекты редактора не сохранены',
    'Editor-Projekte werden noch gesichert …':
        'Проекты редактора ещё сохраняются…',
    'Editor: automatisches Speichern an.':
        'Редактор: автосохранение включено.',
    'Editor: automatisches Speichern aus – Strg+S speichert das Projekt.':
        'Редактор: автосохранение выключено — Ctrl+S сохраняет проект.',
    'Eine wählen …':
        'Выберите…',
    'Erneut prüfen':
        'Проверить снова',
    'Es gibt ein Projekt zu einer gleichnamigen, aber veränderten Aufnahme.':
        'Есть проект для записи с тем же именем, которая изменилась.',
    'Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine Clips.':
        'У этой записи есть сохранённый проект (клипов: {n}). Если взять диапазон из предпросмотра ({a}–{b}), он заменит его клипы.',
    'Gespeichertes Projekt gefunden – die Aufnahme wird geprüft.':
        'Найден сохранённый проект — запись проверяется.',
    'Kein Projekt':
        'Нет проекта',
    'Kein Projekt – Strg+S legt ein neues an.':
        'Нет проекта — Ctrl+S создаёт новый.',
    'Keine öffnen':
        'Не открывать',
    'Laden':
        'Загрузить',
    'Lokal gesicherter Stand eines fehlenden Projekts gefunden.':
        'Найдено локально сохранённое состояние отсутствующего проекта.',
    'Mindestens ein Editor-Stand ist weder im Projekt noch lokal gesichert (Speichern hängt oder der Ordner ist nicht erreichbar). Trotzdem beenden? Die ungesicherten Änderungen gehen dann verloren.':
        'Как минимум одно состояние редактора не сохранено ни в проекте, ни локально (сохранение зависло или папка недоступна). Всё равно выйти? Несохранённые изменения тогда будут потеряны.',
    'Neu beginnen':
        'Начать заново',
    'Neuerer Stand aus der lokalen Rettungskopie geladen.':
        'Загружено более новое состояние из локальной резервной копии.',
    'Neues Projekt':
        'Новый проект',
    'Nicht laden':
        'Не загружать',
    'Nicht schliessen':
        'Не закрывать',
    'Nicht wiederherstellen':
        'Не восстанавливать',
    'Nichts tun':
        'Ничего не делать',
    'Ohne Prüfung laden':
        'Загрузить без проверки',
    'Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, gleiche Grösse).':
        'Найден проект из Fog Scout 1.17 или старше (то же имя, тот же размер).',
    'Projekt aus neuerer Version – wird nicht überschrieben':
        'Проект из более новой версии — не перезаписан',
    'Projekt behalten':
        'Оставить проект',
    'Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen.':
        'Проект открыт — диапазон из предпросмотра не взят.',
    'Projekt nicht gespeichert und keine Rettungskopie möglich: {why}':
        'Проект не сохранён, и резервная копия невозможна: {why}',
    'Projekt wiederherstellen':
        'Восстановить проект',
    'Projekt wird gespeichert …':
        'Сохранение проекта…',
    'Projekt wird gesucht …':
        'Поиск проекта…',
    'Prüfen':
        'Проверить',
    'Prüft Aufnahme …':
        'Проверка записи…',
    'Prüft Aufnahme … {p} %':
        'Проверка записи… {p} %',
    'Speichern und schliessen':
        'Сохранить и закрыть',
    'Trotzdem laden':
        'Всё равно загрузить',
    'Trotzdem schliessen':
        'Всё равно закрыть',
    'Ungespeicherte Änderungen von {when} gefunden.':
        'Найдены несохранённые изменения от {when}.',
    'Ungespeicherte Änderungen.':
        'Несохранённые изменения.',
    'Update wartet: Editor-Projekte werden gesichert …':
        'Обновление ждёт: проекты редактора сохраняются…',
    'Verwerfen und schliessen':
        'Отбросить и закрыть',
    'Wiederherstellen':
        'Восстановить',
    'Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die ganze Aufnahme ist, kann Fog Scout nicht bestätigen.':
        'У этой записи есть проект, который ни разу не был полностью проверен. Начало, конец и размер совпадают; является ли это всей записью, Fog Scout подтвердить не может.',
    'Zuordnung nicht geprüft':
        'Привязка не проверена',
    '{n} Projektdateien passen zu dieser Aufnahme – keine wurde geöffnet.':
        'Этой записи соответствуют файлы проекта ({n}) — ни один не открыт.',
    '● Änderungen':
        '● Изменения',
    '⚠ Mehrere Projektdateien – Auswahl nötig':
        '⚠ Несколько файлов проекта — выберите один',
    '⚠ Nicht gespeichert – {why}':
        '⚠ Не сохранено — {why}',
    '⚠ Nicht im Projekt gespeichert – lokal gesichert':
        '⚠ Не сохранено в проекте — сохранено локально',
    '⚠ Projekt ausserhalb geändert':
        '⚠ Проект изменён извне',
    '⚠ Projektdatei fehlt – Änderungen nur lokal gesichert':
        '⚠ Файл проекта отсутствует — изменения сохранены только локально',
    '⚠ Speichern hängt':
        '⚠ Сохранение зависло',
    '✓ Gespeichert {at}':
        '✓ Сохранено {at}',
    'Der grosse Editor speichert sein Projekt von selbst (1,5 s nach einer Änderung, nie während du ziehst) – mit Sicherungen und einer lokalen Kopie, falls die Projektdatei nicht schreibbar ist. Aus: nur Strg+S schreibt das Projekt; dazwischen hält der Editor einen lokalen Wiederherstellungsstand.':
        'Большой редактор сам сохраняет свой проект (через 1,5 с после изменения, никогда во время перетаскивания) — с резервными копиями и локальной копией на случай, если файл проекта не удастся записать. Выкл.: проект записывает только Ctrl+S; в промежутке редактор хранит локальное состояние для восстановления.',
    'Auf alle Clips':
        'Ко всем клипам',
    'Bild bei {at} der Aufnahme · {length} s ohne Ton':
        'Изображение в {at} записи · {length} с без звука',
    'Den Ausschnitt am Anfang des Clips in der Vorschau ziehen – dazwischen fährt die Kamera gleichmässig.':
        'Тяните рамку в начале клипа в предпросмотре — между началом и концом камера движется равномерно.',
    'Den Ausschnitt am Ende des Clips in der Vorschau ziehen.':
        'Тяните рамку в конце клипа в предпросмотре.',
    'Der Clip zeigt wieder das ganze Bild.':
        'Клип снова показывает всё изображение.',
    'Effekte':
        'Эффекты',
    'Effekte entfernen':
        'Удалить эффекты',
    'Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start.':
        'Фиксированная рамка: начало и конец одинаковы — конечная рамка следует за начальной.',
    'End-Ausschnitt':
        'Конечная рамка',
    'Farbe auf alle {n} Clips übernommen.':
        'Цвет применён ко всем клипам ({n}).',
    'Heller oder dunkler – nur dieser Clip.':
        'Светлее или темнее — только этот клип.',
    'Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen.':
        'Яркость, контраст и насыщенность этого клипа — обратно как записано.',
    'Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton.':
        'Задерживает изображение в позиции воспроизведения на заданное время (клавиша P) — без звука.',
    'Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.':
        'Ярче или бледнее цвета, крайнее левое положение — чёрно-белое; только этот клип.',
    'Mehr oder weniger Kontrast – nur dieser Clip.':
        'Больше или меньше контраста — только этот клип.',
    'Ohne Bewegung':
        'Без движения',
    'Rückwärts':
        'Задом наперёд',
    'Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.':
        'Задом наперёд работает до {n} с на клип — сначала разрежьте этот клип.',
    'Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens {n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).':
        'Воспроизводит клип задом наперёд, вместе со звуком. Для этой записи не более {n} с на клип (иначе ffmpeg нужно слишком много памяти).',
    'Standbild am Abspielkopf einfügen':
        'Вставить кадр в позиции воспроизведения',
    'Standbild einfügen':
        'Вставить кадр',
    'Standbild eingefügt: {n} s ohne Ton.':
        'Кадр вставлен: {n} с без звука.',
    'Standbild hier einfügen':
        'Вставить кадр здесь',
    'Standbild – Clip {n} von {total}':
        'Кадр — клип {n} из {total}',
    'Start-Ausschnitt':
        'Начальная рамка',
    'Wie lange ein Standbild steht – für ein neues, oder für das markierte Standbild.':
        'Как долго держится кадр — для нового или для выбранного кадра.',
    'Zoom':
        'Зум',
    'Zoom entfernen':
        'Удалить зум',
    'Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – Esc beendet.':
        'Зум: тяните рамку в предпросмотре или её углы, чтобы увеличить/уменьшить — Esc завершает.',
    '{n}  Standbild {length} s':
        '{n}  Кадр {length} с',
    'Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig).':
        'Применяет яркость, контраст и насыщенность этого клипа ко всем клипам на шкале времени (один шаг, Ctrl+Z отменяет).',
    'Als Short anzeigen':
        'Показать как Short',
    'Beginnt hier':
        'Начало здесь',
    'Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.':
        'Текст показывается с позиции воспроизведения {n} с внизу Short.',
    'Der markierte Untertitel beginnt am Abspielkopf.':
        'Выбранный субтитр начинается на позиции воспроизведения.',
    'Der markierte Untertitel endet am Abspielkopf.':
        'Выбранный субтитр заканчивается на позиции воспроизведения.',
    'Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen.':
        'Предпросмотр показывает готовое вертикальное видео с заголовком и субтитрами — рисунки и цензура есть в экспорте, здесь не показываются.',
    'Ein Short ist höchstens {limit} min lang, dieser Schnitt {seconds} s – kürzer schneiden.':
        'Short длится не более {limit} мин, этот монтаж — {seconds} с: сократите его.',
    'Endet hier':
        'Конец здесь',
    'Entfernen':
        'Удалить',
    'Entfernt den markierten Untertitel.':
        'Удаляет выбранный субтитр.',
    'Erst den Text des Untertitels eingeben.':
        'Сначала введите текст субтитра.',
    'Hochformat 1080×1920 für YouTube Shorts und TikTok, höchstens 3 min':
        'Вертикальное 1080×1920 для YouTube Shorts и TikTok, не более 3 мин',
    'Schriftgrösse des Titels.':
        'Размер шрифта заголовка.',
    'Short (9:16)':
        'Short (9:16)',
    'Short / TikTok (9:16)':
        'Short / TikTok (9:16)',
    'Short 1080×1920, {fps} fps':
        'Short 1080×1920, {fps} fps',
    'Text eingeben, dann „Untertitel am Abspielkopf“':
        'Введите текст, затем «Субтитр в позиции»',
    'Titel':
        'Заголовок',
    'Titel oben (leer = keiner)':
        'Заголовок сверху (пусто = нет)',
    'Unscharfer Hintergrund':
        'Размытый фон',
    'Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der 9:16-Ausschnitt unter Bild) füllt das Hochformat.':
        'Размытый фон: вся картинка игры посередине, та же картинка размыта сверху и снизу. Обрезка: середина (или обрезка 9:16 в разделе «Изображение») заполняет вертикальный кадр.',
    'Untertitel':
        'Субтитры',
    'Untertitel am Abspielkopf':
        'Субтитр в позиции',
    'Zuschnitt 9:16':
        'Обрезка 9:16',
    'gross':
        'крупный',
    'klein':
        'мелкий',
    'mittel':
        'средний',
    '⚠ länger als {n} min – so nicht exportierbar':
        '⚠ длиннее {n} мин — так экспортировать нельзя',
    '(Datei fehlt – wird nicht exportiert)':
        '(файл отсутствует — не экспортирован)',
    'Beginnt am Abspielkopf':
        'Начинается на позиции воспроизведения',
    'Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt ihn am meisten. Aus: beide gleich laut wie eingestellt.':
        'Звук игры сам становится тише, пока играет музыка — «сильно» приглушает больше всего. Выкл.: оба звучат с заданной громкостью.',
    'Der markierte Ton-Clip beginnt am Abspielkopf.':
        'Выбранный аудиоклип начинается на позиции воспроизведения.',
    'Die Musik wird am Anfang des Clips lauter.':
        'Музыка плавно нарастает в начале клипа.',
    'Die Musik wird zum Ende des Clips leiser.':
        'Музыка плавно затухает к концу клипа.',
    'Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im Export läuft die Musik weiter.':
        'Предпросмотр проигрывает и музыку — кадры в предпросмотре беззвучны, в экспорте музыка продолжает играть.',
    'Eigene Tonspur (A2)':
        'Своя аудиодорожка (A2)',
    'Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die Spur A2 legen – oder die Datei direkt auf A2 ziehen.':
        'Поместить свой аудио- или видеофайл (музыка, комментарий) на дорожку A2 в позиции воспроизведения — или перетащите файл на A2.',
    'Höchstens {n} Ton-Clips.':
        'Не более {n} аудиоклипов.',
    'Kein Ton in {file}.':
        'В {file} нет звука.',
    'Keine Ton- oder Videodatei: {file}':
        'Не аудио- и не видеофайл: {file}',
    'Lautstärke':
        'Громкость',
    'Lautstärke der ganzen Spur A2.':
        'Громкость всей дорожки A2.',
    'Lautstärke des Spieltons im fertigen Clip.':
        'Громкость звука игры в готовом клипе.',
    'Lautstärke nur dieses Ton-Clips.':
        'Громкость только этого аудиоклипа.',
    'Lese {file} …':
        'Чтение {file}…',
    'Musik aus':
        'Затухание музыки',
    'Musik ein':
        'Нарастание музыки',
    'Musik hinzufügen':
        'Добавить музыку',
    'Musik hinzufügen …':
        'Добавить музыку…',
    'Musik oder Kommentar hierher ziehen – oder Rechtsklick „Musik hinzufügen …“':
        'Перетащите сюда музыку или комментарий — или правый щелчок «Добавить музыку…»',
    'Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt.':
        'Убирает выбранный аудиоклип с дорожки A2 — файл остаётся.',
    'Noch keine Musik – Spielton wie aufgenommen.':
        'Музыки пока нет — звук игры как записан.',
    'Spielton':
        'Звук игры',
    'Spielton unter Musik':
        'Игра под музыкой',
    'Ton und Video':
        'Аудио и видео',
    'Ton-Clip entfernen':
        'Удалить аудиоклип',
    'Ton-Clip {file} entfernt – die Datei bleibt.':
        'Аудиоклип {file} удалён — файл остаётся.',
    'leicht':
        'слабо',
    'stark':
        'сильно',
    '{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.':
        '{file} на A2 с {at} — звук игры под ним становится тише.',
    '{file}: {start} – {end} der Datei, im Clip ab {at}':
        '{file}: {start} – {end} файла, в клипе с {at}',
    '{n} Ton-Clip(s) auf A2.':
        'Аудиоклипов на A2: {n}.',
    'Als Montage öffnen …':
        'Открыть как монтаж…',
    'Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.':
        'Другой размер ({w}×{h}) — при экспорте вписывается с чёрными полосами.',
    'Aufnahme fehlt oder ist nicht lesbar: {file}':
        'Запись отсутствует или не читается: {file}',
    'Eine Montage übernimmt keinen Bereich aus der Vorschau.':
        'Монтаж не берёт диапазон из предпросмотра.',
    'Erst wenn das Projekt geladen ist.':
        'Только после загрузки проекта.',
    'Für eine Montage mindestens zwei Videos markieren.':
        'Выберите хотя бы два видео для монтажа.',
    'Höchstens {n} Aufnahmen in einer Montage.':
        'Не более {n} записей в монтаже.',
    'Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das Projekt der Runde bleibt, wie es zuletzt gespeichert war.':
        'Теперь это монтаж — он сохраняется в Clips → Montagen. Проект раунда остаётся таким, каким был сохранён последний раз.',
    'Montage':
        'Монтаж',
    'Montage aus {n} Aufnahmen':
        'Монтаж из записей: {n}',
    'Montage nicht zu öffnen – ihre erste Aufnahme fehlt: {file}':
        'Не удаётся открыть монтаж — нет его первой записи: {file}',
    'Montage {date}':
        'Монтаж {date}',
    'Nicht gefunden: {files} – ihre Clips sind rot, Exportieren geht erst, wenn sie entfernt sind.':
        'Не найдено: {files} — их клипы красные; экспорт заработает, когда они будут удалены.',
    'Nur lesen':
        'Только чтение',
    'Trotzdem verwenden':
        'Всё равно использовать',
    'Video nicht lesbar: {file}':
        'Видео не читается: {file}',
    '{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.':
        '{file} уже не та запись, что была при сохранении.',
    '{file}: {n} Clip(s) angehängt.':
        '{file}: добавлено клипов: {n}.',
    'Audiomediathek':
        'Audio Library',
    'Audiomediathek im Browser geöffnet – heruntergeladene Titel erscheinen im Abschnitt Ton, sobald du zurück im Editor bist.':
        'Audio Library открыта в браузере — скачанные треки появятся в разделе «Звук», когда вы вернётесь в редактор.',
    'Neu im Download-Ordner – Klick legt sie am Abspielkopf auf A2:':
        'Новое в папке загрузок — щелчок помещает на A2 в позиции воспроизведения:',
    'Öffnet YouTubes Audiomediathek im Browser: kostenlose Musik und Effekte, für Videos freigegeben (keine Content-ID-Ansprüche). Heruntergeladene MP3s erscheinen hier darunter.':
        'Открывает фонотеку YouTube (Audio Library) в браузере: бесплатная музыка и эффекты, разрешённые для видео (без претензий Content ID). Скачанные MP3 появятся ниже.',
    'Status, aktuelle Map und deine Runden auf einen Blick':
        'Состояние, текущая карта и ваши раунды с первого взгляда',
    'Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen':
        'Все карты с обозначениями — просмотр, показ вручную, свои изображения и заметки',
    'Was im Spiel erscheint, wo und wie gross':
        'Что показывается в игре, где и какого размера',
    'Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert':
        'Ваши раунды, убийства и время ожидания — хранятся только на этом ПК',
    'Runden, Clips und Screenshots – abspielen, schneiden, aufräumen':
        'Раунды, клипы и скриншоты — смотреть, резать, наводить порядок',
    'Server-Regionen wählen und die Verbindung im Blick behalten':
        'Выбор регионов серверов и наблюдение за соединением',
    'Alles, was Fog Scout tut – suchen mit Strg+F':
        'Всё, что делает Fog Scout — поиск через Ctrl+F',
    'Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche':
        'Что делала программа — для справки и поиска неполадок',
    'Übersicht öffnen':
        'Открыть обзор',
    'Funktionen':
        'Функции',
    'aktiv':
        'активно',
    'wartet auf DBD':
        'ожидание DBD',
    'nimmt auf':
        'запись',
    'verbunden':
        'подключено',
    'verbindet …':
        'подключение…',
    'startet …':
        'запуск…',
    'Fehler – Details im Log':
        'Ошибка — подробности в журнале',
    'nur unter Windows':
        'Только Windows',
    'HWiNFO fehlt':
        'Нет HWiNFO',
    'Mediensteuerung nicht verfügbar':
        'Управление медиа недоступно',
    'Discord nicht erreichbar':
        'Discord недоступен',
    'Anmeldung nötig':
        'Нужен вход',
    'keine Client-ID':
        'нет Client ID',
    'Suche leeren':
        'Очистить поиск',
    'Runden · BP/h erst mit Match-Daten':
        'раунды · для BP/ч нужны данные матчей',
    'Verbindung prüfen …':
        'Проверить подключение…',
    'Öffnet Einstellungen → Verbindungen: OBS-Verbindung (Port, Passwort) und „Verbindung testen“.':
        'Открывает «Настройки → Подключения»: подключение к OBS (порт, пароль) и «Проверить подключение».',
    '{n} Marken':
        'Метки: {n}',
    '1 Marke':
        '1 метка',
    'Keine Aufnahme passt zu den Filtern oben.':
        'Ни одна запись не подходит под фильтры выше.',
    'Kein Clip passt zu den Filtern oben.':
        'Ни один клип не подходит под фильтры выше.',
    'Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.':
        'Строк нет — журнал пуст, или поиск и категории скрывают всё.',
    'OBS nicht verbunden':
        'OBS не подключён',
    'Kills, Entkommen und Bloodpoints zählen hier ohne Custom Games – die Rolle „Custom Games“ zeigt sie.':
        'Убийства, побеги и очки крови здесь учитываются без своих игр — их показывает роль «Свои игры».',
    'Keine Runden in dieser Auswahl – „Filter zurücksetzen“ zeigt wieder alle.':
        'В этой выборке нет раундов — «Сбросить фильтры» снова покажет все.',
    'In dieser Auswahl ist keine Runde einem Match der Stats-Seite zugeordnet – darum fehlen Kills, Entkommen und Bloodpoints.':
        'Ни один раунд этой выборки не связан с матчем на странице статистики — поэтому нет убийств, побегов и очков крови.',
    'Kills, Entkommen und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'Убийства, побеги и очки крови берутся со страницы статистики — для этого один раз настройте данные матчей.',
    'Nicht gezählt: {n} × Rundenende nicht erkannt (die nächste Map kam, bevor das Ende erkannt wurde). Zuletzt: {map}, {when}.':
        'Не засчитано: {n} × конец раунда не распознан (следующая карта появилась раньше, чем был распознан конец). Последний: {map}, {when}.',
    '{n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '{n} × конец раунда не распознан, но засчитан с длительностью со страницы статистики.',
    '{n} × Map mitten im Match falsch erkannt (laut Stats-Seite lief da schon ein Match) – nicht gezählt. Zuletzt: {map}, {when}.':
        '{n} × карта прочитана неверно посреди матча (на странице статистики уже шёл матч) — не засчитано. Последний: {map}, {when}.',
    'Keine Map passt zu „{text}“. Gesucht wird in Map- und Realm-Namen aller Spielsprachen und in Abkürzungen.':
        'Ни одна карта не подходит под «{text}». Поиск учитывает названия карт и миров на всех языках игры и сокращения.',
    'Leert das Suchfeld und zeigt wieder alle Maps.':
        'Очищает поле поиска и снова показывает все карты.',
    'Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter „Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) – die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose.':
        'Каждый флажок — одно место, где Claude помогает по вашему щелчку — никогда сам по себе, никогда во время ввода: поиск (строка «Спросить Claude»: ваш вопрос и названия настроек, страниц и действий), вопросы по статистике (количества и доли), редактор клипов («Правка с Claude»: ваша просьба и монтаж в виде чисел, с его флажком — ещё и кадр) и редактор изображений (вкладка «Claude»: ваша просьба и изображение). Claude только предлагает; ничего не выполняется, пока вы не выберете это или не подтвердите кнопкой «Применить». Никогда не отправляются: раунды, карты, убийцы, пути, имена файлов, серверы или журнал. Нужен свой ключ API из Anthropic Console («Получить ключ API»); API оплачивается с баланса, отдельно от подписки Claude («Пополнить баланс», там же можно задать лимит расходов) — программа оценивает стоимость каждого вопроса по ответу и суммирует её за месяц. Ключ хранится на этом ПК с шифрованием Windows (если оно не работает — до выхода из программы) и никогда не попадает в резервную копию, журнал или диагностику.',
    'Zeigt in der Musikkarte, was in Spotify als Nächstes kommt (Position und Anzahl unter Overlay → Musik). Die Windows-Mediensteuerung kennt nur den laufenden Titel, die Liste holt das Programm deshalb von Spotify selbst: Dafür im Developer-Dashboard „Create app“ anlegen (Name frei, API „Web API“), als Redirect URI genau {uri} eintragen, die Client-ID kopieren und hier einfügen, dann „Mit Spotify verbinden“ – der Browser fragt einmal nach der Freigabe. Gelesen wird nur die Warteschlange, nichts gesteuert; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden) und lässt sich hier trennen. Titel kommen nie ins Log.':
        'Показывает на музыкальной карточке, что дальше играет в Spotify (место и количество — в «Оверлей → Музыка»). Медиаэлементы Windows знают только текущий трек, поэтому программа берёт список у самого Spotify: в панели разработчика «Create app» (любое название, API «Web API»), введите ровно {uri} как redirect URI, скопируйте Client ID и вставьте сюда, затем «Подключить Spotify» — браузер один раз спросит ваше согласие. Читается только очередь, ничем не управляется; согласие хранится на этом ПК с шифрованием Windows (если оно недоступно — только до выхода из программы) и удаляется здесь. Названия никогда не попадают в журнал.',
    'Lädt Clips (F8 und Editor) von selbst auf deinen YouTube-Kanal, Runden nur auf Wunsch: Rechtsklick oder „Auf YouTube hochladen“ unter Aufnahmen. Dafür einmal in der Google Cloud Console ein Projekt anlegen, „YouTube Data API v3“ aktivieren, unter „Anmeldedaten“ einen OAuth-Client vom Typ „Desktop-App“ erstellen und den Zustimmungsbildschirm veröffentlichen (sonst läuft die Anmeldung nach 7 Tagen ab); Client-ID und Client-Secret hier einfügen oder die heruntergeladene JSON-Datei laden, dann „Mit YouTube verbinden“ – der Browser fragt einmal nach der Freigabe. Google erlaubt mit dem Standardkontingent etwa sechs Uploads am Tag; was nicht mehr passt, wartet in der Warteschlange bis zum nächsten Tag. Hochgeladen wird nur, wenn du weder in einer Lobby noch in einer Runde bist; die Datei bleibt immer auch auf der Platte. Gesendet werden nur die Videodatei, Titel (Map, Killer, Datum) und Beschreibung – nie Spielernamen; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden). Mit „Uploads in Playlists einsortieren“ kommt jedes Video zusätzlich in eine Playlist deiner Wahl – dafür fragt die Anmeldung die breitere Berechtigung „YouTube-Konto verwalten“ an (einmal neu verbinden).':
        'Сам загружает клипы (F8 и редактор) на ваш канал YouTube, раунды — только по запросу: правый щелчок или «Загрузить на YouTube» в «Записи». Для этого один раз создайте проект в консоли Google Cloud, включите «YouTube Data API v3», создайте OAuth-клиент типа «Desktop app» в «Credentials» и опубликуйте экран согласия (иначе вход истекает через 7 дней); вставьте сюда Client ID и client secret или загрузите скачанный JSON-файл, затем «Подключить YouTube» — браузер один раз спросит ваше согласие. С квотой по умолчанию Google разрешает около шести загрузок в день; что не поместилось, ждёт в очереди до следующего дня. Загрузки идут, только пока вы не в лобби и не в раунде; файл в любом случае остаётся на диске. Отправляются только видеофайл, заголовок (карта, убийца, дата) и описание — никогда не имена игроков; согласие хранится на этом ПК с шифрованием Windows (если оно недоступно — только до выхода из программы). С «Распределять загрузки по плейлистам» каждое видео также попадает в выбранный вами плейлист — для этого вход запрашивает более широкое разрешение «Управление аккаунтом YouTube» (подключитесь ещё раз).',
    'Liest Client-ID und Client-Secret aus der Datei „client_secret_….json“, die Google nach dem Anlegen des OAuth-Clients zum Herunterladen anbietet („JSON herunterladen“). Die Datei wird nur gelesen und bleibt, wo sie ist; das Secret landet mit der Windows-Verschlüsselung in den Einstellungen (sonst gilt es nur bis zum Beenden).':
        'Читает Client ID и client secret из файла «client_secret_….json», который Google предлагает скачать после создания OAuth-клиента («Download JSON»). Файл только читается и остаётся на месте; secret сохраняется в настройках с шифрованием Windows (иначе только до выхода из программы).',
    'Öffnet die Google-Anmeldung im Browser (nur Recht „Videos hochladen“). Danach kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe mit der Windows-Verschlüsselung auf diesem PC (sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf einem freien Port.':
        'Открывает вход Google в браузере (только право «загрузка видео»). Затем браузер возвращается на 127.0.0.1, и программа хранит согласие на этом ПК с шифрованием Windows (иначе только до выхода из программы). Для этого она один раз слушает свободный порт, только во время входа.',
    'Öffnet die Spotify-Anmeldung im Browser. Nach dem Zustimmen kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe (mit der Windows-Verschlüsselung, nur auf diesem PC – sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf diesem Port.':
        'Открывает вход Spotify в браузере. После вашего согласия браузер возвращается на 127.0.0.1, и программа хранит согласие (с шифрованием Windows, только на этом ПК — иначе только до выхода из программы). Для этого она один раз слушает этот порт, только во время входа.',
    '({how})':
        '({how})',
    'Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird er nicht gespeichert.':
        'Claude: ключ API действует только до выхода из программы — шифрование Windows недоступно, поэтому он не сохраняется.',
    'Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu eintragen oder „Key löschen“.':
        'Claude: сохранённый ключ не удаётся прочитать на этом ПК — введите его снова или нажмите «Удалить ключ».',
    'OBS-Passwort gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'Пароль OBS действует только до выхода из программы — шифрование Windows недоступно, поэтому он не сохраняется.',
    'OBS-Passwort ist nicht verschlüsselt gespeichert – die Windows-Verschlüsselung ist nicht verfügbar.':
        'Пароль OBS хранится незашифрованным — шифрование Windows недоступно.',
    'Spotify: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'Spotify: подключено — только до выхода из программы, шифрование Windows недоступно.',
    'Unverschlüsselt gespeichert (von früher, die Windows-Verschlüsselung ist nicht verfügbar): {names}.':
        'Хранится незашифрованным (с прежних времён, шифрование Windows недоступно): {names}.',
    'YouTube: Client-Secret gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'YouTube: client secret действует только до выхода из программы — шифрование Windows недоступно, поэтому он не сохраняется.',
    'YouTube: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'YouTube: подключено — только до выхода из программы, шифрование Windows недоступно.',
    'nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar':
        'только для этого сеанса — шифрование Windows недоступно',
    'unverschlüsselt gespeichert (alt)':
        'хранится незашифрованным (старое)',
    'verschlüsselt gespeichert':
        'хранится в зашифрованном виде',
    'Befehlspalette':
        'Палитра команд',
    'Suchen':
        'Поиск',
    'Vorschläge':
        'Предложения',
    'OBS-Verbindung':
        'Подключение к OBS',
    'Port und Passwort von OBS stehen unter Verbindungen → OBS-Verbindung.':
        'Порт и пароль OBS — в «Подключения → Подключение к OBS».',
    'Qualität: {word} – {mbps} Mbit/s bei {size}':
        'Качество: {word} — {mbps} Мбит/с при {size}',
    'Qualität: Einstellungen prüfen':
        'Качество: проверьте настройки',
    'Qualität: gemessen wird während einer Aufnahme':
        'Качество: измеряется во время записи',
    '{words} (letzte Aufnahme)':
        '{words} (последняя запись)',
    'gut':
        'хорошее',
    'knapp':
        'на грани',
    'matschig':
        'мыльное',
    'Einstellungen prüfen':
        'проверьте настройки',
    'Qualität verbessern …':
        'Улучшить качество…',
    'OBS-Werte zurücksetzen':
        'Вернуть значения OBS',
    'Aufnahmequalität':
        'Качество записи',
    'In OBS einstellen':
        'Задать в OBS',
    'Empfohlen (in OBS einzustellen):':
        'Рекомендуется (задать в OBS):',
    'Diese Werte lassen sich nur in OBS selbst einstellen – Fog Scout zeigt, wo.':
        'Эти значения можно задать только в самом OBS — Fog Scout показывает где.',
    'Einstellen geht erst nach der Aufnahme.':
        'Настройки можно изменить только после записи.',
    'Fog Scout stellt in OBS ein (die alten Werte werden gemerkt):':
        'Fog Scout задаёт в OBS (старые значения сохраняются):',
    'Die OBS-Werte von vor „In OBS einstellen“ wiederherstellen?':
        'Вернуть значения OBS, которые были до «Задать в OBS»?',
    'Nichts einzustellen.':
        'Нечего задавать.',
    'OBS nimmt gerade auf – Qualität erst nach der Aufnahme einstellen.':
        'OBS записывает — измените качество после записи.',
    'In OBS eingestellt – OBS einmal neu starten, damit alle Werte sicher gelten.':
        'Задано в OBS — перезапустите OBS один раз, чтобы все значения точно применились.',
    'OBS-Einstellungen zurückgesetzt.':
        'Настройки OBS восстановлены.',
    'OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ ist viel schärfer.':
        'OBS записывает с качеством «как у трансляции» или «маленький» — «Неотличимое качество» намного чётче.',
    'OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.':
        'OBS уменьшает изображение ({base} → {out}) — от этого оно мягкое.',
    'OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.':
        'OBS записывает {fps} кадров в секунду — 60 выглядят намного чётче в движении.',
    'Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen.':
        'Кодировщик CPU не успевает (пропущенные кадры) — используйте кодировщик видеокарты.',
    'Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf CQP 18 stellen (siehe Anleitung).':
        'Битрейт слишком низкий для этого изображения — установите управление битрейтом кодировщика на CQP 18 (см. шаги).',
    'Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf.':
        'Битрейта едва хватает — с CQP 18 изображение остаётся чётким и в быстрых сценах.',
    'Ausgabeauflösung = Basisauflösung ({size})':
        'Выходное разрешение = базовое разрешение ({size})',
    'Bildrate 60':
        'Частота кадров 60',
    'Aufnahmequalität „Kaum unterscheidbare Qualität“':
        'Качество записи «Неотличимое качество»',
    'Aufnahme nicht mehr herunterskalieren':
        'Отключить масштабирование записи',
    'OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:':
        'OBS → Настройки → Вывод (режим «Простой») → Запись:',
    'Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“':
        'Качество записи: «Неотличимое качество, большой размер файла»',
    'Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden':
        'Кодировщик: аппаратный (NVENC/AMD/QSV), если доступен',
    'Aufnahmeformat: MKV oder Hybrid-MP4':
        'Формат записи: MKV или гибридный MP4',
    'Video: Ausgabeauflösung = Basisauflösung, Bildrate 60':
        'Видео: выходное разрешение = базовое разрешение, частота кадров 60',
    'OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:':
        'OBS → Настройки → Вывод (режим «Расширенный») → вкладка «Запись»:',
    'Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Видеокодировщик: NVIDIA NVENC H.264 или HEVC (не «Использовать кодировщик потока»)',
    'Ausgabe neu skalieren: aus':
        'Масштабировать вывод: выкл.',
    'x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast':
        'x264: управление битрейтом CRF, значение 18, предустановка veryfast',
    'Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)':
        'Управление битрейтом: CQP, уровень CQ 18 (HEVC 20)',
    'Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei Durchläufe (Viertelauflösung)':
        'Предустановка: P5: Slow (хорошее качество), настройка: высокое качество, многопроходный режим: два прохода (четверть разрешения)',
    'Profil: high (HEVC: main), Keyframe-Intervall: 2 s':
        'Профиль: high (HEVC: main), интервал ключевых кадров: 2 с',
    'Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.':
        'Затем запишите короткий раунд — карточка покажет новый битрейт.',
    'Was die Aufnahme unscharf macht und wie OBS am besten eingestellt wird – was eine Anfrage setzen kann (Ausgabeauflösung, Bildrate, einfache Aufnahmequalität), stellt „In OBS einstellen“ ein, die alten Werte werden gemerkt.':
        'Что делает запись размытой и как лучше настроить OBS — то, что можно задать запросом (выходное разрешение, частота кадров, качество записи в простом режиме), задаёт «Задать в OBS», старые значения сохраняются.',
    'Stellt die OBS-Werte von vor „In OBS einstellen“ wieder her.':
        'Возвращает значения OBS, которые были до «Задать в OBS».',
    'Clips und Editor':
        'Клипы и редактор',
    'Erklärung':
        'Пояснение',
    'Sicherung und Ordner':
        'Резервные копии и папки',
    'Wann aufgenommen wird':
        'Когда записывать',
    'Video-Encoder: AMD HW H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Видеокодировщик: AMD HW H.264 или HEVC (не «Использовать кодировщик потока»)',
    'Frequenzsteuerung: CQP, QP-Werte 18 (HEVC 20)':
        'Управление битрейтом: CQP, значения QP 18 (HEVC 20)',
    'Voreinstellung: Qualität':
        'Предустановка: Quality',
    'Video-Encoder: QuickSync H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        'Видеокодировщик: QuickSync H.264 или HEVC (не «Использовать кодировщик потока»)',
    'Frequenzsteuerung: ICQ (oder CQP), Wert 18':
        'Управление битрейтом: ICQ (или CQP), значение 18',
    'Target Usage: TU1 bis TU4 – kleiner = bessere Qualität':
        'Target usage: от TU1 до TU4 — меньше = лучше качество',
    'Video-Encoder: der Grafikkarten-Encoder (NVENC, AMF oder QuickSync), wenn OBS einen anbietet – sonst x264':
        'Видеокодировщик: кодировщик видеокарты (NVENC, AMF или QuickSync), если OBS его предлагает — иначе x264',
    'Video-Encoder: einen eigenen wählen (nicht „Stream-Encoder verwenden“), am besten den der Grafikkarte, wenn OBS einen anbietet':
        'Видеокодировщик: выберите отдельный (не «Использовать кодировщик потока»), лучше всего видеокарты, если OBS его предлагает',
    'Frequenzsteuerung: gleichbleibende Qualität (CQP, CQ, ICQ oder CRF) um 18 statt einer festen niedrigen Bitrate':
        'Управление битрейтом: постоянное качество (CQP, CQ, ICQ или CRF) около 18 вместо низкого фиксированного битрейта',
    'Einschätzung aus Bitrate, Auflösung, Bildrate und Codec – Bildinhalt, Bewegung, Encoder-Voreinstellung und Quelle beeinflussen das Ergebnis.':
        'Оценка по битрейту, разрешению, частоте кадров и кодеку — содержимое изображения, движение, предустановка кодировщика и источник влияют на результат.',
    'Start und Meldungen':
        'Запуск и уведомления',
    'Fog Scout kann mit Windows starten und still im Infobereich (neben der Uhr) warten, bis DBD läuft. Die Lobby-Meldung sagt dir mit einem Ton, wenn ein Match gefunden wurde.':
        'Fog Scout может запускаться вместе с Windows и тихо ждать в области уведомлений (рядом с часами), пока не запустится DBD. Уведомление о лобби звуком сообщает, что матч найден.',
    'Optional: OBS Studio nimmt jede Runde auf, Fog Scout sagt OBS nur, wann. Ohne OBS einfach „Weiter“.':
        'Необязательно: OBS Studio записывает каждый раунд, Fog Scout лишь говорит OBS когда. Без OBS просто «Далее».',
    '1. In OBS: Werkzeuge → WebSocket-Servereinstellungen → „WebSocket-Server aktivieren“ anhaken; unter „Verbindungsinformationen anzeigen“ stehen Port und Passwort.':
        '1. В OBS: Сервис → Настройки сервера WebSocket → отметьте «Включить сервер WebSocket»; «Показать сведения о подключении» показывает порт и пароль.',
    '2. Port und Passwort hier eintragen und „Verbindung testen“.':
        '2. Введите здесь порт и пароль и нажмите «Проверить подключение».',
    '3. Einen Ordner für die Aufnahmen wählen und die Aufnahmen einschalten.':
        '3. Выберите папку для записей и включите запись.',
    'Wie scharf OBS aufnimmt, zeigt danach die Karte „Aufnahme“ auf der Seite Aufnahmen – dort auch „Qualität verbessern …“.':
        'Насколько чётко записывает OBS, потом покажет карточка «Запись» на странице «Записи» — там же «Улучшить качество…».',
    'Alles hier ist freiwillig und lässt sich später unter Einstellungen → Verbindungen einrichten. Jede Verbindung braucht eine eigene App-ID bzw. einen eigenen Key von dir – „Erklärung“ sagt, wo es sie gibt.':
        'Всё здесь необязательно и настраивается позже в «Настройки → Подключения». Каждому подключению нужен свой ID приложения или ключ — «Пояснение» подскажет, где его взять.',
    'Fog Scout kann anzeigen, mit welchem Spielserver DBD verbunden ist (Region und Ping, auch im Overlay) – dafür fragt Windows einmal nach Administratorrechten.':
        'Fog Scout может показывать, к какому игровому серверу подключена DBD (регион и пинг, в том числе в оверлее) — для этого Windows один раз запросит права администратора.',
    'Auf der Seite Server lässt sich ausserdem festlegen, in welchen Regionen DBD Matches sucht. Das ist freiwillig.':
        'На странице «Сервер» можно также выбрать, в каких регионах DBD ищет матчи. Это необязательно.',
    'Serverregionen auswählen …':
        'Выбрать регионы серверов…',
    'Beendet die Einrichtung und öffnet die Seite Server – dort die Regionen anhaken, in denen DBD Matches suchen soll.':
        'Завершает настройку и открывает страницу «Сервер» — отметьте там регионы, в которых DBD должна искать матчи.',
    'Öffnet den Ordner mit Einstellungen, Runden, Log und Sicherungen im Explorer.':
        'Открывает в проводнике папку с настройками, раундами, журналом и резервными копиями.',
    'Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an Claude schicken“ einschalten und einen API-Key eintragen.':
        'Выкл. — включите «Отправлять изображения из редактора изображений в Claude» в «Настройки → Подключения → Claude» и введите ключ API.',
    'Ausschnitt ausserhalb des Bildes':
        'обрезка за пределами изображения',
    'Bereich unkenntlich machen ({x} %, {y} %)':
        'Скрыть область ({x} %, {y} %)',
    'Bilder im Bild-Editor an Claude schicken':
        'Отправлять изображения из редактора изображений в Claude',
    'Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        'На изображениях могут быть имена игроков — в Claude они попадают только когда вы нажимаете «Предложить», в уменьшенном виде и только в памяти; уже зацензуренные области остаются зацензуренными. Вопросы по статистике отправляют только количества и доли по роли, убийце, карте, региону и времени суток — ни одного отдельного раунда, никаких имён игроков.',
    'Claude hat keine Antwort gegeben.':
        'Claude не ответил.',
    'Claude zur Statistik fragen: „{q}“':
        'Спросить Claude о статистике: «{q}»',
    'Claude: Key eingetragen, Claude ist überall aus.':
        'Claude: ключ введён, Claude везде выключен.',
    'Das Bild hat sich inzwischen geändert – bitte neu vorschlagen.':
        'Изображение тем временем изменилось — запросите предложение заново.',
    'Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude (api.anthropic.com), verkleinert und nur im Speicher.':
        'На изображении могут быть имена игроков — оно попадает в Claude (api.anthropic.com) только по щелчку, в уменьшенном виде и только в памяти.',
    'Das Bild lässt sich nicht für Claude verkleinern.':
        'Не удаётся уменьшить изображение для Claude.',
    'Das Standbild liess sich nicht lesen – nichts gesendet.':
        'Не удалось прочитать кадр — ничего не отправлено.',
    'Die Statistik liess sich nicht zusammenfassen – Details im Log.':
        'Не удалось обобщить статистику — подробности в журнале.',
    'Drehung ohne Winkel':
        'поворот без угла',
    'Farbe ohne Werte':
        'цвет без значений',
    'Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %':
        'Цвет: яркость {b} %, контраст {c} %, насыщенность {s} %',
    'In der Suche Statistik-Fragen an Claude stellen':
        'Задавать Claude вопросы по статистике в поиске',
    'Kasten ausserhalb des Bildes':
        'область за пределами изображения',
    'Kippen':
        'Отразить по вертикали',
    'Noch keine Runden – Claude hätte nichts zum Auswerten.':
        'Раундов пока нет — Claude не на что смотреть.',
    'Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du übernimmst.':
        'Отправляет Claude ваше пожелание и изображение в показанном здесь виде (уже зацензуренные области остаются зацензуренными); ничего не меняется, пока вы не примените.',
    'Schickt die Frage und Zähler/Quoten deiner Runden an Claude – keine einzelne Runde, keine Namen':
        'Отправляет Claude вопрос и количества/доли ваших раундов — ни одного отдельного раунда, никаких имён',
    'Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        'Отправляет также изображение в позиции воспроизведения (в уменьшенном виде, уже зацензуренные области остаются зацензуренными) — так Claude может, например, зацензурить имена. На изображении могут быть имена игроков.',
    'Spiegeln':
        'Отразить',
    'Spiegeln ohne Richtung':
        'отражение без направления',
    'Standbild mitsenden':
        'Отправить кадр',
    'Standbilder aus Aufnahmen im Clip-Editor an Claude schicken':
        'Отправлять кадры из записей в редакторе клипов в Claude',
    'Um {deg}° drehen':
        'Повернуть на {deg}°',
    'Vergisst den Vorschlag; das Bild bleibt, wie es ist.':
        'Забывает предложение; изображение остаётся как есть.',
    'Zensur nur mit Standbild':
        'цензура только с кадром',
    'Zensur: {style}':
        'Цензура: {style}',
    'Zuschneiden auf {w} × {h} %':
        'Обрезать до {w} × {h} %',
    'unbekannte Art der Zensur':
        'неизвестный вид цензуры',
    'unbekannter Schritt':
        'неизвестный шаг',
    'z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller':
        'например, пикселизировать имена игроков, обрезать до 16:9, чуть ярче',
    'zu viele Kästen':
        'слишком много областей',
    'Zeigt im Bild-Editor den Reiter „Claude“: Du schreibst, was mit dem Bild passieren soll (Namen verpixeln, zuschneiden, heller), und auf „Vorschlagen“ gehen Bitte und Bild verkleinert an Claude. Das Bild kann Spielernamen zeigen; bereits zensierte Bereiche bleiben zensiert.':
        'Показывает вкладку «Claude» в редакторе изображений: вы пишете, что сделать с изображением (пикселизировать имена, обрезать, ярче), и по «Предложить» ваше пожелание и уменьшенное изображение отправляются Claude. На изображении могут быть имена игроков; уже зацензуренные области остаются зацензуренными.',
    'Erlaubt im grossen Clip-Editor das Häkchen „Standbild mitsenden“: dann geht das Bild an der Abspielposition mit, und Claude kann z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        'Разрешает флажок «Отправить кадр» в большом редакторе клипов: тогда отправляется и изображение в позиции воспроизведения, и Claude может, например, зацензурить имена. На изображении могут быть имена игроков.',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude zur Statistik fragen“. Gesendet werden deine Frage und Zähler/Quoten deiner Runden je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        'Показывает строку «Спросить Claude о статистике» в поиске (Ctrl+F). Отправляются ваш вопрос и количества/доли ваших раундов по роли, убийце, карте, региону и времени суток — ни одного отдельного раунда, никаких имён игроков.',
    'Start: Fenster bereit nach {total} s seit Programmstart (davon {before} s bis Python).':
        'Запуск: окно готово через {total} с после старта программы (из них {before} с до Python).',
    'Haiku 5.5 – am günstigsten':
        'Haiku 5.5 — самая дешёвая',
    'Opus 5.5 – am genauesten':
        'Opus 5.5 — самая точная',
    'Sonnet 5.5 – halber Preis':
        'Sonnet 5.5 — вдвое дешевле',
    'Modell':
        'Модель',
    'Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat {month}. Abgerechnet wird in der Anthropic Console.':
        'Стоимость (оценка по прейскуранту): в этом сеансе {session} за запросы ({n}), в этом месяце {month}. Счета — в Anthropic Console.',
    'Claude: Welcher Build läuft am besten?':
        'Claude: какая сборка работает лучше всего?',
    'Claude: Woche zusammenfassen':
        'Claude: итоги недели',
    'Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?':
        'Подведи итоги моей недели по сравнению с прошлой: что стало лучше, что хуже?',
    'Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?':
        'Какие из моих навыков работают лучше всего — отдельно за убийцу и за выжившего?',
    'Fog Scout ist abgestürzt':
        'Fog Scout аварийно завершился',
    'Fog Scout wurde am {when} unerwartet beendet. „Diagnose kopieren“ legt einen Bericht mit den Stellen des Absturzes in die Zwischenablage – zum Melden auf GitHub oder im Chat. Der Bericht enthält keine Schlüssel, Titel oder Server-Adressen.':
        'Fog Scout неожиданно завершился {when}. «Копировать диагностику» помещает в буфер обмена отчёт с местами сбоя — чтобы сообщить о нём на GitHub или в чате. Отчёт не содержит ключей, названий или адресов серверов.',
    'Claude hat keine Stelle gefunden, die heraussticht.':
        'Claude не нашёл выделяющегося момента.',
    'Claude sieht sich {n} Standbilder an …':
        'Claude смотрит кадры ({n})…',
    'Highlights finden':
        'Найти лучшие моменты',
    'Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu drei Stellen für einen Short. Die Bilder können Spielernamen zeigen.':
        'Отправляет Claude маленькие кадры монтажа (равномерно и в метках F8, уже зацензуренные области остаются зацензуренными); Claude называет до трёх моментов для Short. На изображениях могут быть имена игроков.',
    'Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ ändert den Schnitt.':
        'Предлагает оставить только эту часть — монтаж меняет только «Применить».',
    'Namen beim Zuschauen':
        'Имена при наблюдении',
    'Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und den Namen oben in der Mitte – bei Bedarf verschieben.':
        'Ставит области на имена так, как DBD показывает их при наблюдении: список слева, выше, и имя вверху по центру — при необходимости сдвиньте их.',
    'Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        'Ставит область туда, где DBD показывает имена выживших в матче (внизу слева на картинке игры) — при необходимости сдвиньте её.',
    'Aufnahme zeigen':
        'Показать запись',
    'Aufnahme abspielen':
        'Воспроизвести запись',
    'Zu dieser Runde gibt es keine Aufnahme.':
        'У этого раунда нет записи.',
    'Die Aufnahme dieser Runde ist durch die Filter der Seite Aufnahmen ausgeblendet.':
        'Запись этого раунда скрыта фильтрами страницы «Записи».',
    'Sitzungen':
        'Сессии',
    'Killer/Survivor':
        'Убийца/Выживший',
    '{n} K':
        '{n} У',
    '{n} S':
        '{n} В',
    'Ø Dauer einer Sitzung':
        'Ср. длительность сессии',
    'Ø Runden je Sitzung':
        'Ср. раундов за сессию',
    'Ø Warten':
        'Ср. ожидание',
    'Eine Sitzung endet nach {n} Minuten ohne Runde. Es gelten die Filter oben – mit einem Rollenfilter zählt eine Sitzung nur die Runden dieser Rolle. Ø Kills, Entkommen und BP laut Stats-Seite. Doppelklick zeigt die Runden der Sitzung unter „Letzte Runden“.':
        'Сессия заканчивается после {n} мин без раунда. Действуют фильтры выше — с фильтром роли сессия учитывает только раунды этой роли. Ср. убийства, побеги и BP — со страницы статистики. Двойной щелчок показывает раунды сессии в «Последних раундах».',
    'Blutpunkte-Stand – letzter Wert {per}':
        'Баланс очков крови — последнее значение {per}',
    'Cap erreicht':
        'Лимит достигнут',
    'Cap in ≈ {n} Runden':
        'Лимит примерно через {n} раундов',
    'Cap: {cap}':
        'Лимит: {cap}',
    'Noch kein Blutpunkte-Stand gelesen – er kommt aus der Lobby nach der Runde.':
        'Баланс очков крови ещё не прочитан — он берётся из лобби после раунда.',
    '{when}: Stand {bp} BP':
        '{when}: баланс {bp} BP',
    '+{n} Level':
        '+{n} ур.',
    '+{n} P':
        '+{n} P',
    'Eine Zeile oben anklicken, um den Verlauf zu sehen.':
        'Щёлкните строку выше, чтобы увидеть тренд.',
    'Keine Matches mit Prestige in dieser Auswahl.':
        'В этой выборке нет матчей с престижем.',
    'Level':
        'Уровень',
    'Matches':
        'Матчи',
    'Noch kein Prestige in dieser Auswahl – es kommt aus den Match-Daten (Userscript ab Version 3).':
        'В этой выборке пока нет престижа — он берётся из данных матчей (юзерскрипт версии 3 или новее).',
    'Prestige':
        'Престиж',
    'Prestige und Level deiner Charaktere laut Stats-Seite (ab Userscript Version 3). „Prestige“ und „Level“ = der neueste Stand; „Zuwachs“ und „Matches“ gelten für die Filter oben. Eine Zeile anklicken zeigt darunter den Verlauf dieses Charakters. „Tempo“ = gewonnene Level pro Woche aus den Matches der letzten {days} Tage, „Nächstes P“ = wie lange es bei diesem Tempo bis zur nächsten Stufe dauert. Level steigen nur, wenn du Blutpunkte im Blutnetz ausgibst – die Prognose sagt, was bisher geschah, keine Zusage. „Main“ = dein Charakter mit den meisten Matches je Rolle. „P100“ und „Höchster“ zählen nur Charaktere, die in deinen Match-Daten vorkommen.':
        'Престиж и уровень ваших персонажей со страницы статистики (юзерскрипт версии 3 или новее). «Престиж» и «Уровень» = последнее состояние; «Прирост» и «Матчи» следуют фильтрам выше. Щёлкните строку, чтобы увидеть тренд этого персонажа ниже. «Темп» = уровней в неделю по матчам за последние {days} дн., «След. P» = сколько займёт следующий престиж при таком темпе. Уровни растут, только когда вы тратите очки крови в паутине крови — прогноз описывает прошлое, а не обещает. «Основной» = ваш персонаж с наибольшим числом матчей в каждой роли. «P100» и «Максимум» учитывают только персонажей из ваших данных матчей.',
    'Prestige von {name} {per}':
        'Престиж {name} {per}',
    'Zuletzt':
        'Последняя игра',
    'Zuwachs':
        'Прирост',
    '{when}: Prestige {p} · Level {level}':
        '{when}: престиж {p} · уровень {level}',
    '+{n} weitere':
        '+ ещё {n}',
    'Charaktere':
        'Персонажи',
    'Höchster':
        'Максимум',
    'Level diese Woche':
        'Уровней за неделю',
    'Main':
        'Основной',
    'Meilenstein: {name} ist jetzt Prestige {p}':
        'Достижение: у {name} теперь престиж {p}',
    'Nächstes P':
        'След. P',
    'P100 erreicht':
        'P100 достигнут',
    'Prestige gesamt':
        'Престиж всего',
    'alle Charaktere':
        'все персонажи',
    'seit Montag':
        'с понедельника',
    '{k} Killer · {s} Survivor':
        'убийца {k} · выживший {s}',
    '{name} ist jetzt Prestige {p}':
        'У {name} теперь престиж {p}',
    '{name} · Level {level}':
        '{name} · уровень {level}',
    '{n} Level/Woche':
        '{n} ур./нед.',
    '≈ 1 Tag':
        '≈ 1 день',
    '≈ 1 Woche':
        '≈ 1 неделя',
    '≈ {n} Tage':
        '≈ {n} дн.',
    '≈ {n} Wochen':
        '≈ {n} нед.',
    '{n} Charaktere':
        'Персонажи: {n}',
    'P100':
        'P100',
    '{n}× Killer':
        '{n}× убийца',
    '{n}× Survivor':
        '{n}× выживший',
    '{n}× Farming':
        '{n}× фарм',
    '{n}× Custom Game':
        '{n}× своя игра',
    '{n}× ohne Rolle':
        '{n}× без роли',
    'Zeigt, was diese Kachel zählt':
        'Показывает, что считает эта плитка',
    'Diese Runden sind durch die Filter der Statistik ausgeblendet.':
        'Эти раунды скрыты фильтрами статистики.',
    'Automatisch (zuletzt benutztes Gerät)':
        'Автоматически (последнее использованное устройство)',
    'Dunkle Fläche hinter den Eingaben':
        'Тёмный фон за вводом',
    'EINGABEN':
        'ВВОД',
    'Eingaben im Spiel':
        'Ввод в игре',
    'Eingaben im Spiel zeigen (Tasten, Maus, Gamepad)':
        'Показывать ввод в игре (клавиши, мышь, геймпад)',
    'Gamepad':
        'Геймпад',
    'Gerät':
        'Устройство',
    'Tastatur und Maus':
        'Клавиатура и мышь',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter den Tasten.':
        'Полупрозрачный тёмный фон со скруглёнными углами за клавишами.',
    'wartet auf eine Runde':
        'ожидание раунда',
    'Eingaben mit der Aufnahme speichern (für den Clip-Editor)':
        'Сохранять ввод вместе с записью (для редактора клипов)',
    'Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). Eine offizielle Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.':
        'Fog Scout только показывает, какие из этих клавиш сейчас зажаты: W, A, S, D, Q, E, R, пробел, Shift, Ctrl, кнопки мыши и геймпад (кнопки, триггеры, стики). Они считываются только во время раунда и только пока DBD — активное окно; Fog Scout никогда не видит ввод текста в других программах. Ничего из этого не записывается в журнал и не отправляется, и ничего не передаётся в игру; с «Сохранять ввод вместе с записью» клавиши раунда сохраняются в файл рядом с его записью OBS (для редактора клипов). Официального одобрения таких показов от Behaviour нет; преимущества в игре они не дают.',
    'Gelesen werden nur W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad – nur während einer Runde und nur, solange DBD vorne ist. Gesendet wird nichts; gespeichert nur mit dem Häkchen oben, als Datei neben der eigenen Aufnahme.':
        'Считываются только W, A, S, D, Q, E, R, пробел, Shift, Ctrl, кнопки мыши и геймпад — только во время раунда и только пока DBD на переднем плане. Ничего не отправляется; сохраняется только с флажком выше, как файл рядом с вашей записью.',
    'Eine Karte im Spiel zeigt, welche Tasten, Maustasten oder Gamepad-Knöpfe du gerade drückst – wie bei Streamern. Gelesen wird nur eine feste Liste von Tasten, nur während einer Runde und nur, solange DBD vorne ist; gesendet wird nichts, gespeichert nur mit „Eingaben mit der Aufnahme speichern“.':
        'Карточка в игре показывает, какие клавиши, кнопки мыши или геймпада вы сейчас нажимаете — как у стримеров. Считывается только фиксированный список клавиш, только во время раунда и только пока DBD на переднем плане; ничего не отправляется, сохраняется только с «Сохранять ввод вместе с записью».',
    'Mit OBS-Aufnahmen: die gedrückten Tasten der Runde kommen als kleine Datei neben die Aufnahme – der Clip-Editor zeigt sie als Spur und kann die Karte ins Video einbrennen. Die Datei wird mit der Aufnahme verschoben und gelöscht.':
        'С записями OBS: зажатые во время раунда клавиши попадают в маленький файл рядом с записью — редактор клипов показывает их как дорожку и может впечатать карточку в видео. Файл перемещается и удаляется вместе с записью.',
    'Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme speichern“). Clips aus F8 haben keine.':
        'Из файла рядом с записью («Оверлей › Ввод › Сохранять ввод вместе с записью»). У клипов F8 его нет.',
    'Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet).':
        'Карточка с зажатыми клавишами раунда попадает в готовое видео — в выбранном углу, синхронно с монтажом (с учётом темпа и обратного воспроизведения).',
    'Dunkle Fläche hinter den Tasten':
        'Тёмный фон за клавишами',
    'Ecke':
        'Угол',
    'Eine halb durchsichtige dunkle Fläche hinter der Karte.':
        'Полупрозрачный тёмный фон за карточкой.',
    'Eingaben im Export zeigen':
        'Показывать ввод в экспорте',
    'Höhe der Karte im Verhältnis zur Bildhöhe.':
        'Высота карточки относительно высоты изображения.',
    'Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade benutzt wurde.':
        'Какой вид показывает карточка — автоматически устройство, которое только что использовалось.',
    'Wo die Karte im Bild liegt.':
        'Где карточка находится на изображении.',
    'Claude baut einen Short aus {n} Standbildern …':
        'Claude собирает Short из кадров ({n})…',
    'Clip um Moment':
        'Клип вокруг момента',
    'Der Schnitt hat sich inzwischen geändert – bitte noch einmal.':
        'Монтаж тем временем изменился — попробуйте снова.',
    'Der Schnitt wird der markierte Moment ({before} s davor bis {after} s danach).':
        'Монтаж становится выбранным моментом (от {before} с до до {after} с после).',
    'Die Bilder liessen sich nicht lesen.':
        'Не удалось прочитать изображения.',
    'F8-Marke':
        'Метка F8',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden.':
        'Сейчас невозможно — сначала завершите текущую правку.',
    'Kein Ladebildschirm am Anfang oder Ende gefunden.':
        'В начале и в конце экран загрузки не найден.',
    'Kein Leerlauf gefunden.':
        'Участков простоя не найдено.',
    'Ladebildschirm abschneiden':
        'Вырезать экран загрузки',
    'Leerlauf kürzen':
        'Убрать простой',
    'Momente':
        'Моменты',
    'Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst „Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen.':
        'Отправляет Claude кадры в найденных моментах (по клавишам, звуку игры и меткам F8, только в виде чисел) и монтаж; Claude предлагает целый Short — диапазон, замедление, заголовок, субтитры. Монтаж меняет только «Применить». На изображениях могут быть имена игроков.',
    'Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war (aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.':
        'Вырезает участки, где ничего не было зажато хотя бы {n} с (по вводу записи) — один шаг отмены.',
    'Sehe mir Anfang und Ende an …':
        'Просмотр начала и конца…',
    'Short vorschlagen':
        'Предложить Short',
    'Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.':
        'Просматривает первые и последние {n} с и вырезает чёрное начало или конец — один шаг отмены.',
    'laut':
        'громко',
    'viele Tasten':
        'много клавиш',
    '{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z macht es rückgängig.':
        'Убрано участков простоя: {n} ({seconds} с) — Ctrl+Z отменяет.',
    '{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – Strg+Z macht es rückgängig.':
        'Вырезано чёрных участков: {n} ({seconds} с) — Ctrl+Z отменяет.',
    'Anordnen':
        'Расставить',
    'Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · Tab = nächstes Element · Esc = fertig':
        'Расстановка — и в игре: тяните элементы · стрелки = точно (Shift = 10 px) · Tab = следующий элемент · Esc = готово',
    'Anordnen: alle Elemente mit der Maus ziehen – in der Vorschau und direkt im Spiel. Strg+Mausrad ändert die Grösse, Esc beendet.':
        'Расстановка: тяните любой элемент мышью — в предпросмотре и прямо в игре. Ctrl+колесо меняет размер, Esc завершает.',
    'Automatisch: im schwarzen Rand neben dem Spielbild bzw. neben dem DBD-Fenster. Frei platzieren: „Anordnen“ oder eine Schnellposition.':
        'Автоматически: в чёрной полосе рядом с картинкой игры или рядом с окном DBD. Чтобы разместить свободно: «Расставить» или быстрое место.',
    'CPU, GPU, RAM':
        'CPU, GPU, RAM',
    'Callout-Karte der Map':
        'Карта с обозначениями',
    'Die Linien in der Vorschau mit „Anordnen“ ziehen – Karte, Systemwerte, Heute und Musik bleiben im Balken dazwischen.':
        'Тяните линии в предпросмотре с «Расставить» — карта, системные данные, «Сегодня» и музыка остаются между ними в полосе.',
    'Ein- oder ausblenden':
        'Показать или скрыть',
    'Elemente':
        'Элементы',
    'Entsperren: wieder verschiebbar':
        'Открепить: снова можно перемещать',
    'Fokus':
        'Фокус',
    'Frei platzieren: „Anordnen“, eine Schnellposition oder Vorgabe „eigene Position“.':
        'Чтобы разместить свободно: «Расставить», быстрое место или настройка «своя позиция».',
    'Gesperrt – erst entsperren':
        'Закреплён — сначала открепите',
    'Gilt für alle Elemente':
        'Действует для всех элементов',
    'Grenzen und Platz':
        'Границы и место',
    'Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen':
        'Линия границы: тяните её туда, докуда могут доходить элементы в полосе',
    'Grösse und Deckkraft':
        'Размер и непрозрачность',
    'Grösse von {name}: Ecke ziehen':
        'Размер {name}: тяните за угол',
    'Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, Rechtsklick = Menü. Ende mit „Fertig“ oder Esc.':
        'Щелчок по элементу выбирает его. С «Расставить»: тянуть элемент = переместить (пунктирная рамка показывает, куда он встанет), тянуть угол или Ctrl+колесо = размер, правый щелчок = меню. Завершить — «Готово» или Esc.',
    'Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel':
        'Щелчок выбирает элемент · «Расставить» включает перемещение — здесь и в игре',
    'Klick wählt {name}':
        'Щелчок выбирает {name}',
    'Layout für {size}':
        'Раскладка для {size}',
    'Läuft gerade':
        'Сейчас играет',
    'Mitte':
        'по центру',
    'Nach {where} legen (mit Rand)':
        'Поставить: {where} (с отступом)',
    'Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein).':
        'Место и размер хранятся для каждого размера окна DBD (вкладка «Общие»).',
    'Runden und Zeit heute':
        'Раунды и время сегодня',
    'Schnellposition':
        'Быстрое место',
    'Sperren':
        'Закрепить',
    'Sperren: im Modus „Anordnen“ nicht mehr verschiebbar':
        'Закрепить: больше не перемещается в «Расставить»',
    'Stil, Abstand, Grenzen, Discord':
        'Стиль, отступ, границы, Discord',
    'Tasten und Gamepad':
        'Клавиши и геймпад',
    'Timer, Bilanz, Server':
        'Таймер, итоги, сервер',
    'Verhalten':
        'Поведение',
    'Zeilen':
        'Строки',
    'Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)':
        'Вернуть на автоматическое место (в чёрной полосе, рядом с остальными)',
    'eigener Platz':
        'своё место',
    'eingerastet':
        'привязано',
    'graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        'серые линии в полосах = границы (выкл.) — перетаскивание одной включает их',
    'links Mitte':
        'слева по центру',
    'oben Mitte':
        'вверху по центру',
    'rastet an Mitte, Balken und anderen ein (Alt = frei)':
        'привязывается к центру, полосам и другим элементам (Alt = свободно)',
    'rechts Mitte':
        'справа по центру',
    'unten Mitte':
        'внизу по центру',
    '{name} entsperrt.':
        '{name}: откреплено.',
    '{name} gesperrt – bleibt beim Anordnen, wo es ist.':
        '{name}: закреплено — остаётся на месте при расстановке.',
    '{name} ist gesperrt – das Schloss in der Liste löst es':
        '{name}: закреплено — замок в списке открепляет',
    '{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü':
        '{name}: тянуть = переместить · угол или Ctrl+колесо = размер · правый щелчок = меню',
    'Üblicher Platz':
        'Обычное место',
    '„Overlay testen“ zeigt die Karte sofort, mit „Anordnen“ ziehst du sie hin.':
        '«Тест оверлея» сразу показывает карту, с «Расставить» вы перетаскиваете её туда.',
    'Nur die Vorschau: Liste und Einstellungen weg, die Navigation schmal – die ganze Fläche zum Anordnen. Esc oder nochmal klicken beendet es.':
        'Только предпросмотр: список и настройки убраны, навигация узкая — вся площадь для расстановки. Esc или ещё один щелчок завершает.',
    'Englisch':
        'Английский',
    'Deutsch':
        'Немецкий',
    'Französisch':
        'Французский',
    'Spanisch':
        'Испанский',
    'Spanisch (Mexiko)':
        'Испанский (Мексика)',
    'Italienisch':
        'Итальянский',
    'Polnisch':
        'Польский',
    'Portugiesisch (Brasilien)':
        'Португальский (Бразилия)',
    'Türkisch':
        'Турецкий',
    'Spielsprache selbst erkennen und anhaken':
        'Определять язык игры и отмечать его автоматически',
    'Spielsprache {lang} erkannt (Banner „{text}“) – automatisch angehakt.':
        'Язык игры «{lang}» определён (баннер «{text}») — отмечен автоматически.',
    'Läuft DBD in einer Sprache, die hier nicht angehakt ist, und passt ein Map-Banner eindeutig zu einer Map in dieser Sprache, hakt Fog Scout sie selbst an – die Karte erscheint dann schon in derselben Runde. Nur am Rundenstart, nie mitten im Match.':
        'Если DBD запущена на языке, который здесь не отмечен, и баннер карты однозначно совпадает с картой на этом языке, Fog Scout отметит его сам — карта появится уже в том же раунде. Только в начале раунда, никогда посреди матча.',
    'Russisch':
        'Русский',
    'Chinesisch (vereinfacht)':
        'Китайский (упрощённый)',
    'Chinesisch (traditionell)':
        'Китайский (традиционный)',
    'Japanisch':
        'Японский',
    'Koreanisch':
        'Корейский',
}
