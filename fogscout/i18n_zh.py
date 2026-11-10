"""Simplified Chinese texts (1.47): the German text of the code is the key, as in i18n_en.EN – a text missing here
shows in English (i18n.table). Made from the English texts; tests/test_i18n.py checks keys and placeholders."""
T = {
    'Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\nKurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden.':
        'Fog Scout 已在运行，但没有响应（或正在关闭）。\n\n请稍等片刻后重新启动。如果仍然无效：在任务管理器的“详细信息”中结束“{exe}”（Fog Scout）。',
    'Fog Scout konnte nicht neu gestartet werden: Die alte Kopie läuft noch im Hintergrund.\n\nIm Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden und das Programm neu starten.':
        'Fog Scout 无法重新启动：旧的副本仍在后台运行。\n\n请在任务管理器的“详细信息”中结束“{exe}”（Fog Scout），然后重新启动程序。',
    'Start fehlgeschlagen:':
        '启动失败：',
    'Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt unverändert.':
        '到目前为止，Fog Scout 是通过 start.bat 使用的：\n{folder}\n\n要将设置、对局、比赛数据、备份和自己的地图图片转移到已安装的版本吗？旧文件夹保持不变。',
    'Übernahme fehlgeschlagen: {error}':
        '转移失败：{error}',
    'Kein Windows: Fenstersuche, Hotkeys und Click-Through sind nur unter Windows aktiv.':
        '不是 Windows：窗口查找、快捷键和点击穿透仅在 Windows 上可用。',
    'Bereit. {n} Maps geladen, Spielsprachen: {langs}.':
        '就绪。已加载 {n} 张地图，游戏语言：{langs}。',
    'Bildschirm {w}×{h} ohne schwarze Balken neben dem Spielbild: Systemwerte, „Heute“ und Musik im Spiel sind ausgeschaltet (sie lägen sonst auf dem Spielbild) – einschalten auf der Seite Overlay.':
        '屏幕 {w}×{h} 在游戏画面两侧没有黑边：游戏中的系统数值、“今日”和音乐已关闭（否则会遮挡游戏画面）。可在“悬浮窗”页面中开启。',
    'Automatisch (Windows-Sprache)':
        '自动（Windows 语言）',
    'Erkennung':
        '识别',
    'Overlay':
        '悬浮窗',
    'System':
        '系统',
    'Fehler':
        '错误',
    'automatisch':
        '自动',
    'oben links':
        '左上',
    'oben rechts':
        '右上',
    'unten links':
        '左下',
    'unten rechts':
        '右下',
    'eigene Position':
        '自定义位置',
    'Karte ein/aus':
        '地图开/关',
    'Layout-Variante':
        '布局变体',
    'Bildschirm scannen':
        '扫描屏幕',
    'Vorherige Map':
        '上一张地图',
    'Nächste Map':
        '下一张地图',
    'Grösser':
        '放大',
    'Kleiner':
        '缩小',
    'Mit Maus verschieben':
        '用鼠标移动',
    'Noch keine Map':
        '尚无地图',
    'Karte ausblenden':
        '隐藏地图',
    'Karte einblenden':
        '显示地图',
    'Scannen':
        '扫描',
    'Overlay testen':
        '测试悬浮窗',
    'Test beenden':
        '结束测试',
    'Bild hinzufügen …':
        '添加图片…',
    'Zuordnen …':
        '分配…',
    'Server':
        '服务器',
    'Einstellungen':
        '设置',
    'Layout {n} von {total}':
        '布局 {n}/{total}',
    '(unsicher)':
        '（不确定）',
    'manuell gewählt':
        '手动选择',
    'per Scan gefunden':
        '通过扫描找到',
    'Letzte Runde: {time}':
        '上一局：{time}',
    'Unbekannte Map gelesen: „{text}“':
        '读取到未知地图：“{text}”',
    'Im Menü – Karte pausiert ({map})':
        '在菜单中，地图已暂停（{map}）',
    'Runde vorbei – wartet auf das nächste Match':
        '对局结束，等待下一场对局',
    'Karte ausgeblendet ({map})':
        '地图已隐藏（{map}）',
    'Wartet auf DBD':
        '正在等待 DBD',
    'DBD läuft – automatische Erkennung ist aus (Map von Hand wählen)':
        'DBD 正在运行，自动识别已关闭（请手动选择地图）',
    'Wartet auf das nächste Match':
        '正在等待下一场对局',
    'Simulation – wartet auf das Map-Banner':
        '模拟中，正在等待地图横幅',
    'Im Match: {map}':
        '对局中：{map}',
    'Karte eingeblendet':
        '地图已显示',
    'Kartenbild hinzufügen …':
        '添加地图图片…',
    'eigenes Bild für eine Map (Hintergrund wird entfernt)':
        '为地图使用你自己的图片（会去除背景）',
    'Eigene Bilder':
        '自己的图片',
    'Position':
        '位置',
    'Zurücksetzen':
        '重置',
    'Horizontal':
        '水平',
    'Vertikal':
        '垂直',
    'Fertig':
        '完成',
    '0 % = links/oben, 100 % = rechts/unten':
        '0 % = 左/上，100 % = 右/下',
    'Karte im schwarzen Rand halten':
        '将地图保持在黑边内',
    'Darstellung':
        '外观',
    'Grösse':
        '大小',
    'Karte anzeigen':
        '显示地图',
    'Karte im Overlay eingeblendet.':
        '地图显示在悬浮窗中。',
    'Karte im Overlay aus – es werden nur Timer, Ort und Ping angezeigt.':
        '悬浮窗中的地图已关闭，只显示计时器、位置和延迟。',
    'nichts anzuzeigen':
        '没有可显示的内容',
    'Aus: Das Overlay zeigt nur Rundentimer, Serverregion und Ping – ohne Karte. Erkennung, Rundenende und Statistik laufen wie gewohnt.':
        '关闭：悬浮窗只显示对局计时器、服务器区域和延迟，不显示地图。识别、对局结束和统计照常工作。',
    'Für diese Map zurücksetzen':
        '重置此地图',
    'eigene Grösse {n} % (Hotkeys/Strg+Mausrad)':
        '自定义大小 {n} %（快捷键/Ctrl+滚轮）',
    'gedreht um {deg}°':
        '旋转 {deg}°',
    'Killer':
        '杀手',
    'Survivor':
        '幸存者',
    'Rolle':
        '角色',
    'Rolle: {role}':
        '角色：{role}',
    'Alle Rollen':
        '所有角色',
    'Custom Game':
        '自定义对局',
    'Custom Games':
        '自定义对局',
    'Farming':
        '刷分',
    'Stil':
        '样式',
    'Original':
        '原版',
    'Dunkel':
        '深色',
    'Die Karten mit lila Boden, wie sie mitgeliefert werden – gilt auch im Spiel.':
        '带紫色地面的原版地图，在游戏中也同样适用。',
    'Klassisch':
        '经典',
    'Glas-Karten':
        '玻璃卡片',
    'Chips & Icons':
        '标签和图标',
    'Minimal Line':
        '极简线条',
    'SYSTEM':
        '系统',
    'Farming an/aus':
        '刷分开/关',
    'Farming-Runden':
        '刷分对局',
    'Runden ohne Crossplay als Farming zählen':
        '将关闭跨平台的对局计为刷分',
    'Alle Runden auf':
        '所有对局开启',
    'Farming-Runden zählen in Statistik und Aufnahmen überall mit; das Häkchen „Farming ausblenden“ (bei den Filtern) hält sie heraus, der Reiter Statistik → Farming listet sie immer. Crossplay aus erkennt das Programm an der Weltkugel mit rotem Kreuz neben dem Lobby-Knopf; Runden auf der gewählten Region zählen immer als Farming, auch ältere. Einzelne Runden: „Farming an/aus“ unter „Letzte Runden“.':
        '刷分对局在统计和录像中处处计入；“隐藏刷分”复选框（在筛选器旁边）可将其排除，“统计 → 刷分”选项卡始终列出它们。跨平台关闭是从大厅按钮旁带红叉的地球图标读取的；所选区域上的对局始终计为刷分，较早的也一样。单个对局：在“最近对局”下使用“刷分开/关”。',
    '{map} ({when}) zählt jetzt als Farming-Runde.':
        '{map}（{when}）现在计为刷分对局。',
    '{map} ({when}) zählt wieder als normale Runde.':
        '{map}（{when}）重新计为普通对局。',
    'Hinweis: Runden auf {region} zählen laut Einstellung weiter als Farming.':
        '注意：根据设置，{region} 上的对局仍计为刷分。',
    'Crossplay war aus – die Runde zählt als Farming-Runde.':
        '跨平台已关闭，该对局计为刷分对局。',
    'Crossplay war aus, die Lobby sah aus wie ein Custom Game – die Runde zählt als Farming-Runde, sobald die Stats-Seite sie als öffentliches Match zeigt.':
        '跨平台已关闭，大厅看起来像自定义对局。一旦统计页面将其显示为公开比赛，该对局即计为刷分对局。',
    '{off} von {n} Blicken mit Kreuz':
        '{n} 次查看中有 {off} 次出现红叉',
    'letzter Blick':
        '最后一次查看',
    'Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.':
        '跨平台已关闭（{looks}），下一局计为刷分对局。',
    'Crossplay ist an ({looks}) – keine Farming-Runde.':
        '跨平台已开启（{looks}），不是刷分对局。',
    'Als Custom Game erkannt – die Runde zählt nicht als Farming (unter „Letzte Runden“ mit „Farming an/aus“ korrigierbar).':
        '识别为自定义对局，该对局不计为刷分（可在“最近对局”下用“刷分开/关”更正）。',
    'Keine Lobby zur Runde ({why}) – sie zählt nicht als Farming.':
        '此对局没有大厅（{why}），不计为刷分。',
    'Lobby zu alt':
        '大厅太旧',
    'Lobby nicht gesehen':
        '未看到大厅',
    'Diese Runde als Farming-Runde zählen bzw. wieder als normale Runde – Farming-Runden zählen überall mit, bis „Farming ausblenden“ sie heraushält; der Reiter „Farming“ listet sie immer. Runden auf der Farming-Region (Einstellungen → Match-Daten) bleiben Farming.':
        '将此对局计为刷分对局或重新计为普通对局。刷分对局处处计入，直到“隐藏刷分”将其排除；“刷分”选项卡始终列出它们。刷分区域（设置 → 比赛数据）上的对局保持为刷分。',
    'Farming ausblenden':
        '隐藏刷分',
    'An: Farming-Runden (Crossplay aus, Farming-Region, Farming-Gegner) bleiben aus Statistik, Aufnahmen und Clips draussen – ein Schalter für alle drei. Aus: sie zählen wie jede andere Runde. Der Reiter Statistik → Farming zeigt sie immer.':
        '开启：刷分对局（跨平台关闭、刷分区域、刷分伙伴）不计入统计、录像和片段，一个开关管三处。关闭：它们和其他对局一样计入。“统计 → 刷分”选项卡始终显示它们。',
    'Zeigt die Lobby die Weltkugel mit rotem Kreuz (Crossplay aus), zählt die nächste Runde als Farming-Runde.':
        '如果大厅显示带红叉的地球图标（跨平台关闭），下一局计为刷分对局。',
    'Custom Game – keine Wartezeit.':
        '自定义对局，没有等待时间。',
    'Suche läuft: {time}':
        '匹配中：{time}',
    'Suche nach einem Match gestartet.':
        '开始匹配对局。',
    'Lobby verlassen – sie zählt für keine Runde.':
        '已离开大厅，不计入任何对局。',
    'Suche abgebrochen.':
        '匹配已取消。',
    'Lobby gefunden nach {time}{role}.':
        '{time} 后找到大厅{role}。',
    'Lobby gefunden{role}.':
        '已找到大厅{role}。',
    'Lobby nur kurz gesehen – Rolle und Crossplay von dort, ohne Wartezeit.':
        '大厅只短暂出现，角色和跨平台取自该处，没有等待时间。',
    'Wartezeit {time}':
        '等待了 {time}',
    'Verbindung in dieser Runde: {n} × Aussetzer, längster {s} s.':
        '本局连接：{n} 次断连，最长 {s} 秒。',
    '{n}× Aussetzer':
        '{n} 次断连',
    'Ergebnisbildschirm (zweiter Blick): gespielt als {role}.':
        '结算界面（第二次查看）：以{role}身份游戏。',
    'Ergebnisbildschirm: gespielt als {role}.':
        '结算界面：以{role}身份游戏。',
    'Wartezeit':
        '等待时间',
    'Regionen':
        '区域',
    'Markierte Runde:':
        '所选对局：',
    'Benachrichtigungen':
        '通知',
    'Runde auf {map} nicht gezählt: ihr Ende wurde nicht erkannt.':
        '{map} 上的对局未计入：未检测到其结束。',
    'Einstellungen exportieren …':
        '导出设置…',
    'Einstellungen importieren …':
        '导入设置…',
    'Einstellungen exportieren':
        '导出设置',
    'Einstellungen importieren':
        '导入设置',
    'Export fehlgeschlagen: {error}':
        '导出失败：{error}',
    'Einstellungen gesichert: {path}':
        '设置已保存：{path}',
    'Das ist keine Einstellungsdatei von Fog Scout ({error}).':
        '这不是 Fog Scout 设置文件（{error}）。',
    'Alle Einstellungen durch die aus der Datei ersetzen? Das Programm startet danach neu.':
        '用文件中的设置替换所有设置吗？之后程序将重新启动。',
    'Einstellungen importiert aus {path}.':
        '已从 {path} 导入设置。',
    'Bitte das Programm jetzt neu starten.':
        '请立即重新启动程序。',
    'Speichert alle Einstellungen in eine Datei: Hotkeys, Grösse und Drehung pro Map, eigene Map-Zuordnungen, Overlay, Regionen … Die Statistik (rounds.jsonl) gehört nicht dazu.':
        '将所有设置保存到文件中：快捷键、每张地图的大小和旋转、自己的地图分配、悬浮窗、区域…… 统计数据（rounds.jsonl）不包含在内。',
    'Lädt eine exportierte Einstellungsdatei und startet das Programm neu. Fehlende Werte (ältere Sicherung) bekommen ihren Standard.':
        '加载导出的设置文件并重新启动程序。缺少的值（较旧的备份）使用默认值。',
    'Ton und Meldung, wenn eine Lobby gefunden wurde':
        '找到大厅时播放声音并通知',
    'Erinnern, wenn der Lobby-Countdown abläuft und READY noch nicht gedrückt ist':
        '大厅倒计时即将结束且尚未按下 READY 时提醒我',
    'Nur wenn DBD nicht das aktive Fenster ist':
        '仅当 DBD 不是活动窗口时',
    'Die Meldung erscheint unten rechts über allen Fenstern – auch bei „Nicht stören“ – und nimmt dem aktiven Fenster nicht den Fokus. Klick darauf schliesst sie.':
        '通知显示在右下角所有窗口之上（“勿扰模式”下也会显示），且不会抢走活动窗口的焦点。点击即可关闭。',
    'Meldung testen':
        '测试通知',
    'Zeigt die Meldung und spielt den Ton – so siehst du, wo sie erscheint.':
        '显示通知并播放声音，让你看到它出现的位置。',
    'Lobby gefunden':
        '已找到大厅',
    'nach {time}':
        '{time} 后',
    'READY drücken.':
        '请按 READY。',
    'Lobby startet gleich':
        '大厅即将开始',
    'Noch {n} s – READY ist noch nicht gedrückt.':
        '还剩 {n} 秒，尚未按下 READY。',
    'Lobby-Countdown läuft ab, READY ist noch nicht gedrückt.':
        '大厅倒计时即将结束，尚未按下 READY。',
    'Ø Ping':
        '平均延迟',
    'Spielt einen Hinweiston und zeigt eine Windows-Meldung, sobald DBD eine Lobby gefunden hat – praktisch, wenn du während der Suche etwas anderes machst.':
        'DBD 一找到大厅就播放声音并显示 Windows 通知，方便你在匹配时做其他事情。',
    'Noch einmal melden, wenn der Countdown der Lobby unter 15 s fällt und du READY nicht gedrückt hast.':
        '大厅倒计时低于 15 秒且你尚未按下 READY 时再次通知。',
    'Keine Meldung, solange DBD im Vordergrund ist – dann siehst du die Lobby ja selbst.':
        'DBD 在前台时不通知，因为你自己能看到大厅。',
    'Bilanz der Sitzung zeigen, wenn DBD beendet wurde':
        '关闭 DBD 时显示本次游戏的数据',
    'Etwa 15 s nachdem DBD geschlossen wurde: eine Meldung mit den Runden der Sitzung, der Spielzeit und – mit Match-Daten – Ø Kills, Entkommen und Bloodpoints. Steht auch im Log.':
        '关闭 DBD 约 15 秒后：显示一条通知，包含本次游戏的对局数、游戏时长，以及（有比赛数据时）平均击杀、逃脱和血点。也会写入日志。',
    'Sitzung beendet':
        '本次游戏结束',
    '1 Runde':
        '1 局',
    '{bp} BP':
        '{bp} 血点',
    'Melden, wenn eine Runde keine Blutpunkte gebracht hat (Cap erreicht)':
        '对局未获得血点（已达上限）时通知',
    'Fog Scout liest in der Lobby den Blutpunkte-Stand oben rechts. Ist er nach einer gezählten Runde derselbe wie davor, ist das Cap erreicht (normal 5 Millionen, nach Tome-Belohnungen auch mehr) – die Punkte der Runde sind verfallen. Ton und Meldung kommen auch, wenn DBD im Vordergrund ist; Custom Games zählen nicht.':
        'Fog Scout 会读取大厅右上角的血点余额。如果计入的对局结束后余额与之前相同，说明已达上限（通常为 500 万，领取档案奖励后更多），该局的血点就浪费了。DBD 在前台时也会有声音和通知；自定义对局不计入。',
    'Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte dieser Runde sind verfallen.':
        '血点未变：对局前后均为 {bp}，已达上限，本局的血点已浪费。',
    'Blutpunkte-Cap erreicht':
        '已达血点上限',
    '{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die nächste Runde nichts.':
        '对局前后均为 {bp} 血点。请在血网中花掉它们，否则下一局也将一无所获。',
    'Blutpunkte: +{gain} in dieser Runde, Stand {bp}.':
        '血点：本局 +{gain}，余额 {bp}。',
    'Blutpunkte: Stand {bp} nach der Runde, vorher {before}.':
        '血点：对局后余额 {bp}，之前为 {before}。',
    'BP-Stand':
        '血点余额',
    'Aussetzer':
        '卡顿',
    'Alles sichern (ZIP) …':
        '全部备份（ZIP）…',
    'Aus Sicherung wiederherstellen (ZIP) …':
        '从备份恢复（ZIP）…',
    'Aus Sicherung wiederherstellen':
        '从备份恢复',
    'Führt eine Sicherung von „Alles sichern“ mit den jetzigen Daten zusammen: Runden, Match-Daten, Kartenbilder und Banner, die fehlen, kommen dazu – Vorhandenes bleibt, wie es ist. Zeigt vorher, was dazukommt. Die Einstellungen der Sicherung nur auf eigene Rückfrage.':
        '将“全部备份”生成的备份与你现有的数据合并：添加缺少的对局、比赛数据、地图图片和横幅，已有内容保持不变。会先显示将要添加的内容。备份中的设置会单独询问。',
    'Während einer Runde nicht möglich – nach dem Rundenende noch einmal.':
        '对局中无法执行，请在对局结束后重试。',
    'Das ist keine Sicherung von Fog Scout ({error}).':
        '这不是 Fog Scout 备份（{error}）。',
    '{rounds} Runden, {lost} nicht gezählte Runden, {matches} Matches, {files} Bilder/Banner':
        '{rounds} 局，{lost} 局未计入，{matches} 场比赛，{files} 个图片/横幅',
    'Alles aus der Sicherung ist schon da – nichts hinzuzufügen.':
        '备份中的所有内容都已存在，无需添加。',
    'Aus der Sicherung hinzufügen: {what}. Schon vorhanden (bleibt, wie es ist): {known}. Vorher kommt eine Kopie der Runden und Match-Daten nach backup/.':
        '从备份中添加：{what}。已存在（保持不变）：{known}。对局和比赛数据会先复制一份到 backup/。',
    'Zusammenführen':
        '合并',
    'Wiederherstellen fehlgeschlagen: {error}':
        '恢复失败：{error}',
    'Aus der Sicherung hinzugefügt: {what}.':
        '已从备份中添加：{what}。',
    'Einstellungen der Sicherung nicht lesbar: {error}':
        '无法读取备份中的设置：{error}',
    'Die Sicherung enthält auch Einstellungen – übernehmen ersetzt die aktuellen.':
        '备份中也包含设置，采用它们将替换当前设置。',
    'Installation prüfen':
        '检查安装',
    'Installation wird geprüft …':
        '正在检查安装…',
    'Installation prüfen – Fehler: {line}':
        '检查安装 – 失败：{line}',
    '{n} von {total} Prüfungen fehlgeschlagen – Einzelheiten im Log. Eine Neuinstallation (Setup erneut ausführen) behebt fehlende Dateien meist.':
        '{total} 项检查中有 {n} 项失败，详见日志。重新安装（再次运行安装程序）通常能修复缺失的文件。',
    'Alle {n} Prüfungen bestanden: {names}.':
        '全部 {n} 项检查通过：{names}。',
    'Installation prüfen: {text}':
        '检查安装：{text}',
    'Prüft, ob alles da ist und läuft: Programmdateien, Kartenbilder, Bibliotheken, alle Module, Telemetrie aus, Texterkennung, ffmpeg, Qt – derselbe Selbsttest wie bei jedem Build. Läuft als eigener Prozess, Ergebnis im Log.':
        '检查所有内容是否齐全且正常工作：程序文件、地图图片、库、所有模块、遥测已关闭、文字识别、ffmpeg、Qt，与每次构建时的自检相同。在独立进程中运行，结果写入日志。',
    'Alles sichern':
        '全部备份',
    'Gesichert: {n} Dateien in {path}':
        '已备份：{n} 个文件到 {path}',
    'Sichern fehlgeschlagen: {error}':
        '备份失败：{error}',
    'Packt Runden, Match-Daten, die Einstellungen (ohne Passwörter und PC-eigene Werte), eigene Kartenbilder und den Banner-Korpus in eine ZIP-Datei – zum Aufbewahren oder für einen anderen PC. Aufnahmen und Logs bleiben draussen.':
        '将对局、比赛数据、设置（不含密码和本机专属值）、自己的地图图片和横幅语料库打包成一个 ZIP 文件，用于保存或在另一台电脑上使用。录像和日志不包含在内。',
    'Spielmodus':
        '游戏模式',
    'Eigener Charakter':
        '自己的人物',
    'Eigene Perks':
        '自己的技能',
    'JSON (für eigene Auswertungen)':
        'JSON（用于自行分析）',
    'Eine Liste mit einem Objekt je Runde, die Spaltentitel als Schlüssel – für eigene Auswertungen (Python, Tabellen, jq).':
        '每个对局一个对象的列表，以列标题为键，用于自行分析（Python、表格、jq）。',
    'Rolle für {map} ({when}) auf {role} geändert.':
        '{map}（{when}）的角色已改为{role}。',
    'Rolle konnte nicht gespeichert werden: {error}':
        '无法保存角色：{error}',
    'Diese Runde als Killer-Runde zählen (falls die Erkennung falsch lag).':
        '将此对局计为杀手对局（如果识别错误）。',
    'Diese Runde als Survivor-Runde zählen (falls die Erkennung falsch lag).':
        '将此对局计为幸存者对局（如果识别错误）。',
    'Diese Runde als Custom Game zählen – sie fliesst dann nicht in die Wartezeit ein.':
        '将此对局计为自定义对局，之后它不计入等待时间。',
    'Noch keine Wartezeiten in dieser Auswahl.':
        '此筛选范围内还没有等待时间。',
    'nach Wochentag':
        '按星期',
    'nach Uhrzeit':
        '按时段',
    'nach Region':
        '按区域',
    'Wann/Wo':
        '时间/地点',
    'Ø Wartezeit':
        '平均等待',
    'Kürzeste':
        '最短',
    'Warten':
        '等待',
    'Uhr':
        '时',
    'Montag':
        '星期一',
    'Dienstag':
        '星期二',
    'Mittwoch':
        '星期三',
    'Donnerstag':
        '星期四',
    'Freitag':
        '星期五',
    'Samstag':
        '星期六',
    'Sonntag':
        '星期日',
    'Gemessen von „CANCEL“ (Suche läuft) bis zur gefundenen Lobby – nur wenn das Programm die Suche gesehen hat. Custom Games haben keine Wartezeit.':
        '从“CANCEL”（匹配中）开始计时，直到找到大厅为止，仅在程序看到匹配过程时有效。自定义对局没有等待时间。',
    'Map-Namen oben einfügen (wie bei den mitgelieferten Karten)':
        '在顶部写上地图名称（与自带地图一样）',
    'Das Bild hat oben schon einen Namen – es wird keiner hinzugefügt.':
        '图片顶部已有名称，不再添加。',
    'Schreibt den Map-Namen weiss mit Schatten über die Karte, im Stil der mitgelieferten Karten. Hat das Bild oben schon einen Namen, passiert nichts. Beim Drehen bleibt der Name aufrecht.':
        '按照自带地图的样式，在地图上方用带阴影的白字写上地图名称。如果图片顶部已有名称，则不做任何操作。旋转地图时名称保持正向。',
    'Drehen':
        '旋转',
    'Karte drehen':
        '旋转地图',
    'Etage wechseln':
        '切换楼层',
    'Beide Etagen':
        '两层',
    'Etage {n} von {total}':
        '楼层 {n}/{total}',
    'Diese Map hat nur eine Etage.':
        '此地图只有一层。',
    'Wechselt die Anzeige bei Karten mit Etagen (Midwich): beide untereinander → unten → oben → beide. Gilt bis zur nächsten Map.':
        '切换多层地图（Midwich）的显示方式：两层上下排列 → 底层 → 顶层 → 两层。持续到下一张地图。',
    'Etagen untereinander zeigen':
        '多层地图上下排列显示',
    'An: Karten mit Etagen (Midwich) zeigen alle Etagen untereinander, oben über unten – jede so groß wie eine normale Karte, soweit der Platz reicht. Aus: Sie starten mit der unteren Etage. Der Knopf „Etage“ oder der Hotkey schaltet jederzeit um.':
        '开启：多层地图（Midwich）将所有楼层上下排列显示，顶层在上、底层在下，在空间允许的情况下每层与普通地图一样大。关闭：从底层开始显示。“楼层”按钮或快捷键随时可以切换。',
    '{map} um {deg}° gedreht.':
        '{map} 已旋转 {deg}°。',
    'Drehung für {map} entfernt.':
        '已移除 {map} 的旋转。',
    'Dreht die angezeigte Karte um 90° im Uhrzeigersinn (für jede Map gemerkt). Der Map-Name darüber bleibt aufrecht, die Zahlen in der Karte drehen sich mit.':
        '将当前显示的地图顺时针旋转 90°（每张地图分别记住）。上方的地图名称保持正向，地图内的数字随之旋转。',
    'Eigene Grösse für {map} entfernt – es gilt wieder der Schieberegler.':
        '已移除 {map} 的自定义大小，重新使用滑块设置。',
    'Entfernt eigene Grösse und Drehung der angezeigten Map – danach gilt wieder der Schieberegler für alle Maps.':
        '移除当前显示地图的自定义大小和旋转，重新使用适用于所有地图的滑块。',
    'Deckkraft':
        '不透明度',
    'Nur zeigen, wenn DBD das aktive Fenster ist':
        '仅在 DBD 为活动窗口时显示',
    'Map-Namen über der Karte anzeigen':
        '在地图上方显示地图名称',
    'Rundentimer unter der Karte anzeigen':
        '在地图下方显示对局计时器',
    'Verbundenen Server unter der Karte':
        '在地图下方显示所连接的服务器',
    'Transparenter Rand um die Karte':
        '地图周围的透明边缘',
    'Map beim Match-Start automatisch erkennen':
        '对局开始时自动识别地图',
    'Overlay ausblenden, sobald ich nicht mehr in der Runde bin':
        '离开对局后立即隐藏悬浮窗',
    'erkennt Ergebnisbildschirm, Lobby/Menüs, Ladebildschirm und geschlossenes DBD':
        '检测结算界面、大厅/菜单、加载界面以及 DBD 关闭',
    'Overlay pausieren, solange ein DBD-Menü offen ist':
        '打开 DBD 菜单时暂停悬浮窗',
    'erkannt am sichtbaren Mauszeiger (ESC-Menü, Ergebnisbildschirm, Lobby)':
        '通过可见的鼠标指针检测（ESC 菜单、结算界面、大厅）',
    'Spielsprache (Map-Namen)':
        '游戏语言（地图名称）',
    'Erweitert':
        '高级',
    'Erweitert (Fehlersuche)':
        '高级（故障排除）',
    'Technik':
        '技术',
    'Auch erkennen, wenn andere Fenster über DBD liegen':
        '其他窗口遮挡 DBD 时也进行识别',
    'Fensteraufnahme wie bei OBS, nur solange DBD im Hintergrund ist':
        '像 OBS 一样进行窗口捕获，仅在 DBD 处于后台时',
    'Scans/Sek.':
        '扫描/秒',
    'Rundenende-Erkennung: {state}':
        '对局结束检测：{state}',
    'Debug-Bilder speichern':
        '保存调试图片',
    'Banner jeder Erkennung für „Erkennung prüfen“ sammeln':
        '为“检查识别”保留每次识别的横幅',
    '{n} Banner gesammelt':
        '已保留 {n} 个横幅',
    '1 Banner gesammelt':
        '已保留 1 个横幅',
    'letzte Prüfung: {hits} von {total} erkannt':
        '上次检查：{total} 个中识别出 {hits} 个',
    'Erkennung prüfen':
        '检查识别',
    'Korpus exportieren …':
        '导出语料库…',
    'Korpus exportieren':
        '导出语料库',
    'Korpus-Ordner öffnen':
        '打开语料库文件夹',
    'Noch keine Banner gesammelt – sie kommen mit jeder erkannten Map.':
        '尚未保留横幅，每识别一张地图就会保留一个。',
    'Erkennung prüfen: {n} Banner werden neu gelesen …':
        '检查识别：正在重新读取 {n} 个横幅…',
    'Erkennung prüfen fehlgeschlagen: {error}':
        '检查识别失败：{error}',
    '{hits} von {total} Bannern wieder erkannt ({seconds} s).':
        '{total} 个横幅中重新识别出 {hits} 个（{seconds} 秒）。',
    '{n} nicht lesbar.':
        '{n} 个无法读取。',
    'Erkennung prüfen: {text}':
        '检查识别：{text}',
    'Erkennung prüfen – {stamp}: erwartet {want}, gelesen „{read}“ → {got}':
        '检查识别 – {stamp}：应为 {want}，读取到“{read}” → {got}',
    'Die Treffer, die fehlen, stehen im Log.':
        '未识别出的横幅已写入日志。',
    'Korpus exportiert: {n} Dateien nach {path}':
        '语料库已导出：{n} 个文件到 {path}',
    'Korpus exportieren fehlgeschlagen: {error}':
        '导出语料库失败：{error}',
    'Speichert bei jeder erkannten Map den Ausschnitt um die Banner-Linie (Name und Realm) im Datenordner unter corpus/, höchstens 300 Stück – die Grundlage für „Erkennung prüfen“. Der Ausschnitt kann den linken HUD-Rand mit Spielernamen zeigen; er bleibt auf diesem PC.':
        '每识别一张地图，就在数据文件夹的 corpus/ 下保留横幅线周围的部分（名称和领域），最多 300 个，作为“检查识别”的基础。该部分可能包含带玩家名称的 HUD 左边缘；它只保存在这台电脑上。',
    'Liest alle gesammelten Banner mit der Erkennung neu und zählt, wie viele wieder die gespeicherte Map ergeben – nach einem Update oder einer geänderten Spielsprache. Läuft im Hintergrund, Ergebnis im Log.':
        '用识别功能重新读取所有保留的横幅，统计有多少能再次得出已保存的地图，适用于更新后或更改游戏语言后。在后台运行，结果写入日志。',
    'Packt alle gesammelten Banner mit ihren Angaben in eine ZIP-Datei – z. B. um sie für die Tests des Projekts weiterzugeben. Vorher die Bilder ansehen: sie können Spielernamen zeigen.':
        '将所有保留的横幅及其详细信息打包成 ZIP 文件，例如提供给本项目的测试使用。请先查看图片：它们可能包含玩家名称。',
    'Öffnet den Ordner corpus/ im Datenordner.':
        '打开数据文件夹中的 corpus/ 文件夹。',
    'Bildschirm jetzt scannen':
        '立即扫描屏幕',
    'Diagnose kopieren':
        '复制诊断信息',
    'Verbundener Spielserver':
        '已连接的游戏服务器',
    'Serverregionen':
        '服务器区域',
    'DBD sucht Matches nur in den angehakten Regionen (über die Windows-hosts-Datei, das Spiel wird nicht verändert). Nach „Auswahl anwenden“ DBD neu starten.':
        'DBD 只在勾选的区域中匹配对局（通过 Windows hosts 文件，不修改游戏）。“应用选择”后请重新启动 DBD。',
    'Region':
        '区域',
    'hosts-Datei':
        'hosts 文件',
    'Ping messen':
        '测量延迟',
    'Auswahl anwenden':
        '应用选择',
    'Alles freigeben':
        '全部允许',
    'Mit VPN unzuverlässig. Region-Tools sind von BHVR weder erlaubt noch verboten – auf eigene Verantwortung.':
        '使用 VPN 时不可靠。BHVR 既未允许也未禁止区域工具，风险自负。',
    'Warte auf Windows (Administratorrechte) …':
        '正在等待 Windows（管理员权限）…',
    'Aus':
        '关',
    'Zeigt Region und Ping des Spielservers, auch im Overlay (braucht Administratorrechte).':
        '显示游戏服务器的区域和延迟，也会显示在悬浮窗中（需要管理员权限）。',
    'DBD läuft mit {w}×{h}, kleiner als 1920×1080: die Erkennung ist unsicherer (vor allem Lobby-Knopf und Killername). Fenster größer ziehen oder „Fenster-Vollbild“ nutzen.':
        'DBD 以 {w}×{h} 运行，小于 1920×1080：识别不太可靠（尤其是大厅按钮和杀手名称）。请把窗口调大或使用“窗口化全屏”。',
    'DBD-Fenster ist schmaler als 16:9 ({w}×{h}): diese Form ist ungetestet, Map- und Rundenende-Erkennung können danebenliegen. Am sichersten: 16:9 oder breiter.':
        'DBD 窗口比 16:9 更窄（{w}×{h}）：此形状未经测试，地图和对局结束识别可能出错。最稳妥：16:9 或更宽。',
    'Verbunden mit: {server}':
        '已连接到：{server}',
    'pausiert, bis DBD läuft':
        '已暂停，直到 DBD 运行',
    'Anzeige des Spielservers beendet.':
        '游戏服务器显示已停止。',
    'Spielserver-Anzeige: {error}':
        '游戏服务器显示：{error}',
    'Spielserver-Anzeige läuft (liest nur Paketköpfe, keine Inhalte).':
        '游戏服务器显示运行中（只读取数据包头，不读取内容）。',
    'Spielserver-Anzeige pausiert – DBD läuft nicht (startet automatisch mit DBD).':
        '游戏服务器显示已暂停，DBD 未运行（DBD 启动后自动恢复）。',
    'Spielserver-Anzeige beendet: {error}':
        '游戏服务器显示已停止：{error}',
    ' – nicht in deiner Regionsauswahl':
        ' – 不在你选择的区域中',
    'Verbunden mit Spielserver: {region}{note}.':
        '已连接到游戏服务器：{region}{note}。',
    'hosts-Datei nicht lesbar: {error}':
        '无法读取 hosts 文件：{error}',
    'Aktiv: nur {regions} erlaubt.':
        '已生效：仅允许 {regions}。',
    '(keine)':
        '（无）',
    'Keine eigene Auswahl aktiv, aber andere Einträge sperren Regionen.':
        '没有生效的自定义选择，但其他条目屏蔽了一些区域。',
    'Keine Region gesperrt – DBD wählt selbst.':
        '未屏蔽任何区域，由 DBD 自行选择。',
    'anderen Programmen':
        '其他程序',
    ' Es gibt {n} Einträge von {who} für DBD-Server (werden beim Anwenden ersetzt).':
        ' 有 {n} 个来自 {who} 的 DBD 服务器条目（应用时会被替换）。',
    'Serverregionen: {text}':
        '服务器区域：{text}',
    'Messe Ping zu den Serverregionen …':
        '正在测量到各服务器区域的延迟…',
    'Ping fehlgeschlagen: {error}':
        '测量延迟失败：{error}',
    'Am schnellsten: {list}.':
        '最快：{list}。',
    'Keine Region hat geantwortet (Internet/Firewall/VPN?).':
        '没有区域响应（网络/防火墙/VPN？）。',
    'Bitte mindestens eine Region anhaken.':
        '请至少勾选一个区域。',
    'Erlaubt bleiben: {names}.\n\nAlle anderen DBD-Serverregionen werden in der Windows-hosts-Datei gesperrt. Windows fragt gleich nach Administratorrechten.':
        '允许：{names}。\n\n其他所有 DBD 服务器区域将在 Windows hosts 文件中被屏蔽。Windows 会请求管理员权限。',
    '{n} vorhandene Einträge anderer Programme (z. B. Make Your Choice) für DBD-Server werden dabei entfernt.':
        '将移除其他程序（例如 Make Your Choice）为 DBD 服务器添加的 {n} 个现有条目。',
    'Danach DBD neu starten, damit es wirkt.':
        '之后请重新启动 DBD 使其生效。',
    'Serverregionen anwenden':
        '应用服务器区域',
    'Nur noch {names} erlaubt':
        '仅允许 {names}',
    'Es ist nichts gesperrt.':
        '未屏蔽任何内容。',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen (auch die von Make Your Choice)?':
        '要从 hosts 文件中移除所有对 DBD 服务器区域的屏蔽（包括 Make Your Choice 的）吗？',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen?':
        '要从 hosts 文件中移除所有对 DBD 服务器区域的屏蔽吗？',
    'Windows fragt gleich nach Administratorrechten. Danach DBD neu starten.':
        'Windows 会请求管理员权限。之后请重新启动 DBD。',
    'Serverregionen freigeben':
        '允许服务器区域',
    'Alle Regionen freigegeben':
        '已允许所有区域',
    'Serverregionen: {text}. DBD neu starten, damit es wirkt.':
        '服务器区域：{text}。请重新启动 DBD 使其生效。',
    '{text}. DBD jetzt neu starten.':
        '{text}。请立即重新启动 DBD。',
    'Keine Änderung nötig.':
        '无需更改。',
    'unbekannter Fehler':
        '未知错误',
    'Firewall-Regeln von Make Your Choice („Enforced“) gefunden – sie sperren Regionen unabhängig von der hosts-Datei. In Make Your Choice „Revert to Default“ drücken.':
        '发现 Make Your Choice 的防火墙规则（“Enforced”），它们会无视 hosts 文件屏蔽区域。请在 Make Your Choice 中点击“Revert to Default”。',
    'Achtung: Firewall-Regeln von Make Your Choice aktiv (siehe Log).':
        '注意：Make Your Choice 的防火墙规则处于生效状态（见日志）。',
    'Europa':
        '欧洲',
    'Amerika':
        '美洲',
    'Asien':
        '亚洲',
    'Ozeanien':
        '大洋洲',
    'frei':
        '已允许',
    'gesperrt':
        '已屏蔽',
    'gesperrt (fremd)':
        '已屏蔽（其他程序）',
    'umgeleitet (fremd)':
        '已重定向（其他程序）',
    'Frankfurt':
        '法兰克福',
    'Irland':
        '爱尔兰',
    'London':
        '伦敦',
    'USA Ost (N. Virginia)':
        '美国东部（弗吉尼亚北部）',
    'USA Ost (Ohio)':
        '美国东部（俄亥俄）',
    'USA West (N. Kalifornien)':
        '美国西部（加利福尼亚北部）',
    'USA West (Oregon)':
        '美国西部（俄勒冈）',
    'Kanada (Zentral)':
        '加拿大（中部）',
    'Südamerika (São Paulo)':
        '南美洲（圣保罗）',
    'Tokio':
        '东京',
    'Seoul':
        '首尔',
    'Mumbai':
        '孟买',
    'Singapur':
        '新加坡',
    'Hongkong':
        '香港',
    'Sydney':
        '悉尼',
    'Name nicht auflösbar':
        '无法解析名称',
    'Start mit Administratorrechten fehlgeschlagen (Fehler {code}).':
        '以管理员权限启动失败（错误 {code}）。',
    'Hilfsprogramm nicht gestartet.':
        '辅助程序未启动。',
    'Das Hilfsprogramm hat kein Ergebnis geliefert (Code {code}).':
        '辅助程序未返回结果（代码 {code}）。',
    'Zeitüberschreitung beim Schreiben der hosts-Datei.':
        '写入 hosts 文件超时。',
    'Abgebrochen (keine Administratorrechte erteilt).':
        '已取消（未授予管理员权限）。',
    'Warte auf Match …':
        '正在等待对局…',
    'Global':
        '全球',
    'keine Daten vom Mitschnitt':
        '捕获未提供数据',
    'Nur unter Windows verfügbar.':
        '仅在 Windows 上可用。',
    'Mitschnitt beendet (Code {code}).':
        '捕获已结束（代码 {code}）。',
    'Fehler: {error}':
        '错误：{error}',
    'Statistik':
        '统计',
    'Maps':
        '地图',
    'Map':
        '地图',
    'Runden':
        '对局',
    'Ø Dauer':
        '平均时长',
    'Letzte Runden':
        '最近对局',
    'Gesamter Zeitraum':
        '全部时间',
    'Heute':
        '今天',
    'Diese Woche':
        '本周',
    'Dieser Monat':
        '本月',
    'Dieses Jahr':
        '今年',
    'Alle Regionen':
        '所有区域',
    'Alle Killer':
        '所有杀手',
    'Häufigste Map':
        '最常见地图',
    'Der markierte Name (Skin oder neuer Killer) zählt ab jetzt als der gewählte Killer – auch in allen bisherigen Runden.':
        '所选名称（皮肤或新杀手）从现在起计为所选杀手，过去的所有对局也一样。',
    'Entfernt alle eigenen Killer-Zuordnungen; die Namen erscheinen wieder so, wie sie gelesen wurden.':
        '移除所有自己的杀手分配；名称将恢复为读取时的样子。',
    'Zuordnen':
        '分配',
    'Warte auf Map':
        '正在等待地图',
    'Solange DBD läuft und keine Karte eingeblendet ist, zeigt das Overlay eine kleine Karte: „Warte auf Map“, darunter Suche/Lobby (z. B. „Suche läuft: 02:13 · Nurse“) oder die letzte Runde. Gilt nicht, wenn du die Karte selbst ausgeblendet hast.':
        'DBD 运行且未显示地图时，悬浮窗会显示一张小卡片：“正在等待地图”，下方是匹配/大厅状态（例如“匹配中：02:13 · Nurse”）或上一局。如果是你自己隐藏了地图，则不显示。',
    'Ohne Karte: „Warte auf Map“ und Lobby-Status anzeigen':
        '没有地图时：显示“正在等待地图”和大厅状态',
    'Killer der Runde:':
        '本局杀手：',
    'Killer setzen':
        '设置杀手',
    'Notiz zum Killer:':
        '关于杀手的备注：',
    'Um diese Tageszeit ({span} Uhr) am schnellsten: {region} – Wartezeit {wait} (Median), {n} Runden':
        '此时段（{span} 时）最快：{region}，等待 {wait}（中位数），{n} 局',
    'Ø {ping} ms':
        '平均 {ping} 毫秒',
    'danach {region} ({wait})':
        '其次 {region}（{wait}）',
    'Notiz speichern':
        '保存备注',
    'Notiz zu {killer} gespeichert.':
        '已保存关于 {killer} 的备注。',
    'Notiz zu {killer} gelöscht.':
        '已移除关于 {killer} 的备注。',
    'Eigene Notiz zum markierten Killer, z. B. „Lithe, nicht vaulten“. Erscheint im Spiel unter der Map-Notiz, sobald dieser Killer in der Runde ist (eigener Killer oder, als Survivor, der aus der Lobby). Leer speichern löscht sie.':
        '你对标记杀手的备注，例如“灵活，别翻窗”。只要该杀手出现在对局中（你自己使用的杀手，或作为幸存者时大厅中的杀手），就会在游戏中显示在地图备注下方。保存为空即可移除。',
    'Killer konnte nicht gespeichert werden: {error}':
        '无法保存杀手：{error}',
    'Killer für {map} ({when}) auf {killer} gesetzt.':
        '{map}（{when}）的杀手已设为 {killer}。',
    'Map der Runde:':
        '本局地图：',
    'Setzt die Map nur für die markierten Runden – wenn das Banner falsch gelesen wurde. Statistik, eigener Rekord und die Verknüpfung mit den Match-Daten folgen; die Aufnahme behält ihren Namen.':
        '仅为标记的对局设置地图，用于横幅读取错误的情况。统计、个人战绩和与比赛数据的关联会随之更新；录像保留原名称。',
    'Map setzen':
        '设置地图',
    'Map konnte nicht gespeichert werden: {error}':
        '无法保存地图：{error}',
    'Map der Runde vom {when} auf {map} gesetzt.':
        '{when} 的对局地图已设为 {map}。',
    'Setzt den Killer nur für die markierte Runde und zählt sie als Killer-Runde – z. B. wenn sie fälschlich als Survivor gezählt wurde oder der Name falsch gelesen wurde.':
        '仅为所选对局设置杀手并将其计为杀手对局，例如被错误计为幸存者或名称读取错误时。',
    'Zuordnungen löschen':
        '删除分配',
    '„{name}“ zählt jetzt als {killer}.':
        '“{name}”现在计为 {killer}。',
    'Alle eigenen Killer-Zuordnungen löschen?':
        '删除所有自己的杀手分配吗？',
    'Killer-Zuordnungen gelöscht.':
        '杀手分配已删除。',
    'ohne Region':
        '无区域',
    'Anteil':
        '占比',
    'Region nur bekannt, wenn im Tab Server „Verbundener Spielserver“ an war.':
        '仅当“服务器”选项卡中开启了“已连接的游戏服务器”时才知道区域。',
    'Wann':
        '时间',
    'Dauer':
        '时长',
    'Alle Runden löschen …':
        '删除所有对局…',
    'Runde löschen':
        '删除对局',
    'Ø {kills} Kills · {n} Runden':
        '平均 {kills} 击杀 · {n} 局',
    'Killer: Ø {kills} Kills, {four}× 4K ({n})':
        '杀手：平均 {kills} 击杀，{four} 次 4 杀（{n}）',
    'Survivor: {share} entkommen ({n})':
        '幸存者：{share} 逃脱（{n}）',
    '{share} entkommen · {n} Runden':
        '{share} 逃脱 · {n} 局',
    'Eigene Bilanz unter dem Timer':
        '在计时器下方显示个人战绩',
    'Eigene Notiz unter dem Timer':
        '在计时器下方显示自己的备注',
    'Zeigt deine eigene Notiz zur Map unter dem Rundentimer – geschrieben auf der Seite Maps (Map anklicken oder Rechtsklick → „Notiz bearbeiten …“), höchstens vier Zeilen.':
        '在对局计时器下方显示你对该地图的备注，在“地图”页面中编写（点击地图或右键 → “编辑备注…”），最多四行。',
    'Deine Notiz zu dieser Map – wird beim Tippen gespeichert und im Spiel unter dem Timer gezeigt (höchstens vier Zeilen). Leer = keine Notiz.':
        '你对这张地图的备注，输入时自动保存，并在游戏中显示在计时器下方（最多四行）。留空 = 无备注。',
    'Eigene Notiz (im Spiel unter dem Timer)':
        '自己的备注（游戏中显示在计时器下方）',
    'z. B. Shack links vom Main, Gen im Keller …':
        '例如：主建筑左边是小屋，地下室有发电机…',
    'Notiz bearbeiten …':
        '编辑备注…',
    'Map-Stile':
        '地图样式',
    'Alle auf einmal':
        '全部一起',
    'Kartenstile für {map} werden im Hintergrund erstellt.':
        '正在后台生成 {map} 的地图样式。',
    'Kartenstil {style} für {map} wird im Hintergrund erstellt.':
        '正在后台生成 {map} 的地图样式 {style}。',
    'Eigene Notiz':
        '自己的备注',
    'Eigene Notiz: {note}':
        '自己的备注：{note}',
    'Zeigt unter dem Rundentimer, wie es dir auf dieser Map bisher ging: als Killer Ø Kills, als Survivor den Anteil Escapes – aus den Runden mit Daten der Stats-Seite, ab 3 Runden.':
        '在对局计时器下方显示你在这张地图上的表现：作为杀手的平均击杀数，作为幸存者的逃脱占比，基于有统计页面数据的对局，满 3 局后显示。',
    'Entfernt die markierte Runde aus der Statistik – z. B. eine Map, die mitten im Match falsch erkannt wurde. Fragt vorher nach.':
        '从统计中移除标记的对局，例如对局中途读错的地图。会先询问。',
    'Runde {what} aus der Statistik löschen?':
        '要从统计中删除对局 {what} 吗？',
    'Runde konnte nicht gelöscht werden: {error}':
        '无法删除对局：{error}',
    'Runde gelöscht: {map} ({when}).':
        '对局已删除：{map}（{when}）。',
    'Noch keine Runden gespeichert.':
        '尚未保存任何对局。',
    'Alle Runden löschen':
        '删除所有对局',
    'Alle gespeicherten Runden löschen? Vorher wird eine Kopie in {folder}/ angelegt.':
        '删除所有已保存的对局吗？会先复制一份到 {folder}/。',
    'Es sind keine Runden gespeichert.':
        '没有已保存的对局。',
    'Die Kopie in {folder}/ konnte nicht angelegt werden – die Runden bleiben gespeichert.':
        '无法在 {folder}/ 中创建副本，对局仍保留。',
    'Nicht angewendet – 1 Änderung. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '未应用 – 1 项更改。“应用选择”会采用它；之后请重新启动 DBD。',
    'Nicht angewendet – {n} Änderungen. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '未应用 – {n} 项更改。“应用选择”会采用它们；之后请重新启动 DBD。',
    'Öffnet die markierten Runden bzw. Clips nacheinander im grossen Editor – als eine Montage (mehrere markieren: Strg- oder Umschalt-Klick).':
        '在大编辑器中依次打开标记的对局或片段，合成一个合集（标记多个：Ctrl 或 Shift 点击）。',
    'Ursache: {cause}':
        '原因：{cause}',
    'Keine Region angehakt – für „Auswahl anwenden“ mindestens eine anhaken.':
        '未勾选任何区域，“应用选择”至少需要勾选一个。',
    'Anwenden':
        '应用',
    'Freigeben':
        '解除屏蔽',
    'Importieren':
        '导入',
    'Markieren':
        '标记',
    'Trotzdem beenden':
        '仍然退出',
    'Rundenverlauf gelöscht.':
        '对局记录已删除。',
    'Löscht alle gespeicherten Runden (Datei rounds.jsonl) – nach einer Rückfrage, vorher kommt eine Kopie in den Ordner backup.':
        '删除所有已保存的对局（文件 rounds.jsonl），会先询问；之前会先复制一份到备份文件夹。',
    'Anzeigen:':
        '显示：',
    'Leeren':
        '清空',
    'Log-Datei öffnen':
        '打开日志文件',
    'Sprache und Darstellung':
        '语言和外观',
    'Wirkt nach dem nächsten Start des Programms.':
        '下次启动程序时生效。',
    'Sprache geändert – wirkt nach dem nächsten Start des Programms.':
        '语言已更改，下次启动程序时生效。',
    'Dark Mode':
        '深色模式',
    'Hotkeys':
        '快捷键',
    'Standard':
        '默认值',
    'Zum Ändern anklicken und die neue Tastenkombination drücken.':
        '点击以更改，然后按下新的组合键。',
    'Start und Infobereich':
        '启动和通知区域',
    'Beim Minimieren in den Infobereich':
        '最小化到通知区域',
    'Mit Windows starten':
        '随 Windows 启动',
    'Updates':
        '更新',
    'Beim Start Updates installieren':
        '启动时安装更新',
    'nur über start.bat bzw. die Desktop-Verknüpfung; eigene Änderungen werden nie überschrieben':
        '仅通过 start.bat 或桌面快捷方式；你自己的修改永远不会被覆盖',
    'Eigene Map-Zuordnungen':
        '自己的地图分配',
    'Jetzt nach Updates suchen':
        '立即检查更新',
    'Aktualisieren und neu starten':
        '更新并重启',
    'Suche nach Updates …':
        '正在检查更新…',
    'Beim Start nach Updates suchen':
        '启动时检查更新',
    'Laden und Installieren nur nach deiner Bestätigung; das Setup wird per SHA-256 geprüft':
        '仅在你确认后才下载和安装；安装程序会用 SHA-256 校验',
    'Update-Prüfung fehlgeschlagen: {error}':
        '检查更新失败：{error}',
    'Kein Update – Version {version} (Build {build}) ist aktuell.':
        '没有更新，版本 {version}（构建 {build}）已是最新。',
    'Update verfügbar: {old} → {new} (Build {build}).':
        '有可用更新：{old} → {new}（构建 {build}）。',
    'Lade Update …':
        '正在下载更新…',
    'GitHub antwortet gerade nicht (HTTP {code}) – bitte in einigen Minuten erneut versuchen.':
        'GitHub 暂时没有响应（HTTP {code}），请几分钟后重试。',
    'Keine Antwort von GitHub (Zeitüberschreitung/Verbindung) – bitte später erneut versuchen.':
        'GitHub 没有响应（超时/连接问题），请稍后重试。',
    'GitHub antwortet nicht – neuer Versuch {n} von {total} …':
        'GitHub 没有响应，第 {n}/{total} 次尝试…',
    'Lade Update … {pct} %':
        '正在下载更新… {pct} %',
    'Update nicht geladen: {error}':
        '更新未下载：{error}',
    'Update {version} (Build {build}) geladen und geprüft.':
        '更新 {version}（构建 {build}）已下载并通过校验。',
    'Update installieren':
        '安装更新',
    'Fog Scout {version} (Build {build}) ist geladen und per SHA-256 geprüft. Jetzt installieren? Das Programm schliesst sich und startet danach neu.':
        'Fog Scout {version}（构建 {build}）已下载并通过 SHA-256 校验。现在安装吗？程序将关闭，之后重新启动。',
    'Installieren':
        '安装',
    'Update gesperrt: eine Runde läuft oder ein Clip wird gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '更新被阻止：有对局正在进行或正在保存片段。之后请再次点击“更新并重启”。',
    'Programm schliesst sich und installiert das Update …':
        '程序正在关闭并安装更新…',
    'Das Update wurde nicht gestartet: Die Setup-Datei hat sich seit dem Download verändert oder fehlt. Bitte das Update noch einmal laden.':
        '更新未启动：安装文件在下载后已被更改或丢失。请重新下载更新。',
    'Das Update wurde nicht gestartet: Die Setup-Datei liess sich nicht sicher bereitstellen ({error}). Bitte das Update noch einmal laden.':
        '更新未启动：无法安全地放置安装文件（{error}）。请重新下载更新。',
    'Das Setup konnte nicht gestartet werden (Abfrage nach Administratorrechten abgebrochen?). Erneut versuchen oder das Setup selbst starten:\n{path}':
        '无法启动安装程序（取消了管理员提示？）。请重试或自行启动安装程序：\n{path}',
    'Neustart nicht möglich: {error}':
        '无法重新启动：{error}',
    'Nur unter Windows: bitte das Programm über start.bat neu starten.':
        '仅限 Windows：请通过 start.bat 重新启动程序。',
    'Programm startet neu und installiert das Update …':
        '程序正在重新启动并安装更新…',
    'Fragt GitHub, ob es eine neue Version gibt (nur bei diesem Klick). Installiert wird erst mit „Aktualisieren und neu starten“.':
        '向 GitHub 查询是否有新版本（仅在此次点击时）。只有点击“更新并重启”才会安装。',
    'Beendet das Programm und startet es über start.bat neu – dabei wird das Update installiert. Die installierte Version lädt das Setup, prüft es per SHA-256 und fragt vor dem Installieren.':
        '关闭程序并通过 start.bat 重新启动，由它安装更新。已安装的版本会下载安装程序，用 SHA-256 校验，并在安装前询问。',
    'Fragt nach jedem Start einmal GitHub, ob es ein neues Release gibt. Geladen und installiert wird nur nach deinem Klick und einer Rückfrage.':
        '每次启动后向 GitHub 查询一次是否有新版本。下载和安装只在你点击并确认后进行。',
    'Alle löschen':
        '全部删除',
    'Datenordner öffnen':
        '打开数据文件夹',
    'Karten-Ordner öffnen':
        '打开地图文件夹',
    'liest nur Bildschirmpixel, sendet keine Eingaben ans Spiel.':
        '只读取屏幕像素，不向游戏发送任何输入。',
    'Inoffizielles Fan-Tool, nicht von Behaviour Interactive genehmigt – Nutzung auf eigene Gefahr (siehe LICENSE).':
        '非官方粉丝工具，未经 Behaviour Interactive 认可，使用风险自负（见 LICENSE）。',
    'Kartenbilder: Lethia (hens333.com/callouts, mit Erlaubnis von Hens) · Map-Namen: Luca Fontanot (DBD Map Overlay).':
        '地图图片：Lethia（hens333.com/callouts，经 Hens 许可）· 地图名称：Luca Fontanot（DBD Map Overlay）。',
    'Keine. Unbekannte Map-Namen lassen sich nach dem Match im Hauptfenster zuordnen.':
        '无。未知的地图名称可在对局结束后在主窗口中分配。',
    'Eigene Zuordnungen':
        '自己的分配',
    'Alle eigenen Map-Zuordnungen löschen?':
        '删除所有自己的地图分配吗？',
    'Eigene Map-Zuordnungen gelöscht.':
        '自己的地图分配已删除。',
    'Spielsprachen: {langs}':
        '游戏语言：{langs}',
    'Änderbar, wenn das Programm über die Desktop-Verknüpfung gestartet wurde (verknuepfung_erstellen.bat einmal ausführen).':
        '通过桌面快捷方式启动程序时可以更改（运行一次 verknuepfung_erstellen.bat）。',
    'Wird eingerichtet …':
        '正在设置…',
    'Startet ab jetzt mit Windows im Infobereich.':
        '从现在起随 Windows 启动到通知区域。',
    'Startet nicht mehr mit Windows.':
        '不再随 Windows 启动。',
    'Startet ab jetzt mit Windows im Infobereich (abschaltbar unter Einstellungen → Start und Infobereich).':
        '从现在起随 Windows 启动到通知区域（可在“设置 → 启动和通知区域”中关闭）。',
    'Autostart mit Windows fehlgeschlagen: {error}':
        '无法设置随 Windows 启动：{error}',
    'Fehlgeschlagen: {error}':
        '失败：{error}',
    'Nur unter Windows.':
        '仅限 Windows。',
    'Tipp: Fog Scout über die Verknüpfung im Startmenü starten – dann läuft es ohne Windows-Abfrage mit den nötigen Rechten.':
        '提示：用开始菜单中的快捷方式启动 Fog Scout，这样它会以所需的权限运行，且不会弹出 Windows 提示。',
    'Änderbar, wenn das Programm über die Verknüpfung im Startmenü gestartet wurde.':
        '通过开始菜单中的快捷方式启动程序时可以更改。',
    'Tipp: Einmal als Administrator starten (Rechtsklick auf start.bat → „Als Administrator ausführen“) – dann richtet das Programm die Desktop-Verknüpfung ein, die künftig ohne Windows-Abfrage startet.':
        '提示：以管理员身份启动一次（右键单击 start.bat → “以管理员身份运行”），程序会设置桌面快捷方式，此后用它启动不会弹出 Windows 提示。',
    'Desktop-Verknüpfung eingerichtet/aktualisiert: startet ab jetzt ohne Windows-Abfrage.':
        '桌面快捷方式已设置/更新：从现在起启动时不会弹出 Windows 提示。',
    'Einrichtung der Verknüpfung fehlgeschlagen: {error}':
        '设置快捷方式失败：{error}',
    'Verknüpfung erstellt: {path}':
        '快捷方式已创建：{path}',
    'Aufgabe konnte nicht angelegt werden: {error}':
        '无法创建计划任务：{error}',
    'Verknüpfung konnte nicht angelegt werden: {error}':
        '无法创建快捷方式：{error}',
    '(Autostart nicht erneuert: {error})':
        '（自动启动未更新：{error}）',
    'Symbol im Infobereich nicht verfügbar ({error}) – Minimieren wie gewohnt.':
        '通知区域图标不可用（{error}），最小化照常工作。',
    'Öffnen nur unter Windows: {path}':
        '打开功能仅在 Windows 上可用：{path}',
    'Kann {path} nicht öffnen: {error}':
        '无法打开 {path}：{error}',
    'Fenster öffnen':
        '打开窗口',
    'Beenden':
        '退出',
    'Hotkey: {keys}':
        '快捷键：{keys}',
    'Hotkey {keys} ({action}) nicht verfügbar: {why}.':
        '快捷键 {keys}（{action}）不可用：{why}。',
    '{n} Hotkey(s) nicht verfügbar – siehe Log.':
        '{n} 个快捷键不可用，详见日志。',
    '– aus –':
        '– 关 –',
    'Tasten drücken …':
        '请按键…',
    'Neue Kombination drücken – Esc bricht ab, Entf schaltet den Hotkey aus.':
        '请按下新的组合键：Esc 取消，Delete 关闭此快捷键。',
    '{keys} ist schon „{action}“ – andere wählen.':
        '{keys} 已用于“{action}”，请选择其他组合。',
    'aus':
        '关',
    'an':
        '开',
    'Hotkey {action}: {keys}.':
        '快捷键 {action}：{keys}。',
    'Standard-Hotkeys wiederhergestellt.':
        '已恢复默认快捷键。',
    'Strg':
        'Ctrl',
    'Taste „{key}“ geht nicht als Hotkey':
        '按键“{key}”不能用作快捷键',
    'Bitte mit Strg und/oder Alt kombinieren':
        '请与 Ctrl 和/或 Alt 组合使用',
    'schon von einem anderen Programm belegt':
        '已被其他程序占用',
    'Für „{map}“ gibt es kein Bild.':
        '没有“{map}”的图片。',
    'Bild konnte nicht geladen werden: {path} ({error})':
        '无法加载图片：{path}（{error}）',
    'Map gewählt: {map}':
        '已选择地图：{map}',
    'Noch keine Map gewählt.':
        '尚未选择地图。',
    'Overlay eingeblendet.':
        '悬浮窗已显示。',
    'Overlay ausgeblendet.':
        '悬浮窗已隐藏。',
    '„{map}“ hat nur ein Layout.':
        '“{map}”只有一种布局。',
    'Layout manuell gewechselt':
        '已手动更改布局',
    'Scanne den Bildschirm nach Map- oder Realm-Namen …':
        '正在屏幕上搜索地图或领域名称…',
    'Testanzeige':
        '测试显示',
    'Test: Overlay 10 s lang an seiner normalen Position, mit Systemwerten, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – nochmal drücken beendet den Test.':
        '测试：悬浮窗在正常位置显示 10 秒，包含系统数值、“今日”和音乐（没有数据时使用示例值）。再按一次结束测试。',
    'Links':
        '左',
    'Mittig':
        '居中',
    'Rechts':
        '右',
    'Im Balken':
        '在黑边内',
    'Abstand':
        '间距',
    'Zeile CPU (Temperatur, Last)':
        'CPU 行（温度、负载）',
    'Zeile GPU (Temperatur, Last)':
        'GPU 行（温度、负载）',
    'Zeile Hotspot / GPU-Speicher (HWiNFO)':
        '热点/显存温度行（HWiNFO）',
    'Zeile VRAM':
        'VRAM 行',
    'Zeile RAM':
        'RAM 行',
    'Zeile in den Systemwerten an/aus. Die Warnungen „CPU/GPU DROSSELT“ erscheinen immer.':
        '开启/关闭系统数值的该行。“CPU/GPU 降频”警告始终显示。',
    'Zeile in den Systemwerten an/aus – Hotspot und Memory Junction kommen nur mit HWiNFO.':
        '开启/关闭系统数值的该行。热点和显存结温仅在使用 HWiNFO 时提供。',
    'Zeile in den Systemwerten an/aus.':
        '开启/关闭系统数值的该行。',
    'Test beendet.':
        '测试已结束。',
    'Diagnose in die Zwischenablage kopiert (auch als diagnose.txt gespeichert).':
        '诊断信息已复制到剪贴板（同时保存为 diagnose.txt）。',
    'Alle Elemente mit der Maus ziehen (im Spiel oder in der Vorschau): Karte, Infos, Systemwerte, Heute, Eingaben, Musik. Rechtsklick auf ein Element = Menü (Ausblenden, Position zurücksetzen, Sperren), Strg+Mausrad = Grösse. Danach „Fertig“ oder Hotkey.':
        '用鼠标拖动每个元素（在游戏中或预览中）：地图、信息、系统数值、今日、输入、音乐。右键单击元素 = 菜单（隐藏、重置位置、锁定），Ctrl+鼠标滚轮 = 大小。然后点击“完成”或按快捷键。',
    '{name} wieder an seinem üblichen Platz.':
        '{name} 已回到原位。',
    'Karte':
        '地图',
    'Systemwerte':
        '系统数值',
    'Musik':
        '音乐',
    'Eingaben':
        '输入',
    'Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = Grösse, Rechtsklick = Menü':
        '移动已开启：拖动（自动吸附，Alt = 自由移动），方向键 = 微调，角落/Ctrl+滚轮 = 大小，右键单击 = 菜单',
    'Position zurücksetzen':
        '重置位置',
    'Rückgängig':
        '撤销',
    'Karte darf grösser als der Balken werden':
        '地图可以比黑边更大',
    'Karte füllt den Balken aus':
        '地图填满黑边',
    'Erlaubt jede Kartengrösse: Ist die Karte breiter als der schwarze Balken, bleibt sie an dessen Aussenrand und ragt ins Spielbild. Aus: Die Karte wird nie breiter als der Balken (auf 3440×1440 etwa 31 % der Bildhöhe).':
        '允许任意地图大小：地图比黑边宽时，它停在黑边的外缘并延伸到游戏画面中。关闭：地图永远不会比黑边宽（在 3440×1440 上约为高度的 31 %）。',
    'Die Karte wird so gross, dass sie den schwarzen Balken von links bis rechts ausfüllt (bis auf den Abstand zum Rand); der Grössen-Regler gilt dann nicht. Eine hohe Karte stoppt an der Bildhöhe.':
        '地图放大到从左到右填满黑边（边距除外）；此时大小滑块不再生效。较高的地图在达到画面高度时停止。',
    'Nimmt die letzte Änderung an Position oder Grösse zurück (Karte, Systemwerte, Musik) – auch mit Strg+Z auf dieser Seite. Ein ganzes Ziehen zählt als ein Schritt.':
        '撤销上一次位置或大小的更改（地图、系统数值、音乐），在此页面也可按 Ctrl+Z。一次完整的拖动算作一步。',
    'Merkt Position und Grösse aller Elemente getrennt für jede Grösse des DBD-Fensters (z. B. Vollbild 3440×1440 und ein kleineres Fenster) und lädt sie automatisch, sobald DBD in dieser Grösse läuft.':
        '为每种 DBD 窗口大小分别记住每个元素的位置和大小（例如全屏 3440×1440 和较小的窗口），DBD 以该大小运行时会自动加载。',
    'Nichts rückgängig zu machen.':
        '没有可撤销的操作。',
    'Position/Grösse rückgängig gemacht.':
        '位置/大小已撤销。',
    'Position und Grösse je DBD-Fenstergrösse merken':
        '按 DBD 窗口大小记住位置和大小',
    'DBD-Fenster {size}: Layout für diese Grösse geladen.':
        'DBD 窗口 {size}：已加载此大小的布局。',
    'DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.':
        'DBD 窗口 {size}：新的大小，从现在起会为它记住布局。',
    'Aktuell: Layout für {size} · {n} Grössen gemerkt':
        '当前：{size} 的布局 · 已记住 {n} 种大小',
    'Position zurückgesetzt (automatisch).':
        '位置已重置（自动）。',
    'keine Map':
        '无地图',
    'ausgeblendet':
        '已隐藏',
    'Menü offen':
        '菜单已打开',
    'aktives Fenster ist {window}':
        '活动窗口是 {window}',
    'DBD-Fenster {w}×{h}':
        'DBD 窗口 {w}×{h}',
    'Bildschirm':
        '屏幕',
    'Overlay sichtbar bei {pos} über {src}.':
        '悬浮窗显示在 {src} 上的 {pos}。',
    'Overlay pausiert: {reason}.':
        '悬浮窗已暂停：{reason}。',
    '{text} – Details in fogscout.log':
        '{text}，详见 fogscout.log',
    '{text} ({n}× seit {since}) – Details in fogscout.log':
        '{text}（自 {since} 起 {n} 次），详见 fogscout.log',
    'Erkennung neu gestartet ({n}/{total})':
        '识别已重新启动（{n}/{total}）',
    'Map-Banner gefunden, lese …':
        '已找到地图横幅，正在读取…',
    'automatisch erkannt ({p})':
        '自动识别（{p}）',
    'Layout {n} ({p})':
        '布局 {n}（{p}）',
    'Rundentimer gestartet.':
        '对局计时器已启动。',
    'Rundentimer gestoppt: {time}.':
        '对局计时器已停止：{time}。',
    'Erkannt: {map} – gelesen „{name}“ / „{realm}“':
        '已识别：{map}，读取到“{name}”/“{realm}”',
    'Layout unsicher – falls falsch: Layout-Knopf oder {keys}.':
        '布局不确定，如有错误：使用布局按钮或 {keys}。',
    'Mitten in der Runde „{name}“ / „{realm}“ gelesen (am ehesten {map}) – ignoriert: Map-Banner gibt es nur am Rundenstart, und die Lesung war nicht eindeutig.':
        '在对局中途读取到“{name}”/“{realm}”（最接近：{map}），已忽略：地图横幅只在对局开始时出现，且读取结果不明确。',
    'Banner gesehen, aber keine bekannte Map: „{text}“. Map manuell wählen oder mit „Zuordnen …“ dauerhaft zuordnen.':
        '看到了横幅，但不是已知地图：“{text}”。请手动选择地图，或用“分配…”永久分配。',
    'Runde vorbei ({reason}) – Overlay ausgeblendet.':
        '对局结束（{reason}），悬浮窗已隐藏。',
    'Runde vorbei ({reason}).':
        '对局结束（{reason}）。',
    'Menü offen (Mauszeiger sichtbar) – Overlay pausiert.':
        '菜单已打开（鼠标指针可见），悬浮窗已暂停。',
    'Zurück im Spiel – Overlay wieder sichtbar.':
        '回到游戏中，悬浮窗重新显示。',
    'Die Erkennung ist abgestürzt – Details in fogscout.log':
        '识别功能崩溃，详见 fogscout.log',
    'Die Erkennung ist abgestürzt:':
        '识别功能崩溃：',
    'Die Erkennung ist abgestürzt – bitte Fog Scout neu starten.':
        '识别功能崩溃，请重新启动 Fog Scout。',
    'Nichts gefunden':
        '未找到',
    'Runde gilt jetzt für {map} (vorher {old}).':
        '该对局现在计为 {map}（之前：{old}）。',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen. Bis zum Neustart wird nichts gespeichert.':
        '无法读取 settings.json（{error}），已加载默认值。重新启动前不会保存任何内容。',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen, die alte Datei liegt als settings.json.broken daneben.':
        '无法读取 settings.json（{error}），已加载默认值，旧文件保留为 settings.json.broken。',
    'Scan fehlgeschlagen: {error}':
        '扫描失败：{error}',
    'per Scan gefunden: „{text}“':
        '通过扫描找到：“{text}”',
    'Scan ({s} s): {map}':
        '扫描（{s} 秒）：{map}',
    'Realm „{realm}“ hat nur diese Map':
        '领域“{realm}”只有这一张地图',
    'Scan: Realm „{realm}“ gefunden – bitte Map in der Liste wählen.':
        '扫描：找到领域“{realm}”，请在列表中选择地图。',
    'Scan ({s} s): kein Map- oder Realm-Name auf dem Bildschirm.':
        '扫描（{s} 秒）：屏幕上没有地图或领域名称。',
    'Ergebnisbildschirm':
        '结算界面',
    'Lobby/Menü':
        '大厅/菜单',
    'Ladebildschirm':
        '加载界面',
    'Clip wird geladen …':
        '正在加载片段…',
    'Vorschaubild und Zeitleiste kommen aus der Aufnahme.':
        '预览图和时间轴从录像中读取。',
    '{n} von {total} Bildern':
        '{n}/{total} 张图片',
    'Lädt länger als erwartet – das Fenster ist trotzdem bedienbar.':
        '比预期耗时更长，但窗口仍可使用。',
    'DBD wurde geschlossen':
        'DBD 已关闭',
    'Menü/Lobby (Mauszeiger lange sichtbar)':
        '菜单/大厅（鼠标指针长时间可见）',
    'keine Map angezeigt':
        '未显示地图',
    'Runde vorbei ({reason})':
        '对局结束（{reason}）',
    'wartet, bis du im Match bist (Map manuell gewählt)':
        '等待你进入对局（地图为手动选择）',
    'Menü offen – Overlay pausiert':
        '菜单已打开，悬浮窗已暂停',
    'im Match':
        '对局中',
    'Ausblenden nach der Runde aus':
        '对局后隐藏已关闭',
    'Mauszeiger-Hinweis aus':
        '鼠标指针提示已关闭',
    'Mauszeiger-Hinweis ab dem nächsten Map-Banner':
        '鼠标指针提示从下一个地图横幅起生效',
    'Mauszeiger: –':
        '鼠标指针：–',
    'Mauszeiger sichtbar':
        '鼠标指针可见',
    'Mauszeiger verborgen':
        '鼠标指针隐藏',
    'aus (Einstellung)':
        '关闭（设置）',
    'Runde vorbei – wartet auf die nächste Map':
        '对局结束，正在等待下一张地图',
    'Automatische Erkennung ist aus':
        '自动识别已关闭',
    'DBD ist minimiert':
        'DBD 已最小化',
    'DBD gefunden ({w}×{h}) – warte auf Map-Banner':
        '已找到 DBD（{w}×{h}），正在等待地图横幅',
    'DBD nicht gefunden – Erkennung startet, sobald DBD läuft':
        '未找到 DBD，DBD 运行后开始识别',
    'Bildschirmaufnahme fehlgeschlagen: {error}':
        '屏幕捕获失败：{error}',
    'Aufnahme ist schwarz – DBD im Modus „Fenster-Vollbild“ betreiben':
        '捕获画面为黑色，请以“窗口化全屏”模式运行 DBD',
    'Fensteraufnahme nicht möglich, nutze Bildschirmaufnahme ({error})':
        '无法进行窗口捕获，改用屏幕捕获（{error}）',
    'DBD im Hintergrund – Fensteraufnahme aktiv: die Map wird auch erkannt, wenn andere Fenster darüber liegen.':
        'DBD 在后台，窗口捕获已启用：即使其他窗口遮挡也能识别地图。',
    'Rundenende-Erkennung für die gewählte Map ist jetzt aktiv.':
        '所选地图的对局结束检测现已启用。',
    'Mauszeiger war beim Map-Banner sichtbar – Menü-Erkennung per Mauszeiger ist für diese Runde aus.':
        '地图横幅出现时鼠标指针可见，本局通过鼠标指针检测菜单的功能已关闭。',
    'Map zuordnen':
        '分配地图',
    'Gelesen: „{text}“':
        '读取到：“{text}”',
    'Welche Map war das? Der Name wird künftig automatisch erkannt.':
        '这是哪张地图？从现在起将自动识别该名称。',
    'Bitte eine Map auswählen.':
        '请选择一张地图。',
    'Abbrechen':
        '取消',
    '„{text}“ wird jetzt als {map} erkannt (eigene Zuordnung).':
        '“{text}”现在被识别为 {map}（自己的分配）。',
    'zugeordnet: „{text}“':
        '已分配：“{text}”',
    'Der gelesene Text ist zu kurz.':
        '读取到的文字太短。',
    'Unbekannte Map.':
        '未知地图。',
    '„{text}“ ist schon der Name von {map}.':
        '“{text}”已经是 {map} 的名称。',
    'Kartenbild hinzufügen':
        '添加地图图片',
    'eigenes Bild':
        '自己的图片',
    'Kartenbild gespeichert: {path}':
        '地图图片已保存：{path}',
    'Eigenes Kartenbild für {map} gespeichert: {path}':
        '{map} 的自己的地图图片已保存：{path}',
    'wird ab jetzt automatisch erkannt.':
        '从现在起会被自动识别。',
    'Eigenes Kartenbild für {map} gelöscht – das mitgelieferte gilt wieder.':
        '{map} 的自己的地图图片已删除，重新使用自带图片。',
    'Bitte den Namen der Map eingeben.':
        '请输入地图名称。',
    '„{name}“ gibt es schon ({map}) – dann „Bild einer vorhandenen Map ersetzen“ wählen.':
        '“{name}”已存在（{map}），请改选“替换现有地图的图片”。',
    'Noch kein Bild gewählt (PNG, JPG, WebP, GIF)':
        '尚未选择图片（PNG、JPG、WebP、GIF）',
    'Für welche Map?':
        '用于哪张地图？',
    'Ergebnis':
        '结果',
    'Eigenes Bild löschen':
        '删除自己的图片',
    'Speichern':
        '保存',
    'Bilder':
        '图片',
    'Kartenbild wählen':
        '选择地图图片',
    'Für diese Map lässt sich kein Bild speichern.':
        '无法为此地图保存图片。',
    'Erst ein Bild wählen.':
        '请先选择一张图片。',
    'Das ist kein lesbares Bild: {error}':
        '这不是可读取的图片：{error}',
    'Bild konnte nicht verarbeitet werden: {error}':
        '无法处理图片：{error}',
    'Speichern fehlgeschlagen: {error}':
        '保存失败：{error}',
    'Eigenes Bild für „{map}“ löschen?':
        '删除你为“{map}”设置的图片吗？',
    'Löschen fehlgeschlagen: {error}':
        '删除失败：{error}',
    'Bild wählen …':
        '选择图片…',
    'Bild einer vorhandenen Map ersetzen':
        '替换现有地图的图片',
    'Neue Map (fehlt im Programm)':
        '新地图（程序中缺少）',
    'Name':
        '名称',
    'Name so, wie er im Map-Banner steht – dann wird die Map automatisch erkannt.':
        '名称与地图横幅中显示的一致，这样地图就能被自动识别。',
    'Hintergrund entfernen (Dunkelblau und Graulila der Community-Karten) und Rand abschneiden':
        '去除背景（社区地图的深蓝色和灰紫色）并裁掉边框',
    'Ordner öffnen':
        '打开文件夹',
    'Animiertes GIF: wird unverändert übernommen.':
        'GIF 动图：原样使用。',
    'Wird gestartet …':
        '正在启动…',
    'Version {version}':
        '版本 {version}',
    'Lade Maps …':
        '正在加载地图…',
    'Bereite Overlay vor …':
        '正在准备悬浮窗…',
    'Baue Oberfläche …':
        '正在构建界面…',
    'Starte Erkennung …':
        '正在启动识别…',
    'Öffne Fenster …':
        '正在打开窗口…',
    'Fog Scout ist bereit.':
        'Fog Scout 已就绪。',
    'Automatische Erkennung':
        '自动识别',
    'Aufnahmen mit OBS':
        '用 OBS 录像',
    'Lobby-Meldung':
        '大厅通知',
    'Spielserver anzeigen':
        '显示游戏服务器',
    'Systemwerte im Spiel':
        '游戏内系统数值',
    '„Heute“ im Spiel':
        '游戏内“今日”',
    'Musik im Spiel':
        '游戏内音乐',
    'Discord-Status':
        'Discord 状态',
    'Spotify „Als nächstes“':
        'Spotify“接下来播放”',
    'YouTube-Upload':
        'YouTube 上传',
    '{name} eingeschaltet.':
        '{name} 已开启。',
    '{name} ausgeschaltet.':
        '{name} 已关闭。',
    'Erkennt die Map beim Match-Start am Banner und blendet die Karte ein. Aus: nur noch von Hand (Scannen, Map wählen). Dasselbe Häkchen steht unter Einstellungen → Erkennung.':
        '对局开始时从横幅读取地图并显示地图。关闭：仅手动（扫描、选择地图）。“设置 → 识别”中有同一个复选框。',
    'OBS nimmt jede Runde auf: Start beim Map-Banner, Stopp beim Rundenende. Aus: keine neue Aufnahme und keine F8-Clips – eine laufende Aufnahme endet normal mit der Runde. Alles Weitere unter Einstellungen → Aufnahmen.':
        'OBS 录制每一局：在地图横幅时开始，对局结束时停止。关闭：不开始新录像，也没有 F8 片段；正在进行的录像照常随对局结束。其他所有设置在“设置 → 录像”中。',
    'Ton und Hinweisfenster, sobald DBD eine Lobby gefunden hat. Die Erinnerung beim Countdown und „nur wenn DBD nicht vorne ist“ bleiben unter Einstellungen → Erkennung → Benachrichtigungen.':
        'DBD 一找到大厅就播放声音并显示通知窗口。倒计时提醒和“仅当 DBD 不在前台时”仍在“设置 → 识别 → 通知”中。',
    'Zeigt Region und Ping des verbundenen Spielservers – auf der Seite Server, im Overlay und in der Statistik. Einschalten fragt Windows einmal nach Administratorrechten; gelesen werden nur Paketköpfe, nie Inhalte.':
        '显示所连接游戏服务器的区域和延迟，显示在“服务器”页面、悬浮窗和统计中。开启时会向 Windows 请求一次管理员权限；只读取数据包头，从不读取内容。',
    'Die Karte mit CPU-/GPU-Temperatur, Last und Speicher im schwarzen Balken. Einschalten bringt sie an die Position, an der sie zuletzt stand; Position und Zeilen unter Overlay → Systemwerte.':
        '黑边中显示 CPU/GPU 温度、负载和内存的卡片。开启后它会回到上次所在的位置；位置和行在“悬浮窗 → 系统数值”中设置。',
    'Die Karte „Heute“ im Spiel: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit. Position unter Overlay → Heute.':
        '游戏内的“今日”卡片：对局数、游戏时长、平均击杀/逃脱、时钟。位置在“悬浮窗 → 今日”中设置。',
    'Die Musikkarte „Läuft gerade“ im Spiel (Titel, Interpret, Cover aus der Windows-Mediensteuerung). Position und Aussehen unter Overlay → Musik.':
        '游戏内的“正在播放”音乐卡片（标题、艺术家、来自 Windows 媒体控件的封面）。位置和外观在“悬浮窗 → 音乐”中设置。',
    'Rich Presence: Map, Rolle und Rundenzeit in deinem Discord-Status. Application-ID und Einzelheiten unter Einstellungen → Verbindungen → Discord.':
        'Rich Presence：在你的 Discord 状态中显示地图、角色和对局时间。应用程序 ID 和详细设置在“设置 → 连接 → Discord”中。',
    'Die Liste „Als nächstes“ aus Spotify in der Musikkarte. Client-ID und Anmeldung unter Einstellungen → Verbindungen → Spotify.':
        '在音乐卡片上显示 Spotify 的“接下来播放”列表。客户端 ID 和登录在“设置 → 连接 → Spotify”中。',
    'Neue Clips (F8, Editor) gehen von selbst auf YouTube. Aus: nichts Neues wird eingereiht – was schon in der Warteschlange steht, lädt fertig; Runden lädst du weiter per Rechtsklick hoch. Einstellungen → Verbindungen → YouTube.':
        '新片段（F8、编辑器）会自动上传到 YouTube。关闭：不再加入新的上传队列，队列中已有的会完成；对局仍可通过右键上传。“设置 → 连接 → YouTube”。',
    'Werkzeuge für die Fehlersuche ein- oder ausklappen: Live-Zustand der Rundenende-Erkennung, Debug-Bilder, Bildschirm scannen.':
        '显示或隐藏故障排除工具：对局结束检测的实时状态、调试图片、扫描屏幕。',
    'Klicken und die neue Tastenkombination drücken: Strg/Alt + Taste, oder eine Taste allein (F1–F12, Numpad, Pause, Rollen, Einfg, Pos1, Ende, Bild↑/↓ – die gilt nur, solange DBD vorne ist). Esc bricht ab, Entf schaltet den Hotkey aus.':
        '点击后按下新的组合键：Ctrl/Alt + 按键，或单个按键（F1–F12、小键盘、Pause、Scroll Lock、Insert、Home、End、Page Up/Down，仅在 DBD 处于前台时有效）。Esc 取消，Delete 关闭此快捷键。',
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
        '仅在 DBD 处于前台时有效，DBD 本身不再收到 {keys}（DBD 中未绑定？）。',
    'Map-Namen in dieser Spielsprache erkennen. Nur die Sprachen anhaken, in denen du spielst – weniger Sprachen, weniger Verwechslungen.':
        '识别此游戏语言中的地图名称。只勾选你使用的游戏语言，语言越少，混淆越少。',
    'Meldungen der Art „{category}“ im Log anzeigen.':
        '在日志中显示“{category}”消息。',
    'Karte ausblenden (die automatische Erkennung läuft weiter).':
        '隐藏地图（自动识别继续运行）。',
    'Karte wieder einblenden.':
        '重新显示地图。',
    'Die Erkennung war beim Layout nicht sicher – stimmt es nicht, hier weiterschalten.':
        '识别对布局不确定，如有错误，请在此切换。',
    'Wechselt zum nächsten Layout dieser Map (z. B. Coal Tower ↔ Coal Tower II). Die Layouts ab II gibt es seit Patch 8.6.0 nur noch in Custom Games.':
        '切换到此地图的下一种布局（例如 Coal Tower ↔ Coal Tower II）。自 8.6.0 补丁起，II 及之后的布局只在自定义对局中出现。',
    'Test sofort beenden.':
        '立即结束测试。',
    'Zeigt 10 s lang alles, was das Overlay im Match zeigt – Karte, Systemwerte, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – an den eingestellten Stellen, auch ohne DBD. Nochmal drücken beendet den Test.':
        '在 10 秒内显示悬浮窗在对局中会显示的所有内容：地图、系统数值、“今日”和音乐（没有数据时使用示例值），各在其位置上，没有 DBD 也可以。再按一次结束测试。',
    'Verschieben beenden.':
        '停止移动。',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen – falls die automatische Erkennung das Banner verpasst hat.':
        '立即在整个屏幕上搜索地图或领域名称，以防自动识别漏掉了横幅。',
    'Eigenes Kartenbild für diese unbekannte Map anlegen – Name und Realm sind schon eingetragen, der Hintergrund wird automatisch entfernt.':
        '为这张未知地图创建你自己的地图图片：名称和领域已填好，背景会自动去除。',
    'Der gelesene Name gehört zu einer vorhandenen Map (z. B. anders geschrieben)? Einmal zuordnen – danach wird er automatisch erkannt.':
        '读取到的名称属于现有地图（例如拼写不同）？分配一次即可，之后会自动识别。',
    'Hinweis ausblenden.':
        '隐藏此提示。',
    'Eigenes Bild für eine Map wählen: vorhandenes Bild ersetzen oder neue Map anlegen. Rand und Hintergrund werden automatisch entfernt.':
        '为地图选择你自己的图片：替换现有图片或创建新地图。边框和背景会自动去除。',
    'Position wieder auf „automatisch“ stellen (auf Ultrawide im linken schwarzen Rand).':
        '将位置恢复为“自动”（在超宽屏上位于左侧黑边内）。',
    'Auf breiten Monitoren bleibt die Karte im schwarzen Balken, in dem sie liegt, und wird bei Bedarf verkleinert. Mitten über dem Spiel platziert gilt keine Begrenzung. Ohne schwarze Balken neben dem Spielbild (16:9, z. B. 1920×1080) sind die Balken-Optionen ausgegraut.':
        '在宽屏显示器上，地图保持在它所在的黑边内，必要时会缩小。放在游戏画面中间时没有限制。游戏画面两侧没有黑边时（16:9，例如 1920×1080），黑边选项显示为灰色。',
    'Karte ausblenden, solange ein anderes Fenster (Browser, Discord …) im Vordergrund ist.':
        '当其他窗口（浏览器、Discord…）位于前台时隐藏地图。',
    'Zusätzliche Namenszeile über der Karte – die meisten Kartenbilder tragen den Namen schon selbst.':
        '在地图上方额外显示一行名称，大多数地图图片本身已显示名称。',
    'Zeit seit dem Einblenden der Karte, gross unter der Karte.':
        '地图出现以来的时间，以大字显示在地图下方。',
    'Region und Ping des Spielservers unter der Karte. Braucht „Verbundener Spielserver“ im Tab Server.':
        '在地图下方显示游戏服务器的区域和延迟。需要在“服务器”选项卡中开启“已连接的游戏服务器”。',
    'Aus: Karte liegt auf einem dunklen Rechteck – besser lesbar über hellen Spielszenen.':
        '关闭：地图放在深色矩形上，在明亮的游戏场景上更易阅读。',
    'Liest das Map-Banner am Match-Anfang und blendet die passende Karte ein. Aus: Map nur von Hand wählen.':
        '对局开始时读取地图横幅并显示对应的地图。关闭：仅手动选择地图。',
    'Blendet die Karte nach der Runde aus (Ergebnisbildschirm, Lobby, Ladebildschirm, DBD beendet).':
        '对局后隐藏地图（结算界面、大厅、加载界面、DBD 关闭）。',
    'Karte verschwindet, solange der Mauszeiger im Spiel sichtbar ist (ESC-Menü), und kommt danach wieder.':
        '游戏中鼠标指针可见时（ESC 菜单）地图消失，之后再出现。',
    'Fensteraufnahme wie bei OBS: erkennt das Banner auch, wenn DBD verdeckt ist. Nur solange DBD im Hintergrund ist.':
        '像 OBS 一样进行窗口捕获：即使 DBD 被遮挡也能识别横幅。仅在 DBD 处于后台时。',
    'Speichert gelesene Banner und verkleinerte Bilder der Runde im Ordner debug/ – nur zur Fehlersuche, kostet Speicherplatz.':
        '将读取的横幅和对局的小图保存到 debug/ 文件夹，仅用于故障排除，会占用磁盘空间。',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen.':
        '立即在整个屏幕上搜索地图或领域名称。',
    'Kopiert technische Infos (Fenster, Overlay, letzte Rundenende-Prüfungen) in die Zwischenablage – zum Weitergeben bei Problemen.':
        '将技术信息（窗口、悬浮窗、最近的对局结束检查）复制到剪贴板，出现问题时可提供给他人。',
    'Misst den Ping zu allen AWS-Regionen (UDP-Beacon von Amazon GameLift).':
        '测量到所有 AWS 区域的延迟（Amazon GameLift 的 UDP 信标）。',
    'Nur die angehakten Regionen erlauben – trägt die übrigen in die Windows-hosts-Datei ein (fragt nach Administratorrechten).':
        '仅允许勾选的区域，将其他区域添加到 Windows hosts 文件（会请求管理员权限）。',
    'Entfernt die Einträge des Programms aus der hosts-Datei – alle Regionen wieder erlaubt.':
        '从 hosts 文件中移除本程序的条目，重新允许所有区域。',
    'Log-Anzeige leeren (die Log-Datei bleibt).':
        '清空日志视图（日志文件保留）。',
    'Öffnet fogscout.log mit allen Details.':
        '打开包含所有详细信息的 fogscout.log。',
    'Dunkle oder helle Darstellung des Steuerfensters.':
        '控制窗口的深色或浅色外观。',
    'Alle Hotkeys auf die Voreinstellung zurücksetzen.':
        '将所有快捷键重置为默认值。',
    'Minimieren versteckt das Fenster im Infobereich; Doppelklick auf das Symbol holt es zurück.':
        '最小化时将窗口隐藏到通知区域；双击图标可恢复。',
    'Startet das Programm bei der Anmeldung im Infobereich. Nur als Administrator änderbar.':
        '登录时在通知区域启动程序。只能以管理员身份更改。',
    'Holt beim Start über die Verknüpfung den neuen Stand von GitHub. Eigene Änderungen werden nie überschrieben.':
        '通过快捷方式启动时从 GitHub 获取最新版本。你自己的修改永远不会被覆盖。',
    'Alle eigenen Map-Zuordnungen löschen (die Namen werden dann wieder als unbekannt gemeldet).':
        '删除所有自己的地图分配（这些名称将重新被报告为未知）。',
    'Öffnet den Ordner mit den mitgelieferten Kartenbildern.':
        '打开包含自带地图图片的文件夹。',
    'PNG, JPG, WebP oder GIF auswählen – zum Beispiel ein Original mit Hintergrund.':
        '选择 PNG、JPG、WebP 或 GIF，例如带背景的原图。',
    'Dein Bild ersetzt das mitgelieferte Bild dieser Map (bzw. dieses Layouts). Löschen stellt das Original wieder her.':
        '你的图片将替换这张地图（或这种布局）的自带图片。删除后恢复原图。',
    'Legt eine neue Map an. Sie wird erkannt, wenn der Name so geschrieben ist wie im Map-Banner.':
        '创建一张新地图。如果名称与地图横幅中的写法一致，它就会被识别。',
    'Öffnet den Ordner user_maps mit deinen eigenen Kartenbildern.':
        '打开包含你自己地图图片的 user_maps 文件夹。',
    'Löscht dein Bild für die gewählte Map – danach gilt wieder das mitgelieferte.':
        '删除你为所选地图设置的图片，重新使用自带图片。',
    'Bild umwandeln und speichern; die Karte wird sofort angezeigt.':
        '转换并保存图片；地图会立即显示。',
    'Schliessen, ohne etwas zu ändern.':
        '关闭且不做任何更改。',
    'Macht Dunkelblau (#282a42) und Graulila (#535781) der Community-Karten transparent, schneidet den gleichfarbigen Rand ab und bringt das Bild auf 1280 px Höhe.':
        '将社区地图的深蓝色（#282a42）和灰紫色（#535781）设为透明，裁掉同色边框，并将图片缩放到 1280 像素高。',
    '? unsicher – {keys} = falsch':
        '? 不确定 – {keys} = 错误',
    'Falsch erkannt':
        '地图错误',
    'Stimmt':
        '正确',
    'Unsicher erkannt: {map} (gelesen „{name}“)':
        '识别不确定：{map}（读取到“{name}”）',
    'Unsicher erkannt: {map} – gelesen „{name}“, Passung {fit}. Falls falsch: {keys} oder „Falsch erkannt“.':
        '识别不确定：{map}，读取到“{name}”，匹配度 {fit}。如有错误：{keys} 或“地图错误”。',
    '{map} bestätigt.':
        '{map} 已确认。',
    'Nichts zu verwerfen: keine automatisch erkannte Map eingeblendet.':
        '没有可丢弃的内容：当前没有显示自动识别的地图。',
    'Verworfen: {map} – die Runde wird nicht gezählt.':
        '已丢弃：{map}，该对局不计入。',
    'Die erkannte Map stimmt nicht: Karte ausblenden, Timer zurücksetzen, die Runde wird nicht gezählt. Geht auch im Spiel mit dem Hotkey (Standard Strg+Alt+X).':
        '识别的地图错误：隐藏地图，重置计时器，该对局不计入。在游戏中也可用快捷键操作（默认 Ctrl+Alt+X）。',
    'Die Map stimmt – Hinweis „unsicher“ ausblenden.':
        '地图正确，隐藏“不确定”提示。',
    'als falsch verworfen':
        '作为错误识别已丢弃',
    'Ping {ms} ms':
        '延迟 {ms} 毫秒',
    'Ø Kills':
        '平均击杀',
    '4K':
        '4 杀',
    'Entkommen':
        '逃脱',
    'entkommen':
        '逃脱',
    'tot':
        '死亡',
    'aufgegeben':
        '放弃',
    'verlassen':
        '离开',
    'Stats-Seite öffnen, wenn DBD beendet wird':
        '关闭 DBD 时打开统计页面',
    'Userscript kopieren':
        '复制用户脚本',
    'Stats-Seite öffnen':
        '打开统计页面',
    '⚠ Unbekannter Status auf der Stats-Seite: {list} – zählt nicht. Bitte melden („Diagnose kopieren“).':
        '⚠ 统计页面上有未知状态：{list}，未计入。请报告（“复制诊断信息”）。',
    '⚠ Lücke: zwischen {start} und {end} fehlen vielleicht Matches – die Seite zeigt nur die letzten 30. Seite öfter öffnen.':
        '⚠ 存在缺口：{start} 到 {end} 之间的比赛可能缺失，该页面只显示最近 30 场。请更频繁地打开该页面。',
    '⚠ {n}× andere Map als erkannt, zuletzt {when}: erkannt {ours}, laut Seite {theirs}.':
        '⚠ {n} 次与识别结果不同的地图，最近一次 {when}：识别为 {ours}，页面显示 {theirs}。',
    '⚠ Das Userscript ist veraltet (Version {old}, aktuell {new}) – „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '⚠ 用户脚本已过时（版本 {old}，当前 {new}），请点击“复制用户脚本”并在 Tampermonkey 中替换。',
    'Stats-Seite konnte nicht geöffnet werden: {error}':
        '无法打开统计页面：{error}',
    'DBD beendet – Stats-Seite geöffnet; das Userscript speichert die Matches.':
        'DBD 已关闭，统计页面已打开；用户脚本会保存比赛数据。',
    'Userscript nicht gefunden: {error}':
        '未找到用户脚本：{error}',
    'Userscript in die Zwischenablage kopiert. In Tampermonkey: „Neues Skript erstellen“ → alles ersetzen (Strg+A, Strg+V) → Speichern. Danach stats.deadbydaylight.com öffnen und anmelden.':
        '用户脚本已复制到剪贴板。在 Tampermonkey 中：“添加新脚本” → 替换全部内容（Ctrl+A、Ctrl+V） → 保存。然后打开 stats.deadbydaylight.com 并登录。',
    'Offizielle Match-Daten: {n} Matches gelesen, {new} neu – Datei gelöscht.':
        '官方比赛数据：读取了 {n} 场比赛，{new} 场新比赛，文件已删除。',
    'Offizielle Match-Daten: zwischen {start} und {end} fehlen vielleicht Matches (die Seite zeigt nur die letzten 30).':
        '官方比赛数据：{start} 到 {end} 之间的比赛可能缺失（该页面只显示最近 30 场）。',
    '{name} gelesen, aber nicht gelöscht: {error}':
        '已读取 {name}，但未删除：{error}',
    '{name} ist keine Match-Datei von Fog Scout – bleibt liegen.':
        '{name} 不是 Fog Scout 比赛文件，未做处理。',
    'Unbekannter Status auf der Stats-Seite: „{status}“ – zählt nicht für Kills/Escapes. Bitte melden.':
        '统计页面上有未知状态：“{status}”，未计入击杀/逃脱。请报告。',
    'Schliesst du DBD nach mindestens einer Runde, öffnet das Programm stats.deadbydaylight.com im Browser. Das Userscript speichert dann die letzten 30 Matches, das Programm liest sie ein und löscht die Datei. Nie während DBD läuft.':
        '当你在至少一局后关闭 DBD 时，程序会在浏览器中打开 stats.deadbydaylight.com。用户脚本随后会保存最近 30 场比赛；程序读取后删除该文件。DBD 运行期间绝不会这样做。',
    'Kopiert das Userscript in die Zwischenablage. In Tampermonkey „Neues Skript erstellen“, alles ersetzen und speichern. Es liest nur die Match-Liste, die die Seite selbst lädt – keine Konto- oder Login-Daten – und schickt nichts irgendwohin.':
        '将用户脚本复制到剪贴板。在 Tampermonkey 中“添加新脚本”，替换全部内容并保存。它只读取页面自己加载的比赛列表，不读取账号或登录数据，也不向任何地方发送内容。',
    'Öffnet stats.deadbydaylight.com jetzt. Mit installiertem Userscript kommen die Matches gleich danach an.':
        '立即打开 stats.deadbydaylight.com。已安装用户脚本时，比赛数据随后就会到达。',
    'Vom Programm erkannt: {seen} von {n} ({share})':
        '程序识别到：{n} 场中的 {seen} 场（{share}）',
    'Nicht erkannt (oder das Programm lief nicht): {list}':
        '未识别到（或程序未运行）：{list}',
    'Rundenende erkannt: Median {off} gegenüber dem Ende laut Seite ({n} Runden; + = später)':
        '检测到的对局结束：与页面上的结束时间相比，中位数 {off}（{n} 局；+ = 较晚）',
    '{n} Mio.':
        '{n}M',
    'Ø BP':
        '平均血点',
    '✓ {n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '✓ {n} 次未检测到对局结束，但已按统计页面上的时长计入。',
    'Runden vom Map-Banner bis zum Rundenende (ab 1 min), nur lokal gespeichert. Kills, Escapes und Bloodpoints laut stats.deadbydaylight.com, sobald eine Runde dort zugeordnet ist.':
        '从地图横幅到对局结束的对局（1 分钟起），仅保存在本地。一旦对局与 stats.deadbydaylight.com 上的比赛关联，就会显示其中的击杀、逃脱和血点。',
    '{n}× Abandon':
        '{n} 次放弃',
    'Ein Skin oder neuer Killer steht unter seinem eigenen Namen? Zeile markieren, Killer wählen, „Zuordnen“ – gilt auch rückwirkend.':
        '某个服装或新杀手以其自身名称显示？选中该行，选择杀手，点击“分配”，过去的对局也会适用。',
    'Abgleich mit der Stats-Seite':
        '与统计页面核对',
    'Noch keine offiziellen Daten.':
        '尚无官方数据。',
    'Neu seit {version}':
        '{version} 以来的新内容',
    'sofort':
        '即时',
    'HWiNFO läuft nicht: CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen.':
        'HWiNFO 未运行：缺少 CPU 温度、CPU 功耗、核心和 FPS。',
    'Systemwerte: HWiNFO läuft nicht – CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen in dieser Runde.':
        '系统数值：HWiNFO 未运行，本局缺少 CPU 温度、CPU 功耗、核心和 FPS。',
    'Vorwoche {value}':
        '上周 {value}',
    '{n} Pkt.':
        '{n} 分',
    'Montag bis jetzt gegenüber der Vorwoche (Mo–So); Custom und Farming zählen nicht.':
        '本周一至今与上周（周一至周日）对比；自定义对局和刷分不计入。',
    'Sicherung: {files} nach {folder}/ kopiert (die letzten {n} Stände bleiben).':
        '备份：{files} 已复制到 {folder}/（保留最近 {n} 份副本）。',
    '{n} Dateien, zuletzt {day}':
        '{n} 个文件，最新 {day}',
    '1 Datei, zuletzt {day}':
        '1 个文件，最新 {day}',
    'behalten (nie aufgeräumt)':
        '已保留（从不清理）',
    'wartet auf den YouTube-Upload':
        '等待上传到 YouTube',
    'auf YouTube':
        '已上传到 YouTube',
    'Karte im Spiel':
        '游戏中的地图',
    'OBS läuft nicht, oder sein WebSocket-Server ist aus':
        'OBS 未运行，或其 WebSocket 服务器已关闭',
    'OBS antwortet nicht':
        'OBS 没有响应',
    'OBS hat die Verbindung getrennt':
        'OBS 关闭了连接',
    'noch keine':
        '暂无',
    'Tägliche Kopie von rounds.jsonl und official.jsonl nach {folder}/ (nur bei Änderungen, die letzten {n} Stände je Datei; vor „Alle Runden löschen“ eine zusätzliche): {state}':
        '每天将 rounds.jsonl 和 official.jsonl 复制到 {folder}/（仅在有更改时，每个文件保留最近 {n} 份副本；“删除所有对局”前会再复制一份）：{state}',
    'Verstanden':
        '知道了',
    'Aus HISTORY.md (Deutsch), die neuesten zuerst.':
        '来自 HISTORY.md（德语），最新的在前。',
    'Blendet die Karte „Neu seit …“ aus, bis die nächste neue Version kommt.':
        '隐藏“…以来的新内容”卡片，直到下一个新版本发布。',
    'Offizielle Match-Daten':
        '官方比赛数据',
    'Einmal einrichten: Tampermonkey im Browser installieren, „Userscript kopieren“ und dort als neues Skript einfügen und speichern, auf stats.deadbydaylight.com anmelden. Chrome/Edge: in den Details der Erweiterung „Allow User Scripts“ einschalten, sonst läuft kein Skript. Beim Öffnen der Seite speichert das Skript neue Matches (die letzten 30) im Download-Ordner; das Programm liest die Datei und löscht sie. Es geht dafür selbst nicht ins Internet.':
        '一次性设置：在浏览器中安装 Tampermonkey，点击“复制用户脚本”，将其粘贴为新脚本并保存，然后登录 stats.deadbydaylight.com。Chrome/Edge：在扩展程序的详细信息中开启“允许用户脚本”，否则任何脚本都不会运行。页面打开时，脚本会将新比赛（最近 30 场）保存到下载文件夹；程序读取该文件后将其删除。程序自身不会为此联网。',
    'Alle Matches neu speichern':
        '重新保存所有比赛',
    'Öffnet die Stats-Seite so, dass das Userscript ihre letzten 30 Matches noch einmal speichert, auch wenn keines neu ist – nach einer Neuinstallation oder wenn die Datei verloren ging.':
        '打开统计页面，让用户脚本再次保存最近 30 场比赛，即使没有新比赛，适用于重新安装后或文件丢失时。',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) speichert ihre letzten 30 Matches noch einmal, auch wenn keines neu ist; das Programm übernimmt sie gleich – bekannte zählen nur einmal. Kommt keine Datei: in der Console des Browsers (F12) steht, ob das Skript läuft. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '统计页面将在浏览器中打开。用户脚本（版本 {n} 或更新）会再次保存最近 30 场比赛，即使没有新比赛；程序会立即读取，已知的比赛只计一次。如果没有生成文件：浏览器的控制台（F12）会显示脚本是否在运行。较旧的用户脚本：请先点击“复制用户脚本”并在 Tampermonkey 中替换。',
    'Verlauf':
        '趋势',
    'Nur Runden, die einem Match auf der Stats-Seite zugeordnet sind. Die Maus über einer Säule zeigt Wert und Anzahl der Runden.':
        '仅包含与统计页面上的比赛关联的对局。将鼠标悬停在柱上可查看其数值和对局数。',
    'Killer – Ø Kills {per}':
        '杀手 – 平均击杀{per}',
    'Survivor – entkommen {per}':
        '幸存者 – 逃脱{per}',
    'pro Stunde':
        '（每小时）',
    'pro Tag':
        '（每天）',
    'pro Woche':
        '（每周）',
    'KW {n}':
        '第 {n} 周',
    '{when}: Ø {kills} Kills · {n} Runden':
        '{when}：平均 {kills} 击杀 · {n} 局',
    '{when}: {share} entkommen · {n} Runden':
        '{when}：{share} 逃脱 · {n} 局',
    'Keine Killer-Runden mit offiziellen Daten in dieser Auswahl.':
        '此筛选范围内没有带官方数据的杀手对局。',
    'Keine Survivor-Runden mit offiziellen Daten in dieser Auswahl.':
        '此筛选范围内没有带官方数据的幸存者对局。',
    'Ø {kills} Kills':
        '平均 {kills} 击杀',
    '{share} entkommen':
        '{share} 逃脱',
    'Meldung, wenn Match-Daten eingelesen und gelöscht wurden':
        '读取并删除比赛数据后通知',
    'Zeigt unten rechts kurz, wie viele Matches gelesen wurden und dass die Datei gelöscht ist – nicht, solange DBD im Vordergrund ist. Im Log steht es immer.':
        '在右下角短暂显示读取了多少场比赛以及文件已删除，DBD 在前台时不显示。日志中始终有记录。',
    '{n} Matches gelesen, davon {new} neu. Die Datei wurde gelöscht.':
        '读取了 {n} 场比赛，其中 {new} 场是新的。文件已删除。',
    '{name} wurde gelesen, konnte aber nicht gelöscht werden – Details im Log.':
        '已读取 {name}，但无法删除，详见日志。',
    'Links oben (über der Karte)':
        '左上（地图上方）',
    'Rechts oben':
        '右上',
    'GPU: {name}':
        'GPU：{name}',
    'GPU: keine NVIDIA-Karte gefunden':
        'GPU：未找到 NVIDIA 显卡',
    'CPU-Temperatur: aus HWiNFO':
        'CPU 温度：来自 HWiNFO',
    'Systemwerte (CPU/GPU-Temperatur, Auslastung, VRAM, RAM)':
        '系统数值（CPU/GPU 温度、负载、VRAM、RAM）',
    'nach Map':
        '按地图',
    'nach Killer':
        '按杀手',
    'GPU Ø °C':
        'GPU 平均 °C',
    'GPU max':
        'GPU 最高',
    'CPU Ø °C':
        'CPU 平均 °C',
    'CPU max':
        'CPU 最高',
    'GPU Ø Last':
        'GPU 平均负载',
    'Ø Watt':
        '平均瓦数',
    'Noch keine Systemwerte in dieser Auswahl (Tab Overlay → Systemwerte einschalten).':
        '此筛选范围内尚无系统数值（“悬浮窗”选项卡 → 开启系统数值）。',
    'GPU DROSSELT (TEMP.)':
        'GPU 降频（温度）',
    'GPU DROSSELT (HW)':
        'GPU 降频（硬件）',
    'Hotspot max {v} °C':
        '热点最高 {v} °C',
    'Hotspot max':
        '热点最高',
    'GPU-Temperatur – Ø {per}':
        'GPU 温度 – 平均{per}',
    'Noch keine GPU-Temperaturen in dieser Auswahl.':
        '此筛选范围内尚无 GPU 温度。',
    '{when}: Ø {avg} °C · max {max} °C · {n} Runden':
        '{when}：平均 {avg} °C · 最高 {max} °C · {n} 局',
    'Werte der Systemwerte-Anzeige (Tab Overlay) während der Runden – nur Runden, in denen sie eingeschaltet war. CPU-Temperatur nur mit HWiNFO. „Wann/Wo“ zeigt, auf welchen Maps oder zu welcher Tageszeit der PC am heißesten läuft. „Gedrosselt“: Sekunden, in denen die GPU wegen Temperatur oder Hardware langsamer lief (nur NVIDIA). „–“: in diesen Runden nicht erfasst – CPU-Temperatur, -Leistung, Kerne und FPS gibt es nur, solange HWiNFO läuft, und jeder Wert braucht mindestens 10 Sekunden Messwerte in der Runde.':
        '对局期间系统数值显示（“悬浮窗”选项卡）的数值，仅包括开启了该显示的对局。CPU 温度仅在使用 HWiNFO 时提供。“时间/地点”显示电脑在哪些地图上或一天中哪个时段温度最高。“降频”：GPU 因温度或硬件原因降速运行的秒数（仅限 NVIDIA）。“–”：这些对局中未记录。CPU 温度、功耗、核心和 FPS 只在 HWiNFO 运行时存在，且每个数值需要对局中至少 10 秒的读数。',
    'Eigene Position (mit der Maus verschieben)':
        '自定义位置（用鼠标拖动）',
    'SYSTEMWERTE':
        '系统数值',
    'Direkt über der Karte (wandert mit)':
        '紧贴地图上方（随地图移动）',
    'Schriftgrösse':
        '字号',
    'Übersicht':
        '概览',
    'Aktuelle Map':
        '当前地图',
    'Rundenzeit':
        '对局时间',
    'Ping':
        '延迟',
    'läuft':
        '进行中',
    'letzte Runde':
        '上一局',
    'startet':
        '正在开始',
    '4K: {n} von {total}':
        '4 杀：{total} 局中 {n} 局',
    '{n} Survivor-Runden':
        '{n} 局幸存者对局',
    '{n} normal':
        '{n} 局普通',
    '{n} Farming-Runden · Ø {bp} BP':
        '{n} 局刷分对局 · 平均 {bp} 血点',
    'Spielzeit heute: {time}':
        '今日已玩：{time}',
    'Systemwerte sind aus (Tab Overlay → Systemwerte).':
        '系统数值已关闭（“悬浮窗”选项卡 → 系统数值）。',
    'Systemwerte gibt es nur unter Windows.':
        '系统数值仅在 Windows 上可用。',
    'Erscheinen, sobald DBD läuft.':
        'DBD 运行后即会显示。',
    'OK':
        '确定',
    '4 Kills · leer = weniger als {n} Runden':
        '4 杀 · 空白 = 少于 {n} 局',
    'Killer × Map – Ø Kills laut Stats-Seite':
        '杀手 × 地图 – 来自统计页面的平均击杀',
    'Maps – am häufigsten gespielt':
        '地图 – 最常玩',
    'Median {time}':
        '中位数 {time}',
    'Noch keine Killer-Runde mit Ergebnis von der Stats-Seite.':
        '尚无带统计页面结果的杀手对局。',
    'keine Killer-Runden mit Stats-Daten':
        '没有带统计数据的杀手对局',
    'keine Survivor-Runden mit Stats-Daten':
        '没有带统计数据的幸存者对局',
    '{map} · {killer}: Ø {kills} Kills ({n} Runden)':
        '{map} · {killer}：平均 {kills} 击杀（{n} 局）',
    '{n} Matches':
        '{n} 场比赛',
    '{time} gespielt':
        '已玩 {time}',
    'Ø Bloodpoints':
        '平均血点',
    'Ø Rundendauer':
        '平均对局时长',
    'Anzeigen':
        '显示',
    'Kartenbild nicht lesbar: {error}':
        '无法读取地图图片：{error}',
    'Keine Map gewählt':
        '未选择地图',
    'Blendet die gewählte Map jetzt als Overlay ein – die Erkennung übernimmt beim nächsten Match wieder.':
        '立即在悬浮窗中显示所选地图，下一场对局时由识别功能重新接管。',
    'Ziehen, um den Kasten zu verschieben':
        '拖动以移动此框',
    'Anordnung zurücksetzen':
        '重置排列',
    'Die Kästen der Seiten lassen sich am Griff rechts im Titel verschieben.':
        '各页面的框可以通过其标题右侧的手柄移动。',
    'Stellt die Kästen auf allen Seiten, die Reiter-Reihen (Statistik, Overlay) und die Navigation links wieder in die ursprüngliche Reihenfolge.':
        '将所有页面的框、选项卡行（统计、悬浮窗）和左侧导航恢复为原始顺序。',
    'Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der du Dead by Daylight spielst (mehrere gehen).':
        '对局开始时，程序会从画面中读取地图名称。请勾选你玩 Dead by Daylight 时使用的语言（可多选）。',
    'Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.':
        '对局开始时地图会自动出现，对局结束后消失。“自动”会将它放在游戏画面旁的黑边中（超宽屏）或 DBD 窗口旁边。',
    'Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle Tasten findest du später unter Einstellungen.':
        '最重要的按键：点击一个进行更改，然后按下新的组合键。所有按键之后都可在“设置”中找到。',
    'Einrichtung starten':
        '开始设置',
    'Öffnet noch einmal die Einrichtung vom ersten Start: Spielsprache, Overlay-Position und die wichtigsten Tasten.':
        '再次打开首次启动时的设置：游戏语言、悬浮窗位置和最重要的按键。',
    'Suchen (Strg+F)':
        '搜索（Ctrl+F）',
    'Strg+F':
        'Ctrl+F',
    'Suchen: Einstellung, Seite, Map, Aktion, Runde …':
        '搜索：设置、页面、地图、操作、对局…',
    'Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst':
        '方向键选择 · Enter 打开 · Ctrl+Enter 在游戏或录像中打开 · Esc 关闭',
    'Aktionen':
        '操作',
    'Seiten':
        '页面',
    'Vorschlag von Claude':
        'Claude 的建议',
    'Enter':
        'Enter',
    'Strg+Enter':
        'Ctrl+Enter',
    'Claude fragen: „{q}“':
        '问 Claude：“{q}”',
    'Schickt nur die Frage und die Namen der Einstellungen an Claude':
        '只将问题和设置名称发送给 Claude',
    'Claude denkt nach …':
        'Claude 正在思考…',
    'Claude hat nichts Passendes gefunden.':
        'Claude 没有找到合适的内容。',
    'Claude hat die Frage abgelehnt.':
        'Claude 拒绝了这个问题。',
    'Claude hat unverständlich geantwortet.':
        'Claude 给出的回答无法读取。',
    'Claude ist nicht erreichbar – keine Internetverbindung?':
        '无法连接到 Claude，没有网络连接？',
    'Claude: Zu viele Anfragen – gleich noch einmal versuchen.':
        'Claude：请求过多，请稍后再试。',
    'Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen.':
        '没有 API 密钥，请在“设置 → 连接 → Claude”中输入。',
    'Zeigt im grossen Clip-Editor den Abschnitt „Mit Claude bearbeiten“: Du schreibst, was mit dem Schnitt passieren soll, Claude schlägt Schritte vor, du übernimmst oder verwirfst sie. Gesendet werden nur deine Bitte und der Schnitt als Zahlen – kein Bild, kein Dateiname. Braucht einen eigenen API-Key.':
        '在大片段编辑器中显示“用 Claude 编辑”部分：你写下希望对剪辑做什么，Claude 建议步骤，你可以应用或丢弃。只发送你的要求和以数字表示的剪辑，不发送图片和文件名。需要你自己的 API 密钥。',
    'Claude':
        'Claude',
    'Im Clip-Editor Claude nutzen':
        '在片段编辑器中使用 Claude',
    'Mit Claude bearbeiten':
        '用 Claude 编辑',
    'z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short':
        '例如：去掉前 10 秒，从 0:40 起两倍速，做成短视频',
    'Vorschlagen':
        '建议',
    'Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst.':
        '将你的要求和以数字表示的剪辑（时间、速度、淡入淡出，不含图片和文件名）发送给 Claude；在你应用之前不会有任何更改。',
    'Übernehmen':
        '应用',
    'Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z).':
        '执行建议的步骤，可一步撤销（Ctrl+Z）。',
    'Verwerfen':
        '丢弃',
    'Vergisst den Vorschlag; der Schnitt bleibt, wie er ist.':
        '放弃该建议；剪辑保持不变。',
    'Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude nutzen“ einschalten und einen API-Key eintragen.':
        '已关闭：请在“设置 → 连接 → Claude”中开启“在片段编辑器中使用 Claude”并输入 API 密钥。',
    'Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen.':
        '剪辑在此期间已更改，请重新获取建议。',
    'Claude hat keinen passenden Schritt gefunden.':
        'Claude 没有找到合适的步骤。',
    'Übernommen – Strg+Z macht es rückgängig.':
        '已应用，按 Ctrl+Z 撤销。',
    'übersprungen: {why}':
        '已跳过：{why}',
    'unbekannte Aktion':
        '未知操作',
    'Zeiten fehlen':
        '缺少时间',
    'Bereich zu kurz oder ausserhalb':
        '范围太短或超出范围',
    'Tempo nicht erlaubt':
        '不支持该速度',
    '{a}–{b} mit Tempo {f}×':
        '{a}–{b} 以 {f}× 速度',
    'würde alles entfernen':
        '会删除所有内容',
    '{a}–{b} herausgeschnitten':
        '已剪掉 {a}–{b}',
    'nur {a}–{b} behalten':
        '只保留 {a}–{b}',
    'Stelle ausserhalb':
        '时刻超出范围',
    'Schnitt bei {a}':
        '在 {a} 处分割',
    'keine Änderung':
        '无更改',
    'Blende ungültig':
        '不支持该淡变',
    'Standbild: Dauer ungültig':
        '定格画面：不允许该时长',
    'Untertitel zu kurz':
        '字幕太短',
    '{n} weitere Schritte nicht ausgeführt (höchstens {max})':
        '另有 {n} 个步骤未执行（最多 {max} 个）',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen.':
        '现在无法执行，请先完成当前编辑，然后再应用。',
    'Standbild bei {a} für {s} s':
        '在 {a} 处定格 {s} 秒',
    'Blende ohne Dauer':
        '淡变没有时长',
    'Blenden: ein {i} s, aus {o} s':
        '淡变：淡入 {i} 秒，淡出 {o} 秒',
    'Export-Art unbekannt':
        '未知导出类型',
    'Export-Art: {m}':
        '导出类型：{m}',
    'nur bei Export-Art Short':
        '仅适用于导出类型“短视频”',
    'Text fehlt':
        '缺少文字',
    'Short-Titel „{t}“':
        '短视频标题“{t}”',
    'Untertitel: Zeiten fehlen':
        '字幕：缺少时间',
    'zu viele Untertitel':
        '字幕过多',
    'Untertitel {a}–{b}':
        '字幕 {a}–{b}',
    'Claude: Der API-Key wird nicht angenommen – unter Einstellungen → Verbindungen prüfen („API-Key holen“ öffnet die Anthropic Console).':
        'Claude：API 密钥未被接受，请在“设置 → 连接”中检查（“获取 API 密钥”会打开 Anthropic Console）。',
    'Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen → Verbindungen → „Guthaben aufladen“.':
        'Claude：API 账户余额不足，请前往“设置 → 连接 → 充值”。',
    'API-Key holen':
        '获取 API 密钥',
    'Guthaben aufladen':
        '充值',
    'Öffnet die Seite „API keys“ der Anthropic Console im Browser (platform.claude.com). Dort einen Key anlegen und hier einfügen – er beginnt mit sk-ant-.':
        '在浏览器中打开 Anthropic Console 的“API keys”页面（platform.claude.com）。在那里创建密钥并粘贴到这里，它以 sk-ant- 开头。',
    'Öffnet die Seite „Billing“ der Anthropic Console im Browser. Die API wird getrennt von einem Claude-Abo im Voraus bezahlt; dort lässt sich auch ein monatliches Ausgabenlimit setzen.':
        '在浏览器中打开 Anthropic Console 的“Billing”页面。API 需预先付费，与 Claude 订阅分开；在那里也可以设置每月支出上限。',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude fragen“. Erst wenn du sie wählst, gehen deine Frage und die Namen der Einstellungen, Seiten und Aktionen an Claude (api.anthropic.com) – nie Runden, Maps oder Spieldaten. Braucht einen eigenen API-Key.':
        '在搜索（Ctrl+F）中显示“问 Claude”行。只有当你选择它时，你的问题以及设置、页面和操作的名称才会发送给 Claude（api.anthropic.com），绝不发送对局、地图或游戏数据。需要你自己的 API 密钥。',
    'Schickt eine kleine Probefrage an Claude und sagt, ob der API-Key angenommen wird (kostet einen kleinen Betrag deines API-Guthabens).':
        '向 Claude 发送一个小的测试问题，并告诉你 API 密钥是否被接受（会消耗少量 API 余额）。',
    'Entfernt den API-Key von diesem PC; die Suche fragt Claude dann nicht mehr.':
        '从这台电脑上移除 API 密钥；之后搜索不再询问 Claude。',
    'In der Suche Claude fragen können':
        '让搜索询问 Claude',
    'API-Key':
        'API 密钥',
    'Key prüfen':
        '检查密钥',
    'Key löschen':
        '删除密钥',
    'Claude: Key funktioniert.':
        'Claude：密钥有效。',
    'Claude: prüfe den Key …':
        'Claude：正在检查密钥…',
    'Claude: kein API-Key eingetragen.':
        'Claude：未输入 API 密钥。',
    'Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-).':
        'Claude：这看起来不像 API 密钥（它以 sk-ant- 开头）。',
    'Claude: Key eingetragen.':
        'Claude：已输入密钥。',
    'Schritt {n} von {total}':
        '第 {n} 步，共 {total} 步',
    'Sprache':
        '语言',
    'Sprache dieses Programms:':
        '本程序的语言：',
    'Weiter':
        '下一步',
    'Zurück':
        '上一步',
    'Überspringen':
        '跳过',
    'Einrichtung: {step}':
        '设置：{step}',
    'Aufgeteilt':
        '细分',
    'CPU-Temperatur':
        'CPU 温度',
    'GPU gedrosselt':
        'GPU 降频',
    'GPU-Leistung':
        'GPU 功耗',
    'GPU-Speicher':
        'GPU 显存',
    'GPU-Temperatur':
        'GPU 温度',
    'Hotspot':
        '热点',
    'Höchstwert':
        '最高',
    'Höchstwerte':
        '最高值',
    'RAM':
        'RAM',
    'Runden, zusammen {time}':
        '局，共 {time}',
    'VRAM':
        'VRAM',
    'Wert':
        '数值',
    '{n} von {total}':
        '{n}/{total}',
    'Ø CPU-Temperatur':
        '平均 CPU 温度',
    'Ø GPU-Last':
        '平均 GPU 负载',
    'Ø GPU-Leistung':
        '平均 GPU 功耗',
    'Ø GPU-Temperatur':
        '平均 GPU 温度',
    'über {n} Runden':
        '共 {n} 局',
    'Bilanz: Ø 2,8 Kills · 12 Runden':
        '战绩：平均 2.8 击杀 · 12 局',
    'Infos und Schrift (Name, Timer, Bilanz, Server)':
        '信息和文字（名称、计时器、战绩、服务器）',
    'Eigenes Element unter der Karte':
        '独立元素，位于地图下方',
    'Eigenes Element über der Karte':
        '独立元素，位于地图上方',
    'Eigenes Element, eigene Position':
        '独立元素，自定义位置',
    'Mit der Karte verbunden, unten':
        '与地图相连，位于下方',
    'Mit der Karte verbunden, oben':
        '与地图相连，位于上方',
    'Infos':
        '信息',
    'INFOS':
        '信息',
    'Infos (Timer, Bilanz, Server)':
        '信息（计时器、战绩、服务器）',
    'In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine Sofort-Clips (F8) und keinen Vorlauf.':
        'OBS 的回放缓存未启用：在 OBS 中依次打开“设置 → 输出 → 回放缓存 → 启用回放缓存”并应用。没有它就没有即时片段（F8）和预录。',
    'Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)':
        'OBS 中未启用回放缓存（设置 → 输出 → 回放缓存）',
    'Karten im selben Balken gleich breit':
        '同一黑边中的卡片宽度相同',
    'Zu einer Spalte zusammenführen':
        '合并为一列',
    'Die Karten, die im selben schwarzen Balken stehen, werden so breit gezeichnet wie die breiteste von ihnen – untereinander ergeben sie eine Spalte mit bündigen Rändern.':
        '位于同一黑边中的卡片按其中最宽的一张绘制，上下排列时形成边缘对齐的一列。',
    'Heute unter die Systemwerte, die Musik unter Heute, alle gleich breit – eine Spalte im Balken der Systemwerte. Rückgängig mit Strg+Z.':
        '“今日”放在系统数值下方，音乐放在“今日”下方，宽度一致，在系统数值所在的黑边中排成一列。按 Ctrl+Z 撤销。',
    'Cover':
        '封面',
    'Discord-Overlay freihalten':
        '为 Discord 悬浮窗留出空间',
    'Karte, Infos, Systemwerte, Heute und Musik weichen den Stellen aus, an denen Discords Overlay seine Widgets zeigt (in der Vorschau schraffiert). Das Programm liest nichts aus Discord – die Flächen sind fest.':
        '地图、信息、系统数值、今日和音乐会避开 Discord 悬浮窗显示小组件的位置（预览中以阴影线标出）。程序不从 Discord 读取任何内容，这些区域是固定的。',
    'Wie der Stil':
        '跟随样式',
    'Rund':
        '圆角',
    'Eckig':
        '直角',
    '{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr (der schwarze Balken ist voll).':
        '{what} 在这里已达最大，滑块超过 {cap} % 后不再有变化（黑边已填满）。',
    'Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).':
        '开启“地图可以比黑边更大”可以更大（此时它会延伸到游戏画面中）。',
    'Spielbild':
        '游戏画面',
    'Map-Name':
        '地图名称',
    'Farbthema':
        '颜色主题',
    'Gold (Standard)':
        '金色（默认）',
    'Blutrot':
        '血红',
    'Eisblau':
        '冰蓝',
    'Giftgrün':
        '毒绿',
    'Lila':
        '紫色',
    '„Heute“: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit':
        '“今日”：对局数、游戏时长、平均击杀/逃脱、时钟',
    'Eine eigene Karte, solange eine Map im Match zu sehen ist: wie viele Runden du heute gespielt hast, wie lange, Ø Kills bzw. Entkommen laut Stats-Seite und die Uhrzeit. Position darunter, Grösse über den Grössenregler („Heute“ wählen).':
        '对局中地图显示在屏幕上时的独立卡片：今天玩了多少局、玩了多久、来自统计页面的平均击杀或逃脱，以及当前时间。位置在下方设置，大小通过大小滑块设置（选择“今日”）。',
    'Dunkle Fläche hinter „Heute“':
        '“今日”后面的深色背景',
    'Vorlage':
        '预设',
    'Vorlage anwenden':
        '应用预设',
    'Alles links':
        '全部在左',
    'Alles rechts':
        '全部在右',
    'Verteilt: Karte links, Werte rechts':
        '分散：地图在左，数值在右',
    'Vorlage „{name}“ angewendet.':
        '已应用预设“{name}”。',
    'Setzt Karte, Systemwerte, „Heute“ und Musik auf einmal auf die gewählte Anordnung. „Rückgängig“ holt die vorherige zurück.':
        '一次性将地图、系统数值、“今日”和音乐放到所选的排列中。“撤销”可恢复之前的排列。',
    'Weich ein- und ausblenden':
        '平滑淡入淡出',
    'In kleinen DBD-Fenstern ausblenden':
        'DBD 窗口较小时隐藏',
    'Läuft DBD in einem kleinen Fenster (Bild kleiner als 1920×1080 oder schmaler als 16:9), zeigt das Programm im Spiel nichts – wie der Hauptschalter. Map-Erkennung, Statistik und OBS-Aufnahmen laufen weiter. Wird das Fenster wieder gross, erscheint das Overlay von selbst.':
        '如果 DBD 在小窗口中运行（画面小于 1920×1080 或比 16:9 更窄），程序不在游戏中显示任何内容，与总开关效果相同。地图识别、统计和 OBS 录像继续进行。窗口再次变大时，悬浮窗会自动恢复。',
    'Kleines DBD-Fenster ({w}×{h}) – Overlay ausgeblendet, Runden werden weiter gezählt und aufgenommen.':
        'DBD 窗口较小（{w}×{h}），悬浮窗已隐藏，对局仍会被计入和录制。',
    'Update gesperrt: eine Runde läuft. Nach dem Rundenende noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '更新已锁定：有对局正在进行。对局结束后请再次点击“更新并重启”。',
    'Alle Farming-Runden der Auswahl (Zeitraum, Region, Map, Modus) – unabhängig vom Rollen-Filter und von „Farming ausblenden“. Farming = Crossplay war in der Lobby aus (oder die eingestellte Farming-Region); korrigieren unter „Letzte Runden“ mit „Farming an/aus“. Aufnahmen liegen im Unterordner „Farming“ des Aufnahmeordners. Wartezeit „sofort“: die Lobby war voll, bevor eine Suchzeit messbar war. Server nur, wenn „Verbunden mit“ auf der Seite Server läuft.':
        '所选范围（时间段、区域、地图、模式）内的所有刷分对局，不受角色筛选和“隐藏刷分”影响。刷分 = 大厅中跨平台已关闭（或你设置的刷分区域）；可在“最近对局”下用“刷分开/关”更正。录像位于录像文件夹的“Farming”子文件夹中。等待“即时”：在能测量匹配时间之前大厅就已满员。服务器信息仅在“服务器”页面的“已连接到”运行时提供。',
    'Keine Farming-Runden in dieser Auswahl.':
        '此筛选范围内没有刷分对局。',
    '{n} als Killer · {m} als Survivor':
        '{n} 局杀手 · {m} 局幸存者',
    'Spielzeit':
        '游戏时长',
    'vom Map-Banner bis zum Rundenende':
        '从地图横幅到对局结束',
    'BP':
        '血点',
    '{n} gespeicherte Matches haben ein Loadout, aber keines davon ist in dieser Auswahl. Custom Games zählen nur mit dem Rollen-Filter „Custom Games“, Farming-Runden nicht mit „Farming ausblenden“, Matches ohne erkannte Runde gar nicht.':
        '{n} 场已保存的比赛有配装，但都不在此筛选范围内。自定义对局只在角色筛选为“自定义对局”时计入，刷分对局在“隐藏刷分”时不计入，没有识别到对局的比赛完全不计入。',
    'DBD-Fenster wieder gross genug – Overlay wieder an.':
        'DBD 窗口重新足够大，悬浮窗已恢复。',
    'Overlay anzeigen':
        '显示悬浮窗',
    'Hauptschalter: aus = das Programm zeigt im Spiel nichts (Karte, Systemwerte, Heute, Musik). Erkennung, Statistik und Aufnahmen laufen weiter. Auch als Knopf in der Übersicht.':
        '总开关：关闭 = 程序在游戏中不显示任何内容（地图、系统数值、今日、音乐）。识别、统计和录像继续进行。概览页上也有一个按钮。',
    'Overlay eingeschaltet.':
        '悬浮窗已开启。',
    'Overlay ausgeschaltet – die Erkennung läuft weiter.':
        '悬浮窗已关闭，识别继续进行。',
    'Overlay ausschalten':
        '关闭悬浮窗',
    'Overlay einschalten':
        '开启悬浮窗',
    'Blendet alles aus, was das Programm im Spiel zeigt – Karte, Systemwerte, Heute, Musik. Die Erkennung, Statistik und Aufnahmen laufen weiter.':
        '隐藏程序在游戏中显示的所有内容：地图、系统数值、今日、音乐。识别、统计和录像继续进行。',
    'Zeigt das Overlay im Spiel wieder an.':
        '在游戏中重新显示悬浮窗。',
    'Karte, Systemwerte und „Heute“ blenden in einer Drittelsekunde ein und aus, statt hart zu erscheinen. Die Musik hat ihr eigenes Häkchen.':
        '地图、系统数值和“今日”在三分之一秒内淡入淡出，而不是突然弹出。音乐有单独的复选框。',
    'Unter „Heute“':
        '“今日”下方',
    'Unter der Musik':
        '音乐下方',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter „Heute“.':
        '在“今日”后面加一块带圆角的半透明深色背景。',
    'HEUTE':
        '今日',
    'ENTKOMMEN ':
        '逃脱 ',
    'HEUTE ':
        '今日 ',
    'UHR ':
        '时间 ',
    '{n} RUNDEN · {time}':
        '{n} 局 · {time}',
    'Ø KILLS ':
        '平均击杀 ',
    'NORMAL ':
        '普通 ',
    'FARMING ':
        '刷分 ',
    'BP/H ':
        '血点/时 ',
    'OLED-Schwarz':
        'OLED 纯黑',
    'Hintergründe in echtem Schwarz statt Dunkelgrau – passt zu OLED-Bildschirmen und geht mit jeder Akzentfarbe. Im hellen Modus ohne Wirkung.':
        '背景使用纯黑而非深灰，适合 OLED 屏幕，且与所有强调色搭配。浅色模式下无效。',
    'Eigene Farbe':
        '自定义颜色',
    'Eigene Farbe …':
        '自定义颜色…',
    'Beliebige Farbe wählen – das Programm passt die Helligkeit an, bis alles lesbar ist.':
        '选择任意颜色，程序会调整其亮度，直到所有内容都清晰可读。',
    '„Läuft gerade“: Titel, Interpret und Cover':
        '“正在播放”：标题、艺术家和封面',
    'Liest Titel und Interpret aus der Windows-Mediensteuerung (dieselbe Liste wie beim Lautstärkeregler von Windows) – nur Anzeige, das Programm steuert nichts und speichert nichts.':
        '从 Windows 媒体控件（与 Windows 音量浮窗中的列表相同）读取标题和艺术家，仅用于显示，程序不控制也不保存任何内容。',
    'Unter den Systemwerten':
        '系统数值下方',
    'Rechts unten im Balken':
        '黑边内右下',
    'Links unten im Balken':
        '黑边内左下',
    'MUSIK':
        '音乐',
    'läuft gerade':
        '正在播放',
    'Albumcover zeigen':
        '显示专辑封面',
    'Auch Videos zeigen (YouTube, Twitch …) – aus: nur Musik':
        '也显示视频（YouTube、Twitch…），关闭：仅音乐',
    'Die Mediensteuerung meldet auch Videos aus dem Browser. An: ein Video erscheint als „▶ Titel“ mit dem Kanal darunter. Aus: die Karte zeigt nur Musik. Unterschieden wird am Album: Musikdienste melden eins, ein Video nicht.':
        '媒体控件也会报告浏览器中的视频。开启：视频显示为“▶ 标题”，下方是频道。关闭：卡片只显示音乐。通过专辑区分：音乐服务会报告专辑，视频则不会。',
    'Balken in der Farbe des Covers':
        '进度条使用封面颜色',
    'Dunkle Fläche hinter Karte und Infos':
        '地图及其文字行后面的深色背景',
    'Dunkle Fläche hinter den Systemwerten':
        '系统数值后面的深色背景',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Karte, Timer und Infozeilen (auch hinter „Warte auf Map“) – gut lesbar über hellen Stellen im Spiel.':
        '在地图、计时器和信息行后面（“正在等待地图”后面也有）加一块带圆角的半透明深色背景，在游戏的明亮部分上也易于阅读。',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Systemwerten und „Heute“.':
        '在系统数值和“今日”后面加一块带圆角的半透明深色背景。',
    'Restzeit statt Länge (−1:46)':
        '显示剩余时间而非总时长（−1:46）',
    'Dunkle Fläche hinter der Musikkarte':
        '音乐卡片后面的深色背景',
    'Weich ein- und ausblenden (auch beim nächsten Lied)':
        '平滑淡入淡出（切换下一首时也是）',
    'Der Fortschrittsbalken nimmt die Hauptfarbe des Albumcovers an, wie bei Spotify. Graue Cover: weiss.':
        '进度条采用专辑封面的主色，就像 Spotify 一样。灰色封面：白色。',
    'Rechts neben dem Balken steht, wie lange das Lied noch läuft, statt seiner Gesamtlänge.':
        '进度条右侧显示歌曲还剩多长时间，而不是总时长。',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Cover und Text – gut lesbar, wenn die Karte über hellen Stellen im Spiel liegt.':
        '在封面和文字后面加一块带圆角的半透明深色背景，卡片位于游戏的明亮部分上时也易于阅读。',
    'Die Musikkarte blendet in einer Drittelsekunde ein und aus, statt hart zu erscheinen – auch wenn ein neues Lied beginnt.':
        '音乐卡片在三分之一秒内淡入淡出，而不是突然弹出，开始播放新歌时也是如此。',
    'Das Bild zum Lied links neben Titel und Interpret – Windows liefert es mit; es bleibt nur im Speicher.':
        '在标题和艺术家左侧显示歌曲图片，由 Windows 提供；只保存在内存中。',
    'Gross – Cover oben, Titel darunter':
        '大 – 封面在上，标题在下',
    'Kompakt – Cover links':
        '紧凑 – 封面在左',
    'Fortschritt des Lieds zeigen':
        '显示歌曲进度',
    'Unter Titel und Künstler: wie weit das Lied ist, mit Balken und Länge – wie in Spotify.':
        '在标题和艺术家下方显示歌曲播放到哪里，带进度条和时长，就像 Spotify 一样。',
    'KARTE · Strg+Mausrad = Grösse':
        '地图 · Ctrl+滚轮 = 大小',
    'Ziehst: {name}':
        '正在拖动：{name}',
    'Unter der Maus: {name}':
        '鼠标下方：{name}',
    'Kartenstil':
        '地图样式',
    'Kartenstil: {style}.':
        '地图样式：{style}。',
    'Map wählen …':
        '选择地图…',
    'Zur Seite Maps: eine Map von Hand anzeigen (Doppelklick oder „Anzeigen“). Beim nächsten Match übernimmt die automatische Erkennung wieder.':
        '前往“地图”页面：手动显示一张地图（双击或“显示”）。下一场对局时自动识别会重新接管。',
    'Erscheint automatisch, sobald im Match das Map-Banner kommt – oder von Hand über „Map wählen“.':
        '对局中地图横幅一出现就会自动显示，也可通过“选择地图”手动显示。',
    'Wann zeigen':
        '显示时机',
    'Alle Maps':
        '所有地图',
    'Zuletzt gespielt':
        '最近玩过',
    'Suchen: Name, Realm, Abkürzung …':
        '搜索：名称、领域、缩写…',
    'Klick oder Enter = groß ansehen · Doppelklick oder Strg+Enter = jetzt anzeigen. Die Erkennung übernimmt beim nächsten Match wieder.':
        '单击或 Enter = 大图查看 · 双击或 Ctrl+Enter = 立即显示。下一场对局时识别功能会重新接管。',
    'Zurück zu den Karten des Realms (Esc).':
        '返回该领域的地图（Esc）。',
    'Allgemein':
        '常规',
    'Alle Einstellungen zurücksetzen':
        '重置所有设置',
    'Alle Einstellungen auf die Auslieferung zurücksetzen? Runden, Match-Daten und eigene Bilder bleiben. Das Programm startet danach neu.':
        '将所有设置重置为初始状态吗？对局、比赛数据和自己的图片会保留。之后程序将重新启动。',
    'Alle Einstellungen zurückgesetzt.':
        '所有设置已重置。',
    'Standard wiederherstellen':
        '恢复默认',
    'Ausschalten':
        '关闭',
    '{free} von {total} Regionen freigegeben':
        '{total} 个区域中允许 {free} 个',
    'DBD läuft gerade – die Änderung gilt erst nach einem Neustart von DBD.':
        'DBD 正在运行，更改在 DBD 重新启动后才会生效。',
    'Suchen …':
        '搜索…',
    'Setzt jede Einstellung auf die Auslieferung zurück (Overlay, Hotkeys, Erkennung, Server-Auswahl im Programm …). Runden, Match-Daten und eigene Bilder bleiben; das Programm startet danach neu. Vorher sichern: „Einstellungen exportieren“.':
        '将所有设置重置为初始状态（悬浮窗、快捷键、识别、程序中的区域选择…）。对局、比赛数据和自己的图片会保留；之后程序将重新启动。请先备份：“导出设置”。',
    'Grösse {pct} %':
        '大小 {pct} %',
    'Eigene Einstellungen dieser Map: {what}':
        '此地图的自定义设置：{what}',
    'Eigene Grösse und Drehung zurücksetzen':
        '重置自定义大小和旋转',
    'Kartenbild ersetzen …':
        '替换地图图片…',
    'Im schwarzen Rand, solange die Karte im Match zu sehen ist. GPU-Werte von NVIDIA (Treiber), CPU-Temperatur nur mit HWiNFO („Shared Memory Support“ an) – kein eigener Treiber.':
        '对局中地图显示在屏幕上时位于黑边中。GPU 数值来自 NVIDIA（驱动程序），CPU 温度仅在使用 HWiNFO 时提供（需开启“Shared Memory Support”），不安装任何自己的驱动程序。',
    'Standard (wie ausgeliefert)':
        '标准（初始状态）',
    'Fenster {size}':
        '窗口 {size}',
    'alle Fenstergrössen':
        '所有窗口大小',
    'Gilt für: {window}':
        '适用于：{window}',
    'Gilt für: {maps} · {window}':
        '适用于：{maps} · {window}',
    'nur {map}':
        '仅 {map}',
    'alle Maps (keine Map eingeblendet)':
        '所有地图（屏幕上无地图）',
    'Letzte 7 Tage':
        '最近 7 天',
    'Letzte 30 Tage':
        '最近 30 天',
    'Rolle/Killer':
        '角色/杀手',
    'Weitere 100 Runden anzeigen':
        '再显示 100 局',
    'Runden exportieren':
        '导出对局',
    '{n} Runden exportiert: {path}':
        '已导出 {n} 局：{path}',
    'Median':
        '中位数',
    '{n} Runden':
        '{n} 局',
    'Längste':
        '最长',
    'Die Liste zeigt die neuesten 100 Runden der Auswahl; jeder Klick hängt 100 ältere an.':
        '列表显示所选范围内最新的 100 局；每次点击会追加 100 局更早的对局。',
    'Server-Tab öffnen':
        '打开服务器选项卡',
    'Match-Daten einrichten …':
        '设置比赛数据…',
    'Einrichten …':
        '设置…',
    'Noch keine Runden heute':
        '今天还没有对局',
    'Stats-Seite':
        '统计页面',
    'nicht eingerichtet':
        '未设置',
    'Match-Daten':
        '比赛数据',
    'Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → Match-Daten → Offizielle Match-Daten).':
        '你对局中的击杀、逃脱和血点来自 stats.deadbydaylight.com，由你的浏览器加载，而不是由程序加载。也可以之后再设置（设置 → 比赛数据 → 官方比赛数据）。',
    'Zur Seite Server: dort „Spielserver anzeigen“ anhaken – Region und Ping stehen dann hier und im Overlay.':
        '前往“服务器”页面：在那里勾选“显示游戏服务器”，之后区域和延迟会显示在这里和悬浮窗中。',
    'Zu Einstellungen → Match-Daten → Offizielle Match-Daten: einmal das Userscript in den Browser, danach zählen Kills, Entkommen und Bloodpoints in der Statistik.':
        '前往“设置 → 比赛数据 → 官方比赛数据”：将用户脚本装入浏览器一次，之后击杀、逃脱和血点就会计入统计。',
    'CPU DROSSELT (TEMP.)':
        'CPU 降频（温度）',
    'CPU gedr.':
        'CPU 降频',
    'GPU gedr.':
        'GPU 降频',
    'CPU gedrosselt':
        'CPU 降频',
    'CPU Ø W':
        'CPU 平均瓦数',
    'CPU-Leistung':
        'CPU 功耗',
    'Kern Ø %':
        '核心平均 %',
    'Ø CPU-Leistung':
        '平均 CPU 功耗',
    'Ø stärkster CPU-Kern':
        '最忙 CPU 核心平均',
    'Niedrigstes FPS-Tief':
        '最低 FPS low',
    'Ø FPS':
        '平均 FPS',
    'Ø FPS-Tief':
        '平均 FPS low',
    'FPS Ø':
        'FPS 平均',
    'FPS Tief':
        'FPS low',
    'Klick: sortieren · Rechtsklick: Spalten ein-/ausblenden':
        '单击：排序 · 右键单击：显示/隐藏列',
    'Alle Spalten zeigen':
        '显示所有列',
    'Exportieren …':
        '导出…',
    'Zeitraum':
        '时间范围',
    'Von':
        '从',
    'Bis':
        '到',
    'TT.MM.JJJJ HH:MM – auch nur ein Datum (ganzer Tag) oder nur eine Uhrzeit (heute); leer = offen.':
        'DD.MM.YYYY HH:MM，也可以只写日期（全天）或只写时间（今天）；留空 = 不限。',
    'Gestern':
        '昨天',
    'Alles':
        '全部',
    'Eigener Zeitraum':
        '自定义范围',
    'Filter':
        '筛选',
    'Custom Games einschliessen':
        '包括自定义对局',
    'Farming-Runden einschliessen':
        '包括刷分对局',
    'Spalten':
        '列',
    'Start':
        '开始',
    'Realm':
        '领域',
    'Ping (ms)':
        '延迟（毫秒）',
    'Kills':
        '击杀',
    'Normal':
        '普通',
    'ja':
        '是',
    'nein':
        '否',
    'CSV-Datei (Excel)':
        'CSV 文件（Excel）',
    'Textliste (eine Zeile je Runde)':
        '文本列表（每局一行）',
    '{n} Runden, {m} Spalten':
        '{n} 局，{m} 列',
    'Zeitangabe nicht lesbar: „{text}“ – Format TT.MM.JJJJ HH:MM.':
        '无法读取时间“{text}”，格式为 DD.MM.YYYY HH:MM。',
    'Nichts zu kopieren – keine Runde passt, oder keine Spalte gewählt.':
        '没有可复制的内容：没有匹配的对局，或未选择任何列。',
    'Nichts zu speichern – keine Runde passt, oder keine Spalte gewählt.':
        '没有可保存的内容：没有匹配的对局，或未选择任何列。',
    'In Zwischenablage kopieren':
        '复制到剪贴板',
    'Als Datei speichern …':
        '另存为文件…',
    'Schliessen':
        '关闭',
    '{n} Runden in die Zwischenablage kopiert.':
        '已将 {n} 局复制到剪贴板。',
    'Spalte „{name}“ mit ausgeben.':
        '包括“{name}”列。',
    'Öffnet das Export-Fenster: Zeitraum (auch von–bis), Rolle, Killer, Map, Region, Spalten nach Wahl – als CSV für Excel oder als Textliste in die Zwischenablage. Die Filter der Statistik sind vorbelegt.':
        '打开导出窗口：时间范围（也可指定起止）、角色、杀手、地图、区域、自选列，导出为 Excel 用的 CSV 或复制到剪贴板的文本列表。统计中的筛选条件会预先填入。',
    'Kopiert die Runden in der gewählten Form (CSV oder Textliste) in die Zwischenablage – zum Einfügen in Discord, Excel oder einen Editor.':
        '以所选格式（CSV 或文本列表）将对局复制到剪贴板，可粘贴到 Discord、Excel 或编辑器中。',
    'Speichert die Runden als Datei: CSV (Semikolon, UTF-8 mit BOM – Excel öffnet sie direkt) oder Textliste (.txt).':
        '将对局保存为文件：CSV（分号分隔，带 BOM 的 UTF-8，Excel 可直接打开）或文本列表（.txt）。',
    'Schliesst das Fenster.':
        '关闭窗口。',
    'Aus: Custom Games (eigene Lobbys, Bots) bleiben draussen.':
        '关闭：不包括自定义对局（自己的大厅、机器人）。',
    'Aus: Farming-Runden (Crossplay aus bzw. Farming-Region) bleiben draussen.':
        '关闭：不包括刷分对局（跨平台关闭或刷分区域）。',
    'Eine Zeile je Runde, Spalten durch Semikolon getrennt, mit Kopfzeile.':
        '每局一行，各列用分号分隔，带标题行。',
    'Eine Zeile je Runde, die gewählten Spalten mit „ · “ getrennt, ohne Kopfzeile – zum Einfügen in einen Chat.':
        '每局一行，所选列用“ · ”分隔，不带标题，可直接粘贴到聊天中。',
    'Verbindungen':
        '连接',
    'Ton':
        '声音',
    'Aufräumen':
        '清理',
    'Jede Runde mit OBS aufnehmen':
        '用 OBS 录制每一局',
    'Port':
        '端口',
    'Passwort':
        '密码',
    'Verbindung testen':
        '测试连接',
    'Aufnahmeordner wählen …':
        '选择录像文件夹…',
    '(kein Ordner gewählt)':
        '（未选择文件夹）',
    'Platz für Aufnahmen':
        '录像空间',
    'Ganze Platte (Älteste weg, wenn sie voll wird)':
        '整个驱动器（满时删除最旧的）',
    'Vorlauf aus dem OBS-Wiederholungspuffer sichern':
        '保留 OBS 回放缓存中的前导部分',
    'OBS nimmt auf, das Programm sagt nur wann: Start beim Map-Banner, Stopp beim erkannten Rundenende, Datei nach Datum, Map und Killer benannt. Dafür in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server einschalten und Port und Passwort unter Verbindungen → OBS-Verbindung eintragen; Verbindung nur auf diesem PC (127.0.0.1). Empfohlen: Aufnahmeformat MKV oder Hybrid-MP4 (bleibt bei Abbruch lesbar), Fenster- oder Bildschirmaufnahme statt Spielaufnahme. Der Ordner wird über sein Laufwerk gemerkt – ist die Platte nicht angeschlossen, wird nicht aufgenommen.':
        '录制由 OBS 完成，程序只告诉它何时录制：在地图横幅时开始，在检测到对局结束时停止，文件以日期、地图和杀手命名。在 OBS 中通过“工具 → WebSocket 服务器设置”启用服务器，并在“连接 → OBS 连接”中输入端口和密码；连接只在这台电脑上（127.0.0.1）。推荐：录像格式 MKV 或混合 MP4（崩溃后仍可读取），使用窗口采集或显示器采集而不是游戏采集。文件夹按驱动器记住，驱动器拔出时不会录制任何内容。',
    'Ordner für die Aufnahmen (z. B. auf der externen Platte)':
        '录像文件夹（例如在外部驱动器上）',
    'Aufnahmeordner: {path}':
        '录像文件夹：{path}',
    'Verbinde mit OBS …':
        '正在连接 OBS…',
    'Aufnahme: {text}':
        '录像：{text}',
    'Aufnahme gespeichert: {file}':
        '录像已保存：{file}',
    'Aufnahmen gelöscht (Platz): {n}':
        '已删除录像（空间）：{n}',
    'OBS hat die Verbindung geschlossen':
        'OBS 关闭了连接',
    'OBS antwortet nicht auf die Anfrage {kind}':
        'OBS 未响应请求 {kind}',
    'OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})':
        '无法连接 OBS：OBS 是否正在运行且已开启 WebSocket 服务器？（{error}）',
    'Keine Antwort von obs-websocket':
        'obs-websocket 没有响应',
    'Kein obs-websocket auf diesem Port':
        '此端口上没有 obs-websocket',
    'Falsche WebSocket-Antwort':
        'WebSocket 响应错误',
    'Unerwartete Begrüssung von OBS':
        'OBS 的问候消息异常',
    'OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)':
        'OBS 需要密码（OBS：工具 → WebSocket 服务器设置）',
    'OBS hat die Anmeldung abgelehnt – Passwort falsch?':
        'OBS 拒绝了登录，密码错误？',
    'OBS {version} verbunden':
        '已连接 OBS {version}',
    'nimmt gerade auf':
        '正在录制',
    'bereit':
        '就绪',
    'Wiederholungspuffer läuft':
        '回放缓存运行中',
    'Wiederholungspuffer aus (kein Vorlauf)':
        '回放缓存已关闭（无预录）',
    'Ordner: {folder}':
        '文件夹：{folder}',
    'Ordner/Laufwerk nicht gefunden':
        '未找到文件夹/驱动器',
    'Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen':
        '录像驱动器未连接，该局不会被录制',
    'Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen':
        '录像驱动器几乎已满，该局不会被录制',
    'OBS nimmt schon auf (von Hand?) – nichts gestartet':
        'OBS 已在录制（手动？），未开始任何录制',
    'Nimmt die Runde auf':
        '正在录制对局',
    'OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet':
        'OBS 未提供文件名，录像未关联',
    "Aufnahme liegt in OBS' eigenem Ordner: {path}":
        '录像位于 OBS 自己的文件夹中：{path}',
    'Gespeichert: {file}':
        '已保存：{file}',
    'Das Programm startet die OBS-Aufnahme beim Map-Banner und stoppt sie beim erkannten Rundenende (obs-websocket, nur auf diesem PC). OBS muss laufen.':
        '程序在地图横幅时开始 OBS 录制，在检测到对局结束时停止（obs-websocket，仅在这台电脑上）。OBS 必须在运行。',
    'Verbindet sich einmal mit OBS und zeigt Version, Aufnahmezustand, Wiederholungspuffer und ob der Aufnahmeordner erreichbar ist.':
        '连接一次 OBS，显示其版本、是否在录制、回放缓存以及录像文件夹是否可访问。',
    'Ordner, in den OBS die Runden legt – z. B. auf der externen Platte. Gemerkt wird das Laufwerk, nicht der Buchstabe: bekommt die Platte einen anderen, findet das Programm den Ordner trotzdem.':
        'OBS 存放对局录像的文件夹，例如在外部驱动器上。记住的是驱动器而不是其盘符：如果驱动器换了盘符，程序仍能找到该文件夹。',
    'Läuft in OBS der Wiederholungspuffer, wird er beim Map-Banner gespeichert – der Anfang (Spawn) fehlt dann nicht, aber die Datei enthält auch Lobby und Ladebildschirm. Seit 1.5.5 standardmässig aus (Wunsch des Nutzers: nur die Runde). Die Datei liegt als „(Vorlauf)“ neben der Runde.':
        '如果 OBS 的回放缓存正在运行，会在地图横幅时保存它，这样开头（出生点）就不会缺失，但文件中也会包含大厅和加载界面。自 1.5.5 起默认关闭（用户希望：只录对局）。该文件以“(Vorlauf)”放在对局录像旁边。',
    'Wiederholungspuffer mit DBD starten und stoppen':
        '随 DBD 启动和停止回放缓存',
    'Nur das DBD-Fenster aufnehmen':
        '只录制 DBD 窗口',
    'Dafür die OBS-Spielaufnahme verwenden':
        '为此使用 OBS 的游戏采集',
    'Statt der Fensteraufnahme legt das Programm in OBS eine Spielaufnahme „Fog Scout – DBD-Spiel“ an und blendet die Fensteraufnahme aus. Die Spielaufnahme braucht etwas weniger Leistung; OBS hängt sich dafür mit seinem Anti-Cheat-kompatiblen Hook ins Spiel – das macht OBS, nicht dieses Programm. Ihr eigener Ton bleibt aus, der Spielton kommt weiter über die Tonquelle „Fog Scout – DBD“. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“.':
        '程序会在 OBS 中创建游戏采集源“Fog Scout – DBD-Spiel”来代替窗口采集，并隐藏窗口采集。游戏采集需要的性能稍少；为此 OBS 会用其兼容反作弊的挂钩接入游戏，这是 OBS 做的，不是本程序。它自身的声音保持关闭，游戏声音仍通过音频源“Fog Scout – DBD”传入。仅与“只录制 DBD 窗口”一起使用。',
    'Bildquelle {name} über {over} gelegt':
        '图像源 {name} 已放在 {over} 之上',
    'Bildquelle angelegt: {name} (Szene „{scene}“)':
        '已创建图像源：{name}（场景“{scene}”）',
    'Bildquelle in der Szene „{scene}“ ausgeblendet: {name}':
        '已在场景“{scene}”中隐藏图像源：{name}',
    'Bildquelle zur Szene „{scene}“ hinzugefügt: {name}':
        '已将图像源添加到场景“{scene}”：{name}',
    'Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        '已在场景“{scene}”中重新显示图像源：{name}',
    'Bildquelle {name} zeigt jetzt {exe}':
        '图像源 {name} 现在显示 {exe}',
    'DBD-Fenster in OBS nicht eingerichtet: {error}':
        '未在 OBS 中设置 DBD 窗口：{error}',
    'OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin keine Sofort-Clips (F8) und kein Vorlauf.':
        'OBS 无法启动回放缓存（OBS 报告输出错误，多半是编码器问题，详见 OBS 日志）。程序只会在下次启动 DBD 时重试；在此之前没有即时片段（F8）和预录。',
    'Das Programm legt in OBS eine Fensteraufnahme „Fog Scout – DBD-Fenster“ an (oben in der laufenden Szene, auf die Leinwand eingepasst) und stellt sie auf Steam, Epic oder Store um. Aufgenommen wird dann nur das Spiel – ohne Discord, Benachrichtigungen und ohne das Overlay dieses Programms. OBS nimmt dabei über Windows auf; die Spielaufnahme gibt es als Häkchen darunter. Aus: die Quelle wird nur ausgeblendet, deine eigene Bildschirmaufnahme bleibt unangetastet.':
        '程序会在 OBS 中创建窗口采集源“Fog Scout – DBD-Fenster”（位于当前播出场景的最上层，适配画布），并将其切换到 Steam、Epic 或 Store 版本。这样只录制游戏，不含 Discord、通知以及本程序的悬浮窗。此处 OBS 通过 Windows 采集；游戏采集是下面的复选框。关闭：该源只会被隐藏，你自己的显示器采集保持不变。',
    'Das Programm startet den Wiederholungspuffer in OBS, sobald DBD läuft, und stoppt ihn, wenn DBD zu ist – so kostet er ausserhalb des Spiels nichts und du musst nicht daran denken.':
        'DBD 一运行，程序就启动 OBS 的回放缓存，DBD 关闭时将其停止，这样在游戏之外不消耗资源，你也无需操心。',
    'Nachlauf nach dem Rundenende':
        '对局结束后的尾段',
    'Overlay mit in die Aufnahme':
        '将悬浮窗录入录像',
    'Die Fensteraufnahme enthält das Overlay dieses Programms nicht (eigene Fenster). Mit Häkchen schreibt das Programm das sichtbare Overlay – Karte, Infos, Systemwerte, Heute, Musik – als Bild in seinen Cache-Ordner und legt in OBS eine Bildquelle „Fog Scout – Overlay“ darauf an, genau dort, wo das Overlay über dem DBD-Fenster liegt. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“; bei einer Bildschirmaufnahme ist das Overlay ohnehin im Bild. Aus: die Quelle wird nur ausgeblendet.':
        '窗口采集不包含本程序的悬浮窗（它们是独立窗口）。勾选后，程序会将可见的悬浮窗（地图、文字行、系统数值、今日、音乐）作为图片写入其缓存文件夹，并在 OBS 中基于它创建图像源“Fog Scout – Overlay”，位置正好与悬浮窗在 DBD 窗口上的位置相同。仅与“只录制 DBD 窗口”一起使用；显示器采集本来就会显示悬浮窗。关闭：该源只会被隐藏。',
    'Overlay in OBS nicht eingerichtet: {error}':
        '未在 OBS 中设置悬浮窗：{error}',
    '{n} s':
        '{n} 秒',
    'keiner':
        '无',
    'Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen.':
        '录像驱动器未连接，对局不会被录制。',
    'OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})':
        'OBS 未运行，对局不会被录制。（{error}）',
    'OBS bereit – Runden werden aufgenommen':
        'OBS 已就绪，对局会被录制',
    'Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).':
        '录像似乎已损坏（{why}）：{file}，请检查 OBS 设置（编码器、驱动器）。',
    'Aufnahme':
        '录像',
    'Vorlauf und Runde zu einer Datei zusammenfügen':
        '将预录和对局合并为一个文件',
    'Nach der Runde hängt ffmpeg den Vorlauf vorne an die Aufnahme – ohne Neukodierung, in Sekunden. Seit 1.5.5 standardmässig aus: Am PC des Nutzers lief der Rundenteil der zusammengefügten Datei zu schnell. Klappt es nicht, bleiben beide Dateien liegen.':
        '对局结束后，ffmpeg 会把预录放在录像前面，不重新编码，几秒钟即可完成。自 1.5.5 起默认关闭：在用户的电脑上，合并文件中的对局部分播放过快。如果失败，两个文件都会保留。',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start; bis dahin bleibt der Vorlauf eine eigene Datei.':
        '缺少 ffmpeg（imageio-ffmpeg 包），start.bat 会在下次启动时安装它；在此之前预录仍是一个单独的文件。',
    'Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben':
        '已保存：{file}，预录未合并，作为单独的文件放在旁边',
    'Clip-Marke setzen':
        '设置片段标记',
    'Clip-Marke {n} bei {pos} gesetzt.':
        '已在 {pos} 处设置片段标记 {n}。',
    'Keine Aufnahme läuft – keine Clip-Marke gesetzt.':
        '没有正在进行的录制，未设置片段标记。',
    'Aufnahmen':
        '录像',
    'Aufnahmen einrichten …':
        '设置录像…',
    'Öffnet die Einstellungen für die Aufnahmen mit OBS (Ordner, Verbindung).':
        '打开用 OBS 录像的设置（文件夹、连接）。',
    'Platte nicht angeschlossen':
        '驱动器未连接',
    'kein Ordner gewählt':
        '未选择文件夹',
    'Platz wird gemessen …':
        '正在测量空间…',
    '{n} mit Marke':
        '{n} 个带标记',
    'älteste {date}':
        '最早 {date}',
    '{size} frei':
        '可用 {size}',
    '1 Aufnahme':
        '1 个录像',
    '{n} Aufnahmen':
        '{n} 个录像',
    'Abspielen':
        '播放',
    'Alle Aufnahmen':
        '所有录像',
    'Aufnahme fehlt: {file}':
        '录像缺失：{file}',
    'Aufnahme gelöscht: {file}':
        '录像已删除：{file}',
    'Aufnahme löschen':
        '删除录像',
    'Aufnahme nicht gelöscht ({error}): {file}':
        '录像未删除（{error}）：{file}',
    'Aufnahme wird behalten: {file}':
        '录像将被保留：{file}',
    'Aufnahme wird nicht mehr behalten: {file}':
        '录像不再保留：{file}',
    'Aufnahme-Laufwerk nicht angeschlossen.':
        '录像驱动器未连接。',
    'Aufnahmeordner öffnen':
        '打开录像文件夹',
    'Behalten':
        '保留',
    'Beschädigt':
        '已损坏',
    'Datei':
        '文件',
    'Einschalten unter Einstellungen → Aufnahmen.':
        '请在“设置 → 录像”中开启。',
    'Im Explorer zeigen':
        '在资源管理器中显示',
    'Keine Marken – F8 während der Runde setzt eine.':
        '没有标记，对局中按 F8 可设置标记。',
    'Marken: {list}':
        '标记：{list}',
    'Mit Marke':
        '带标记',
    'Nicht mehr behalten':
        '取消保留',
    'Noch kein Aufnahmeordner gewählt.':
        '尚未选择录像文件夹。',
    'fehlt':
        '缺失',
    '{file} von der Platte löschen?':
        '要从驱动器中删除 {file} 吗？',
    'Spielt die markierte Aufnahme im Standard-Videoplayer ab.':
        '用默认视频播放器播放标记的录像。',
    'Öffnet den Explorer mit der markierten Datei.':
        '打开资源管理器并选中标记的文件。',
    'Eine behaltene Aufnahme wird nie fürs Aufräumen gelöscht, wenn die Platte Platz braucht. Nochmal drücken hebt es auf.':
        '驱动器需要空间时，清理功能永远不会删除保留的录像。再按一次可撤销。',
    'Löscht die markierte Aufnahme (und ihren Vorlauf) von der Platte – nach Rückfrage.':
        '从驱动器中删除标记的录像（及其预录），会先确认。',
    'Öffnet den Aufnahmeordner im Explorer.':
        '在资源管理器中打开录像文件夹。',
    'Farming-Runden im Unterordner „Farming“ ablegen':
        '将刷分对局放入“Farming”子文件夹',
    'Runden, die das Programm als Farming erkennt (Crossplay aus oder die Farming-Region), landen im Unterordner „Farming“ des Aufnahmeordners statt zwischen den normalen Runden. Clips gehen immer in den Ordner „Clips“.':
        '程序识别为刷分的对局（跨平台关闭或刷分区域）会放入录像文件夹的“Farming”子文件夹，而不是与普通对局放在一起。片段始终放入“Clips”文件夹。',
    'Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in debug/lobby).':
        '无法读取跨平台标识，该对局不计为刷分（截图在 debug/lobby 中）。',
    'Rolle für {n} Runden auf {role} geändert.':
        '{n} 局的角色已改为{role}。',
    '{n} Runden aus der Statistik löschen?':
        '要从统计中删除 {n} 局吗？',
    '{n} Runden gelöscht.':
        '已删除 {n} 局。',
    '{n} Runden zählen jetzt als Farming-Runden.':
        '{n} 局现在计为刷分对局。',
    '{n} Runden zählen wieder als normale Runden.':
        '{n} 局重新计为普通对局。',
    'Clip bearbeiten …':
        '编辑片段…',
    'Öffnet den Clip-Editor für die markierte Aufnahme: Vorschau, Zeitleiste mit Marken, Start/Ende setzen, Ausschnitt als MP4 in den Ordner „Clips“ speichern.':
        '为标记的录像打开片段编辑器：预览、带标记的时间轴、设置开始/结束，将剪辑保存为 MP4 到“Clips”文件夹。',
    'Clip bearbeiten – {name}':
        '编辑片段 – {name}',
    'Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)':
        '快速（按关键帧，开头可能提前几秒）',
    'Genau (Bild neu kodiert, dauert etwas)':
        '精确（重新编码画面，需要一点时间）',
    '5 Sekunden vor (Shift+→)':
        '前进 5 秒（Shift+→）',
    '5 Sekunden zurück (Shift+←)':
        '后退 5 秒（Shift+←）',
    '▶ Abspielen':
        '▶ 播放',
    '⏸ Pause':
        '⏸ 暂停',
    'Abspielen / Pause (Leertaste)':
        '播放/暂停（空格键）',
    'Start setzen':
        '设置开始',
    'Ende setzen':
        '设置结束',
    'Der Clip beginnt am Abspielkopf (Taste I).':
        '片段从播放头处开始（按键 I）。',
    'Der Clip endet am Abspielkopf (Taste O).':
        '片段在播放头处结束（按键 O）。',
    'Zur Marke ▸':
        '转到标记 ▸',
    'Marken (F8)':
        '标记（F8）',
    'Clip um Marke':
        '围绕标记的片段',
    'Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der nächsten am Abspielkopf) und endet {after} s danach.':
        '片段从所选标记前 {before} 秒开始（未选择时：离播放头最近的标记），在其后 {after} 秒结束。',
    'Springt zur nächsten F8-Marke (Taste M).':
        '跳到下一个 F8 标记（按键 M）。',
    'Clip: {start} – {end} ({length} s)':
        '片段：{start} – {end}（{length} 秒）',
    'Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows).':
        '预览时同时播放录像的声音（Windows）。',
    'Ton im Clip':
        '片段中的声音',
    'Abspielkopf hierher':
        '播放头移到此处',
    'Als Custom Game':
        '作为自定义对局',
    'Als Killer-Runde':
        '作为杀手对局',
    'Als Survivor-Runde':
        '作为幸存者对局',
    'Ausblenden':
        '隐藏',
    'Bild':
        '画面',
    'Clip beginnt hier':
        '片段从这里开始',
    'Clip endet hier':
        '片段在这里结束',
    'Dunkle Fläche dahinter':
        '后面加深色背景',
    'Grösse zurücksetzen':
        '重置大小',
    'Standbild gespeichert: {file}':
        '静帧已保存：{file}',
    'Standbild hier speichern':
        '在此处保存静帧',
    'Standbild nicht gespeichert.':
        '静帧未保存。',
    '{n} Runden löschen':
        '删除 {n} 局',
    'Grosser Editor …':
        '大编辑器…',
    'Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle und allen Tasten.':
        '在单独的窗口中打开片段，带打码、每个声源的音量和所有快捷键。',
    'Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton.':
        'Discord 语音聊天 – OBS 音轨 3。关闭 = 片段中没有 Discord 声音。',
    'Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird).':
        '你的麦克风 – OBS 音轨 4（仅当 OBS 录制它时）。',
    'Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen).':
        '此声源在片段中的音量（100 % = 与录制时相同）。',
    'Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen).':
        '只有一条音轨。如需混音，OBS 需用音轨 1–4 录制（设置 → 录像）。',
    'ohne Ton':
        '无声音',
    'Ton neu gemischt':
        '声音已重新混音',
    'Clip speichern':
        '保存片段',
    'Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen.':
        '将剪辑保存为 MP4，放入录像旁边的“Clips”文件夹。',
    'Clips-Ordner öffnen':
        '打开片段文件夹',
    'Öffnet den Ordner „Clips“ im Explorer.':
        '在资源管理器中打开“Clips”文件夹。',
    'Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau.':
        '文件无法读取或缺少 ffmpeg，无法预览。',
    'Clips-Ordner nicht anlegbar: {error}':
        '无法创建片段文件夹：{error}',
    'Schreibe {file} …':
        '正在写入 {file}…',
    'Clip gespeichert: {file}':
        '片段已保存：{file}',
    'Clip nicht gespeichert: {why}':
        '片段未保存：{why}',
    '(Sofort-Clip)':
        '（即时片段）',
    'Aufnahme schon am Ladebildschirm starten':
        '在加载界面开始录制',
    'Aufnahme-Laufwerk nicht angeschlossen':
        '录像驱动器未连接',
    'Clip':
        '片段',
    'DBD':
        'DBD',
    'Discord':
        'Discord',
    'F8 speichert die letzten Sekunden als Sofort-Clip':
        'F8 将最后几秒保存为即时片段',
    'Kein Sofort-Clip: {why}':
        '没有即时片段：{why}',
    'Ladebildschirm vorbei – das Match beginnt.':
        '加载界面结束，对局开始。',
    'Mikrofon':
        '麦克风',
    'Spiel':
        '游戏',
    'Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner':
        '录制中：自加载界面结束起，正在等待地图横幅',
    'Nimmt die Runde auf (seit dem Ladebildschirm)':
        '正在录制对局（自加载界面起）',
    'OBS hat den Puffer nicht gespeichert':
        'OBS 未保存缓存',
    'Sofort-Clip gespeichert ({n} s): {file}':
        '即时片段已保存（{n} 秒）：{file}',
    'Ton in OBS einstellen, sobald DBD startet:':
        'DBD 启动后立即在 OBS 中设置声音：',
    'Ton in OBS nicht eingestellt: {error}':
        '未在 OBS 中设置声音：{error}',
    'OBS bereit – Runden werden aufgenommen. {problem}':
        'OBS 已就绪，对局会被录制。{problem}',
    'Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)':
        '为了在片段编辑器中混音，在 OBS 中：设置 → 输出 → 输出模式“高级” → “录像”选项卡 → 勾选音轨 1 到 5（1 全部，2 游戏，3 Discord，4 麦克风，5 背景）',
    'Jede Tonquelle auf eine eigene OBS-Tonspur':
        '每个声源各占一条 OBS 音轨',
    'Dafür in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken. Das Programm prüft das beim DBD-Start und meldet es im Kasten „Aufnahmen mit OBS“; es ändert nichts am OBS-Profil.':
        '为此需在 OBS 中：设置 → 输出 → 输出模式“高级” → “录像”选项卡 → 勾选音轨 1 到 5。程序会在 DBD 启动时检查这一点，并在“用 OBS 录像”卡片中报告；它不会更改 OBS 配置文件中的任何内容。',
    'Sofort-Clip (F8) mit Ton von:':
        '即时片段（F8）的声音来自：',
    'Wie bei Medal: Das Programm weist in OBS jede Tonquelle der Spur 1 (alles – spielt in jedem Player) und ihrer eigenen Spur zu: nur DBD 2, Discord 3, Mikrofon 4, alle anderen Tonquellen in OBS (z. B. Spotify, Browser) 5 = Hintergrund. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt deshalb nur auf Spur 1. Im Clip-Editor schaltest du jede Quelle an oder aus und regelst ihre Lautstärke; beim Speichern mischt ffmpeg sie zusammen. OBS schreibt die Spuren nur im Ausgabemodus „Erweitert“ mit Audiospur 1 bis 5 angehakt (MKV oder MP4, nicht FLV); das Programm prüft das beim DBD-Start und meldet es, ändert aber nichts am OBS-Profil. Aus = Spuren bleiben, wie sie in OBS stehen.':
        '与 Medal 类似：程序将 OBS 中的每个声源分配到音轨 1（全部，任何播放器都能播放）以及它自己的音轨：仅 DBD 为 2，Discord 为 3，麦克风为 4，OBS 中的其他声源（例如 Spotify、浏览器）为 5 = 背景。Windows 的桌面音频也包含 DBD 和 Discord，因此只在音轨 1 上。在片段编辑器中可以开关每个声源并设置其音量；保存时由 ffmpeg 混音。OBS 只有在输出模式“高级”且勾选了音轨 1 到 5 时才会写入这些音轨（MKV 或 MP4，不能是 FLV）；程序在 DBD 启动时检查并报告这一点，但不会更改 OBS 配置文件中的任何内容。关闭 = 音轨保持 OBS 中的设置。',
    'Nur der Ton von DBD im Sofort-Clip.':
        '即时片段中只有 DBD 的声音。',
    'Ton von Discord (Sprachchat) in der Aufnahme bzw. im Sofort-Clip.':
        '录像或即时片段中包含 Discord（语音聊天）的声音。',
    'Dein Mikrofon – die Quelle „Mikrofon/AUX“ in OBS bzw. seine Spur im Sofort-Clip.':
        '你的麦克风 – OBS 中的“麦克风/辅助”源，或即时片段中的对应音轨。',
    'Hintergrund':
        '背景',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.':
        '在 OBS 中有自己声源的其他程序（例如 Spotify、浏览器） – OBS 音轨 5。Windows 的桌面音频也包含 DBD 和 Discord，只在音轨 1 上。',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) im Sofort-Clip – OBS-Spur 5.':
        '即时片段中，在 OBS 中有自己声源的其他程序（例如 Spotify、浏览器）的声音 – OBS 音轨 5。',
    'Tonquelle angelegt: {name}':
        '已创建声源：{name}',
    'Farming-Aufnahmen löschen nach':
        '刷分录像删除时间',
    'nie':
        '从不',
    '{n} Tagen':
        '{n} 天',
    'Alte Farming-Aufnahmen gelöscht (älter als {days} Tage): {n}':
        '已删除旧的刷分录像（超过 {days} 天）：{n}',
    '{name} – keine Quelle':
        '{name} – 无声源',
    '{name} – in OBS aus':
        '{name} – 在 OBS 中已关闭',
    'In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf Spur 5.':
        'OBS 在此录像中没有背景声源。对于 Spotify、浏览器等，请在 OBS 中为每个程序添加一个应用程序音频采集，程序会将其放到音轨 5。',
    'Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen ausgeschaltet.':
        '录制时，此声源已在“设置 → 录像”中关闭。',
    'Tonquelle {name} hört jetzt auf {exe}':
        '声源 {name} 现在采集 {exe}',
    'Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}':
        '在音轨 5（背景）上，而非与游戏/Discord/麦克风一起：{names}',
    'Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.':
        '整个录像中音轨 {n} 上听不到任何声音。',
    'Tonquelle zur Szene „{scene}“ hinzugefügt: {name}':
        '已将声源添加到场景“{scene}”：{name}',
    'Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        '已在场景“{scene}”中重新显示声源：{name}',
    '{name} (Spur {n})':
        '{name}（音轨 {n}）',
    'Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.':
        '此录像中无声：{names}，OBS 在这些音轨上没有录到任何内容。请在 OBS 中检查：声源在正在录制的场景中、未静音、已勾选音轨。',
    '{name} – still':
        '{name} – 无声',
    'Nur der Ton von Dead by Daylight – OBS-Spur 2.':
        '只有 Dead by Daylight 的声音 – OBS 音轨 2。',
    'Unbekannte Map':
        '未知地图',
    'Wiederholungspuffer in OBS läuft nicht':
        'OBS 的回放缓存未运行',
    'Übriger Desktop-Ton':
        '其他桌面声音',
    'Das Map-Banner kommt erst einige Sekunden nach dem Spawn. Mit diesem Häkchen startet OBS schon, wenn der Ladebildschirm nach der Lobby endet – ohne Lobby, mit Spawn. Das Banner benennt die Aufnahme danach. Kommt 3 Minuten lang kein Banner, endet die Aufnahme und heisst „Unbekannte Map“.':
        '地图横幅在出生几秒后才出现。勾选此框后，大厅之后的加载界面一结束 OBS 就开始录制，不含大厅，包含出生画面。之后由横幅为录像命名。如果 3 分钟内没有横幅，录制结束并命名为“未知地图”。',
    'F8 sichert den Wiederholungspuffer von OBS und legt die letzten Sekunden als MP4 in den Ordner „Clips“ – Bild ohne Neukodierung, in Sekunden. Spur 1 ist die unten gewählte Tonmischung (spielt überall), dahinter liegen die Einzelspuren des Puffers für den Clip-Editor. Der Wiederholungspuffer muss in OBS eingerichtet sein. Die Marke in der Rundenaufnahme setzt F8 weiterhin.':
        'F8 保存 OBS 的回放缓存，并将其最后几秒作为 MP4 放入“Clips”文件夹，画面不重新编码，几秒钟即可完成。音轨 1 是下面选择的混音（在任何地方都能播放），其后是缓存自身的音轨，供片段编辑器使用。回放缓存需要在 OBS 中设置。F8 仍会在对局录像中设置标记。',
    'Das Programm legt in der aktuellen OBS-Szene je eine Anwendungs-Audioaufnahme für DBD und Discord an (einmalig) und schaltet die Tonquellen wie gewählt stumm oder laut – beim Start von DBD und bei jeder Änderung hier, auch mitten in der Runde. Aufnehmen tut OBS, das Programm fasst DBD nicht an. Braucht OBS 28 oder neuer.':
        '程序在当前 OBS 场景中为 DBD 和 Discord 各创建一个应用程序音频采集（一次），并根据选择将声源静音或取消静音，在 DBD 启动时以及此处每次更改时（对局中途也会）。采集由 OBS 完成，程序不接触 DBD。需要 OBS 28 或更新版本。',
    'Ton des Spiels in der Aufnahme.':
        '录像中的游戏声音。',
    'Alles andere, was am PC zu hören ist (Musik, Browser, Systemtöne) – die Quelle „Desktop-Audio“ in OBS.':
        '你在电脑上听到的其他所有声音（音乐、浏览器、系统声音） – OBS 的“桌面音频”源。',
    'Als Farming markieren':
        '标记为刷分',
    'Grund':
        '原因',
    'Ist Farming':
        '是刷分',
    'Kein Farming':
        '不是刷分',
    'Alle als Farming':
        '全部设为刷分',
    'Alle ignorieren':
        '全部忽略',
    'Custom Game, laut Stats-Seite öffentlich':
        '自定义对局，统计页面上为公开比赛',
    'kurze Serie, gleicher Gegner':
        '短时间对局，同一对手',
    '{n} Runden bleiben normale Runden (kein Farming).':
        '{n} 局保持为普通对局（不是刷分）。',
    'Markiert alle Runden der Liste als Farming-Runden (mit Rückfrage) – wie „Ist Farming“ für jede.':
        '将列表中的每一局标记为刷分对局（会先询问），相当于对每一局点击“是刷分”。',
    'Keine der Runden der Liste mehr vorschlagen – sie bleiben, wie sie sind.':
        '不再建议列表中的任何对局，它们保持原样。',
    'Die markierten Runden der Liste sind Farming-Runden (und kein Custom Game mehr); ihre Aufnahmen wandern in den Ordner „Farming“. Zurück: „Farming an/aus“ unter „Letzte Runden“.':
        '列表中标记的对局是刷分对局（不再是自定义对局）；它们的录像会移到“Farming”文件夹。撤回：在“最近对局”下使用“刷分开/关”。',
    'Die markierten Runden der Liste sind normale Runden – sie bleiben, wie sie sind, und werden nie wieder vorgeschlagen.':
        '列表中标记的对局是普通对局，它们保持原样，且不再被建议。',
    'Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB.':
        'Discord：无 Nitro 10 MB，Nitro Basic 50 MB，Nitro 500 MB。',
    'Format':
        '格式',
    'Für Discord (passt unter die Zielgrösse)':
        '适用于 Discord（不超过目标大小）',
    'Gespeichert: {file} ({mb} MB)':
        '已保存：{file}（{mb} MB）',
    'Ignorieren':
        '忽略',
    'Runden nicht geändert: {error}':
        '对局未更改：{error}',
    'Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück.':
        '只播放片段本身，然后跳回其开头。',
    'Zeigt den zuletzt gespeicherten Clip im Explorer.':
        '在资源管理器中显示上次保存的片段。',
    '{n} Runden als Farming markiert.':
        '已将 {n} 局标记为刷分。',
    '{n} Runden als Farming-Runden markieren?':
        '要将 {n} 局标记为刷分对局吗？',
    '{n} Runden sehen nach Farming aus: {reasons}. Zuletzt: {map}, {when}.':
        '{n} 局看起来像刷分：{reasons}。最近一局：{map}，{when}。',
    '{n} als Custom Game gespeichert, laut Stats-Seite aber öffentliche Matches (vor 1.5.5 so erkannt)':
        '{n} 局保存为自定义对局，但在统计页面上是公开比赛（1.5.5 之前是这样读取的）',
    '{n} kurze Runden (bis 3 min) hintereinander gegen denselben Charakter':
        '{n} 局连续对同一人物的短对局（最多 3 分钟）',
    'Farming?':
        '刷分？',
    'Runden sehen nach Farming aus':
        '局看起来像刷分',
    'Farming prüfen …':
        '检查刷分…',
    'Öffnet die Statistik-Übersicht mit der Zeile, die sagt, warum diese Runden nach Farming aussehen – dort markieren oder ignorieren.':
        '打开统计概览，其中有一行说明这些对局为何看起来像刷分，可在那里标记或忽略它们。',
    'etwa {mb} MB':
        '约 {mb} MB',
    'wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB':
        '将变为 {h}p {fps} fps，≈ {kbps} kbit/s，小于 {mb} MB',
    '≤ {n} MB':
        '≤ {n} MB',
    '▶ Clip ansehen':
        '▶ 观看片段',
    'Markiert alle genannten Runden als Farming-Runden (und nicht mehr als Custom Game); ihre Aufnahmen wandern in den Ordner „Farming“. Einzeln zurück: „Farming an/aus“ unter „Letzte Runden“.':
        '将所有这些对局标记为刷分对局（不再是自定义对局）；它们的录像会移入“Farming”文件夹。逐个撤回：在“最近对局”下使用“刷分开/关”。',
    'Diese Runden nicht mehr vorschlagen – sie bleiben, wie sie sind.':
        '不再建议这些对局，它们保持原样。',
    'Alle':
        '全部',
    'BP/h':
        '血点/时',
    'BP/h mit Wartezeit':
        '血点/时（含等待）',
    'Bloodpoints':
        '血点',
    'Bloodpoints laut Stats-Seite. BP/h = je Stunde im Match; mit Wartezeit = je Stunde aus Match und Suche zusammen. Was das Farmen allein bringt, steht im Reiter „Farming“; „Farming ausblenden“ rechnet hier ohne Farming-Runden.':
        '来自统计页面的血点。血点/时 = 对局中每小时；含等待 = 对局和匹配合计每小时。仅刷分获得的血点见“刷分”选项卡；“隐藏刷分”会在此处排除刷分对局。',
    'Bloodpoints pro Stunde':
        '每小时血点',
    'Summe':
        '总计',
    'mit Wartezeit {bp}':
        '含等待 {bp}',
    'Rekorde':
        '记录',
    'Serien zählen Runden mit Ergebnis laut Stats-Seite in zeitlicher Reihenfolge – „aktuell“ ist die Serie der neuesten Runden der Auswahl. Beste Woche ab {n} Runden mit Ergebnis. Eine Sitzung endet nach 45 Minuten ohne Runde.':
        '连胜按时间顺序统计带统计页面结果的对局，“当前”是所选范围内最新对局的连胜。最佳周至少需要 {n} 局有结果的对局。45 分钟内没有对局即视为一次游戏结束。',
    'Noch keine Runden in dieser Auswahl.':
        '此筛选范围内还没有对局。',
    'aktuell {n}':
        '当前 {n}',
    'zuletzt {date}':
        '最近 {date}',
    '4K-Serie':
        '4 杀连胜',
    'Ø {kills} Kills · {n} Runden als {killer}':
        '平均 {kills} 击杀 · 作为 {killer} {n} 局',
    '{share} entkommen · {n} Runden gegen {killer}':
        '{share} 逃脱 · 对阵 {killer} {n} 局',
    '4K-Serie {n}':
        '4 杀连胜 {n}',
    'Entkommen-Serie {n}':
        '逃脱连胜 {n}',
    'Entkommen-Serie':
        '逃脱连胜',
    'Beste Woche als Killer':
        '杀手最佳周',
    'ab {date} · {n} Runden':
        '从 {date} 起 · {n} 局',
    'ab {n} Killer-Runden in einer Woche':
        '一周内至少 {n} 局杀手对局',
    'Beste Woche als Survivor':
        '幸存者最佳周',
    'ab {n} Survivor-Runden in einer Woche':
        '一周内至少 {n} 局幸存者对局',
    'Meiste Runden an einem Tag':
        '单日最多对局',
    'Längste Sitzung':
        '最长游戏时段',
    'Längste Runde':
        '最长对局',
    'Spielstatus in Discord anzeigen (Rich Presence)':
        '在 Discord 中显示游戏状态（Rich Presence）',
    'Application-ID':
        '应用程序 ID',
    'Discord testen':
        '测试 Discord',
    'Developer-Portal öffnen':
        '打开开发者门户',
    'Killer in Discord anzeigen':
        '在 Discord 中显示杀手',
    'Auch Lobby, Suche und Menü anzeigen':
        '也显示大厅、匹配和菜单',
    'Zeigt in deinem Discord-Status, was gerade läuft: „Nurse auf Coal Tower“ mit Rundenzeit, in der Lobby „Sucht ein Match“. Discord braucht dafür eine Application-ID: im Developer-Portal „New Application“ anlegen (als Name z. B. „Dead by Daylight“ – so steht es im Status), die Application-ID kopieren und hier eintragen. Das Programm spricht nur mit dem Discord-Client auf diesem PC (lokale Pipe), ohne ID wird nichts gesendet; Discord erfährt nur Map, Rolle, Killer und die Startzeit.':
        '在你的 Discord 状态中显示当前情况：例如“Nurse 在 Coal Tower”及对局时间，在大厅中显示“正在匹配对局”。为此 Discord 需要一个应用程序 ID：在开发者门户中创建“New Application”（例如命名为“Dead by Daylight”，状态中显示的就是这个名称），复制其 Application ID 并在此输入。程序只与这台电脑上的 Discord 客户端通信（本地管道）；没有 ID 就不发送任何内容；Discord 只会得知地图、角色、杀手和开始时间。',
    'Verbinde mit Discord …':
        '正在连接 Discord…',
    'Discord nicht gefunden – läuft es?':
        '未找到 Discord，它在运行吗？',
    'Killer · {killer}':
        '杀手 · {killer}',
    'Im Match':
        '对局中',
    'Sucht ein Match':
        '正在匹配对局',
    'In der Lobby':
        '在大厅中',
    'Bereit machen':
        '正在准备',
    'Im Menü':
        '在菜单中',
    'Discord: aus':
        'Discord：关闭',
    'Discord: Fehler – {error}':
        'Discord：错误 – {error}',
    'Application-ID fehlt – im Developer-Portal anlegen und hier eintragen.':
        '缺少应用程序 ID，请在开发者门户中创建并在此输入。',
    'Ungültige Application-ID ({error})':
        '应用程序 ID 无效（{error}）',
    'Discord: verbunden':
        'Discord：已连接',
    'Als Killer steht dein Killer im Status („Killer · The Nurse“); aus = nur „Killer“.':
        '作为杀手时，状态中会显示你的杀手（“杀手 · The Nurse”）；关闭 = 只显示“杀手”。',
    'Aus = der Status erscheint nur während einer Runde; sonst auch „Sucht ein Match“, „In der Lobby“ und „Im Menü“, solange DBD läuft.':
        '关闭 = 状态只在对局中显示；否则 DBD 运行时还会显示“正在匹配对局”“在大厅中”和“在菜单中”。',
    'Dein Discord-Status zeigt Map, Rolle, Killer und die Rundenzeit (in der Lobby: Suche/Lobby). Braucht eine Application-ID aus dem Discord-Developer-Portal; das Programm spricht nur mit dem Discord-Client auf diesem PC.':
        '你的 Discord 状态会显示地图、角色、杀手和对局时间（在大厅中：匹配/大厅）。需要 Discord 开发者门户中的应用程序 ID；程序只与这台电脑上的 Discord 客户端通信。',
    'Verbindet sich einmal mit dem laufenden Discord und zeigt, ob die Application-ID angenommen wird.':
        '连接一次正在运行的 Discord，显示应用程序 ID 是否被接受。',
    'Öffnet discord.com/developers im Browser: „New Application“ anlegen (Name z. B. „Dead by Daylight“), die Application-ID kopieren und links eintragen.':
        '在浏览器中打开 discord.com/developers：创建“New Application”（例如命名为“Dead by Daylight”），复制其 Application ID 并在左侧输入。',
    'Ø pro Runde':
        '每局平均',
    'BP/h im Match':
        '对局中血点/时',
    'Spielzeit laut Stats-Seite':
        '来自统计页面的游戏时长',
    'Match und Suche zusammen':
        '对局和匹配合计',
    'Beste Runde':
        '最佳对局',
    'Ø BP als Killer':
        '杀手平均血点',
    'Ø BP als Survivor':
        '幸存者平均血点',
    '{when}: Ø {bp} BP · {n} Runden · Summe {sum}':
        '{when}：平均 {bp} 血点 · {n} 局 · 总计 {sum}',
    'Ø Bloodpoints pro Runde {per}':
        '每局平均血点{per}',
    'Keine Runden mit Bloodpoints in dieser Auswahl.':
        '此筛选范围内没有带血点的对局。',
    'Verpixelt':
        '像素化',
    'Verwischt':
        '模糊',
    'Schwarz':
        '黑色',
    'Zensieren':
        '打码',
    'Beim Speichern anwenden':
        '保存时应用',
    'Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das Bild neu kodiert, auch im Format „Schnell“).':
        '保存的片段中这些框会被遮盖（为此会重新编码画面，即使是“快速”格式）。',
    'Kasten zeichnen':
        '绘制框',
    'Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug.':
        '在画面上拖出一个区域；框可以移动，并可通过右下角调整大小。再按一次结束该工具。',
    'Namen links unten':
        '左下角名称',
    'Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        '在 DBD 显示幸存者名称的位置（游戏画面左下角）放置一个框，需要时可移动。',
    'Kasten entfernen':
        '移除框',
    'Entfernt den markierten Kasten (Taste Entf).':
        '移除标记的框（Del 键）。',
    'Alle entfernen':
        '全部移除',
    'Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ lässt dich einen aufziehen.':
        '还没有框。“左下角名称”会在幸存者名称上放一个框，“绘制框”可以让你拖出一个框。',
    '{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.':
        '{n} 个框 – 拖动 = 移动，右下角 = 大小，点击 = 标记。',
    '{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.':
        '已记住 {n} 个框，它们也会应用到下一个片段。',
    'mit Zensur neu kodiert (wie „Genau“)':
        '为打码而重新编码（与“精确”相同）',
    'Retusche (aus der Umgebung übermalt)':
        '修饰（用周围画面覆盖）',
    'Spotify':
        'Spotify',
    '„Als nächstes“ aus Spotify in der Musikkarte zeigen':
        '在音乐卡片上显示 Spotify 的“接下来播放”',
    'Client-ID':
        '客户端 ID',
    'Developer-Dashboard öffnen':
        '打开开发者仪表板',
    'Mit Spotify verbinden':
        '连接 Spotify',
    'Spotify-Verbindung trennen':
        '断开 Spotify',
    'Spotify: öffne die Anmeldung im Browser …':
        'Spotify：正在浏览器中打开登录页面…',
    'YouTube':
        'YouTube',
    'Privat':
        '私享',
    'Nicht gelistet':
        '不公开',
    'Öffentlich':
        '公开',
    'Client-Secret':
        '客户端密钥',
    'Sichtbarkeit':
        '可见性',
    'Clips automatisch auf YouTube hochladen':
        '自动将片段上传到 YouTube',
    'Google Cloud Console öffnen':
        '打开 Google Cloud 控制台',
    'Client-Datei laden …':
        '加载客户端文件…',
    'Client-Datei laden':
        '加载客户端文件',
    'Client-Datei von Google laden':
        '加载 Google 的客户端文件',
    'Das ist keine Client-Datei von Google ({error}).':
        '这不是 Google 的客户端文件（{error}）。',
    'YouTube: Client-ID und Client-Secret aus {file} übernommen – jetzt „Mit YouTube verbinden“ klicken.':
        'YouTube：已从 {file} 读取客户端 ID 和客户端密钥，现在请点击“连接 YouTube”。',
    'YouTube: Client-Daten aus {file} übernommen.':
        'YouTube：已从 {file} 读取客户端数据。',
    'Datei zu gross':
        '文件过大',
    'nicht lesbar: {error}':
        '无法读取：{error}',
    'kein JSON: {error}':
        '不是 JSON：{error}',
    'kein JSON-Objekt':
        '不是 JSON 对象',
    'OAuth-Client vom Typ „Webanwendung“ – in der Cloud Console einen vom Typ „Desktop-App“ anlegen':
        'OAuth 客户端类型为“Web application”，请在 Cloud 控制台中创建“Desktop app”类型的客户端',
    'kein Abschnitt „installed“':
        '没有“installed”部分',
    'Client-ID fehlt oder endet nicht auf .apps.googleusercontent.com':
        '缺少客户端 ID，或其不以 .apps.googleusercontent.com 结尾',
    'Client-Secret fehlt':
        '缺少客户端密钥',
    'Mit YouTube verbinden':
        '连接 YouTube',
    'YouTube-Verbindung trennen':
        '断开 YouTube',
    'Auf YouTube hochladen':
        '上传到 YouTube',
    'YouTube-Link kopieren':
        '复制 YouTube 链接',
    'Auf YouTube öffnen':
        '在 YouTube 上打开',
    'YouTube: Client-ID (…apps.googleusercontent.com) und Client-Secret eintragen.':
        'YouTube：请输入客户端 ID（…apps.googleusercontent.com）和客户端密钥。',
    'YouTube: öffne die Anmeldung im Browser …':
        'YouTube：正在浏览器中打开登录页面…',
    'Hochgeladen: {file}':
        '已上传：{file}',
    'YouTube: nicht hochgeladen – {file}: {why}':
        'YouTube：未上传 – {file}：{why}',
    'YouTube: in die Warteschlange – {file}':
        'YouTube：已加入队列 – {file}',
    'YouTube-Link kopiert: {url}':
        '已复制 YouTube 链接：{url}',
    'Clip: {what}':
        '片段：{what}',
    'Dauer {d}':
        '时长 {d}',
    'Aufgenommen mit Fog Scout':
        '用 Fog Scout 录制',
    'keine Upload-Sitzung erhalten':
        '未收到上传会话',
    'Antwort ohne Video-ID':
        '回复中没有视频 ID',
    'nicht angemeldet':
        '未登录',
    'Datei nicht gefunden':
        '未找到文件',
    'Aufnahmeordner nicht da':
        '录像文件夹不存在',
    'YouTube: aus':
        'YouTube：关闭',
    'YouTube: nicht verbunden – „Mit YouTube verbinden“ klicken.':
        'YouTube：未连接，请点击“连接 YouTube”。',
    'Mit YouTube verbunden – du kannst dieses Fenster schliessen.':
        '已连接 YouTube，你可以关闭此窗口。',
    'Google hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Google 拒绝了登录，你可以关闭此窗口。',
    'YouTube: Anmeldung nicht möglich – {error}':
        'YouTube：无法登录 – {error}',
    'YouTube: Browser nicht geöffnet – {error}':
        'YouTube：未打开浏览器 – {error}',
    'YouTube: Anmeldung abgelehnt ({error})':
        'YouTube：登录被拒绝（{error}）',
    'YouTube: Google gab kein dauerhaftes Token – in der Cloud Console den OAuth-Client als „Desktop“ anlegen und den Zustimmungsbildschirm veröffentlichen.':
        'YouTube：Google 未提供长期令牌，请在 Cloud 控制台中将 OAuth 客户端创建为“Desktop app”，并发布同意屏幕。',
    'YouTube: verbunden':
        'YouTube：已连接',
    'YouTube: Anmeldung abgelaufen – noch einmal „Mit YouTube verbinden“ klicken.':
        'YouTube：登录已过期，请再次点击“连接 YouTube”。',
    'YouTube: {n} in der Warteschlange – wartet, bis Lobby und Runde vorbei sind':
        'YouTube：{n} 个在队列中，等待大厅和对局结束',
    'YouTube: {n} in der Warteschlange – Tageskontingent aufgebraucht, weiter ab {when}':
        'YouTube：{n} 个在队列中，每日配额已用完，将于 {when} 继续',
    'YouTube: lädt {file} hoch ({pct} %)':
        'YouTube：正在上传 {file}（{pct} %）',
    'YouTube: hochgeladen – {file}':
        'YouTube：已上传 – {file}',
    'YouTube: {error} – neuer Versuch in {s} s':
        'YouTube：{error}，{s} 秒后重试',
    'YouTube: {n} in der Warteschlange – {why}':
        'YouTube：{n} 个在队列中 – {why}',
    'Uploads in Playlists einsortieren':
        '将上传内容归入播放列表',
    'Playlists laden':
        '加载播放列表',
    'Clips in':
        '片段放入',
    'Runden in':
        '对局放入',
    'YouTube: lade Playlists …':
        'YouTube：正在加载播放列表…',
    'YouTube: zuerst „Uploads in Playlists einsortieren“ anhaken.':
        'YouTube：请先勾选“将上传内容归入播放列表”。',
    'YouTube: {n} Playlists geladen – im Kasten auswählen':
        'YouTube：已加载 {n} 个播放列表，请在框中选择',
    'YouTube: keine Playlists auf dem Kanal – zuerst auf YouTube eine anlegen':
        'YouTube：频道上没有播放列表，请先在 YouTube 上创建一个',
    'YouTube: Playlists nicht geladen – {why}':
        'YouTube：未加载播放列表 – {why}',
    'YouTube: {file} in Playlist „{name}“ einsortiert':
        'YouTube：{file} 已归入播放列表“{name}”',
    'YouTube: {file} hochgeladen, aber nicht in die Playlist – {why}':
        'YouTube：{file} 已上传，但未放入播放列表 – {why}',
    'Berechtigung fehlt – noch einmal „Mit YouTube verbinden“ klicken':
        '缺少权限，请再次点击“连接 YouTube”',
    'YouTube: verbunden – für Playlists einmal neu „Mit YouTube verbinden“ klicken.':
        'YouTube：已连接。如需使用播放列表，请再次点击“连接 YouTube”。',
    'Nach dem Upload kommt jedes Video in die gewählte Playlist – für Clips und Runden getrennt wählbar, beide dürfen dieselbe sein. Braucht bei Google die Berechtigung „YouTube-Konto verwalten“ statt nur „Videos hochladen“: nach dem Anhaken einmal neu „Mit YouTube verbinden“. Das Programm nutzt davon nur Playlists auflisten und Video einsortieren (50 Einheiten je Video; es bleiben sechs Uploads am Tag).':
        '上传后，每个视频都会放入所选的播放列表，片段和对局分开设置，两者也可以相同。需要 Google 的“管理你的 YouTube 账号”权限，而不仅是“上传视频”：勾选后请再次点击“连接 YouTube”。程序仅用它来列出播放列表和将视频归入其中（每个视频 50 个单位；每天仍可上传六次）。',
    'Holt die Liste deiner Playlists von YouTube (1 Einheit) in die beiden Auswahlfelder. Neue Playlists legst du auf YouTube an und lädst die Liste danach neu.':
        '从 YouTube 获取你的播放列表（1 个单位）并填入两个选项。在 YouTube 上创建新播放列表后，请重新加载列表。',
    'YouTube: Fehler – {error}':
        'YouTube：错误 – {error}',
    'Jeder neue Clip (F8 und aus dem Editor) kommt in die Warteschlange und geht auf deinen Kanal, sobald du weder in einer Lobby noch in einer Runde bist – mit der Sichtbarkeit rechts, Standard privat. Runden lädst du nur auf Wunsch hoch (Rechtsklick unter Aufnahmen). Google erlaubt etwa sechs Uploads am Tag, der Rest wartet bis zum nächsten Tag. Die Datei bleibt auf der Platte.':
        '每个新片段（F8 和来自编辑器的）都会加入队列，并在你既不在大厅也不在对局中时上传到你的频道，可见性按右侧设置，默认为私享。对局只在你要求时上传（在“录像”下右键单击）。Google 每天大约允许上传六次，其余的等到第二天。文件保留在磁盘上。',
    'Öffnet die Anmeldedaten der Google Cloud Console im Browser: Projekt anlegen, „YouTube Data API v3“ aktivieren, OAuth-Client „Desktop-App“ erstellen, Client-ID und -Secret hier einfügen.':
        '在浏览器中打开 Google Cloud 控制台的凭据页面：创建项目，启用“YouTube Data API v3”，创建“Desktop app”类型的 OAuth 客户端，将客户端 ID 和密钥粘贴到这里。',
    'Vergisst die Google-Freigabe auf diesem PC; die Warteschlange wartet, bis du dich neu verbindest. In deinem Google-Konto unter Sicherheit → Drittanbieter-Apps lässt sich der Zugriff ebenfalls entfernen.':
        '清除这台电脑上的 Google 授权；队列会等到你重新连接。也可以在你的 Google 账号中“安全性 → 第三方应用”下移除访问权限。',
    'Die markierte Datei in die YouTube-Warteschlange (Sichtbarkeit wie in den Einstellungen, Standard privat). Hochgeladen wird, sobald du weder in einer Lobby noch in einer Runde bist und das Tageskontingent reicht; der Link erscheint danach im Rechtsklick-Menü.':
        '将标记的文件加入 YouTube 队列（可见性按设置，默认私享）。当你既不在大厅也不在对局中且每日配额允许时上传；之后链接会出现在右键菜单中。',
    'Spotify: Client-ID sieht falsch aus – erwartet werden 32 Zeichen aus 0–9 und a–f (Dashboard → deine App → Settings → Basic Information → Client ID).':
        'Spotify：客户端 ID 似乎有误，应为 32 个由 0–9 和 a–f 组成的字符（仪表板 → 你的应用 → Settings → Basic Information → Client ID）。',
    'ALS NÄCHSTES':
        '接下来播放',
    'Unter dem Lied':
        '歌曲下方',
    'Rechts neben dem Lied':
        '歌曲右侧',
    'Als nächstes':
        '接下来播放',
    'Anzahl Titel':
        '显示曲目数',
    'Die Liste kommt aus Spotify – einrichten unter Einstellungen → Verbindungen → Spotify.':
        '该列表来自 Spotify，请在“设置 → 连接 → Spotify”中设置。',
    'Spotify: aus':
        'Spotify：关闭',
    'Spotify: Client-ID fehlt – im Developer-Dashboard anlegen und hier eintragen.':
        'Spotify：缺少客户端 ID，请在开发者仪表板中创建并在此输入。',
    'Spotify: nicht verbunden – „Mit Spotify verbinden“ klicken.':
        'Spotify：未连接，请点击“连接 Spotify”。',
    'Spotify: Anmeldung im Browser offen – dort bei Spotify anmelden und zustimmen …':
        'Spotify：登录页面已在浏览器中打开，请在那里登录 Spotify 并同意…',
    'Spotify: Port {port} ist belegt – Anmeldung nicht möglich.':
        'Spotify：端口 {port} 已被占用，无法登录。',
    'Spotify: Browser konnte nicht geöffnet werden ({error})':
        'Spotify：无法打开浏览器（{error}）',
    'Spotify: Anmeldung fehlgeschlagen ({error})':
        'Spotify：登录失败（{error}）',
    'Spotify: Anmeldung abgelehnt ({error})':
        'Spotify：登录被拒绝（{error}）',
    'Spotify: keine Antwort vom Browser – Anmeldung abgebrochen.':
        'Spotify：浏览器没有响应，登录已取消。',
    'Spotify: verbunden':
        'Spotify：已连接',
    'Spotify: Anmeldung abgelaufen – bitte neu verbinden.':
        'Spotify：登录已过期，请重新连接。',
    'Spotify: kein Zugriff ({error}) – ist dein Spotify-Konto in der Developer-App unter „User Management“ eingetragen?':
        'Spotify：无权访问（{error}），你的 Spotify 账号是否已列在开发者应用的“User Management”中？',
    'Spotify: Fehler – {error}':
        'Spotify：错误 – {error}',
    'Spotify: Kontingent der Developer-App aufgebraucht – „Als nächstes“ pausiert bis {time}.':
        'Spotify：开发者应用的配额已用完，“接下来播放”暂停至 {time}。',
    'keine Antwort mit Token':
        '回复中没有令牌',
    'Mit Spotify verbunden – du kannst dieses Fenster schliessen.':
        '已连接 Spotify，你可以关闭此窗口。',
    'Spotify hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Spotify 拒绝了登录，你可以关闭此窗口。',
    'Die nächsten Titel deiner Spotify-Warteschlange unter oder neben dem laufenden Lied. Braucht eine eigene App im Spotify-Developer-Dashboard (Client-ID) und einmal die Anmeldung im Browser; nur solange Spotify spielt.':
        '在当前歌曲下方或旁边显示 Spotify 队列中的下几首曲目。需要你在 Spotify 开发者仪表板中自己创建一个应用（客户端 ID），并在浏览器中登录一次；仅在 Spotify 播放时有效。',
    'Öffnet developer.spotify.com/dashboard im Browser: „Create app“, Redirect URI wie unten angegeben eintragen, die Client-ID kopieren und links einfügen.':
        '在浏览器中打开 developer.spotify.com/dashboard：点击“Create app”，输入下面给出的重定向 URI，复制客户端 ID 并粘贴到左侧。',
    'Vergisst die Spotify-Freigabe auf diesem PC; die Liste verschwindet. In Spotify selbst lässt sich die App unter Konto → Apps ebenfalls entfernen.':
        '清除这台电脑上的 Spotify 授权；列表将消失。也可以在 Spotify 中“账户 → 应用”下移除该应用。',
    'Alle Arten':
        '所有类型',
    'Art':
        '类型',
    'Clip abspielen':
        '播放片段',
    'Clip im Editor öffnen …':
        '在编辑器中打开片段…',
    'Im Editor öffnen …':
        '在编辑器中打开…',
    'Datei kopieren (zum Einfügen)':
        '复制文件（用于粘贴）',
    'Zur Runde springen':
        '转到对局',
    'Farming-Runde':
        '刷分对局',
    'Datei fehlt: {file}':
        '文件缺失：{file}',
    '{file} kopiert – mit Strg+V z. B. in Discord einfügen.':
        '已复制 {file}，可用 Ctrl+V 粘贴，例如粘贴到 Discord 中。',
    'Die Aufnahme dieser Runde gibt es nicht mehr.':
        '此对局的录像已不存在。',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start.':
        '缺少 ffmpeg（imageio-ffmpeg 包），start.bat 会在下次启动时安装它。',
    'Öffnet den markierten Clip (auch Sofort-Clips von F8) im Clip-Editor: kürzen, zensieren, Ton mischen. Gespeichert wird ein neuer Clip, der alte bleibt.':
        '在片段编辑器中打开标记的片段（F8 即时片段也可以）：裁剪、打码、混音。会保存为新片段，旧片段保留。',
    'Clip fehlt: {file}':
        '片段缺失：{file}',
    'Keine Videodatei: {file}':
        '不是视频文件：{file}',
    'Clip gelöscht: {file}':
        '片段已删除：{file}',
    'Clip im Explorer zeigen':
        '在资源管理器中显示片段',
    'Clip löschen':
        '删除片段',
    'Clip nicht gelöscht ({error}): {file}':
        '片段未删除（{error}）：{file}',
    'Kein Aufnahmeordner – die Clips liegen in seinem Ordner „Clips“.':
        '没有录像文件夹，片段保存在其“Clips”文件夹中。',
    'Länge':
        '时长',
    'Noch keine Clips – „Clip bearbeiten …“ bei einer Runde oder F8 im Spiel.':
        '还没有片段：对某一局使用“编辑片段…”，或在游戏中按 F8。',
    'Sofort-Clip':
        '即时片段',
    'Sofort-Clips (F8)':
        '即时片段（F8）',
    'Standbild':
        '静帧',
    'Standbilder':
        '静帧',
    '{n} von {total} Clips':
        '{n}/{total} 个片段',
    'Spielt den markierten Clip im Standard-Player von Windows ab.':
        '用 Windows 默认播放器播放标记的片段。',
    'Öffnet den Explorer mit dem markierten Clip.':
        '打开资源管理器并选中标记的片段。',
    'Löscht den markierten Clip von der Platte – nach Rückfrage. Nur Dateien, die das Programm selbst angelegt hat.':
        '从驱动器中删除标记的片段，会先询问。仅限程序自己生成的文件。',
    'Öffnet den Ordner „Clips“ neben den Aufnahmen im Explorer.':
        '在资源管理器中打开录像旁边的“Clips”文件夹。',
    'Clips':
        '片段',
    'Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '黑边中的灰线 = 边界（关闭），拖动其中一条即可开启',
    'mit kurzer Meldung':
        '带简短通知',
    'Clip wird gespeichert …':
        '正在保存片段…',
    'Die letzten {n} s aus dem Puffer von OBS':
        'OBS 缓存中的最后 {n} 秒',
    'Clip gespeichert ✓':
        '片段已保存 ✓',
    '{n} s · im Tab Aufnahmen → Clips':
        '{n} 秒 · 位于“录像 → 片段”选项卡',
    'Kein Clip':
        '没有片段',
    'Zeigt beim Sofort-Clip (F8) unten rechts ein kleines Hinweisfenster – „Clip wird gespeichert …“ und danach „Clip gespeichert“ bzw. warum nicht. Auch im Spiel, ohne Ton; nimmt nie den Fokus.':
        '为即时片段（F8）在右下角显示一个小通知窗口：“正在保存片段…”，然后是“片段已保存”或失败原因。在游戏中也会显示，没有声音；从不抢占焦点。',
    'Grenzen oben und unten in den schwarzen Balken':
        '黑边顶部和底部的边界',
    'Grenzen zurücksetzen':
        '重置边界',
    'Links und rechts gleich':
        '左右相同',
    'In jedem schwarzen Balken (links und rechts) eine Linie oben und eine unten: Karte, Systemwerte, Heute und Musik bleiben dazwischen – z. B. frei für eine FPS-Anzeige oder Benachrichtigungen. Die Karte wird bei Bedarf kleiner.':
        '每条黑边（左侧和右侧）顶部和底部各有一条线：地图、系统数值、今日和音乐都保持在两线之间，例如为 FPS 计数器或通知留出空间。需要时地图会缩小。',
    'Eine Linie ziehen bewegt die gleiche Linie im anderen Balken mit.':
        '拖动一条线时，另一条黑边中的同一条线会一起移动。',
    'Setzt alle vier Linien auf 8 % vom Rand zurück.':
        '将四条线都恢复到距边缘 8 % 的位置。',
    'Dunkelgrauer Boden mit hellem Rand – gilt auch im Spiel.':
        '深灰色底面，带浅色边缘，在游戏中也一样。',
    'Dunkelgrauer Boden – die Form der Map bleibt auf dem schwarzen Balken sichtbar. Gilt auch im Spiel.':
        '深灰色底面，地图形状在黑边上保持可见。在游戏中也一样。',
    'Dunkles Lila mit lila Rand, erinnert an die Originalfarbe – gilt auch im Spiel.':
        '深丁香紫色，带丁香紫色边缘，接近原始颜色，在游戏中也一样。',
    'Durchsichtiger Boden mit dunklem Rand – gilt auch im Spiel.':
        '透明底面，带深色边缘，在游戏中也一样。',
    'Grau':
        '灰色',
    'Grau mit Rand':
        '灰色带边缘',
    'Lila dunkel':
        '深丁香紫',
    'Lila transparent':
        '丁香紫透明',
    'Lila Boden, halb durchsichtig – gilt auch im Spiel.':
        '丁香紫底面，半透明，在游戏中也一样。',
    'Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe unsichtbar.':
        '重要：在 DBD 的“设置 → 图像”中将显示模式选择为“窗口化全屏”。在独占全屏模式下，Windows 无法在游戏上方显示窗口，地图将不可见。',
    'Ungültiger Servername im Auftrag: {name}':
        '任务中的服务器名称无效：{name}',
    'Die hosts-Datei wurde direkt nach dem Schreiben wieder verändert (Virenschutz oder ein anderes Programm?).':
        'hosts 文件在写入后立即又被更改（杀毒软件或其他程序？）。',
    'Keine Schreibrechte auf die hosts-Datei (Administratorrechte?).':
        '没有写入 hosts 文件的权限（管理员权限？）。',
    'Aufbau der Match-Daten speichern':
        '保存比赛数据的结构',
    'Öffnet die Stats-Seite so, dass das Userscript einmal den Aufbau ihrer Match-Daten im Download-Ordner speichert: nur Feldnamen und Arten, keine Werte. Damit lässt sich entscheiden, welche Daten das Programm zusätzlich auswerten könnte.':
        '打开统计页面，让用户脚本将其比赛数据的结构在下载文件夹中保存一次：只有字段名和类型，没有数值。这能显示程序还可以使用哪些数据。',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) legt danach „{file}“ in den Download-Ordner: nur die Namen und Arten der Felder, die die Seite liefert – keine Werte, keine Namen, keine IDs. Das Programm liest diese Datei nicht; du kannst sie weitergeben, um zu entscheiden, welche Felder zusätzlich übernommen werden sollen. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '统计页面将在浏览器中打开。用户脚本（版本 {n} 或更新）随后会将“{file}”放入下载文件夹：只有页面所发送字段的名称和类型，没有数值、名称或 ID。程序不读取此文件；你可以把它提供出去，以决定还应采用哪些字段。较旧的用户脚本：请先点击“复制用户脚本”并在 Tampermonkey 中替换。',
    'Gegner':
        '对手',
    'Charakter':
        '人物',
    'Begegnungen':
        '遭遇次数',
    'Geopfert':
        '献祭',
    'Getötet':
        '被杀',
    'Aufgegeben':
        '放弃',
    'Laut Stats-Seite: als Killer die Survivor gegen dich und wie ihr Match endete, als Survivor der Killer und wie dein Match endete. „Getötet“ = vom Killer direkt getötet (z. B. Mori), „Aufgegeben“ schließt verlassene Matches ein. „Ø Kills ohne Aufgaben“ zählt nur Matches, in denen kein Survivor aufgab oder ging. „Farming“ = Begegnungen in Farming-Runden, die „Begegnungen“ nicht zählen.':
        '来自统计页面：作为杀手时是与你对局的幸存者及其比赛结局，作为幸存者时是杀手及你的比赛结局。“被杀” = 被杀手直接杀死（例如处决），“放弃”包括中途离开的比赛。“干净平均击杀”只统计没有幸存者放弃或离开的比赛。“刷分” = 刷分对局中的遭遇，“遭遇次数”不包括这些。',
    'Noch keine Runden mit Daten der Stats-Seite in dieser Auswahl.':
        '此筛选范围内还没有带统计页面数据的对局。',
    'Schnellste 4K':
        '最快 4 杀',
    '{n} von {total} Runden':
        '{total} 局中 {n} 局',
    '{n} Survivor':
        '{n} 名幸存者',
    'Ø Kills ohne Aufgaben':
        '干净平均击杀',
    'OBS mit DBD starten, falls es noch nicht läuft':
        'DBD 启动时如果 OBS 尚未运行则启动 OBS',
    'Startet DBD und ist OBS nicht erreichbar, startet das Programm OBS einmal minimiert im Infobereich – nur, wenn kein OBS-Fenster offen ist. OBS bleibt offen, wenn DBD beendet wird. OBS läuft dann mit denselben Rechten wie das Programm (Administrator).':
        'DBD 启动且无法连接 OBS 时，程序会启动一次 OBS，并最小化到通知区域，前提是没有打开任何 OBS 窗口。DBD 关闭时 OBS 保持打开。OBS 将以与程序相同的权限（管理员）运行。',
    'OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS 已启动但无法连接，请在 OBS 的“工具 → WebSocket 服务器设置”中启用服务器并检查端口/密码。（{error}）',
    'OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio).':
        '未找到 OBS，请自行启动 OBS（已在 Program Files\\obs-studio 中查找）。',
    'OBS konnte nicht gestartet werden: {error}':
        '无法启动 OBS：{error}',
    'OBS wird gestartet …':
        '正在启动 OBS…',
    'OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS 已打开但无法连接，请在 OBS 的“工具 → WebSocket 服务器设置”中启用服务器并检查端口/密码。（{error}）',
    'Builds':
        '配装',
    'Build (4 Perks)':
        '配装（4 个技能）',
    'Perk':
        '技能',
    'Add-on':
        '附加品',
    'Opfergabe':
        '祭品',
    'Kraft/Item':
        '能力/道具',
    'ohne':
        '不带',
    'Dein Loadout laut Stats-Seite (ab Userscript Version 3). „Ergebnis“ = als Killer Ø Kills, als Survivor Anteil entkommen; „ohne“ = dasselbe in deinen Runden derselben Rolle ohne diesen Eintrag. Builds ab {n} Runden. Embleme: Ø Stufe von keins (0) bis Iri (4); „voll“ = Kategorie mit {max} Punkten.':
        '来自统计页面的你的配装（用户脚本版本 3 或更新）。“结果” = 作为杀手时为平均击杀，作为幸存者时为逃脱占比；“不带” = 你在该角色下不带此项的对局中的相同数据。配装至少需要 {n} 局。徽章：平均等级，从无（0）到虹彩（4）；“满” = 该类别达到 {max} 分。',
    'Event-Modus':
        '活动模式',
    'keins':
        '无',
    'Bronze':
        '铜',
    'Silber':
        '银',
    'Gold':
        '金',
    'Iri':
        '虹彩',
    'Emblem':
        '徽章',
    'Ø Stufe':
        '平均等级',
    'Punktekategorie':
        '分数类别',
    'Ø Punkte':
        '平均分数',
    'voll':
        '满',
    'Killer-Wertung: {list}':
        '杀手评分：{list}',
    'Noch keine Matches mit Loadout in dieser Auswahl – die Stats-Seite liefert es ab Userscript Version 3 (Einstellungen → Match-Daten → Offizielle Match-Daten → „Userscript kopieren“).':
        '此筛选范围内还没有带配装的比赛。统计页面从用户脚本版本 3 起会发送配装（设置 → 比赛数据 → 官方比赛数据 → “复制用户脚本”）。',
    'Alle Modi':
        '所有模式',
    '„{name}“ nicht mehr als Farming-Gegner':
        '“{name}”不再是刷分伙伴',
    '„{name}“ als Farming-Gegner (Runden mit diesem Charakter zählen als Farming)':
        '将“{name}”设为刷分伙伴（与该人物的对局计为刷分）',
    '„{name}“ gilt jetzt als Farming-Gegner – {n} Runden zählen als Farming (auch ältere; Aufnahmen bleiben, wo sie sind).':
        '“{name}”现在计为刷分伙伴，{n} 局计为刷分（较早的也一样；录像保留在原位置）。',
    '„{name}“ gilt nicht mehr als Farming-Gegner.':
        '“{name}”不再计为刷分伙伴。',
    'Farming-Gegner (Rechtsklick auf einen Charakter im Reiter „Gegner“): {names}':
        '刷分伙伴（在“对手”选项卡中右键单击人物）：{names}',
    'Gegner & Builds':
        '对手和配装',
    'Maps, Server & PC':
        '地图、服务器和电脑',
    'Bloodpoints & Farming':
        '血点和刷分',
    'Aufnahme markieren: abspielen, Clip schneiden, behalten, löschen – oder Rechtsklick.':
        '标记一个录像：播放、剪辑片段、保留、删除，或右键单击。',
    'Clip markieren: abspielen, im Editor öffnen, löschen – oder Rechtsklick.':
        '标记一个片段：播放、在编辑器中打开、删除，或右键单击。',
    'Filter{count}':
        '筛选{count}',
    'Filter zurücksetzen':
        '重置筛选',
    'Alle Filter der Statistik zurück auf „alle“ – Zeitraum, Rolle, Region, Killer, Map, Modus und „Farming ausblenden“.':
        '将统计的所有筛选条件恢复为“全部”：时间段、角色、区域、杀手、地图、模式和“隐藏刷分”。',
    'Region, Killer, Map, Modus und „Farming ausblenden“ ein- oder ausklappen. Die Zahl sagt, wie viele davon gerade filtern.':
        '显示或隐藏区域、杀手、地图、模式和“隐藏刷分”。数字表示当前有几项正在筛选。',
    'Noch keine Runden gespeichert':
        '尚未保存任何对局',
    'Eine Runde zählt vom Map-Banner bis zum Rundenende (ab 1 Minute) und erscheint hier von selbst. Kills, Escapes und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        '从地图横幅到对局结束（1 分钟起）计为一局，并会自动显示在这里。击杀、逃脱和血点来自统计页面，为此需要设置一次比赛数据。',
    'Noch keine Aufnahmen – OBS nimmt ab dem nächsten Map-Banner auf. Runden erscheinen hier, Clips (F8 oder aus dem Editor) im Reiter „Clips“.':
        '还没有录像，OBS 从下一个地图横幅起开始录制。对局显示在这里，片段（F8 或来自编辑器的）显示在“片段”选项卡中。',
    'Runden pro Tag – letzte {n} Tage':
        '每天对局数 – 最近 {n} 天',
    '{when}: {n} Runden ({k} Killer, {s} Survivor)':
        '{when}：{n} 局（{k} 局杀手，{s} 局幸存者）',
    '1 s ab Abspielkopf':
        '从播放头起 1 秒',
    '10 s ab Abspielkopf':
        '从播放头起 10 秒',
    '100 % = unverändert.':
        '100 % = 不变。',
    '3 s ab Abspielkopf':
        '从播放头起 3 秒',
    '5 s ab Abspielkopf':
        '从播放头起 5 秒',
    '9:16 (Hochformat)':
        '9:16（竖屏）',
    'Alle Bilder':
        '所有图片',
    'Alle Zeichnungen entfernen':
        '移除所有绘图',
    'Alles zurücksetzen':
        '全部重置',
    'Anderen Ordner …':
        '其他文件夹…',
    'Aufgenommen (F12)':
        '已截取（F12）',
    'Ausschnitt':
        '裁剪',
    'Ausschnitt {w}×{h}':
        '裁剪 {w}×{h}',
    'Bearbeitet':
        '已编辑',
    'Bearbeitete Bilder öffnen':
        '打开已编辑的图片',
    'Bild bearbeiten – {name}':
        '编辑图片 – {name}',
    'Bild bearbeiten …':
        '编辑图片…',
    'Bild gespeichert: {file}':
        '图片已保存：{file}',
    'Bild im Explorer zeigen':
        '在资源管理器中显示图片',
    'Bild nicht gespeichert: {error}':
        '图片未保存：{error}',
    'Speichert …':
        '正在保存…',
    'Bild nicht lesbar: {error}':
        '无法读取图片：{error}',
    'Bild speichern':
        '保存图片',
    'Der Clip beginnt aus Schwarz und mit leisem Ton.':
        '片段从黑屏开始，声音渐强。',
    'Der Clip endet in Schwarz, der Ton wird leiser.':
        '片段以黑屏结束，声音渐弱。',
    'Dick':
        '粗',
    'Dünn':
        '细',
    'Eigener Ordner':
        '自己的文件夹',
    'Eigener Ordner nicht gefunden: {path}':
        '未找到自己的文件夹：{path}',
    'Einblenden':
        '淡入',
    'Entfernt den markierten Kasten (Entf).':
        '移除标记的框（Del）。',
    'Entfernt die markierte Zeichnung (Entf).':
        '移除标记的绘图（Del）。',
    'Farbe':
        '颜色',
    'Farbe zurücksetzen':
        '重置颜色',
    'Frei':
        '自由',
    'Freihand':
        '手绘',
    'GIF (ohne Ton, für Chats)':
        'GIF（无声音，用于聊天）',
    'GIF {h}p, {fps} Bilder/s, ohne Ton':
        'GIF {h}p，{fps} 帧/秒，无声音',
    'Helligkeit':
        '亮度',
    'Helligkeit, Kontrast und Sättigung auf 100 %.':
        '亮度、对比度和饱和度恢复为 100 %。',
    'Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats).':
        'GIF 的高度，越小文件越小（Discord、聊天）。',
    'Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern.':
        '在图片中拖出一个区域使其无法辨认：名称、聊天、好友列表。框可以移动，并可通过右下角调整大小。',
    'Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt sie, Entf löscht sie.':
        '在图片中拖动（文字：单击）。单击绘图可标记它，拖动可移动它，Del 删除它。',
    'Immer':
        '始终',
    'In Zwischenablage':
        '到剪贴板',
    'In die Zwischenablage kopiert – in Discord mit Strg+V einfügen.':
        '已复制到剪贴板，可在 Discord 中按 Ctrl+V 粘贴。',
    'Ohne schwarze Ränder':
        '去除黑边',
    'Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das Spielbild, „Kein Ausschnitt“ das ganze Bild.':
        '录像带有黑边：“去除黑边”只保存游戏画面，“不裁剪”保存整个画面。',
    'Kein Ausschnitt':
        '不裁剪',
    'Kein Screenshot-Ordner von Steam für DBD gefunden – noch kein F12-Screenshot, oder Steam speichert woanders („Anderen Ordner …“).':
        '未找到 DBD 的 Steam 截图文件夹：还没有用 F12 截图，或 Steam 保存在其他位置（“其他文件夹…”）。',
    'Kontrast':
        '对比度',
    'Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C).':
        '复制编辑后的图片，可在 Discord 中按 Ctrl+V 粘贴（Ctrl+C）。',
    'Kreis':
        '椭圆',
    'Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen':
        'Space 播放 · ←/→ 1 秒 · Shift 5 秒 · Ctrl 1 帧 · I/O 开始/结束 · A 片段 · M 标记 · Home/End 开头/结尾 · Del 移除框/绘图 · Esc 关闭',
    'Letzten Schritt zurücknehmen (Strg+Z).':
        '撤销上一步（Ctrl+Z）。',
    'Linie':
        '直线',
    'Links und rechts tauschen.':
        '左右交换。',
    'Mittel':
        '中',
    'Oben und unten tauschen.':
        '上下交换。',
    'Ordner mit deinen Screenshots':
        '你的截图文件夹',
    'Ordner nicht anlegbar: {error}':
        '无法创建文件夹：{error}',
    'PNG: verlustfrei · JPG: kleinere Datei.':
        'PNG：无损 · JPG：文件更小。',
    'Pfeil':
        '箭头',
    'Rahmen':
        '方框',
    'Rahmen bearbeiten':
        '编辑画框',
    'Rahmen im Bild ziehen, verschieben, an den Ecken ändern.':
        '在图片中拖动画框、移动它，或在角上调整它。',
    'Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. Nochmal drücken beendet das Werkzeug.':
        '在预览中移动画框，或拖动其角放大/缩小。再按一次结束该工具。',
    'Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen.':
        '从图片中裁出一个区域：9:16 用于 YouTube Shorts 和 TikTok，1:1 用于 Instagram。在预览中移动画框并拖动其角。',
    'Screenshots':
        '截图',
    'Sehr dick':
        '很粗',
    'Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den Ecken ziehen.':
        '裁剪的宽高比；在图片中移动画框并拖动其角。',
    'Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im Screenshot-Ordner von Steam) bleibt unverändert (Strg+S).':
        '在 Fog Scout 的文件夹中保存一份编辑后的副本，原图（例如在 Steam 截图文件夹中）保持不变（Ctrl+S）。',
    'Steam (F12)':
        'Steam（F12）',
    'Steam-Ordner verwenden':
        '使用 Steam 的文件夹',
    'Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf Markiertes löschen · Esc schliessen':
        'Ctrl+Z 撤销 · Ctrl+Y 重做 · Ctrl+C 复制 · Ctrl+S 保存 · Del 移除标记项 · Esc 关闭',
    'Strichstärke bzw. Textgrösse.':
        '线宽或文字大小。',
    'Sättigung':
        '饱和度',
    'Tempo':
        '速度',
    'Text':
        '文字',
    'Text für das Text-Werkzeug':
        '文字工具的文字',
    'Um 90° gegen den Uhrzeigersinn drehen.':
        '逆时针旋转 90°。',
    'Um 90° im Uhrzeigersinn drehen.':
        '顺时针旋转 90°。',
    'Verwirft alle Änderungen – das Original bleibt ohnehin unverändert.':
        '放弃所有更改，原图本来就保持不变。',
    'Wie der Bereich unkenntlich wird.':
        '使区域无法辨认的方式。',
    'Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des Abspielkopfs. Gilt für neue und für die markierte Zeichnung.':
        '绘图在片段中显示多长时间，从播放头起算。适用于新绘图和标记的绘图。',
    'Zeichnen':
        '绘图',
    'Zeichnung entfernen':
        '移除绘图',
    'Zeigt das zuletzt gespeicherte Bild im Explorer.':
        '在资源管理器中显示上次保存的图片。',
    'Zurückgenommenen Schritt wiederholen (Strg+Y).':
        '重做已撤销的步骤（Ctrl+Y）。',
    'Zuschneiden':
        '裁剪',
    'neu kodiert (wie „Genau“)':
        '已重新编码（与“精确”相同）',
    'normal':
        '普通',
    '{n} Abschnitt(e), {length} s':
        '{n} 个片段，{length} 秒',
    '{w} × {h} Pixel · Original bleibt unverändert':
        '{w} × {h} 像素 · 原图保持不变',
    '↶ Rückgängig':
        '↶ 撤销',
    '↷ Wiederholen':
        '↷ 重做',
    '⇅ Kippen':
        '⇅ 上下翻转',
    '⇆ Spiegeln':
        '⇆ 镜像',
    '⟲ Links drehen':
        '⟲ 向左旋转',
    '⟳ Rechts drehen':
        '⟳ 向右旋转',
    'Öffnet das markierte Bild im Bild-Editor: zuschneiden, drehen, Pfeile und Text, zensieren, Farbe – gespeichert wird eine Kopie, das Original bleibt.':
        '在图片编辑器中打开标记的图片：裁剪、旋转、箭头和文字、打码、颜色。会保存一份副本，原图保留。',
    'Zeigt die Bilddatei im Explorer.':
        '在资源管理器中显示图片文件。',
    'Öffnet den Ordner mit den bearbeiteten Bildern (Screenshots neben den Aufnahmen bzw. Bilder/Fog Scout).':
        '打开存放已编辑图片的文件夹（录像旁边的 Screenshots，或 图片/Fog Scout）。',
    'Bilder aus einem eigenen Ordner zeigen – z. B. wenn Steam die Screenshots unkomprimiert in einen anderen Ordner speichert.':
        '显示你自己文件夹中的图片，例如 Steam 将未压缩的截图保存到另一个文件夹时。',
    'Wieder die Screenshots aus Steams Ordner für DBD zeigen (F12 im Spiel).':
        '重新显示 Steam 的 DBD 文件夹中的截图（游戏中按 F12）。',
    'Bild anklicken: bearbeiten (zuschneiden, zeichnen, zensieren), im Explorer zeigen – Doppelklick öffnet den Editor.':
        '单击图片：编辑（裁剪、绘图、打码）、在资源管理器中显示；双击打开编辑器。',
    'F12 im Spiel ist Steams Screenshot-Taste; das Programm liest Steams Ordner nur. Bearbeitete Bilder sind Kopien im Ordner „Screenshots“ neben den Aufnahmen.':
        '游戏中的 F12 是 Steam 的截图键；程序只读取 Steam 的文件夹。编辑后的图片是保存在录像旁边“Screenshots”文件夹中的副本。',
    '1 Bild':
        '1 张图片',
    '{n} Bilder':
        '{n} 张图片',
    '★ behalten (nie aufgeräumt) · ⚑ Marken (F8 in der Runde) · ▶ auf YouTube · Rechtsklick auf die Spaltenköpfe: Spalten ein-/ausblenden':
        '★ 已保留（从不清理） · ⚑ 标记（对局中按 F8） · ▶ 已上传到 YouTube · 右键单击列标题：显示/隐藏列',
    'Clips aus dem Editor, Sofort-Clips (F8) und Standbilder, mit ihrer Runde · ▶ auf YouTube · gelöscht werden nur Dateien, die das Programm selbst angelegt hat':
        '来自编辑器的片段、即时片段（F8）和静帧，以及其所属对局 · ▶ 已上传到 YouTube · 只会删除程序自己生成的文件',
    'Status':
        '状态',
    'Schnell (ohne Neukodieren)':
        '快速（不重新编码）',
    'Genau (neu kodiert)':
        '精确（重新编码）',
    'Für Discord (Zielgrösse)':
        '适用于 Discord（目标大小）',
    'GIF (ohne Ton)':
        'GIF（无声音）',
    'Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als Video speichern.':
        'GIF 最长 {limit} 秒，此片段为 {seconds} 秒，请剪短或保存为视频。',
    'beim Beenden abgebrochen':
        '程序退出时已停止',
    'Update gesperrt: ein Clip wird noch gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        '更新已锁定：仍在保存片段。之后请再次点击“更新并重启”。',
    '(gerade {n})':
        '（现在 {n}）',
    'Aufnahme gestartet':
        '录制已开始',
    'Aufnahme läuft weiter':
        '录制已继续',
    'Aufnahme läuft weiter.':
        '录制已继续。',
    'Aufnahme pausieren/weiter':
        '暂停/继续录制',
    'Aufnahme pausiert':
        '录制已暂停',
    'Aufnahme pausiert.':
        '录制已暂停。',
    'Aufnahme starten':
        '开始录制',
    'Aufnahme starten/stoppen':
        '开始/停止录制',
    'Aufnahme stoppen':
        '停止录制',
    'Aufnahme von Hand gestartet.':
        '已手动开始录制。',
    'Aufnahme wird beendet …':
        '正在停止录制…',
    'Aufnahme-Laufwerk fast voll – Aufnahme beendet':
        '录像驱动器几乎已满，录制已停止',
    'Aufnahme-Laufwerk fast voll – nichts gestartet':
        '录像驱动器几乎已满，未开始录制',
    'Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet':
        '录像驱动器未连接，未开始录制',
    'Aufnahmen sind aus.':
        '录像已关闭。',
    'Ausgewogen':
        '均衡',
    'Automatisch':
        '自动',
    'Bereit':
        '就绪',
    'Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert.':
        '片段的画面高度，小于录像时会缩小，绝不会放大。',
    'CPU (x264/x265)':
        'CPU（x264/x265）',
    'Clip speichern (F8)':
        '保存片段（F8）',
    "Der Sofort-Clip (F8) ist auf {clip} s eingestellt, OBS' Wiederholungspuffer hält nur {buf} s – in OBS: Einstellungen → Ausgabe → Wiederholungspuffer → Maximale Wiederholungszeit.":
        '即时片段（F8）设置为 {clip} 秒，但 OBS 的回放缓存只保存 {buf} 秒。在 OBS 中：设置 → 输出 → 回放缓存 → 最长回放时间。',
    'Die Datei erscheint im Tab Aufnahmen':
        '文件会显示在“录像”选项卡中',
    'Es läuft schon eine Aufnahme':
        '已有录制正在进行',
    'H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel kleiner, braucht aber einen neueren Player.':
        'H.264 到处都能播放；HEVC（H.265）在相同画质下约小三分之一，但需要较新的播放器。',
    'Hoch':
        '高',
    'Kein Aufnahmeordner gewählt – Einstellungen → Aufnahmen.':
        '未选择录像文件夹 – 设置 → 录像。',
    'Keine Aufnahme':
        '无录像',
    'Keine Aufnahme läuft':
        '没有正在进行的录制',
    'Keine Aufnahme läuft.':
        '没有正在进行的录制。',
    'Kodiere {file} … ({how}, dauert etwas)':
        '正在编码 {file}…（{how}，需要一点时间）',
    'Kodierung':
        '编码',
    'Marke setzen':
        '设置标记',
    'Nimmt auf':
        '正在录制',
    'Nimmt auf (von Hand gestartet)':
        '正在录制（手动开始）',
    'Nimmt die Runde in der laufenden Aufnahme auf':
        '在正在进行的录制中录制对局',
    'OBS lässt Bilder aus ({n} von {total}, Kodierer überlastet) – in OBS Voreinstellung oder Auflösung senken.':
        'OBS 正在跳帧（{total} 帧中 {n} 帧，编码器过载），请在 OBS 中降低预设或分辨率。',
    'OBS nicht erreichbar':
        '无法连接 OBS',
    'OBS starten, WebSocket-Server einschalten, Port/Passwort prüfen (Einstellungen → Verbindungen → OBS-Verbindung → Verbindung testen). {why}':
        '请启动 OBS，启用其 WebSocket 服务器，检查端口/密码（设置 → 连接 → OBS 连接 → 测试连接）。{why}',
    'OBS verpasst Bilder beim Rendern ({n} von {total}, Grafikkarte ausgelastet).':
        'OBS 渲染时丢帧（{total} 帧中 {n} 帧，显卡繁忙）。',
    'Pause':
        '暂停',
    'Pausiert':
        '已暂停',
    'Schnell':
        '快速',
    'Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. Hoch: grösser, nahe am Original.':
        '快速：更小更快，明显更模糊。均衡：与以前相同。高：更大，接近原画质。',
    'Stoppen mit demselben Hotkey oder im Tab Aufnahmen':
        '用同一快捷键或在“录像”选项卡中停止',
    'Warte auf OBS …':
        '正在等待 OBS…',
    'Wie aufgenommen':
        '与录制时相同',
    'Wiederholungspuffer aus':
        '回放缓存已关闭',
    'Wiederholungspuffer in OBS nicht aktiviert':
        'OBS 中未启用回放缓存',
    'Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; „Automatisch“ nimmt die erste, die geht.':
        '由什么编码片段：显卡（NVENC、AMF、Quick Sync，仅当 ffmpeg 在此确实能使用时）几乎不占用处理器；“自动”会选择第一个可用的。',
    'letzter Clip {file} (vor {age})':
        '上一个片段 {file}（{age}前）',
    'Fortsetzen':
        '继续',
    'von Hand gestartet':
        '手动开始',
    'von OBS selbst gestartet':
        '在 OBS 中开始',
    'Beendet die laufende Aufnahme jetzt (bei einer Runde ohne Nachlauf) und legt sie in den Aufnahmeordner.':
        '立即停止正在进行的录制（对局没有尾段），并将其归档到录像文件夹。',
    'Hält die laufende Aufnahme an (OBS pausiert); „Fortsetzen“ setzt sie in derselben Datei fort. Marken bleiben an ihrer Stelle.':
        '暂停正在进行的录制（OBS 暂停）；“继续”会在同一文件中继续录制。标记保持原位。',
    'Merkt diesen Moment in der laufenden Aufnahme (⚑) – der Clip-Editor springt später dorthin. Ohne Sofort-Clip.':
        '在正在进行的录制中记下此刻（⚑），片段编辑器之后会跳到这里。不生成即时片段。',
    'Setzt die pausierte Aufnahme fort.':
        '继续已暂停的录制。',
    'Startet jetzt eine OBS-Aufnahme von Hand – auch ausserhalb einer Runde. Sie läuft, bis du sie stoppst oder DBD beendet wird; ein Map-Banner benennt sie. Hotkey einstellbar.':
        '立即手动开始 OBS 录制，在对局之外也可以。它会一直运行，直到你停止它或 DBD 关闭；地图横幅会为它命名。快捷键可配置。',
    'Wie F8: speichert die letzten Sekunden aus dem OBS-Wiederholungspuffer als Sofort-Clip (Länge unter Einstellungen → Aufnahmen) und setzt eine Marke, falls eine Aufnahme läuft.':
        '与 F8 相同：将 OBS 回放缓存的最后几秒保存为即时片段（时长在“设置 → 录像”中设置），如果有录制正在进行，还会设置一个标记。',
    '1 Eintrag':
        '1 个条目',
    '{n} Einträge':
        '{n} 个条目',
    '5 Sekunden vor (Shift+→).':
        '前进 5 秒（Shift+→）。',
    '5 Sekunden zurück (Shift+←).':
        '后退 5 秒（Shift+←）。',
    'Auf der Zeitleiste öffnen':
        '在时间轴上打开',
    'Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s':
        '录像 {start} – {end} · 在时间轴上从 {at} 起 · {length} 秒',
    'Auswahl':
        '选择',
    'Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).':
        '模糊区域：名称、聊天、好友列表（X）。',
    'Bibliothek':
        '媒体库',
    'Bibliothek ein-/ausblenden.':
        '显示/隐藏媒体库。',
    'Bildausschnitt – den Rahmen in der Vorschau ziehen (C).':
        '裁剪：在查看器中拖动画框（C）。',
    'Clip entfernt – die Aufnahme bleibt, wie sie ist.':
        '片段已移除，录像保持不变。',
    'Clip geteilt – jetzt {n} Clips.':
        '片段已分割，现在共 {n} 个片段。',
    'Clip {n} von {total}':
        '片段 {n}/{total}',
    'Clips auf der Zeitleiste wählen, verschieben und trimmen (V).':
        '在时间轴上选择、移动和修剪片段（V）。',
    'Den ganzen Schnitt einpassen (Strg+0).':
        '适应整个剪辑（Ctrl+0）。',
    'Der Clip unter dem Abspielkopf beginnt hier (Taste I).':
        '播放头下的片段从这里开始（按键 I）。',
    'Der Clip unter dem Abspielkopf endet hier (Taste O).':
        '播放头下的片段在这里结束（按键 O）。',
    'Diese Aufnahme ist schon auf der Zeitleiste.':
        '此录像已在时间轴上。',
    'Ein Bild vor (Strg+→); → eine Sekunde.':
        '前进一帧（Ctrl+→）；→ 前进一秒。',
    'Ein Bild zurück (Strg+←); ← eine Sekunde.':
        '后退一帧（Ctrl+←）；← 后退一秒。',
    'Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt.':
        '从时间轴上移除标记的片段（Del），录像保留。',
    'Export':
        '导出',
    'Exportieren':
        '导出',
    'Fog Scout · Editor':
        'Fog Scout · 编辑器',
    'Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze.':
        '此处无法分割：播放头位于片段边缘。',
    'Hier teilen':
        '在此分割',
    'Inspector':
        '检查器',
    'Inspector ein-/ausblenden.':
        '显示/隐藏检查器。',
    'Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine andere Videodatei.':
        '没有录像：OBS 录像和片段会显示在这里，“导入”可导入其他视频文件。',
    'Keine Clips auf der Zeitleiste.':
        '时间轴上没有片段。',
    'Kürzeste zuerst':
        '最短的在前',
    'Lautstärke der Vorschau (nicht des Clips).':
        '预览的音量（不是片段的音量）。',
    '? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export':
        '? 所有快捷键 · Space 播放 · ←/→ 1 秒 · Shift 5 秒 · Ctrl 或 ,/. 1 帧 · I/O 片段从此处开始/结束 · S 分割 · Del 删除 · Ctrl+Z/Y 撤销/重做 · F 全屏 · Ctrl+S 项目 · Ctrl+E 导出',
    'Längste zuerst':
        '最长的在前',
    'Löschen':
        '删除',
    'Name A–Z':
        '名称 A–Z',
    'Name des Projekts – auch der Name des exportierten Clips.':
        '项目名称，也是导出片段的名称。',
    'Neueste zuerst':
        '最新的在前',
    'Pause (Leertaste)':
        '暂停（Space）',
    'Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D).':
        '在画面上绘制箭头、方框、手绘和文字（D）。',
    'Projekt':
        '项目',
    'Projekt geladen: {name}':
        '项目已加载：{name}',
    'Projekt gespeichert: {file}':
        '项目已保存：{file}',
    'Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten.':
        '保存项目（Ctrl+S）：此录像的剪辑、裁剪、绘图、打码和导出设置，以便之后继续编辑。',
    'Runde':
        '对局',
    'Rückgängig (Strg+Z).':
        '撤销（Ctrl+Z）。',
    'Rückgängig.':
        '已撤销。',
    'Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen (Strg+E) – Format und Kodierung im Inspector unter Export.':
        '将剪辑作为片段写入录像旁边的“Clips”文件夹（Ctrl+E），格式和编码在检查器的“导出”下设置。',
    'Sichtbar':
        '可见',
    'Sortierung der Bibliothek.':
        '媒体库的排序。',
    'Spielt den ganzen Schnitt von vorn ab und springt danach zurück.':
        '从头播放整个剪辑，之后跳回。',
    'Standbild am Abspielkopf als PNG neben den Clips speichern.':
        '在播放头处将静帧保存为 PNG，放在片段旁边。',
    'Stärke':
        '粗细',
    'Teilen':
        '分割',
    'Teilt den Clip unter dem Abspielkopf in zwei (Taste S).':
        '将播放头下的片段一分为二（按键 S）。',
    'Ton der Vorschau an/aus (Windows).':
        '预览声音开/关（Windows）。',
    'Videodatei importieren':
        '导入视频文件',
    'Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie eine Aufnahme öffnen.':
        '导入一个视频文件，它会出现在媒体库中，并能像录像一样打开。',
    'Videos':
        '视频',
    'Vollbild – nur die Vorschau (F, Esc beendet).':
        '全屏，只显示查看器（F，Esc 退出）。',
    'Wiederholen (Strg+Y).':
        '重做（Ctrl+Y）。',
    'Wiederholt.':
        '已重做。',
    'Zeitleiste':
        '时间轴',
    'Zeitleiste ein-/ausblenden.':
        '显示/隐藏时间轴。',
    'Zeitleiste einpassen':
        '适应时间轴',
    'Zeitleiste herauszoomen (−, Strg+Mausrad).':
        '缩小时间轴（−，Ctrl+滚轮）。',
    'Zeitleiste hineinzoomen (+, Strg+Mausrad).':
        '放大时间轴（+，Ctrl+滚轮）。',
    'Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit.':
        '为标记的片段设置慢动作或快进。声音随之变化。',
    'Zum Anfang (Pos1).':
        '到开头（Home）。',
    'Zum Ende (Ende).':
        '到结尾（End）。',
    '{at} liegt in keinem Clip der Zeitleiste.':
        '{at} 不在时间轴的任何片段中。',
    '{n} Clip(s) · {length} s':
        '{n} 个片段 · {length} 秒',
    'Älteste zuerst':
        '最早的在前',
    'Öffnen aus der Bibliothek ist hier nicht verfügbar.':
        '此处无法从媒体库打开。',
    'Fehler in {step} – siehe Log.':
        '{step} 出错，详见日志。',
    'Strg+{n}':
        'Ctrl+{n}',
    'Tastenkürzel':
        '键盘快捷键',
    'Schliessen (? oder Esc)':
        '关闭（? 或 Esc）',
    'Wiedergabe':
        '播放',
    'Werkzeuge':
        '工具',
    'Leertaste':
        'Space',
    'Abspielen / Anhalten':
        '播放/暂停',
    '1 Sekunde zurück / vor':
        '后退/前进 1 秒',
    'Shift+← / →':
        'Shift+← / →',
    '5 Sekunden zurück / vor':
        '后退/前进 5 秒',
    'Strg+← / →  ·  , / .':
        'Ctrl+← / →  ·  , / .',
    '1 Bild zurück / vor':
        '后退/前进 1 帧',
    'Pos1 / Ende':
        'Home / End',
    'Zum Anfang / zum Schluss':
        '到开头/到结尾',
    'Zur nächsten Marke':
        '到下一个标记',
    'Untertitel {a}–{b}.':
        '字幕 {a}–{b}。',
    '{file} wartet – {n} Export(e) davor.':
        '{file} 正在等待，前面还有 {n} 个导出。',
    'Kodiere {file} …':
        '正在编码 {file}…',
    'Titel & Vorschaubild':
        '标题和缩略图',
    'Claude fragt: {question}':
        'Claude 提问：{question}',
    'Deine Antwort …':
        '你的回答…',
    'Name der Vorlage':
        '模板名称',
    'Als Vorlage speichern':
        '另存为模板',
    'Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen.':
        '将你刚才执行的步骤（不含打码框）保存为模板，时间从开头或结尾算起，因此也适用于其他时长。',
    'Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, kostenlos; erst „Übernehmen“ ändert den Schnitt.':
        '为此剪辑建议模板中的步骤，不使用 Claude，免费；只有“应用”才会更改剪辑。',
    'Vorlage löschen':
        '删除模板',
    'Entfernt die gewählte Vorlage.':
        '移除所选模板。',
    'Bitte einen Namen für die Vorlage eingeben.':
        '请为模板输入名称。',
    'Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu).':
        '没有可作为模板的内容（打码框不属于模板）。',
    'Vorlage „{name}“ gespeichert.':
        '模板“{name}”已保存。',
    'Vorlage „{name}“':
        '模板“{name}”',
    'Vorlage „{name}“ gelöscht.':
        '模板“{name}”已删除。',
    'Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts wird hochgeladen.':
        '将与“检查导出”相同的八张静帧发送给 Claude；Claude 选出最佳缩略图并建议一个标题。标题由你自己采用，缩略图只作为图片保存在“Clips”中，不会上传任何内容。',
    'Claude sucht unter {n} Standbildern ein Vorschaubild …':
        'Claude 正在从 {n} 张静帧中挑选缩略图…',
    'Als Short-Titel: „{title}“':
        '作为短视频标题：“{title}”',
    'Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für YouTube kopierst du ihn selbst.':
        '将该标题用作短视频标题（一个撤销步骤）。用于 YouTube 时请自行复制。',
    'Vorschaubild bei {at} speichern':
        '保存 {at} 处的缩略图',
    'Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im Export, mit dem Titel. Hochgeladen wird nichts.':
        '将此静帧以完整尺寸保存为 PNG 到“Clips”中，按导出时的方式打码，并带标题。不会上传任何内容。',
    'Short-Titel übernommen.':
        '已采用短视频标题。',
    'Vorschaubild':
        '缩略图',
    'Export prüfen':
        '检查导出',
    'Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf einen Fund springt hin und schlägt einen Zensurkasten vor.':
        '将完成剪辑的八张静帧（按导出方式裁剪，打码区域已打码）发送给 Claude；Claude 会报告仍可辨认的名称或聊天，以及其他不应以这种方式分享的内容。单击某项发现会跳到该处并建议一个打码框。',
    'Claude prüft {n} Standbilder des fertigen Schnitts …':
        'Claude 正在检查完成剪辑的 {n} 张静帧…',
    'Claude hat nichts gefunden, das so nicht geteilt werden sollte.':
        'Claude 没有发现不应以这种方式分享的内容。',
    'Springt hin und schlägt einen Zensurkasten für diese Stelle vor.':
        '跳到该处并为此位置建议一个打码框。',
    'Springt hin.':
        '跳到该处。',
    'Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.':
        '{at} 处的建议，“采用建议”会遮盖该位置。',
    'Name lesbar':
        '名称可辨认',
    'Chat lesbar':
        '聊天可辨认',
    'Auffällig':
        '引人注意',
    'Text finden':
        '查找文字',
    'Sucht auf dem Bild am Abspielkopf nach Text (Namen, Chat) – auf diesem PC, nichts wird gesendet. Die Fundstellen erscheinen nummeriert.':
        '在播放头处的画面中查找文字（名称、聊天），在这台电脑上进行，不发送任何内容。找到的内容会编号显示。',
    'Vorschläge übernehmen':
        '采用建议',
    'Macht aus den nummerierten Fundstellen Zensurkästen (ein Schritt zum Rückgängigmachen).':
        '将编号的发现转为打码框（一个撤销步骤）。',
    'Vorschläge verwerfen':
        '放弃建议',
    'Claude: nur Namen':
        'Claude：只要名称',
    'Schickt das Standbild (zensierte Bereiche bleiben zensiert) mit den nummerierten Fundstellen an Claude; Claude nennt nur die Nummern, die Namen oder Chat zeigen – die übrigen Vorschläge fallen weg.':
        '将静帧（打码区域保持打码）连同编号的发现发送给 Claude；Claude 只指出显示名称或聊天的编号，其他建议将被移除。',
    'Die Texterkennung ist in dieser Installation nicht vorhanden.':
        '此安装中没有文字检测功能。',
    'Suche Text im Bild …':
        '正在画面中查找文字…',
    'Das Bild liess sich nicht nach Text durchsuchen.':
        '无法在画面中搜索文字。',
    'Kein Text gefunden, der nicht schon verdeckt ist.':
        '没有找到尚未遮盖的文字。',
    '{n} Textstellen gefunden – „Vorschläge übernehmen“ verdeckt sie.':
        '找到 {n} 处文字，“采用建议”会将其遮盖。',
    '{n} Kästen gesetzt.':
        '已设置 {n} 个框。',
    'Claude sieht sich {n} Fundstellen an …':
        'Claude 正在查看 {n} 处发现…',
    'Claude hält keine Fundstelle für einen Namen oder Chat.':
        'Claude 认为这些发现中没有名称或聊天。',
    '{n} Fundstellen zeigen laut Claude Namen oder Chat.':
        'Claude 说有 {n} 处发现显示名称或聊天。',
    'Kasten ab hier':
        '框从此处开始',
    'Kasten bis hier':
        '框到此处为止',
    'Kasten immer':
        '框始终有效',
    'Der markierte Kasten gilt erst ab dem Bild am Abspielkopf – z. B. wenn ein Name erst später erscheint.':
        '标记的框只从播放头处的画面起生效，例如某个名称较晚才出现时。',
    'Der markierte Kasten gilt nur bis zum Bild am Abspielkopf.':
        '标记的框只到播放头处的画面为止有效。',
    'Der markierte Kasten gilt wieder für die ganze Aufnahme.':
        '标记的框重新对整个录像生效。',
    'Kasten {n} gilt von {a} bis {b} der Aufnahme.':
        '框 {n} 在录像的 {a} 到 {b} 之间生效。',
    'Kasten {n} gilt für die ganze Aufnahme.':
        '框 {n} 对整个录像生效。',
    'Am Anfang der Aufnahme gibt es kein „bis hier“.':
        '录像开头处没有“到此处为止”。',
    '{n} davon nur zeitweise.':
        '其中 {n} 个只在一段时间内有效。',
    'Zurückspringen / Anhalten / Abspielen – L mehrmals: ×2, ×4':
        '后退/停止/播放，再按 L：×2、×4',
    'Vollbild an / aus':
        '全屏开/关',
    'Clip beginnt / endet am Abspielkopf':
        '片段在播放头处开始/结束',
    'S oder Strg+B':
        'S 或 Ctrl+B',
    'Clip am Abspielkopf teilen':
        '在播放头处分割片段',
    'Entf':
        'Del',
    'Markierten Clip löschen':
        '删除标记的片段',
    'Hinein- / herauszoomen':
        '放大/缩小',
    'Strg+0':
        'Ctrl+0',
    'Ganze Zeitleiste zeigen':
        '显示整个时间轴',
    'Auswählen':
        '选择',
    'Bildausschnitt':
        '裁剪',
    'Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie':
        '取消、退出工具或清除选择，绝不会关闭',
    'Strg+W':
        'Ctrl+W',
    'Editor schliessen':
        '关闭编辑器',
    'Abgebrochen.':
        '已取消。',
    'Esc schliesst den Editor nicht – schliessen mit × oder Strg+W.':
        'Esc 不会关闭编辑器，请用 × 或 Ctrl+W 关闭。',
    'Strg+Z / Strg+Y':
        'Ctrl+Z / Ctrl+Y',
    'Rückgängig / Wiederholen':
        '撤销/重做',
    'Strg+S':
        'Ctrl+S',
    'Projekt speichern':
        '保存项目',
    'Strg+E':
        'Ctrl+E',
    'Diese Übersicht ein / aus':
        '此概览开/关',
    'In der Statistik zeigen':
        '在统计中显示',
    'Aufnahme dieser Runde öffnen':
        '打开此对局的录像',
    'Runde markieren: Rolle, Farming, Killer oder Map korrigieren, löschen – oder Rechtsklick. Doppelklick zeigt die Aufnahme.':
        '标记一局：更正角色、刷分、杀手或地图，删除，或右键单击。双击显示录像。',
    'OBS-Passwort ist auf diesem PC/Benutzerkonto nicht lesbar – bitte neu eingeben.':
        '在这台电脑/用户账户上无法读取 OBS 密码，请重新输入。',
    'Als neues Projekt speichern':
        '另存为新项目',
    'Autosave aus':
        '自动保存已关闭',
    'Bereich übernehmen':
        '采用该范围',
    'Bereich übernommen – Strg+Z stellt das Projekt wieder her.':
        '已采用该范围，Ctrl+Z 可恢复项目。',
    'Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. Deine Fassung liegt unter Sicherungen und lokal.':
        '项目在 Fog Scout 之外被更改或存在两份。你的版本保存在 Sicherungen 下以及本地。',
    'Die Aufnahme konnte nicht geprüft werden.':
        '无法检查录像。',
    'Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz herunterladen.':
        '录像只在云端，检查它需要下载整个文件。',
    'Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt ist anders). Es wurde nicht geladen.':
        '录像与已保存的项目不匹配（内容不同），未加载。',
    'Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt.':
        '项目的片段无法读取，显示默认片段。',
    'Die Projektdatei ist unlesbar und wurde nicht geladen.':
        '项目文件无法读取，未加载。',
    'Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist lokal gesichert.':
        '项目文件在 Fog Scout 之外被删除或移动。你的状态保存在本地。',
    'Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.':
        '项目文件已被重命名。你的状态保存在本地。',
    'Dieses Projekt ist schon in einem anderen Fenster offen – hier wird nichts gespeichert.':
        '此项目已在另一个窗口中打开，此处不会保存任何内容。',
    'Editor-Projekte automatisch speichern':
        '自动保存编辑器项目',
    'Editor-Projekte nicht gesichert':
        '编辑器项目未安全保存',
    'Editor-Projekte werden noch gesichert …':
        '编辑器项目仍在安全保存中…',
    'Editor: automatisches Speichern an.':
        '编辑器：自动保存已开启。',
    'Editor: automatisches Speichern aus – Strg+S speichert das Projekt.':
        '编辑器：自动保存已关闭，按 Ctrl+S 保存项目。',
    'Eine wählen …':
        '选择一个…',
    'Erneut prüfen':
        '重新检查',
    'Es gibt ein Projekt zu einer gleichnamigen, aber veränderten Aufnahme.':
        '存在一个用于同名录像的项目，但该录像已更改。',
    'Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine Clips.':
        '此录像有一个已保存的项目（{n} 个片段）。采用预览中的范围（{a}–{b}）将替换其片段。',
    'Gespeichertes Projekt gefunden – die Aufnahme wird geprüft.':
        '找到已保存的项目，正在检查录像。',
    'Kein Projekt':
        '无项目',
    'Kein Projekt – Strg+S legt ein neues an.':
        '无项目，按 Ctrl+S 新建一个。',
    'Keine öffnen':
        '都不打开',
    'Laden':
        '加载',
    'Lokal gesicherter Stand eines fehlenden Projekts gefunden.':
        '找到一个缺失项目在本地保存的状态。',
    'Mindestens ein Editor-Stand ist weder im Projekt noch lokal gesichert (Speichern hängt oder der Ordner ist nicht erreichbar). Trotzdem beenden? Die ungesicherten Änderungen gehen dann verloren.':
        '至少有一个编辑器状态既不在其项目中，也未保存在本地（保存卡住或无法访问文件夹）。仍然退出吗？未安全保存的更改将会丢失。',
    'Neu beginnen':
        '新建',
    'Neuerer Stand aus der lokalen Rettungskopie geladen.':
        '已从本地救援副本加载较新的状态。',
    'Neues Projekt':
        '新项目',
    'Nicht laden':
        '不加载',
    'Nicht schliessen':
        '不关闭',
    'Nicht wiederherstellen':
        '不恢复',
    'Nichts tun':
        '什么也不做',
    'Ohne Prüfung laden':
        '不检查直接加载',
    'Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, gleiche Grösse).':
        '找到 Fog Scout 1.17 或更早版本的项目（名称相同，大小相同）。',
    'Projekt aus neuerer Version – wird nicht überschrieben':
        '来自较新版本的项目，未覆盖',
    'Projekt behalten':
        '保留项目',
    'Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen.':
        '项目已打开，未采用预览中的范围。',
    'Projekt nicht gespeichert und keine Rettungskopie möglich: {why}':
        '项目未保存，且无法创建救援副本：{why}',
    'Projekt wiederherstellen':
        '恢复项目',
    'Projekt wird gespeichert …':
        '正在保存项目…',
    'Projekt wird gesucht …':
        '正在查找项目…',
    'Prüfen':
        '检查',
    'Prüft Aufnahme …':
        '正在检查录像…',
    'Prüft Aufnahme … {p} %':
        '正在检查录像… {p} %',
    'Speichern und schliessen':
        '保存并关闭',
    'Trotzdem laden':
        '仍然加载',
    'Trotzdem schliessen':
        '仍然关闭',
    'Ungespeicherte Änderungen von {when} gefunden.':
        '发现 {when} 的未保存更改。',
    'Ungespeicherte Änderungen.':
        '未保存的更改。',
    'Update wartet: Editor-Projekte werden gesichert …':
        '更新正在等待：编辑器项目正在安全保存…',
    'Verwerfen und schliessen':
        '放弃并关闭',
    'Wiederherstellen':
        '恢复',
    'Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die ganze Aufnahme ist, kann Fog Scout nicht bestätigen.':
        '此录像有一个从未完整检查过的项目。开始、结束和大小都匹配；但 Fog Scout 无法确认它是否是完整的录像。',
    'Zuordnung nicht geprüft':
        '关联未检查',
    '{n} Projektdateien passen zu dieser Aufnahme – keine wurde geöffnet.':
        '有 {n} 个项目文件与此录像匹配，未打开任何一个。',
    '● Änderungen':
        '● 有更改',
    '⚠ Mehrere Projektdateien – Auswahl nötig':
        '⚠ 有多个项目文件，请选择一个',
    '⚠ Nicht gespeichert – {why}':
        '⚠ 未保存 – {why}',
    '⚠ Nicht im Projekt gespeichert – lokal gesichert':
        '⚠ 未保存在项目中，已保存在本地',
    '⚠ Projekt ausserhalb geändert':
        '⚠ 项目在外部被更改',
    '⚠ Projektdatei fehlt – Änderungen nur lokal gesichert':
        '⚠ 项目文件缺失，更改仅保存在本地',
    '⚠ Speichern hängt':
        '⚠ 保存卡住',
    '✓ Gespeichert {at}':
        '✓ 已于 {at} 保存',
    'Der grosse Editor speichert sein Projekt von selbst (1,5 s nach einer Änderung, nie während du ziehst) – mit Sicherungen und einer lokalen Kopie, falls die Projektdatei nicht schreibbar ist. Aus: nur Strg+S schreibt das Projekt; dazwischen hält der Editor einen lokalen Wiederherstellungsstand.':
        '大编辑器会自动保存其项目（更改后 1.5 秒，拖动时绝不保存），并带有备份和本地副本，以防项目文件无法写入。关闭：只有 Ctrl+S 会写入项目；在此期间编辑器会保留一个本地恢复状态。',
    'Auf alle Clips':
        '应用到所有片段',
    'Bild bei {at} der Aufnahme · {length} s ohne Ton':
        '录像 {at} 处的画面 · {length} 秒，无声音',
    'Den Ausschnitt am Anfang des Clips in der Vorschau ziehen – dazwischen fährt die Kamera gleichmässig.':
        '在预览中拖动片段开始处的画框，期间镜头会匀速移动。',
    'Den Ausschnitt am Ende des Clips in der Vorschau ziehen.':
        '在预览中拖动片段结束处的画框。',
    'Der Clip zeigt wieder das ganze Bild.':
        '片段重新显示整个画面。',
    'Effekte':
        '效果',
    'Effekte entfernen':
        '移除效果',
    'Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start.':
        '固定画框：开始和结束相同，结束画框跟随开始画框。',
    'End-Ausschnitt':
        '结束画框',
    'Farbe auf alle {n} Clips übernommen.':
        '颜色已应用到全部 {n} 个片段。',
    'Heller oder dunkler – nur dieser Clip.':
        '更亮或更暗，仅此片段。',
    'Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen.':
        '将此片段的亮度、对比度和饱和度恢复为录制时的状态。',
    'Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton.':
        '将播放头处的画面保持设定的时长（按键 P），无声音。',
    'Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.':
        '颜色更浓或更淡，最左边为黑白，仅此片段。',
    'Mehr oder weniger Kontrast – nur dieser Clip.':
        '对比度更高或更低，仅此片段。',
    'Ohne Bewegung':
        '不移动',
    'Rückwärts':
        '倒放',
    'Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.':
        '倒放每个片段最多 {n} 秒，请先分割此片段。',
    'Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens {n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).':
        '倒放片段，声音也一样。此录像每个片段最多 {n} 秒（否则 ffmpeg 需要的内存太多）。',
    'Standbild am Abspielkopf einfügen':
        '在播放头处插入静帧',
    'Standbild einfügen':
        '插入静帧',
    'Standbild eingefügt: {n} s ohne Ton.':
        '已插入静帧：{n} 秒，无声音。',
    'Standbild hier einfügen':
        '在此插入静帧',
    'Standbild – Clip {n} von {total}':
        '静帧 – 片段 {n}/{total}',
    'Start-Ausschnitt':
        '开始画框',
    'Wie lange ein Standbild steht – für ein neues, oder für das markierte Standbild.':
        '静帧保持多长时间，适用于新静帧或标记的静帧。',
    'Zoom':
        '缩放',
    'Zoom entfernen':
        '移除缩放',
    'Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – Esc beendet.':
        '缩放：在预览中拖动画框，或拖动其角放大/缩小，Esc 结束。',
    '{n}  Standbild {length} s':
        '{n}  静帧 {length} 秒',
    'Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig).':
        '将此片段的亮度、对比度和饱和度应用到时间轴上的所有片段（一步，Ctrl+Z 可撤销）。',
    'Als Short anzeigen':
        '以短视频显示',
    'Beginnt hier':
        '从这里开始',
    'Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.':
        '文字从播放头起在短视频底部显示 {n} 秒。',
    'Der markierte Untertitel beginnt am Abspielkopf.':
        '标记的字幕从播放头处开始。',
    'Der markierte Untertitel endet am Abspielkopf.':
        '标记的字幕在播放头处结束。',
    'Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen.':
        '预览显示带标题和字幕的完成竖屏视频，绘图和打码在导出中生效，此处不显示。',
    'Ein Short ist höchstens {limit} min lang, dieser Schnitt {seconds} s – kürzer schneiden.':
        '短视频最长 {limit} 分钟，此剪辑为 {seconds} 秒，请剪短。',
    'Endet hier':
        '在这里结束',
    'Entfernen':
        '移除',
    'Entfernt den markierten Untertitel.':
        '移除标记的字幕。',
    'Erst den Text des Untertitels eingeben.':
        '请先输入字幕文字。',
    'Hochformat 1080×1920 für YouTube Shorts und TikTok, höchstens 3 min':
        '竖屏 1080×1920，用于 YouTube Shorts 和 TikTok，最长 3 分钟',
    'Schriftgrösse des Titels.':
        '标题的字号。',
    'Short (9:16)':
        '短视频（9:16）',
    'Short / TikTok (9:16)':
        '短视频 / TikTok（9:16）',
    'Short 1080×1920, {fps} fps':
        '短视频 1080×1920，{fps} fps',
    'Text eingeben, dann „Untertitel am Abspielkopf“':
        '输入文字，然后点击“在播放头处添加字幕”',
    'Titel':
        '标题',
    'Titel oben (leer = keiner)':
        '顶部标题（留空 = 无）',
    'Unscharfer Hintergrund':
        '模糊背景',
    'Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der 9:16-Ausschnitt unter Bild) füllt das Hochformat.':
        '模糊背景：整个游戏画面位于中间，上下是同一画面的模糊版本。裁剪：中间部分（或“画面”下的 9:16 裁剪）填满竖屏画框。',
    'Untertitel':
        '字幕',
    'Untertitel am Abspielkopf':
        '在播放头处添加字幕',
    'Zuschnitt 9:16':
        '裁剪 9:16',
    'gross':
        '大',
    'klein':
        '小',
    'mittel':
        '中',
    '⚠ länger als {n} min – so nicht exportierbar':
        '⚠ 超过 {n} 分钟，无法这样导出',
    '(Datei fehlt – wird nicht exportiert)':
        '（文件缺失，未导出）',
    'Beginnt am Abspielkopf':
        '从播放头处开始',
    'Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt ihn am meisten. Aus: beide gleich laut wie eingestellt.':
        '播放音乐时游戏声音会自动变小，“强”降低得最多。关闭：两者都按设定的音量。',
    'Der markierte Ton-Clip beginnt am Abspielkopf.':
        '所选音频片段从播放头处开始。',
    'Die Musik wird am Anfang des Clips lauter.':
        '音乐在片段开头淡入。',
    'Die Musik wird zum Ende des Clips leiser.':
        '音乐在片段结尾淡出。',
    'Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im Export läuft die Musik weiter.':
        '预览中也会播放音乐；静帧在预览中无声，导出时音乐会继续播放。',
    'Eigene Tonspur (A2)':
        '自己的音轨（A2）',
    'Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die Spur A2 legen – oder die Datei direkt auf A2 ziehen.':
        '将你自己的音频或视频文件（音乐、解说）放到播放头处的 A2 音轨上，或将文件拖到 A2 上。',
    'Höchstens {n} Ton-Clips.':
        '最多 {n} 个音频片段。',
    'Kein Ton in {file}.':
        '{file} 中没有声音。',
    'Keine Ton- oder Videodatei: {file}':
        '不是音频或视频文件：{file}',
    'Lautstärke':
        '音量',
    'Lautstärke der ganzen Spur A2.':
        '整个 A2 音轨的音量。',
    'Lautstärke des Spieltons im fertigen Clip.':
        '完成的片段中游戏声音的音量。',
    'Lautstärke nur dieses Ton-Clips.':
        '仅此音频片段的音量。',
    'Lese {file} …':
        '正在读取 {file}…',
    'Musik aus':
        '音乐淡出',
    'Musik ein':
        '音乐淡入',
    'Musik hinzufügen':
        '添加音乐',
    'Musik hinzufügen …':
        '添加音乐…',
    'Musik oder Kommentar hierher ziehen – oder Rechtsklick „Musik hinzufügen …“':
        '将音乐或解说拖到这里，或右键单击“添加音乐…”',
    'Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt.':
        '将所选音频片段从 A2 音轨上移除，文件保留。',
    'Noch keine Musik – Spielton wie aufgenommen.':
        '还没有音乐，游戏声音保持录制时的样子。',
    'Spielton':
        '游戏声音',
    'Spielton unter Musik':
        '音乐下的游戏声音',
    'Ton und Video':
        '音频和视频',
    'Ton-Clip entfernen':
        '移除音频片段',
    'Ton-Clip {file} entfernt – die Datei bleibt.':
        '已移除音频片段 {file}，文件保留。',
    'leicht':
        '轻',
    'stark':
        '强',
    '{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.':
        '{file} 从 {at} 起位于 A2 上，其下的游戏声音会变小。',
    '{file}: {start} – {end} der Datei, im Clip ab {at}':
        '{file}：文件的 {start} – {end}，在片段中从 {at} 起',
    '{n} Ton-Clip(s) auf A2.':
        'A2 上有 {n} 个音频片段。',
    'Als Montage öffnen …':
        '作为合集打开…',
    'Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.':
        '尺寸不同（{w}×{h}），导出时会加黑边适配。',
    'Aufnahme fehlt oder ist nicht lesbar: {file}':
        '录像缺失或无法读取：{file}',
    'Eine Montage übernimmt keinen Bereich aus der Vorschau.':
        '合集不会采用预览中的范围。',
    'Erst wenn das Projekt geladen ist.':
        '仅在项目加载后。',
    'Für eine Montage mindestens zwei Videos markieren.':
        '合集至少需要选择两个视频。',
    'Höchstens {n} Aufnahmen in einer Montage.':
        '一个合集最多 {n} 个录像。',
    'Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das Projekt der Runde bleibt, wie es zuletzt gespeichert war.':
        '现在是合集，它保存在 Clips → Montagen 下。该对局的项目保持上次保存时的状态。',
    'Montage':
        '合集',
    'Montage aus {n} Aufnahmen':
        '{n} 个录像的合集',
    'Montage nicht zu öffnen – ihre erste Aufnahme fehlt: {file}':
        '无法打开合集，其第一个录像缺失：{file}',
    'Montage {date}':
        '合集 {date}',
    'Nicht gefunden: {files} – ihre Clips sind rot, Exportieren geht erst, wenn sie entfernt sind.':
        '未找到：{files}，它们的片段显示为红色；移除后即可导出。',
    'Nur lesen':
        '只读',
    'Trotzdem verwenden':
        '仍然使用',
    'Video nicht lesbar: {file}':
        '视频无法读取：{file}',
    '{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.':
        '{file} 已不是保存时的同一个录像。',
    '{file}: {n} Clip(s) angehängt.':
        '{file}：已追加 {n} 个片段。',
    'Audiomediathek':
        '音频库',
    'Audiomediathek im Browser geöffnet – heruntergeladene Titel erscheinen im Abschnitt Ton, sobald du zurück im Editor bist.':
        '音频库已在浏览器中打开，回到编辑器后，下载的曲目会显示在“声音”部分。',
    'Neu im Download-Ordner – Klick legt sie am Abspielkopf auf A2:':
        '下载文件夹中的新文件，单击即可放到播放头处的 A2 上：',
    'Öffnet YouTubes Audiomediathek im Browser: kostenlose Musik und Effekte, für Videos freigegeben (keine Content-ID-Ansprüche). Heruntergeladene MP3s erscheinen hier darunter.':
        '在浏览器中打开 YouTube 音频库：免费的音乐和音效，可用于视频（不会被 Content ID 认领）。下载的 MP3 会显示在下方。',
    'Status, aktuelle Map und deine Runden auf einen Blick':
        '状态、当前地图和你的对局一览',
    'Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen':
        '所有标注地图：查看、手动显示、自己的图片和备注',
    'Was im Spiel erscheint, wo und wie gross':
        '游戏中显示什么、在哪里、多大',
    'Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert':
        '你的对局、击杀和等待时间，仅保存在这台电脑上',
    'Runden, Clips und Screenshots – abspielen, schneiden, aufräumen':
        '对局、片段和截图：播放、剪辑、整理',
    'Server-Regionen wählen und die Verbindung im Blick behalten':
        '选择服务器区域并关注连接状况',
    'Alles, was Fog Scout tut – suchen mit Strg+F':
        'Fog Scout 的所有功能，按 Ctrl+F 搜索',
    'Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche':
        '程序做了什么，供查阅和故障排除',
    'Übersicht öffnen':
        '打开概览',
    'Funktionen':
        '功能',
    'aktiv':
        '已启用',
    'wartet auf DBD':
        '正在等待 DBD',
    'nimmt auf':
        '录制中',
    'verbunden':
        '已连接',
    'verbindet …':
        '正在连接…',
    'startet …':
        '正在启动…',
    'Fehler – Details im Log':
        '错误，详见日志',
    'nur unter Windows':
        '仅限 Windows',
    'HWiNFO fehlt':
        '缺少 HWiNFO',
    'Mediensteuerung nicht verfügbar':
        '媒体控制不可用',
    'Discord nicht erreichbar':
        '无法连接 Discord',
    'Anmeldung nötig':
        '需要登录',
    'keine Client-ID':
        '无客户端 ID',
    'Suche leeren':
        '清除搜索',
    'Runden · BP/h erst mit Match-Daten':
        '局 · 血点/时需要比赛数据',
    'Verbindung prüfen …':
        '检查连接…',
    'Öffnet Einstellungen → Verbindungen: OBS-Verbindung (Port, Passwort) und „Verbindung testen“.':
        '打开“设置 → 连接”：OBS 连接（端口、密码）和“测试连接”。',
    '{n} Marken':
        '{n} 个标记',
    '1 Marke':
        '1 个标记',
    'Keine Aufnahme passt zu den Filtern oben.':
        '没有符合上述筛选条件的录像。',
    'Kein Clip passt zu den Filtern oben.':
        '没有符合上述筛选条件的片段。',
    'Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.':
        '没有内容：日志为空，或搜索和类别隐藏了所有内容。',
    'OBS nicht verbunden':
        'OBS 未连接',
    'Kills, Entkommen und Bloodpoints zählen hier ohne Custom Games – die Rolle „Custom Games“ zeigt sie.':
        '此处的击杀、逃脱和血点不包括自定义对局，角色“自定义对局”会显示它们。',
    'Keine Runden in dieser Auswahl – „Filter zurücksetzen“ zeigt wieder alle.':
        '此筛选范围内没有对局，“重置筛选”会重新显示全部。',
    'In dieser Auswahl ist keine Runde einem Match der Stats-Seite zugeordnet – darum fehlen Kills, Entkommen und Bloodpoints.':
        '此筛选范围内没有对局与统计页面的比赛关联，因此缺少击杀、逃脱和血点。',
    'Kills, Entkommen und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        '击杀、逃脱和血点来自统计页面，为此需要设置一次比赛数据。',
    'Nicht gezählt: {n} × Rundenende nicht erkannt (die nächste Map kam, bevor das Ende erkannt wurde). Zuletzt: {map}, {when}.':
        '未计入：{n} 次未检测到对局结束（在检测到结束之前下一张地图就出现了）。最近一次：{map}，{when}。',
    '{n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '{n} 次未检测到对局结束，但已按统计页面上的时长计入。',
    '{n} × Map mitten im Match falsch erkannt (laut Stats-Seite lief da schon ein Match) – nicht gezählt. Zuletzt: {map}, {when}.':
        '{n} 次在对局中途读错地图（统计页面上已有一场比赛正在进行），未计入。最近一次：{map}，{when}。',
    'Keine Map passt zu „{text}“. Gesucht wird in Map- und Realm-Namen aller Spielsprachen und in Abkürzungen.':
        '没有与“{text}”匹配的地图。搜索会查找所有游戏语言中的地图和领域名称以及缩写。',
    'Leert das Suchfeld und zeigt wieder alle Maps.':
        '清空搜索框并重新显示所有地图。',
    'Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter „Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) – die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose.':
        '每个勾选项都是 Claude 在你点击时提供帮助的一个地方，绝不会自动进行，也绝不会在你输入时进行：搜索（“问 Claude”行：你的问题以及设置、页面和操作的名称）、统计问题（计数和比率）、片段编辑器（“用 Claude 编辑”：你的要求和以数字表示的剪辑，勾选其选项时还包括一张静帧）以及图片编辑器（“Claude”选项卡：你的要求和图片）。Claude 只提供建议；在你选择或点击“应用”确认之前，不会执行任何操作。绝不发送：对局、地图、杀手、路径、文件名、服务器或日志。需要你自己从 Anthropic Console 获取的 API 密钥（“获取 API 密钥”）；API 从余额中付费，与 Claude 订阅分开（“充值”，在那里可以设置支出上限）。程序会根据回复估算每个问题的费用，并按月累计。密钥使用 Windows 加密保存在这台电脑上（如果加密失败，则只保留到你退出程序），绝不会进入备份、日志或诊断信息。',
    'Zeigt in der Musikkarte, was in Spotify als Nächstes kommt (Position und Anzahl unter Overlay → Musik). Die Windows-Mediensteuerung kennt nur den laufenden Titel, die Liste holt das Programm deshalb von Spotify selbst: Dafür im Developer-Dashboard „Create app“ anlegen (Name frei, API „Web API“), als Redirect URI genau {uri} eintragen, die Client-ID kopieren und hier einfügen, dann „Mit Spotify verbinden“ – der Browser fragt einmal nach der Freigabe. Gelesen wird nur die Warteschlange, nichts gesteuert; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden) und lässt sich hier trennen. Titel kommen nie ins Log.':
        '在音乐卡片上显示 Spotify 中接下来播放的内容（位置和数量在“悬浮窗 → 音乐”中设置）。Windows 媒体控件只知道当前曲目，因此程序直接从 Spotify 获取列表：在开发者仪表板中点击“Create app”（名称任意，API 选“Web API”），将重定向 URI 准确填写为 {uri}，复制客户端 ID 并粘贴到这里，然后点击“连接 Spotify”，浏览器会请求一次你的授权。只读取队列，不控制任何内容；授权使用 Windows 加密保存在这台电脑上（如果加密不可用，则只保留到你退出程序），并可在这里移除。曲目标题绝不会写入日志。',
    'Lädt Clips (F8 und Editor) von selbst auf deinen YouTube-Kanal, Runden nur auf Wunsch: Rechtsklick oder „Auf YouTube hochladen“ unter Aufnahmen. Dafür einmal in der Google Cloud Console ein Projekt anlegen, „YouTube Data API v3“ aktivieren, unter „Anmeldedaten“ einen OAuth-Client vom Typ „Desktop-App“ erstellen und den Zustimmungsbildschirm veröffentlichen (sonst läuft die Anmeldung nach 7 Tagen ab); Client-ID und Client-Secret hier einfügen oder die heruntergeladene JSON-Datei laden, dann „Mit YouTube verbinden“ – der Browser fragt einmal nach der Freigabe. Google erlaubt mit dem Standardkontingent etwa sechs Uploads am Tag; was nicht mehr passt, wartet in der Warteschlange bis zum nächsten Tag. Hochgeladen wird nur, wenn du weder in einer Lobby noch in einer Runde bist; die Datei bleibt immer auch auf der Platte. Gesendet werden nur die Videodatei, Titel (Map, Killer, Datum) und Beschreibung – nie Spielernamen; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden). Mit „Uploads in Playlists einsortieren“ kommt jedes Video zusätzlich in eine Playlist deiner Wahl – dafür fragt die Anmeldung die breitere Berechtigung „YouTube-Konto verwalten“ an (einmal neu verbinden).':
        '自动将片段（F8 和编辑器）上传到你的 YouTube 频道，对局只在你要求时上传：在“录像”下右键单击或点击“上传到 YouTube”。为此，请在 Google Cloud 控制台中创建一次项目，启用“YouTube Data API v3”，在“凭据”下创建“Desktop app”类型的 OAuth 客户端，并发布同意屏幕（否则登录会在 7 天后过期）；将客户端 ID 和客户端密钥粘贴到这里或加载下载的 JSON 文件，然后点击“连接 YouTube”，浏览器会请求一次你的授权。在默认配额下，Google 每天大约允许上传六次；放不下的会在队列中等到第二天。上传只在你既不在大厅也不在对局中时进行；文件也始终保留在磁盘上。只发送视频文件、标题（地图、杀手、日期）和描述，绝不发送玩家名称；授权使用 Windows 加密保存在这台电脑上（如果加密不可用，则只保留到你退出程序）。开启“将上传内容归入播放列表”后，每个视频还会放入你选择的播放列表，为此登录时会请求更广泛的“管理你的 YouTube 账号”权限（需重新连接一次）。',
    'Liest Client-ID und Client-Secret aus der Datei „client_secret_….json“, die Google nach dem Anlegen des OAuth-Clients zum Herunterladen anbietet („JSON herunterladen“). Die Datei wird nur gelesen und bleibt, wo sie ist; das Secret landet mit der Windows-Verschlüsselung in den Einstellungen (sonst gilt es nur bis zum Beenden).':
        '从 Google 在创建 OAuth 客户端后提供下载的“client_secret_….json”文件（“Download JSON”）中读取客户端 ID 和客户端密钥。该文件只会被读取并保留在原处；密钥使用 Windows 加密保存到设置中（否则只保留到你退出程序）。',
    'Öffnet die Google-Anmeldung im Browser (nur Recht „Videos hochladen“). Danach kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe mit der Windows-Verschlüsselung auf diesem PC (sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf einem freien Port.':
        '在浏览器中打开 Google 登录页面（仅“上传视频”权限）。之后浏览器会返回 127.0.0.1，程序使用 Windows 加密将授权保存在这台电脑上（否则只保留到你退出程序）。为此它仅在登录期间在一个空闲端口上监听一次。',
    'Öffnet die Spotify-Anmeldung im Browser. Nach dem Zustimmen kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe (mit der Windows-Verschlüsselung, nur auf diesem PC – sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf diesem Port.':
        '在浏览器中打开 Spotify 登录页面。你同意后，浏览器会返回 127.0.0.1，程序会保存授权（使用 Windows 加密，仅在这台电脑上，否则只保留到你退出程序）。为此它仅在登录期间在此端口上监听一次。',
    '({how})':
        '（{how}）',
    'Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird er nicht gespeichert.':
        'Claude：API 密钥只保留到你退出程序，因为 Windows 加密不可用，所以不会保存。',
    'Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu eintragen oder „Key löschen“.':
        'Claude：无法在这台电脑上读取已保存的密钥，请重新输入或使用“删除密钥”。',
    'OBS-Passwort gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'OBS 密码只保留到你退出程序，因为 Windows 加密不可用，所以不会保存。',
    'OBS-Passwort ist nicht verschlüsselt gespeichert – die Windows-Verschlüsselung ist nicht verfügbar.':
        'OBS 密码以未加密方式保存，因为 Windows 加密不可用。',
    'Spotify: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'Spotify：已连接，但只保留到你退出程序，因为 Windows 加密不可用。',
    'Unverschlüsselt gespeichert (von früher, die Windows-Verschlüsselung ist nicht verfügbar): {names}.':
        '以未加密方式保存（以前保存的，Windows 加密不可用）：{names}。',
    'YouTube: Client-Secret gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'YouTube：客户端密钥只保留到你退出程序，因为 Windows 加密不可用，所以不会保存。',
    'YouTube: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'YouTube：已连接，但只保留到你退出程序，因为 Windows 加密不可用。',
    'nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar':
        '仅限本次会话，Windows 加密不可用',
    'unverschlüsselt gespeichert (alt)':
        '以未加密方式保存（旧）',
    'verschlüsselt gespeichert':
        '已加密保存',
    'Befehlspalette':
        '命令面板',
    'Suchen':
        '搜索',
    'Vorschläge':
        '建议',
    'OBS-Verbindung':
        'OBS 连接',
    'Port und Passwort von OBS stehen unter Verbindungen → OBS-Verbindung.':
        'OBS 端口和密码在“连接 → OBS 连接”中。',
    'Qualität: {word} – {mbps} Mbit/s bei {size}':
        '画质：{word} – {size} 下 {mbps} Mbit/s',
    'Qualität: Einstellungen prüfen':
        '画质：请检查设置',
    'Qualität: gemessen wird während einer Aufnahme':
        '画质：录制时测量',
    '{words} (letzte Aufnahme)':
        '{words}（上次录像）',
    'gut':
        '良好',
    'knapp':
        '勉强',
    'matschig':
        '模糊',
    'Einstellungen prüfen':
        '请检查设置',
    'Qualität verbessern …':
        '提升画质…',
    'OBS-Werte zurücksetzen':
        '恢复 OBS 数值',
    'Aufnahmequalität':
        '录像画质',
    'In OBS einstellen':
        '在 OBS 中设置',
    'Empfohlen (in OBS einzustellen):':
        '推荐（在 OBS 中设置）：',
    'Diese Werte lassen sich nur in OBS selbst einstellen – Fog Scout zeigt, wo.':
        '这些数值只能在 OBS 中设置，Fog Scout 会告诉你在哪里设置。',
    'Einstellen geht erst nach der Aufnahme.':
        '只有在录制结束后才能更改设置。',
    'Fog Scout stellt in OBS ein (die alten Werte werden gemerkt):':
        'Fog Scout 将在 OBS 中设置（旧数值会保留）：',
    'Die OBS-Werte von vor „In OBS einstellen“ wiederherstellen?':
        '要恢复“在 OBS 中设置”之前的 OBS 数值吗？',
    'Nichts einzustellen.':
        '无需设置。',
    'OBS nimmt gerade auf – Qualität erst nach der Aufnahme einstellen.':
        'OBS 正在录制，请在录制结束后更改画质。',
    'In OBS eingestellt – OBS einmal neu starten, damit alle Werte sicher gelten.':
        '已在 OBS 中设置，请重新启动一次 OBS，确保所有数值都生效。',
    'OBS-Einstellungen zurückgesetzt.':
        'OBS 设置已恢复。',
    'OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ ist viel schärfer.':
        'OBS 以“与串流画质相同”或“小”画质录制，“几乎无损的质量”要清晰得多。',
    'OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.':
        'OBS 会缩小画面（{base} → {out}），这会使画面变软。',
    'OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.':
        'OBS 以每秒 {fps} 帧录制，60 帧在运动时看起来清晰得多。',
    'Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen.':
        'CPU 编码器跟不上（跳帧），请使用显卡的编码器。',
    'Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf CQP 18 stellen (siehe Anleitung).':
        '对于此画面码率太低，请将编码器的码率控制设为 CQP 18（见步骤）。',
    'Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf.':
        '码率刚好够用，使用 CQP 18 时快速场景中画面也能保持清晰。',
    'Ausgabeauflösung = Basisauflösung ({size})':
        '输出分辨率 = 基础分辨率（{size}）',
    'Bildrate 60':
        '帧率 60',
    'Aufnahmequalität „Kaum unterscheidbare Qualität“':
        '录像质量“几乎无损的质量”',
    'Aufnahme nicht mehr herunterskalieren':
        '停止对录像重新缩放',
    'OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:':
        'OBS → 设置 → 输出（模式“简单”） → 录像：',
    'Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“':
        '录像质量：“几乎无损的质量，文件巨大”',
    'Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden':
        '编码器：硬件（NVENC/AMD/QSV），如果可用',
    'Aufnahmeformat: MKV oder Hybrid-MP4':
        '录像格式：MKV 或混合 MP4',
    'Video: Ausgabeauflösung = Basisauflösung, Bildrate 60':
        '视频：输出分辨率 = 基础分辨率，帧率 60',
    'OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:':
        'OBS → 设置 → 输出（模式“高级”） → “录像”选项卡：',
    'Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '视频编码器：NVIDIA NVENC H.264 或 HEVC（不要选“使用串流编码器”）',
    'Ausgabe neu skalieren: aus':
        '重新缩放输出：关闭',
    'x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast':
        'x264：码率控制 CRF，数值 18，预设 veryfast',
    'Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)':
        '码率控制：CQP，CQ 级别 18（HEVC 20）',
    'Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei Durchläufe (Viertelauflösung)':
        '预设：P5: Slow（良好质量），调节：高质量，多次编码：两次（四分之一分辨率）',
    'Profil: high (HEVC: main), Keyframe-Intervall: 2 s':
        '配置：high（HEVC：main），关键帧间隔：2 秒',
    'Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.':
        '然后录制一局短对局，卡片会显示新的码率。',
    'Was die Aufnahme unscharf macht und wie OBS am besten eingestellt wird – was eine Anfrage setzen kann (Ausgabeauflösung, Bildrate, einfache Aufnahmequalität), stellt „In OBS einstellen“ ein, die alten Werte werden gemerkt.':
        '是什么让录像模糊，以及如何最好地设置 OBS。凡是能通过请求设置的（输出分辨率、帧率、简单模式的录像质量），“在 OBS 中设置”都会设置，旧数值会保留。',
    'Stellt die OBS-Werte von vor „In OBS einstellen“ wieder her.':
        '恢复“在 OBS 中设置”之前的 OBS 数值。',
    'Clips und Editor':
        '片段和编辑器',
    'Erklärung':
        '说明',
    'Sicherung und Ordner':
        '备份和文件夹',
    'Wann aufgenommen wird':
        '何时录制',
    'Video-Encoder: AMD HW H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '视频编码器：AMD HW H.264 或 HEVC（不要选“使用串流编码器”）',
    'Frequenzsteuerung: CQP, QP-Werte 18 (HEVC 20)':
        '码率控制：CQP，QP 值 18（HEVC 20）',
    'Voreinstellung: Qualität':
        '预设：Quality',
    'Video-Encoder: QuickSync H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '视频编码器：QuickSync H.264 或 HEVC（不要选“使用串流编码器”）',
    'Frequenzsteuerung: ICQ (oder CQP), Wert 18':
        '码率控制：ICQ（或 CQP），数值 18',
    'Target Usage: TU1 bis TU4 – kleiner = bessere Qualität':
        '目标用途：TU1 到 TU4，越低质量越好',
    'Video-Encoder: der Grafikkarten-Encoder (NVENC, AMF oder QuickSync), wenn OBS einen anbietet – sonst x264':
        '视频编码器：显卡的编码器（NVENC、AMF 或 QuickSync），如果 OBS 提供；否则用 x264',
    'Video-Encoder: einen eigenen wählen (nicht „Stream-Encoder verwenden“), am besten den der Grafikkarte, wenn OBS einen anbietet':
        '视频编码器：单独选择一个（不要选“使用串流编码器”），如果 OBS 提供显卡编码器则最好用它',
    'Frequenzsteuerung: gleichbleibende Qualität (CQP, CQ, ICQ oder CRF) um 18 statt einer festen niedrigen Bitrate':
        '码率控制：恒定质量（CQP、CQ、ICQ 或 CRF），约 18，而不是较低的固定码率',
    'Einschätzung aus Bitrate, Auflösung, Bildrate und Codec – Bildinhalt, Bewegung, Encoder-Voreinstellung und Quelle beeinflussen das Ergebnis.':
        '根据码率、分辨率、帧率和编解码器估算，画面内容、运动、编码器预设和源都会影响结果。',
    'Start und Meldungen':
        '启动和通知',
    'Fog Scout kann mit Windows starten und still im Infobereich (neben der Uhr) warten, bis DBD läuft. Die Lobby-Meldung sagt dir mit einem Ton, wenn ein Match gefunden wurde.':
        'Fog Scout 可以随 Windows 启动，并在通知区域（时钟旁边）静静等待，直到 DBD 运行。找到对局时，大厅通知会用声音提醒你。',
    'Optional: OBS Studio nimmt jede Runde auf, Fog Scout sagt OBS nur, wann. Ohne OBS einfach „Weiter“.':
        '可选：OBS Studio 录制每一局，Fog Scout 只告诉 OBS 何时录制。不使用 OBS 请直接点击“下一步”。',
    '1. In OBS: Werkzeuge → WebSocket-Servereinstellungen → „WebSocket-Server aktivieren“ anhaken; unter „Verbindungsinformationen anzeigen“ stehen Port und Passwort.':
        '1. 在 OBS 中：工具 → WebSocket 服务器设置 → 勾选“开启 WebSocket 服务器”；“显示连接信息”会显示端口和密码。',
    '2. Port und Passwort hier eintragen und „Verbindung testen“.':
        '2. 在这里输入端口和密码，然后点击“测试连接”。',
    '3. Einen Ordner für die Aufnahmen wählen und die Aufnahmen einschalten.':
        '3. 选择录像文件夹并开启录制。',
    'Wie scharf OBS aufnimmt, zeigt danach die Karte „Aufnahme“ auf der Seite Aufnahmen – dort auch „Qualität verbessern …“.':
        'OBS 录得有多清晰，之后会在“录像”页面的“录像”卡片中显示，那里也有“提升画质…”。',
    'Alles hier ist freiwillig und lässt sich später unter Einstellungen → Verbindungen einrichten. Jede Verbindung braucht eine eigene App-ID bzw. einen eigenen Key von dir – „Erklärung“ sagt, wo es sie gibt.':
        '这里的所有内容都是可选的，之后也可以在“设置 → 连接”中设置。每个连接都需要你自己的应用 ID 或密钥，“说明”会告诉你从哪里获取。',
    'Fog Scout kann anzeigen, mit welchem Spielserver DBD verbunden ist (Region und Ping, auch im Overlay) – dafür fragt Windows einmal nach Administratorrechten.':
        'Fog Scout 可以显示 DBD 连接的是哪个游戏服务器（区域和延迟，也会显示在悬浮窗中），为此 Windows 会请求一次管理员权限。',
    'Auf der Seite Server lässt sich ausserdem festlegen, in welchen Regionen DBD Matches sucht. Das ist freiwillig.':
        '在“服务器”页面中，你还可以选择 DBD 在哪些区域中匹配对局。这是可选的。',
    'Serverregionen auswählen …':
        '选择服务器区域…',
    'Beendet die Einrichtung und öffnet die Seite Server – dort die Regionen anhaken, in denen DBD Matches suchen soll.':
        '结束设置并打开“服务器”页面，在那里勾选 DBD 应在其中匹配对局的区域。',
    'Öffnet den Ordner mit Einstellungen, Runden, Log und Sicherungen im Explorer.':
        '在资源管理器中打开存放设置、对局、日志和备份的文件夹。',
    'Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an Claude schicken“ einschalten und einen API-Key eintragen.':
        '已关闭：请在“设置 → 连接 → Claude”中开启“将图片编辑器中的图片发送给 Claude”并输入 API 密钥。',
    'Ausschnitt ausserhalb des Bildes':
        '裁剪超出图片范围',
    'Bereich unkenntlich machen ({x} %, {y} %)':
        '遮盖一个区域（{x} %，{y} %）',
    'Bilder im Bild-Editor an Claude schicken':
        '将图片编辑器中的图片发送给 Claude',
    'Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '图片可能包含玩家名称：只有当你点击“建议”时才会发送给 Claude，经过缩小且只在内存中；已打码的区域保持打码。统计问题只发送按角色、杀手、地图、区域和时段统计的计数和比率，不发送单个对局，不发送玩家名称。',
    'Claude hat keine Antwort gegeben.':
        'Claude 没有回答。',
    'Claude zur Statistik fragen: „{q}“':
        '就统计问 Claude：“{q}”',
    'Claude: Key eingetragen, Claude ist überall aus.':
        'Claude：已输入密钥，但所有地方的 Claude 都已关闭。',
    'Das Bild hat sich inzwischen geändert – bitte neu vorschlagen.':
        '图片在此期间已更改，请重新获取建议。',
    'Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude (api.anthropic.com), verkleinert und nur im Speicher.':
        '图片可能包含玩家名称：只有在点击时才会发送给 Claude（api.anthropic.com），经过缩小且只在内存中。',
    'Das Bild lässt sich nicht für Claude verkleinern.':
        '无法为 Claude 缩小图片。',
    'Das Standbild liess sich nicht lesen – nichts gesendet.':
        '无法读取静帧，未发送任何内容。',
    'Die Statistik liess sich nicht zusammenfassen – Details im Log.':
        '无法汇总统计，详见日志。',
    'Drehung ohne Winkel':
        '旋转缺少角度',
    'Farbe ohne Werte':
        '颜色缺少数值',
    'Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %':
        '颜色：亮度 {b} %，对比度 {c} %，饱和度 {s} %',
    'In der Suche Statistik-Fragen an Claude stellen':
        '在搜索中向 Claude 提出统计问题',
    'Kasten ausserhalb des Bildes':
        '框超出图片范围',
    'Kippen':
        '垂直翻转',
    'Noch keine Runden – Claude hätte nichts zum Auswerten.':
        '还没有对局，Claude 没有可查看的内容。',
    'Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du übernimmst.':
        '将你的要求和此处显示的图片（已打码的区域保持打码）发送给 Claude；在你应用之前不会有任何更改。',
    'Schickt die Frage und Zähler/Quoten deiner Runden an Claude – keine einzelne Runde, keine Namen':
        '将问题和你对局的计数/比率发送给 Claude，不发送单个对局，不发送名称',
    'Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '同时发送播放头处的画面（经过缩小，已打码的区域保持打码），这样 Claude 可以例如为名称打码。画面可能包含玩家名称。',
    'Spiegeln':
        '镜像',
    'Spiegeln ohne Richtung':
        '镜像缺少方向',
    'Standbild mitsenden':
        '附带发送一张静帧',
    'Standbilder aus Aufnahmen im Clip-Editor an Claude schicken':
        '将片段编辑器中录像的静帧发送给 Claude',
    'Um {deg}° drehen':
        '旋转 {deg}°',
    'Vergisst den Vorschlag; das Bild bleibt, wie es ist.':
        '放弃该建议；图片保持不变。',
    'Zensur nur mit Standbild':
        '打码只能配合静帧',
    'Zensur: {style}':
        '打码：{style}',
    'Zuschneiden auf {w} × {h} %':
        '裁剪为 {w} × {h} %',
    'unbekannte Art der Zensur':
        '未知的打码方式',
    'unbekannter Schritt':
        '未知步骤',
    'z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller':
        '例如：将玩家名称像素化，裁剪为 16:9，稍微调亮',
    'zu viele Kästen':
        '框太多',
    'Zeigt im Bild-Editor den Reiter „Claude“: Du schreibst, was mit dem Bild passieren soll (Namen verpixeln, zuschneiden, heller), und auf „Vorschlagen“ gehen Bitte und Bild verkleinert an Claude. Das Bild kann Spielernamen zeigen; bereits zensierte Bereiche bleiben zensiert.':
        '在图片编辑器中显示“Claude”选项卡：你写下希望对图片做什么（将名称像素化、裁剪、调亮），点击“建议”时，你的要求和缩小后的图片会发送给 Claude。图片可能包含玩家名称；已打码的区域保持打码。',
    'Erlaubt im grossen Clip-Editor das Häkchen „Standbild mitsenden“: dann geht das Bild an der Abspielposition mit, und Claude kann z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '在大片段编辑器中允许“附带发送一张静帧”勾选项：此时播放头处的画面会一并发送，Claude 可以例如为名称打码。画面可能包含玩家名称。',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude zur Statistik fragen“. Gesendet werden deine Frage und Zähler/Quoten deiner Runden je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '在搜索（Ctrl+F）中显示“就统计问 Claude”行。发送的内容是你的问题以及按角色、杀手、地图、区域和时段统计的你的对局计数/比率，不发送单个对局，不发送玩家名称。',
    'Start: Fenster bereit nach {total} s seit Programmstart (davon {before} s bis Python).':
        '启动：程序启动后 {total} 秒窗口就绪（其中 {before} 秒用于启动 Python）。',
    'Haiku 5.5 – am günstigsten':
        'Haiku 5.5 – 最便宜',
    'Opus 5.5 – am genauesten':
        'Opus 5.5 – 最准确',
    'Sonnet 5.5 – halber Preis':
        'Sonnet 5.5 – 半价',
    'Modell':
        '模型',
    'Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat {month}. Abgerechnet wird in der Anthropic Console.':
        '费用（按标价估算）：本次会话 {n} 次请求共 {session}，本月 {month}。账单在 Anthropic Console 中。',
    'Claude: Welcher Build läuft am besten?':
        'Claude：哪套配装效果最好？',
    'Claude: Woche zusammenfassen':
        'Claude：总结本周',
    'Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?':
        '总结我这一周与上一周相比的情况：哪些变好了，哪些变差了？',
    'Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?':
        '我的哪些技能效果最好？杀手和幸存者分开说。',
    'Fog Scout ist abgestürzt':
        'Fog Scout 已崩溃',
    'Fog Scout wurde am {when} unerwartet beendet. „Diagnose kopieren“ legt einen Bericht mit den Stellen des Absturzes in die Zwischenablage – zum Melden auf GitHub oder im Chat. Der Bericht enthält keine Schlüssel, Titel oder Server-Adressen.':
        'Fog Scout 于 {when} 意外结束。“复制诊断信息”会将一份包含崩溃位置的报告放到剪贴板，可在 GitHub 或聊天中报告。报告中不包含密钥、标题或服务器地址。',
    'Claude hat keine Stelle gefunden, die heraussticht.':
        'Claude 没有找到突出的时刻。',
    'Claude sieht sich {n} Standbilder an …':
        'Claude 正在查看 {n} 张静帧…',
    'Highlights finden':
        '查找精彩时刻',
    'Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu drei Stellen für einen Short. Die Bilder können Spielernamen zeigen.':
        '将剪辑的小静帧（均匀分布以及位于 F8 标记处，已打码的区域保持打码）发送给 Claude；Claude 会为短视频指出最多三个时刻。图片可能包含玩家名称。',
    'Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ ändert den Schnitt.':
        '建议只保留这一部分，只有“应用”才会更改剪辑。',
    'Namen beim Zuschauen':
        '观战时的名称',
    'Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und den Namen oben in der Mitte – bei Bedarf verschieben.':
        '在 DBD 观战时显示名称的位置放置框：左侧较高处的列表，以及顶部中间的名称，需要时可移动。',
    'Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        '在对局中 DBD 显示幸存者名称的位置（游戏画面左下角）放置一个框，需要时可移动。',
    'Aufnahme zeigen':
        '显示录像',
    'Aufnahme abspielen':
        '播放录像',
    'Zu dieser Runde gibt es keine Aufnahme.':
        '此对局没有录像。',
    'Die Aufnahme dieser Runde ist durch die Filter der Seite Aufnahmen ausgeblendet.':
        '此对局的录像被“录像”页面的筛选条件隐藏了。',
    'Sitzungen':
        '游戏时段',
    'Killer/Survivor':
        '杀手/幸存者',
    '{n} K':
        '{n} 杀手',
    '{n} S':
        '{n} 幸存者',
    'Ø Dauer einer Sitzung':
        '平均时段时长',
    'Ø Runden je Sitzung':
        '每个时段平均对局数',
    'Ø Warten':
        '平均等待',
    'Eine Sitzung endet nach {n} Minuten ohne Runde. Es gelten die Filter oben – mit einem Rollenfilter zählt eine Sitzung nur die Runden dieser Rolle. Ø Kills, Entkommen und BP laut Stats-Seite. Doppelklick zeigt die Runden der Sitzung unter „Letzte Runden“.':
        '{n} 分钟内没有对局即视为一个游戏时段结束。上方的筛选条件适用：使用角色筛选时，一个时段只统计该角色的对局。平均击杀、逃脱和血点来自统计页面。双击会在“最近对局”下显示该时段的对局。',
    'Blutpunkte-Stand – letzter Wert {per}':
        '血点余额 – 最后数值{per}',
    'Cap erreicht':
        '已达上限',
    'Cap in ≈ {n} Runden':
        '约 {n} 局后达到上限',
    'Cap: {cap}':
        '上限：{cap}',
    'Noch kein Blutpunkte-Stand gelesen – er kommt aus der Lobby nach der Runde.':
        '尚未读取到血点余额，它会在对局结束后从大厅读取。',
    '{when}: Stand {bp} BP':
        '{when}：余额 {bp} 血点',
    '+{n} Level':
        '+{n} 级',
    '+{n} P':
        '+{n} 威望',
    'Eine Zeile oben anklicken, um den Verlauf zu sehen.':
        '单击上方某一行可查看趋势。',
    'Keine Matches mit Prestige in dieser Auswahl.':
        '此筛选范围内没有带威望的比赛。',
    'Level':
        '等级',
    'Matches':
        '比赛',
    'Noch kein Prestige in dieser Auswahl – es kommt aus den Match-Daten (Userscript ab Version 3).':
        '此筛选范围内尚无威望，它来自比赛数据（用户脚本版本 3 或更新）。',
    'Prestige':
        '威望',
    'Prestige und Level deiner Charaktere laut Stats-Seite (ab Userscript Version 3). „Prestige“ und „Level“ = der neueste Stand; „Zuwachs“ und „Matches“ gelten für die Filter oben. Eine Zeile anklicken zeigt darunter den Verlauf dieses Charakters. „Tempo“ = gewonnene Level pro Woche aus den Matches der letzten {days} Tage, „Nächstes P“ = wie lange es bei diesem Tempo bis zur nächsten Stufe dauert. Level steigen nur, wenn du Blutpunkte im Blutnetz ausgibst – die Prognose sagt, was bisher geschah, keine Zusage. „Main“ = dein Charakter mit den meisten Matches je Rolle. „P100“ und „Höchster“ zählen nur Charaktere, die in deinen Match-Daten vorkommen.':
        '来自统计页面的你的人物威望和等级（用户脚本版本 3 或更新）。“威望”和“等级” = 最新状态；“提升”和“比赛”遵循上方的筛选条件。单击某一行可在下方查看该人物的趋势。“速度” = 根据最近 {days} 天的比赛计算的每周提升等级数，“下一威望” = 按此速度达到下一级威望需要多长时间。只有在血网中花费血点时等级才会提升，预测只说明到目前为止的情况，不作任何保证。“主玩” = 每个阵营中比赛最多的人物。“P100”和“最高”只统计出现在你的比赛数据中的人物。',
    'Prestige von {name} {per}':
        '{name} 的威望{per}',
    'Zuletzt':
        '最近一次游玩',
    'Zuwachs':
        '提升',
    '{when}: Prestige {p} · Level {level}':
        '{when}：威望 {p} · 等级 {level}',
    '+{n} weitere':
        '另有 {n} 个',
    'Charaktere':
        '人物',
    'Höchster':
        '最高',
    'Level diese Woche':
        '本周等级',
    'Main':
        '主玩',
    'Meilenstein: {name} ist jetzt Prestige {p}':
        '里程碑：{name} 现在是威望 {p}',
    'Nächstes P':
        '下一威望',
    'P100 erreicht':
        '已达到 P100',
    'Prestige gesamt':
        '威望总计',
    'alle Charaktere':
        '所有人物',
    'seit Montag':
        '自周一起',
    '{k} Killer · {s} Survivor':
        '{k} 杀手 · {s} 幸存者',
    '{name} ist jetzt Prestige {p}':
        '{name} 现在是威望 {p}',
    '{name} · Level {level}':
        '{name} · 等级 {level}',
    '{n} Level/Woche':
        '{n} 级/周',
    '≈ 1 Tag':
        '约 1 天',
    '≈ 1 Woche':
        '约 1 周',
    '≈ {n} Tage':
        '约 {n} 天',
    '≈ {n} Wochen':
        '约 {n} 周',
    '{n} Charaktere':
        '{n} 个人物',
    'P100':
        'P100',
    '{n}× Killer':
        '{n} 次杀手',
    '{n}× Survivor':
        '{n} 次幸存者',
    '{n}× Farming':
        '{n} 次刷分',
    '{n}× Custom Game':
        '{n} 次自定义对局',
    '{n}× ohne Rolle':
        '{n} 次无角色',
    'Zeigt, was diese Kachel zählt':
        '显示此卡片统计的内容',
    'Diese Runden sind durch die Filter der Statistik ausgeblendet.':
        '这些对局被统计的筛选条件隐藏了。',
    'Automatisch (zuletzt benutztes Gerät)':
        '自动（最近使用的设备）',
    'Dunkle Fläche hinter den Eingaben':
        '输入后面的深色背景',
    'EINGABEN':
        '输入',
    'Eingaben im Spiel':
        '游戏中的输入',
    'Eingaben im Spiel zeigen (Tasten, Maus, Gamepad)':
        '在游戏中显示输入（按键、鼠标、手柄）',
    'Gamepad':
        '手柄',
    'Gerät':
        '设备',
    'Tastatur und Maus':
        '键盘和鼠标',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter den Tasten.':
        '在按键后面加一块带圆角的半透明深色背景。',
    'wartet auf eine Runde':
        '正在等待对局',
    'Eingaben mit der Aufnahme speichern (für den Clip-Editor)':
        '随录像保存输入（供片段编辑器使用）',
    'Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). Eine offizielle Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.':
        'Fog Scout 只显示以下按键中当前按住了哪些：W、A、S、D、Q、E、R、Space、Shift、Ctrl、鼠标按键和手柄（按键、扳机、摇杆）。只在对局中且 DBD 为活动窗口时读取，Fog Scout 绝不会看到你在其他程序中的输入。这些内容不会写入日志或发送出去，也不会传给游戏；开启“随录像保存输入”后，一局的按键会作为文件保存在其 OBS 录像旁边（供片段编辑器使用）。Behaviour 并未正式批准此类显示；它们在游戏中不提供任何优势。',
    'Gelesen werden nur W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad – nur während einer Runde und nur, solange DBD vorne ist. Gesendet wird nichts; gespeichert nur mit dem Häkchen oben, als Datei neben der eigenen Aufnahme.':
        '只读取 W、A、S、D、Q、E、R、Space、Shift、Ctrl、鼠标按键和手柄，只在对局中且 DBD 处于前台时读取。不发送任何内容；只有勾选上方的框时才会保存，作为文件放在你自己的录像旁边。',
    'Eine Karte im Spiel zeigt, welche Tasten, Maustasten oder Gamepad-Knöpfe du gerade drückst – wie bei Streamern. Gelesen wird nur eine feste Liste von Tasten, nur während einer Runde und nur, solange DBD vorne ist; gesendet wird nichts, gespeichert nur mit „Eingaben mit der Aufnahme speichern“.':
        '游戏中的一张卡片会显示你当前按下了哪些按键、鼠标按键或手柄按键，就像主播那样。只读取一份固定的按键列表，只在对局中且 DBD 处于前台时读取；不发送任何内容，只有开启“随录像保存输入”时才会保存。',
    'Mit OBS-Aufnahmen: die gedrückten Tasten der Runde kommen als kleine Datei neben die Aufnahme – der Clip-Editor zeigt sie als Spur und kann die Karte ins Video einbrennen. Die Datei wird mit der Aufnahme verschoben und gelöscht.':
        '使用 OBS 录像时：对局中按住的按键会保存到录像旁边的一个小文件中，片段编辑器会将其显示为一条轨道，并可将卡片烧录到视频中。该文件会随录像一起移动和删除。',
    'Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme speichern“). Clips aus F8 haben keine.':
        '来自录像旁边的文件（悬浮窗 › 输入 › “随录像保存输入”）。F8 片段没有该文件。',
    'Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet).':
        '带有对局中按住按键的卡片会进入完成的视频，位于所选的角落，与剪辑同步（包括速度和倒放）。',
    'Dunkle Fläche hinter den Tasten':
        '按键后面的深色背景',
    'Ecke':
        '角落',
    'Eine halb durchsichtige dunkle Fläche hinter der Karte.':
        '在卡片后面加一块半透明深色背景。',
    'Eingaben im Export zeigen':
        '在导出中显示输入',
    'Höhe der Karte im Verhältnis zur Bildhöhe.':
        '卡片高度相对于画面高度的比例。',
    'Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade benutzt wurde.':
        '卡片显示哪种视图，自动选择刚刚使用的设备。',
    'Wo die Karte im Bild liegt.':
        '卡片在画面中的位置。',
    'Claude baut einen Short aus {n} Standbildern …':
        'Claude 正在用 {n} 张静帧制作短视频…',
    'Clip um Moment':
        '围绕时刻的片段',
    'Der Schnitt hat sich inzwischen geändert – bitte noch einmal.':
        '剪辑在此期间已更改，请重试。',
    'Der Schnitt wird der markierte Moment ({before} s davor bis {after} s danach).':
        '剪辑变为所选时刻（之前 {before} 秒到之后 {after} 秒）。',
    'Die Bilder liessen sich nicht lesen.':
        '无法读取图片。',
    'F8-Marke':
        'F8 标记',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden.':
        '现在无法执行，请先完成当前编辑。',
    'Kein Ladebildschirm am Anfang oder Ende gefunden.':
        '开头或结尾没有找到加载界面。',
    'Kein Leerlauf gefunden.':
        '没有找到空闲片段。',
    'Ladebildschirm abschneiden':
        '剪掉加载界面',
    'Leerlauf kürzen':
        '修剪空闲时间',
    'Momente':
        '时刻',
    'Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst „Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen.':
        '将找到的时刻处的静帧（根据按键、游戏声音和 F8 标记，仅以数字表示）和剪辑发送给 Claude；Claude 会建议一个完整的短视频：范围、慢动作、标题、字幕。只有“应用”才会更改剪辑。图片可能包含玩家名称。',
    'Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war (aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.':
        '剪掉至少 {n} 秒内没有按住任何按键的部分（根据录像的输入），一个撤销步骤。',
    'Sehe mir Anfang und Ende an …':
        '正在查看开头和结尾…',
    'Short vorschlagen':
        '建议短视频',
    'Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.':
        '查看开头和结尾的 {n} 秒，剪掉黑屏的开头或结尾，一个撤销步骤。',
    'laut':
        '响亮',
    'viele Tasten':
        '按键多',
    '{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z macht es rückgängig.':
        '已修剪 {n} 段空闲片段（{seconds} 秒），Ctrl+Z 可撤销。',
    '{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – Strg+Z macht es rückgängig.':
        '已剪掉 {n} 段黑屏片段（{seconds} 秒），Ctrl+Z 可撤销。',
    'Anordnen':
        '排列',
    'Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · Tab = nächstes Element · Esc = fertig':
        '排列中（游戏中也可以）：拖动元素 · 方向键 = 微调（Shift = 10 像素） · Tab = 下一个元素 · Esc = 完成',
    'Anordnen: alle Elemente mit der Maus ziehen – in der Vorschau und direkt im Spiel. Strg+Mausrad ändert die Grösse, Esc beendet.':
        '排列：用鼠标拖动每个元素，在预览中和游戏中都可以。Ctrl+滚轮更改大小，Esc 结束。',
    'Automatisch: im schwarzen Rand neben dem Spielbild bzw. neben dem DBD-Fenster. Frei platzieren: „Anordnen“ oder eine Schnellposition.':
        '自动：位于游戏画面旁的黑边中或 DBD 窗口旁边。如需自由放置：“排列”或快速位置。',
    'CPU, GPU, RAM':
        'CPU、GPU、RAM',
    'Callout-Karte der Map':
        '当前地图的标注地图',
    'Die Linien in der Vorschau mit „Anordnen“ ziehen – Karte, Systemwerte, Heute und Musik bleiben im Balken dazwischen.':
        '使用“排列”在预览中拖动这些线，地图、系统数值、今日和音乐会保持在黑边中两线之间。',
    'Ein- oder ausblenden':
        '显示或隐藏',
    'Elemente':
        '元素',
    'Entsperren: wieder verschiebbar':
        '解锁：可以再次移动',
    'Fokus':
        '焦点',
    'Frei platzieren: „Anordnen“, eine Schnellposition oder Vorgabe „eigene Position“.':
        '如需自由放置：“排列”、快速位置或设置“自定义位置”。',
    'Gesperrt – erst entsperren':
        '已锁定，请先解锁',
    'Gilt für alle Elemente':
        '适用于所有元素',
    'Grenzen und Platz':
        '边界和空间',
    'Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen':
        '边界线：拖到黑边中元素可以到达的位置',
    'Grösse und Deckkraft':
        '大小和不透明度',
    'Grösse von {name}: Ecke ziehen':
        '{name} 的大小：拖动角落',
    'Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, Rechtsklick = Menü. Ende mit „Fertig“ oder Esc.':
        '单击元素即可选中它。使用“排列”时：拖动元素 = 移动（虚线框显示其落点），拖动其角落或 Ctrl+滚轮 = 大小，右键单击 = 菜单。用“完成”或 Esc 结束。',
    'Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel':
        '单击选中元素 · “排列”开启移动，在这里和游戏中都可以',
    'Klick wählt {name}':
        '单击选中 {name}',
    'Layout für {size}':
        '{size} 的布局',
    'Läuft gerade':
        '正在播放',
    'Mitte':
        '中间',
    'Nach {where} legen (mit Rand)':
        '放到{where}（留有边距）',
    'Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein).':
        '位置和大小按 DBD 窗口大小分别保存（“常规”选项卡）。',
    'Runden und Zeit heute':
        '今日对局和时间',
    'Schnellposition':
        '快速位置',
    'Sperren':
        '锁定',
    'Sperren: im Modus „Anordnen“ nicht mehr verschiebbar':
        '锁定：在“排列”中不再移动',
    'Stil, Abstand, Grenzen, Discord':
        '样式、间距、边界、Discord',
    'Tasten und Gamepad':
        '按键和手柄',
    'Timer, Bilanz, Server':
        '计时器、战绩、服务器',
    'Verhalten':
        '行为',
    'Zeilen':
        '行',
    'Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)':
        '回到自动位置（在黑边中，其他元素旁边）',
    'eigener Platz':
        '自定义位置',
    'eingerastet':
        '已吸附',
    'graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '黑边中的灰线 = 边界（关闭），拖动其中一条即可开启',
    'links Mitte':
        '左侧中间',
    'oben Mitte':
        '顶部中间',
    'rastet an Mitte, Balken und anderen ein (Alt = frei)':
        '吸附到中间、黑边和其他元素（Alt = 自由）',
    'rechts Mitte':
        '右侧中间',
    'unten Mitte':
        '底部中间',
    '{name} entsperrt.':
        '{name} 已解锁。',
    '{name} gesperrt – bleibt beim Anordnen, wo es ist.':
        '{name} 已锁定，排列时保持原位。',
    '{name} ist gesperrt – das Schloss in der Liste löst es':
        '{name} 已锁定，列表中的锁可将其解锁',
    '{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü':
        '{name}：拖动 = 移动 · 角落或 Ctrl+滚轮 = 大小 · 右键单击 = 菜单',
    'Üblicher Platz':
        '常规位置',
    '„Overlay testen“ zeigt die Karte sofort, mit „Anordnen“ ziehst du sie hin.':
        '“测试悬浮窗”会立即显示地图，使用“排列”可将其拖到那里。',
    'Nur die Vorschau: Liste und Einstellungen weg, die Navigation schmal – die ganze Fläche zum Anordnen. Esc oder nochmal klicken beendet es.':
        '仅预览：列表和设置隐藏，导航变窄，整个区域用于排列。按 Esc 或再次单击结束。',
    'Englisch':
        '英语',
    'Deutsch':
        '德语',
    'Französisch':
        '法语',
    'Spanisch':
        '西班牙语',
    'Spanisch (Mexiko)':
        '西班牙语（墨西哥）',
    'Italienisch':
        '意大利语',
    'Polnisch':
        '波兰语',
    'Portugiesisch (Brasilien)':
        '葡萄牙语（巴西）',
    'Türkisch':
        '土耳其语',
    'Spielsprache selbst erkennen und anhaken':
        '自动识别并勾选游戏语言',
    'Spielsprache {lang} erkannt (Banner „{text}“) – automatisch angehakt.':
        '已识别游戏语言{lang}（横幅“{text}”）——已自动勾选。',
    'Läuft DBD in einer Sprache, die hier nicht angehakt ist, und passt ein Map-Banner eindeutig zu einer Map in dieser Sprache, hakt Fog Scout sie selbst an – die Karte erscheint dann schon in derselben Runde. Nur am Rundenstart, nie mitten im Match.':
        '如果 DBD 使用的语言未在此勾选，而地图横幅明确对应该语言中的某张地图，Fog Scout 会自动勾选该语言——地图会在同一局中显示。仅在对局开始时进行，绝不会在对局中途进行。',
}
