Rendered banners, not game pictures (1.49): the map name, the line and the realm drawn with Noto Sans fonts on a
dark noisy frame of 3440×1440, laid out like the real banner. They test that the models, the names in `maps.json`
and the crop for other scripts work together – not how the game's own fonts read. Each JSON says where the JPEG
sits in the captured region (`offset` in `roi`). Real banners belong in `tests/data/corpus`. The `*-one-line` banners (1.49.2) draw a long name on one line with a line as long as the name, as the game does
in Russian – one in a 3440×1440 frame, one in 2560×1440 without bars.
