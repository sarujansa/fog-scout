"""Japanese texts (1.47): the German text of the code is the key, as in i18n_en.EN – a text missing here
shows in English (i18n.table). Made from the English texts; tests/test_i18n.py checks keys and placeholders."""
T = {
    'Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\nKurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden.':
        'Fog Scout は既に起動していますが、応答がありません（または終了処理中です）。\n\nしばらく待ってから再度起動してください。それでも解決しない場合は、タスクマネージャーの「詳細」で「{exe}」（Fog Scout）を終了してください。',
    'Fog Scout konnte nicht neu gestartet werden: Die alte Kopie läuft noch im Hintergrund.\n\nIm Task-Manager unter „Details“ „{exe}“ (Fog Scout) beenden und das Programm neu starten.':
        'Fog Scout を再起動できませんでした：古いプロセスがまだバックグラウンドで動作しています。\n\nタスクマネージャーの「詳細」で「{exe}」（Fog Scout）を終了してから、プログラムを再度起動してください。',
    'Start fehlgeschlagen:':
        '起動に失敗しました：',
    'Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt unverändert.':
        'これまで Fog Scout は start.bat から使用されていました：\n{folder}\n\n設定、ラウンド、マッチデータ、バックアップ、独自のマップ画像をインストール版に引き継ぎますか？古いフォルダーは変更されません。',
    'Übernahme fehlgeschlagen: {error}':
        '引き継ぎに失敗しました：{error}',
    'Kein Windows: Fenstersuche, Hotkeys und Click-Through sind nur unter Windows aktiv.':
        'Windows ではありません：ウィンドウ検索、ホットキー、クリック透過は Windows でのみ動作します。',
    'Bereit. {n} Maps geladen, Spielsprachen: {langs}.':
        '準備完了。{n} 個のマップを読み込みました。ゲーム言語：{langs}。',
    'Bildschirm {w}×{h} ohne schwarze Balken neben dem Spielbild: Systemwerte, „Heute“ und Musik im Spiel sind ausgeschaltet (sie lägen sonst auf dem Spielbild) – einschalten auf der Seite Overlay.':
        '画面 {w}×{h} でゲーム画面の横に黒帯がありません：ゲーム内のシステム値、「今日」、音楽はオフになりました（ゲーム画面に重なるため）。オーバーレイページでオンにできます。',
    'Automatisch (Windows-Sprache)':
        '自動（Windows の言語）',
    'Erkennung':
        '検出',
    'Overlay':
        'オーバーレイ',
    'System':
        'システム',
    'Fehler':
        'エラー',
    'automatisch':
        '自動',
    'oben links':
        '左上',
    'oben rechts':
        '右上',
    'unten links':
        '左下',
    'unten rechts':
        '右下',
    'eigene Position':
        'カスタム位置',
    'Karte ein/aus':
        'マップ オン/オフ',
    'Layout-Variante':
        'レイアウトの種類',
    'Bildschirm scannen':
        '画面をスキャン',
    'Vorherige Map':
        '前のマップ',
    'Nächste Map':
        '次のマップ',
    'Grösser':
        '大きく',
    'Kleiner':
        '小さく',
    'Mit Maus verschieben':
        'マウスで移動',
    'Noch keine Map':
        'まだマップがありません',
    'Karte ausblenden':
        'マップを非表示',
    'Karte einblenden':
        'マップを表示',
    'Scannen':
        'スキャン',
    'Overlay testen':
        'オーバーレイをテスト',
    'Test beenden':
        'テストを終了',
    'Bild hinzufügen …':
        '画像を追加…',
    'Zuordnen …':
        '割り当て…',
    'Server':
        'サーバー',
    'Einstellungen':
        '設定',
    'Layout {n} von {total}':
        'レイアウト {n} / {total}',
    '(unsicher)':
        '（不確実）',
    'manuell gewählt':
        '手動で選択',
    'per Scan gefunden':
        'スキャンで検出',
    'Letzte Runde: {time}':
        '前回のラウンド：{time}',
    'Unbekannte Map gelesen: „{text}“':
        '不明なマップ名を読み取りました：「{text}」',
    'Im Menü – Karte pausiert ({map})':
        'メニュー中 – マップを一時停止（{map}）',
    'Runde vorbei – wartet auf das nächste Match':
        'ラウンド終了 – 次のマッチを待機中',
    'Karte ausgeblendet ({map})':
        'マップ非表示（{map}）',
    'Wartet auf DBD':
        'DBD を待機中',
    'DBD läuft – automatische Erkennung ist aus (Map von Hand wählen)':
        'DBD は起動中 – 自動検出はオフです（マップを手動で選択してください）',
    'Wartet auf das nächste Match':
        '次のマッチを待機中',
    'Simulation – wartet auf das Map-Banner':
        'シミュレーション – マップバナーを待機中',
    'Im Match: {map}':
        'マッチ中：{map}',
    'Karte eingeblendet':
        'マップを表示中',
    'Kartenbild hinzufügen …':
        'マップ画像を追加…',
    'eigenes Bild für eine Map (Hintergrund wird entfernt)':
        'マップ用の独自画像（背景は除去されます）',
    'Eigene Bilder':
        '独自の画像',
    'Position':
        '位置',
    'Zurücksetzen':
        'リセット',
    'Horizontal':
        '水平',
    'Vertikal':
        '垂直',
    'Fertig':
        '完了',
    '0 % = links/oben, 100 % = rechts/unten':
        '0 % = 左/上、100 % = 右/下',
    'Karte im schwarzen Rand halten':
        'マップを黒帯の中に収める',
    'Darstellung':
        '外観',
    'Grösse':
        'サイズ',
    'Karte anzeigen':
        'マップを表示する',
    'Karte im Overlay eingeblendet.':
        'オーバーレイにマップを表示します。',
    'Karte im Overlay aus – es werden nur Timer, Ort und Ping angezeigt.':
        'オーバーレイのマップはオフ – タイマー、場所、Ping のみ表示されます。',
    'nichts anzuzeigen':
        '表示するものがありません',
    'Aus: Das Overlay zeigt nur Rundentimer, Serverregion und Ping – ohne Karte. Erkennung, Rundenende und Statistik laufen wie gewohnt.':
        'オフ：オーバーレイにはマップなしで、ラウンドタイマー、サーバーリージョン、Ping のみ表示されます。検出、ラウンド終了、統計は通常どおり動作します。',
    'Für diese Map zurücksetzen':
        'このマップをリセット',
    'eigene Grösse {n} % (Hotkeys/Strg+Mausrad)':
        '個別サイズ {n} %（ホットキー/Ctrl+ホイール）',
    'gedreht um {deg}°':
        '{deg}° 回転',
    'Killer':
        'キラー',
    'Survivor':
        'サバイバー',
    'Rolle':
        '役割',
    'Rolle: {role}':
        '役割：{role}',
    'Alle Rollen':
        'すべての役割',
    'Custom Game':
        'カスタムマッチ',
    'Custom Games':
        'カスタムマッチ',
    'Farming':
        'ファーミング',
    'Stil':
        'スタイル',
    'Original':
        'オリジナル',
    'Dunkel':
        'ダーク',
    'Die Karten mit lila Boden, wie sie mitgeliefert werden – gilt auch im Spiel.':
        '紫の床のマップをそのままの状態で表示します – ゲーム内にも適用されます。',
    'Klassisch':
        'クラシック',
    'Glas-Karten':
        'ガラスカード',
    'Chips & Icons':
        'チップとアイコン',
    'Minimal Line':
        'ミニマルライン',
    'SYSTEM':
        'システム',
    'Farming an/aus':
        'ファーミング オン/オフ',
    'Farming-Runden':
        'ファーミングラウンド',
    'Runden ohne Crossplay als Farming zählen':
        'クロスプレイなしのラウンドをファーミングとして数える',
    'Alle Runden auf':
        'すべてのラウンドで有効',
    'Farming-Runden zählen in Statistik und Aufnahmen überall mit; das Häkchen „Farming ausblenden“ (bei den Filtern) hält sie heraus, der Reiter Statistik → Farming listet sie immer. Crossplay aus erkennt das Programm an der Weltkugel mit rotem Kreuz neben dem Lobby-Knopf; Runden auf der gewählten Region zählen immer als Farming, auch ältere. Einzelne Runden: „Farming an/aus“ unter „Letzte Runden“.':
        'ファーミングラウンドは統計と録画のすべてで数えられます。フィルターの横にある「ファーミングを除外」で除外でき、「統計」→「ファーミング」タブには常に一覧表示されます。クロスプレイのオフは、ロビーボタンの横にある赤い×印の付いた地球アイコンから読み取ります。選択したリージョンのラウンドは、過去のものも含め常にファーミングとして数えられます。個別のラウンド：「最近のラウンド」の「ファーミング オン/オフ」。',
    '{map} ({when}) zählt jetzt als Farming-Runde.':
        '{map}（{when}）をファーミングラウンドとして数えるようになりました。',
    '{map} ({when}) zählt wieder als normale Runde.':
        '{map}（{when}）を再び通常のラウンドとして数えます。',
    'Hinweis: Runden auf {region} zählen laut Einstellung weiter als Farming.':
        '注意：{region} のラウンドは設定により引き続きファーミングとして数えられます。',
    'Crossplay war aus – die Runde zählt als Farming-Runde.':
        'クロスプレイがオフでした – このラウンドはファーミングラウンドとして数えられます。',
    'Crossplay war aus, die Lobby sah aus wie ein Custom Game – die Runde zählt als Farming-Runde, sobald die Stats-Seite sie als öffentliches Match zeigt.':
        'クロスプレイがオフで、ロビーはカスタムマッチのように見えました – 統計ページで公開マッチと表示されれば、このラウンドはファーミングラウンドとして数えられます。',
    '{off} von {n} Blicken mit Kreuz':
        '{n} 回中 {off} 回、×印あり',
    'letzter Blick':
        '最後の確認',
    'Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.':
        'クロスプレイはオフです（{looks}）– 次のラウンドはファーミングラウンドとして数えられます。',
    'Crossplay ist an ({looks}) – keine Farming-Runde.':
        'クロスプレイはオンです（{looks}）– ファーミングラウンドではありません。',
    'Als Custom Game erkannt – die Runde zählt nicht als Farming (unter „Letzte Runden“ mit „Farming an/aus“ korrigierbar).':
        'カスタムマッチとして認識されました – このラウンドはファーミングとして数えられません（「最近のラウンド」の「ファーミング オン/オフ」で修正できます）。',
    'Keine Lobby zur Runde ({why}) – sie zählt nicht als Farming.':
        'このラウンドのロビーがありません（{why}）– ファーミングとして数えられません。',
    'Lobby zu alt':
        'ロビーが古すぎます',
    'Lobby nicht gesehen':
        'ロビーが確認されていません',
    'Diese Runde als Farming-Runde zählen bzw. wieder als normale Runde – Farming-Runden zählen überall mit, bis „Farming ausblenden“ sie heraushält; der Reiter „Farming“ listet sie immer. Runden auf der Farming-Region (Einstellungen → Match-Daten) bleiben Farming.':
        'このラウンドをファーミングラウンドとして、または再び通常のラウンドとして数えます – ファーミングラウンドは「ファーミングを除外」で除外しない限りすべてで数えられ、「ファーミング」タブには常に一覧表示されます。ファーミングリージョン（設定 → マッチデータ）のラウンドはファーミングのままです。',
    'Farming ausblenden':
        'ファーミングを除外',
    'An: Farming-Runden (Crossplay aus, Farming-Region, Farming-Gegner) bleiben aus Statistik, Aufnahmen und Clips draussen – ein Schalter für alle drei. Aus: sie zählen wie jede andere Runde. Der Reiter Statistik → Farming zeigt sie immer.':
        'オン：ファーミングラウンド（クロスプレイオフ、ファーミングリージョン、ファーミング仲間）を統計、録画、クリップから除外します – 3 つすべてに共通のスイッチです。オフ：他のラウンドと同様に数えます。「統計」→「ファーミング」タブには常に表示されます。',
    'Zeigt die Lobby die Weltkugel mit rotem Kreuz (Crossplay aus), zählt die nächste Runde als Farming-Runde.':
        'ロビーに赤い×印の付いた地球アイコン（クロスプレイオフ）が表示されている場合、次のラウンドはファーミングラウンドとして数えられます。',
    'Custom Game – keine Wartezeit.':
        'カスタムマッチ – 待ち時間なし。',
    'Suche läuft: {time}':
        '検索中：{time}',
    'Suche nach einem Match gestartet.':
        'マッチの検索を開始しました。',
    'Lobby verlassen – sie zählt für keine Runde.':
        'ロビーを離れました – どのラウンドにも数えられません。',
    'Suche abgebrochen.':
        '検索をキャンセルしました。',
    'Lobby gefunden nach {time}{role}.':
        '{time} 後にロビーが見つかりました{role}。',
    'Lobby gefunden{role}.':
        'ロビーが見つかりました{role}。',
    'Lobby nur kurz gesehen – Rolle und Crossplay von dort, ohne Wartezeit.':
        'ロビーは一瞬しか確認できませんでした – 役割とクロスプレイはそこから取得、待ち時間はなし。',
    'Wartezeit {time}':
        '{time} 待機',
    'Verbindung in dieser Runde: {n} × Aussetzer, längster {s} s.':
        'このラウンドの接続：途切れ {n} 回、最長 {s} 秒。',
    '{n}× Aussetzer':
        '途切れ {n} 回',
    'Ergebnisbildschirm (zweiter Blick): gespielt als {role}.':
        'リザルト画面（2 回目の確認）：{role} としてプレイ。',
    'Ergebnisbildschirm: gespielt als {role}.':
        'リザルト画面：{role} としてプレイ。',
    'Wartezeit':
        '待ち時間',
    'Regionen':
        'リージョン',
    'Markierte Runde:':
        '選択したラウンド：',
    'Benachrichtigungen':
        '通知',
    'Runde auf {map} nicht gezählt: ihr Ende wurde nicht erkannt.':
        '{map} のラウンドは数えられませんでした：終了が検出されませんでした。',
    'Einstellungen exportieren …':
        '設定をエクスポート…',
    'Einstellungen importieren …':
        '設定をインポート…',
    'Einstellungen exportieren':
        '設定をエクスポート',
    'Einstellungen importieren':
        '設定をインポート',
    'Export fehlgeschlagen: {error}':
        'エクスポートに失敗しました：{error}',
    'Einstellungen gesichert: {path}':
        '設定を保存しました：{path}',
    'Das ist keine Einstellungsdatei von Fog Scout ({error}).':
        'これは Fog Scout の設定ファイルではありません（{error}）。',
    'Alle Einstellungen durch die aus der Datei ersetzen? Das Programm startet danach neu.':
        'すべての設定をファイルの設定で置き換えますか？その後プログラムが再起動します。',
    'Einstellungen importiert aus {path}.':
        '{path} から設定をインポートしました。',
    'Bitte das Programm jetzt neu starten.':
        '今すぐプログラムを再起動してください。',
    'Speichert alle Einstellungen in eine Datei: Hotkeys, Grösse und Drehung pro Map, eigene Map-Zuordnungen, Overlay, Regionen … Die Statistik (rounds.jsonl) gehört nicht dazu.':
        'すべての設定をファイルに保存します：ホットキー、マップごとのサイズと回転、独自のマップ割り当て、オーバーレイ、リージョン…統計（rounds.jsonl）は含まれません。',
    'Lädt eine exportierte Einstellungsdatei und startet das Programm neu. Fehlende Werte (ältere Sicherung) bekommen ihren Standard.':
        'エクスポートした設定ファイルを読み込み、プログラムを再起動します。不足している値（古いバックアップ）は既定値になります。',
    'Ton und Meldung, wenn eine Lobby gefunden wurde':
        'ロビーが見つかったら音と通知で知らせる',
    'Erinnern, wenn der Lobby-Countdown abläuft und READY noch nicht gedrückt ist':
        'ロビーのカウントダウンが終わりそうなのに READY が押されていない場合に知らせる',
    'Nur wenn DBD nicht das aktive Fenster ist':
        'DBD がアクティブウィンドウでない場合のみ',
    'Die Meldung erscheint unten rechts über allen Fenstern – auch bei „Nicht stören“ – und nimmt dem aktiven Fenster nicht den Fokus. Klick darauf schliesst sie.':
        '通知は右下にすべてのウィンドウの上に表示され（「応答不可」中も）、アクティブウィンドウのフォーカスを奪いません。クリックすると閉じます。',
    'Meldung testen':
        '通知をテスト',
    'Zeigt die Meldung und spielt den Ton – so siehst du, wo sie erscheint.':
        '通知を表示して音を鳴らします – 表示される場所を確認できます。',
    'Lobby gefunden':
        'ロビーが見つかりました',
    'nach {time}':
        '{time} 後',
    'READY drücken.':
        'READY を押してください。',
    'Lobby startet gleich':
        'まもなくロビーが開始します',
    'Noch {n} s – READY ist noch nicht gedrückt.':
        '残り {n} 秒 – READY がまだ押されていません。',
    'Lobby-Countdown läuft ab, READY ist noch nicht gedrückt.':
        'ロビーのカウントダウンが終わりそうですが、READY が押されていません。',
    'Ø Ping':
        '平均 Ping',
    'Spielt einen Hinweiston und zeigt eine Windows-Meldung, sobald DBD eine Lobby gefunden hat – praktisch, wenn du während der Suche etwas anderes machst.':
        'DBD がロビーを見つけるとすぐに音を鳴らし、Windows の通知を表示します – 検索中に別のことをしているときに便利です。',
    'Noch einmal melden, wenn der Countdown der Lobby unter 15 s fällt und du READY nicht gedrückt hast.':
        'ロビーのカウントダウンが 15 秒を切っても READY を押していない場合に、再度通知します。',
    'Keine Meldung, solange DBD im Vordergrund ist – dann siehst du die Lobby ja selbst.':
        'DBD が前面にある間は通知しません – その場合はロビーを自分で確認できます。',
    'Bilanz der Sitzung zeigen, wenn DBD beendet wurde':
        'DBD を閉じたときにセッションの数値を表示する',
    'Etwa 15 s nachdem DBD geschlossen wurde: eine Meldung mit den Runden der Sitzung, der Spielzeit und – mit Match-Daten – Ø Kills, Entkommen und Bloodpoints. Steht auch im Log.':
        'DBD を閉じてから約 15 秒後に、セッションのラウンド数、プレイ時間、さらにマッチデータがあれば平均キル数、脱出数、ブラッドポイントを通知します。ログにも記録されます。',
    'Sitzung beendet':
        'セッション終了',
    '1 Runde':
        '1 ラウンド',
    '{bp} BP':
        '{bp} BP',
    'Melden, wenn eine Runde keine Blutpunkte gebracht hat (Cap erreicht)':
        'ラウンドでブラッドポイントが得られなかった場合に通知する（上限到達）',
    'Fog Scout liest in der Lobby den Blutpunkte-Stand oben rechts. Ist er nach einer gezählten Runde derselbe wie davor, ist das Cap erreicht (normal 5 Millionen, nach Tome-Belohnungen auch mehr) – die Punkte der Runde sind verfallen. Ton und Meldung kommen auch, wenn DBD im Vordergrund ist; Custom Games zählen nicht.':
        'Fog Scout はロビー右上のブラッドポイント残高を読み取ります。数えられたラウンドの後も残高が変わらなければ上限に達しています（通常 500 万、アーカイブの報酬でさらに増加）– そのラウンドのポイントは失われます。音と通知は DBD が前面にあるときも鳴ります。カスタムマッチは数えません。',
    'Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte dieser Runde sind verfallen.':
        'ブラッドポイントが変化していません：ラウンドの前後とも {bp} – 上限に達しており、このラウンドのポイントは失われました。',
    'Blutpunkte-Cap erreicht':
        'ブラッドポイントの上限に到達',
    '{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die nächste Runde nichts.':
        'ラウンドの前後とも {bp} BP – ブラッドウェブで使ってください。さもないと次のラウンドも何も得られません。',
    'Blutpunkte: +{gain} in dieser Runde, Stand {bp}.':
        'ブラッドポイント：このラウンドで +{gain}、残高 {bp}。',
    'Blutpunkte: Stand {bp} nach der Runde, vorher {before}.':
        'ブラッドポイント：ラウンド後の残高 {bp}、ラウンド前 {before}。',
    'BP-Stand':
        'BP 残高',
    'Aussetzer':
        'カクつき',
    'Alles sichern (ZIP) …':
        'すべてをバックアップ（ZIP）…',
    'Aus Sicherung wiederherstellen (ZIP) …':
        'バックアップから復元（ZIP）…',
    'Aus Sicherung wiederherstellen':
        'バックアップから復元',
    'Führt eine Sicherung von „Alles sichern“ mit den jetzigen Daten zusammen: Runden, Match-Daten, Kartenbilder und Banner, die fehlen, kommen dazu – Vorhandenes bleibt, wie es ist. Zeigt vorher, was dazukommt. Die Einstellungen der Sicherung nur auf eigene Rückfrage.':
        '「すべてをバックアップ」のバックアップを現在のデータと統合します：不足しているラウンド、マッチデータ、マップ画像、バナーが追加され、既存のものはそのまま残ります。追加される内容を先に表示します。バックアップの設定は別途確認したうえでのみ取り込みます。',
    'Während einer Runde nicht möglich – nach dem Rundenende noch einmal.':
        'ラウンド中はできません – 終了後にもう一度お試しください。',
    'Das ist keine Sicherung von Fog Scout ({error}).':
        'これは Fog Scout のバックアップではありません（{error}）。',
    '{rounds} Runden, {lost} nicht gezählte Runden, {matches} Matches, {files} Bilder/Banner':
        '{rounds} ラウンド、数えられなかったラウンド {lost}、{matches} マッチ、{files} 個の画像/バナー',
    'Alles aus der Sicherung ist schon da – nichts hinzuzufügen.':
        'バックアップの内容はすべて既に存在します – 追加するものはありません。',
    'Aus der Sicherung hinzufügen: {what}. Schon vorhanden (bleibt, wie es ist): {known}. Vorher kommt eine Kopie der Runden und Match-Daten nach backup/.':
        'バックアップから追加：{what}。既に存在（そのまま）：{known}。先にラウンドとマッチデータのコピーが backup/ に保存されます。',
    'Zusammenführen':
        '統合',
    'Wiederherstellen fehlgeschlagen: {error}':
        '復元に失敗しました：{error}',
    'Aus der Sicherung hinzugefügt: {what}.':
        'バックアップから追加しました：{what}。',
    'Einstellungen der Sicherung nicht lesbar: {error}':
        'バックアップの設定を読み取れません：{error}',
    'Die Sicherung enthält auch Einstellungen – übernehmen ersetzt die aktuellen.':
        'バックアップには設定も含まれています – 取り込むと現在の設定が置き換えられます。',
    'Installation prüfen':
        'インストールを確認',
    'Installation wird geprüft …':
        'インストールを確認中…',
    'Installation prüfen – Fehler: {line}':
        'インストールの確認 – 失敗：{line}',
    '{n} von {total} Prüfungen fehlgeschlagen – Einzelheiten im Log. Eine Neuinstallation (Setup erneut ausführen) behebt fehlende Dateien meist.':
        '{total} 件中 {n} 件の確認に失敗しました – 詳細はログを参照。再インストール（セットアップを再実行）すると、不足ファイルは通常解決します。',
    'Alle {n} Prüfungen bestanden: {names}.':
        '{n} 件の確認すべてに合格：{names}。',
    'Installation prüfen: {text}':
        'インストールの確認：{text}',
    'Prüft, ob alles da ist und läuft: Programmdateien, Kartenbilder, Bibliotheken, alle Module, Telemetrie aus, Texterkennung, ffmpeg, Qt – derselbe Selbsttest wie bei jedem Build. Läuft als eigener Prozess, Ergebnis im Log.':
        'すべてが揃って動作するか確認します：プログラムファイル、マップ画像、ライブラリ、全モジュール、テレメトリーのオフ、文字認識、ffmpeg、Qt – ビルドごとに行うのと同じ自己チェックです。独立したプロセスとして実行し、結果はログに記録されます。',
    'Alles sichern':
        'すべてをバックアップ',
    'Gesichert: {n} Dateien in {path}':
        'バックアップしました：{n} 個のファイルを {path} へ',
    'Sichern fehlgeschlagen: {error}':
        'バックアップに失敗しました：{error}',
    'Packt Runden, Match-Daten, die Einstellungen (ohne Passwörter und PC-eigene Werte), eigene Kartenbilder und den Banner-Korpus in eine ZIP-Datei – zum Aufbewahren oder für einen anderen PC. Aufnahmen und Logs bleiben draussen.':
        'ラウンド、マッチデータ、設定（パスワードとこの PC 固有の値を除く）、独自のマップ画像、バナーコーパスを 1 つの ZIP ファイルにまとめます – 保管用や別の PC 用に。録画とログは含まれません。',
    'Spielmodus':
        'ゲームモード',
    'Eigener Charakter':
        '自分のキャラクター',
    'Eigene Perks':
        '自分のパーク',
    'JSON (für eigene Auswertungen)':
        'JSON（独自の分析用）',
    'Eine Liste mit einem Objekt je Runde, die Spaltentitel als Schlüssel – für eigene Auswertungen (Python, Tabellen, jq).':
        'ラウンドごとに 1 つのオブジェクトを持つリストで、列タイトルがキーになります – 独自の分析用（Python、スプレッドシート、jq）。',
    'Rolle für {map} ({when}) auf {role} geändert.':
        '{map}（{when}）の役割を {role} に変更しました。',
    'Rolle konnte nicht gespeichert werden: {error}':
        '役割を保存できませんでした：{error}',
    'Diese Runde als Killer-Runde zählen (falls die Erkennung falsch lag).':
        'このラウンドをキラーのラウンドとして数えます（検出が誤っていた場合）。',
    'Diese Runde als Survivor-Runde zählen (falls die Erkennung falsch lag).':
        'このラウンドをサバイバーのラウンドとして数えます（検出が誤っていた場合）。',
    'Diese Runde als Custom Game zählen – sie fliesst dann nicht in die Wartezeit ein.':
        'このラウンドをカスタムマッチとして数えます – 待ち時間から除外されます。',
    'Noch keine Wartezeiten in dieser Auswahl.':
        'この選択範囲にはまだ待ち時間がありません。',
    'nach Wochentag':
        '曜日別',
    'nach Uhrzeit':
        '時間帯別',
    'nach Region':
        'リージョン別',
    'Wann/Wo':
        'いつ/どこで',
    'Ø Wartezeit':
        '平均待ち時間',
    'Kürzeste':
        '最短',
    'Warten':
        '待機',
    'Uhr':
        '時間',
    'Montag':
        '月曜日',
    'Dienstag':
        '火曜日',
    'Mittwoch':
        '水曜日',
    'Donnerstag':
        '木曜日',
    'Freitag':
        '金曜日',
    'Samstag':
        '土曜日',
    'Sonntag':
        '日曜日',
    'Gemessen von „CANCEL“ (Suche läuft) bis zur gefundenen Lobby – nur wenn das Programm die Suche gesehen hat. Custom Games haben keine Wartezeit.':
        '「CANCEL」（検索中）からロビーが見つかるまでを計測します – プログラムが検索を確認できた場合のみ。カスタムマッチには待ち時間がありません。',
    'Map-Namen oben einfügen (wie bei den mitgelieferten Karten)':
        'マップ名を上部に表示する（付属のマップと同様）',
    'Das Bild hat oben schon einen Namen – es wird keiner hinzugefügt.':
        '画像の上部には既に名前があります – 追加しません。',
    'Schreibt den Map-Namen weiss mit Schatten über die Karte, im Stil der mitgelieferten Karten. Hat das Bild oben schon einen Namen, passiert nichts. Beim Drehen bleibt der Name aufrecht.':
        '付属マップのスタイルで、マップの上に影付きの白い文字でマップ名を書き込みます。画像の上部に既に名前がある場合は何もしません。マップを回転しても名前は正立したままです。',
    'Drehen':
        '回転',
    'Karte drehen':
        'マップを回転',
    'Etage wechseln':
        '階を切り替え',
    'Beide Etagen':
        '両方の階',
    'Etage {n} von {total}':
        '{n} / {total} 階',
    'Diese Map hat nur eine Etage.':
        'このマップには階が 1 つしかありません。',
    'Wechselt die Anzeige bei Karten mit Etagen (Midwich): beide untereinander → unten → oben → beide. Gilt bis zur nächsten Map.':
        '階のあるマップ（Midwich）の表示を切り替えます：両方を上下に並べる → 下の階 → 上の階 → 両方。次のマップまで有効です。',
    'Etagen untereinander zeigen':
        '階を上下に並べて表示する',
    'An: Karten mit Etagen (Midwich) zeigen alle Etagen untereinander, oben über unten – jede so groß wie eine normale Karte, soweit der Platz reicht. Aus: Sie starten mit der unteren Etage. Der Knopf „Etage“ oder der Hotkey schaltet jederzeit um.':
        'オン：階のあるマップ（Midwich）は、すべての階を上下に（上の階を上に）表示します – スペースが許す限り、それぞれ通常のマップと同じ大きさです。オフ：下の階から表示します。「階」ボタンまたはホットキーでいつでも切り替えられます。',
    '{map} um {deg}° gedreht.':
        '{map} を {deg}° 回転しました。',
    'Drehung für {map} entfernt.':
        '{map} の回転を解除しました。',
    'Dreht die angezeigte Karte um 90° im Uhrzeigersinn (für jede Map gemerkt). Der Map-Name darüber bleibt aufrecht, die Zahlen in der Karte drehen sich mit.':
        '表示中のマップを時計回りに 90° 回転します（マップごとに記憶）。上のマップ名は正立したままで、マップ内の数字は一緒に回転します。',
    'Eigene Grösse für {map} entfernt – es gilt wieder der Schieberegler.':
        '{map} の個別サイズを解除しました – スライダーの値が再び適用されます。',
    'Entfernt eigene Grösse und Drehung der angezeigten Map – danach gilt wieder der Schieberegler für alle Maps.':
        '表示中のマップの個別サイズと回転を解除します – 全マップ共通のスライダーが再び適用されます。',
    'Deckkraft':
        '不透明度',
    'Nur zeigen, wenn DBD das aktive Fenster ist':
        'DBD がアクティブウィンドウの間のみ表示する',
    'Map-Namen über der Karte anzeigen':
        'マップの上にマップ名を表示する',
    'Rundentimer unter der Karte anzeigen':
        'マップの下にラウンドタイマーを表示する',
    'Verbundenen Server unter der Karte':
        'マップの下に接続中のサーバー',
    'Transparenter Rand um die Karte':
        'マップの周囲の縁を透明にする',
    'Map beim Match-Start automatisch erkennen':
        'マッチ開始時にマップを自動で検出する',
    'Overlay ausblenden, sobald ich nicht mehr in der Runde bin':
        'ラウンドから抜けたらすぐにオーバーレイを隠す',
    'erkennt Ergebnisbildschirm, Lobby/Menüs, Ladebildschirm und geschlossenes DBD':
        'リザルト画面、ロビー/メニュー、ロード画面、DBD の終了を検出します',
    'Overlay pausieren, solange ein DBD-Menü offen ist':
        'DBD のメニューが開いている間はオーバーレイを一時停止する',
    'erkannt am sichtbaren Mauszeiger (ESC-Menü, Ergebnisbildschirm, Lobby)':
        'マウスポインターの表示で検出します（ESC メニュー、リザルト画面、ロビー）',
    'Spielsprache (Map-Namen)':
        'ゲーム言語（マップ名）',
    'Erweitert':
        '詳細',
    'Erweitert (Fehlersuche)':
        '詳細（トラブルシューティング）',
    'Technik':
        '技術',
    'Auch erkennen, wenn andere Fenster über DBD liegen':
        '他のウィンドウが DBD を覆っていても検出する',
    'Fensteraufnahme wie bei OBS, nur solange DBD im Hintergrund ist':
        'OBS のようなウィンドウキャプチャ。DBD がバックグラウンドの間のみ',
    'Scans/Sek.':
        'スキャン/秒',
    'Rundenende-Erkennung: {state}':
        'ラウンド終了の検出：{state}',
    'Debug-Bilder speichern':
        'デバッグ画像を保存',
    'Banner jeder Erkennung für „Erkennung prüfen“ sammeln':
        '「検出を確認」のために検出ごとのバナーを保持する',
    '{n} Banner gesammelt':
        '{n} 個のバナーを保持中',
    '1 Banner gesammelt':
        '1 個のバナーを保持中',
    'letzte Prüfung: {hits} von {total} erkannt':
        '前回の確認：{total} 個中 {hits} 個を認識',
    'Erkennung prüfen':
        '検出を確認',
    'Korpus exportieren …':
        'コーパスをエクスポート…',
    'Korpus exportieren':
        'コーパスをエクスポート',
    'Korpus-Ordner öffnen':
        'コーパスフォルダーを開く',
    'Noch keine Banner gesammelt – sie kommen mit jeder erkannten Map.':
        '保持中のバナーはまだありません – マップを検出するたびに追加されます。',
    'Erkennung prüfen: {n} Banner werden neu gelesen …':
        '検出を確認：{n} 個のバナーを再読み取り中…',
    'Erkennung prüfen fehlgeschlagen: {error}':
        '検出の確認に失敗しました：{error}',
    '{hits} von {total} Bannern wieder erkannt ({seconds} s).':
        '{total} 個中 {hits} 個のバナーを再認識しました（{seconds} 秒）。',
    '{n} nicht lesbar.':
        '{n} 個は読み取れません。',
    'Erkennung prüfen: {text}':
        '検出を確認：{text}',
    'Erkennung prüfen – {stamp}: erwartet {want}, gelesen „{read}“ → {got}':
        '検出を確認 – {stamp}：期待値 {want}、読み取り「{read}」→ {got}',
    'Die Treffer, die fehlen, stehen im Log.':
        '認識できなかったバナーはログに記録されています。',
    'Korpus exportiert: {n} Dateien nach {path}':
        'コーパスをエクスポートしました：{n} 個のファイルを {path} へ',
    'Korpus exportieren fehlgeschlagen: {error}':
        'コーパスのエクスポートに失敗しました：{error}',
    'Speichert bei jeder erkannten Map den Ausschnitt um die Banner-Linie (Name und Realm) im Datenordner unter corpus/, höchstens 300 Stück – die Grundlage für „Erkennung prüfen“. Der Ausschnitt kann den linken HUD-Rand mit Spielernamen zeigen; er bleibt auf diesem PC.':
        '検出したマップごとに、バナーライン周辺の部分（名前とレルム）をデータフォルダーの corpus/ に保持します（最大 300 個）– 「検出を確認」の基礎です。この部分には、プレイヤー名を含む HUD の左端が写ることがあります。データはこの PC 内にとどまります。',
    'Liest alle gesammelten Banner mit der Erkennung neu und zählt, wie viele wieder die gespeicherte Map ergeben – nach einem Update oder einer geänderten Spielsprache. Läuft im Hintergrund, Ergebnis im Log.':
        '保持中のすべてのバナーを検出機能で再読み取りし、保存されたマップが再び得られる数を数えます – アップデート後やゲーム言語を変更した後に。バックグラウンドで実行し、結果はログに記録されます。',
    'Packt alle gesammelten Banner mit ihren Angaben in eine ZIP-Datei – z. B. um sie für die Tests des Projekts weiterzugeben. Vorher die Bilder ansehen: sie können Spielernamen zeigen.':
        '保持中のすべてのバナーを詳細情報とともに ZIP ファイルにまとめます – 例：プロジェクトのテストに提供するため。先に画像を確認してください：プレイヤー名が写っていることがあります。',
    'Öffnet den Ordner corpus/ im Datenordner.':
        'データフォルダー内の corpus/ フォルダーを開きます。',
    'Bildschirm jetzt scannen':
        '今すぐ画面をスキャン',
    'Diagnose kopieren':
        '診断情報をコピー',
    'Verbundener Spielserver':
        '接続中のゲームサーバー',
    'Serverregionen':
        'サーバーリージョン',
    'DBD sucht Matches nur in den angehakten Regionen (über die Windows-hosts-Datei, das Spiel wird nicht verändert). Nach „Auswahl anwenden“ DBD neu starten.':
        'DBD はチェックを入れたリージョンでのみマッチを検索します（Windows の hosts ファイルを使用、ゲームは変更されません）。「選択を適用」の後に DBD を再起動してください。',
    'Region':
        'リージョン',
    'hosts-Datei':
        'hosts ファイル',
    'Ping messen':
        'Ping を測定',
    'Auswahl anwenden':
        '選択を適用',
    'Alles freigeben':
        'すべて許可',
    'Mit VPN unzuverlässig. Region-Tools sind von BHVR weder erlaubt noch verboten – auf eigene Verantwortung.':
        'VPN 使用時は不確実です。リージョンツールは BHVR によって許可も禁止もされていません – 自己責任でご利用ください。',
    'Warte auf Windows (Administratorrechte) …':
        'Windows（管理者権限）を待機中…',
    'Aus':
        'オフ',
    'Zeigt Region und Ping des Spielservers, auch im Overlay (braucht Administratorrechte).':
        'ゲームサーバーのリージョンと Ping を、オーバーレイにも表示します（管理者権限が必要）。',
    'DBD läuft mit {w}×{h}, kleiner als 1920×1080: die Erkennung ist unsicherer (vor allem Lobby-Knopf und Killername). Fenster größer ziehen oder „Fenster-Vollbild“ nutzen.':
        'DBD は {w}×{h} で動作しており、1920×1080 より小さいため、検出の信頼性が下がります（特にロビーボタンとキラー名）。ウィンドウを大きくするか、「ウィンドウフルスクリーン」を使用してください。',
    'DBD-Fenster ist schmaler als 16:9 ({w}×{h}): diese Form ist ungetestet, Map- und Rundenende-Erkennung können danebenliegen. Am sichersten: 16:9 oder breiter.':
        'DBD のウィンドウが 16:9 より狭くなっています（{w}×{h}）：この形状はテストされておらず、マップとラウンド終了の検出がずれる可能性があります。最も確実なのは 16:9 以上の横長です。',
    'Verbunden mit: {server}':
        '接続先：{server}',
    'pausiert, bis DBD läuft':
        'DBD が起動するまで一時停止',
    'Anzeige des Spielservers beendet.':
        'ゲームサーバー表示を停止しました。',
    'Spielserver-Anzeige: {error}':
        'ゲームサーバー表示：{error}',
    'Spielserver-Anzeige läuft (liest nur Paketköpfe, keine Inhalte).':
        'ゲームサーバー表示を実行中（パケットヘッダーのみを読み取り、内容は読み取りません）。',
    'Spielserver-Anzeige pausiert – DBD läuft nicht (startet automatisch mit DBD).':
        'ゲームサーバー表示を一時停止中 – DBD が起動していません（DBD の起動で再開します）。',
    'Spielserver-Anzeige beendet: {error}':
        'ゲームサーバー表示が停止しました：{error}',
    ' – nicht in deiner Regionsauswahl':
        ' – 選択したリージョンに含まれていません',
    'Verbunden mit Spielserver: {region}{note}.':
        'ゲームサーバーに接続しました：{region}{note}。',
    'hosts-Datei nicht lesbar: {error}':
        'hosts ファイルを読み取れません：{error}',
    'Aktiv: nur {regions} erlaubt.':
        '有効：{regions} のみ許可。',
    '(keine)':
        '（なし）',
    'Keine eigene Auswahl aktiv, aber andere Einträge sperren Regionen.':
        '独自の選択は有効ではありませんが、他のエントリーがリージョンをブロックしています。',
    'Keine Region gesperrt – DBD wählt selbst.':
        'ブロック中のリージョンはありません – DBD が自動で選択します。',
    'anderen Programmen':
        '他のプログラム',
    ' Es gibt {n} Einträge von {who} für DBD-Server (werden beim Anwenden ersetzt).':
        ' DBD サーバー用に {who} のエントリーが {n} 件あります（適用時に置き換えられます）。',
    'Serverregionen: {text}':
        'サーバーリージョン：{text}',
    'Messe Ping zu den Serverregionen …':
        'サーバーリージョンへの Ping を測定中…',
    'Ping fehlgeschlagen: {error}':
        'Ping に失敗しました：{error}',
    'Am schnellsten: {list}.':
        '最速：{list}。',
    'Keine Region hat geantwortet (Internet/Firewall/VPN?).':
        'どのリージョンも応答しませんでした（インターネット/ファイアウォール/VPN？）。',
    'Bitte mindestens eine Region anhaken.':
        '少なくとも 1 つのリージョンにチェックを入れてください。',
    'Erlaubt bleiben: {names}.\n\nAlle anderen DBD-Serverregionen werden in der Windows-hosts-Datei gesperrt. Windows fragt gleich nach Administratorrechten.':
        '許可：{names}。\n\nその他の DBD サーバーリージョンはすべて Windows の hosts ファイルでブロックされます。Windows が管理者権限を要求します。',
    '{n} vorhandene Einträge anderer Programme (z. B. Make Your Choice) für DBD-Server werden dabei entfernt.':
        'DBD サーバー用の他のプログラム（例：Make Your Choice）の既存エントリー {n} 件が削除されます。',
    'Danach DBD neu starten, damit es wirkt.':
        '反映させるには、その後 DBD を再起動してください。',
    'Serverregionen anwenden':
        'サーバーリージョンを適用',
    'Nur noch {names} erlaubt':
        '{names} のみ許可',
    'Es ist nichts gesperrt.':
        '何もブロックされていません。',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen (auch die von Make Your Choice)?':
        'DBD サーバーリージョンのブロックを hosts ファイルからすべて削除しますか（Make Your Choice のものを含む）？',
    'Alle Sperren für DBD-Serverregionen aus der hosts-Datei entfernen?':
        'DBD サーバーリージョンのブロックを hosts ファイルからすべて削除しますか？',
    'Windows fragt gleich nach Administratorrechten. Danach DBD neu starten.':
        'Windows が管理者権限を要求します。その後 DBD を再起動してください。',
    'Serverregionen freigeben':
        'サーバーリージョンを許可',
    'Alle Regionen freigegeben':
        'すべてのリージョンを許可',
    'Serverregionen: {text}. DBD neu starten, damit es wirkt.':
        'サーバーリージョン：{text}。反映させるには DBD を再起動してください。',
    '{text}. DBD jetzt neu starten.':
        '{text}。今すぐ DBD を再起動してください。',
    'Keine Änderung nötig.':
        '変更の必要はありません。',
    'unbekannter Fehler':
        '不明なエラー',
    'Firewall-Regeln von Make Your Choice („Enforced“) gefunden – sie sperren Regionen unabhängig von der hosts-Datei. In Make Your Choice „Revert to Default“ drücken.':
        'Make Your Choice のファイアウォールルール（「Enforced」）が見つかりました – hosts ファイルとは無関係にリージョンをブロックします。Make Your Choice で「Revert to Default」を押してください。',
    'Achtung: Firewall-Regeln von Make Your Choice aktiv (siehe Log).':
        '注意：Make Your Choice のファイアウォールルールが有効です（ログを参照）。',
    'Europa':
        'ヨーロッパ',
    'Amerika':
        '南北アメリカ',
    'Asien':
        'アジア',
    'Ozeanien':
        'オセアニア',
    'frei':
        '許可',
    'gesperrt':
        'ブロック',
    'gesperrt (fremd)':
        'ブロック（他のプログラム）',
    'umgeleitet (fremd)':
        'リダイレクト（他のプログラム）',
    'Frankfurt':
        'フランクフルト',
    'Irland':
        'アイルランド',
    'London':
        'ロンドン',
    'USA Ost (N. Virginia)':
        '米国東部（バージニア北部）',
    'USA Ost (Ohio)':
        '米国東部（オハイオ）',
    'USA West (N. Kalifornien)':
        '米国西部（北カリフォルニア）',
    'USA West (Oregon)':
        '米国西部（オレゴン）',
    'Kanada (Zentral)':
        'カナダ（中部）',
    'Südamerika (São Paulo)':
        '南米（サンパウロ）',
    'Tokio':
        '東京',
    'Seoul':
        'ソウル',
    'Mumbai':
        'ムンバイ',
    'Singapur':
        'シンガポール',
    'Hongkong':
        '香港',
    'Sydney':
        'シドニー',
    'Name nicht auflösbar':
        '名前を解決できません',
    'Start mit Administratorrechten fehlgeschlagen (Fehler {code}).':
        '管理者権限での起動に失敗しました（エラー {code}）。',
    'Hilfsprogramm nicht gestartet.':
        'ヘルパープログラムが起動していません。',
    'Das Hilfsprogramm hat kein Ergebnis geliefert (Code {code}).':
        'ヘルパープログラムが結果を返しませんでした（コード {code}）。',
    'Zeitüberschreitung beim Schreiben der hosts-Datei.':
        'hosts ファイルの書き込み中にタイムアウトしました。',
    'Abgebrochen (keine Administratorrechte erteilt).':
        'キャンセルしました（管理者権限が許可されませんでした）。',
    'Warte auf Match …':
        'マッチを待機中…',
    'Global':
        'グローバル',
    'keine Daten vom Mitschnitt':
        'キャプチャからのデータがありません',
    'Nur unter Windows verfügbar.':
        'Windows でのみ利用できます。',
    'Mitschnitt beendet (Code {code}).':
        'キャプチャが終了しました（コード {code}）。',
    'Fehler: {error}':
        'エラー：{error}',
    'Statistik':
        '統計',
    'Maps':
        'マップ',
    'Map':
        'マップ',
    'Runden':
        'ラウンド',
    'Ø Dauer':
        '平均の長さ',
    'Letzte Runden':
        '最近のラウンド',
    'Gesamter Zeitraum':
        '全期間',
    'Heute':
        '今日',
    'Diese Woche':
        '今週',
    'Dieser Monat':
        '今月',
    'Dieses Jahr':
        '今年',
    'Alle Regionen':
        'すべてのリージョン',
    'Alle Killer':
        'すべてのキラー',
    'Häufigste Map':
        '最も多いマップ',
    'Der markierte Name (Skin oder neuer Killer) zählt ab jetzt als der gewählte Killer – auch in allen bisherigen Runden.':
        '選択した名前（スキンまたは新キラー）を今後は選択したキラーとして数えます – 過去のすべてのラウンドでも。',
    'Entfernt alle eigenen Killer-Zuordnungen; die Namen erscheinen wieder so, wie sie gelesen wurden.':
        '独自のキラー割り当てをすべて削除します。名前は読み取ったとおりに再び表示されます。',
    'Zuordnen':
        '割り当て',
    'Warte auf Map':
        'マップを待機中',
    'Solange DBD läuft und keine Karte eingeblendet ist, zeigt das Overlay eine kleine Karte: „Warte auf Map“, darunter Suche/Lobby (z. B. „Suche läuft: 02:13 · Nurse“) oder die letzte Runde. Gilt nicht, wenn du die Karte selbst ausgeblendet hast.':
        'DBD の起動中にマップが表示されていない場合、オーバーレイに小さなカードを表示します：「マップを待機中」、その下に検索/ロビーの状態（例：「検索中：02:13 · Nurse」）または前回のラウンド。自分でマップを非表示にした場合は表示しません。',
    'Ohne Karte: „Warte auf Map“ und Lobby-Status anzeigen':
        'マップがないとき：「マップを待機中」とロビーの状態を表示する',
    'Killer der Runde:':
        'ラウンドのキラー：',
    'Killer setzen':
        'キラーを設定',
    'Notiz zum Killer:':
        'キラーのメモ：',
    'Um diese Tageszeit ({span} Uhr) am schnellsten: {region} – Wartezeit {wait} (Median), {n} Runden':
        'この時間帯（{span} 時）で最速：{region} – 待ち時間 {wait}（中央値）、{n} ラウンド',
    'Ø {ping} ms':
        '平均 {ping} ms',
    'danach {region} ({wait})':
        '次に {region}（{wait}）',
    'Notiz speichern':
        'メモを保存',
    'Notiz zu {killer} gespeichert.':
        '{killer} のメモを保存しました。',
    'Notiz zu {killer} gelöscht.':
        '{killer} のメモを削除しました。',
    'Eigene Notiz zum markierten Killer, z. B. „Lithe, nicht vaulten“. Erscheint im Spiel unter der Map-Notiz, sobald dieser Killer in der Runde ist (eigener Killer oder, als Survivor, der aus der Lobby). Leer speichern löscht sie.':
        '選択したキラーについての独自のメモ（例：「軽快、乗り越え禁止」）。このキラーがラウンドにいるとき（自分のキラー、またはサバイバー時はロビーで確認したキラー）、ゲーム内でマップのメモの下に表示されます。空のまま保存すると削除されます。',
    'Killer konnte nicht gespeichert werden: {error}':
        'キラーを保存できませんでした：{error}',
    'Killer für {map} ({when}) auf {killer} gesetzt.':
        '{map}（{when}）のキラーを {killer} に設定しました。',
    'Map der Runde:':
        'ラウンドのマップ：',
    'Setzt die Map nur für die markierten Runden – wenn das Banner falsch gelesen wurde. Statistik, eigener Rekord und die Verknüpfung mit den Match-Daten folgen; die Aufnahme behält ihren Namen.':
        '選択したラウンドのマップのみを設定します – バナーが誤って読み取られた場合に。統計、自己記録、マッチデータとの紐付けが追従し、録画の名前はそのままです。',
    'Map setzen':
        'マップを設定',
    'Map konnte nicht gespeichert werden: {error}':
        'マップを保存できませんでした：{error}',
    'Map der Runde vom {when} auf {map} gesetzt.':
        '{when} のラウンドのマップを {map} に設定しました。',
    'Setzt den Killer nur für die markierte Runde und zählt sie als Killer-Runde – z. B. wenn sie fälschlich als Survivor gezählt wurde oder der Name falsch gelesen wurde.':
        '選択したラウンドのキラーのみを設定し、キラーのラウンドとして数えます – 例：誤ってサバイバーとして数えられた場合や、名前が誤って読み取られた場合。',
    'Zuordnungen löschen':
        '割り当てを削除',
    '„{name}“ zählt jetzt als {killer}.':
        '「{name}」を {killer} として数えるようになりました。',
    'Alle eigenen Killer-Zuordnungen löschen?':
        '独自のキラー割り当てをすべて削除しますか？',
    'Killer-Zuordnungen gelöscht.':
        'キラーの割り当てを削除しました。',
    'ohne Region':
        'リージョンなし',
    'Anteil':
        '割合',
    'Region nur bekannt, wenn im Tab Server „Verbundener Spielserver“ an war.':
        'リージョンは、「サーバー」タブで「接続中のゲームサーバー」がオンだった場合のみわかります。',
    'Wann':
        '日時',
    'Dauer':
        '長さ',
    'Alle Runden löschen …':
        'すべてのラウンドを削除…',
    'Runde löschen':
        'ラウンドを削除',
    'Ø {kills} Kills · {n} Runden':
        '平均 {kills} キル · {n} ラウンド',
    'Killer: Ø {kills} Kills, {four}× 4K ({n})':
        'キラー：平均 {kills} キル、4K {four} 回（{n}）',
    'Survivor: {share} entkommen ({n})':
        'サバイバー：脱出 {share}（{n}）',
    '{share} entkommen · {n} Runden':
        '脱出 {share} · {n} ラウンド',
    'Eigene Bilanz unter dem Timer':
        'タイマーの下に自己記録',
    'Eigene Notiz unter dem Timer':
        'タイマーの下に独自のメモ',
    'Zeigt deine eigene Notiz zur Map unter dem Rundentimer – geschrieben auf der Seite Maps (Map anklicken oder Rechtsklick → „Notiz bearbeiten …“), höchstens vier Zeilen.':
        'マップの独自のメモをラウンドタイマーの下に表示します – 「マップ」ページで記入します（マップをクリック、または右クリック →「メモを編集…」）。最大 4 行です。',
    'Deine Notiz zu dieser Map – wird beim Tippen gespeichert und im Spiel unter dem Timer gezeigt (höchstens vier Zeilen). Leer = keine Notiz.':
        'このマップのメモ – 入力中に保存され、ゲーム内でタイマーの下に表示されます（最大 4 行）。空 = メモなし。',
    'Eigene Notiz (im Spiel unter dem Timer)':
        '独自のメモ（ゲーム内でタイマーの下）',
    'z. B. Shack links vom Main, Gen im Keller …':
        '例：小屋はメインの左、地下に発電機…',
    'Notiz bearbeiten …':
        'メモを編集…',
    'Map-Stile':
        'マップスタイル',
    'Alle auf einmal':
        'すべて一括',
    'Kartenstile für {map} werden im Hintergrund erstellt.':
        '{map} のマップスタイルをバックグラウンドで作成中です。',
    'Kartenstil {style} für {map} wird im Hintergrund erstellt.':
        '{map} のマップスタイル {style} をバックグラウンドで作成中です。',
    'Eigene Notiz':
        '独自のメモ',
    'Eigene Notiz: {note}':
        '独自のメモ：{note}',
    'Zeigt unter dem Rundentimer, wie es dir auf dieser Map bisher ging: als Killer Ø Kills, als Survivor den Anteil Escapes – aus den Runden mit Daten der Stats-Seite, ab 3 Runden.':
        'このマップでのこれまでの成績をラウンドタイマーの下に表示します：キラーでは平均キル数、サバイバーでは脱出率 – 統計ページのデータがあるラウンドから、3 ラウンド以上で表示します。',
    'Entfernt die markierte Runde aus der Statistik – z. B. eine Map, die mitten im Match falsch erkannt wurde. Fragt vorher nach.':
        '選択したラウンドを統計から削除します – 例：マッチの途中でマップが誤って読み取られた場合。先に確認します。',
    'Runde {what} aus der Statistik löschen?':
        'ラウンド {what} を統計から削除しますか？',
    'Runde konnte nicht gelöscht werden: {error}':
        'ラウンドを削除できませんでした：{error}',
    'Runde gelöscht: {map} ({when}).':
        'ラウンドを削除しました：{map}（{when}）。',
    'Noch keine Runden gespeichert.':
        '保存されたラウンドはまだありません。',
    'Alle Runden löschen':
        'すべてのラウンドを削除',
    'Alle gespeicherten Runden löschen? Vorher wird eine Kopie in {folder}/ angelegt.':
        '保存されたすべてのラウンドを削除しますか？先にコピーが {folder}/ に保存されます。',
    'Es sind keine Runden gespeichert.':
        '保存されたラウンドはありません。',
    'Die Kopie in {folder}/ konnte nicht angelegt werden – die Runden bleiben gespeichert.':
        '{folder}/ にコピーを作成できませんでした – ラウンドは保存されたままです。',
    'Nicht angewendet – 1 Änderung. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '未適用 – 変更 1 件。「選択を適用」で反映し、その後 DBD を再起動してください。',
    'Nicht angewendet – {n} Änderungen. „Auswahl anwenden“ übernimmt sie, danach DBD neu starten.':
        '未適用 – 変更 {n} 件。「選択を適用」で反映し、その後 DBD を再起動してください。',
    'Öffnet die markierten Runden bzw. Clips nacheinander im grossen Editor – als eine Montage (mehrere markieren: Strg- oder Umschalt-Klick).':
        '選択したラウンドやクリップを、大きなエディターで 1 つのモンタージュとして順に開きます（複数選択：Ctrl または Shift を押しながらクリック）。',
    'Ursache: {cause}':
        '原因：{cause}',
    'Keine Region angehakt – für „Auswahl anwenden“ mindestens eine anhaken.':
        'チェックの入ったリージョンがありません – 「選択を適用」には少なくとも 1 つチェックを入れてください。',
    'Anwenden':
        '適用',
    'Freigeben':
        'ブロック解除',
    'Importieren':
        'インポート',
    'Markieren':
        'マーク',
    'Trotzdem beenden':
        'それでも終了',
    'Rundenverlauf gelöscht.':
        'ラウンド履歴を削除しました。',
    'Löscht alle gespeicherten Runden (Datei rounds.jsonl) – nach einer Rückfrage, vorher kommt eine Kopie in den Ordner backup.':
        '保存されたすべてのラウンド（ファイル rounds.jsonl）を削除します – 確認後、先にコピーがバックアップフォルダーに保存されます。',
    'Anzeigen:':
        '表示：',
    'Leeren':
        'クリア',
    'Log-Datei öffnen':
        'ログファイルを開く',
    'Sprache und Darstellung':
        '言語と外観',
    'Wirkt nach dem nächsten Start des Programms.':
        '次回のプログラム起動時に反映されます。',
    'Sprache geändert – wirkt nach dem nächsten Start des Programms.':
        '言語を変更しました – 次回のプログラム起動時に反映されます。',
    'Dark Mode':
        'ダークモード',
    'Hotkeys':
        'ホットキー',
    'Standard':
        '既定値',
    'Zum Ändern anklicken und die neue Tastenkombination drücken.':
        'クリックして変更し、新しいキーの組み合わせを押してください。',
    'Start und Infobereich':
        '起動と通知領域',
    'Beim Minimieren in den Infobereich':
        '通知領域に最小化する',
    'Mit Windows starten':
        'Windows と同時に起動する',
    'Updates':
        'アップデート',
    'Beim Start Updates installieren':
        '起動時にアップデートをインストールする',
    'nur über start.bat bzw. die Desktop-Verknüpfung; eigene Änderungen werden nie überschrieben':
        'start.bat またはデスクトップのショートカットからのみ。独自の変更が上書きされることはありません',
    'Eigene Map-Zuordnungen':
        '独自のマップ割り当て',
    'Jetzt nach Updates suchen':
        '今すぐアップデートを確認',
    'Aktualisieren und neu starten':
        'アップデートして再起動',
    'Suche nach Updates …':
        'アップデートを確認中…',
    'Beim Start nach Updates suchen':
        '起動時にアップデートを確認する',
    'Laden und Installieren nur nach deiner Bestätigung; das Setup wird per SHA-256 geprüft':
        '確認後にのみダウンロードしてインストールします。セットアップは SHA-256 で検証されます',
    'Update-Prüfung fehlgeschlagen: {error}':
        'アップデートの確認に失敗しました：{error}',
    'Kein Update – Version {version} (Build {build}) ist aktuell.':
        'アップデートはありません – バージョン {version}（ビルド {build}）は最新です。',
    'Update verfügbar: {old} → {new} (Build {build}).':
        'アップデートがあります：{old} → {new}（ビルド {build}）。',
    'Lade Update …':
        'アップデートをダウンロード中…',
    'GitHub antwortet gerade nicht (HTTP {code}) – bitte in einigen Minuten erneut versuchen.':
        'GitHub が現在応答していません（HTTP {code}）– 数分後にもう一度お試しください。',
    'Keine Antwort von GitHub (Zeitüberschreitung/Verbindung) – bitte später erneut versuchen.':
        'GitHub から応答がありません（タイムアウト/接続）– 後でもう一度お試しください。',
    'GitHub antwortet nicht – neuer Versuch {n} von {total} …':
        'GitHub が応答していません – 試行 {n} / {total}…',
    'Lade Update … {pct} %':
        'アップデートをダウンロード中… {pct} %',
    'Update nicht geladen: {error}':
        'アップデートはダウンロードされませんでした：{error}',
    'Update {version} (Build {build}) geladen und geprüft.':
        'アップデート {version}（ビルド {build}）をダウンロードし、検証しました。',
    'Update installieren':
        'アップデートをインストール',
    'Fog Scout {version} (Build {build}) ist geladen und per SHA-256 geprüft. Jetzt installieren? Das Programm schliesst sich und startet danach neu.':
        'Fog Scout {version}（ビルド {build}）のダウンロードと SHA-256 による検証が完了しました。今すぐインストールしますか？プログラムは終了し、その後再起動します。',
    'Installieren':
        'インストール',
    'Update gesperrt: eine Runde läuft oder ein Clip wird gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'アップデートがブロックされました：ラウンドが進行中か、クリップを保存中です。その後もう一度「アップデートして再起動」をクリックしてください。',
    'Programm schliesst sich und installiert das Update …':
        'プログラムを終了してアップデートをインストールします…',
    'Das Update wurde nicht gestartet: Die Setup-Datei hat sich seit dem Download verändert oder fehlt. Bitte das Update noch einmal laden.':
        'アップデートは開始されませんでした：ダウンロード後にセットアップファイルが変更されたか、見つかりません。もう一度アップデートをダウンロードしてください。',
    'Das Update wurde nicht gestartet: Die Setup-Datei liess sich nicht sicher bereitstellen ({error}). Bitte das Update noch einmal laden.':
        'アップデートは開始されませんでした：セットアップファイルを安全に配置できませんでした（{error}）。もう一度アップデートをダウンロードしてください。',
    'Das Setup konnte nicht gestartet werden (Abfrage nach Administratorrechten abgebrochen?). Erneut versuchen oder das Setup selbst starten:\n{path}':
        'セットアップを起動できませんでした（管理者の確認をキャンセルしましたか？）。もう一度試すか、セットアップを自分で起動してください：\n{path}',
    'Neustart nicht möglich: {error}':
        '再起動できません：{error}',
    'Nur unter Windows: bitte das Programm über start.bat neu starten.':
        'Windows のみ：start.bat からプログラムを再起動してください。',
    'Programm startet neu und installiert das Update …':
        'プログラムを再起動してアップデートをインストールします…',
    'Fragt GitHub, ob es eine neue Version gibt (nur bei diesem Klick). Installiert wird erst mit „Aktualisieren und neu starten“.':
        '新しいバージョンがあるか GitHub に問い合わせます（このクリック時のみ）。インストールは「アップデートして再起動」でのみ行われます。',
    'Beendet das Programm und startet es über start.bat neu – dabei wird das Update installiert. Die installierte Version lädt das Setup, prüft es per SHA-256 und fragt vor dem Installieren.':
        'プログラムを終了し、start.bat から再起動します – その際にアップデートがインストールされます。インストール版はセットアップをダウンロードし、SHA-256 で検証してから、インストール前に確認します。',
    'Fragt nach jedem Start einmal GitHub, ob es ein neues Release gibt. Geladen und installiert wird nur nach deinem Klick und einer Rückfrage.':
        '起動するたびに一度、新しいリリースがあるか GitHub に問い合わせます。ダウンロードとインストールは、クリックして確認した後にのみ行われます。',
    'Alle löschen':
        'すべて削除',
    'Datenordner öffnen':
        'データフォルダーを開く',
    'Karten-Ordner öffnen':
        'マップフォルダーを開く',
    'liest nur Bildschirmpixel, sendet keine Eingaben ans Spiel.':
        '画面のピクセルを読み取るだけで、ゲームに入力を送信しません。',
    'Inoffizielles Fan-Tool, nicht von Behaviour Interactive genehmigt – Nutzung auf eigene Gefahr (siehe LICENSE).':
        '非公式のファンツールで、Behaviour Interactive の承認は受けていません – 自己責任でご利用ください（LICENSE を参照）。',
    'Kartenbilder: Lethia (hens333.com/callouts, mit Erlaubnis von Hens) · Map-Namen: Luca Fontanot (DBD Map Overlay).':
        'マップ画像：Lethia（hens333.com/callouts、Hens の許可を得て使用）· マップ名：Luca Fontanot（DBD Map Overlay）。',
    'Keine. Unbekannte Map-Namen lassen sich nach dem Match im Hauptfenster zuordnen.':
        'なし。不明なマップ名は、マッチ後にメインウィンドウで割り当てられます。',
    'Eigene Zuordnungen':
        '独自の割り当て',
    'Alle eigenen Map-Zuordnungen löschen?':
        '独自のマップ割り当てをすべて削除しますか？',
    'Eigene Map-Zuordnungen gelöscht.':
        '独自のマップ割り当てを削除しました。',
    'Spielsprachen: {langs}':
        'ゲーム言語：{langs}',
    'Änderbar, wenn das Programm über die Desktop-Verknüpfung gestartet wurde (verknuepfung_erstellen.bat einmal ausführen).':
        'デスクトップのショートカットからプログラムを起動した場合に変更できます（verknuepfung_erstellen.bat を一度実行してください）。',
    'Wird eingerichtet …':
        '設定中…',
    'Startet ab jetzt mit Windows im Infobereich.':
        '今後は Windows と同時に通知領域で起動します。',
    'Startet nicht mehr mit Windows.':
        'Windows と同時に起動しなくなりました。',
    'Startet ab jetzt mit Windows im Infobereich (abschaltbar unter Einstellungen → Start und Infobereich).':
        '今後は Windows と同時に通知領域で起動します（設定 →「起動と通知領域」でオフにできます）。',
    'Autostart mit Windows fehlgeschlagen: {error}':
        'Windows との同時起動を設定できませんでした：{error}',
    'Fehlgeschlagen: {error}':
        '失敗しました：{error}',
    'Nur unter Windows.':
        'Windows のみ。',
    'Tipp: Fog Scout über die Verknüpfung im Startmenü starten – dann läuft es ohne Windows-Abfrage mit den nötigen Rechten.':
        'ヒント：スタートメニューのショートカットから Fog Scout を起動してください – 必要な権限で、Windows の確認なしに実行されます。',
    'Änderbar, wenn das Programm über die Verknüpfung im Startmenü gestartet wurde.':
        'スタートメニューのショートカットからプログラムを起動した場合に変更できます。',
    'Tipp: Einmal als Administrator starten (Rechtsklick auf start.bat → „Als Administrator ausführen“) – dann richtet das Programm die Desktop-Verknüpfung ein, die künftig ohne Windows-Abfrage startet.':
        'ヒント：一度管理者として起動してください（start.bat を右クリック →「管理者として実行」）– プログラムがデスクトップのショートカットを設定し、以後は Windows の確認なしに起動します。',
    'Desktop-Verknüpfung eingerichtet/aktualisiert: startet ab jetzt ohne Windows-Abfrage.':
        'デスクトップのショートカットを設定/更新しました：今後は Windows の確認なしに起動します。',
    'Einrichtung der Verknüpfung fehlgeschlagen: {error}':
        'ショートカットの設定に失敗しました：{error}',
    'Verknüpfung erstellt: {path}':
        'ショートカットを作成しました：{path}',
    'Aufgabe konnte nicht angelegt werden: {error}':
        'タスクスケジューラのタスクを作成できませんでした：{error}',
    'Verknüpfung konnte nicht angelegt werden: {error}':
        'ショートカットを作成できませんでした：{error}',
    '(Autostart nicht erneuert: {error})':
        '（自動起動は更新されませんでした：{error}）',
    'Symbol im Infobereich nicht verfügbar ({error}) – Minimieren wie gewohnt.':
        '通知領域のアイコンを使用できません（{error}）– 最小化は通常どおり動作します。',
    'Öffnen nur unter Windows: {path}':
        '開く操作は Windows でのみ動作します：{path}',
    'Kann {path} nicht öffnen: {error}':
        '{path} を開けません：{error}',
    'Fenster öffnen':
        'ウィンドウを開く',
    'Beenden':
        '終了',
    'Hotkey: {keys}':
        'ホットキー：{keys}',
    'Hotkey {keys} ({action}) nicht verfügbar: {why}.':
        'ホットキー {keys}（{action}）は使用できません：{why}。',
    '{n} Hotkey(s) nicht verfügbar – siehe Log.':
        '{n} 個のホットキーが使用できません – ログを参照。',
    '– aus –':
        '– オフ –',
    'Tasten drücken …':
        'キーを押してください…',
    'Neue Kombination drücken – Esc bricht ab, Entf schaltet den Hotkey aus.':
        '新しい組み合わせを押してください – Esc でキャンセル、Delete でホットキーをオフにします。',
    '{keys} ist schon „{action}“ – andere wählen.':
        '{keys} は既に「{action}」に割り当てられています – 別の組み合わせを選んでください。',
    'aus':
        'オフ',
    'an':
        'オン',
    'Hotkey {action}: {keys}.':
        'ホットキー {action}：{keys}。',
    'Standard-Hotkeys wiederhergestellt.':
        '既定のホットキーを復元しました。',
    'Strg':
        'Ctrl',
    'Taste „{key}“ geht nicht als Hotkey':
        'キー「{key}」はホットキーとして使用できません',
    'Bitte mit Strg und/oder Alt kombinieren':
        'Ctrl または Alt と組み合わせてください',
    'schon von einem anderen Programm belegt':
        '既に他のプログラムで使用されています',
    'Für „{map}“ gibt es kein Bild.':
        '「{map}」の画像がありません。',
    'Bild konnte nicht geladen werden: {path} ({error})':
        '画像を読み込めませんでした：{path}（{error}）',
    'Map gewählt: {map}':
        '選択したマップ：{map}',
    'Noch keine Map gewählt.':
        'まだマップが選択されていません。',
    'Overlay eingeblendet.':
        'オーバーレイを表示しました。',
    'Overlay ausgeblendet.':
        'オーバーレイを非表示にしました。',
    '„{map}“ hat nur ein Layout.':
        '「{map}」にはレイアウトが 1 つしかありません。',
    'Layout manuell gewechselt':
        'レイアウトを手動で変更',
    'Scanne den Bildschirm nach Map- oder Realm-Namen …':
        '画面からマップ名またはレルム名をスキャン中…',
    'Testanzeige':
        'テスト表示',
    'Test: Overlay 10 s lang an seiner normalen Position, mit Systemwerten, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – nochmal drücken beendet den Test.':
        'テスト：オーバーレイを通常の位置に 10 秒間、システム値、「今日」、音楽とともに表示します（何もない場合はサンプル値）– もう一度押すとテストを終了します。',
    'Links':
        '左',
    'Mittig':
        '中央',
    'Rechts':
        '右',
    'Im Balken':
        '帯の中',
    'Abstand':
        '間隔',
    'Zeile CPU (Temperatur, Last)':
        'CPU の行（温度、負荷）',
    'Zeile GPU (Temperatur, Last)':
        'GPU の行（温度、負荷）',
    'Zeile Hotspot / GPU-Speicher (HWiNFO)':
        'ホットスポット / GPU メモリの行（HWiNFO）',
    'Zeile VRAM':
        'VRAM の行',
    'Zeile RAM':
        'RAM の行',
    'Zeile in den Systemwerten an/aus. Die Warnungen „CPU/GPU DROSSELT“ erscheinen immer.':
        'システム値の行のオン/オフ。「CPU/GPU THROTTLED」の警告は常に表示されます。',
    'Zeile in den Systemwerten an/aus – Hotspot und Memory Junction kommen nur mit HWiNFO.':
        'システム値の行のオン/オフ – ホットスポットとメモリジャンクションは HWiNFO 使用時のみ表示されます。',
    'Zeile in den Systemwerten an/aus.':
        'システム値の行のオン/オフ。',
    'Test beendet.':
        'テストを終了しました。',
    'Diagnose in die Zwischenablage kopiert (auch als diagnose.txt gespeichert).':
        '診断情報をクリップボードにコピーしました（diagnose.txt としても保存）。',
    'Alle Elemente mit der Maus ziehen (im Spiel oder in der Vorschau): Karte, Infos, Systemwerte, Heute, Eingaben, Musik. Rechtsklick auf ein Element = Menü (Ausblenden, Position zurücksetzen, Sperren), Strg+Mausrad = Grösse. Danach „Fertig“ oder Hotkey.':
        '各要素をマウスでドラッグしてください（ゲーム内またはプレビューで）：マップ、情報、システム値、今日、入力、音楽。要素を右クリック = メニュー（非表示、位置をリセット、ロック）、Ctrl+マウスホイール = サイズ。その後「完了」またはホットキー。',
    '{name} wieder an seinem üblichen Platz.':
        '{name} を通常の位置に戻しました。',
    'Karte':
        'マップ',
    'Systemwerte':
        'システム値',
    'Musik':
        '音楽',
    'Eingaben':
        '入力',
    'Verschieben aktiv – ziehen (rastet ein, Alt = frei), Pfeiltasten = fein, Ecke/Strg+Mausrad = Grösse, Rechtsklick = Menü':
        '移動モード – ドラッグ（スナップ、Alt = 自由）、矢印キー = 微調整、角/Ctrl+ホイール = サイズ、右クリック = メニュー',
    'Position zurücksetzen':
        '位置をリセット',
    'Rückgängig':
        '元に戻す',
    'Karte darf grösser als der Balken werden':
        'マップを帯より大きくできる',
    'Karte füllt den Balken aus':
        'マップで帯を埋める',
    'Erlaubt jede Kartengrösse: Ist die Karte breiter als der schwarze Balken, bleibt sie an dessen Aussenrand und ragt ins Spielbild. Aus: Die Karte wird nie breiter als der Balken (auf 3440×1440 etwa 31 % der Bildhöhe).':
        'どのマップサイズも許可します：マップが黒帯より広い場合、帯の外側の端に留まり、ゲーム画面にはみ出します。オフ：マップが帯より広くなることはありません（3440×1440 で高さの約 31 %）。',
    'Die Karte wird so gross, dass sie den schwarzen Balken von links bis rechts ausfüllt (bis auf den Abstand zum Rand); der Grössen-Regler gilt dann nicht. Eine hohe Karte stoppt an der Bildhöhe.':
        'マップが黒帯を左から右まで埋めるまで拡大します（端からの距離を除く）。その場合サイズスライダーは適用されません。縦長のマップは画面の高さで止まります。',
    'Nimmt die letzte Änderung an Position oder Grösse zurück (Karte, Systemwerte, Musik) – auch mit Strg+Z auf dieser Seite. Ein ganzes Ziehen zählt als ein Schritt.':
        '位置やサイズの最後の変更を取り消します（マップ、システム値、音楽）– このページでは Ctrl+Z でも可能です。1 回のドラッグ全体が 1 ステップです。',
    'Merkt Position und Grösse aller Elemente getrennt für jede Grösse des DBD-Fensters (z. B. Vollbild 3440×1440 und ein kleineres Fenster) und lädt sie automatisch, sobald DBD in dieser Grösse läuft.':
        '各要素の位置とサイズを DBD ウィンドウのサイズごとに別々に記憶し（例：フルスクリーン 3440×1440 と小さいウィンドウ）、DBD がそのサイズで起動するとすぐに自動で読み込みます。',
    'Nichts rückgängig zu machen.':
        '元に戻すものはありません。',
    'Position/Grösse rückgängig gemacht.':
        '位置/サイズを元に戻しました。',
    'Position und Grösse je DBD-Fenstergrösse merken':
        'DBD のウィンドウサイズごとに位置とサイズを記憶する',
    'DBD-Fenster {size}: Layout für diese Grösse geladen.':
        'DBD ウィンドウ {size}：このサイズのレイアウトを読み込みました。',
    'DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.':
        'DBD ウィンドウ {size}：新しいサイズ – 今後はこのサイズのレイアウトを記憶します。',
    'Aktuell: Layout für {size} · {n} Grössen gemerkt':
        '現在：{size} のレイアウト · {n} 個のサイズを記憶中',
    'Position zurückgesetzt (automatisch).':
        '位置をリセットしました（自動）。',
    'keine Map':
        'マップなし',
    'ausgeblendet':
        '非表示',
    'Menü offen':
        'メニューが開いている',
    'aktives Fenster ist {window}':
        'アクティブウィンドウは {window}',
    'DBD-Fenster {w}×{h}':
        'DBD ウィンドウ {w}×{h}',
    'Bildschirm':
        '画面',
    'Overlay sichtbar bei {pos} über {src}.':
        'オーバーレイを {src} 上の {pos} に表示中。',
    'Overlay pausiert: {reason}.':
        'オーバーレイを一時停止：{reason}。',
    '{text} – Details in fogscout.log':
        '{text} – 詳細は fogscout.log に記録',
    '{text} ({n}× seit {since}) – Details in fogscout.log':
        '{text}（{since} 以降 {n} 回）– 詳細は fogscout.log に記録',
    'Erkennung neu gestartet ({n}/{total})':
        '検出を再開しました（{n}/{total}）',
    'Map-Banner gefunden, lese …':
        'マップバナーを検出、読み取り中…',
    'automatisch erkannt ({p})':
        '自動検出（{p}）',
    'Layout {n} ({p})':
        'レイアウト {n}（{p}）',
    'Rundentimer gestartet.':
        'ラウンドタイマーを開始しました。',
    'Rundentimer gestoppt: {time}.':
        'ラウンドタイマーを停止しました：{time}。',
    'Erkannt: {map} – gelesen „{name}“ / „{realm}“':
        '検出：{map} – 読み取り「{name}」/「{realm}」',
    'Layout unsicher – falls falsch: Layout-Knopf oder {keys}.':
        'レイアウトが不確実です – 誤っている場合：レイアウトボタンまたは {keys}。',
    'Mitten in der Runde „{name}“ / „{realm}“ gelesen (am ehesten {map}) – ignoriert: Map-Banner gibt es nur am Rundenstart, und die Lesung war nicht eindeutig.':
        'ラウンドの途中で「{name}」/「{realm}」を読み取りました（最も近い：{map}）– 無視しました：マップバナーはラウンド開始時にのみ表示され、読み取りも明確ではありませんでした。',
    'Banner gesehen, aber keine bekannte Map: „{text}“. Map manuell wählen oder mit „Zuordnen …“ dauerhaft zuordnen.':
        'バナーを確認しましたが、既知のマップではありません：「{text}」。マップを手動で選択するか、「割り当て…」で恒久的に割り当ててください。',
    'Runde vorbei ({reason}) – Overlay ausgeblendet.':
        'ラウンド終了（{reason}）– オーバーレイを非表示にしました。',
    'Runde vorbei ({reason}).':
        'ラウンド終了（{reason}）。',
    'Menü offen (Mauszeiger sichtbar) – Overlay pausiert.':
        'メニューが開いています（マウスポインター表示中）– オーバーレイを一時停止しました。',
    'Zurück im Spiel – Overlay wieder sichtbar.':
        'ゲームに戻りました – オーバーレイを再表示しました。',
    'Die Erkennung ist abgestürzt – Details in fogscout.log':
        '検出がクラッシュしました – 詳細は fogscout.log に記録',
    'Die Erkennung ist abgestürzt:':
        '検出がクラッシュしました：',
    'Die Erkennung ist abgestürzt – bitte Fog Scout neu starten.':
        '検出がクラッシュしました – Fog Scout を再起動してください。',
    'Nichts gefunden':
        '何も見つかりませんでした',
    'Runde gilt jetzt für {map} (vorher {old}).':
        'このラウンドは {map} として数えられるようになりました（以前：{old}）。',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen. Bis zum Neustart wird nichts gespeichert.':
        'settings.json を読み取れませんでした（{error}）– 既定値を読み込みました。再起動まで何も保存されません。',
    'settings.json war nicht lesbar ({error}) – Standardwerte geladen, die alte Datei liegt als settings.json.broken daneben.':
        'settings.json を読み取れませんでした（{error}）– 既定値を読み込み、古いファイルは settings.json.broken として保管しました。',
    'Scan fehlgeschlagen: {error}':
        'スキャンに失敗しました：{error}',
    'per Scan gefunden: „{text}“':
        'スキャンで検出：「{text}」',
    'Scan ({s} s): {map}':
        'スキャン（{s} 秒）：{map}',
    'Realm „{realm}“ hat nur diese Map':
        'レルム「{realm}」にはこのマップしかありません',
    'Scan: Realm „{realm}“ gefunden – bitte Map in der Liste wählen.':
        'スキャン：レルム「{realm}」を検出しました – リストからマップを選択してください。',
    'Scan ({s} s): kein Map- oder Realm-Name auf dem Bildschirm.':
        'スキャン（{s} 秒）：画面にマップ名もレルム名もありません。',
    'Ergebnisbildschirm':
        'リザルト画面',
    'Lobby/Menü':
        'ロビー/メニュー',
    'Ladebildschirm':
        'ロード画面',
    'Clip wird geladen …':
        'クリップを読み込み中…',
    'Vorschaubild und Zeitleiste kommen aus der Aufnahme.':
        'プレビュー画像とタイムラインを録画から読み込んでいます。',
    '{n} von {total} Bildern':
        '{total} 枚中 {n} 枚の画像',
    'Lädt länger als erwartet – das Fenster ist trotzdem bedienbar.':
        '予想より時間がかかっています – ウィンドウはそのまま使用できます。',
    'DBD wurde geschlossen':
        'DBD が終了しました',
    'Menü/Lobby (Mauszeiger lange sichtbar)':
        'メニュー/ロビー（マウスポインターが長時間表示）',
    'keine Map angezeigt':
        'マップが表示されていません',
    'Runde vorbei ({reason})':
        'ラウンド終了（{reason}）',
    'wartet, bis du im Match bist (Map manuell gewählt)':
        'マッチに入るまで待機中（マップは手動選択）',
    'Menü offen – Overlay pausiert':
        'メニューが開いている – オーバーレイを一時停止',
    'im Match':
        'マッチ中',
    'Ausblenden nach der Runde aus':
        'ラウンド後に隠す：オフ',
    'Mauszeiger-Hinweis aus':
        'マウスポインターによる判定：オフ',
    'Mauszeiger-Hinweis ab dem nächsten Map-Banner':
        'マウスポインターによる判定は次のマップバナーから',
    'Mauszeiger: –':
        'マウスポインター：–',
    'Mauszeiger sichtbar':
        'マウスポインター表示',
    'Mauszeiger verborgen':
        'マウスポインター非表示',
    'aus (Einstellung)':
        'オフ（設定）',
    'Runde vorbei – wartet auf die nächste Map':
        'ラウンド終了 – 次のマップを待機中',
    'Automatische Erkennung ist aus':
        '自動検出はオフです',
    'DBD ist minimiert':
        'DBD が最小化されています',
    'DBD gefunden ({w}×{h}) – warte auf Map-Banner':
        'DBD を検出しました（{w}×{h}）– マップバナーを待機中',
    'DBD nicht gefunden – Erkennung startet, sobald DBD läuft':
        'DBD が見つかりません – DBD が起動すると検出を開始します',
    'Bildschirmaufnahme fehlgeschlagen: {error}':
        '画面キャプチャに失敗しました：{error}',
    'Aufnahme ist schwarz – DBD im Modus „Fenster-Vollbild“ betreiben':
        'キャプチャが真っ黒です – DBD を「ウィンドウフルスクリーン」モードで実行してください',
    'Fensteraufnahme nicht möglich, nutze Bildschirmaufnahme ({error})':
        'ウィンドウキャプチャができないため、画面キャプチャを使用します（{error}）',
    'DBD im Hintergrund – Fensteraufnahme aktiv: die Map wird auch erkannt, wenn andere Fenster darüber liegen.':
        'DBD はバックグラウンド – ウィンドウキャプチャ有効：他のウィンドウに覆われていてもマップを検出します。',
    'Rundenende-Erkennung für die gewählte Map ist jetzt aktiv.':
        '選択したマップのラウンド終了検出が有効になりました。',
    'Mauszeiger war beim Map-Banner sichtbar – Menü-Erkennung per Mauszeiger ist für diese Runde aus.':
        'マップバナーの時点でマウスポインターが表示されていました – このラウンドではマウスポインターによるメニュー検出はオフです。',
    'Map zuordnen':
        'マップを割り当て',
    'Gelesen: „{text}“':
        '読み取り：「{text}」',
    'Welche Map war das? Der Name wird künftig automatisch erkannt.':
        'どのマップでしたか？今後はこの名前が自動で認識されます。',
    'Bitte eine Map auswählen.':
        'マップを選択してください。',
    'Abbrechen':
        'キャンセル',
    '„{text}“ wird jetzt als {map} erkannt (eigene Zuordnung).':
        '「{text}」は今後 {map} として認識されます（独自の割り当て）。',
    'zugeordnet: „{text}“':
        '割り当て済み：「{text}」',
    'Der gelesene Text ist zu kurz.':
        '読み取った文字が短すぎます。',
    'Unbekannte Map.':
        '不明なマップです。',
    '„{text}“ ist schon der Name von {map}.':
        '「{text}」は既に {map} の名前です。',
    'Kartenbild hinzufügen':
        'マップ画像を追加',
    'eigenes Bild':
        '独自の画像',
    'Kartenbild gespeichert: {path}':
        'マップ画像を保存しました：{path}',
    'Eigenes Kartenbild für {map} gespeichert: {path}':
        '{map} の独自のマップ画像を保存しました：{path}',
    'wird ab jetzt automatisch erkannt.':
        '今後は自動で検出されます。',
    'Eigenes Kartenbild für {map} gelöscht – das mitgelieferte gilt wieder.':
        '{map} の独自のマップ画像を削除しました – 付属の画像が再び使用されます。',
    'Bitte den Namen der Map eingeben.':
        'マップ名を入力してください。',
    '„{name}“ gibt es schon ({map}) – dann „Bild einer vorhandenen Map ersetzen“ wählen.':
        '「{name}」は既に存在します（{map}）– 代わりに「既存のマップの画像を置き換える」を選んでください。',
    'Noch kein Bild gewählt (PNG, JPG, WebP, GIF)':
        'まだ画像が選択されていません（PNG、JPG、WebP、GIF）',
    'Für welche Map?':
        'どのマップ用ですか？',
    'Ergebnis':
        '結果',
    'Eigenes Bild löschen':
        '独自の画像を削除',
    'Speichern':
        '保存',
    'Bilder':
        '画像',
    'Kartenbild wählen':
        'マップ画像を選択',
    'Für diese Map lässt sich kein Bild speichern.':
        'このマップには画像を保存できません。',
    'Erst ein Bild wählen.':
        '先に画像を選択してください。',
    'Das ist kein lesbares Bild: {error}':
        '読み取り可能な画像ではありません：{error}',
    'Bild konnte nicht verarbeitet werden: {error}':
        '画像を処理できませんでした：{error}',
    'Speichern fehlgeschlagen: {error}':
        '保存に失敗しました：{error}',
    'Eigenes Bild für „{map}“ löschen?':
        '「{map}」の独自の画像を削除しますか？',
    'Löschen fehlgeschlagen: {error}':
        '削除に失敗しました：{error}',
    'Bild wählen …':
        '画像を選択…',
    'Bild einer vorhandenen Map ersetzen':
        '既存のマップの画像を置き換える',
    'Neue Map (fehlt im Programm)':
        '新しいマップ（プログラムにないもの）',
    'Name':
        '名前',
    'Name so, wie er im Map-Banner steht – dann wird die Map automatisch erkannt.':
        'マップバナーに表示されるとおりの名前 – これでマップが自動で検出されます。',
    'Hintergrund entfernen (Dunkelblau und Graulila der Community-Karten) und Rand abschneiden':
        '背景（コミュニティマップの濃い青と灰紫）を除去し、枠を切り取る',
    'Ordner öffnen':
        'フォルダーを開く',
    'Animiertes GIF: wird unverändert übernommen.':
        'アニメーション GIF：そのまま使用します。',
    'Wird gestartet …':
        '起動中…',
    'Version {version}':
        'バージョン {version}',
    'Lade Maps …':
        'マップを読み込み中…',
    'Bereite Overlay vor …':
        'オーバーレイを準備中…',
    'Baue Oberfläche …':
        'インターフェースを構築中…',
    'Starte Erkennung …':
        '検出を開始中…',
    'Öffne Fenster …':
        'ウィンドウを開いています…',
    'Fog Scout ist bereit.':
        'Fog Scout の準備ができました。',
    'Automatische Erkennung':
        '自動検出',
    'Aufnahmen mit OBS':
        'OBS で録画',
    'Lobby-Meldung':
        'ロビー通知',
    'Spielserver anzeigen':
        'ゲームサーバーを表示',
    'Systemwerte im Spiel':
        'ゲーム内のシステム値',
    '„Heute“ im Spiel':
        'ゲーム内の「今日」',
    'Musik im Spiel':
        'ゲーム内の音楽',
    'Discord-Status':
        'Discord のステータス',
    'Spotify „Als nächstes“':
        'Spotify「次の曲」',
    'YouTube-Upload':
        'YouTube アップロード',
    '{name} eingeschaltet.':
        '{name} をオンにしました。',
    '{name} ausgeschaltet.':
        '{name} をオフにしました。',
    'Erkennt die Map beim Match-Start am Banner und blendet die Karte ein. Aus: nur noch von Hand (Scannen, Map wählen). Dasselbe Häkchen steht unter Einstellungen → Erkennung.':
        'マッチ開始時にバナーからマップを読み取り、マップを表示します。オフ：手動のみ（スキャン、マップ選択）。同じチェックボックスが「設定」→「検出」にもあります。',
    'OBS nimmt jede Runde auf: Start beim Map-Banner, Stopp beim Rundenende. Aus: keine neue Aufnahme und keine F8-Clips – eine laufende Aufnahme endet normal mit der Runde. Alles Weitere unter Einstellungen → Aufnahmen.':
        'OBS がすべてのラウンドを録画します：マップバナーで開始、ラウンド終了で停止。オフ：新しい録画も F8 クリップもなし – 実行中の録画は通常どおりラウンドとともに終了します。その他はすべて「設定」→「録画」で。',
    'Ton und Hinweisfenster, sobald DBD eine Lobby gefunden hat. Die Erinnerung beim Countdown und „nur wenn DBD nicht vorne ist“ bleiben unter Einstellungen → Erkennung → Benachrichtigungen.':
        'DBD がロビーを見つけるとすぐに音と通知ウィンドウで知らせます。カウントダウンのリマインダーと「DBD が前面にないときのみ」は「設定」→「検出」→「通知」にあります。',
    'Zeigt Region und Ping des verbundenen Spielservers – auf der Seite Server, im Overlay und in der Statistik. Einschalten fragt Windows einmal nach Administratorrechten; gelesen werden nur Paketköpfe, nie Inhalte.':
        '接続中のゲームサーバーのリージョンと Ping を表示します – サーバーページ、オーバーレイ、統計で。オンにすると Windows が一度管理者権限を要求します。読み取るのはパケットヘッダーのみで、内容は読み取りません。',
    'Die Karte mit CPU-/GPU-Temperatur, Last und Speicher im schwarzen Balken. Einschalten bringt sie an die Position, an der sie zuletzt stand; Position und Zeilen unter Overlay → Systemwerte.':
        '黒帯に CPU/GPU の温度、負荷、メモリを表示するカード。オンにすると最後の位置に戻ります。位置と行は「オーバーレイ」→「システム値」で。',
    'Die Karte „Heute“ im Spiel: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit. Position unter Overlay → Heute.':
        'ゲーム内の「今日」カード：ラウンド数、プレイ時間、平均キル数/脱出数、時計。位置は「オーバーレイ」→「今日」で。',
    'Die Musikkarte „Läuft gerade“ im Spiel (Titel, Interpret, Cover aus der Windows-Mediensteuerung). Position und Aussehen unter Overlay → Musik.':
        'ゲーム内の「再生中」音楽カード（Windows のメディアコントロールから取得したタイトル、アーティスト、カバー）。位置と外観は「オーバーレイ」→「音楽」で。',
    'Rich Presence: Map, Rolle und Rundenzeit in deinem Discord-Status. Application-ID und Einzelheiten unter Einstellungen → Verbindungen → Discord.':
        'Rich Presence：マップ、役割、ラウンド時間を Discord のステータスに表示します。アプリケーション ID と詳細は「設定」→「接続」→「Discord」で。',
    'Die Liste „Als nächstes“ aus Spotify in der Musikkarte. Client-ID und Anmeldung unter Einstellungen → Verbindungen → Spotify.':
        'Spotify の「次の曲」リストを音楽カードに表示します。クライアント ID とログインは「設定」→「接続」→「Spotify」で。',
    'Neue Clips (F8, Editor) gehen von selbst auf YouTube. Aus: nichts Neues wird eingereiht – was schon in der Warteschlange steht, lädt fertig; Runden lädst du weiter per Rechtsklick hoch. Einstellungen → Verbindungen → YouTube.':
        '新しいクリップ（F8、エディター）を自動で YouTube にアップロードします。オフ：新しいものはキューに入りません – キュー内のものは完了します。ラウンドは引き続き右クリックでアップロードできます。「設定」→「接続」→「YouTube」。',
    'Werkzeuge für die Fehlersuche ein- oder ausklappen: Live-Zustand der Rundenende-Erkennung, Debug-Bilder, Bildschirm scannen.':
        'トラブルシューティングツールを表示/非表示にします：ラウンド終了検出のライブ状態、デバッグ画像、画面スキャン。',
    'Klicken und die neue Tastenkombination drücken: Strg/Alt + Taste, oder eine Taste allein (F1–F12, Numpad, Pause, Rollen, Einfg, Pos1, Ende, Bild↑/↓ – die gilt nur, solange DBD vorne ist). Esc bricht ab, Entf schaltet den Hotkey aus.':
        'クリックして新しいキーの組み合わせを押してください：Ctrl/Alt + キー、または単一キー（F1～F12、テンキー、Pause、Scroll Lock、Insert、Home、End、Page Up/Down – DBD が前面にある間のみ動作）。Esc でキャンセル、Delete でホットキーをオフにします。',
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
        'DBD が前面にある間のみ動作します – DBD 自体は {keys} を受け取らなくなります（DBD で割り当てていない場合は問題ありません）。',
    'Map-Namen in dieser Spielsprache erkennen. Nur die Sprachen anhaken, in denen du spielst – weniger Sprachen, weniger Verwechslungen.':
        'このゲーム言語のマップ名を認識します。プレイする言語のみにチェックを入れてください – 言語が少ないほど取り違えも減ります。',
    'Meldungen der Art „{category}“ im Log anzeigen.':
        '「{category}」のメッセージをログに表示します。',
    'Karte ausblenden (die automatische Erkennung läuft weiter).':
        'マップを非表示にします（自動検出は継続します）。',
    'Karte wieder einblenden.':
        'マップを再表示します。',
    'Die Erkennung war beim Layout nicht sicher – stimmt es nicht, hier weiterschalten.':
        '検出がレイアウトについて確信を持てませんでした – 誤っている場合はここで切り替えてください。',
    'Wechselt zum nächsten Layout dieser Map (z. B. Coal Tower ↔ Coal Tower II). Die Layouts ab II gibt es seit Patch 8.6.0 nur noch in Custom Games.':
        'このマップの次のレイアウトに切り替えます（例：Coal Tower ↔ Coal Tower II）。パッチ 8.6.0 以降、II 以降のレイアウトはカスタムマッチにのみ存在します。',
    'Test sofort beenden.':
        '今すぐテストを終了します。',
    'Zeigt 10 s lang alles, was das Overlay im Match zeigt – Karte, Systemwerte, „Heute“ und Musik (Beispielwerte, wenn nichts anliegt) – an den eingestellten Stellen, auch ohne DBD. Nochmal drücken beendet den Test.':
        'マッチ中にオーバーレイが表示するものすべて（マップ、システム値、「今日」、音楽。何もない場合はサンプル値）を、DBD なしでもそれぞれの位置に 10 秒間表示します。もう一度押すとテストを終了します。',
    'Verschieben beenden.':
        '移動を終了します。',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen – falls die automatische Erkennung das Banner verpasst hat.':
        '画面全体からマップ名またはレルム名をすぐに検索します – 自動検出がバナーを見逃した場合に。',
    'Eigenes Kartenbild für diese unbekannte Map anlegen – Name und Realm sind schon eingetragen, der Hintergrund wird automatisch entfernt.':
        'この不明なマップ用に独自のマップ画像を作成します – 名前とレルムは入力済みで、背景は自動で除去されます。',
    'Der gelesene Name gehört zu einer vorhandenen Map (z. B. anders geschrieben)? Einmal zuordnen – danach wird er automatisch erkannt.':
        '読み取った名前が既存のマップのものですか（例：綴りが異なる）？一度割り当てれば、以後は自動で認識されます。',
    'Hinweis ausblenden.':
        'この通知を非表示にします。',
    'Eigenes Bild für eine Map wählen: vorhandenes Bild ersetzen oder neue Map anlegen. Rand und Hintergrund werden automatisch entfernt.':
        'マップ用の独自の画像を選択します：既存の画像を置き換えるか、新しいマップを作成します。枠と背景は自動で除去されます。',
    'Position wieder auf „automatisch“ stellen (auf Ultrawide im linken schwarzen Rand).':
        '位置を「自動」に戻します（ウルトラワイドでは左の黒帯）。',
    'Auf breiten Monitoren bleibt die Karte im schwarzen Balken, in dem sie liegt, und wird bei Bedarf verkleinert. Mitten über dem Spiel platziert gilt keine Begrenzung. Ohne schwarze Balken neben dem Spielbild (16:9, z. B. 1920×1080) sind die Balken-Optionen ausgegraut.':
        'ワイドモニターでは、マップは配置された黒帯の中に留まり、必要に応じて縮小されます。ゲームの中央に配置した場合は制限がありません。ゲーム画面の横に黒帯がない場合（16:9、例：1920×1080）、帯のオプションはグレー表示になります。',
    'Karte ausblenden, solange ein anderes Fenster (Browser, Discord …) im Vordergrund ist.':
        '別のウィンドウ（ブラウザー、Discord…）が前面にある間はマップを隠します。',
    'Zusätzliche Namenszeile über der Karte – die meisten Kartenbilder tragen den Namen schon selbst.':
        'マップの上に追加の名前行 – ほとんどのマップ画像には既に名前が入っています。',
    'Zeit seit dem Einblenden der Karte, gross unter der Karte.':
        'マップが表示されてからの時間を、マップの下に大きく表示します。',
    'Region und Ping des Spielservers unter der Karte. Braucht „Verbundener Spielserver“ im Tab Server.':
        'ゲームサーバーのリージョンと Ping をマップの下に表示します。「サーバー」タブの「接続中のゲームサーバー」が必要です。',
    'Aus: Karte liegt auf einem dunklen Rechteck – besser lesbar über hellen Spielszenen.':
        'オフ：マップを暗い長方形の上に表示します – 明るいゲームシーンでも読みやすくなります。',
    'Liest das Map-Banner am Match-Anfang und blendet die passende Karte ein. Aus: Map nur von Hand wählen.':
        'マッチ開始時にマップバナーを読み取り、該当するマップを表示します。オフ：マップは手動でのみ選択します。',
    'Blendet die Karte nach der Runde aus (Ergebnisbildschirm, Lobby, Ladebildschirm, DBD beendet).':
        'ラウンド後にマップを隠します（リザルト画面、ロビー、ロード画面、DBD の終了）。',
    'Karte verschwindet, solange der Mauszeiger im Spiel sichtbar ist (ESC-Menü), und kommt danach wieder.':
        'ゲーム内でマウスポインターが表示されている間（ESC メニュー）はマップが消え、その後再表示されます。',
    'Fensteraufnahme wie bei OBS: erkennt das Banner auch, wenn DBD verdeckt ist. Nur solange DBD im Hintergrund ist.':
        'OBS のようなウィンドウキャプチャ：DBD が覆われていてもバナーを検出します。DBD がバックグラウンドの間のみ。',
    'Speichert gelesene Banner und verkleinerte Bilder der Runde im Ordner debug/ – nur zur Fehlersuche, kostet Speicherplatz.':
        '読み取ったバナーとラウンドの小さな画像を debug/ フォルダーに保存します – トラブルシューティング専用で、ディスク容量を使用します。',
    'Sucht sofort auf dem ganzen Bildschirm nach einem Map- oder Realm-Namen.':
        '画面全体からマップ名またはレルム名をすぐに検索します。',
    'Kopiert technische Infos (Fenster, Overlay, letzte Rundenende-Prüfungen) in die Zwischenablage – zum Weitergeben bei Problemen.':
        '技術情報（ウィンドウ、オーバーレイ、直近のラウンド終了チェック）をクリップボードにコピーします – 問題が起きたときに伝えるために。',
    'Misst den Ping zu allen AWS-Regionen (UDP-Beacon von Amazon GameLift).':
        'すべての AWS リージョンへの Ping を測定します（Amazon GameLift の UDP ビーコン）。',
    'Nur die angehakten Regionen erlauben – trägt die übrigen in die Windows-hosts-Datei ein (fragt nach Administratorrechten).':
        'チェックを入れたリージョンのみを許可します – その他を Windows の hosts ファイルに追加します（管理者権限を要求します）。',
    'Entfernt die Einträge des Programms aus der hosts-Datei – alle Regionen wieder erlaubt.':
        'hosts ファイルからプログラムのエントリーを削除します – すべてのリージョンが再び許可されます。',
    'Log-Anzeige leeren (die Log-Datei bleibt).':
        'ログ表示をクリアします（ログファイルは残ります）。',
    'Öffnet fogscout.log mit allen Details.':
        'すべての詳細を含む fogscout.log を開きます。',
    'Dunkle oder helle Darstellung des Steuerfensters.':
        'コントロールウィンドウのダーク/ライトの外観。',
    'Alle Hotkeys auf die Voreinstellung zurücksetzen.':
        'すべてのホットキーを既定値に戻します。',
    'Minimieren versteckt das Fenster im Infobereich; Doppelklick auf das Symbol holt es zurück.':
        '最小化するとウィンドウが通知領域に隠れます。アイコンをダブルクリックすると元に戻ります。',
    'Startet das Programm bei der Anmeldung im Infobereich. Nur als Administrator änderbar.':
        'サインイン時にプログラムを通知領域で起動します。管理者のみ変更できます。',
    'Holt beim Start über die Verknüpfung den neuen Stand von GitHub. Eigene Änderungen werden nie überschrieben.':
        'ショートカットから起動したときに GitHub から最新バージョンを取得します。独自の変更が上書きされることはありません。',
    'Alle eigenen Map-Zuordnungen löschen (die Namen werden dann wieder als unbekannt gemeldet).':
        '独自のマップ割り当てをすべて削除します（名前は再び不明として報告されます）。',
    'Öffnet den Ordner mit den mitgelieferten Kartenbildern.':
        '付属のマップ画像のフォルダーを開きます。',
    'PNG, JPG, WebP oder GIF auswählen – zum Beispiel ein Original mit Hintergrund.':
        'PNG、JPG、WebP または GIF を選択してください – 例えば背景付きのオリジナル。',
    'Dein Bild ersetzt das mitgelieferte Bild dieser Map (bzw. dieses Layouts). Löschen stellt das Original wieder her.':
        'この画像が、このマップ（またはこのレイアウト）の付属画像を置き換えます。削除するとオリジナルに戻ります。',
    'Legt eine neue Map an. Sie wird erkannt, wenn der Name so geschrieben ist wie im Map-Banner.':
        '新しいマップを作成します。名前がマップバナーと同じ表記なら検出されます。',
    'Öffnet den Ordner user_maps mit deinen eigenen Kartenbildern.':
        '独自のマップ画像がある user_maps フォルダーを開きます。',
    'Löscht dein Bild für die gewählte Map – danach gilt wieder das mitgelieferte.':
        '選択したマップの独自の画像を削除します – 付属の画像が再び使用されます。',
    'Bild umwandeln und speichern; die Karte wird sofort angezeigt.':
        '画像を変換して保存します。マップはすぐに表示されます。',
    'Schliessen, ohne etwas zu ändern.':
        '何も変更せずに閉じます。',
    'Macht Dunkelblau (#282a42) und Graulila (#535781) der Community-Karten transparent, schneidet den gleichfarbigen Rand ab und bringt das Bild auf 1280 px Höhe.':
        'コミュニティマップの濃い青（#282a42）と灰紫（#535781）を透明にし、同じ色の枠を切り取り、画像の高さを 1280 px に拡大縮小します。',
    '? unsicher – {keys} = falsch':
        '? 不確実 – {keys} = 誤り',
    'Falsch erkannt':
        'マップが違う',
    'Stimmt':
        '正しい',
    'Unsicher erkannt: {map} (gelesen „{name}“)':
        '不確実な検出：{map}（読み取り「{name}」）',
    'Unsicher erkannt: {map} – gelesen „{name}“, Passung {fit}. Falls falsch: {keys} oder „Falsch erkannt“.':
        '不確実な検出：{map} – 読み取り「{name}」、一致度 {fit}。誤っている場合：{keys} または「マップが違う」。',
    '{map} bestätigt.':
        '{map} を確定しました。',
    'Nichts zu verwerfen: keine automatisch erkannte Map eingeblendet.':
        '破棄するものはありません：自動検出されたマップが表示されていません。',
    'Verworfen: {map} – die Runde wird nicht gezählt.':
        '破棄しました：{map} – このラウンドは数えられません。',
    'Die erkannte Map stimmt nicht: Karte ausblenden, Timer zurücksetzen, die Runde wird nicht gezählt. Geht auch im Spiel mit dem Hotkey (Standard Strg+Alt+X).':
        '検出されたマップが間違っています：マップを隠し、タイマーをリセットし、ラウンドは数えられません。ゲーム内でもホットキー（既定 Ctrl+Alt+X）で操作できます。',
    'Die Map stimmt – Hinweis „unsicher“ ausblenden.':
        'マップは正しい – 「不確実」の表示を隠します。',
    'als falsch verworfen':
        '誤りとして破棄',
    'Ping {ms} ms':
        'Ping {ms} ms',
    'Ø Kills':
        '平均キル数',
    '4K':
        '4K',
    'Entkommen':
        '脱出',
    'entkommen':
        '脱出',
    'tot':
        '死亡',
    'aufgegeben':
        '放棄',
    'verlassen':
        '退出',
    'Stats-Seite öffnen, wenn DBD beendet wird':
        'DBD を閉じたら統計ページを開く',
    'Userscript kopieren':
        'ユーザースクリプトをコピー',
    'Stats-Seite öffnen':
        '統計ページを開く',
    '⚠ Unbekannter Status auf der Stats-Seite: {list} – zählt nicht. Bitte melden („Diagnose kopieren“).':
        '⚠ 統計ページに不明なステータス：{list} – 数えられていません。報告してください（「診断情報をコピー」）。',
    '⚠ Lücke: zwischen {start} und {end} fehlen vielleicht Matches – die Seite zeigt nur die letzten 30. Seite öfter öffnen.':
        '⚠ 欠落：{start} から {end} の間のマッチが欠けている可能性があります – ページには直近 30 件しか表示されません。ページをもっと頻繁に開いてください。',
    '⚠ {n}× andere Map als erkannt, zuletzt {when}: erkannt {ours}, laut Seite {theirs}.':
        '⚠ 検出と異なるマップが {n} 回、最後は {when}：検出 {ours}、ページでは {theirs}。',
    '⚠ Das Userscript ist veraltet (Version {old}, aktuell {new}) – „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '⚠ ユーザースクリプトが古くなっています（バージョン {old}、最新 {new}）– 「ユーザースクリプトをコピー」して Tampermonkey で置き換えてください。',
    'Stats-Seite konnte nicht geöffnet werden: {error}':
        '統計ページを開けませんでした：{error}',
    'DBD beendet – Stats-Seite geöffnet; das Userscript speichert die Matches.':
        'DBD を閉じました – 統計ページを開きました。ユーザースクリプトがマッチを保存します。',
    'Userscript nicht gefunden: {error}':
        'ユーザースクリプトが見つかりません：{error}',
    'Userscript in die Zwischenablage kopiert. In Tampermonkey: „Neues Skript erstellen“ → alles ersetzen (Strg+A, Strg+V) → Speichern. Danach stats.deadbydaylight.com öffnen und anmelden.':
        'ユーザースクリプトをクリップボードにコピーしました。Tampermonkey で：「新規スクリプトを作成」→ すべて置き換え（Ctrl+A、Ctrl+V）→ 保存。その後 stats.deadbydaylight.com を開いてサインインしてください。',
    'Offizielle Match-Daten: {n} Matches gelesen, {new} neu – Datei gelöscht.':
        '公式マッチデータ：{n} 件のマッチを読み取り、うち新規 {new} 件 – ファイルを削除しました。',
    'Offizielle Match-Daten: zwischen {start} und {end} fehlen vielleicht Matches (die Seite zeigt nur die letzten 30).':
        '公式マッチデータ：{start} から {end} の間のマッチが欠けている可能性があります（ページには直近 30 件しか表示されません）。',
    '{name} gelesen, aber nicht gelöscht: {error}':
        '{name} を読み取りましたが、削除できませんでした：{error}',
    '{name} ist keine Match-Datei von Fog Scout – bleibt liegen.':
        '{name} は Fog Scout のマッチファイルではありません – そのままにしました。',
    'Unbekannter Status auf der Stats-Seite: „{status}“ – zählt nicht für Kills/Escapes. Bitte melden.':
        '統計ページに不明なステータス：「{status}」– キル/脱出には数えられていません。報告してください。',
    'Schliesst du DBD nach mindestens einer Runde, öffnet das Programm stats.deadbydaylight.com im Browser. Das Userscript speichert dann die letzten 30 Matches, das Programm liest sie ein und löscht die Datei. Nie während DBD läuft.':
        '少なくとも 1 ラウンドプレイした後に DBD を閉じると、プログラムがブラウザーで stats.deadbydaylight.com を開きます。ユーザースクリプトが直近 30 件のマッチを保存し、プログラムがそれを読み取ってファイルを削除します。DBD の実行中は決して開きません。',
    'Kopiert das Userscript in die Zwischenablage. In Tampermonkey „Neues Skript erstellen“, alles ersetzen und speichern. Es liest nur die Match-Liste, die die Seite selbst lädt – keine Konto- oder Login-Daten – und schickt nichts irgendwohin.':
        'ユーザースクリプトをクリップボードにコピーします。Tampermonkey で「新規スクリプトを作成」し、すべて置き換えて保存してください。ページ自体が読み込むマッチリストのみを読み取り（アカウントやログインのデータは読み取りません）、どこにも何も送信しません。',
    'Öffnet stats.deadbydaylight.com jetzt. Mit installiertem Userscript kommen die Matches gleich danach an.':
        '今すぐ stats.deadbydaylight.com を開きます。ユーザースクリプトがインストールされていれば、その直後にマッチが届きます。',
    'Vom Programm erkannt: {seen} von {n} ({share})':
        'プログラムが検出：{n} 件中 {seen} 件（{share}）',
    'Nicht erkannt (oder das Programm lief nicht): {list}':
        '検出されなかった（またはプログラムが実行されていなかった）：{list}',
    'Rundenende erkannt: Median {off} gegenüber dem Ende laut Seite ({n} Runden; + = später)':
        'ラウンド終了の検出：ページ上の終了時刻に対して中央値 {off}（{n} ラウンド、+ = 遅い）',
    '{n} Mio.':
        '{n}M',
    'Ø BP':
        '平均 BP',
    '✓ {n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        '✓ ラウンド終了が {n} 回検出されませんでしたが、統計ページの長さで数えました。',
    'Runden vom Map-Banner bis zum Rundenende (ab 1 min), nur lokal gespeichert. Kills, Escapes und Bloodpoints laut stats.deadbydaylight.com, sobald eine Runde dort zugeordnet ist.':
        'マップバナーからラウンド終了までのラウンド（1 分以上）。ローカルにのみ保存されます。キル、脱出、ブラッドポイントは、ラウンドが stats.deadbydaylight.com のマッチと紐付けられると取得されます。',
    '{n}× Abandon':
        '放棄 {n} 回',
    'Ein Skin oder neuer Killer steht unter seinem eigenen Namen? Zeile markieren, Killer wählen, „Zuordnen“ – gilt auch rückwirkend.':
        '衣装や新キラーが独自の名前で表示されますか？行を選択し、キラーを選んで「割り当て」– 過去のラウンドにも適用されます。',
    'Abgleich mit der Stats-Seite':
        '統計ページと照合',
    'Noch keine offiziellen Daten.':
        '公式データはまだありません。',
    'Neu seit {version}':
        '{version} 以降の新機能',
    'sofort':
        '即時',
    'HWiNFO läuft nicht: CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen.':
        'HWiNFO が実行されていません：CPU 温度、CPU 電力、コア、FPS がありません。',
    'Systemwerte: HWiNFO läuft nicht – CPU-Temperatur, CPU-Leistung, Kerne und FPS fehlen in dieser Runde.':
        'システム値：HWiNFO が実行されていません – このラウンドでは CPU 温度、CPU 電力、コア、FPS がありません。',
    'Vorwoche {value}':
        '先週 {value}',
    '{n} Pkt.':
        '{n} pt',
    'Montag bis jetzt gegenüber der Vorwoche (Mo–So); Custom und Farming zählen nicht.':
        '月曜日から現在までを前週（月～日）と比較。カスタムマッチとファーミングは数えません。',
    'Sicherung: {files} nach {folder}/ kopiert (die letzten {n} Stände bleiben).':
        'バックアップ：{files} を {folder}/ にコピーしました（直近 {n} 個のコピーを保持）。',
    '{n} Dateien, zuletzt {day}':
        '{n} 個のファイル、最新 {day}',
    '1 Datei, zuletzt {day}':
        '1 個のファイル、最新 {day}',
    'behalten (nie aufgeräumt)':
        '保持（自動削除しない）',
    'wartet auf den YouTube-Upload':
        'YouTube へのアップロード待ち',
    'auf YouTube':
        'YouTube にあり',
    'Karte im Spiel':
        'ゲーム内のマップ',
    'OBS läuft nicht, oder sein WebSocket-Server ist aus':
        'OBS が起動していないか、WebSocket サーバーがオフです',
    'OBS antwortet nicht':
        'OBS が応答しません',
    'OBS hat die Verbindung getrennt':
        'OBS が接続を閉じました',
    'noch keine':
        'まだありません',
    'Tägliche Kopie von rounds.jsonl und official.jsonl nach {folder}/ (nur bei Änderungen, die letzten {n} Stände je Datei; vor „Alle Runden löschen“ eine zusätzliche): {state}':
        'rounds.jsonl と official.jsonl を毎日 {folder}/ にコピー（変更時のみ、ファイルごとに直近 {n} 個のコピー。「すべてのラウンドを削除」の前にもう 1 個）：{state}',
    'Verstanden':
        '了解',
    'Aus HISTORY.md (Deutsch), die neuesten zuerst.':
        'HISTORY.md（ドイツ語）より、新しい順。',
    'Blendet die Karte „Neu seit …“ aus, bis die nächste neue Version kommt.':
        '次の新バージョンが届くまで「… 以降の新機能」カードを隠します。',
    'Offizielle Match-Daten':
        '公式マッチデータ',
    'Einmal einrichten: Tampermonkey im Browser installieren, „Userscript kopieren“ und dort als neues Skript einfügen und speichern, auf stats.deadbydaylight.com anmelden. Chrome/Edge: in den Details der Erweiterung „Allow User Scripts“ einschalten, sonst läuft kein Skript. Beim Öffnen der Seite speichert das Skript neue Matches (die letzten 30) im Download-Ordner; das Programm liest die Datei und löscht sie. Es geht dafür selbst nicht ins Internet.':
        '初回設定：ブラウザーに Tampermonkey をインストールし、「ユーザースクリプトをコピー」して新規スクリプトとして貼り付けて保存し、stats.deadbydaylight.com にサインインします。Chrome/Edge：拡張機能の詳細で「ユーザースクリプトを許可」をオンにしてください。そうしないとスクリプトが実行されません。ページを開くと、スクリプトが新しいマッチ（直近 30 件）をダウンロードフォルダーに保存し、プログラムがそのファイルを読み取って削除します。プログラム自身はこのためにインターネットに接続しません。',
    'Alle Matches neu speichern':
        'すべてのマッチを再保存',
    'Öffnet die Stats-Seite so, dass das Userscript ihre letzten 30 Matches noch einmal speichert, auch wenn keines neu ist – nach einer Neuinstallation oder wenn die Datei verloren ging.':
        '統計ページを開き、新しいマッチがなくてもユーザースクリプトに直近 30 件のマッチをもう一度保存させます – 再インストール後やファイルを紛失した場合に。',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) speichert ihre letzten 30 Matches noch einmal, auch wenn keines neu ist; das Programm übernimmt sie gleich – bekannte zählen nur einmal. Kommt keine Datei: in der Console des Browsers (F12) steht, ob das Skript läuft. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '統計ページがブラウザーで開きます。ユーザースクリプト（バージョン {n} 以降）は、新しいマッチがなくても直近 30 件のマッチをもう一度保存します。プログラムはすぐに取り込みます – 既知のものは 1 回だけ数えます。ファイルが届かない場合：ブラウザーのコンソール（F12）でスクリプトが動作しているか確認できます。古いユーザースクリプト：先に「ユーザースクリプトをコピー」して Tampermonkey で置き換えてください。',
    'Verlauf':
        '推移',
    'Nur Runden, die einem Match auf der Stats-Seite zugeordnet sind. Die Maus über einer Säule zeigt Wert und Anzahl der Runden.':
        '統計ページのマッチと紐付けられたラウンドのみ。列にカーソルを合わせると値とラウンド数が表示されます。',
    'Killer – Ø Kills {per}':
        'キラー – 平均キル数 {per}',
    'Survivor – entkommen {per}':
        'サバイバー – 脱出 {per}',
    'pro Stunde':
        '1 時間あたり',
    'pro Tag':
        '1 日あたり',
    'pro Woche':
        '1 週間あたり',
    'KW {n}':
        '第 {n} 週',
    '{when}: Ø {kills} Kills · {n} Runden':
        '{when}：平均 {kills} キル · {n} ラウンド',
    '{when}: {share} entkommen · {n} Runden':
        '{when}：脱出 {share} · {n} ラウンド',
    'Keine Killer-Runden mit offiziellen Daten in dieser Auswahl.':
        'この選択範囲には公式データのあるキラーのラウンドがありません。',
    'Keine Survivor-Runden mit offiziellen Daten in dieser Auswahl.':
        'この選択範囲には公式データのあるサバイバーのラウンドがありません。',
    'Ø {kills} Kills':
        '平均 {kills} キル',
    '{share} entkommen':
        '脱出 {share}',
    'Meldung, wenn Match-Daten eingelesen und gelöscht wurden':
        'マッチデータを読み取って削除したら通知する',
    'Zeigt unten rechts kurz, wie viele Matches gelesen wurden und dass die Datei gelöscht ist – nicht, solange DBD im Vordergrund ist. Im Log steht es immer.':
        '読み取ったマッチ数とファイルを削除したことを、右下に短く表示します – DBD が前面にある間は表示しません。ログには常に記録されます。',
    '{n} Matches gelesen, davon {new} neu. Die Datei wurde gelöscht.':
        '{n} 件のマッチを読み取り、うち新規 {new} 件。ファイルは削除されました。',
    '{name} wurde gelesen, konnte aber nicht gelöscht werden – Details im Log.':
        '{name} を読み取りましたが、削除できませんでした – 詳細はログを参照。',
    'Links oben (über der Karte)':
        '左上（マップの上）',
    'Rechts oben':
        '右上',
    'GPU: {name}':
        'GPU：{name}',
    'GPU: keine NVIDIA-Karte gefunden':
        'GPU：NVIDIA カードが見つかりません',
    'CPU-Temperatur: aus HWiNFO':
        'CPU 温度：HWiNFO から取得',
    'Systemwerte (CPU/GPU-Temperatur, Auslastung, VRAM, RAM)':
        'システム値（CPU/GPU 温度、負荷、VRAM、RAM）',
    'nach Map':
        'マップ別',
    'nach Killer':
        'キラー別',
    'GPU Ø °C':
        'GPU 平均 °C',
    'GPU max':
        'GPU 最大',
    'CPU Ø °C':
        'CPU 平均 °C',
    'CPU max':
        'CPU 最大',
    'GPU Ø Last':
        'GPU 平均負荷',
    'Ø Watt':
        '平均ワット',
    'Noch keine Systemwerte in dieser Auswahl (Tab Overlay → Systemwerte einschalten).':
        'この選択範囲にはまだシステム値がありません（「オーバーレイ」タブ → システム値をオン）。',
    'GPU DROSSELT (TEMP.)':
        'GPU THROTTLED（温度）',
    'GPU DROSSELT (HW)':
        'GPU THROTTLED（HW）',
    'Hotspot max {v} °C':
        'ホットスポット最大 {v} °C',
    'Hotspot max':
        'ホットスポット最大',
    'GPU-Temperatur – Ø {per}':
        'GPU 温度 – 平均 {per}',
    'Noch keine GPU-Temperaturen in dieser Auswahl.':
        'この選択範囲にはまだ GPU 温度がありません。',
    '{when}: Ø {avg} °C · max {max} °C · {n} Runden':
        '{when}：平均 {avg} °C · 最大 {max} °C · {n} ラウンド',
    'Werte der Systemwerte-Anzeige (Tab Overlay) während der Runden – nur Runden, in denen sie eingeschaltet war. CPU-Temperatur nur mit HWiNFO. „Wann/Wo“ zeigt, auf welchen Maps oder zu welcher Tageszeit der PC am heißesten läuft. „Gedrosselt“: Sekunden, in denen die GPU wegen Temperatur oder Hardware langsamer lief (nur NVIDIA). „–“: in diesen Runden nicht erfasst – CPU-Temperatur, -Leistung, Kerne und FPS gibt es nur, solange HWiNFO läuft, und jeder Wert braucht mindestens 10 Sekunden Messwerte in der Runde.':
        'ラウンド中のシステム値表示（「オーバーレイ」タブ）の値 – 表示がオンだったラウンドのみ。CPU 温度は HWiNFO 使用時のみ。「いつ/どこで」は、PC が最も熱くなるマップや時間帯を示します。「Throttled」：温度またはハードウェアが原因で GPU の速度が落ちていた秒数（NVIDIA のみ）。「–」：そのラウンドでは記録されていません – CPU 温度、電力、コア、FPS は HWiNFO の実行中のみ存在し、各値にはラウンド中に少なくとも 10 秒間の測定値が必要です。',
    'Eigene Position (mit der Maus verschieben)':
        '独自の位置（マウスでドラッグ）',
    'SYSTEMWERTE':
        'システム値',
    'Direkt über der Karte (wandert mit)':
        'マップのすぐ上（マップとともに移動）',
    'Schriftgrösse':
        'フォントサイズ',
    'Übersicht':
        '概要',
    'Aktuelle Map':
        '現在のマップ',
    'Rundenzeit':
        'ラウンド時間',
    'Ping':
        'Ping',
    'läuft':
        '進行中',
    'letzte Runde':
        '前回のラウンド',
    'startet':
        '開始中',
    '4K: {n} von {total}':
        '4K：{total} 回中 {n} 回',
    '{n} Survivor-Runden':
        'サバイバーのラウンド {n} 回',
    '{n} normal':
        '通常 {n} 回',
    '{n} Farming-Runden · Ø {bp} BP':
        'ファーミングラウンド {n} 回 · 平均 {bp} BP',
    'Spielzeit heute: {time}':
        '今日のプレイ時間：{time}',
    'Systemwerte sind aus (Tab Overlay → Systemwerte).':
        'システム値はオフです（「オーバーレイ」タブ →「システム値」）。',
    'Systemwerte gibt es nur unter Windows.':
        'システム値は Windows でのみ利用できます。',
    'Erscheinen, sobald DBD läuft.':
        'DBD が起動するとすぐに表示されます。',
    'OK':
        'OK',
    '4 Kills · leer = weniger als {n} Runden':
        '4 キル · 空欄 = {n} ラウンド未満',
    'Killer × Map – Ø Kills laut Stats-Seite':
        'キラー × マップ – 統計ページの平均キル数',
    'Maps – am häufigsten gespielt':
        'マップ – プレイ回数順',
    'Median {time}':
        '中央値 {time}',
    'Noch keine Killer-Runde mit Ergebnis von der Stats-Seite.':
        '統計ページの結果があるキラーのラウンドはまだありません。',
    'keine Killer-Runden mit Stats-Daten':
        '統計データのあるキラーのラウンドなし',
    'keine Survivor-Runden mit Stats-Daten':
        '統計データのあるサバイバーのラウンドなし',
    '{map} · {killer}: Ø {kills} Kills ({n} Runden)':
        '{map} · {killer}：平均 {kills} キル（{n} ラウンド）',
    '{n} Matches':
        '{n} マッチ',
    '{time} gespielt':
        '{time} プレイ',
    'Ø Bloodpoints':
        '平均ブラッドポイント',
    'Ø Rundendauer':
        '平均ラウンド時間',
    'Anzeigen':
        '表示',
    'Kartenbild nicht lesbar: {error}':
        'マップ画像を読み取れません：{error}',
    'Keine Map gewählt':
        'マップが選択されていません',
    'Blendet die gewählte Map jetzt als Overlay ein – die Erkennung übernimmt beim nächsten Match wieder.':
        '選択したマップを今すぐオーバーレイに表示します – 次のマッチで再び検出が引き継ぎます。',
    'Ziehen, um den Kasten zu verschieben':
        'ドラッグしてこのボックスを移動',
    'Anordnung zurücksetzen':
        '配置をリセット',
    'Die Kästen der Seiten lassen sich am Griff rechts im Titel verschieben.':
        '各ページのボックスは、タイトルの右にあるハンドルで移動できます。',
    'Stellt die Kästen auf allen Seiten, die Reiter-Reihen (Statistik, Overlay) und die Navigation links wieder in die ursprüngliche Reihenfolge.':
        'すべてのページのボックス、タブ列（統計、オーバーレイ）、左のナビゲーションを元の順序に戻します。',
    'Das Programm liest beim Match-Start den Map-Namen aus dem Bild. Hake die Sprache an, in der du Dead by Daylight spielst (mehrere gehen).':
        'マッチ開始時に、プログラムが画像からマップ名を読み取ります。Dead by Daylight をプレイしている言語にチェックを入れてください（複数可）。',
    'Die Karte erscheint beim Match-Start von selbst und verschwindet nach der Runde. „automatisch“ legt sie in den schwarzen Rand neben dem Spielbild (Ultrawide) bzw. neben das DBD-Fenster.':
        'マップはマッチ開始時に自動で表示され、ラウンド後に消えます。「自動」では、ゲーム画面の横の黒帯（ウルトラワイド）または DBD ウィンドウの横に配置されます。',
    'Die wichtigsten Tasten – zum Ändern draufklicken und die neue Kombination drücken. Alle Tasten findest du später unter Einstellungen.':
        '最も重要なキー – クリックして変更し、新しい組み合わせを押してください。すべてのキーは後で「設定」から変更できます。',
    'Einrichtung starten':
        'セットアップを開始',
    'Öffnet noch einmal die Einrichtung vom ersten Start: Spielsprache, Overlay-Position und die wichtigsten Tasten.':
        '初回起動時のセットアップを再度開きます：ゲーム言語、オーバーレイの位置、最も重要なキー。',
    'Suchen (Strg+F)':
        '検索（Ctrl+F）',
    'Strg+F':
        'Ctrl+F',
    'Suchen: Einstellung, Seite, Map, Aktion, Runde …':
        '検索：設定、ページ、マップ、操作、ラウンド…',
    'Pfeiltasten wählen · Enter öffnen · Strg+Enter im Spiel bzw. die Aufnahme · Esc schliesst':
        '矢印キーで選択 · Enter で開く · Ctrl+Enter でゲームまたは録画内で · Esc で閉じる',
    'Aktionen':
        '操作',
    'Seiten':
        'ページ',
    'Vorschlag von Claude':
        'Claude の提案',
    'Enter':
        'Enter',
    'Strg+Enter':
        'Ctrl+Enter',
    'Claude fragen: „{q}“':
        'Claude に質問：「{q}」',
    'Schickt nur die Frage und die Namen der Einstellungen an Claude':
        '質問と設定の名前のみを Claude に送信します',
    'Claude denkt nach …':
        'Claude が考えています…',
    'Claude hat nichts Passendes gefunden.':
        'Claude は該当するものを見つけられませんでした。',
    'Claude hat die Frage abgelehnt.':
        'Claude は質問を拒否しました。',
    'Claude hat unverständlich geantwortet.':
        'Claude の回答を読み取れませんでした。',
    'Claude ist nicht erreichbar – keine Internetverbindung?':
        'Claude に接続できません – インターネット接続はありますか？',
    'Claude: Zu viele Anfragen – gleich noch einmal versuchen.':
        'Claude：リクエストが多すぎます – しばらくしてからもう一度お試しください。',
    'Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen.':
        'API キーがありません – 「設定」→「接続」→「Claude」で入力してください。',
    'Zeigt im grossen Clip-Editor den Abschnitt „Mit Claude bearbeiten“: Du schreibst, was mit dem Schnitt passieren soll, Claude schlägt Schritte vor, du übernimmst oder verwirfst sie. Gesendet werden nur deine Bitte und der Schnitt als Zahlen – kein Bild, kein Dateiname. Braucht einen eigenen API-Key.':
        '大きなクリップエディターに「Claude で編集」セクションを表示します：カットに対して行いたいことを書くと、Claude が手順を提案し、適用するか破棄するかを選べます。送信されるのは要望と、数値で表したカットのみ – 画像もファイル名も送信しません。ご自身の API キーが必要です。',
    'Claude':
        'Claude',
    'Im Clip-Editor Claude nutzen':
        'クリップエディターで Claude を使用する',
    'Mit Claude bearbeiten':
        'Claude で編集',
    'z. B. erste 10 s weg, ab 0:40 doppelt so schnell, als Short':
        '例：最初の 10 秒を削除、0:40 から 2 倍速、ショートとして',
    'Vorschlagen':
        '提案',
    'Schickt deine Bitte und den Schnitt als Zahlen (Zeiten, Tempo, Blenden – kein Bild, kein Dateiname) an Claude; nichts wird geändert, bevor du übernimmst.':
        '要望と、数値で表したカット（時間、速度、フェード – 画像もファイル名もなし）を Claude に送信します。適用するまで何も変わりません。',
    'Übernehmen':
        '適用',
    'Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen (Strg+Z).':
        '提案された手順を実行します – 1 ステップで元に戻せます（Ctrl+Z）。',
    'Verwerfen':
        '破棄',
    'Vergisst den Vorschlag; der Schnitt bleibt, wie er ist.':
        '提案を破棄します。カットはそのままです。',
    'Aus – in Einstellungen → Verbindungen → Claude „Im Clip-Editor Claude nutzen“ einschalten und einen API-Key eintragen.':
        'オフ – 「設定」→「接続」→「Claude」で「クリップエディターで Claude を使用する」をオンにし、API キーを入力してください。',
    'Der Schnitt hat sich inzwischen geändert – bitte neu vorschlagen.':
        'その間にカットが変更されました – もう一度提案させてください。',
    'Claude hat keinen passenden Schritt gefunden.':
        'Claude は該当する手順を見つけられませんでした。',
    'Übernommen – Strg+Z macht es rückgängig.':
        '適用しました – Ctrl+Z で元に戻せます。',
    'übersprungen: {why}':
        'スキップ：{why}',
    'unbekannte Aktion':
        '不明な操作',
    'Zeiten fehlen':
        '時間がありません',
    'Bereich zu kurz oder ausserhalb':
        '範囲が短すぎるか範囲外です',
    'Tempo nicht erlaubt':
        'この速度は使用できません',
    '{a}–{b} mit Tempo {f}×':
        '{a}–{b} を {f}× の速度で',
    'würde alles entfernen':
        'すべてが削除されてしまいます',
    '{a}–{b} herausgeschnitten':
        '{a}–{b} をカット',
    'nur {a}–{b} behalten':
        '{a}–{b} のみ残す',
    'Stelle ausserhalb':
        '範囲外の時点',
    'Schnitt bei {a}':
        '{a} で分割',
    'keine Änderung':
        '変更なし',
    'Blende ungültig':
        'このフェードは使用できません',
    'Standbild: Dauer ungültig':
        '静止画：この長さは使用できません',
    'Untertitel zu kurz':
        '字幕が短すぎます',
    '{n} weitere Schritte nicht ausgeführt (höchstens {max})':
        'さらに {n} 個の手順は実行されませんでした（最大 {max}）',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden, dann übernehmen.':
        '現在はできません – 先に現在の編集を終えてから適用してください。',
    'Standbild bei {a} für {s} s':
        '{a} で {s} 秒の静止画',
    'Blende ohne Dauer':
        '長さのないフェード',
    'Blenden: ein {i} s, aus {o} s':
        'フェード：イン {i} 秒、アウト {o} 秒',
    'Export-Art unbekannt':
        '不明なエクスポート形式',
    'Export-Art: {m}':
        'エクスポート形式：{m}',
    'nur bei Export-Art Short':
        'エクスポート形式「ショート」でのみ',
    'Text fehlt':
        'テキストがありません',
    'Short-Titel „{t}“':
        'ショートのタイトル「{t}」',
    'Untertitel: Zeiten fehlen':
        '字幕：時間がありません',
    'zu viele Untertitel':
        '字幕が多すぎます',
    'Untertitel {a}–{b}':
        '字幕 {a}–{b}',
    'Claude: Der API-Key wird nicht angenommen – unter Einstellungen → Verbindungen prüfen („API-Key holen“ öffnet die Anthropic Console).':
        'Claude：API キーが受け付けられません – 「設定」→「接続」で確認してください（「API キーを取得」で Anthropic Console が開きます）。',
    'Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen → Verbindungen → „Guthaben aufladen“.':
        'Claude：API アカウントにクレジットが残っていません – 「設定」→「接続」→「クレジットを追加」。',
    'API-Key holen':
        'API キーを取得',
    'Guthaben aufladen':
        'クレジットを追加',
    'Öffnet die Seite „API keys“ der Anthropic Console im Browser (platform.claude.com). Dort einen Key anlegen und hier einfügen – er beginnt mit sk-ant-.':
        'ブラウザーで Anthropic Console の「API keys」ページを開きます（platform.claude.com）。そこでキーを作成し、ここに貼り付けてください – キーは sk-ant- で始まります。',
    'Öffnet die Seite „Billing“ der Anthropic Console im Browser. Die API wird getrennt von einem Claude-Abo im Voraus bezahlt; dort lässt sich auch ein monatliches Ausgabenlimit setzen.':
        'ブラウザーで Anthropic Console の「Billing」ページを開きます。API は Claude のサブスクリプションとは別に前払いで支払います。そこで月ごとの利用上限も設定できます。',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude fragen“. Erst wenn du sie wählst, gehen deine Frage und die Namen der Einstellungen, Seiten und Aktionen an Claude (api.anthropic.com) – nie Runden, Maps oder Spieldaten. Braucht einen eigenen API-Key.':
        '検索（Ctrl+F）に「Claude に質問」の行を表示します。その行を選んだときにのみ、質問と、設定・ページ・操作の名前が Claude（api.anthropic.com）に送信されます – ラウンド、マップ、ゲームデータは決して送信しません。ご自身の API キーが必要です。',
    'Schickt eine kleine Probefrage an Claude und sagt, ob der API-Key angenommen wird (kostet einen kleinen Betrag deines API-Guthabens).':
        'Claude に小さなテスト質問を送信し、API キーが受け付けられるかどうかを表示します（API クレジットを少額消費します）。',
    'Entfernt den API-Key von diesem PC; die Suche fragt Claude dann nicht mehr.':
        'この PC から API キーを削除します。以後、検索は Claude に質問しなくなります。',
    'In der Suche Claude fragen können':
        '検索で Claude に質問できるようにする',
    'API-Key':
        'API キー',
    'Key prüfen':
        'キーを確認',
    'Key löschen':
        'キーを削除',
    'Claude: Key funktioniert.':
        'Claude：キーは有効です。',
    'Claude: prüfe den Key …':
        'Claude：キーを確認中…',
    'Claude: kein API-Key eingetragen.':
        'Claude：API キーが入力されていません。',
    'Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-).':
        'Claude：API キーのようには見えません（sk-ant- で始まります）。',
    'Claude: Key eingetragen.':
        'Claude：キーを入力しました。',
    'Schritt {n} von {total}':
        'ステップ {n} / {total}',
    'Sprache':
        '言語',
    'Sprache dieses Programms:':
        'このプログラムの言語：',
    'Weiter':
        '次へ',
    'Zurück':
        '戻る',
    'Überspringen':
        'スキップ',
    'Einrichtung: {step}':
        'セットアップ：{step}',
    'Aufgeteilt':
        '内訳',
    'CPU-Temperatur':
        'CPU 温度',
    'GPU gedrosselt':
        'GPU スロットリング',
    'GPU-Leistung':
        'GPU 電力',
    'GPU-Speicher':
        'GPU メモリ',
    'GPU-Temperatur':
        'GPU 温度',
    'Hotspot':
        'ホットスポット',
    'Höchstwert':
        '最高',
    'Höchstwerte':
        '最高値',
    'RAM':
        'RAM',
    'Runden, zusammen {time}':
        'ラウンド、合計 {time}',
    'VRAM':
        'VRAM',
    'Wert':
        '値',
    '{n} von {total}':
        '{n} / {total}',
    'Ø CPU-Temperatur':
        '平均 CPU 温度',
    'Ø GPU-Last':
        '平均 GPU 負荷',
    'Ø GPU-Leistung':
        '平均 GPU 電力',
    'Ø GPU-Temperatur':
        '平均 GPU 温度',
    'über {n} Runden':
        '{n} ラウンドで',
    'Bilanz: Ø 2,8 Kills · 12 Runden':
        '記録：平均 2.8 キル · 12 ラウンド',
    'Infos und Schrift (Name, Timer, Bilanz, Server)':
        '情報とテキスト（名前、タイマー、記録、サーバー）',
    'Eigenes Element unter der Karte':
        'マップの下の独立した要素',
    'Eigenes Element über der Karte':
        'マップの上の独立した要素',
    'Eigenes Element, eigene Position':
        '独立した要素、独自の位置',
    'Mit der Karte verbunden, unten':
        'マップに連結、下',
    'Mit der Karte verbunden, oben':
        'マップに連結、上',
    'Infos':
        '情報',
    'INFOS':
        '情報',
    'Infos (Timer, Bilanz, Server)':
        '情報（タイマー、記録、サーバー）',
    'In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine Sofort-Clips (F8) und keinen Vorlauf.':
        'OBS のリプレイバッファが有効になっていません – OBS：「設定」→「出力」→「リプレイバッファ」→「リプレイバッファを有効にする」にして適用してください。これがないとインスタントクリップ（F8）もプリロールもありません。',
    'Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)':
        'OBS でリプレイバッファが有効になっていません（「設定」→「出力」→「リプレイバッファ」）',
    'Karten im selben Balken gleich breit':
        '同じ帯のカードを同じ幅にする',
    'Zu einer Spalte zusammenführen':
        '1 列にまとめる',
    'Die Karten, die im selben schwarzen Balken stehen, werden so breit gezeichnet wie die breiteste von ihnen – untereinander ergeben sie eine Spalte mit bündigen Rändern.':
        '同じ黒帯にあるカードを、その中で最も幅の広いカードと同じ幅で描画します – 上下に並べると端の揃った 1 列になります。',
    'Heute unter die Systemwerte, die Musik unter Heute, alle gleich breit – eine Spalte im Balken der Systemwerte. Rückgängig mit Strg+Z.':
        'システム値の下に今日、今日の下に音楽を、すべて同じ幅で配置します – システム値の帯に 1 列。Ctrl+Z で元に戻せます。',
    'Cover':
        'カバー',
    'Discord-Overlay freihalten':
        'Discord のオーバーレイの場所を空けておく',
    'Karte, Infos, Systemwerte, Heute und Musik weichen den Stellen aus, an denen Discords Overlay seine Widgets zeigt (in der Vorschau schraffiert). Das Programm liest nichts aus Discord – die Flächen sind fest.':
        'マップ、情報、システム値、今日、音楽が、Discord のオーバーレイがウィジェットを表示する場所（プレビューでは斜線）を避けます。プログラムは Discord から何も読み取りません – 領域は固定です。',
    'Wie der Stil':
        'スタイルに合わせる',
    'Rund':
        '丸',
    'Eckig':
        '四角',
    '{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr (der schwarze Balken ist voll).':
        '{what} はここではこれ以上大きくなりません – スライダーの {cap} % 以上では何も変わりません（黒帯がいっぱいです）。',
    'Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).':
        '「マップを帯より大きくできる」でさらに大きくなります（その場合ゲーム画面にはみ出します）。',
    'Spielbild':
        'ゲーム画面',
    'Map-Name':
        'マップ名',
    'Farbthema':
        'カラーテーマ',
    'Gold (Standard)':
        'ゴールド（既定）',
    'Blutrot':
        'ブラッドレッド',
    'Eisblau':
        'アイスブルー',
    'Giftgrün':
        'トキシックグリーン',
    'Lila':
        'パープル',
    '„Heute“: Runden, Spielzeit, Ø Kills/Entkommen, Uhrzeit':
        '「今日」：ラウンド数、プレイ時間、平均キル数/脱出数、時計',
    'Eine eigene Karte, solange eine Map im Match zu sehen ist: wie viele Runden du heute gespielt hast, wie lange, Ø Kills bzw. Entkommen laut Stats-Seite und die Uhrzeit. Position darunter, Grösse über den Grössenregler („Heute“ wählen).':
        'マッチ中にマップが表示されている間の独立したカード：今日プレイしたラウンド数とプレイ時間、統計ページの平均キル数または脱出数、時刻。位置は下で、サイズはサイズスライダーで（「今日」を選択）。',
    'Dunkle Fläche hinter „Heute“':
        '「今日」の背後に暗い領域',
    'Vorlage':
        'プリセット',
    'Vorlage anwenden':
        'プリセットを適用',
    'Alles links':
        'すべて左',
    'Alles rechts':
        'すべて右',
    'Verteilt: Karte links, Werte rechts':
        '分散：マップは左、値は右',
    'Vorlage „{name}“ angewendet.':
        'プリセット「{name}」を適用しました。',
    'Setzt Karte, Systemwerte, „Heute“ und Musik auf einmal auf die gewählte Anordnung. „Rückgängig“ holt die vorherige zurück.':
        'マップ、システム値、「今日」、音楽を選んだ配置に一度に並べます。「元に戻す」で以前の配置に戻ります。',
    'Weich ein- und ausblenden':
        '滑らかにフェードイン/アウトする',
    'In kleinen DBD-Fenstern ausblenden':
        '小さな DBD ウィンドウでは隠す',
    'Läuft DBD in einem kleinen Fenster (Bild kleiner als 1920×1080 oder schmaler als 16:9), zeigt das Programm im Spiel nichts – wie der Hauptschalter. Map-Erkennung, Statistik und OBS-Aufnahmen laufen weiter. Wird das Fenster wieder gross, erscheint das Overlay von selbst.':
        'DBD が小さなウィンドウで実行されている場合（画面が 1920×1080 未満または 16:9 より狭い）、プログラムはゲーム内に何も表示しません – マスタースイッチと同様です。マップ検出、統計、OBS 録画は継続します。ウィンドウが再び大きくなると、オーバーレイは自動で戻ります。',
    'Kleines DBD-Fenster ({w}×{h}) – Overlay ausgeblendet, Runden werden weiter gezählt und aufgenommen.':
        '小さな DBD ウィンドウ（{w}×{h}）– オーバーレイを非表示。ラウンドは引き続き数えられ、録画されます。',
    'Update gesperrt: eine Runde läuft. Nach dem Rundenende noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'アップデートはロック中です：ラウンドが進行中です。ラウンド終了後にもう一度「アップデートして再起動」をクリックしてください。',
    'Alle Farming-Runden der Auswahl (Zeitraum, Region, Map, Modus) – unabhängig vom Rollen-Filter und von „Farming ausblenden“. Farming = Crossplay war in der Lobby aus (oder die eingestellte Farming-Region); korrigieren unter „Letzte Runden“ mit „Farming an/aus“. Aufnahmen liegen im Unterordner „Farming“ des Aufnahmeordners. Wartezeit „sofort“: die Lobby war voll, bevor eine Suchzeit messbar war. Server nur, wenn „Verbunden mit“ auf der Seite Server läuft.':
        '選択範囲（期間、リージョン、マップ、モード）のすべてのファーミングラウンド – 役割フィルターや「ファーミングを除外」の設定にかかわらず。ファーミング = ロビーでクロスプレイがオフだった（または設定したファーミングリージョン）。「最近のラウンド」の「ファーミング オン/オフ」で修正できます。録画は録画フォルダーの「Farming」サブフォルダーにあります。待ち時間「即時」：検索時間を測る前にロビーが満員になりました。サーバーは「サーバー」ページで「接続先」が動作している間のみ。',
    'Keine Farming-Runden in dieser Auswahl.':
        'この選択範囲にはファーミングラウンドがありません。',
    '{n} als Killer · {m} als Survivor':
        'キラーで {n} 回 · サバイバーで {m} 回',
    'Spielzeit':
        'プレイ時間',
    'vom Map-Banner bis zum Rundenende':
        'マップバナーからラウンド終了まで',
    'BP':
        'BP',
    '{n} gespeicherte Matches haben ein Loadout, aber keines davon ist in dieser Auswahl. Custom Games zählen nur mit dem Rollen-Filter „Custom Games“, Farming-Runden nicht mit „Farming ausblenden“, Matches ohne erkannte Runde gar nicht.':
        '保存された {n} 件のマッチにロードアウトがありますが、この選択範囲には含まれていません。カスタムマッチは役割フィルター「カスタムマッチ」でのみ、ファーミングラウンドは「ファーミングを除外」がオンだと数えられず、検出されたラウンドのないマッチは一切数えられません。',
    'DBD-Fenster wieder gross genug – Overlay wieder an.':
        'DBD ウィンドウが再び十分な大きさになりました – オーバーレイを再表示しました。',
    'Overlay anzeigen':
        'オーバーレイを表示する',
    'Hauptschalter: aus = das Programm zeigt im Spiel nichts (Karte, Systemwerte, Heute, Musik). Erkennung, Statistik und Aufnahmen laufen weiter. Auch als Knopf in der Übersicht.':
        'マスタースイッチ：オフ = プログラムはゲーム内に何も表示しません（マップ、システム値、今日、音楽）。検出、統計、録画は継続します。概要ページにもボタンがあります。',
    'Overlay eingeschaltet.':
        'オーバーレイをオンにしました。',
    'Overlay ausgeschaltet – die Erkennung läuft weiter.':
        'オーバーレイをオフにしました – 検出は継続します。',
    'Overlay ausschalten':
        'オーバーレイをオフ',
    'Overlay einschalten':
        'オーバーレイをオン',
    'Blendet alles aus, was das Programm im Spiel zeigt – Karte, Systemwerte, Heute, Musik. Die Erkennung, Statistik und Aufnahmen laufen weiter.':
        'プログラムがゲーム内に表示するものすべて（マップ、システム値、今日、音楽）を隠します。検出、統計、録画は継続します。',
    'Zeigt das Overlay im Spiel wieder an.':
        'ゲーム内にオーバーレイを再表示します。',
    'Karte, Systemwerte und „Heute“ blenden in einer Drittelsekunde ein und aus, statt hart zu erscheinen. Die Musik hat ihr eigenes Häkchen.':
        'マップ、システム値、「今日」が、突然現れる代わりに 1/3 秒でフェードイン/アウトします。音楽には専用のチェックボックスがあります。',
    'Unter „Heute“':
        '「今日」の下',
    'Unter der Musik':
        '音楽の下',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter „Heute“.':
        '「今日」の背後に角の丸い半透明の暗い領域を表示します。',
    'HEUTE':
        '今日',
    'ENTKOMMEN ':
        '脱出 ',
    'HEUTE ':
        '今日 ',
    'UHR ':
        '時間 ',
    '{n} RUNDEN · {time}':
        '{n} ラウンド · {time}',
    'Ø KILLS ':
        '平均キル ',
    'NORMAL ':
        '通常 ',
    'FARMING ':
        'ファーミング ',
    'BP/H ':
        'BP/時 ',
    'OLED-Schwarz':
        'OLED ブラック',
    'Hintergründe in echtem Schwarz statt Dunkelgrau – passt zu OLED-Bildschirmen und geht mit jeder Akzentfarbe. Im hellen Modus ohne Wirkung.':
        '背景をダークグレーではなく純粋な黒にします – OLED 画面に適しており、どのアクセントカラーにも合います。ライトモードでは効果がありません。',
    'Eigene Farbe':
        '独自の色',
    'Eigene Farbe …':
        '独自の色…',
    'Beliebige Farbe wählen – das Programm passt die Helligkeit an, bis alles lesbar ist.':
        '好きな色を選んでください – すべてが読みやすくなるまで、プログラムが明るさを調整します。',
    '„Läuft gerade“: Titel, Interpret und Cover':
        '「再生中」：タイトル、アーティスト、カバー',
    'Liest Titel und Interpret aus der Windows-Mediensteuerung (dieselbe Liste wie beim Lautstärkeregler von Windows) – nur Anzeige, das Programm steuert nichts und speichert nichts.':
        'Windows のメディアコントロール（Windows の音量フライアウトと同じリスト）からタイトルとアーティストを読み取ります – 表示のみで、プログラムは何も操作せず、何も保存しません。',
    'Unter den Systemwerten':
        'システム値の下',
    'Rechts unten im Balken':
        '帯の右下',
    'Links unten im Balken':
        '帯の左下',
    'MUSIK':
        '音楽',
    'läuft gerade':
        '再生中',
    'Albumcover zeigen':
        'アルバムカバーを表示する',
    'Auch Videos zeigen (YouTube, Twitch …) – aus: nur Musik':
        '動画も表示する（YouTube、Twitch…）– オフ：音楽のみ',
    'Die Mediensteuerung meldet auch Videos aus dem Browser. An: ein Video erscheint als „▶ Titel“ mit dem Kanal darunter. Aus: die Karte zeigt nur Musik. Unterschieden wird am Album: Musikdienste melden eins, ein Video nicht.':
        'メディアコントロールはブラウザーの動画も報告します。オン：動画は「▶ タイトル」として、その下にチャンネル名とともに表示されます。オフ：カードには音楽のみ表示されます。区別はアルバムで行います：音楽サービスはアルバムを報告し、動画は報告しません。',
    'Balken in der Farbe des Covers':
        'バーをカバーの色にする',
    'Dunkle Fläche hinter Karte und Infos':
        'マップとその行の背後に暗い領域',
    'Dunkle Fläche hinter den Systemwerten':
        'システム値の背後に暗い領域',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Karte, Timer und Infozeilen (auch hinter „Warte auf Map“) – gut lesbar über hellen Stellen im Spiel.':
        'マップ、タイマー、情報行の背後（「マップを待機中」の背後にも）に角の丸い半透明の暗い領域を表示します – ゲームの明るい部分の上でも読みやすくなります。',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Systemwerten und „Heute“.':
        'システム値と「今日」の背後に角の丸い半透明の暗い領域を表示します。',
    'Restzeit statt Länge (−1:46)':
        '長さの代わりに残り時間（−1:46）',
    'Dunkle Fläche hinter der Musikkarte':
        '音楽カードの背後に暗い領域',
    'Weich ein- und ausblenden (auch beim nächsten Lied)':
        '滑らかにフェードイン/アウトする（次の曲でも）',
    'Der Fortschrittsbalken nimmt die Hauptfarbe des Albumcovers an, wie bei Spotify. Graue Cover: weiss.':
        'プログレスバーが Spotify のようにアルバムカバーのメインカラーになります。灰色のカバー：白。',
    'Rechts neben dem Balken steht, wie lange das Lied noch läuft, statt seiner Gesamtlänge.':
        'バーの右：曲の全体の長さの代わりに残り時間を表示します。',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter Cover und Text – gut lesbar, wenn die Karte über hellen Stellen im Spiel liegt.':
        'カバーとテキストの背後に角の丸い半透明の暗い領域を表示します – カードがゲームの明るい部分に重なっても読みやすくなります。',
    'Die Musikkarte blendet in einer Drittelsekunde ein und aus, statt hart zu erscheinen – auch wenn ein neues Lied beginnt.':
        '音楽カードが突然現れる代わりに 1/3 秒でフェードイン/アウトします – 新しい曲が始まったときも。',
    'Das Bild zum Lied links neben Titel und Interpret – Windows liefert es mit; es bleibt nur im Speicher.':
        'タイトルとアーティストの左に曲の画像を表示します – Windows が提供し、メモリ内にのみ保持されます。',
    'Gross – Cover oben, Titel darunter':
        '大 – カバーが上、タイトルが下',
    'Kompakt – Cover links':
        'コンパクト – カバーが左',
    'Fortschritt des Lieds zeigen':
        '曲の進行状況を表示する',
    'Unter Titel und Künstler: wie weit das Lied ist, mit Balken und Länge – wie in Spotify.':
        'タイトルとアーティストの下に：曲がどこまで進んだかを、バーと長さで表示します – Spotify と同様です。',
    'KARTE · Strg+Mausrad = Grösse':
        'マップ · Ctrl+ホイール = サイズ',
    'Ziehst: {name}':
        'ドラッグ中：{name}',
    'Unter der Maus: {name}':
        'マウスの下：{name}',
    'Kartenstil':
        'マップスタイル',
    'Kartenstil: {style}.':
        'マップスタイル：{style}。',
    'Map wählen …':
        'マップを選択…',
    'Zur Seite Maps: eine Map von Hand anzeigen (Doppelklick oder „Anzeigen“). Beim nächsten Match übernimmt die automatische Erkennung wieder.':
        '「マップ」ページへ：マップを手動で表示します（ダブルクリックまたは「表示」）。次のマッチで再び自動検出が引き継ぎます。',
    'Erscheint automatisch, sobald im Match das Map-Banner kommt – oder von Hand über „Map wählen“.':
        'マッチでマップバナーが表示されるとすぐに自動で表示されます – または「マップを選択」で手動で。',
    'Wann zeigen':
        '表示するタイミング',
    'Alle Maps':
        'すべてのマップ',
    'Zuletzt gespielt':
        '最近プレイ',
    'Suchen: Name, Realm, Abkürzung …':
        '検索：名前、レルム、略称…',
    'Klick oder Enter = groß ansehen · Doppelklick oder Strg+Enter = jetzt anzeigen. Die Erkennung übernimmt beim nächsten Match wieder.':
        'クリックまたは Enter = 大きく表示 · ダブルクリックまたは Ctrl+Enter = 今すぐ表示。次のマッチで再び検出が引き継ぎます。',
    'Zurück zu den Karten des Realms (Esc).':
        'レルムのマップに戻る（Esc）。',
    'Allgemein':
        '一般',
    'Alle Einstellungen zurücksetzen':
        'すべての設定をリセット',
    'Alle Einstellungen auf die Auslieferung zurücksetzen? Runden, Match-Daten und eigene Bilder bleiben. Das Programm startet danach neu.':
        'すべての設定を初期状態に戻しますか？ラウンド、マッチデータ、独自の画像は残ります。その後プログラムが再起動します。',
    'Alle Einstellungen zurückgesetzt.':
        'すべての設定をリセットしました。',
    'Standard wiederherstellen':
        '既定値に戻す',
    'Ausschalten':
        'オフにする',
    '{free} von {total} Regionen freigegeben':
        '{total} 個中 {free} 個のリージョンを許可',
    'DBD läuft gerade – die Änderung gilt erst nach einem Neustart von DBD.':
        'DBD は起動中です – 変更は DBD の再起動後に反映されます。',
    'Suchen …':
        '検索…',
    'Setzt jede Einstellung auf die Auslieferung zurück (Overlay, Hotkeys, Erkennung, Server-Auswahl im Programm …). Runden, Match-Daten und eigene Bilder bleiben; das Programm startet danach neu. Vorher sichern: „Einstellungen exportieren“.':
        'すべての設定を初期状態に戻します（オーバーレイ、ホットキー、検出、プログラム内のリージョン選択…）。ラウンド、マッチデータ、独自の画像は残ります。その後プログラムが再起動します。先にバックアップを：「設定をエクスポート」。',
    'Grösse {pct} %':
        'サイズ {pct} %',
    'Eigene Einstellungen dieser Map: {what}':
        'このマップの独自の設定：{what}',
    'Eigene Grösse und Drehung zurücksetzen':
        '個別サイズと回転をリセット',
    'Kartenbild ersetzen …':
        'マップ画像を置き換え…',
    'Im schwarzen Rand, solange die Karte im Match zu sehen ist. GPU-Werte von NVIDIA (Treiber), CPU-Temperatur nur mit HWiNFO („Shared Memory Support“ an) – kein eigener Treiber.':
        'マッチ中にマップが表示されている間、黒帯に表示されます。GPU の値は NVIDIA（ドライバー）から、CPU 温度は HWiNFO 使用時のみ（「Shared Memory Support」をオン）– 独自のドライバーは使用しません。',
    'Standard (wie ausgeliefert)':
        '標準（初期状態）',
    'Fenster {size}':
        'ウィンドウ {size}',
    'alle Fenstergrössen':
        'すべてのウィンドウサイズ',
    'Gilt für: {window}':
        '適用先：{window}',
    'Gilt für: {maps} · {window}':
        '適用先：{maps} · {window}',
    'nur {map}':
        '{map} のみ',
    'alle Maps (keine Map eingeblendet)':
        'すべてのマップ（マップ非表示時）',
    'Letzte 7 Tage':
        '過去 7 日間',
    'Letzte 30 Tage':
        '過去 30 日間',
    'Rolle/Killer':
        '役割/キラー',
    'Weitere 100 Runden anzeigen':
        'さらに 100 ラウンド表示',
    'Runden exportieren':
        'ラウンドをエクスポート',
    '{n} Runden exportiert: {path}':
        '{n} ラウンドをエクスポートしました：{path}',
    'Median':
        '中央値',
    '{n} Runden':
        '{n} ラウンド',
    'Längste':
        '最長',
    'Die Liste zeigt die neuesten 100 Runden der Auswahl; jeder Klick hängt 100 ältere an.':
        'リストには選択範囲の最新 100 ラウンドが表示されます。クリックするたびに、さらに古い 100 ラウンドが追加されます。',
    'Server-Tab öffnen':
        'サーバータブを開く',
    'Match-Daten einrichten …':
        'マッチデータを設定…',
    'Einrichten …':
        '設定…',
    'Noch keine Runden heute':
        '今日のラウンドはまだありません',
    'Stats-Seite':
        '統計ページ',
    'nicht eingerichtet':
        '未設定',
    'Match-Daten':
        'マッチデータ',
    'Kills, Entkommen und Bloodpoints deiner Runden kommen von stats.deadbydaylight.com – geladen von deinem Browser, nicht vom Programm. Lässt sich auch später einrichten (Einstellungen → Match-Daten → Offizielle Match-Daten).':
        'ラウンドのキル、脱出、ブラッドポイントは stats.deadbydaylight.com から取得します – 読み込むのはプログラムではなく、お使いのブラウザーです。後からでも設定できます（「設定」→「マッチデータ」→「公式マッチデータ」）。',
    'Zur Seite Server: dort „Spielserver anzeigen“ anhaken – Region und Ping stehen dann hier und im Overlay.':
        '「サーバー」ページへ：そこで「ゲームサーバーを表示」にチェックを入れると、リージョンと Ping がここやオーバーレイに表示されます。',
    'Zu Einstellungen → Match-Daten → Offizielle Match-Daten: einmal das Userscript in den Browser, danach zählen Kills, Entkommen und Bloodpoints in der Statistik.':
        '「設定」→「マッチデータ」→「公式マッチデータ」へ：ユーザースクリプトを一度ブラウザーに入れると、キル、脱出、ブラッドポイントが統計に反映されます。',
    'CPU DROSSELT (TEMP.)':
        'CPU THROTTLED（温度）',
    'CPU gedr.':
        'CPU 制限',
    'GPU gedr.':
        'GPU 制限',
    'CPU gedrosselt':
        'CPU スロットリング',
    'CPU Ø W':
        'CPU 平均 W',
    'CPU-Leistung':
        'CPU 電力',
    'Kern Ø %':
        'コア平均 %',
    'Ø CPU-Leistung':
        '平均 CPU 電力',
    'Ø stärkster CPU-Kern':
        '最も負荷の高い CPU コアの平均',
    'Niedrigstes FPS-Tief':
        '最低の FPS low',
    'Ø FPS':
        '平均 FPS',
    'Ø FPS-Tief':
        '平均 FPS low',
    'FPS Ø':
        'FPS 平均',
    'FPS Tief':
        'FPS low',
    'Klick: sortieren · Rechtsklick: Spalten ein-/ausblenden':
        'クリック：並べ替え · 右クリック：列の表示/非表示',
    'Alle Spalten zeigen':
        'すべての列を表示',
    'Exportieren …':
        'エクスポート…',
    'Zeitraum':
        '期間',
    'Von':
        '開始',
    'Bis':
        '終了',
    'TT.MM.JJJJ HH:MM – auch nur ein Datum (ganzer Tag) oder nur eine Uhrzeit (heute); leer = offen.':
        'DD.MM.YYYY HH:MM – 日付のみ（その日全体）または時刻のみ（今日）も可。空欄 = 制限なし。',
    'Gestern':
        '昨日',
    'Alles':
        'すべて',
    'Eigener Zeitraum':
        'カスタム期間',
    'Filter':
        'フィルター',
    'Custom Games einschliessen':
        'カスタムマッチを含める',
    'Farming-Runden einschliessen':
        'ファーミングラウンドを含める',
    'Spalten':
        '列',
    'Start':
        '開始',
    'Realm':
        'レルム',
    'Ping (ms)':
        'Ping（ms）',
    'Kills':
        'キル',
    'Normal':
        '通常',
    'ja':
        'はい',
    'nein':
        'いいえ',
    'CSV-Datei (Excel)':
        'CSV ファイル（Excel）',
    'Textliste (eine Zeile je Runde)':
        'テキストリスト（1 ラウンド 1 行）',
    '{n} Runden, {m} Spalten':
        '{n} ラウンド、{m} 列',
    'Zeitangabe nicht lesbar: „{text}“ – Format TT.MM.JJJJ HH:MM.':
        '時刻「{text}」を読み取れません – 形式は DD.MM.YYYY HH:MM です。',
    'Nichts zu kopieren – keine Runde passt, oder keine Spalte gewählt.':
        'コピーするものがありません – 該当するラウンドがないか、列が選択されていません。',
    'Nichts zu speichern – keine Runde passt, oder keine Spalte gewählt.':
        '保存するものがありません – 該当するラウンドがないか、列が選択されていません。',
    'In Zwischenablage kopieren':
        'クリップボードにコピー',
    'Als Datei speichern …':
        'ファイルとして保存…',
    'Schliessen':
        '閉じる',
    '{n} Runden in die Zwischenablage kopiert.':
        '{n} ラウンドをクリップボードにコピーしました。',
    'Spalte „{name}“ mit ausgeben.':
        '列「{name}」を含めます。',
    'Öffnet das Export-Fenster: Zeitraum (auch von–bis), Rolle, Killer, Map, Region, Spalten nach Wahl – als CSV für Excel oder als Textliste in die Zwischenablage. Die Filter der Statistik sind vorbelegt.':
        'エクスポートウィンドウを開きます：期間（開始～終了も可）、役割、キラー、マップ、リージョン、任意の列 – Excel 用の CSV として、またはテキストリストとしてクリップボードへ。統計のフィルターが事前に設定されます。',
    'Kopiert die Runden in der gewählten Form (CSV oder Textliste) in die Zwischenablage – zum Einfügen in Discord, Excel oder einen Editor.':
        '選択した形式（CSV またはテキストリスト）でラウンドをクリップボードにコピーします – Discord、Excel、エディターに貼り付けるために。',
    'Speichert die Runden als Datei: CSV (Semikolon, UTF-8 mit BOM – Excel öffnet sie direkt) oder Textliste (.txt).':
        'ラウンドをファイルとして保存します：CSV（セミコロン区切り、BOM 付き UTF-8 – Excel で直接開けます）またはテキストリスト（.txt）。',
    'Schliesst das Fenster.':
        'ウィンドウを閉じます。',
    'Aus: Custom Games (eigene Lobbys, Bots) bleiben draussen.':
        'オフ：カスタムマッチ（独自のロビー、ボット）は除外されます。',
    'Aus: Farming-Runden (Crossplay aus bzw. Farming-Region) bleiben draussen.':
        'オフ：ファーミングラウンド（クロスプレイオフまたはファーミングリージョン）は除外されます。',
    'Eine Zeile je Runde, Spalten durch Semikolon getrennt, mit Kopfzeile.':
        '1 ラウンド 1 行、列はセミコロン区切り、ヘッダー行付き。',
    'Eine Zeile je Runde, die gewählten Spalten mit „ · “ getrennt, ohne Kopfzeile – zum Einfügen in einen Chat.':
        '1 ラウンド 1 行、選択した列を「 · 」で区切り、ヘッダーなし – チャットに貼り付けるために。',
    'Verbindungen':
        '接続',
    'Ton':
        'サウンド',
    'Aufräumen':
        'クリーンアップ',
    'Jede Runde mit OBS aufnehmen':
        'すべてのラウンドを OBS で録画する',
    'Port':
        'ポート',
    'Passwort':
        'パスワード',
    'Verbindung testen':
        '接続をテスト',
    'Aufnahmeordner wählen …':
        '録画フォルダーを選択…',
    '(kein Ordner gewählt)':
        '（フォルダー未選択）',
    'Platz für Aufnahmen':
        '録画用の容量',
    'Ganze Platte (Älteste weg, wenn sie voll wird)':
        'ドライブ全体（いっぱいになると最も古いものから削除）',
    'Vorlauf aus dem OBS-Wiederholungspuffer sichern':
        'OBS のリプレイバッファからリードインを残す',
    'OBS nimmt auf, das Programm sagt nur wann: Start beim Map-Banner, Stopp beim erkannten Rundenende, Datei nach Datum, Map und Killer benannt. Dafür in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server einschalten und Port und Passwort unter Verbindungen → OBS-Verbindung eintragen; Verbindung nur auf diesem PC (127.0.0.1). Empfohlen: Aufnahmeformat MKV oder Hybrid-MP4 (bleibt bei Abbruch lesbar), Fenster- oder Bildschirmaufnahme statt Spielaufnahme. Der Ordner wird über sein Laufwerk gemerkt – ist die Platte nicht angeschlossen, wird nicht aufgenommen.':
        '録画は OBS が行い、プログラムはタイミングを伝えるだけです：マップバナーで開始、検出したラウンド終了で停止、ファイル名は日付、マップ、キラーから付けます。OBS の「ツール」→「WebSocket サーバー設定」でサーバーを有効にし、「接続」→「OBS 接続」でポートとパスワードを入力してください。接続はこの PC 内にとどまります（127.0.0.1）。推奨：録画フォーマットは MKV またはハイブリッド MP4（クラッシュ後も読み取り可能）、ゲームキャプチャよりもウィンドウキャプチャまたは画面キャプチャ。フォルダーはドライブ単位で記憶されます – ドライブが取り外されていると何も録画されません。',
    'Ordner für die Aufnahmen (z. B. auf der externen Platte)':
        '録画用のフォルダー（例：外付けドライブ上）',
    'Aufnahmeordner: {path}':
        '録画フォルダー：{path}',
    'Verbinde mit OBS …':
        'OBS に接続中…',
    'Aufnahme: {text}':
        '録画：{text}',
    'Aufnahme gespeichert: {file}':
        '録画を保存しました：{file}',
    'Aufnahmen gelöscht (Platz): {n}':
        '削除した録画（容量）：{n}',
    'OBS hat die Verbindung geschlossen':
        'OBS が接続を閉じました',
    'OBS antwortet nicht auf die Anfrage {kind}':
        'OBS がリクエスト {kind} に応答しません',
    'OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})':
        'OBS に接続できません – OBS は WebSocket サーバーをオンにして起動していますか？（{error}）',
    'Keine Antwort von obs-websocket':
        'obs-websocket から応答がありません',
    'Kein obs-websocket auf diesem Port':
        'このポートに obs-websocket がありません',
    'Falsche WebSocket-Antwort':
        'WebSocket の応答が不正です',
    'Unerwartete Begrüssung von OBS':
        'OBS から予期しない応答がありました',
    'OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)':
        'OBS がパスワードを要求しています（OBS：「ツール」→「WebSocket サーバー設定」）',
    'OBS hat die Anmeldung abgelehnt – Passwort falsch?':
        'OBS がログインを拒否しました – パスワードが間違っていますか？',
    'OBS {version} verbunden':
        'OBS {version} に接続しました',
    'nimmt gerade auf':
        '録画中',
    'bereit':
        '準備完了',
    'Wiederholungspuffer läuft':
        'リプレイバッファ実行中',
    'Wiederholungspuffer aus (kein Vorlauf)':
        'リプレイバッファ オフ（プリロールなし）',
    'Ordner: {folder}':
        'フォルダー：{folder}',
    'Ordner/Laufwerk nicht gefunden':
        'フォルダー/ドライブが見つかりません',
    'Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen':
        '録画ドライブが接続されていません – このラウンドは録画されません',
    'Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen':
        '録画ドライブがほぼいっぱいです – このラウンドは録画されません',
    'OBS nimmt schon auf (von Hand?) – nichts gestartet':
        'OBS は既に録画中です（手動？）– 何も開始しませんでした',
    'Nimmt die Runde auf':
        'ラウンドを録画中',
    'OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet':
        'OBS がファイル名を返しませんでした – 録画は割り当てられていません',
    "Aufnahme liegt in OBS' eigenem Ordner: {path}":
        '録画は OBS 独自のフォルダーにあります：{path}',
    'Gespeichert: {file}':
        '保存しました：{file}',
    'Das Programm startet die OBS-Aufnahme beim Map-Banner und stoppt sie beim erkannten Rundenende (obs-websocket, nur auf diesem PC). OBS muss laufen.':
        'プログラムはマップバナーで OBS の録画を開始し、検出したラウンド終了で停止します（obs-websocket、この PC 内のみ）。OBS が起動している必要があります。',
    'Verbindet sich einmal mit OBS und zeigt Version, Aufnahmezustand, Wiederholungspuffer und ob der Aufnahmeordner erreichbar ist.':
        'OBS に一度接続し、バージョン、録画中かどうか、リプレイバッファ、録画フォルダーにアクセスできるかを表示します。',
    'Ordner, in den OBS die Runden legt – z. B. auf der externen Platte. Gemerkt wird das Laufwerk, nicht der Buchstabe: bekommt die Platte einen anderen, findet das Programm den Ordner trotzdem.':
        'OBS がラウンドを保存するフォルダー – 例：外付けドライブ上。記憶するのはドライブ自体で、ドライブ文字ではありません：ドライブ文字が変わっても、プログラムはフォルダーを見つけます。',
    'Läuft in OBS der Wiederholungspuffer, wird er beim Map-Banner gespeichert – der Anfang (Spawn) fehlt dann nicht, aber die Datei enthält auch Lobby und Ladebildschirm. Seit 1.5.5 standardmässig aus (Wunsch des Nutzers: nur die Runde). Die Datei liegt als „(Vorlauf)“ neben der Runde.':
        'OBS のリプレイバッファが実行中の場合、マップバナーの時点で保存されます – 開始（スポーン）が欠けることはありませんが、ファイルにはロビーとロード画面も含まれます。1.5.5 以降は既定でオフ（ユーザーの要望：ラウンドのみ）。ファイルは「(Vorlauf)」としてラウンドの隣に置かれます。',
    'Wiederholungspuffer mit DBD starten und stoppen':
        'DBD とともにリプレイバッファを開始/停止する',
    'Nur das DBD-Fenster aufnehmen':
        'DBD のウィンドウのみを録画する',
    'Dafür die OBS-Spielaufnahme verwenden':
        'その際 OBS のゲームキャプチャを使用する',
    'Statt der Fensteraufnahme legt das Programm in OBS eine Spielaufnahme „Fog Scout – DBD-Spiel“ an und blendet die Fensteraufnahme aus. Die Spielaufnahme braucht etwas weniger Leistung; OBS hängt sich dafür mit seinem Anti-Cheat-kompatiblen Hook ins Spiel – das macht OBS, nicht dieses Programm. Ihr eigener Ton bleibt aus, der Spielton kommt weiter über die Tonquelle „Fog Scout – DBD“. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“.':
        'ウィンドウキャプチャの代わりに、プログラムは OBS にゲームキャプチャ「Fog Scout – DBD-Spiel」を作成し、ウィンドウキャプチャを隠します。ゲームキャプチャのほうが負荷がわずかに少なくなります。そのため OBS はアンチチート対応のフックでゲームにフックします – これを行うのは OBS であり、このプログラムではありません。ゲームキャプチャ自体の音声はオフのままで、ゲーム音は引き続き音声ソース「Fog Scout – DBD」から入ります。「DBD のウィンドウのみを録画する」と併用した場合のみ。',
    'Bildquelle {name} über {over} gelegt':
        '映像ソース {name} を {over} の上に配置しました',
    'Bildquelle angelegt: {name} (Szene „{scene}“)':
        '映像ソースを作成しました：{name}（シーン「{scene}」）',
    'Bildquelle in der Szene „{scene}“ ausgeblendet: {name}':
        'シーン「{scene}」で映像ソースを非表示にしました：{name}',
    'Bildquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'シーン「{scene}」に映像ソースを追加しました：{name}',
    'Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'シーン「{scene}」で映像ソースを再表示しました：{name}',
    'Bildquelle {name} zeigt jetzt {exe}':
        '映像ソース {name} は {exe} を表示するようになりました',
    'DBD-Fenster in OBS nicht eingerichtet: {error}':
        'OBS で DBD のウィンドウが設定されていません：{error}',
    'OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin keine Sofort-Clips (F8) und kein Vorlauf.':
        'OBS がリプレイバッファを開始できませんでした（OBS は出力エラーを報告しています。主にエンコーダーが原因 – 詳細は OBS のログ）。プログラムは次回の DBD 起動時にのみ再試行します。それまではインスタントクリップ（F8）もプリロールもありません。',
    'Das Programm legt in OBS eine Fensteraufnahme „Fog Scout – DBD-Fenster“ an (oben in der laufenden Szene, auf die Leinwand eingepasst) und stellt sie auf Steam, Epic oder Store um. Aufgenommen wird dann nur das Spiel – ohne Discord, Benachrichtigungen und ohne das Overlay dieses Programms. OBS nimmt dabei über Windows auf; die Spielaufnahme gibt es als Häkchen darunter. Aus: die Quelle wird nur ausgeblendet, deine eigene Bildschirmaufnahme bleibt unangetastet.':
        'プログラムは OBS にウィンドウキャプチャ「Fog Scout – DBD-Fenster」を作成し（配信中のシーンの最前面、キャンバスに合わせて）、Steam、Epic、Store のいずれかに切り替えます。これでゲームのみが録画されます – Discord、通知、このプログラムのオーバーレイは含まれません。ここでは OBS が Windows 経由でキャプチャします。ゲームキャプチャは下のチェックボックスです。オフ：ソースは隠されるだけで、独自の画面キャプチャには一切触れません。',
    'Das Programm startet den Wiederholungspuffer in OBS, sobald DBD läuft, und stoppt ihn, wenn DBD zu ist – so kostet er ausserhalb des Spiels nichts und du musst nicht daran denken.':
        'DBD が起動するとすぐに OBS のリプレイバッファを開始し、DBD を閉じると停止します – ゲーム外では負荷がかからず、気にする必要もありません。',
    'Nachlauf nach dem Rundenende':
        'ラウンド終了後の余白',
    'Overlay mit in die Aufnahme':
        'オーバーレイを録画に含める',
    'Die Fensteraufnahme enthält das Overlay dieses Programms nicht (eigene Fenster). Mit Häkchen schreibt das Programm das sichtbare Overlay – Karte, Infos, Systemwerte, Heute, Musik – als Bild in seinen Cache-Ordner und legt in OBS eine Bildquelle „Fog Scout – Overlay“ darauf an, genau dort, wo das Overlay über dem DBD-Fenster liegt. Nur zusammen mit „Nur das DBD-Fenster aufnehmen“; bei einer Bildschirmaufnahme ist das Overlay ohnehin im Bild. Aus: die Quelle wird nur ausgeblendet.':
        'ウィンドウキャプチャには、このプログラムのオーバーレイ（独自のウィンドウ）は含まれません。チェックを入れると、プログラムは表示中のオーバーレイ（マップ、行、システム値、今日、音楽）を画像としてキャッシュフォルダーに書き込み、OBS にそれを表示する画像ソース「Fog Scout – Overlay」を、オーバーレイが DBD ウィンドウに重なる位置にぴったり作成します。「DBD のウィンドウのみを録画する」と併用した場合のみ。画面キャプチャにはいずれにせよオーバーレイが写ります。オフ：ソースは隠されるだけです。',
    'Overlay in OBS nicht eingerichtet: {error}':
        'OBS でオーバーレイが設定されていません：{error}',
    '{n} s':
        '{n} 秒',
    'keiner':
        'なし',
    'Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen.':
        '録画ドライブが接続されていません – ラウンドは録画されません。',
    'OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})':
        'OBS が起動していません – ラウンドは録画されません。（{error}）',
    'OBS bereit – Runden werden aufgenommen':
        'OBS 準備完了 – ラウンドは録画されます',
    'Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).':
        '録画が壊れているようです（{why}）：{file} – OBS の設定（エンコーダー、ドライブ）を確認してください。',
    'Aufnahme':
        '録画',
    'Vorlauf und Runde zu einer Datei zusammenfügen':
        'プリロールとラウンドを 1 つのファイルに結合する',
    'Nach der Runde hängt ffmpeg den Vorlauf vorne an die Aufnahme – ohne Neukodierung, in Sekunden. Seit 1.5.5 standardmässig aus: Am PC des Nutzers lief der Rundenteil der zusammengefügten Datei zu schnell. Klappt es nicht, bleiben beide Dateien liegen.':
        'ラウンド後、ffmpeg がプリロールを録画の前に付けます – 再エンコードなし、数秒の処理です。1.5.5 以降は既定でオフ：ユーザーの PC では、結合したファイルのラウンド部分が速く再生されすぎました。失敗した場合は両方のファイルが残ります。',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start; bis dahin bleibt der Vorlauf eine eigene Datei.':
        'ffmpeg がありません（パッケージ imageio-ffmpeg）– start.bat が次回の起動時にインストールします。それまではプリロールは別のファイルのままです。',
    'Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben':
        '保存しました：{file} – プリロールは結合されず、別のファイルとして隣にあります',
    'Clip-Marke setzen':
        'クリップマークを設定',
    'Clip-Marke {n} bei {pos} gesetzt.':
        'クリップマーク {n} を {pos} に設定しました。',
    'Keine Aufnahme läuft – keine Clip-Marke gesetzt.':
        '録画が実行されていません – クリップマークは設定されませんでした。',
    'Aufnahmen':
        '録画',
    'Aufnahmen einrichten …':
        '録画を設定…',
    'Öffnet die Einstellungen für die Aufnahmen mit OBS (Ordner, Verbindung).':
        'OBS での録画の設定（フォルダー、接続）を開きます。',
    'Platte nicht angeschlossen':
        'ドライブが接続されていません',
    'kein Ordner gewählt':
        'フォルダー未選択',
    'Platz wird gemessen …':
        '容量を計測中…',
    '{n} mit Marke':
        'マーク付き {n} 件',
    'älteste {date}':
        '最も古いもの {date}',
    '{size} frei':
        '空き {size}',
    '1 Aufnahme':
        '1 件の録画',
    '{n} Aufnahmen':
        '{n} 件の録画',
    'Abspielen':
        '再生',
    'Alle Aufnahmen':
        'すべての録画',
    'Aufnahme fehlt: {file}':
        '録画が見つかりません：{file}',
    'Aufnahme gelöscht: {file}':
        '録画を削除しました：{file}',
    'Aufnahme löschen':
        '録画を削除',
    'Aufnahme nicht gelöscht ({error}): {file}':
        '録画は削除されませんでした（{error}）：{file}',
    'Aufnahme wird behalten: {file}':
        '録画を保持します：{file}',
    'Aufnahme wird nicht mehr behalten: {file}':
        '録画の保持を解除しました：{file}',
    'Aufnahme-Laufwerk nicht angeschlossen.':
        '録画ドライブが接続されていません。',
    'Aufnahmeordner öffnen':
        '録画フォルダーを開く',
    'Behalten':
        '保持',
    'Beschädigt':
        '破損',
    'Datei':
        'ファイル',
    'Einschalten unter Einstellungen → Aufnahmen.':
        '「設定」→「録画」でオンにしてください。',
    'Im Explorer zeigen':
        'エクスプローラーで表示',
    'Keine Marken – F8 während der Runde setzt eine.':
        'マークなし – ラウンド中に F8 で設定できます。',
    'Marken: {list}':
        'マーク：{list}',
    'Mit Marke':
        'マーク付き',
    'Nicht mehr behalten':
        '保持を解除',
    'Noch kein Aufnahmeordner gewählt.':
        '録画フォルダーがまだ選択されていません。',
    'fehlt':
        '見つかりません',
    '{file} von der Platte löschen?':
        '{file} をドライブから削除しますか？',
    'Spielt die markierte Aufnahme im Standard-Videoplayer ab.':
        '選択した録画を既定のビデオプレーヤーで再生します。',
    'Öffnet den Explorer mit der markierten Datei.':
        '選択したファイルを選択した状態でエクスプローラーを開きます。',
    'Eine behaltene Aufnahme wird nie fürs Aufräumen gelöscht, wenn die Platte Platz braucht. Nochmal drücken hebt es auf.':
        '保持した録画は、ドライブの容量が必要になってもクリーンアップで削除されません。もう一度押すと元に戻ります。',
    'Löscht die markierte Aufnahme (und ihren Vorlauf) von der Platte – nach Rückfrage.':
        '選択した録画（とそのプリロール）を、確認後にドライブから削除します。',
    'Öffnet den Aufnahmeordner im Explorer.':
        '録画フォルダーをエクスプローラーで開きます。',
    'Farming-Runden im Unterordner „Farming“ ablegen':
        'ファーミングラウンドをサブフォルダー「Farming」に入れる',
    'Runden, die das Programm als Farming erkennt (Crossplay aus oder die Farming-Region), landen im Unterordner „Farming“ des Aufnahmeordners statt zwischen den normalen Runden. Clips gehen immer in den Ordner „Clips“.':
        'プログラムがファーミング（クロスプレイオフまたはファーミングリージョン）と認識したラウンドは、通常のラウンドの中ではなく、録画フォルダーのサブフォルダー「Farming」に保存されます。クリップは常に「Clips」フォルダーに入ります。',
    'Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in debug/lobby).':
        'クロスプレイの表示を読み取れません – このラウンドはファーミングとして数えられません（切り抜きは debug/lobby に）。',
    'Rolle für {n} Runden auf {role} geändert.':
        '{n} ラウンドの役割を {role} に変更しました。',
    '{n} Runden aus der Statistik löschen?':
        '{n} ラウンドを統計から削除しますか？',
    '{n} Runden gelöscht.':
        '{n} ラウンドを削除しました。',
    '{n} Runden zählen jetzt als Farming-Runden.':
        '{n} ラウンドをファーミングラウンドとして数えるようになりました。',
    '{n} Runden zählen wieder als normale Runden.':
        '{n} ラウンドを再び通常のラウンドとして数えます。',
    'Clip bearbeiten …':
        'クリップを編集…',
    'Öffnet den Clip-Editor für die markierte Aufnahme: Vorschau, Zeitleiste mit Marken, Start/Ende setzen, Ausschnitt als MP4 in den Ordner „Clips“ speichern.':
        '選択した録画のクリップエディターを開きます：プレビュー、マーク付きタイムライン、開始/終了の設定、カットを MP4 として「Clips」フォルダーに保存。',
    'Clip bearbeiten – {name}':
        'クリップを編集 – {name}',
    'Schnell (an Schlüsselbildern, Anfang bis zu ein paar Sekunden früher)':
        '高速（キーフレーム単位、開始が数秒早くなることがあります）',
    'Genau (Bild neu kodiert, dauert etwas)':
        '正確（映像を再エンコード、少し時間がかかります）',
    '5 Sekunden vor (Shift+→)':
        '5 秒進む（Shift+→）',
    '5 Sekunden zurück (Shift+←)':
        '5 秒戻る（Shift+←）',
    '▶ Abspielen':
        '▶ 再生',
    '⏸ Pause':
        '⏸ 一時停止',
    'Abspielen / Pause (Leertaste)':
        '再生 / 一時停止（スペースキー）',
    'Start setzen':
        '開始を設定',
    'Ende setzen':
        '終了を設定',
    'Der Clip beginnt am Abspielkopf (Taste I).':
        'クリップは再生ヘッドの位置から始まります（キー I）。',
    'Der Clip endet am Abspielkopf (Taste O).':
        'クリップは再生ヘッドの位置で終わります（キー O）。',
    'Zur Marke ▸':
        'マークへ ▸',
    'Marken (F8)':
        'マーク（F8）',
    'Clip um Marke':
        'マーク周辺のクリップ',
    'Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der nächsten am Abspielkopf) und endet {after} s danach.':
        'クリップは選択したマーク（未選択の場合は再生ヘッドに最も近いマーク）の {before} 秒前から始まり、{after} 秒後に終わります。',
    'Springt zur nächsten F8-Marke (Taste M).':
        '次の F8 マークへジャンプします（キー M）。',
    'Clip: {start} – {end} ({length} s)':
        'クリップ：{start} – {end}（{length} 秒）',
    'Beim Abspielen den Ton der Aufnahme mitlaufen lassen (Windows).':
        'プレビューと一緒に録画の音声を再生します（Windows）。',
    'Ton im Clip':
        'クリップの音声',
    'Abspielkopf hierher':
        'ここに再生ヘッド',
    'Als Custom Game':
        'カスタムマッチとして',
    'Als Killer-Runde':
        'キラーのラウンドとして',
    'Als Survivor-Runde':
        'サバイバーのラウンドとして',
    'Ausblenden':
        '非表示',
    'Bild':
        '画像',
    'Clip beginnt hier':
        'クリップの開始をここに',
    'Clip endet hier':
        'クリップの終了をここに',
    'Dunkle Fläche dahinter':
        '背後に暗い領域',
    'Grösse zurücksetzen':
        'サイズをリセット',
    'Standbild gespeichert: {file}':
        '静止画を保存しました：{file}',
    'Standbild hier speichern':
        'ここで静止画を保存',
    'Standbild nicht gespeichert.':
        '静止画は保存されませんでした。',
    '{n} Runden löschen':
        '{n} ラウンドを削除',
    'Grosser Editor …':
        '大きなエディター…',
    'Öffnet den Clip im eigenen Fenster – mit Zensieren, Lautstärke je Tonquelle und allen Tasten.':
        'クリップを専用ウィンドウで開きます – 検閲、音声ソースごとの音量、すべてのキー操作付き。',
    'Discord-Sprachchat – OBS-Spur 3. Aus = der Clip hat keinen Discord-Ton.':
        'Discord のボイスチャット – OBS トラック 3。オフ = クリップに Discord の音声が入りません。',
    'Dein Mikrofon – OBS-Spur 4 (nur, wenn es in OBS aufgenommen wird).':
        'マイク – OBS トラック 4（OBS が録音している場合のみ）。',
    'Lautstärke dieser Quelle im Clip (100 % = wie aufgenommen).':
        'クリップ内でのこのソースの音量（100 % = 録音したまま）。',
    'Eine Tonspur – zum Mischen nimmt OBS mit Spur 1–4 auf (Einstellungen → Aufnahmen).':
        'オーディオトラックが 1 つです – ミキシングするには、OBS でトラック 1～4 を録音してください（「設定」→「録画」）。',
    'ohne Ton':
        '音声なし',
    'Ton neu gemischt':
        '音声を再ミックス',
    'Clip speichern':
        'クリップを保存',
    'Schreibt den Ausschnitt als MP4 in den Ordner „Clips“ neben den Aufnahmen.':
        'カットを MP4 として録画の隣の「Clips」フォルダーに書き込みます。',
    'Clips-Ordner öffnen':
        'クリップフォルダーを開く',
    'Öffnet den Ordner „Clips“ im Explorer.':
        '「Clips」フォルダーをエクスプローラーで開きます。',
    'Datei nicht lesbar oder ffmpeg fehlt – keine Vorschau.':
        'ファイルを読み取れないか、ffmpeg がありません – プレビューなし。',
    'Clips-Ordner nicht anlegbar: {error}':
        'クリップフォルダーを作成できません：{error}',
    'Schreibe {file} …':
        '{file} を書き込み中…',
    'Clip gespeichert: {file}':
        'クリップを保存しました：{file}',
    'Clip nicht gespeichert: {why}':
        'クリップは保存されませんでした：{why}',
    '(Sofort-Clip)':
        '（インスタントクリップ）',
    'Aufnahme schon am Ladebildschirm starten':
        'ロード画面から録画を開始する',
    'Aufnahme-Laufwerk nicht angeschlossen':
        '録画ドライブが接続されていません',
    'Clip':
        'クリップ',
    'DBD':
        'DBD',
    'Discord':
        'Discord',
    'F8 speichert die letzten Sekunden als Sofort-Clip':
        'F8 で直近の数秒をインスタントクリップとして保存する',
    'Kein Sofort-Clip: {why}':
        'インスタントクリップなし：{why}',
    'Ladebildschirm vorbei – das Match beginnt.':
        'ロード画面終了 – マッチが始まります。',
    'Mikrofon':
        'マイク',
    'Spiel':
        'ゲーム',
    'Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner':
        '録画中 – ロード画面の終了から、マップバナーを待機中',
    'Nimmt die Runde auf (seit dem Ladebildschirm)':
        'ラウンドを録画中（ロード画面から）',
    'OBS hat den Puffer nicht gespeichert':
        'OBS がバッファを保存しませんでした',
    'Sofort-Clip gespeichert ({n} s): {file}':
        'インスタントクリップを保存しました（{n} 秒）：{file}',
    'Ton in OBS einstellen, sobald DBD startet:':
        'DBD の起動と同時に OBS の音声を設定する：',
    'Ton in OBS nicht eingestellt: {error}':
        'OBS の音声が設定されていません：{error}',
    'OBS bereit – Runden werden aufgenommen. {problem}':
        'OBS 準備完了 – ラウンドは録画されます。{problem}',
    'Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)':
        'クリップエディターでの音声ミックスのため、OBS で：「設定」→「出力」→ 出力モード「詳細」→「録画」タブ → 音声トラック 1～5 にチェック（1 すべて、2 ゲーム、3 Discord、4 マイク、5 バックグラウンド）',
    'Jede Tonquelle auf eine eigene OBS-Tonspur':
        '各音声ソースを OBS の個別のトラックに',
    'Dafür in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter Aufnahme → Audiospur 1 bis 5 anhaken. Das Programm prüft das beim DBD-Start und meldet es im Kasten „Aufnahmen mit OBS“; es ändert nichts am OBS-Profil.':
        'そのため OBS で：「設定」→「出力」→ 出力モード「詳細」→「録画」タブ → 音声トラック 1～5 にチェック。プログラムは DBD の起動時にこれを確認し、「OBS で録画」カードで報告します。OBS のプロファイルは何も変更しません。',
    'Sofort-Clip (F8) mit Ton von:':
        'インスタントクリップ（F8）の音声ソース：',
    'Wie bei Medal: Das Programm weist in OBS jede Tonquelle der Spur 1 (alles – spielt in jedem Player) und ihrer eigenen Spur zu: nur DBD 2, Discord 3, Mikrofon 4, alle anderen Tonquellen in OBS (z. B. Spotify, Browser) 5 = Hintergrund. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt deshalb nur auf Spur 1. Im Clip-Editor schaltest du jede Quelle an oder aus und regelst ihre Lautstärke; beim Speichern mischt ffmpeg sie zusammen. OBS schreibt die Spuren nur im Ausgabemodus „Erweitert“ mit Audiospur 1 bis 5 angehakt (MKV oder MP4, nicht FLV); das Programm prüft das beim DBD-Start und meldet es, ändert aber nichts am OBS-Profil. Aus = Spuren bleiben, wie sie in OBS stehen.':
        'Medal のように：プログラムは OBS の各音声ソースをトラック 1（すべて – どのプレーヤーでも再生可能）と専用のトラックに割り当てます：DBD のみ 2、Discord 3、マイク 4、OBS のその他の音声ソース（例：Spotify、ブラウザー）は 5 = バックグラウンド。Windows のデスクトップ音声には DBD と Discord も含まれるため、トラック 1 のみに置かれます。クリップエディターで各ソースのオン/オフと音量を設定でき、保存時に ffmpeg がミックスします。OBS がトラックを書き込むのは出力モード「詳細」で音声トラック 1～5 にチェックが入っている場合のみです（MKV または MP4、FLV は不可）。プログラムは DBD の起動時にこれを確認して報告しますが、OBS のプロファイルは何も変更しません。オフ = トラックは OBS の設定のままです。',
    'Nur der Ton von DBD im Sofort-Clip.':
        'インスタントクリップには DBD の音声のみ。',
    'Ton von Discord (Sprachchat) in der Aufnahme bzw. im Sofort-Clip.':
        '録画またはインスタントクリップに Discord（ボイスチャット）の音声を入れます。',
    'Dein Mikrofon – die Quelle „Mikrofon/AUX“ in OBS bzw. seine Spur im Sofort-Clip.':
        'マイク – OBS のソース「マイク/AUX」、またはインスタントクリップ内のそのトラック。',
    'Hintergrund':
        'バックグラウンド',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) – OBS-Spur 5. Der Desktop-Ton von Windows enthält auch DBD und Discord und liegt nur auf Spur 1.':
        'OBS に専用の音声ソースを持つその他のプログラム（例：Spotify、ブラウザー）– OBS トラック 5。Windows のデスクトップ音声には DBD と Discord も含まれ、トラック 1 のみに置かれます。',
    'Andere Programme mit eigener Tonquelle in OBS (z. B. Spotify, Browser) im Sofort-Clip – OBS-Spur 5.':
        'インスタントクリップに入れる、OBS に専用の音声ソースを持つその他のプログラム（例：Spotify、ブラウザー）– OBS トラック 5。',
    'Tonquelle angelegt: {name}':
        '音声ソースを作成しました：{name}',
    'Farming-Aufnahmen löschen nach':
        'ファーミングの録画を削除するまでの期間',
    'nie':
        'しない',
    '{n} Tagen':
        '{n} 日',
    'Alte Farming-Aufnahmen gelöscht (älter als {days} Tage): {n}':
        '古いファーミングの録画を削除しました（{days} 日より前）：{n}',
    '{name} – keine Quelle':
        '{name} – ソースなし',
    '{name} – in OBS aus':
        '{name} – OBS でオフ',
    'In OBS gab es bei dieser Aufnahme keine Hintergrund-Quelle. Für Spotify, Browser & Co. in OBS je Programm eine Anwendungs-Audioaufnahme anlegen – das Programm legt sie auf Spur 5.':
        'この録画では OBS にバックグラウンドソースがありませんでした。Spotify やブラウザーなどには、OBS でプログラムごとにアプリケーション音声キャプチャを追加してください – プログラムがそれをトラック 5 に置きます。',
    'Diese Tonquelle war bei der Aufnahme unter Einstellungen → Aufnahmen ausgeschaltet.':
        'この録画時、この音声ソースは「設定」→「録画」でオフになっていました。',
    'Tonquelle {name} hört jetzt auf {exe}':
        '音声ソース {name} は {exe} を聞くようになりました',
    'Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}':
        'ゲーム/Discord/マイクの代わりにトラック 5（バックグラウンド）へ：{names}',
    'Auf Spur {n} ist in der ganzen Aufnahme nichts zu hören.':
        '録画全体を通して、トラック {n} には何も聞こえません。',
    'Tonquelle zur Szene „{scene}“ hinzugefügt: {name}':
        'シーン「{scene}」に音声ソースを追加しました：{name}',
    'Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}':
        'シーン「{scene}」で音声ソースを再表示しました：{name}',
    '{name} (Spur {n})':
        '{name}（トラック {n}）',
    'Still in dieser Aufnahme: {names} – OBS hat dort nichts aufgenommen. In OBS prüfen: Quelle in der Szene der Aufnahme, nicht stumm, Spur angehakt.':
        'この録画では無音：{names} – OBS はそこに何も録音しませんでした。OBS で確認してください：録画中のシーンにソースがあるか、ミュートされていないか、トラックにチェックが入っているか。',
    '{name} – still':
        '{name} – 無音',
    'Nur der Ton von Dead by Daylight – OBS-Spur 2.':
        'Dead by Daylight の音声のみ – OBS トラック 2。',
    'Unbekannte Map':
        '不明なマップ',
    'Wiederholungspuffer in OBS läuft nicht':
        'OBS のリプレイバッファが実行されていません',
    'Übriger Desktop-Ton':
        'その他のデスクトップ音声',
    'Das Map-Banner kommt erst einige Sekunden nach dem Spawn. Mit diesem Häkchen startet OBS schon, wenn der Ladebildschirm nach der Lobby endet – ohne Lobby, mit Spawn. Das Banner benennt die Aufnahme danach. Kommt 3 Minuten lang kein Banner, endet die Aufnahme und heisst „Unbekannte Map“.':
        'マップバナーはスポーンの数秒後に表示されます。このチェックボックスを使うと、ロビー後のロード画面が終わるとすぐに OBS が録画を開始します – ロビーなし、スポーン込みです。録画の名前は後からバナーで付けられます。3 分間バナーがない場合、録画は終了し「不明なマップ」という名前になります。',
    'F8 sichert den Wiederholungspuffer von OBS und legt die letzten Sekunden als MP4 in den Ordner „Clips“ – Bild ohne Neukodierung, in Sekunden. Spur 1 ist die unten gewählte Tonmischung (spielt überall), dahinter liegen die Einzelspuren des Puffers für den Clip-Editor. Der Wiederholungspuffer muss in OBS eingerichtet sein. Die Marke in der Rundenaufnahme setzt F8 weiterhin.':
        'F8 で OBS のリプレイバッファを保存し、その直近の数秒を MP4 として「Clips」フォルダーに入れます – 映像は再エンコードなし、数秒の処理です。トラック 1 は下で選んだ音声ミックス（どこでも再生可能）で、その後ろにクリップエディター用のバッファ自体のトラックが続きます。リプレイバッファは OBS で設定する必要があります。F8 はラウンドの録画にもマークを設定します。',
    'Das Programm legt in der aktuellen OBS-Szene je eine Anwendungs-Audioaufnahme für DBD und Discord an (einmalig) und schaltet die Tonquellen wie gewählt stumm oder laut – beim Start von DBD und bei jeder Änderung hier, auch mitten in der Runde. Aufnehmen tut OBS, das Programm fasst DBD nicht an. Braucht OBS 28 oder neuer.':
        'プログラムは現在の OBS シーンに DBD と Discord 用のアプリケーション音声キャプチャをそれぞれ 1 つ作成し（一度だけ）、選択に応じて音声ソースをミュート/ミュート解除します – DBD の起動時と、ここでの変更のたびに（ラウンド中も）。キャプチャを行うのは OBS で、プログラムは DBD に触れません。OBS 28 以降が必要です。',
    'Ton des Spiels in der Aufnahme.':
        '録画内のゲームの音声。',
    'Alles andere, was am PC zu hören ist (Musik, Browser, Systemtöne) – die Quelle „Desktop-Audio“ in OBS.':
        'PC で聞こえるその他すべて（音楽、ブラウザー、システム音）– OBS のソース「デスクトップ音声」。',
    'Als Farming markieren':
        'ファーミングとしてマーク',
    'Grund':
        '理由',
    'Ist Farming':
        'ファーミングである',
    'Kein Farming':
        'ファーミングではない',
    'Alle als Farming':
        'すべてファーミングに',
    'Alle ignorieren':
        'すべて無視',
    'Custom Game, laut Stats-Seite öffentlich':
        'カスタムマッチ、統計ページでは公開',
    'kurze Serie, gleicher Gegner':
        '短いラウンド、同じ相手',
    '{n} Runden bleiben normale Runden (kein Farming).':
        '{n} ラウンドは通常のラウンドのままです（ファーミングではありません）。',
    'Markiert alle Runden der Liste als Farming-Runden (mit Rückfrage) – wie „Ist Farming“ für jede.':
        'リストのすべてのラウンドをファーミングラウンドとしてマークします（先に確認します）– 各ラウンドで「ファーミングである」を選ぶのと同じです。',
    'Keine der Runden der Liste mehr vorschlagen – sie bleiben, wie sie sind.':
        'リストのラウンドを今後一切提案しません – そのままにします。',
    'Die markierten Runden der Liste sind Farming-Runden (und kein Custom Game mehr); ihre Aufnahmen wandern in den Ordner „Farming“. Zurück: „Farming an/aus“ unter „Letzte Runden“.':
        'リストで選択したラウンドはファーミングラウンドです（カスタムマッチではなくなります）。録画は「Farming」フォルダーに移動します。戻すには：「最近のラウンド」の「ファーミング オン/オフ」。',
    'Die markierten Runden der Liste sind normale Runden – sie bleiben, wie sie sind, und werden nie wieder vorgeschlagen.':
        'リストで選択したラウンドは通常のラウンドです – そのままにし、今後提案しません。',
    'Discord: ohne Nitro 10 MB, Nitro Basic 50 MB, Nitro 500 MB.':
        'Discord：Nitro なしは 10 MB、Nitro Basic は 50 MB、Nitro は 500 MB。',
    'Format':
        '形式',
    'Für Discord (passt unter die Zielgrösse)':
        'Discord 用（目標サイズに収める）',
    'Gespeichert: {file} ({mb} MB)':
        '保存しました：{file}（{mb} MB）',
    'Ignorieren':
        '無視',
    'Runden nicht geändert: {error}':
        'ラウンドは変更されませんでした：{error}',
    'Spielt genau den Ausschnitt ab und springt danach an seinen Anfang zurück.':
        'クリップの範囲だけを再生し、その後開始位置に戻ります。',
    'Zeigt den zuletzt gespeicherten Clip im Explorer.':
        '最後に保存したクリップをエクスプローラーで表示します。',
    '{n} Runden als Farming markiert.':
        '{n} ラウンドをファーミングとしてマークしました。',
    '{n} Runden als Farming-Runden markieren?':
        '{n} ラウンドをファーミングラウンドとしてマークしますか？',
    '{n} Runden sehen nach Farming aus: {reasons}. Zuletzt: {map}, {when}.':
        '{n} ラウンドがファーミングのようです：{reasons}。最新：{map}、{when}。',
    '{n} als Custom Game gespeichert, laut Stats-Seite aber öffentliche Matches (vor 1.5.5 so erkannt)':
        '{n} 件がカスタムマッチとして保存されていますが、統計ページでは公開マッチです（1.5.5 より前の読み取り）',
    '{n} kurze Runden (bis 3 min) hintereinander gegen denselben Charakter':
        '同じキャラクターとの短いラウンド（3 分以内）が {n} 回連続',
    'Farming?':
        'ファーミング？',
    'Runden sehen nach Farming aus':
        'ラウンドがファーミングのようです',
    'Farming prüfen …':
        'ファーミングを確認…',
    'Öffnet die Statistik-Übersicht mit der Zeile, die sagt, warum diese Runden nach Farming aussehen – dort markieren oder ignorieren.':
        'これらのラウンドがファーミングに見える理由の行とともに、統計の概要を開きます – そこでマークするか無視してください。',
    'etwa {mb} MB':
        '約 {mb} MB',
    'wird {h}p {fps} fps, ≈ {kbps} kbit/s, unter {mb} MB':
        '{h}p {fps} fps、≈ {kbps} kbit/s、{mb} MB 未満になります',
    '≤ {n} MB':
        '≤ {n} MB',
    '▶ Clip ansehen':
        '▶ クリップを見る',
    'Markiert alle genannten Runden als Farming-Runden (und nicht mehr als Custom Game); ihre Aufnahmen wandern in den Ordner „Farming“. Einzeln zurück: „Farming an/aus“ unter „Letzte Runden“.':
        'これらのラウンドをすべてファーミングラウンドとしてマークします（カスタムマッチではなくなります）。録画は「Farming」フォルダーに移動します。1 つずつ戻すには：「最近のラウンド」の「ファーミング オン/オフ」。',
    'Diese Runden nicht mehr vorschlagen – sie bleiben, wie sie sind.':
        'これらのラウンドを今後提案しません – そのままにします。',
    'Alle':
        'すべて',
    'BP/h':
        'BP/時',
    'BP/h mit Wartezeit':
        '待ち時間込み BP/時',
    'Bloodpoints':
        'ブラッドポイント',
    'Bloodpoints laut Stats-Seite. BP/h = je Stunde im Match; mit Wartezeit = je Stunde aus Match und Suche zusammen. Was das Farmen allein bringt, steht im Reiter „Farming“; „Farming ausblenden“ rechnet hier ohne Farming-Runden.':
        '統計ページのブラッドポイント。BP/時 = マッチ中の 1 時間あたり。待ち時間込み = マッチと検索を合わせた 1 時間あたり。ファーミングだけで得たものは「ファーミング」タブにあります。「ファーミングを除外」でここからファーミングラウンドを除外できます。',
    'Bloodpoints pro Stunde':
        '1 時間あたりのブラッドポイント',
    'Summe':
        '合計',
    'mit Wartezeit {bp}':
        '待ち時間込み {bp}',
    'Rekorde':
        '記録',
    'Serien zählen Runden mit Ergebnis laut Stats-Seite in zeitlicher Reihenfolge – „aktuell“ ist die Serie der neuesten Runden der Auswahl. Beste Woche ab {n} Runden mit Ergebnis. Eine Sitzung endet nach 45 Minuten ohne Runde.':
        '連続記録は、統計ページの結果があるラウンドを時間順に数えます – 「現在」は選択範囲の最新ラウンドでの連続記録です。ベストウィークは結果のあるラウンドが {n} 回以上の週から。セッションはラウンドなしで 45 分経過すると終了します。',
    'Noch keine Runden in dieser Auswahl.':
        'この選択範囲にはまだラウンドがありません。',
    'aktuell {n}':
        '現在 {n}',
    'zuletzt {date}':
        '最終 {date}',
    '4K-Serie':
        '4K 連続',
    'Ø {kills} Kills · {n} Runden als {killer}':
        '平均 {kills} キル · {killer} で {n} ラウンド',
    '{share} entkommen · {n} Runden gegen {killer}':
        '脱出 {share} · {killer} 相手に {n} ラウンド',
    '4K-Serie {n}':
        '4K 連続 {n}',
    'Entkommen-Serie {n}':
        '脱出連続 {n}',
    'Entkommen-Serie':
        '脱出連続',
    'Beste Woche als Killer':
        'キラーのベストウィーク',
    'ab {date} · {n} Runden':
        '{date} から · {n} ラウンド',
    'ab {n} Killer-Runden in einer Woche':
        '1 週間にキラーのラウンドが {n} 回以上',
    'Beste Woche als Survivor':
        'サバイバーのベストウィーク',
    'ab {n} Survivor-Runden in einer Woche':
        '1 週間にサバイバーのラウンドが {n} 回以上',
    'Meiste Runden an einem Tag':
        '1 日の最多ラウンド',
    'Längste Sitzung':
        '最長セッション',
    'Längste Runde':
        '最長ラウンド',
    'Spielstatus in Discord anzeigen (Rich Presence)':
        'Discord にゲームのステータスを表示する（Rich Presence）',
    'Application-ID':
        'アプリケーション ID',
    'Discord testen':
        'Discord をテスト',
    'Developer-Portal öffnen':
        '開発者ポータルを開く',
    'Killer in Discord anzeigen':
        'Discord にキラーを表示する',
    'Auch Lobby, Suche und Menü anzeigen':
        'ロビー、検索、メニューも表示する',
    'Zeigt in deinem Discord-Status, was gerade läuft: „Nurse auf Coal Tower“ mit Rundenzeit, in der Lobby „Sucht ein Match“. Discord braucht dafür eine Application-ID: im Developer-Portal „New Application“ anlegen (als Name z. B. „Dead by Daylight“ – so steht es im Status), die Application-ID kopieren und hier eintragen. Das Programm spricht nur mit dem Discord-Client auf diesem PC (lokale Pipe), ohne ID wird nichts gesendet; Discord erfährt nur Map, Rolle, Killer und die Startzeit.':
        'Discord のステータスに状況を表示します：ラウンド時間とともに「Nurse on Coal Tower」、ロビーでは「マッチを検索中」。そのために Discord にはアプリケーション ID が必要です：開発者ポータルで「New Application」を作成し（名前は例えば「Dead by Daylight」– これがステータスに表示されます）、そのアプリケーション ID をコピーしてここに入力してください。プログラムはこの PC の Discord クライアントとのみ通信します（ローカルパイプ）。ID がなければ何も送信されません。Discord が知るのはマップ、役割、キラー、開始時刻のみです。',
    'Verbinde mit Discord …':
        'Discord に接続中…',
    'Discord nicht gefunden – läuft es?':
        'Discord が見つかりません – 起動していますか？',
    'Killer · {killer}':
        'キラー · {killer}',
    'Im Match':
        'マッチ中',
    'Sucht ein Match':
        'マッチを検索中',
    'In der Lobby':
        'ロビー',
    'Bereit machen':
        '準備中',
    'Im Menü':
        'メニュー',
    'Discord: aus':
        'Discord：オフ',
    'Discord: Fehler – {error}':
        'Discord：エラー – {error}',
    'Application-ID fehlt – im Developer-Portal anlegen und hier eintragen.':
        'アプリケーション ID がありません – 開発者ポータルで作成し、ここに入力してください。',
    'Ungültige Application-ID ({error})':
        '無効なアプリケーション ID（{error}）',
    'Discord: verbunden':
        'Discord：接続済み',
    'Als Killer steht dein Killer im Status („Killer · The Nurse“); aus = nur „Killer“.':
        'キラーの場合、ステータスにキラー名を表示します（「キラー · The Nurse」）。オフ = 「キラー」のみ。',
    'Aus = der Status erscheint nur während einer Runde; sonst auch „Sucht ein Match“, „In der Lobby“ und „Im Menü“, solange DBD läuft.':
        'オフ = ステータスはラウンド中のみ表示されます。オンなら DBD の起動中は「マッチを検索中」「ロビー」「メニュー」も表示されます。',
    'Dein Discord-Status zeigt Map, Rolle, Killer und die Rundenzeit (in der Lobby: Suche/Lobby). Braucht eine Application-ID aus dem Discord-Developer-Portal; das Programm spricht nur mit dem Discord-Client auf diesem PC.':
        'Discord のステータスにマップ、役割、キラー、ラウンド時間を表示します（ロビーでは検索/ロビー）。Discord の開発者ポータルのアプリケーション ID が必要です。プログラムはこの PC の Discord クライアントとのみ通信します。',
    'Verbindet sich einmal mit dem laufenden Discord und zeigt, ob die Application-ID angenommen wird.':
        '起動中の Discord に一度接続し、アプリケーション ID が受け付けられるかどうかを表示します。',
    'Öffnet discord.com/developers im Browser: „New Application“ anlegen (Name z. B. „Dead by Daylight“), die Application-ID kopieren und links eintragen.':
        'ブラウザーで discord.com/developers を開きます：「New Application」を作成し（名前は例えば「Dead by Daylight」）、そのアプリケーション ID をコピーして左に入力してください。',
    'Ø pro Runde':
        'ラウンドあたりの平均',
    'BP/h im Match':
        'マッチ中の BP/時',
    'Spielzeit laut Stats-Seite':
        '統計ページのプレイ時間',
    'Match und Suche zusammen':
        'マッチと検索の合計',
    'Beste Runde':
        'ベストラウンド',
    'Ø BP als Killer':
        'キラーの平均 BP',
    'Ø BP als Survivor':
        'サバイバーの平均 BP',
    '{when}: Ø {bp} BP · {n} Runden · Summe {sum}':
        '{when}：平均 {bp} BP · {n} ラウンド · 合計 {sum}',
    'Ø Bloodpoints pro Runde {per}':
        'ラウンドあたりの平均ブラッドポイント {per}',
    'Keine Runden mit Bloodpoints in dieser Auswahl.':
        'この選択範囲にはブラッドポイントのあるラウンドがありません。',
    'Verpixelt':
        'モザイク',
    'Verwischt':
        'ぼかし',
    'Schwarz':
        '黒塗り',
    'Zensieren':
        '検閲',
    'Beim Speichern anwenden':
        '保存時に適用',
    'Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das Bild neu kodiert, auch im Format „Schnell“).':
        '保存したクリップでは枠の部分が隠されます（そのため映像は再エンコードされます。「高速」形式でも同様です）。',
    'Kasten zeichnen':
        '枠を描く',
    'Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug.':
        '画像上で領域をドラッグしてください。枠は移動でき、右下の角でサイズを変更できます。もう一度押すとツールを終了します。',
    'Namen links unten':
        '左下の名前',
    'Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        'DBD がサバイバー名を表示する場所（ゲーム画面の左下）に枠を置きます – 必要に応じて移動してください。',
    'Kasten entfernen':
        '枠を削除',
    'Entfernt den markierten Kasten (Taste Entf).':
        '選択した枠を削除します（Del キー）。',
    'Alle entfernen':
        'すべて削除',
    'Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ lässt dich einen aufziehen.':
        'まだ枠がありません。「左下の名前」でサバイバー名に枠を置くか、「枠を描く」でドラッグして作成できます。',
    '{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.':
        '枠 {n} 個 – ドラッグ = 移動、右下の角 = サイズ、クリック = 選択。',
    '{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.':
        '枠 {n} 個を記憶 – 次のクリップにも適用されます。',
    'mit Zensur neu kodiert (wie „Genau“)':
        '検閲のため再エンコード（「正確」と同様）',
    'Retusche (aus der Umgebung übermalt)':
        'レタッチ（周囲から塗りつぶし）',
    'Spotify':
        'Spotify',
    '„Als nächstes“ aus Spotify in der Musikkarte zeigen':
        '音楽カードに Spotify の「次の曲」を表示する',
    'Client-ID':
        'クライアント ID',
    'Developer-Dashboard öffnen':
        '開発者ダッシュボードを開く',
    'Mit Spotify verbinden':
        'Spotify に接続',
    'Spotify-Verbindung trennen':
        'Spotify との接続を解除',
    'Spotify: öffne die Anmeldung im Browser …':
        'Spotify：ブラウザーでログインを開いています…',
    'YouTube':
        'YouTube',
    'Privat':
        '非公開',
    'Nicht gelistet':
        '限定公開',
    'Öffentlich':
        '公開',
    'Client-Secret':
        'クライアントシークレット',
    'Sichtbarkeit':
        '公開設定',
    'Clips automatisch auf YouTube hochladen':
        'クリップを自動で YouTube にアップロードする',
    'Google Cloud Console öffnen':
        'Google Cloud コンソールを開く',
    'Client-Datei laden …':
        'クライアントファイルを読み込む…',
    'Client-Datei laden':
        'クライアントファイルを読み込む',
    'Client-Datei von Google laden':
        'Google のクライアントファイルを読み込みます',
    'Das ist keine Client-Datei von Google ({error}).':
        'これは Google のクライアントファイルではありません（{error}）。',
    'YouTube: Client-ID und Client-Secret aus {file} übernommen – jetzt „Mit YouTube verbinden“ klicken.':
        'YouTube：{file} からクライアント ID とクライアントシークレットを取得しました – 「YouTube に接続」をクリックしてください。',
    'YouTube: Client-Daten aus {file} übernommen.':
        'YouTube：{file} からクライアントデータを取得しました。',
    'Datei zu gross':
        'ファイルが大きすぎます',
    'nicht lesbar: {error}':
        '読み取れません：{error}',
    'kein JSON: {error}':
        'JSON ではありません：{error}',
    'kein JSON-Objekt':
        'JSON オブジェクトではありません',
    'OAuth-Client vom Typ „Webanwendung“ – in der Cloud Console einen vom Typ „Desktop-App“ anlegen':
        '種類が「ウェブ アプリケーション」の OAuth クライアントです – Cloud コンソールで種類「デスクトップ アプリ」のクライアントを作成してください',
    'kein Abschnitt „installed“':
        '「installed」セクションがありません',
    'Client-ID fehlt oder endet nicht auf .apps.googleusercontent.com':
        'クライアント ID がないか、.apps.googleusercontent.com で終わっていません',
    'Client-Secret fehlt':
        'クライアントシークレットがありません',
    'Mit YouTube verbinden':
        'YouTube に接続',
    'YouTube-Verbindung trennen':
        'YouTube との接続を解除',
    'Auf YouTube hochladen':
        'YouTube にアップロード',
    'YouTube-Link kopieren':
        'YouTube のリンクをコピー',
    'Auf YouTube öffnen':
        'YouTube で開く',
    'YouTube: Client-ID (…apps.googleusercontent.com) und Client-Secret eintragen.':
        'YouTube：クライアント ID（…apps.googleusercontent.com）とクライアントシークレットを入力してください。',
    'YouTube: öffne die Anmeldung im Browser …':
        'YouTube：ブラウザーでログインを開いています…',
    'Hochgeladen: {file}':
        'アップロードしました：{file}',
    'YouTube: nicht hochgeladen – {file}: {why}':
        'YouTube：アップロードされませんでした – {file}：{why}',
    'YouTube: in die Warteschlange – {file}':
        'YouTube：キューに追加 – {file}',
    'YouTube-Link kopiert: {url}':
        'YouTube のリンクをコピーしました：{url}',
    'Clip: {what}':
        'クリップ：{what}',
    'Dauer {d}':
        '長さ {d}',
    'Aufgenommen mit Fog Scout':
        'Fog Scout で録画',
    'keine Upload-Sitzung erhalten':
        'アップロードセッションを受け取れませんでした',
    'Antwort ohne Video-ID':
        '動画 ID のない応答',
    'nicht angemeldet':
        'ログインしていません',
    'Datei nicht gefunden':
        'ファイルが見つかりません',
    'Aufnahmeordner nicht da':
        '録画フォルダーがありません',
    'YouTube: aus':
        'YouTube：オフ',
    'YouTube: nicht verbunden – „Mit YouTube verbinden“ klicken.':
        'YouTube：未接続 – 「YouTube に接続」をクリックしてください。',
    'Mit YouTube verbunden – du kannst dieses Fenster schliessen.':
        'YouTube に接続しました – このウィンドウは閉じてかまいません。',
    'Google hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Google がログインを拒否しました – このウィンドウは閉じてかまいません。',
    'YouTube: Anmeldung nicht möglich – {error}':
        'YouTube：ログインできません – {error}',
    'YouTube: Browser nicht geöffnet – {error}':
        'YouTube：ブラウザーが開きませんでした – {error}',
    'YouTube: Anmeldung abgelehnt ({error})':
        'YouTube：ログインが拒否されました（{error}）',
    'YouTube: Google gab kein dauerhaftes Token – in der Cloud Console den OAuth-Client als „Desktop“ anlegen und den Zustimmungsbildschirm veröffentlichen.':
        'YouTube：Google が永続的なトークンを発行しませんでした – Cloud コンソールで OAuth クライアントを「デスクトップ アプリ」として作成し、同意画面を公開してください。',
    'YouTube: verbunden':
        'YouTube：接続済み',
    'YouTube: Anmeldung abgelaufen – noch einmal „Mit YouTube verbinden“ klicken.':
        'YouTube：ログインの有効期限が切れました – もう一度「YouTube に接続」をクリックしてください。',
    'YouTube: {n} in der Warteschlange – wartet, bis Lobby und Runde vorbei sind':
        'YouTube：{n} 件待機中 – ロビーとラウンドが終わるまで待機',
    'YouTube: {n} in der Warteschlange – Tageskontingent aufgebraucht, weiter ab {when}':
        'YouTube：{n} 件待機中 – 1 日の割り当てを使い切りました。{when} に再開します',
    'YouTube: lädt {file} hoch ({pct} %)':
        'YouTube：{file} をアップロード中（{pct} %）',
    'YouTube: hochgeladen – {file}':
        'YouTube：アップロードしました – {file}',
    'YouTube: {error} – neuer Versuch in {s} s':
        'YouTube：{error} – {s} 秒後に再試行します',
    'YouTube: {n} in der Warteschlange – {why}':
        'YouTube：{n} 件待機中 – {why}',
    'Uploads in Playlists einsortieren':
        'アップロードを再生リストに振り分ける',
    'Playlists laden':
        '再生リストを読み込む',
    'Clips in':
        'クリップの追加先',
    'Runden in':
        'ラウンドの追加先',
    'YouTube: lade Playlists …':
        'YouTube：再生リストを読み込み中…',
    'YouTube: zuerst „Uploads in Playlists einsortieren“ anhaken.':
        'YouTube：先に「アップロードを再生リストに振り分ける」にチェックを入れてください。',
    'YouTube: {n} Playlists geladen – im Kasten auswählen':
        'YouTube：{n} 個の再生リストを読み込みました – ボックスで選択してください',
    'YouTube: keine Playlists auf dem Kanal – zuerst auf YouTube eine anlegen':
        'YouTube：チャンネルに再生リストがありません – 先に YouTube で作成してください',
    'YouTube: Playlists nicht geladen – {why}':
        'YouTube：再生リストを読み込めませんでした – {why}',
    'YouTube: {file} in Playlist „{name}“ einsortiert':
        'YouTube：{file} を再生リスト「{name}」に振り分けました',
    'YouTube: {file} hochgeladen, aber nicht in die Playlist – {why}':
        'YouTube：{file} はアップロードされましたが、再生リストには追加されませんでした – {why}',
    'Berechtigung fehlt – noch einmal „Mit YouTube verbinden“ klicken':
        '権限がありません – もう一度「YouTube に接続」をクリックしてください',
    'YouTube: verbunden – für Playlists einmal neu „Mit YouTube verbinden“ klicken.':
        'YouTube：接続済み – 再生リストを使うには、もう一度「YouTube に接続」をクリックしてください。',
    'Nach dem Upload kommt jedes Video in die gewählte Playlist – für Clips und Runden getrennt wählbar, beide dürfen dieselbe sein. Braucht bei Google die Berechtigung „YouTube-Konto verwalten“ statt nur „Videos hochladen“: nach dem Anhaken einmal neu „Mit YouTube verbinden“. Das Programm nutzt davon nur Playlists auflisten und Video einsortieren (50 Einheiten je Video; es bleiben sechs Uploads am Tag).':
        'アップロード後、各動画を選択した再生リストに追加します – クリップとラウンドで別々に設定でき、同じでもかまいません。「動画のアップロード」だけでなく Google の権限「YouTube アカウントの管理」が必要です：チェックを入れた後、もう一度「YouTube に接続」をクリックしてください。プログラムはこの権限を再生リストの一覧取得と動画の振り分けにのみ使用します（動画 1 本につき 50 ユニット。1 日 6 件のアップロードは引き続き可能です）。',
    'Holt die Liste deiner Playlists von YouTube (1 Einheit) in die beiden Auswahlfelder. Neue Playlists legst du auf YouTube an und lädst die Liste danach neu.':
        'YouTube から再生リストの一覧を取得し（1 ユニット）、2 つの選択肢に入れます。新しい再生リストは YouTube で作成してから、一覧を再度読み込んでください。',
    'YouTube: Fehler – {error}':
        'YouTube：エラー – {error}',
    'Jeder neue Clip (F8 und aus dem Editor) kommt in die Warteschlange und geht auf deinen Kanal, sobald du weder in einer Lobby noch in einer Runde bist – mit der Sichtbarkeit rechts, Standard privat. Runden lädst du nur auf Wunsch hoch (Rechtsklick unter Aufnahmen). Google erlaubt etwa sechs Uploads am Tag, der Rest wartet bis zum nächsten Tag. Die Datei bleibt auf der Platte.':
        '新しいクリップ（F8 とエディターから）はすべてキューに入り、ロビーにもラウンドにもいないときにチャンネルへアップロードされます – 公開設定は右の設定どおりで、既定は非公開です。ラウンドはリクエストした場合のみアップロードされます（「録画」で右クリック）。Google が許可するのは 1 日約 6 件のアップロードで、残りは翌日まで待機します。ファイルはディスクに残ります。',
    'Öffnet die Anmeldedaten der Google Cloud Console im Browser: Projekt anlegen, „YouTube Data API v3“ aktivieren, OAuth-Client „Desktop-App“ erstellen, Client-ID und -Secret hier einfügen.':
        'ブラウザーで Google Cloud コンソールの認証情報ページを開きます：プロジェクトを作成し、「YouTube Data API v3」を有効にし、OAuth クライアント「デスクトップ アプリ」を作成して、クライアント ID とシークレットをここに貼り付けてください。',
    'Vergisst die Google-Freigabe auf diesem PC; die Warteschlange wartet, bis du dich neu verbindest. In deinem Google-Konto unter Sicherheit → Drittanbieter-Apps lässt sich der Zugriff ebenfalls entfernen.':
        'この PC での Google の同意を破棄します。キューは再接続するまで待機します。Google アカウントの「セキュリティ」→「サードパーティ製アプリ」でもアクセスを削除できます。',
    'Die markierte Datei in die YouTube-Warteschlange (Sichtbarkeit wie in den Einstellungen, Standard privat). Hochgeladen wird, sobald du weder in einer Lobby noch in einer Runde bist und das Tageskontingent reicht; der Link erscheint danach im Rechtsklick-Menü.':
        '選択したファイルを YouTube のキューに入れます（公開設定は設定どおり、既定は非公開）。ロビーにもラウンドにもおらず、1 日の割り当てに余裕があればアップロードされ、その後リンクが右クリックメニューに表示されます。',
    'Spotify: Client-ID sieht falsch aus – erwartet werden 32 Zeichen aus 0–9 und a–f (Dashboard → deine App → Settings → Basic Information → Client ID).':
        'Spotify：クライアント ID が正しくないようです – 0～9 と a～f の 32 文字が必要です（ダッシュボード → アプリ → Settings → Basic Information → Client ID）。',
    'ALS NÄCHSTES':
        '次の曲',
    'Unter dem Lied':
        '曲の下',
    'Rechts neben dem Lied':
        '曲の右',
    'Als nächstes':
        '次の曲',
    'Anzahl Titel':
        '表示する曲数',
    'Die Liste kommt aus Spotify – einrichten unter Einstellungen → Verbindungen → Spotify.':
        'リストは Spotify から取得します – 「設定」→「接続」→「Spotify」で設定してください。',
    'Spotify: aus':
        'Spotify：オフ',
    'Spotify: Client-ID fehlt – im Developer-Dashboard anlegen und hier eintragen.':
        'Spotify：クライアント ID がありません – 開発者ダッシュボードで作成し、ここに入力してください。',
    'Spotify: nicht verbunden – „Mit Spotify verbinden“ klicken.':
        'Spotify：未接続 – 「Spotify に接続」をクリックしてください。',
    'Spotify: Anmeldung im Browser offen – dort bei Spotify anmelden und zustimmen …':
        'Spotify：ブラウザーでログイン画面を開いています – そこで Spotify にサインインして同意してください…',
    'Spotify: Port {port} ist belegt – Anmeldung nicht möglich.':
        'Spotify：ポート {port} は使用中です – ログインできません。',
    'Spotify: Browser konnte nicht geöffnet werden ({error})':
        'Spotify：ブラウザーを開けませんでした（{error}）',
    'Spotify: Anmeldung fehlgeschlagen ({error})':
        'Spotify：ログインに失敗しました（{error}）',
    'Spotify: Anmeldung abgelehnt ({error})':
        'Spotify：ログインが拒否されました（{error}）',
    'Spotify: keine Antwort vom Browser – Anmeldung abgebrochen.':
        'Spotify：ブラウザーから応答がありません – ログインをキャンセルしました。',
    'Spotify: verbunden':
        'Spotify：接続済み',
    'Spotify: Anmeldung abgelaufen – bitte neu verbinden.':
        'Spotify：ログインの有効期限が切れました – もう一度接続してください。',
    'Spotify: kein Zugriff ({error}) – ist dein Spotify-Konto in der Developer-App unter „User Management“ eingetragen?':
        'Spotify：アクセスできません（{error}）– 開発者アプリの「User Management」にお使いの Spotify アカウントが登録されていますか？',
    'Spotify: Fehler – {error}':
        'Spotify：エラー – {error}',
    'Spotify: Kontingent der Developer-App aufgebraucht – „Als nächstes“ pausiert bis {time}.':
        'Spotify：開発者アプリの割り当てを使い切りました – 「次の曲」は {time} まで一時停止します。',
    'keine Antwort mit Token':
        'トークンを含む応答がありません',
    'Mit Spotify verbunden – du kannst dieses Fenster schliessen.':
        'Spotify に接続しました – このウィンドウは閉じてかまいません。',
    'Spotify hat die Anmeldung abgelehnt – du kannst dieses Fenster schliessen.':
        'Spotify がログインを拒否しました – このウィンドウは閉じてかまいません。',
    'Die nächsten Titel deiner Spotify-Warteschlange unter oder neben dem laufenden Lied. Braucht eine eigene App im Spotify-Developer-Dashboard (Client-ID) und einmal die Anmeldung im Browser; nur solange Spotify spielt.':
        'Spotify のキューの次の曲を、現在の曲の下または横に表示します。Spotify 開発者ダッシュボードの独自のアプリ（クライアント ID）と、ブラウザーでの一度のログインが必要です。Spotify の再生中のみ。',
    'Öffnet developer.spotify.com/dashboard im Browser: „Create app“, Redirect URI wie unten angegeben eintragen, die Client-ID kopieren und links einfügen.':
        'ブラウザーで developer.spotify.com/dashboard を開きます：「Create app」で下に示したリダイレクト URI を入力し、クライアント ID をコピーして左に貼り付けてください。',
    'Vergisst die Spotify-Freigabe auf diesem PC; die Liste verschwindet. In Spotify selbst lässt sich die App unter Konto → Apps ebenfalls entfernen.':
        'この PC での Spotify の同意を破棄します。リストは消えます。Spotify 側でも「アカウント」→「アプリ」でアプリを削除できます。',
    'Alle Arten':
        'すべての種類',
    'Art':
        '種類',
    'Clip abspielen':
        'クリップを再生',
    'Clip im Editor öffnen …':
        'クリップをエディターで開く…',
    'Im Editor öffnen …':
        'エディターで開く…',
    'Datei kopieren (zum Einfügen)':
        'ファイルをコピー（貼り付け用）',
    'Zur Runde springen':
        'ラウンドへ移動',
    'Farming-Runde':
        'ファーミングラウンド',
    'Datei fehlt: {file}':
        'ファイルが見つかりません：{file}',
    '{file} kopiert – mit Strg+V z. B. in Discord einfügen.':
        '{file} をコピーしました – Ctrl+V で貼り付けられます（例：Discord に）。',
    'Die Aufnahme dieser Runde gibt es nicht mehr.':
        'このラウンドの録画はありません。',
    'ffmpeg fehlt (Paket imageio-ffmpeg) – start.bat installiert es beim nächsten Start.':
        'ffmpeg がありません（パッケージ imageio-ffmpeg）– start.bat が次回の起動時にインストールします。',
    'Öffnet den markierten Clip (auch Sofort-Clips von F8) im Clip-Editor: kürzen, zensieren, Ton mischen. Gespeichert wird ein neuer Clip, der alte bleibt.':
        '選択したクリップ（F8 のインスタントクリップも）をクリップエディターで開きます：トリミング、検閲、音声のミックス。新しいクリップとして保存され、元のクリップは残ります。',
    'Clip fehlt: {file}':
        'クリップが見つかりません：{file}',
    'Keine Videodatei: {file}':
        '動画ファイルではありません：{file}',
    'Clip gelöscht: {file}':
        'クリップを削除しました：{file}',
    'Clip im Explorer zeigen':
        'クリップをエクスプローラーで表示',
    'Clip löschen':
        'クリップを削除',
    'Clip nicht gelöscht ({error}): {file}':
        'クリップは削除されませんでした（{error}）：{file}',
    'Kein Aufnahmeordner – die Clips liegen in seinem Ordner „Clips“.':
        '録画フォルダーがありません – クリップはその「Clips」フォルダーに保存されます。',
    'Länge':
        '長さ',
    'Noch keine Clips – „Clip bearbeiten …“ bei einer Runde oder F8 im Spiel.':
        'まだクリップはありません – ラウンドで「クリップを編集…」、またはゲーム内で F8。',
    'Sofort-Clip':
        'インスタントクリップ',
    'Sofort-Clips (F8)':
        'インスタントクリップ（F8）',
    'Standbild':
        '静止画',
    'Standbilder':
        '静止画',
    '{n} von {total} Clips':
        '{total} 個中 {n} 個のクリップ',
    'Spielt den markierten Clip im Standard-Player von Windows ab.':
        '選択したクリップを Windows の既定のプレーヤーで再生します。',
    'Öffnet den Explorer mit dem markierten Clip.':
        '選択したクリップをエクスプローラーで開きます。',
    'Löscht den markierten Clip von der Platte – nach Rückfrage. Nur Dateien, die das Programm selbst angelegt hat.':
        '選択したクリップを確認後にドライブから削除します。プログラム自身が作成したファイルのみ。',
    'Öffnet den Ordner „Clips“ neben den Aufnahmen im Explorer.':
        '録画の隣にある「Clips」フォルダーをエクスプローラーで開きます。',
    'Clips':
        'クリップ',
    'Graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '帯の中の灰色の線 = 境界（オフ）– ドラッグするとオンになります',
    'mit kurzer Meldung':
        '短い通知付き',
    'Clip wird gespeichert …':
        'クリップを保存中…',
    'Die letzten {n} s aus dem Puffer von OBS':
        'OBS のバッファの直近 {n} 秒',
    'Clip gespeichert ✓':
        'クリップを保存しました ✓',
    '{n} s · im Tab Aufnahmen → Clips':
        '{n} 秒 · 「録画」→「クリップ」タブ',
    'Kein Clip':
        'クリップなし',
    'Zeigt beim Sofort-Clip (F8) unten rechts ein kleines Hinweisfenster – „Clip wird gespeichert …“ und danach „Clip gespeichert“ bzw. warum nicht. Auch im Spiel, ohne Ton; nimmt nie den Fokus.':
        'インスタントクリップ（F8）について、右下に小さな通知ウィンドウを表示します – 「クリップを保存中…」の後に「クリップを保存しました」、または保存できなかった理由。ゲーム内でも音なしで表示され、フォーカスを奪うことはありません。',
    'Grenzen oben und unten in den schwarzen Balken':
        '黒帯の上下の境界',
    'Grenzen zurücksetzen':
        '境界をリセット',
    'Links und rechts gleich':
        '左右同じ',
    'In jedem schwarzen Balken (links und rechts) eine Linie oben und eine unten: Karte, Systemwerte, Heute und Musik bleiben dazwischen – z. B. frei für eine FPS-Anzeige oder Benachrichtigungen. Die Karte wird bei Bedarf kleiner.':
        '各黒帯（左右）の上と下に 1 本ずつ線を引きます：マップ、システム値、今日、音楽はその間に収まります – 例：FPS カウンターや通知の場所を空けるために。必要に応じてマップは小さくなります。',
    'Eine Linie ziehen bewegt die gleiche Linie im anderen Balken mit.':
        '線をドラッグすると、もう一方の帯の同じ線も一緒に動きます。',
    'Setzt alle vier Linien auf 8 % vom Rand zurück.':
        '4 本の線をすべて端から 8 % の位置に戻します。',
    'Dunkelgrauer Boden mit hellem Rand – gilt auch im Spiel.':
        '明るい縁のダークグレーの床 – ゲーム内にも適用されます。',
    'Dunkelgrauer Boden – die Form der Map bleibt auf dem schwarzen Balken sichtbar. Gilt auch im Spiel.':
        'ダークグレーの床 – 黒帯の上でもマップの形が見えます。ゲーム内にも適用されます。',
    'Dunkles Lila mit lila Rand, erinnert an die Originalfarbe – gilt auch im Spiel.':
        'ライラックの縁のダークライラック、元の色に近い – ゲーム内にも適用されます。',
    'Durchsichtiger Boden mit dunklem Rand – gilt auch im Spiel.':
        '暗い縁の透ける床 – ゲーム内にも適用されます。',
    'Grau':
        'グレー',
    'Grau mit Rand':
        '縁付きグレー',
    'Lila dunkel':
        'ダークライラック',
    'Lila transparent':
        'ライラック（透過）',
    'Lila Boden, halb durchsichtig – gilt auch im Spiel.':
        'ライラックの床、半透明 – ゲーム内にも適用されます。',
    'Wichtig: In DBD unter Einstellungen → Grafik den Anzeigemodus „Fenster-Vollbild“ wählen. Im exklusiven Vollbild kann Windows kein Fenster über dem Spiel zeigen – die Karte bliebe unsichtbar.':
        '重要：DBD の「設定」→「グラフィック」で表示モード「ウィンドウフルスクリーン」を選択してください。排他的フルスクリーンでは、Windows はゲームの上にウィンドウを表示できず、マップが見えないままになります。',
    'Ungültiger Servername im Auftrag: {name}':
        'ジョブ内のサーバー名が無効です：{name}',
    'Die hosts-Datei wurde direkt nach dem Schreiben wieder verändert (Virenschutz oder ein anderes Programm?).':
        '書き込み直後に hosts ファイルが再び変更されました（ウイルス対策ソフトまたは他のプログラム？）。',
    'Keine Schreibrechte auf die hosts-Datei (Administratorrechte?).':
        'hosts ファイルを書き込む権限がありません（管理者権限？）。',
    'Aufbau der Match-Daten speichern':
        'マッチデータの構造を保存',
    'Öffnet die Stats-Seite so, dass das Userscript einmal den Aufbau ihrer Match-Daten im Download-Ordner speichert: nur Feldnamen und Arten, keine Werte. Damit lässt sich entscheiden, welche Daten das Programm zusätzlich auswerten könnte.':
        '統計ページを開き、ユーザースクリプトにマッチデータの構造を一度ダウンロードフォルダーに保存させます：フィールド名と型のみで、値は含みません。これでプログラムがさらにどのデータを使えるかがわかります。',
    'Die Stats-Seite öffnet sich im Browser. Das Userscript (ab Version {n}) legt danach „{file}“ in den Download-Ordner: nur die Namen und Arten der Felder, die die Seite liefert – keine Werte, keine Namen, keine IDs. Das Programm liest diese Datei nicht; du kannst sie weitergeben, um zu entscheiden, welche Felder zusätzlich übernommen werden sollen. Ältere Userscripts: vorher „Userscript kopieren“ und in Tampermonkey ersetzen.':
        '統計ページがブラウザーで開きます。ユーザースクリプト（バージョン {n} 以降）は「{file}」をダウンロードフォルダーに保存します：ページが送信するフィールドの名前と種類のみ – 値、名前、ID は含みません。プログラムはこのファイルを読み取りません。どのフィールドを追加で取り込むべきか判断するために、ファイルを渡すことができます。古いユーザースクリプト：先に「ユーザースクリプトをコピー」して Tampermonkey で置き換えてください。',
    'Gegner':
        '対戦相手',
    'Charakter':
        'キャラクター',
    'Begegnungen':
        '遭遇',
    'Geopfert':
        '生贄',
    'Getötet':
        '殺害',
    'Aufgegeben':
        '放棄',
    'Laut Stats-Seite: als Killer die Survivor gegen dich und wie ihr Match endete, als Survivor der Killer und wie dein Match endete. „Getötet“ = vom Killer direkt getötet (z. B. Mori), „Aufgegeben“ schließt verlassene Matches ein. „Ø Kills ohne Aufgaben“ zählt nur Matches, in denen kein Survivor aufgab oder ging. „Farming“ = Begegnungen in Farming-Runden, die „Begegnungen“ nicht zählen.':
        '統計ページより：キラーではあなたと対戦したサバイバーとそのマッチの結果、サバイバーではキラーとあなたのマッチの結果。「殺害」= キラーに直接殺害された（例：メメント・モリ）、「放棄」には途中退出したマッチも含みます。「クリーン平均キル」は、どのサバイバーも放棄・退出しなかったマッチのみを数えます。「ファーミング」= ファーミングラウンドでの遭遇で、「遭遇」には含まれません。',
    'Noch keine Runden mit Daten der Stats-Seite in dieser Auswahl.':
        'この選択範囲にはまだ統計ページのデータがあるラウンドがありません。',
    'Schnellste 4K':
        '最速 4K',
    '{n} von {total} Runden':
        '{total} ラウンド中 {n} ラウンド',
    '{n} Survivor':
        'サバイバー {n} 人',
    'Ø Kills ohne Aufgaben':
        'クリーン平均キル',
    'OBS mit DBD starten, falls es noch nicht läuft':
        'DBD の起動時に OBS が起動していなければ起動する',
    'Startet DBD und ist OBS nicht erreichbar, startet das Programm OBS einmal minimiert im Infobereich – nur, wenn kein OBS-Fenster offen ist. OBS bleibt offen, wenn DBD beendet wird. OBS läuft dann mit denselben Rechten wie das Programm (Administrator).':
        'DBD が起動して OBS に接続できない場合、プログラムは OBS を一度、通知領域に最小化した状態で起動します – OBS のウィンドウが開いていない場合のみ。DBD を閉じても OBS は開いたままです。OBS はプログラムと同じ権限（管理者）で実行されます。',
    'OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS は起動しましたが接続できません – OBS の「ツール」→「WebSocket サーバー設定」でサーバーを有効にし、ポート/パスワードを確認してください。（{error}）',
    'OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio).':
        'OBS が見つかりません – OBS を自分で起動してください（Program Files\\obs-studio を検索しました）。',
    'OBS konnte nicht gestartet werden: {error}':
        'OBS を起動できませんでした：{error}',
    'OBS wird gestartet …':
        'OBS を起動中…',
    'OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})':
        'OBS は開いていますが接続できません – OBS の「ツール」→「WebSocket サーバー設定」でサーバーを有効にし、ポート/パスワードを確認してください。（{error}）',
    'Builds':
        'ビルド',
    'Build (4 Perks)':
        'ビルド（パーク 4 つ）',
    'Perk':
        'パーク',
    'Add-on':
        'アドオン',
    'Opfergabe':
        'オファリング',
    'Kraft/Item':
        '能力/アイテム',
    'ohne':
        'なし',
    'Dein Loadout laut Stats-Seite (ab Userscript Version 3). „Ergebnis“ = als Killer Ø Kills, als Survivor Anteil entkommen; „ohne“ = dasselbe in deinen Runden derselben Rolle ohne diesen Eintrag. Builds ab {n} Runden. Embleme: Ø Stufe von keins (0) bis Iri (4); „voll“ = Kategorie mit {max} Punkten.':
        '統計ページのロードアウト（ユーザースクリプト バージョン 3 以降）。「結果」= キラーでは平均キル数、サバイバーでは脱出率。「なし」= その役割のラウンドのうち、この項目がないものでの同じ値。ビルドは {n} ラウンド以上から。エンブレム：平均ティアはなし（0）から虹（4）まで。「満点」= カテゴリーが {max} ポイント。',
    'Event-Modus':
        'イベントモード',
    'keins':
        'なし',
    'Bronze':
        'ブロンズ',
    'Silber':
        'シルバー',
    'Gold':
        'ゴールド',
    'Iri':
        '虹',
    'Emblem':
        'エンブレム',
    'Ø Stufe':
        '平均ティア',
    'Punktekategorie':
        'スコアカテゴリー',
    'Ø Punkte':
        '平均ポイント',
    'voll':
        '満点',
    'Killer-Wertung: {list}':
        'キラーの評価：{list}',
    'Noch keine Matches mit Loadout in dieser Auswahl – die Stats-Seite liefert es ab Userscript Version 3 (Einstellungen → Match-Daten → Offizielle Match-Daten → „Userscript kopieren“).':
        'この選択範囲にはまだロードアウトのあるマッチがありません – 統計ページはユーザースクリプト バージョン 3 以降でロードアウトを送信します（「設定」→「マッチデータ」→「公式マッチデータ」→「ユーザースクリプトをコピー」）。',
    'Alle Modi':
        'すべてのモード',
    '„{name}“ nicht mehr als Farming-Gegner':
        '「{name}」をファーミング仲間から外す',
    '„{name}“ als Farming-Gegner (Runden mit diesem Charakter zählen als Farming)':
        '「{name}」をファーミング仲間にする（このキャラクターとのラウンドはファーミングとして数えます）',
    '„{name}“ gilt jetzt als Farming-Gegner – {n} Runden zählen als Farming (auch ältere; Aufnahmen bleiben, wo sie sind).':
        '「{name}」をファーミング仲間として数えるようになりました – {n} ラウンドがファーミングとして数えられます（過去のものも。録画はそのままの場所にあります）。',
    '„{name}“ gilt nicht mehr als Farming-Gegner.':
        '「{name}」をファーミング仲間として数えなくなりました。',
    'Farming-Gegner (Rechtsklick auf einen Charakter im Reiter „Gegner“): {names}':
        'ファーミング仲間（「対戦相手」タブでキャラクターを右クリック）：{names}',
    'Gegner & Builds':
        '対戦相手とビルド',
    'Maps, Server & PC':
        'マップ、サーバー、PC',
    'Bloodpoints & Farming':
        'ブラッドポイントとファーミング',
    'Aufnahme markieren: abspielen, Clip schneiden, behalten, löschen – oder Rechtsklick.':
        '録画を選択：再生、クリップの切り出し、保持、削除 – または右クリック。',
    'Clip markieren: abspielen, im Editor öffnen, löschen – oder Rechtsklick.':
        'クリップを選択：再生、エディターで開く、削除 – または右クリック。',
    'Filter{count}':
        'フィルター{count}',
    'Filter zurücksetzen':
        'フィルターをリセット',
    'Alle Filter der Statistik zurück auf „alle“ – Zeitraum, Rolle, Region, Killer, Map, Modus und „Farming ausblenden“.':
        '統計のすべてのフィルターを「すべて」に戻します – 期間、役割、リージョン、キラー、マップ、モード、「ファーミングを除外」。',
    'Region, Killer, Map, Modus und „Farming ausblenden“ ein- oder ausklappen. Die Zahl sagt, wie viele davon gerade filtern.':
        'リージョン、キラー、マップ、モード、「ファーミングを除外」を表示/非表示にします。数字は現在いくつが絞り込みに使われているかを示します。',
    'Noch keine Runden gespeichert':
        '保存されたラウンドはまだありません',
    'Eine Runde zählt vom Map-Banner bis zum Rundenende (ab 1 Minute) und erscheint hier von selbst. Kills, Escapes und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'ラウンドはマップバナーからラウンド終了まで（1 分以上）を数え、ここに自動で表示されます。キル、脱出、ブラッドポイントは統計ページから取得します – そのためにマッチデータを一度設定してください。',
    'Noch keine Aufnahmen – OBS nimmt ab dem nächsten Map-Banner auf. Runden erscheinen hier, Clips (F8 oder aus dem Editor) im Reiter „Clips“.':
        'まだ録画はありません – OBS は次のマップバナーから録画します。ラウンドはここに、クリップ（F8 またはエディターから）は「クリップ」タブに表示されます。',
    'Runden pro Tag – letzte {n} Tage':
        '1 日あたりのラウンド – 過去 {n} 日間',
    '{when}: {n} Runden ({k} Killer, {s} Survivor)':
        '{when}：{n} ラウンド（キラー {k}、サバイバー {s}）',
    '1 s ab Abspielkopf':
        '再生ヘッドから 1 秒',
    '10 s ab Abspielkopf':
        '再生ヘッドから 10 秒',
    '100 % = unverändert.':
        '100 % = 変更なし。',
    '3 s ab Abspielkopf':
        '再生ヘッドから 3 秒',
    '5 s ab Abspielkopf':
        '再生ヘッドから 5 秒',
    '9:16 (Hochformat)':
        '9:16（縦向き）',
    'Alle Bilder':
        'すべての画像',
    'Alle Zeichnungen entfernen':
        'すべての描画を削除',
    'Alles zurücksetzen':
        'すべてリセット',
    'Anderen Ordner …':
        '別のフォルダー…',
    'Aufgenommen (F12)':
        '撮影（F12）',
    'Ausschnitt':
        '切り抜き',
    'Ausschnitt {w}×{h}':
        '切り抜き {w}×{h}',
    'Bearbeitet':
        '編集済み',
    'Bearbeitete Bilder öffnen':
        '編集済みの画像を開く',
    'Bild bearbeiten – {name}':
        '画像を編集 – {name}',
    'Bild bearbeiten …':
        '画像を編集…',
    'Bild gespeichert: {file}':
        '画像を保存しました：{file}',
    'Bild im Explorer zeigen':
        '画像をエクスプローラーで表示',
    'Bild nicht gespeichert: {error}':
        '画像は保存されませんでした：{error}',
    'Speichert …':
        '保存中…',
    'Bild nicht lesbar: {error}':
        '画像を読み取れません：{error}',
    'Bild speichern':
        '画像を保存',
    'Der Clip beginnt aus Schwarz und mit leisem Ton.':
        'クリップは黒から始まり、音声が徐々に大きくなります。',
    'Der Clip endet in Schwarz, der Ton wird leiser.':
        'クリップは黒で終わり、音声がフェードアウトします。',
    'Dick':
        '太い',
    'Dünn':
        '細い',
    'Eigener Ordner':
        '独自のフォルダー',
    'Eigener Ordner nicht gefunden: {path}':
        '独自のフォルダーが見つかりません：{path}',
    'Einblenden':
        'フェードイン',
    'Entfernt den markierten Kasten (Entf).':
        '選択した枠を削除します（Del）。',
    'Entfernt die markierte Zeichnung (Entf).':
        '選択した描画を削除します（Del）。',
    'Farbe':
        '色',
    'Farbe zurücksetzen':
        '色をリセット',
    'Frei':
        '自由',
    'Freihand':
        'フリーハンド',
    'GIF (ohne Ton, für Chats)':
        'GIF（音声なし、チャット用）',
    'GIF {h}p, {fps} Bilder/s, ohne Ton':
        'GIF {h}p、{fps} フレーム/秒、音声なし',
    'Helligkeit':
        '明るさ',
    'Helligkeit, Kontrast und Sättigung auf 100 %.':
        '明るさ、コントラスト、彩度を 100 % に戻します。',
    'Höhe des GIFs – kleiner = kleinere Datei (Discord, Chats).':
        'GIF の高さ – 小さいほどファイルも小さくなります（Discord、チャット）。',
    'Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten vergrössern.':
        '画像上で読めなくする領域をドラッグしてください – 名前、チャット、フレンドリスト。枠は移動でき、右下の角でサイズを変更できます。',
    'Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert sie, ziehen verschiebt sie, Entf löscht sie.':
        '画像上でドラッグしてください（テキスト：クリック）。描画をクリックで選択、ドラッグで移動、Del で削除。',
    'Immer':
        '常に',
    'In Zwischenablage':
        'クリップボードへ',
    'In die Zwischenablage kopiert – in Discord mit Strg+V einfügen.':
        'クリップボードにコピーしました – Discord で Ctrl+V で貼り付けられます。',
    'Ohne schwarze Ränder':
        '黒帯なし',
    'Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das Spielbild, „Kein Ausschnitt“ das ganze Bild.':
        '録画に黒帯があります：「黒帯なし」はゲーム画面のみを、「切り抜きなし」は画像全体を保存します。',
    'Kein Ausschnitt':
        '切り抜きなし',
    'Kein Screenshot-Ordner von Steam für DBD gefunden – noch kein F12-Screenshot, oder Steam speichert woanders („Anderen Ordner …“).':
        'DBD の Steam スクリーンショットフォルダーが見つかりません – まだ F12 のスクリーンショットがないか、Steam が別の場所に保存しています（「別のフォルダー…」）。',
    'Kontrast':
        'コントラスト',
    'Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C).':
        '編集した画像をコピーします – Discord で Ctrl+V で貼り付けられます（Ctrl+C）。',
    'Kreis':
        '楕円',
    'Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg 1 Bild · I/O Start/Ende · A Abschnitt · M Marke · Pos1/Ende Anfang/Schluss · Entf Kasten/Zeichnung weg · Esc schliessen':
        'スペース 再生 · ←/→ 1 秒 · Shift 5 秒 · Ctrl 1 フレーム · I/O 開始/終了 · A 区間 · M マーク · Home/End 先頭/末尾 · Del 枠/描画を削除 · Esc 閉じる',
    'Letzten Schritt zurücknehmen (Strg+Z).':
        '最後の操作を元に戻します（Ctrl+Z）。',
    'Linie':
        '線',
    'Links und rechts tauschen.':
        '左右を入れ替えます。',
    'Mittel':
        '中',
    'Oben und unten tauschen.':
        '上下を入れ替えます。',
    'Ordner mit deinen Screenshots':
        'スクリーンショットのフォルダー',
    'Ordner nicht anlegbar: {error}':
        'フォルダーを作成できません：{error}',
    'PNG: verlustfrei · JPG: kleinere Datei.':
        'PNG：可逆圧縮 · JPG：ファイルが小さい。',
    'Pfeil':
        '矢印',
    'Rahmen':
        '枠',
    'Rahmen bearbeiten':
        'フレームを編集',
    'Rahmen im Bild ziehen, verschieben, an den Ecken ändern.':
        '画像上でフレームをドラッグし、移動し、角で変更します。',
    'Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. Nochmal drücken beendet das Werkzeug.':
        'プレビューでフレームを移動するか、角をドラッグして拡大/縮小してください。もう一度押すとツールを終了します。',
    'Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen.':
        '画像の一部を切り抜きます – YouTube ショートと TikTok には 9:16、Instagram には 1:1。プレビューでフレームを移動し、角をドラッグしてください。',
    'Screenshots':
        'スクリーンショット',
    'Sehr dick':
        '極太',
    'Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den Ecken ziehen.':
        '切り抜きの縦横比。画像上でフレームを移動し、角をドラッグしてください。',
    'Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im Screenshot-Ordner von Steam) bleibt unverändert (Strg+S).':
        '編集したコピーを Fog Scout のフォルダーに保存します – オリジナル（例：Steam のスクリーンショットフォルダー内）はそのままです（Ctrl+S）。',
    'Steam (F12)':
        'Steam（F12）',
    'Steam-Ordner verwenden':
        'Steam のフォルダーを使用',
    'Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf Markiertes löschen · Esc schliessen':
        'Ctrl+Z 元に戻す · Ctrl+Y やり直し · Ctrl+C コピー · Ctrl+S 保存 · Del 選択したものを削除 · Esc 閉じる',
    'Strichstärke bzw. Textgrösse.':
        '線の太さまたは文字サイズ。',
    'Sättigung':
        '彩度',
    'Tempo':
        '速度',
    'Text':
        'テキスト',
    'Text für das Text-Werkzeug':
        'テキストツール用の文字',
    'Um 90° gegen den Uhrzeigersinn drehen.':
        '左に 90° 回転します。',
    'Um 90° im Uhrzeigersinn drehen.':
        '右に 90° 回転します。',
    'Verwirft alle Änderungen – das Original bleibt ohnehin unverändert.':
        'すべての変更を破棄します – いずれにせよオリジナルはそのままです。',
    'Wie der Bereich unkenntlich wird.':
        '領域を読めなくする方法。',
    'Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des Abspielkopfs. Gilt für neue und für die markierte Zeichnung.':
        '描画がクリップ内に表示される時間 – 再生ヘッドの位置から。新しい描画と選択した描画に適用されます。',
    'Zeichnen':
        '描画',
    'Zeichnung entfernen':
        '描画を削除',
    'Zeigt das zuletzt gespeicherte Bild im Explorer.':
        '最後に保存した画像をエクスプローラーで表示します。',
    'Zurückgenommenen Schritt wiederholen (Strg+Y).':
        '元に戻した操作をやり直します（Ctrl+Y）。',
    'Zuschneiden':
        'トリミング',
    'neu kodiert (wie „Genau“)':
        '再エンコード（「正確」と同様）',
    'normal':
        '通常',
    '{n} Abschnitt(e), {length} s':
        '{n} 区間、{length} 秒',
    '{w} × {h} Pixel · Original bleibt unverändert':
        '{w} × {h} ピクセル · オリジナルはそのまま',
    '↶ Rückgängig':
        '↶ 元に戻す',
    '↷ Wiederholen':
        '↷ やり直し',
    '⇅ Kippen':
        '⇅ 上下反転',
    '⇆ Spiegeln':
        '⇆ 左右反転',
    '⟲ Links drehen':
        '⟲ 左に回転',
    '⟳ Rechts drehen':
        '⟳ 右に回転',
    'Öffnet das markierte Bild im Bild-Editor: zuschneiden, drehen, Pfeile und Text, zensieren, Farbe – gespeichert wird eine Kopie, das Original bleibt.':
        '選択した画像を画像エディターで開きます：切り抜き、回転、矢印とテキスト、検閲、色 – コピーが保存され、オリジナルは残ります。',
    'Zeigt die Bilddatei im Explorer.':
        '画像ファイルをエクスプローラーで表示します。',
    'Öffnet den Ordner mit den bearbeiteten Bildern (Screenshots neben den Aufnahmen bzw. Bilder/Fog Scout).':
        '編集した画像のフォルダーを開きます（録画の隣の Screenshots、または ピクチャ/Fog Scout）。',
    'Bilder aus einem eigenen Ordner zeigen – z. B. wenn Steam die Screenshots unkomprimiert in einen anderen Ordner speichert.':
        '独自のフォルダーの画像を表示します – 例：Steam が非圧縮のスクリーンショットを別のフォルダーに保存する場合。',
    'Wieder die Screenshots aus Steams Ordner für DBD zeigen (F12 im Spiel).':
        'Steam の DBD フォルダーのスクリーンショット（ゲーム内で F12）を再び表示します。',
    'Bild anklicken: bearbeiten (zuschneiden, zeichnen, zensieren), im Explorer zeigen – Doppelklick öffnet den Editor.':
        '画像をクリック：編集（切り抜き、描画、検閲）、エクスプローラーで表示 – ダブルクリックでエディターが開きます。',
    'F12 im Spiel ist Steams Screenshot-Taste; das Programm liest Steams Ordner nur. Bearbeitete Bilder sind Kopien im Ordner „Screenshots“ neben den Aufnahmen.':
        'ゲーム内の F12 は Steam のスクリーンショットキーです。プログラムは Steam のフォルダーを読み取るだけです。編集した画像は、録画の隣の「Screenshots」フォルダーにコピーとして保存されます。',
    '1 Bild':
        '1 枚の画像',
    '{n} Bilder':
        '{n} 枚の画像',
    '★ behalten (nie aufgeräumt) · ⚑ Marken (F8 in der Runde) · ▶ auf YouTube · Rechtsklick auf die Spaltenköpfe: Spalten ein-/ausblenden':
        '★ 保持（自動削除しない）· ⚑ マーク（ラウンド中に F8）· ▶ YouTube にあり · 見出しを右クリック：列の表示/非表示',
    'Clips aus dem Editor, Sofort-Clips (F8) und Standbilder, mit ihrer Runde · ▶ auf YouTube · gelöscht werden nur Dateien, die das Programm selbst angelegt hat':
        'エディターのクリップ、インスタントクリップ（F8）、静止画をそのラウンドとともに表示 · ▶ YouTube にあり · 削除されるのはプログラム自身が作成したファイルのみ',
    'Status':
        '状態',
    'Schnell (ohne Neukodieren)':
        '高速（再エンコードなし）',
    'Genau (neu kodiert)':
        '正確（再エンコード）',
    'Für Discord (Zielgrösse)':
        'Discord 用（目標サイズ）',
    'GIF (ohne Ton)':
        'GIF（音声なし）',
    'Ein GIF ist höchstens {limit} s lang, dieser Clip {seconds} s – kürzer schneiden oder als Video speichern.':
        'GIF は最大 {limit} 秒ですが、このクリップは {seconds} 秒です – 短くカットするか、動画として保存してください。',
    'beim Beenden abgebrochen':
        'プログラムの終了時に停止',
    'Update gesperrt: ein Clip wird noch gespeichert. Danach noch einmal auf „Aktualisieren und neu starten“ klicken.':
        'アップデートはロック中です：クリップを保存中です。その後もう一度「アップデートして再起動」をクリックしてください。',
    '(gerade {n})':
        '（現在 {n}）',
    'Aufnahme gestartet':
        '録画を開始しました',
    'Aufnahme läuft weiter':
        '録画を再開しました',
    'Aufnahme läuft weiter.':
        '録画を再開しました。',
    'Aufnahme pausieren/weiter':
        '録画を一時停止/再開',
    'Aufnahme pausiert':
        '録画を一時停止しました',
    'Aufnahme pausiert.':
        '録画を一時停止しました。',
    'Aufnahme starten':
        '録画を開始',
    'Aufnahme starten/stoppen':
        '録画を開始/停止',
    'Aufnahme stoppen':
        '録画を停止',
    'Aufnahme von Hand gestartet.':
        '手動で録画を開始しました。',
    'Aufnahme wird beendet …':
        '録画を停止中…',
    'Aufnahme-Laufwerk fast voll – Aufnahme beendet':
        '録画ドライブがほぼいっぱいです – 録画を停止しました',
    'Aufnahme-Laufwerk fast voll – nichts gestartet':
        '録画ドライブがほぼいっぱいです – 何も開始しませんでした',
    'Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet':
        '録画ドライブが接続されていません – 何も開始しませんでした',
    'Aufnahmen sind aus.':
        '録画はオフです。',
    'Ausgewogen':
        'バランス',
    'Automatisch':
        '自動',
    'Bereit':
        '準備完了',
    'Bildhöhe des Clips – kleiner als die Aufnahme verkleinert, nie vergrössert.':
        'クリップの映像の高さ – 録画より小さい場合は縮小し、拡大はしません。',
    'CPU (x264/x265)':
        'CPU（x264/x265）',
    'Clip speichern (F8)':
        'クリップを保存（F8）',
    "Der Sofort-Clip (F8) ist auf {clip} s eingestellt, OBS' Wiederholungspuffer hält nur {buf} s – in OBS: Einstellungen → Ausgabe → Wiederholungspuffer → Maximale Wiederholungszeit.":
        'インスタントクリップ（F8）は {clip} 秒に設定されていますが、OBS のリプレイバッファは {buf} 秒しか保持しません – OBS で：「設定」→「出力」→「リプレイバッファ」→「最大リプレイ時間」。',
    'Die Datei erscheint im Tab Aufnahmen':
        'ファイルは「録画」タブに表示されます',
    'Es läuft schon eine Aufnahme':
        '既に録画が実行中です',
    'H.264 spielt überall; HEVC (H.265) ist bei gleicher Qualität etwa ein Drittel kleiner, braucht aber einen neueren Player.':
        'H.264 はどこでも再生できます。HEVC（H.265）は同じ品質で約 3 分の 1 小さくなりますが、新しいプレーヤーが必要です。',
    'Hoch':
        '高',
    'Kein Aufnahmeordner gewählt – Einstellungen → Aufnahmen.':
        '録画フォルダーが選択されていません – 「設定」→「録画」。',
    'Keine Aufnahme':
        '録画なし',
    'Keine Aufnahme läuft':
        '録画は実行されていません',
    'Keine Aufnahme läuft.':
        '録画は実行されていません。',
    'Kodiere {file} … ({how}, dauert etwas)':
        '{file} をエンコード中…（{how}、少し時間がかかります）',
    'Kodierung':
        'エンコード',
    'Marke setzen':
        'マークを設定',
    'Nimmt auf':
        '録画中',
    'Nimmt auf (von Hand gestartet)':
        '録画中（手動で開始）',
    'Nimmt die Runde in der laufenden Aufnahme auf':
        '実行中の録画内でラウンドを録画中',
    'OBS lässt Bilder aus ({n} von {total}, Kodierer überlastet) – in OBS Voreinstellung oder Auflösung senken.':
        'OBS がフレームをスキップしています（{total} 中 {n}、エンコーダーの過負荷）– OBS でプリセットまたは解像度を下げてください。',
    'OBS nicht erreichbar':
        'OBS に接続できません',
    'OBS starten, WebSocket-Server einschalten, Port/Passwort prüfen (Einstellungen → Verbindungen → OBS-Verbindung → Verbindung testen). {why}':
        'OBS を起動し、WebSocket サーバーを有効にして、ポート/パスワードを確認してください（「設定」→「接続」→「OBS 接続」→「接続をテスト」）。{why}',
    'OBS verpasst Bilder beim Rendern ({n} von {total}, Grafikkarte ausgelastet).':
        'OBS がレンダリング中にフレームを落としています（{total} 中 {n}、グラフィックカードが高負荷）。',
    'Pause':
        '一時停止',
    'Pausiert':
        '一時停止中',
    'Schnell':
        '高速',
    'Schnell: kleiner und schneller, sichtbar weicher. Ausgewogen: wie bisher. Hoch: grösser, nahe am Original.':
        '高速：小さく速いが、目に見えて柔らかくなります。バランス：従来どおり。高：大きく、オリジナルに近い。',
    'Stoppen mit demselben Hotkey oder im Tab Aufnahmen':
        '同じホットキーまたは「録画」タブで停止します',
    'Warte auf OBS …':
        'OBS を待機中…',
    'Wie aufgenommen':
        '録画したまま',
    'Wiederholungspuffer aus':
        'リプレイバッファ オフ',
    'Wiederholungspuffer in OBS nicht aktiviert':
        'OBS でリプレイバッファが有効になっていません',
    'Womit der Clip kodiert wird: die Grafikkarte (NVENC, AMF, Quick Sync – nur, wenn ffmpeg sie hier wirklich ansprechen kann) belastet den Prozessor kaum; „Automatisch“ nimmt die erste, die geht.':
        'クリップをエンコードするもの：グラフィックカード（NVENC、AMF、Quick Sync – ここで ffmpeg が実際に使える場合のみ）はプロセッサーにほとんど負荷をかけません。「自動」は最初に動作したものを使用します。',
    'letzter Clip {file} (vor {age})':
        '前回のクリップ {file}（{age} 前）',
    'Fortsetzen':
        '再開',
    'von Hand gestartet':
        '手動で開始',
    'von OBS selbst gestartet':
        'OBS 自体で開始',
    'Beendet die laufende Aufnahme jetzt (bei einer Runde ohne Nachlauf) und legt sie in den Aufnahmeordner.':
        '実行中の録画を今すぐ停止し（余白なしのラウンド）、録画フォルダーに保存します。',
    'Hält die laufende Aufnahme an (OBS pausiert); „Fortsetzen“ setzt sie in derselben Datei fort. Marken bleiben an ihrer Stelle.':
        '実行中の録画を一時停止します（OBS が一時停止）。「再開」で同じファイルに続けて録画します。マークの位置は保たれます。',
    'Merkt diesen Moment in der laufenden Aufnahme (⚑) – der Clip-Editor springt später dorthin. Ohne Sofort-Clip.':
        '実行中の録画にこの瞬間を記録します（⚑）– 後でクリップエディターがそこへジャンプします。インスタントクリップは作成しません。',
    'Setzt die pausierte Aufnahme fort.':
        '一時停止中の録画を再開します。',
    'Startet jetzt eine OBS-Aufnahme von Hand – auch ausserhalb einer Runde. Sie läuft, bis du sie stoppst oder DBD beendet wird; ein Map-Banner benennt sie. Hotkey einstellbar.':
        '今すぐ手動で OBS の録画を開始します – ラウンド外でも可能です。停止するか DBD を閉じるまで続き、マップバナーで名前が付きます。ホットキーは設定可能です。',
    'Wie F8: speichert die letzten Sekunden aus dem OBS-Wiederholungspuffer als Sofort-Clip (Länge unter Einstellungen → Aufnahmen) und setzt eine Marke, falls eine Aufnahme läuft.':
        'F8 と同様：OBS のリプレイバッファの直近の数秒をインスタントクリップとして保存し（長さは「設定」→「録画」で）、録画が実行中ならマークを設定します。',
    '1 Eintrag':
        '1 件',
    '{n} Einträge':
        '{n} 件',
    '5 Sekunden vor (Shift+→).':
        '5 秒進む（Shift+→）。',
    '5 Sekunden zurück (Shift+←).':
        '5 秒戻る（Shift+←）。',
    'Auf der Zeitleiste öffnen':
        'タイムラインで開く',
    'Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s':
        '録画 {start} – {end} · タイムライン上で {at} から · {length} 秒',
    'Auswahl':
        '選択',
    'Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).':
        '領域をぼかします – 名前、チャット、フレンドリスト（X）。',
    'Bibliothek':
        'ライブラリ',
    'Bibliothek ein-/ausblenden.':
        'ライブラリを表示/非表示にします。',
    'Bildausschnitt – den Rahmen in der Vorschau ziehen (C).':
        '切り抜き – ビューアーでフレームをドラッグします（C）。',
    'Clip entfernt – die Aufnahme bleibt, wie sie ist.':
        'クリップを削除しました – 録画はそのままです。',
    'Clip geteilt – jetzt {n} Clips.':
        'クリップを分割しました – 現在 {n} クリップ。',
    'Clip {n} von {total}':
        'クリップ {n} / {total}',
    'Clips auf der Zeitleiste wählen, verschieben und trimmen (V).':
        'タイムライン上でクリップを選択、移動、トリミングします（V）。',
    'Den ganzen Schnitt einpassen (Strg+0).':
        'カット全体を表示します（Ctrl+0）。',
    'Der Clip unter dem Abspielkopf beginnt hier (Taste I).':
        '再生ヘッドの下のクリップがここから始まります（キー I）。',
    'Der Clip unter dem Abspielkopf endet hier (Taste O).':
        '再生ヘッドの下のクリップがここで終わります（キー O）。',
    'Diese Aufnahme ist schon auf der Zeitleiste.':
        'この録画は既にタイムライン上にあります。',
    'Ein Bild vor (Strg+→); → eine Sekunde.':
        '1 フレーム進む（Ctrl+→）。→ で 1 秒。',
    'Ein Bild zurück (Strg+←); ← eine Sekunde.':
        '1 フレーム戻る（Ctrl+←）。← で 1 秒。',
    'Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt.':
        '選択したクリップをタイムラインから削除します（Del）– 録画は残ります。',
    'Export':
        'エクスポート',
    'Exportieren':
        'エクスポート',
    'Fog Scout · Editor':
        'Fog Scout · エディター',
    'Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze.':
        'ここでは分割するものがありません – 再生ヘッドがクリップの端にあります。',
    'Hier teilen':
        'ここで分割',
    'Inspector':
        'インスペクター',
    'Inspector ein-/ausblenden.':
        'インスペクターを表示/非表示にします。',
    'Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine andere Videodatei.':
        '録画がありません – OBS の録画とクリップがここに表示されます。「インポート」で別の動画ファイルを取り込めます。',
    'Keine Clips auf der Zeitleiste.':
        'タイムラインにクリップがありません。',
    'Kürzeste zuerst':
        '短い順',
    'Lautstärke der Vorschau (nicht des Clips).':
        'プレビューの音量（クリップの音量ではありません）。',
    '? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export':
        '? すべてのショートカット · スペース 再生 · ←/→ 1 秒 · Shift 5 秒 · Ctrl または ,/. 1 フレーム · I/O クリップの開始/終了をここに · S 分割 · Del 削除 · Ctrl+Z/Y 元に戻す/やり直し · F フルスクリーン · Ctrl+S プロジェクト · Ctrl+E エクスポート',
    'Längste zuerst':
        '長い順',
    'Löschen':
        '削除',
    'Name A–Z':
        '名前 A–Z',
    'Name des Projekts – auch der Name des exportierten Clips.':
        'プロジェクトの名前 – エクスポートしたクリップの名前にもなります。',
    'Neueste zuerst':
        '新しい順',
    'Pause (Leertaste)':
        '一時停止（スペース）',
    'Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D).':
        '画像に矢印、枠、フリーハンド、テキストを描きます（D）。',
    'Projekt':
        'プロジェクト',
    'Projekt geladen: {name}':
        'プロジェクトを読み込みました：{name}',
    'Projekt gespeichert: {file}':
        'プロジェクトを保存しました：{file}',
    'Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten.':
        'プロジェクトを保存します（Ctrl+S）– この録画のカット、切り抜き、描画、検閲、エクスポート設定を、後で続けられるように。',
    'Runde':
        'ラウンド',
    'Rückgängig (Strg+Z).':
        '元に戻す（Ctrl+Z）。',
    'Rückgängig.':
        '元に戻しました。',
    'Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen (Strg+E) – Format und Kodierung im Inspector unter Export.':
        'カットをクリップとして録画の隣の「Clips」フォルダーに書き込みます（Ctrl+E）– 形式とエンコードはインスペクターの「エクスポート」で。',
    'Sichtbar':
        '表示',
    'Sortierung der Bibliothek.':
        'ライブラリの並び順。',
    'Spielt den ganzen Schnitt von vorn ab und springt danach zurück.':
        'カット全体を最初から再生し、その後元の位置に戻ります。',
    'Standbild am Abspielkopf als PNG neben den Clips speichern.':
        '再生ヘッドの位置の静止画を PNG としてクリップの隣に保存します。',
    'Stärke':
        '太さ',
    'Teilen':
        '分割',
    'Teilt den Clip unter dem Abspielkopf in zwei (Taste S).':
        '再生ヘッドの下のクリップを 2 つに分割します（キー S）。',
    'Ton der Vorschau an/aus (Windows).':
        'プレビューの音声 オン/オフ（Windows）。',
    'Videodatei importieren':
        '動画ファイルをインポート',
    'Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie eine Aufnahme öffnen.':
        '動画ファイルをインポートします – ライブラリに表示され、録画と同様に開けます。',
    'Videos':
        '動画',
    'Vollbild – nur die Vorschau (F, Esc beendet).':
        'フルスクリーン – ビューアーのみ（F、Esc で終了）。',
    'Wiederholen (Strg+Y).':
        'やり直し（Ctrl+Y）。',
    'Wiederholt.':
        'やり直しました。',
    'Zeitleiste':
        'タイムライン',
    'Zeitleiste ein-/ausblenden.':
        'タイムラインを表示/非表示にします。',
    'Zeitleiste einpassen':
        'タイムラインを合わせる',
    'Zeitleiste herauszoomen (−, Strg+Mausrad).':
        'タイムラインを縮小します（−、Ctrl+ホイール）。',
    'Zeitleiste hineinzoomen (+, Strg+Mausrad).':
        'タイムラインを拡大します（+、Ctrl+ホイール）。',
    'Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit.':
        '選択したクリップのスローモーションまたは早送り。音声も追従します。',
    'Zum Anfang (Pos1).':
        '先頭へ（Home）。',
    'Zum Ende (Ende).':
        '末尾へ（End）。',
    '{at} liegt in keinem Clip der Zeitleiste.':
        '{at} はタイムラインのどのクリップにも含まれていません。',
    '{n} Clip(s) · {length} s':
        '{n} クリップ · {length} 秒',
    'Älteste zuerst':
        '古い順',
    'Öffnen aus der Bibliothek ist hier nicht verfügbar.':
        'ここではライブラリから開くことはできません。',
    'Fehler in {step} – siehe Log.':
        '{step} でエラー – ログを参照。',
    'Strg+{n}':
        'Ctrl+{n}',
    'Tastenkürzel':
        'キーボードショートカット',
    'Schliessen (? oder Esc)':
        '閉じる（? または Esc）',
    'Wiedergabe':
        '再生',
    'Werkzeuge':
        'ツール',
    'Leertaste':
        'スペース',
    'Abspielen / Anhalten':
        '再生 / 一時停止',
    '1 Sekunde zurück / vor':
        '1 秒戻る / 進む',
    'Shift+← / →':
        'Shift+← / →',
    '5 Sekunden zurück / vor':
        '5 秒戻る / 進む',
    'Strg+← / →  ·  , / .':
        'Ctrl+← / →  ·  , / .',
    '1 Bild zurück / vor':
        '1 フレーム戻る / 進む',
    'Pos1 / Ende':
        'Home / End',
    'Zum Anfang / zum Schluss':
        '先頭へ / 末尾へ',
    'Zur nächsten Marke':
        '次のマークへ',
    'Untertitel {a}–{b}.':
        '字幕 {a}–{b}。',
    '{file} wartet – {n} Export(e) davor.':
        '{file} は待機中 – 前に {n} 件のエクスポートがあります。',
    'Kodiere {file} …':
        '{file} をエンコード中…',
    'Titel & Vorschaubild':
        'タイトルとサムネイル',
    'Claude fragt: {question}':
        'Claude からの質問：{question}',
    'Deine Antwort …':
        '回答…',
    'Name der Vorlage':
        'テンプレート名',
    'Als Vorlage speichern':
        'テンプレートとして保存',
    'Merkt sich die eben übernommenen Schritte (ohne Zensurkästen) als Vorlage – Zeiten vom Anfang bzw. vom Ende aus, damit sie auch bei anderen Längen passen.':
        '今行った手順（検閲枠を除く）をテンプレートとして保存します – 時間は先頭または末尾からの値なので、他の長さにも合います。',
    'Schlägt die Schritte der Vorlage für diesen Schnitt vor – ohne Claude, kostenlos; erst „Übernehmen“ ändert den Schnitt.':
        'このカットに対してテンプレートの手順を提案します – Claude なし、無料。カットが変わるのは「適用」したときだけです。',
    'Vorlage löschen':
        'テンプレートを削除',
    'Entfernt die gewählte Vorlage.':
        '選択したテンプレートを削除します。',
    'Bitte einen Namen für die Vorlage eingeben.':
        'テンプレートの名前を入力してください。',
    'Nichts, was als Vorlage taugt (Zensurkästen gehören nicht dazu).':
        'テンプレートにできるものがありません（検閲枠はテンプレートに含まれません）。',
    'Vorlage „{name}“ gespeichert.':
        'テンプレート「{name}」を保存しました。',
    'Vorlage „{name}“':
        'テンプレート「{name}」',
    'Vorlage „{name}“ gelöscht.':
        'テンプレート「{name}」を削除しました。',
    'Schickt dieselben acht Standbilder wie „Export prüfen“ an Claude; Claude wählt das beste Vorschaubild und schlägt einen Titel vor. Den Titel übernimmst du selbst, das Vorschaubild wird nur als Bild in „Clips“ gespeichert – nichts wird hochgeladen.':
        '「エクスポートを確認」と同じ 8 枚の静止画を Claude に送信します。Claude が最適なサムネイルを選び、タイトルを提案します。タイトルは自分で採用し、サムネイルは「Clips」に画像として保存されるだけです – 何もアップロードされません。',
    'Claude sucht unter {n} Standbildern ein Vorschaubild …':
        'Claude が {n} 枚の静止画からサムネイルを選んでいます…',
    'Als Short-Titel: „{title}“':
        'ショートのタイトルとして：「{title}」',
    'Übernimmt den Titel als Titel des Shorts (ein Schritt zum Rückgängigmachen). Für YouTube kopierst du ihn selbst.':
        'このタイトルをショートのタイトルとして採用します（1 ステップで元に戻せます）。YouTube 用には自分でコピーしてください。',
    'Vorschaubild bei {at} speichern':
        '{at} のサムネイルを保存',
    'Speichert dieses Standbild in voller Grösse als PNG in „Clips“ – zensiert wie im Export, mit dem Titel. Hochgeladen wird nichts.':
        'この静止画をフルサイズの PNG として「Clips」に保存します – エクスポートと同様に検閲し、タイトル付き。何もアップロードされません。',
    'Short-Titel übernommen.':
        'ショートのタイトルを採用しました。',
    'Vorschaubild':
        'サムネイル',
    'Export prüfen':
        'エクスポートを確認',
    'Schickt acht Standbilder des fertigen Schnitts (Bildausschnitt wie im Export, bereits zensierte Bereiche zensiert) an Claude; Claude meldet noch lesbare Namen oder Chat und anderes, das so nicht geteilt werden sollte. Ein Klick auf einen Fund springt hin und schlägt einen Zensurkasten vor.':
        '完成したカットの静止画 8 枚（エクスポートと同様に切り抜き、検閲した領域は検閲済み）を Claude に送信します。Claude は、まだ読める名前やチャット、その他このまま共有すべきでないものを報告します。指摘をクリックするとその場所へジャンプし、検閲枠を提案します。',
    'Claude prüft {n} Standbilder des fertigen Schnitts …':
        'Claude が完成したカットの静止画 {n} 枚を確認しています…',
    'Claude hat nichts gefunden, das so nicht geteilt werden sollte.':
        'Claude は、このまま共有すべきでないものを見つけませんでした。',
    'Springt hin und schlägt einen Zensurkasten für diese Stelle vor.':
        'その場所へジャンプし、この箇所に検閲枠を提案します。',
    'Springt hin.':
        'その場所へジャンプします。',
    'Vorschlag bei {at} – „Vorschläge übernehmen“ verdeckt die Stelle.':
        '{at} に提案あり – 「提案を採用」でその箇所を隠します。',
    'Name lesbar':
        '名前が読める',
    'Chat lesbar':
        'チャットが読める',
    'Auffällig':
        '目立つ',
    'Text finden':
        'テキストを検索',
    'Sucht auf dem Bild am Abspielkopf nach Text (Namen, Chat) – auf diesem PC, nichts wird gesendet. Die Fundstellen erscheinen nummeriert.':
        '再生ヘッドの位置の画像からテキスト（名前、チャット）を探します – この PC 上で処理し、何も送信しません。見つかったものには番号が付きます。',
    'Vorschläge übernehmen':
        '提案を採用',
    'Macht aus den nummerierten Fundstellen Zensurkästen (ein Schritt zum Rückgängigmachen).':
        '番号付きの検出結果を検閲枠にします（1 ステップで元に戻せます）。',
    'Vorschläge verwerfen':
        '提案を破棄',
    'Claude: nur Namen':
        'Claude：名前のみ',
    'Schickt das Standbild (zensierte Bereiche bleiben zensiert) mit den nummerierten Fundstellen an Claude; Claude nennt nur die Nummern, die Namen oder Chat zeigen – die übrigen Vorschläge fallen weg.':
        '静止画（検閲した領域は検閲されたまま）を番号付きの検出結果とともに Claude に送信します。Claude は名前やチャットが写っている番号のみを挙げ、その他の提案は外されます。',
    'Die Texterkennung ist in dieser Installation nicht vorhanden.':
        'このインストールではテキスト検出を利用できません。',
    'Suche Text im Bild …':
        '画像内のテキストを探しています…',
    'Das Bild liess sich nicht nach Text durchsuchen.':
        '画像内のテキストを検索できませんでした。',
    'Kein Text gefunden, der nicht schon verdeckt ist.':
        'まだ隠されていないテキストは見つかりませんでした。',
    '{n} Textstellen gefunden – „Vorschläge übernehmen“ verdeckt sie.':
        'テキスト箇所が {n} 個見つかりました – 「提案を採用」で隠します。',
    '{n} Kästen gesetzt.':
        '枠を {n} 個設定しました。',
    'Claude sieht sich {n} Fundstellen an …':
        'Claude が {n} 個の検出結果を確認しています…',
    'Claude hält keine Fundstelle für einen Namen oder Chat.':
        'Claude によると、検出結果に名前やチャットはありません。',
    '{n} Fundstellen zeigen laut Claude Namen oder Chat.':
        'Claude によると、{n} 個の検出結果に名前またはチャットが写っています。',
    'Kasten ab hier':
        'ここから枠',
    'Kasten bis hier':
        'ここまで枠',
    'Kasten immer':
        '常に枠',
    'Der markierte Kasten gilt erst ab dem Bild am Abspielkopf – z. B. wenn ein Name erst später erscheint.':
        '選択した枠を再生ヘッドの位置の画像以降のみに適用します – 例：名前が後から表示される場合。',
    'Der markierte Kasten gilt nur bis zum Bild am Abspielkopf.':
        '選択した枠を再生ヘッドの位置の画像までのみに適用します。',
    'Der markierte Kasten gilt wieder für die ganze Aufnahme.':
        '選択した枠を再び録画全体に適用します。',
    'Kasten {n} gilt von {a} bis {b} der Aufnahme.':
        '枠 {n} は録画の {a} から {b} に適用されます。',
    'Kasten {n} gilt für die ganze Aufnahme.':
        '枠 {n} は録画全体に適用されます。',
    'Am Anfang der Aufnahme gibt es kein „bis hier“.':
        '録画の先頭では「ここまで」は使えません。',
    '{n} davon nur zeitweise.':
        'そのうち {n} 個は一定時間のみ。',
    'Zurückspringen / Anhalten / Abspielen – L mehrmals: ×2, ×4':
        '戻る / 停止 / 再生 – L をもう一度押すと：×2、×4',
    'Vollbild an / aus':
        'フルスクリーン オン / オフ',
    'Clip beginnt / endet am Abspielkopf':
        'クリップの開始 / 終了を再生ヘッドに',
    'S oder Strg+B':
        'S または Ctrl+B',
    'Clip am Abspielkopf teilen':
        '再生ヘッドの位置でクリップを分割',
    'Entf':
        'Del',
    'Markierten Clip löschen':
        '選択したクリップを削除',
    'Hinein- / herauszoomen':
        '拡大 / 縮小',
    'Strg+0':
        'Ctrl+0',
    'Ganze Zeitleiste zeigen':
        'タイムライン全体を表示',
    'Auswählen':
        '選択',
    'Bildausschnitt':
        '切り抜き',
    'Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie':
        'キャンセル、ツールを終了、または選択を解除 – 閉じることはありません',
    'Strg+W':
        'Ctrl+W',
    'Editor schliessen':
        'エディターを閉じる',
    'Abgebrochen.':
        'キャンセルしました。',
    'Esc schliesst den Editor nicht – schliessen mit × oder Strg+W.':
        'Esc ではエディターは閉じません – × または Ctrl+W で閉じてください。',
    'Strg+Z / Strg+Y':
        'Ctrl+Z / Ctrl+Y',
    'Rückgängig / Wiederholen':
        '元に戻す / やり直し',
    'Strg+S':
        'Ctrl+S',
    'Projekt speichern':
        'プロジェクトを保存',
    'Strg+E':
        'Ctrl+E',
    'Diese Übersicht ein / aus':
        'この一覧 オン / オフ',
    'In der Statistik zeigen':
        '統計で表示',
    'Aufnahme dieser Runde öffnen':
        'このラウンドの録画を開く',
    'Runde markieren: Rolle, Farming, Killer oder Map korrigieren, löschen – oder Rechtsklick. Doppelklick zeigt die Aufnahme.':
        'ラウンドを選択：役割、ファーミング、キラー、マップの修正、削除 – または右クリック。ダブルクリックで録画を表示します。',
    'OBS-Passwort ist auf diesem PC/Benutzerkonto nicht lesbar – bitte neu eingeben.':
        'この PC/ユーザーアカウントでは OBS のパスワードを読み取れません – もう一度入力してください。',
    'Als neues Projekt speichern':
        '新しいプロジェクトとして保存',
    'Autosave aus':
        '自動保存 オフ',
    'Bereich übernehmen':
        '範囲を採用',
    'Bereich übernommen – Strg+Z stellt das Projekt wieder her.':
        '範囲を採用しました – Ctrl+Z でプロジェクトが元に戻ります。',
    'Das Projekt wurde ausserhalb geändert oder liegt doppelt vor. Deine Fassung liegt unter Sicherungen und lokal.':
        'プロジェクトが Fog Scout の外で変更されたか、2 つ存在します。あなたのバージョンは Sicherungen とローカルに保管されています。',
    'Die Aufnahme konnte nicht geprüft werden.':
        '録画を確認できませんでした。',
    'Die Aufnahme liegt nur in der Cloud – die Prüfung würde sie ganz herunterladen.':
        '録画はクラウドにしかありません – 確認すると全体がダウンロードされます。',
    'Die Aufnahme passt nicht zum gespeicherten Projekt (ihr Inhalt ist anders). Es wurde nicht geladen.':
        '録画が保存されたプロジェクトと一致しません（内容が異なります）。読み込まれませんでした。',
    'Die Clips des Projekts waren unlesbar – der Standardclip wird gezeigt.':
        'プロジェクトのクリップを読み取れませんでした – 既定のクリップを表示しています。',
    'Die Projektdatei ist unlesbar und wurde nicht geladen.':
        'プロジェクトファイルを読み取れないため、読み込まれませんでした。',
    'Die Projektdatei wurde ausserhalb von Fog Scout gelöscht oder verschoben. Dein Stand ist lokal gesichert.':
        'プロジェクトファイルが Fog Scout の外で削除または移動されました。状態はローカルに保管されています。',
    'Die Projektdatei wurde umbenannt. Dein Stand ist lokal gesichert.':
        'プロジェクトファイルの名前が変更されました。状態はローカルに保管されています。',
    'Dieses Projekt ist schon in einem anderen Fenster offen – hier wird nichts gespeichert.':
        'このプロジェクトは既に別のウィンドウで開いています – ここでは何も保存されません。',
    'Editor-Projekte automatisch speichern':
        'エディターのプロジェクトを自動で保存する',
    'Editor-Projekte nicht gesichert':
        'エディターのプロジェクトが保護されていません',
    'Editor-Projekte werden noch gesichert …':
        'エディターのプロジェクトを保護中…',
    'Editor: automatisches Speichern an.':
        'エディター：自動保存 オン。',
    'Editor: automatisches Speichern aus – Strg+S speichert das Projekt.':
        'エディター：自動保存 オフ – Ctrl+S でプロジェクトを保存します。',
    'Eine wählen …':
        '1 つ選択…',
    'Erneut prüfen':
        '再確認',
    'Es gibt ein Projekt zu einer gleichnamigen, aber veränderten Aufnahme.':
        '同じ名前の録画用のプロジェクトがありますが、録画が変更されています。',
    'Für diese Aufnahme gibt es ein gespeichertes Projekt ({n} Clips). Den Bereich aus der Vorschau ({a}–{b}) übernehmen ersetzt seine Clips.':
        'この録画には保存されたプロジェクトがあります（{n} クリップ）。プレビューの範囲（{a}–{b}）を採用すると、そのクリップが置き換えられます。',
    'Gespeichertes Projekt gefunden – die Aufnahme wird geprüft.':
        '保存されたプロジェクトが見つかりました – 録画を確認中です。',
    'Kein Projekt':
        'プロジェクトなし',
    'Kein Projekt – Strg+S legt ein neues an.':
        'プロジェクトなし – Ctrl+S で新規作成します。',
    'Keine öffnen':
        'どれも開かない',
    'Laden':
        '読み込む',
    'Lokal gesicherter Stand eines fehlenden Projekts gefunden.':
        '見つからないプロジェクトのローカル保管状態が見つかりました。',
    'Mindestens ein Editor-Stand ist weder im Projekt noch lokal gesichert (Speichern hängt oder der Ordner ist nicht erreichbar). Trotzdem beenden? Die ungesicherten Änderungen gehen dann verloren.':
        '少なくとも 1 つのエディターの状態が、プロジェクトにもローカルにも保管されていません（保存が止まっているか、フォルダーにアクセスできません）。それでも終了しますか？その場合、保護されていない変更は失われます。',
    'Neu beginnen':
        '新規に開始',
    'Neuerer Stand aus der lokalen Rettungskopie geladen.':
        'ローカルの救出用コピーから新しい状態を読み込みました。',
    'Neues Projekt':
        '新しいプロジェクト',
    'Nicht laden':
        '読み込まない',
    'Nicht schliessen':
        '閉じない',
    'Nicht wiederherstellen':
        '復元しない',
    'Nichts tun':
        '何もしない',
    'Ohne Prüfung laden':
        '確認せずに読み込む',
    'Projekt aus Fog Scout 1.17 oder älter gefunden (gleicher Name, gleiche Grösse).':
        'Fog Scout 1.17 以前のプロジェクトが見つかりました（同じ名前、同じサイズ）。',
    'Projekt aus neuerer Version – wird nicht überschrieben':
        '新しいバージョンのプロジェクト – 上書きしません',
    'Projekt behalten':
        'プロジェクトを残す',
    'Projekt geöffnet – der Bereich aus der Vorschau wurde nicht übernommen.':
        'プロジェクトを開きました – プレビューの範囲は採用されていません。',
    'Projekt nicht gespeichert und keine Rettungskopie möglich: {why}':
        'プロジェクトは保存されず、救出用コピーも作成できません：{why}',
    'Projekt wiederherstellen':
        'プロジェクトを復元',
    'Projekt wird gespeichert …':
        'プロジェクトを保存中…',
    'Projekt wird gesucht …':
        'プロジェクトを探しています…',
    'Prüfen':
        '確認',
    'Prüft Aufnahme …':
        '録画を確認中…',
    'Prüft Aufnahme … {p} %':
        '録画を確認中… {p} %',
    'Speichern und schliessen':
        '保存して閉じる',
    'Trotzdem laden':
        'それでも読み込む',
    'Trotzdem schliessen':
        'それでも閉じる',
    'Ungespeicherte Änderungen von {when} gefunden.':
        '{when} の未保存の変更が見つかりました。',
    'Ungespeicherte Änderungen.':
        '未保存の変更があります。',
    'Update wartet: Editor-Projekte werden gesichert …':
        'アップデートは待機中：エディターのプロジェクトを保護中…',
    'Verwerfen und schliessen':
        '破棄して閉じる',
    'Wiederherstellen':
        '復元',
    'Zu dieser Aufnahme gibt es ein Projekt, das nie vollständig geprüft wurde. Anfang, Ende und Grösse stimmen; ob es die ganze Aufnahme ist, kann Fog Scout nicht bestätigen.':
        'この録画には、完全に確認されたことのないプロジェクトがあります。開始、終了、サイズは一致していますが、それが録画全体かどうかを Fog Scout は確認できません。',
    'Zuordnung nicht geprüft':
        '割り当て未確認',
    '{n} Projektdateien passen zu dieser Aufnahme – keine wurde geöffnet.':
        '{n} 個のプロジェクトファイルがこの録画に一致します – どれも開きませんでした。',
    '● Änderungen':
        '● 変更あり',
    '⚠ Mehrere Projektdateien – Auswahl nötig':
        '⚠ 複数のプロジェクトファイル – 1 つ選んでください',
    '⚠ Nicht gespeichert – {why}':
        '⚠ 保存されていません – {why}',
    '⚠ Nicht im Projekt gespeichert – lokal gesichert':
        '⚠ プロジェクトに保存されていません – ローカルに保管',
    '⚠ Projekt ausserhalb geändert':
        '⚠ プロジェクトが外部で変更されました',
    '⚠ Projektdatei fehlt – Änderungen nur lokal gesichert':
        '⚠ プロジェクトファイルがありません – 変更はローカルにのみ保管',
    '⚠ Speichern hängt':
        '⚠ 保存が止まっています',
    '✓ Gespeichert {at}':
        '✓ {at} に保存',
    'Der grosse Editor speichert sein Projekt von selbst (1,5 s nach einer Änderung, nie während du ziehst) – mit Sicherungen und einer lokalen Kopie, falls die Projektdatei nicht schreibbar ist. Aus: nur Strg+S schreibt das Projekt; dazwischen hält der Editor einen lokalen Wiederherstellungsstand.':
        '大きなエディターはプロジェクトを自動で保存します（変更から 1.5 秒後、ドラッグ中は保存しません）– プロジェクトファイルを書き込めない場合に備えて、バックアップとローカルコピーも作成します。オフ：Ctrl+S でのみプロジェクトを書き込みます。その間、エディターはローカルに復旧用の状態を保持します。',
    'Auf alle Clips':
        'すべてのクリップに',
    'Bild bei {at} der Aufnahme · {length} s ohne Ton':
        '録画の {at} の画像 · {length} 秒、音声なし',
    'Den Ausschnitt am Anfang des Clips in der Vorschau ziehen – dazwischen fährt die Kamera gleichmässig.':
        'プレビューでクリップの開始時点のフレームをドラッグしてください – その間、カメラは一定の速さで移動します。',
    'Den Ausschnitt am Ende des Clips in der Vorschau ziehen.':
        'プレビューでクリップの終了時点のフレームをドラッグしてください。',
    'Der Clip zeigt wieder das ganze Bild.':
        'クリップは再び画像全体を表示します。',
    'Effekte':
        'エフェクト',
    'Effekte entfernen':
        'エフェクトを削除',
    'Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start.':
        '固定フレーム：開始と終了が同じ – 終了フレームが開始に追従します。',
    'End-Ausschnitt':
        '終了フレーム',
    'Farbe auf alle {n} Clips übernommen.':
        '色を {n} 個すべてのクリップに適用しました。',
    'Heller oder dunkler – nur dieser Clip.':
        '明るく、または暗く – このクリップのみ。',
    'Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen.':
        'このクリップの明るさ、コントラスト、彩度を録画時の状態に戻します。',
    'Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton.':
        '再生ヘッドの位置の画像を設定した時間だけ静止させます（キー P）– 音声なし。',
    'Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.':
        '色を濃く、または淡く。左端は白黒 – このクリップのみ。',
    'Mehr oder weniger Kontrast – nur dieser Clip.':
        'コントラストを強く、または弱く – このクリップのみ。',
    'Ohne Bewegung':
        '動きなし',
    'Rückwärts':
        '逆再生',
    'Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.':
        '逆再生はクリップあたり {n} 秒までです – 先にこのクリップを分割してください。',
    'Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens {n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).':
        'クリップを音声も含めて逆再生します。この録画ではクリップあたり最大 {n} 秒です（それ以上は ffmpeg が大量のメモリを必要とします）。',
    'Standbild am Abspielkopf einfügen':
        '再生ヘッドの位置に静止画を挿入',
    'Standbild einfügen':
        '静止画を挿入',
    'Standbild eingefügt: {n} s ohne Ton.':
        '静止画を挿入しました：{n} 秒、音声なし。',
    'Standbild hier einfügen':
        'ここに静止画を挿入',
    'Standbild – Clip {n} von {total}':
        '静止画 – クリップ {n} / {total}',
    'Start-Ausschnitt':
        '開始フレーム',
    'Wie lange ein Standbild steht – für ein neues, oder für das markierte Standbild.':
        '静止画を止める時間 – 新しい静止画、または選択した静止画に適用されます。',
    'Zoom':
        'ズーム',
    'Zoom entfernen':
        'ズームを削除',
    'Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – Esc beendet.':
        'ズーム：プレビューでフレームをドラッグするか、角を引いて拡大/縮小します – Esc で終了。',
    '{n}  Standbild {length} s':
        '{n}  静止画 {length} 秒',
    'Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig).':
        'このクリップの明るさ、コントラスト、彩度をタイムライン上のすべてのクリップに適用します（1 ステップ、Ctrl+Z で元に戻せます）。',
    'Als Short anzeigen':
        'ショートとして表示',
    'Beginnt hier':
        'ここから開始',
    'Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.':
        'テキストは再生ヘッドの位置から {n} 秒間、ショートの下部に表示されます。',
    'Der markierte Untertitel beginnt am Abspielkopf.':
        '選択した字幕は再生ヘッドの位置から始まります。',
    'Der markierte Untertitel endet am Abspielkopf.':
        '選択した字幕は再生ヘッドの位置で終わります。',
    'Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen.':
        'プレビューには、タイトルと字幕付きの完成した縦型動画が表示されます – 描画と検閲はエクスポートに含まれますが、ここには表示されません。',
    'Ein Short ist höchstens {limit} min lang, dieser Schnitt {seconds} s – kürzer schneiden.':
        'ショートは最大 {limit} 分ですが、このカットは {seconds} 秒です – 短くカットしてください。',
    'Endet hier':
        'ここで終了',
    'Entfernen':
        '削除',
    'Entfernt den markierten Untertitel.':
        '選択した字幕を削除します。',
    'Erst den Text des Untertitels eingeben.':
        '先に字幕のテキストを入力してください。',
    'Hochformat 1080×1920 für YouTube Shorts und TikTok, höchstens 3 min':
        'YouTube ショートと TikTok 用の縦型 1080×1920、最大 3 分',
    'Schriftgrösse des Titels.':
        'タイトルのフォントサイズ。',
    'Short (9:16)':
        'ショート（9:16）',
    'Short / TikTok (9:16)':
        'ショート / TikTok（9:16）',
    'Short 1080×1920, {fps} fps':
        'ショート 1080×1920、{fps} fps',
    'Text eingeben, dann „Untertitel am Abspielkopf“':
        'テキストを入力してから「再生ヘッドに字幕」',
    'Titel':
        'タイトル',
    'Titel oben (leer = keiner)':
        '上部のタイトル（空欄 = なし）',
    'Unscharfer Hintergrund':
        'ぼかし背景',
    'Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der 9:16-Ausschnitt unter Bild) füllt das Hochformat.':
        'ぼかし背景：ゲーム画面全体を中央に、同じ画像をぼかして上下に配置します。切り抜き：中央部分（または「画像」の 9:16 切り抜き）で縦型フレームを埋めます。',
    'Untertitel':
        '字幕',
    'Untertitel am Abspielkopf':
        '再生ヘッドに字幕',
    'Zuschnitt 9:16':
        '9:16 で切り抜き',
    'gross':
        '大',
    'klein':
        '小',
    'mittel':
        '中',
    '⚠ länger als {n} min – so nicht exportierbar':
        '⚠ {n} 分より長い – このままではエクスポートできません',
    '(Datei fehlt – wird nicht exportiert)':
        '（ファイルなし – エクスポートされません）',
    'Beginnt am Abspielkopf':
        '再生ヘッドから開始',
    'Der Spielton wird von selbst leiser, solange Musik läuft – „stark“ drückt ihn am meisten. Aus: beide gleich laut wie eingestellt.':
        '音楽の再生中はゲーム音が自動で小さくなります – 「強」で最も下がります。オフ：どちらも設定した音量のまま。',
    'Der markierte Ton-Clip beginnt am Abspielkopf.':
        '選択したオーディオクリップは再生ヘッドの位置から始まります。',
    'Die Musik wird am Anfang des Clips lauter.':
        'クリップの開始時に音楽がフェードインします。',
    'Die Musik wird zum Ende des Clips leiser.':
        'クリップの終わりに向けて音楽がフェードアウトします。',
    'Die Vorschau spielt die Musik mit – Standbilder sind in der Vorschau still, im Export läuft die Musik weiter.':
        'プレビューでも音楽を再生します – 静止画はプレビューでは無音ですが、エクスポートでは音楽が流れ続けます。',
    'Eigene Tonspur (A2)':
        '独自のオーディオトラック（A2）',
    'Eine eigene Ton- oder Videodatei (Musik, Kommentar) am Abspielkopf auf die Spur A2 legen – oder die Datei direkt auf A2 ziehen.':
        '独自の音声または動画ファイル（音楽、解説）を再生ヘッドの位置でトラック A2 に置きます – またはファイルを A2 にドラッグしてください。',
    'Höchstens {n} Ton-Clips.':
        'オーディオクリップは最大 {n} 個です。',
    'Kein Ton in {file}.':
        '{file} に音声がありません。',
    'Keine Ton- oder Videodatei: {file}':
        '音声または動画ファイルではありません：{file}',
    'Lautstärke':
        '音量',
    'Lautstärke der ganzen Spur A2.':
        'トラック A2 全体の音量。',
    'Lautstärke des Spieltons im fertigen Clip.':
        '完成したクリップでのゲーム音の音量。',
    'Lautstärke nur dieses Ton-Clips.':
        'このオーディオクリップのみの音量。',
    'Lese {file} …':
        '{file} を読み込み中…',
    'Musik aus':
        '音楽アウト',
    'Musik ein':
        '音楽イン',
    'Musik hinzufügen':
        '音楽を追加',
    'Musik hinzufügen …':
        '音楽を追加…',
    'Musik oder Kommentar hierher ziehen – oder Rechtsklick „Musik hinzufügen …“':
        '音楽や解説をここにドラッグ – または右クリックで「音楽を追加…」',
    'Nimmt den markierten Ton-Clip von der Spur A2 – die Datei bleibt.':
        '選択したオーディオクリップをトラック A2 から外します – ファイルは残ります。',
    'Noch keine Musik – Spielton wie aufgenommen.':
        'まだ音楽はありません – ゲーム音は録音したまま。',
    'Spielton':
        'ゲーム音',
    'Spielton unter Musik':
        '音楽の下のゲーム音',
    'Ton und Video':
        '音声と動画',
    'Ton-Clip entfernen':
        'オーディオクリップを削除',
    'Ton-Clip {file} entfernt – die Datei bleibt.':
        'オーディオクリップ {file} を削除しました – ファイルは残ります。',
    'leicht':
        '弱',
    'stark':
        '強',
    '{file} liegt auf A2 ab {at} – der Spielton wird darunter leiser.':
        '{file} は {at} から A2 にあります – その間ゲーム音は小さくなります。',
    '{file}: {start} – {end} der Datei, im Clip ab {at}':
        '{file}：ファイルの {start} – {end}、クリップ内では {at} から',
    '{n} Ton-Clip(s) auf A2.':
        'A2 にオーディオクリップ {n} 個。',
    'Als Montage öffnen …':
        'モンタージュとして開く…',
    'Andere Grösse ({w}×{h}) – im Export mit schwarzen Rändern eingepasst.':
        'サイズが異なります（{w}×{h}）– エクスポートでは黒帯を付けて合わせます。',
    'Aufnahme fehlt oder ist nicht lesbar: {file}':
        '録画が見つからないか読み取れません：{file}',
    'Eine Montage übernimmt keinen Bereich aus der Vorschau.':
        'モンタージュはプレビューから範囲を採用しません。',
    'Erst wenn das Projekt geladen ist.':
        'プロジェクトが読み込まれてからのみ。',
    'Für eine Montage mindestens zwei Videos markieren.':
        'モンタージュには少なくとも 2 つの動画を選択してください。',
    'Höchstens {n} Aufnahmen in einer Montage.':
        'モンタージュの録画は最大 {n} 個です。',
    'Jetzt eine Montage – sie wird unter Clips → Montagen gespeichert. Das Projekt der Runde bleibt, wie es zuletzt gespeichert war.':
        'モンタージュになりました – Clips → Montagen に保存されます。ラウンドのプロジェクトは最後に保存した状態のままです。',
    'Montage':
        'モンタージュ',
    'Montage aus {n} Aufnahmen':
        '{n} 個の録画のモンタージュ',
    'Montage nicht zu öffnen – ihre erste Aufnahme fehlt: {file}':
        'モンタージュを開けません – 最初の録画が見つかりません：{file}',
    'Montage {date}':
        'モンタージュ {date}',
    'Nicht gefunden: {files} – ihre Clips sind rot, Exportieren geht erst, wenn sie entfernt sind.':
        '見つかりません：{files} – そのクリップは赤で表示されます。削除すればエクスポートできます。',
    'Nur lesen':
        '読み取り専用',
    'Trotzdem verwenden':
        'それでも使用',
    'Video nicht lesbar: {file}':
        '動画を読み取れません：{file}',
    '{file} ist nicht mehr dieselbe Aufnahme wie beim Speichern.':
        '{file} は保存時と同じ録画ではなくなっています。',
    '{file}: {n} Clip(s) angehängt.':
        '{file}：{n} クリップを追加しました。',
    'Audiomediathek':
        'オーディオ ライブラリ',
    'Audiomediathek im Browser geöffnet – heruntergeladene Titel erscheinen im Abschnitt Ton, sobald du zurück im Editor bist.':
        'ブラウザーでオーディオ ライブラリを開きました – ダウンロードした曲は、エディターに戻ると「サウンド」セクションに表示されます。',
    'Neu im Download-Ordner – Klick legt sie am Abspielkopf auf A2:':
        'ダウンロードフォルダーの新着 – クリックすると再生ヘッドの位置で A2 に置きます：',
    'Öffnet YouTubes Audiomediathek im Browser: kostenlose Musik und Effekte, für Videos freigegeben (keine Content-ID-Ansprüche). Heruntergeladene MP3s erscheinen hier darunter.':
        'ブラウザーで YouTube のオーディオ ライブラリを開きます：動画用に許諾済みの無料の音楽と効果音（Content ID の申し立てなし）。ダウンロードした MP3 は下に表示されます。',
    'Status, aktuelle Map und deine Runden auf einen Blick':
        '状態、現在のマップ、ラウンドをひと目で',
    'Alle Callout-Karten – ansehen, von Hand einblenden, eigene Bilder und Notizen':
        'すべてのコールアウトマップ – 閲覧、手動表示、独自の画像とメモ',
    'Was im Spiel erscheint, wo und wie gross':
        'ゲーム内に何を、どこに、どの大きさで表示するか',
    'Deine Runden, Kills und Wartezeiten – nur auf diesem PC gespeichert':
        'ラウンド、キル、待ち時間 – この PC にのみ保存',
    'Runden, Clips und Screenshots – abspielen, schneiden, aufräumen':
        'ラウンド、クリップ、スクリーンショット – 再生、カット、整理',
    'Server-Regionen wählen und die Verbindung im Blick behalten':
        'サーバーリージョンを選択し、接続を見守る',
    'Alles, was Fog Scout tut – suchen mit Strg+F':
        'Fog Scout のすべての機能 – Ctrl+F で検索',
    'Was das Programm gemacht hat – zum Nachlesen und für die Fehlersuche':
        'プログラムが行ったこと – 確認用とトラブルシューティング用',
    'Übersicht öffnen':
        '概要を開く',
    'Funktionen':
        '機能',
    'aktiv':
        '有効',
    'wartet auf DBD':
        'DBD を待機中',
    'nimmt auf':
        '録画中',
    'verbunden':
        '接続済み',
    'verbindet …':
        '接続中…',
    'startet …':
        '起動中…',
    'Fehler – Details im Log':
        'エラー – 詳細はログに',
    'nur unter Windows':
        'Windows のみ',
    'HWiNFO fehlt':
        'HWiNFO がありません',
    'Mediensteuerung nicht verfügbar':
        'メディアコントロールを利用できません',
    'Discord nicht erreichbar':
        'Discord に接続できません',
    'Anmeldung nötig':
        'サインインが必要です',
    'keine Client-ID':
        'クライアント ID なし',
    'Suche leeren':
        '検索をクリア',
    'Runden · BP/h erst mit Match-Daten':
        'ラウンド · BP/時にはマッチデータが必要です',
    'Verbindung prüfen …':
        '接続を確認…',
    'Öffnet Einstellungen → Verbindungen: OBS-Verbindung (Port, Passwort) und „Verbindung testen“.':
        '「設定」→「接続」を開きます：OBS 接続（ポート、パスワード）と「接続をテスト」。',
    '{n} Marken':
        'マーク {n} 個',
    '1 Marke':
        'マーク 1 個',
    'Keine Aufnahme passt zu den Filtern oben.':
        '上のフィルターに一致する録画はありません。',
    'Kein Clip passt zu den Filtern oben.':
        '上のフィルターに一致するクリップはありません。',
    'Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.':
        '行がありません – ログが空か、検索とカテゴリーですべて非表示になっています。',
    'OBS nicht verbunden':
        'OBS 未接続',
    'Kills, Entkommen und Bloodpoints zählen hier ohne Custom Games – die Rolle „Custom Games“ zeigt sie.':
        'ここでのキル、脱出、ブラッドポイントはカスタムマッチを除いて数えます – 役割「カスタムマッチ」で表示されます。',
    'Keine Runden in dieser Auswahl – „Filter zurücksetzen“ zeigt wieder alle.':
        'この選択範囲にはラウンドがありません – 「フィルターをリセット」ですべて再表示されます。',
    'In dieser Auswahl ist keine Runde einem Match der Stats-Seite zugeordnet – darum fehlen Kills, Entkommen und Bloodpoints.':
        'この選択範囲のどのラウンドも統計ページのマッチと紐付けられていません – そのためキル、脱出、ブラッドポイントがありません。',
    'Kills, Entkommen und Bloodpoints kommen von der Stats-Seite – dafür einmal die Match-Daten einrichten.':
        'キル、脱出、ブラッドポイントは統計ページから取得します – そのためにマッチデータを一度設定してください。',
    'Nicht gezählt: {n} × Rundenende nicht erkannt (die nächste Map kam, bevor das Ende erkannt wurde). Zuletzt: {map}, {when}.':
        '数えられていません：ラウンド終了が {n} 回検出されませんでした（終了を検出する前に次のマップが来ました）。最後：{map}、{when}。',
    '{n} × Rundenende nicht erkannt, aber mit der Dauer laut Stats-Seite gezählt.':
        'ラウンド終了が {n} 回検出されませんでしたが、統計ページの長さで数えました。',
    '{n} × Map mitten im Match falsch erkannt (laut Stats-Seite lief da schon ein Match) – nicht gezählt. Zuletzt: {map}, {when}.':
        'マッチの途中でマップが誤って読み取られたことが {n} 回あります（統計ページでは既にマッチが進行中でした）– 数えられていません。最後：{map}、{when}。',
    'Keine Map passt zu „{text}“. Gesucht wird in Map- und Realm-Namen aller Spielsprachen und in Abkürzungen.':
        '「{text}」に一致するマップはありません。検索は、すべてのゲーム言語のマップ名とレルム名、および略称を対象にします。',
    'Leert das Suchfeld und zeigt wieder alle Maps.':
        '検索欄をクリアし、すべてのマップを再表示します。',
    'Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter „Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) – die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose.':
        '各チェックは、クリックしたときに Claude が手伝う場所です – 自動で動くことも、入力中に動くこともありません：検索（「Claude に質問」の行：質問と、設定・ページ・操作の名前）、統計の質問（件数と割合）、クリップエディター（「Claude で編集」：要望と数値で表したカット。チェックを入れると静止画も）、画像エディター（「Claude」タブ：要望と画像）。Claude は提案するだけで、選択するか「適用」で確定するまで何も実行されません。決して送信しないもの：ラウンド、マップ、キラー、パス、ファイル名、サーバー、ログ。Anthropic Console のご自身の API キーが必要です（「API キーを取得」）。API は Claude のサブスクリプションとは別にクレジットから支払います（「クレジットを追加」、そこで利用上限も設定できます）– プログラムは各質問の費用を応答から概算し、月ごとに合計します。キーは Windows の暗号化でこの PC に保存され（失敗した場合は終了するまで有効）、バックアップ、ログ、診断情報には決して含まれません。',
    'Zeigt in der Musikkarte, was in Spotify als Nächstes kommt (Position und Anzahl unter Overlay → Musik). Die Windows-Mediensteuerung kennt nur den laufenden Titel, die Liste holt das Programm deshalb von Spotify selbst: Dafür im Developer-Dashboard „Create app“ anlegen (Name frei, API „Web API“), als Redirect URI genau {uri} eintragen, die Client-ID kopieren und hier einfügen, dann „Mit Spotify verbinden“ – der Browser fragt einmal nach der Freigabe. Gelesen wird nur die Warteschlange, nichts gesteuert; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden) und lässt sich hier trennen. Titel kommen nie ins Log.':
        'Spotify で次に再生される曲を音楽カードに表示します（位置と曲数は「オーバーレイ」→「音楽」で）。Windows のメディアコントロールは現在の曲しか知らないため、プログラムは Spotify 自体からリストを取得します：開発者ダッシュボードで「Create app」（名前は任意、API は「Web API」）、リダイレクト URI に正確に {uri} を入力し、クライアント ID をコピーしてここに貼り付け、「Spotify に接続」をクリックします – ブラウザーで一度だけ同意を求められます。読み取るのはキューのみで、何も操作しません。同意は Windows の暗号化でこの PC に保存され（利用できない場合は終了するまでのみ有効）、ここで削除できます。曲名がログに記録されることはありません。',
    'Lädt Clips (F8 und Editor) von selbst auf deinen YouTube-Kanal, Runden nur auf Wunsch: Rechtsklick oder „Auf YouTube hochladen“ unter Aufnahmen. Dafür einmal in der Google Cloud Console ein Projekt anlegen, „YouTube Data API v3“ aktivieren, unter „Anmeldedaten“ einen OAuth-Client vom Typ „Desktop-App“ erstellen und den Zustimmungsbildschirm veröffentlichen (sonst läuft die Anmeldung nach 7 Tagen ab); Client-ID und Client-Secret hier einfügen oder die heruntergeladene JSON-Datei laden, dann „Mit YouTube verbinden“ – der Browser fragt einmal nach der Freigabe. Google erlaubt mit dem Standardkontingent etwa sechs Uploads am Tag; was nicht mehr passt, wartet in der Warteschlange bis zum nächsten Tag. Hochgeladen wird nur, wenn du weder in einer Lobby noch in einer Runde bist; die Datei bleibt immer auch auf der Platte. Gesendet werden nur die Videodatei, Titel (Map, Killer, Datum) und Beschreibung – nie Spielernamen; die Freigabe wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt sie nur bis zum Beenden). Mit „Uploads in Playlists einsortieren“ kommt jedes Video zusätzlich in eine Playlist deiner Wahl – dafür fragt die Anmeldung die breitere Berechtigung „YouTube-Konto verwalten“ an (einmal neu verbinden).':
        'クリップ（F8 とエディター）を自動で YouTube チャンネルにアップロードします。ラウンドはリクエストした場合のみ：「録画」で右クリック、または「YouTube にアップロード」。そのために、Google Cloud コンソールで一度プロジェクトを作成し、「YouTube Data API v3」を有効にし、「認証情報」で種類「デスクトップ アプリ」の OAuth クライアントを作成して、同意画面を公開してください（公開しないとログインが 7 日で期限切れになります）。クライアント ID とクライアントシークレットをここに貼り付けるか、ダウンロードした JSON ファイルを読み込み、「YouTube に接続」をクリックします – ブラウザーで一度だけ同意を求められます。既定の割り当てでは Google が許可するのは 1 日約 6 件のアップロードで、収まらないものは翌日までキューで待機します。アップロードはロビーにもラウンドにもいない間のみ実行され、ファイルは常にディスクにも残ります。送信されるのは動画ファイル、タイトル（マップ、キラー、日付）、説明のみ – プレイヤー名は決して送信しません。同意は Windows の暗号化でこの PC に保存されます（利用できない場合は終了するまでのみ有効）。「アップロードを再生リストに振り分ける」を使うと、各動画が選択した再生リストにも追加されます – そのためログイン時により広い権限「YouTube アカウントの管理」を求められます（もう一度接続してください）。',
    'Liest Client-ID und Client-Secret aus der Datei „client_secret_….json“, die Google nach dem Anlegen des OAuth-Clients zum Herunterladen anbietet („JSON herunterladen“). Die Datei wird nur gelesen und bleibt, wo sie ist; das Secret landet mit der Windows-Verschlüsselung in den Einstellungen (sonst gilt es nur bis zum Beenden).':
        'OAuth クライアントの作成後に Google がダウンロード用に提供するファイル「client_secret_….json」（「JSON をダウンロード」）から、クライアント ID とクライアントシークレットを読み取ります。ファイルは読み取るだけでそのまま残ります。シークレットは Windows の暗号化で設定に保存されます（そうでない場合は終了するまでのみ有効）。',
    'Öffnet die Google-Anmeldung im Browser (nur Recht „Videos hochladen“). Danach kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe mit der Windows-Verschlüsselung auf diesem PC (sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf einem freien Port.':
        'ブラウザーで Google のログインを開きます（権限は「動画のアップロード」のみ）。その後ブラウザーは 127.0.0.1 に戻り、プログラムは同意を Windows の暗号化でこの PC に保管します（そうでない場合は終了するまでのみ）。そのため、ログイン中のみ一度、空いているポートで待ち受けます。',
    'Öffnet die Spotify-Anmeldung im Browser. Nach dem Zustimmen kommt der Browser auf 127.0.0.1 zurück und das Programm merkt sich die Freigabe (mit der Windows-Verschlüsselung, nur auf diesem PC – sonst nur bis zum Beenden). Dafür hört es nur während der Anmeldung einmal auf diesem Port.':
        'ブラウザーで Spotify のログインを開きます。同意すると、ブラウザーは 127.0.0.1 に戻り、プログラムは同意を保管します（Windows の暗号化で、この PC のみ – そうでない場合は終了するまでのみ）。そのため、ログイン中のみ一度、このポートで待ち受けます。',
    '({how})':
        '（{how}）',
    'Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird er nicht gespeichert.':
        'Claude：API キーは終了するまでのみ有効です – Windows の暗号化を利用できないため、保存されません。',
    'Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu eintragen oder „Key löschen“.':
        'Claude：保存されたキーをこの PC で読み取れません – もう一度入力するか、「キーを削除」を使用してください。',
    'OBS-Passwort gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'OBS のパスワードは終了するまでのみ有効です – Windows の暗号化を利用できないため、保存されません。',
    'OBS-Passwort ist nicht verschlüsselt gespeichert – die Windows-Verschlüsselung ist nicht verfügbar.':
        'OBS のパスワードは暗号化されずに保存されています – Windows の暗号化を利用できません。',
    'Spotify: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'Spotify：接続済み – 終了するまでのみ。Windows の暗号化を利用できません。',
    'Unverschlüsselt gespeichert (von früher, die Windows-Verschlüsselung ist nicht verfügbar): {names}.':
        '暗号化されずに保存されています（以前のもの。Windows の暗号化を利用できません）：{names}。',
    'YouTube: Client-Secret gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, darum wird es nicht gespeichert.':
        'YouTube：クライアントシークレットは終了するまでのみ有効です – Windows の暗号化を利用できないため、保存されません。',
    'YouTube: verbunden – nur bis zum Beenden, die Windows-Verschlüsselung ist nicht verfügbar.':
        'YouTube：接続済み – 終了するまでのみ。Windows の暗号化を利用できません。',
    'nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar':
        'このセッションのみ – Windows の暗号化を利用できません',
    'unverschlüsselt gespeichert (alt)':
        '暗号化されずに保存（旧）',
    'verschlüsselt gespeichert':
        '暗号化して保存済み',
    'Befehlspalette':
        'コマンドパレット',
    'Suchen':
        '検索',
    'Vorschläge':
        '候補',
    'OBS-Verbindung':
        'OBS 接続',
    'Port und Passwort von OBS stehen unter Verbindungen → OBS-Verbindung.':
        'OBS のポートとパスワードは「接続」→「OBS 接続」にあります。',
    'Qualität: {word} – {mbps} Mbit/s bei {size}':
        '品質：{word} – {size} で {mbps} Mbit/s',
    'Qualität: Einstellungen prüfen':
        '品質：設定を確認してください',
    'Qualität: gemessen wird während einer Aufnahme':
        '品質：録画中に測定',
    '{words} (letzte Aufnahme)':
        '{words}（前回の録画）',
    'gut':
        '良好',
    'knapp':
        'ぎりぎり',
    'matschig':
        '不鮮明',
    'Einstellungen prüfen':
        '設定を確認してください',
    'Qualität verbessern …':
        '品質を改善…',
    'OBS-Werte zurücksetzen':
        'OBS の値を元に戻す',
    'Aufnahmequalität':
        '録画品質',
    'In OBS einstellen':
        'OBS に設定',
    'Empfohlen (in OBS einzustellen):':
        '推奨（OBS に設定）：',
    'Diese Werte lassen sich nur in OBS selbst einstellen – Fog Scout zeigt, wo.':
        'これらの値は OBS 自体でしか設定できません – Fog Scout は場所を示します。',
    'Einstellen geht erst nach der Aufnahme.':
        '設定は録画後にのみ変更できます。',
    'Fog Scout stellt in OBS ein (die alten Werte werden gemerkt):':
        'Fog Scout が OBS に設定する値（以前の値は保持されます）：',
    'Die OBS-Werte von vor „In OBS einstellen“ wiederherstellen?':
        '「OBS に設定」の前の OBS の値に戻しますか？',
    'Nichts einzustellen.':
        '設定するものはありません。',
    'OBS nimmt gerade auf – Qualität erst nach der Aufnahme einstellen.':
        'OBS は録画中です – 品質は録画後に変更してください。',
    'In OBS eingestellt – OBS einmal neu starten, damit alle Werte sicher gelten.':
        'OBS に設定しました – すべての値が確実に適用されるよう、OBS を一度再起動してください。',
    'OBS-Einstellungen zurückgesetzt.':
        'OBS の設定を元に戻しました。',
    'OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ ist viel schärfer.':
        'OBS は品質「配信と同じ」または「小」で録画しています – 「区別がつかない画質」のほうがはるかに鮮明です。',
    'OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.':
        'OBS は画像を縮小しています（{base} → {out}）– そのため柔らかくなります。',
    'OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.':
        'OBS は毎秒 {fps} フレームで録画しています – 60 にすると動きがはるかに鮮明に見えます。',
    'Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen.':
        'CPU エンコーダーが追いついていません（フレームのスキップ）– グラフィックカードのエンコーダーを使用してください。',
    'Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf CQP 18 stellen (siehe Anleitung).':
        'この画像にはビットレートが低すぎます – エンコーダーのレート制御を CQP 18 に設定してください（手順を参照）。',
    'Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf.':
        'ビットレートはぎりぎり足りています – CQP 18 なら速いシーンでも画像が鮮明なままです。',
    'Ausgabeauflösung = Basisauflösung ({size})':
        '出力解像度 = 基本解像度（{size}）',
    'Bildrate 60':
        'フレームレート 60',
    'Aufnahmequalität „Kaum unterscheidbare Qualität“':
        '録画品質「区別がつかない画質」',
    'Aufnahme nicht mehr herunterskalieren':
        '録画の拡大縮小をやめる',
    'OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:':
        'OBS →「設定」→「出力」（モード「基本」）→「録画」：',
    'Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“':
        '録画品質：「区別がつかない画質、ファイルサイズ大」',
    'Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden':
        'エンコーダー：利用可能ならハードウェア（NVENC/AMD/QSV）',
    'Aufnahmeformat: MKV oder Hybrid-MP4':
        '録画フォーマット：MKV またはハイブリッド MP4',
    'Video: Ausgabeauflösung = Basisauflösung, Bildrate 60':
        '映像：出力解像度 = 基本解像度、フレームレート 60',
    'OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:':
        'OBS →「設定」→「出力」（モード「詳細」）→「録画」タブ：',
    'Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '映像エンコーダー：NVIDIA NVENC H.264 または HEVC（「配信エンコーダーを使用」ではなく）',
    'Ausgabe neu skalieren: aus':
        '出力をスケーリング：オフ',
    'x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast':
        'x264：レート制御 CRF、値 18、プリセット veryfast',
    'Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)':
        'レート制御：CQP、CQ レベル 18（HEVC は 20）',
    'Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei Durchläufe (Viertelauflösung)':
        'プリセット：P5: Slow（高品質）、チューニング：高品質、マルチパス：2 パス（1/4 解像度）',
    'Profil: high (HEVC: main), Keyframe-Intervall: 2 s':
        'プロファイル：high（HEVC：main）、キーフレーム間隔：2 秒',
    'Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.':
        'その後、短いラウンドを録画してください – カードに新しいビットレートが表示されます。',
    'Was die Aufnahme unscharf macht und wie OBS am besten eingestellt wird – was eine Anfrage setzen kann (Ausgabeauflösung, Bildrate, einfache Aufnahmequalität), stellt „In OBS einstellen“ ein, die alten Werte werden gemerkt.':
        '録画がぼやける原因と OBS の最適な設定方法 – リクエストで設定できるもの（出力解像度、フレームレート、基本の録画品質）は「OBS に設定」で設定され、以前の値は保持されます。',
    'Stellt die OBS-Werte von vor „In OBS einstellen“ wieder her.':
        '「OBS に設定」の前の OBS の値に戻します。',
    'Clips und Editor':
        'クリップとエディター',
    'Erklärung':
        '説明',
    'Sicherung und Ordner':
        'バックアップとフォルダー',
    'Wann aufgenommen wird':
        '録画するタイミング',
    'Video-Encoder: AMD HW H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '映像エンコーダー：AMD HW H.264 または HEVC（「配信エンコーダーを使用」ではなく）',
    'Frequenzsteuerung: CQP, QP-Werte 18 (HEVC 20)':
        'レート制御：CQP、QP 値 18（HEVC は 20）',
    'Voreinstellung: Qualität':
        'プリセット：Quality',
    'Video-Encoder: QuickSync H.264 oder HEVC (nicht „Stream-Encoder verwenden“)':
        '映像エンコーダー：QuickSync H.264 または HEVC（「配信エンコーダーを使用」ではなく）',
    'Frequenzsteuerung: ICQ (oder CQP), Wert 18':
        'レート制御：ICQ（または CQP）、値 18',
    'Target Usage: TU1 bis TU4 – kleiner = bessere Qualität':
        'ターゲット使用法：TU1～TU4 – 低いほど高品質',
    'Video-Encoder: der Grafikkarten-Encoder (NVENC, AMF oder QuickSync), wenn OBS einen anbietet – sonst x264':
        '映像エンコーダー：OBS が提供していればグラフィックカードのエンコーダー（NVENC、AMF または QuickSync）– なければ x264',
    'Video-Encoder: einen eigenen wählen (nicht „Stream-Encoder verwenden“), am besten den der Grafikkarte, wenn OBS einen anbietet':
        '映像エンコーダー：独自のエンコーダーを選択（「配信エンコーダーを使用」ではなく）。OBS が提供していればグラフィックカードのものが最適',
    'Frequenzsteuerung: gleichbleibende Qualität (CQP, CQ, ICQ oder CRF) um 18 statt einer festen niedrigen Bitrate':
        'レート制御：低い固定ビットレートではなく、18 前後の固定品質（CQP、CQ、ICQ または CRF）',
    'Einschätzung aus Bitrate, Auflösung, Bildrate und Codec – Bildinhalt, Bewegung, Encoder-Voreinstellung und Quelle beeinflussen das Ergebnis.':
        'ビットレート、解像度、フレームレート、コーデックからの推定値です – 画像の内容、動き、エンコーダーのプリセット、ソースによって結果は変わります。',
    'Start und Meldungen':
        '起動と通知',
    'Fog Scout kann mit Windows starten und still im Infobereich (neben der Uhr) warten, bis DBD läuft. Die Lobby-Meldung sagt dir mit einem Ton, wenn ein Match gefunden wurde.':
        'Fog Scout は Windows と同時に起動し、DBD が起動するまで通知領域（時計の横）で静かに待機できます。ロビー通知は、マッチが見つかったときに音で知らせます。',
    'Optional: OBS Studio nimmt jede Runde auf, Fog Scout sagt OBS nur, wann. Ohne OBS einfach „Weiter“.':
        '任意：OBS Studio がすべてのラウンドを録画し、Fog Scout は OBS にタイミングを伝えるだけです。OBS を使わない場合はそのまま「次へ」。',
    '1. In OBS: Werkzeuge → WebSocket-Servereinstellungen → „WebSocket-Server aktivieren“ anhaken; unter „Verbindungsinformationen anzeigen“ stehen Port und Passwort.':
        '1. OBS で：「ツール」→「WebSocket サーバー設定」→「WebSocket サーバーを有効にする」にチェック。「接続情報を表示」でポートとパスワードが表示されます。',
    '2. Port und Passwort hier eintragen und „Verbindung testen“.':
        '2. ここにポートとパスワードを入力し、「接続をテスト」をクリックしてください。',
    '3. Einen Ordner für die Aufnahmen wählen und die Aufnahmen einschalten.':
        '3. 録画用のフォルダーを選択し、録画をオンにしてください。',
    'Wie scharf OBS aufnimmt, zeigt danach die Karte „Aufnahme“ auf der Seite Aufnahmen – dort auch „Qualität verbessern …“.':
        'OBS の録画がどれだけ鮮明かは、後で「録画」ページの「録画」カードに表示されます – そこには「品質を改善…」もあります。',
    'Alles hier ist freiwillig und lässt sich später unter Einstellungen → Verbindungen einrichten. Jede Verbindung braucht eine eigene App-ID bzw. einen eigenen Key von dir – „Erklärung“ sagt, wo es sie gibt.':
        'ここにあるものはすべて任意で、後から「設定」→「接続」で設定できます。各接続には独自のアプリ ID またはキーが必要です – 取得場所は「説明」に記載されています。',
    'Fog Scout kann anzeigen, mit welchem Spielserver DBD verbunden ist (Region und Ping, auch im Overlay) – dafür fragt Windows einmal nach Administratorrechten.':
        'Fog Scout は DBD が接続しているゲームサーバーを表示できます（リージョンと Ping、オーバーレイにも）– そのために Windows が一度管理者権限を要求します。',
    'Auf der Seite Server lässt sich ausserdem festlegen, in welchen Regionen DBD Matches sucht. Das ist freiwillig.':
        '「サーバー」ページでは、DBD がマッチを探すリージョンも選択できます。これは任意です。',
    'Serverregionen auswählen …':
        'サーバーリージョンを選択…',
    'Beendet die Einrichtung und öffnet die Seite Server – dort die Regionen anhaken, in denen DBD Matches suchen soll.':
        'セットアップを終了し、「サーバー」ページを開きます – そこで DBD がマッチを探すリージョンにチェックを入れてください。',
    'Öffnet den Ordner mit Einstellungen, Runden, Log und Sicherungen im Explorer.':
        '設定、ラウンド、ログ、バックアップのあるフォルダーをエクスプローラーで開きます。',
    'Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an Claude schicken“ einschalten und einen API-Key eintragen.':
        'オフ – 「設定」→「接続」→「Claude」で「画像エディターの画像を Claude に送信する」をオンにし、API キーを入力してください。',
    'Ausschnitt ausserhalb des Bildes':
        '画像の外側の切り抜き',
    'Bereich unkenntlich machen ({x} %, {y} %)':
        '領域を隠す（{x} %、{y} %）',
    'Bilder im Bild-Editor an Claude schicken':
        '画像エディターの画像を Claude に送信する',
    'Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '画像にはプレイヤー名が写っていることがあります – Claude に送られるのは「提案」をクリックしたときのみで、縮小され、メモリ内にのみ保持されます。既に検閲した領域は検閲されたままです。統計の質問で送信されるのは、役割、キラー、マップ、リージョン、時間帯ごとの件数と割合のみ – 個別のラウンドもプレイヤー名も送信しません。',
    'Claude hat keine Antwort gegeben.':
        'Claude から回答がありませんでした。',
    'Claude zur Statistik fragen: „{q}“':
        '統計について Claude に質問：「{q}」',
    'Claude: Key eingetragen, Claude ist überall aus.':
        'Claude：キーは入力済みですが、Claude はすべての場所でオフです。',
    'Das Bild hat sich inzwischen geändert – bitte neu vorschlagen.':
        'その間に画像が変更されました – もう一度提案させてください。',
    'Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude (api.anthropic.com), verkleinert und nur im Speicher.':
        '画像にはプレイヤー名が写っていることがあります – Claude（api.anthropic.com）に送られるのはクリックしたときのみで、縮小され、メモリ内にのみ保持されます。',
    'Das Bild lässt sich nicht für Claude verkleinern.':
        'Claude 用に画像を縮小できません。',
    'Das Standbild liess sich nicht lesen – nichts gesendet.':
        '静止画を読み取れませんでした – 何も送信されていません。',
    'Die Statistik liess sich nicht zusammenfassen – Details im Log.':
        '統計を集計できませんでした – 詳細はログを参照。',
    'Drehung ohne Winkel':
        '角度のない回転',
    'Farbe ohne Werte':
        '値のない色',
    'Farbe: Helligkeit {b} %, Kontrast {c} %, Sättigung {s} %':
        '色：明るさ {b} %、コントラスト {c} %、彩度 {s} %',
    'In der Suche Statistik-Fragen an Claude stellen':
        '検索で Claude に統計の質問をできるようにする',
    'Kasten ausserhalb des Bildes':
        '画像の外側の枠',
    'Kippen':
        '上下反転',
    'Noch keine Runden – Claude hätte nichts zum Auswerten.':
        'まだラウンドがありません – Claude が確認するものがありません。',
    'Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du übernimmst.':
        '要望と、ここに表示されているとおりの画像（既に検閲した領域は検閲されたまま）を Claude に送信します。適用するまで何も変わりません。',
    'Schickt die Frage und Zähler/Quoten deiner Runden an Claude – keine einzelne Runde, keine Namen':
        '質問と、ラウンドの件数/割合を Claude に送信します – 個別のラウンドも名前も送信しません',
    'Schickt zusätzlich das Bild an der Abspielposition (verkleinert, bereits zensierte Bereiche bleiben zensiert) – damit kann Claude z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '再生ヘッドの位置の画像も送信します（縮小、既に検閲した領域は検閲されたまま）– これで Claude が例えば名前を検閲できます。画像にはプレイヤー名が写っていることがあります。',
    'Spiegeln':
        '左右反転',
    'Spiegeln ohne Richtung':
        '方向のない反転',
    'Standbild mitsenden':
        '静止画も送信',
    'Standbilder aus Aufnahmen im Clip-Editor an Claude schicken':
        'クリップエディターで録画の静止画を Claude に送信する',
    'Um {deg}° drehen':
        '{deg}° 回転',
    'Vergisst den Vorschlag; das Bild bleibt, wie es ist.':
        '提案を破棄します。画像はそのままです。',
    'Zensur nur mit Standbild':
        '検閲は静止画がある場合のみ',
    'Zensur: {style}':
        '検閲：{style}',
    'Zuschneiden auf {w} × {h} %':
        '{w} × {h} % に切り抜き',
    'unbekannte Art der Zensur':
        '不明な種類の検閲',
    'unbekannter Schritt':
        '不明な手順',
    'z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller':
        '例：プレイヤー名にモザイク、16:9 に切り抜き、少し明るく',
    'zu viele Kästen':
        '枠が多すぎます',
    'Zeigt im Bild-Editor den Reiter „Claude“: Du schreibst, was mit dem Bild passieren soll (Namen verpixeln, zuschneiden, heller), und auf „Vorschlagen“ gehen Bitte und Bild verkleinert an Claude. Das Bild kann Spielernamen zeigen; bereits zensierte Bereiche bleiben zensiert.':
        '画像エディターに「Claude」タブを表示します：画像に対して行いたいこと（名前にモザイク、切り抜き、明るく）を書くと、「提案」で要望と縮小した画像が Claude に送られます。画像にはプレイヤー名が写っていることがあります。既に検閲した領域は検閲されたままです。',
    'Erlaubt im grossen Clip-Editor das Häkchen „Standbild mitsenden“: dann geht das Bild an der Abspielposition mit, und Claude kann z. B. Namen zensieren. Das Bild kann Spielernamen zeigen.':
        '大きなクリップエディターで「静止画も送信」のチェックを使えるようにします：再生ヘッドの位置の画像も送られ、Claude が例えば名前を検閲できます。画像にはプレイヤー名が写っていることがあります。',
    'Zeigt in der Suche (Strg+F) die Zeile „Claude zur Statistik fragen“. Gesendet werden deine Frage und Zähler/Quoten deiner Runden je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von Spielern.':
        '検索（Ctrl+F）に「統計について Claude に質問」の行を表示します。送信されるのは質問と、役割、キラー、マップ、リージョン、時間帯ごとのラウンドの件数/割合のみ – 個別のラウンドもプレイヤー名も送信しません。',
    'Start: Fenster bereit nach {total} s seit Programmstart (davon {before} s bis Python).':
        '起動：プログラムの起動から {total} 秒でウィンドウの準備完了（うち Python までが {before} 秒）。',
    'Haiku 5.5 – am günstigsten':
        'Haiku 5.5 – 最安',
    'Opus 5.5 – am genauesten':
        'Opus 5.5 – 最も正確',
    'Sonnet 5.5 – halber Preis':
        'Sonnet 5.5 – 半額',
    'Modell':
        'モデル',
    'Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat {month}. Abgerechnet wird in der Anthropic Console.':
        '費用（定価での概算）：このセッション {session}（{n} 件のリクエスト）、今月 {month}。請求は Anthropic Console で行われます。',
    'Claude: Welcher Build läuft am besten?':
        'Claude：どのビルドが最も効果的？',
    'Claude: Woche zusammenfassen':
        'Claude：今週をまとめる',
    'Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?':
        '今週を先週と比べてまとめてください：何が良くなり、何が悪くなりましたか？',
    'Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?':
        '私のパークのうち最も効果的なのはどれですか – キラーとサバイバーを分けて教えてください。',
    'Fog Scout ist abgestürzt':
        'Fog Scout がクラッシュしました',
    'Fog Scout wurde am {when} unerwartet beendet. „Diagnose kopieren“ legt einen Bericht mit den Stellen des Absturzes in die Zwischenablage – zum Melden auf GitHub oder im Chat. Der Bericht enthält keine Schlüssel, Titel oder Server-Adressen.':
        'Fog Scout は {when} に予期せず終了しました。「診断情報をコピー」で、クラッシュ箇所を含むレポートがクリップボードにコピーされます – GitHub やチャットで報告するために。レポートにはキー、タイトル、サーバーアドレスは含まれません。',
    'Claude hat keine Stelle gefunden, die heraussticht.':
        'Claude は目立つ瞬間を見つけられませんでした。',
    'Claude sieht sich {n} Standbilder an …':
        'Claude が {n} 枚の静止画を確認しています…',
    'Highlights finden':
        'ハイライトを探す',
    'Schickt kleine Standbilder des Schnitts (gleichmässig verteilt und an den F8-Marken, bereits zensierte Bereiche zensiert) an Claude; Claude nennt bis zu drei Stellen für einen Short. Die Bilder können Spielernamen zeigen.':
        'カットの小さな静止画（均等に、および F8 マークの位置で。既に検閲した領域は検閲されたまま）を Claude に送信します。Claude がショート用に最大 3 つの瞬間を挙げます。画像にはプレイヤー名が写っていることがあります。',
    'Schlägt vor, nur diesen Teil zu behalten – erst „Übernehmen“ ändert den Schnitt.':
        'この部分だけを残すことを提案します – カットが変わるのは「適用」したときだけです。',
    'Namen beim Zuschauen':
        '観戦中の名前',
    'Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und den Namen oben in der Mitte – bei Bedarf verschieben.':
        '観戦中に DBD が名前を表示する場所に枠を置きます：左のやや上にあるリストと、上部中央の名前 – 必要に応じて移動してください。',
    'Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im Spielbild) – bei Bedarf verschieben.':
        'マッチ中に DBD がサバイバーの名前を表示する場所（ゲーム画面の左下）に枠を置きます – 必要に応じて移動してください。',
    'Aufnahme zeigen':
        '録画を表示',
    'Aufnahme abspielen':
        '録画を再生',
    'Zu dieser Runde gibt es keine Aufnahme.':
        'このラウンドの録画はありません。',
    'Die Aufnahme dieser Runde ist durch die Filter der Seite Aufnahmen ausgeblendet.':
        'このラウンドの録画は「録画」ページのフィルターで非表示になっています。',
    'Sitzungen':
        'セッション',
    'Killer/Survivor':
        'キラー/サバイバー',
    '{n} K':
        'K {n}',
    '{n} S':
        'S {n}',
    'Ø Dauer einer Sitzung':
        '平均セッション時間',
    'Ø Runden je Sitzung':
        'セッションあたりの平均ラウンド数',
    'Ø Warten':
        '平均待ち時間',
    'Eine Sitzung endet nach {n} Minuten ohne Runde. Es gelten die Filter oben – mit einem Rollenfilter zählt eine Sitzung nur die Runden dieser Rolle. Ø Kills, Entkommen und BP laut Stats-Seite. Doppelklick zeigt die Runden der Sitzung unter „Letzte Runden“.':
        'セッションはラウンドなしで {n} 分経過すると終了します。上のフィルターが適用されます – 役割フィルターを使うと、セッションはその役割のラウンドのみを数えます。平均キル、脱出、BP は統計ページから。ダブルクリックでセッションのラウンドを「最近のラウンド」に表示します。',
    'Blutpunkte-Stand – letzter Wert {per}':
        'ブラッドポイント残高 – 最新値 {per}',
    'Cap erreicht':
        '上限到達',
    'Cap in ≈ {n} Runden':
        '約 {n} ラウンドで上限',
    'Cap: {cap}':
        '上限：{cap}',
    'Noch kein Blutpunkte-Stand gelesen – er kommt aus der Lobby nach der Runde.':
        'ブラッドポイント残高はまだ読み取られていません – ラウンド後のロビーで取得します。',
    '{when}: Stand {bp} BP':
        '{when}：残高 {bp} BP',
    '+{n} Level':
        '+{n} レベル',
    '+{n} P':
        '+{n} P',
    'Eine Zeile oben anklicken, um den Verlauf zu sehen.':
        '上の行をクリックすると推移が表示されます。',
    'Keine Matches mit Prestige in dieser Auswahl.':
        'この選択範囲には威光のあるマッチがありません。',
    'Level':
        'レベル',
    'Matches':
        'マッチ',
    'Noch kein Prestige in dieser Auswahl – es kommt aus den Match-Daten (Userscript ab Version 3).':
        'この選択範囲にはまだ威光がありません – マッチデータ（ユーザースクリプト バージョン 3 以降）から取得します。',
    'Prestige':
        '威光',
    'Prestige und Level deiner Charaktere laut Stats-Seite (ab Userscript Version 3). „Prestige“ und „Level“ = der neueste Stand; „Zuwachs“ und „Matches“ gelten für die Filter oben. Eine Zeile anklicken zeigt darunter den Verlauf dieses Charakters. „Tempo“ = gewonnene Level pro Woche aus den Matches der letzten {days} Tage, „Nächstes P“ = wie lange es bei diesem Tempo bis zur nächsten Stufe dauert. Level steigen nur, wenn du Blutpunkte im Blutnetz ausgibst – die Prognose sagt, was bisher geschah, keine Zusage. „Main“ = dein Charakter mit den meisten Matches je Rolle. „P100“ und „Höchster“ zählen nur Charaktere, die in deinen Match-Daten vorkommen.':
        '統計ページから取得したキャラクターの威光とレベル（ユーザースクリプト バージョン 3 以降）。「威光」と「レベル」= 最新の状態。「増加」と「マッチ」は上のフィルターに従います。行をクリックすると、そのキャラクターの推移が下に表示されます。「速度」= 過去 {days} 日間のマッチで 1 週間に上がったレベル、「次の P」= そのペースで次の段階までにかかる時間。レベルはブラッドウェブでブラッドポイントを使ったときにのみ上がります – 予測はこれまでの実績を示すもので、保証ではありません。「メイン」= 役割ごとにマッチ数が最も多いキャラクター。「P100」と「最高」は、マッチデータに登場するキャラクターのみを数えます。',
    'Prestige von {name} {per}':
        '{name} の威光 {per}',
    'Zuletzt':
        '最終プレイ',
    'Zuwachs':
        '増加',
    '{when}: Prestige {p} · Level {level}':
        '{when}：威光 {p} · レベル {level}',
    '+{n} weitere':
        '他 +{n}',
    'Charaktere':
        'キャラクター',
    'Höchster':
        '最高',
    'Level diese Woche':
        '今週のレベル',
    'Main':
        'メイン',
    'Meilenstein: {name} ist jetzt Prestige {p}':
        '節目：{name} が威光 {p} になりました',
    'Nächstes P':
        '次の P',
    'P100 erreicht':
        'P100 到達',
    'Prestige gesamt':
        '威光の合計',
    'alle Charaktere':
        '全キャラクター',
    'seit Montag':
        '月曜日から',
    '{k} Killer · {s} Survivor':
        'キラー {k} · サバイバー {s}',
    '{name} ist jetzt Prestige {p}':
        '{name} が威光 {p} になりました',
    '{name} · Level {level}':
        '{name} · レベル {level}',
    '{n} Level/Woche':
        '{n} レベル/週',
    '≈ 1 Tag':
        '約 1 日',
    '≈ 1 Woche':
        '約 1 週間',
    '≈ {n} Tage':
        '約 {n} 日',
    '≈ {n} Wochen':
        '約 {n} 週間',
    '{n} Charaktere':
        '{n} キャラクター',
    'P100':
        'P100',
    '{n}× Killer':
        'キラー {n} 回',
    '{n}× Survivor':
        'サバイバー {n} 回',
    '{n}× Farming':
        'ファーミング {n} 回',
    '{n}× Custom Game':
        'カスタムマッチ {n} 回',
    '{n}× ohne Rolle':
        '役割なし {n} 回',
    'Zeigt, was diese Kachel zählt':
        'このタイルが数えるものを表示します',
    'Diese Runden sind durch die Filter der Statistik ausgeblendet.':
        'これらのラウンドは統計のフィルターで非表示になっています。',
    'Automatisch (zuletzt benutztes Gerät)':
        '自動（最後に使用したデバイス）',
    'Dunkle Fläche hinter den Eingaben':
        '入力の背後に暗い領域',
    'EINGABEN':
        '入力',
    'Eingaben im Spiel':
        'ゲーム内の入力',
    'Eingaben im Spiel zeigen (Tasten, Maus, Gamepad)':
        'ゲーム内に入力を表示する（キー、マウス、ゲームパッド）',
    'Gamepad':
        'ゲームパッド',
    'Gerät':
        'デバイス',
    'Tastatur und Maus':
        'キーボードとマウス',
    'Eine halb durchsichtige dunkle Fläche mit runden Ecken hinter den Tasten.':
        'キーの背後に角の丸い半透明の暗い領域を表示します。',
    'wartet auf eine Runde':
        'ラウンドを待機中',
    'Eingaben mit der Aufnahme speichern (für den Clip-Editor)':
        '入力を録画とともに保存する（クリップエディター用）',
    'Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). Eine offizielle Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.':
        'Fog Scout が表示するのは、次のキーのうち現在押されているものだけです：W、A、S、D、Q、E、R、スペース、Shift、Ctrl、マウスボタン、ゲームパッド（ボタン、トリガー、スティック）。読み取るのはラウンド中、かつ DBD がアクティブウィンドウの間のみ – 他のプログラムでの入力を Fog Scout が見ることはありません。ログへの記録も送信も一切せず、ゲームにも何も送りません。「入力を録画とともに保存する」を使うと、ラウンドのキー入力が OBS の録画の隣にファイルとして保存されます（クリップエディター用）。Behaviour はこのような表示を公式に承認していませんが、ゲーム上の有利にはなりません。',
    'Gelesen werden nur W, A, S, D, Q, E, R, Leertaste, Shift, Strg, die Maustasten und ein Gamepad – nur während einer Runde und nur, solange DBD vorne ist. Gesendet wird nichts; gespeichert nur mit dem Häkchen oben, als Datei neben der eigenen Aufnahme.':
        '読み取るのは W、A、S、D、Q、E、R、スペース、Shift、Ctrl、マウスボタン、ゲームパッドのみ – ラウンド中、かつ DBD が前面にある間のみです。何も送信しません。保存は上のチェックボックスを使った場合のみで、ご自身の録画の隣にファイルとして保存されます。',
    'Eine Karte im Spiel zeigt, welche Tasten, Maustasten oder Gamepad-Knöpfe du gerade drückst – wie bei Streamern. Gelesen wird nur eine feste Liste von Tasten, nur während einer Runde und nur, solange DBD vorne ist; gesendet wird nichts, gespeichert nur mit „Eingaben mit der Aufnahme speichern“.':
        'ゲーム内のカードに、現在押しているキー、マウスボタン、ゲームパッドのボタンを表示します – 配信者がよく使う表示です。読み取るのは決められたキーのリストのみ、ラウンド中、かつ DBD が前面にある間のみです。何も送信せず、保存は「入力を録画とともに保存する」を使った場合のみです。',
    'Mit OBS-Aufnahmen: die gedrückten Tasten der Runde kommen als kleine Datei neben die Aufnahme – der Clip-Editor zeigt sie als Spur und kann die Karte ins Video einbrennen. Die Datei wird mit der Aufnahme verschoben und gelöscht.':
        'OBS の録画時：ラウンド中に押していたキーを録画の隣の小さなファイルに保存します – クリップエディターはそれをトラックとして表示し、カードを動画に焼き込めます。ファイルは録画とともに移動・削除されます。',
    'Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme speichern“). Clips aus F8 haben keine.':
        '録画の隣のファイルから（「オーバーレイ」›「入力」›「入力を録画とともに保存する」）。F8 クリップにはありません。',
    'Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet).':
        'ラウンド中に押していたキーのカードを完成した動画に入れます – 選んだ角に、カットに合わせて（速度と逆再生も含む）。',
    'Dunkle Fläche hinter den Tasten':
        'キーの背後に暗い領域',
    'Ecke':
        '角',
    'Eine halb durchsichtige dunkle Fläche hinter der Karte.':
        'カードの背後に半透明の暗い領域を表示します。',
    'Eingaben im Export zeigen':
        'エクスポートに入力を表示する',
    'Höhe der Karte im Verhältnis zur Bildhöhe.':
        '画像の高さに対するカードの高さ。',
    'Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade benutzt wurde.':
        'カードが表示する画面 – 自動では直前に使ったデバイス。',
    'Wo die Karte im Bild liegt.':
        '画像内でのカードの位置。',
    'Claude baut einen Short aus {n} Standbildern …':
        'Claude が {n} 枚の静止画からショートを作成しています…',
    'Clip um Moment':
        '瞬間周辺のクリップ',
    'Der Schnitt hat sich inzwischen geändert – bitte noch einmal.':
        'その間にカットが変更されました – もう一度お試しください。',
    'Der Schnitt wird der markierte Moment ({before} s davor bis {after} s danach).':
        'カットを選択した瞬間（{before} 秒前から {after} 秒後まで）にします。',
    'Die Bilder liessen sich nicht lesen.':
        '画像を読み取れませんでした。',
    'F8-Marke':
        'F8 マーク',
    'Gerade nicht möglich – erst die laufende Bearbeitung beenden.':
        '現在はできません – 先に現在の編集を終えてください。',
    'Kein Ladebildschirm am Anfang oder Ende gefunden.':
        '先頭にも末尾にもロード画面が見つかりません。',
    'Kein Leerlauf gefunden.':
        'アイドル区間が見つかりません。',
    'Ladebildschirm abschneiden':
        'ロード画面をカット',
    'Leerlauf kürzen':
        'アイドル時間をトリミング',
    'Momente':
        '瞬間',
    'Schickt Standbilder an den gefundenen Momenten (aus Tasten, Spielton und F8-Marken, nur als Zahlen) und den Schnitt an Claude; Claude schlägt einen ganzen Short vor – Ausschnitt, Zeitlupe, Titel, Untertitel. Erst „Übernehmen“ ändert den Schnitt. Die Bilder können Spielernamen zeigen.':
        '見つかった瞬間（キー、ゲーム音、F8 マークから。数値のみ）の静止画とカットを Claude に送信します。Claude がショート全体を提案します – 範囲、スローモーション、タイトル、字幕。カットが変わるのは「適用」したときだけです。画像にはプレイヤー名が写っていることがあります。',
    'Schneidet Stellen heraus, an denen mindestens {n} s nichts gedrückt war (aus den Eingaben der Aufnahme) – ein Schritt zum Rückgängigmachen.':
        '少なくとも {n} 秒間何も押されていない区間をカットします（録画の入力から）– 1 ステップで元に戻せます。',
    'Sehe mir Anfang und Ende an …':
        '先頭と末尾を確認中…',
    'Short vorschlagen':
        'ショートを提案',
    'Sieht sich die ersten und letzten {n} s an und schneidet einen schwarzen Anfang oder ein schwarzes Ende weg – ein Schritt zum Rückgängigmachen.':
        '最初と最後の {n} 秒を確認し、黒い先頭または末尾をカットします – 1 ステップで元に戻せます。',
    'laut':
        '大音量',
    'viele Tasten':
        '多数のキー',
    '{n} Leerlauf-Stelle(n) gekürzt ({seconds} s) – Strg+Z macht es rückgängig.':
        'アイドル区間を {n} 個トリミングしました（{seconds} 秒）– Ctrl+Z で元に戻せます。',
    '{n} schwarze Stelle(n) abgeschnitten ({seconds} s) – Strg+Z macht es rückgängig.':
        '黒い区間を {n} 個カットしました（{seconds} 秒）– Ctrl+Z で元に戻せます。',
    'Anordnen':
        '配置',
    'Anordnen aktiv – auch im Spiel: Elemente ziehen · Pfeiltasten = fein (Shift = 10 px) · Tab = nächstes Element · Esc = fertig':
        '配置中 – ゲーム内でも：要素をドラッグ · 矢印キー = 微調整（Shift = 10 px）· Tab = 次の要素 · Esc = 完了',
    'Anordnen: alle Elemente mit der Maus ziehen – in der Vorschau und direkt im Spiel. Strg+Mausrad ändert die Grösse, Esc beendet.':
        '配置：各要素をマウスでドラッグします – プレビューでも、ゲーム内でも直接。Ctrl+ホイールでサイズを変更、Esc で終了。',
    'Automatisch: im schwarzen Rand neben dem Spielbild bzw. neben dem DBD-Fenster. Frei platzieren: „Anordnen“ oder eine Schnellposition.':
        '自動：ゲーム画面の横の黒帯、または DBD ウィンドウの横。自由に配置するには：「配置」またはクイック配置。',
    'CPU, GPU, RAM':
        'CPU、GPU、RAM',
    'Callout-Karte der Map':
        'マップのコールアウトマップ',
    'Die Linien in der Vorschau mit „Anordnen“ ziehen – Karte, Systemwerte, Heute und Musik bleiben im Balken dazwischen.':
        '「配置」中にプレビューで線をドラッグしてください – マップ、システム値、今日、音楽は帯の中でその間に収まります。',
    'Ein- oder ausblenden':
        '表示または非表示',
    'Elemente':
        '要素',
    'Entsperren: wieder verschiebbar':
        'ロック解除：再び移動できます',
    'Fokus':
        'フォーカス',
    'Frei platzieren: „Anordnen“, eine Schnellposition oder Vorgabe „eigene Position“.':
        '自由に配置するには：「配置」、クイック配置、または設定「独自の位置」。',
    'Gesperrt – erst entsperren':
        'ロック中 – 先にロックを解除してください',
    'Gilt für alle Elemente':
        'すべての要素に適用',
    'Grenzen und Platz':
        '境界と余白',
    'Grenzlinie: ziehen, bis wohin die Elemente im Balken reichen':
        '境界線：帯の中の要素が届いてよい位置までドラッグしてください',
    'Grösse und Deckkraft':
        'サイズと不透明度',
    'Grösse von {name}: Ecke ziehen':
        '{name} のサイズ：角をドラッグ',
    'Klick auf ein Element wählt es. Mit „Anordnen“: Element ziehen = verschieben (der gestrichelte Rahmen zeigt, wo es landet), an der Ecke ziehen oder Strg+Mausrad = Grösse, Rechtsklick = Menü. Ende mit „Fertig“ oder Esc.':
        '要素をクリックすると選択されます。「配置」中：要素をドラッグ = 移動（点線の枠が移動先を示します）、角をドラッグまたは Ctrl+ホイール = サイズ、右クリック = メニュー。「完了」または Esc で終了します。',
    'Klick wählt ein Element · „Anordnen“ schaltet das Verschieben ein – hier und im Spiel':
        'クリックで要素を選択 · 「配置」で移動モードをオン – ここでもゲーム内でも',
    'Klick wählt {name}':
        'クリックで {name} を選択',
    'Layout für {size}':
        '{size} のレイアウト',
    'Läuft gerade':
        '再生中',
    'Mitte':
        '中央',
    'Nach {where} legen (mit Rand)':
        '{where} に配置（余白付き）',
    'Position und Grösse werden je DBD-Fenstergrösse gemerkt (Reiter Allgemein).':
        '位置とサイズは DBD のウィンドウサイズごとに保持されます（「一般」タブ）。',
    'Runden und Zeit heute':
        '今日のラウンドと時間',
    'Schnellposition':
        'クイック配置',
    'Sperren':
        'ロック',
    'Sperren: im Modus „Anordnen“ nicht mehr verschiebbar':
        'ロック：「配置」で移動しなくなります',
    'Stil, Abstand, Grenzen, Discord':
        'スタイル、間隔、境界、Discord',
    'Tasten und Gamepad':
        'キーとゲームパッド',
    'Timer, Bilanz, Server':
        'タイマー、記録、サーバー',
    'Verhalten':
        '動作',
    'Zeilen':
        '行',
    'Zurück an den automatischen Platz (im schwarzen Balken, neben den anderen)':
        '自動の位置に戻す（黒帯の中、他の要素の横）',
    'eigener Platz':
        '独自の位置',
    'eingerastet':
        'スナップ',
    'graue Linien in den Balken = Grenzen (aus) – eine ziehen schaltet sie ein':
        '帯の中の灰色の線 = 境界（オフ）– ドラッグするとオンになります',
    'links Mitte':
        '左中央',
    'oben Mitte':
        '上中央',
    'rastet an Mitte, Balken und anderen ein (Alt = frei)':
        '中央、帯、他の要素にスナップします（Alt = 自由）',
    'rechts Mitte':
        '右中央',
    'unten Mitte':
        '下中央',
    '{name} entsperrt.':
        '{name} のロックを解除しました。',
    '{name} gesperrt – bleibt beim Anordnen, wo es ist.':
        '{name} をロックしました – 配置中もその場所に留まります。',
    '{name} ist gesperrt – das Schloss in der Liste löst es':
        '{name} はロック中です – リストの鍵で解除できます',
    '{name}: ziehen = verschieben · Ecke oder Strg+Mausrad = Grösse · Rechtsklick = Menü':
        '{name}：ドラッグ = 移動 · 角または Ctrl+ホイール = サイズ · 右クリック = メニュー',
    'Üblicher Platz':
        '通常の位置',
    '„Overlay testen“ zeigt die Karte sofort, mit „Anordnen“ ziehst du sie hin.':
        '「オーバーレイをテスト」でマップがすぐに表示され、「配置」でそこまでドラッグできます。',
    'Nur die Vorschau: Liste und Einstellungen weg, die Navigation schmal – die ganze Fläche zum Anordnen. Esc oder nochmal klicken beendet es.':
        'プレビューのみ：リストと設定を隠し、ナビゲーションを狭くします – 領域全体を配置に使えます。Esc または別の場所をクリックで終了します。',
}
