
CATEGORIES = {
    'futebol': [
        'futebol',
        'mesa redonda',
        'bola da vez',
        'soccer',
        'bate bola',
        'resenha',
        'campeonato alemão',
        'campeonato francês',
        'linha de passe',
        'borussia dortmund',
        'campeonato português',
        'supercopa da inglaterra',
        'premier league',
        'copa do rei',
        'george best',
    ],
    'jornalismo': [
        'sportscenter',
        'espn agora'
    ],
    'americanos': [
        'nfl',
        'nhl',
        'nba',
        'mlb',
        'baseball',
        'hockey',
        'basketball'
    ],
    'radicais': [
        'x games'
    ],
    'esports': [
        'esports',
        'league of legends',
        'lol',
        'multiplayer',
    ]
}

def get_category(name):
    name = name.lower()
    for category in CATEGORIES:
        for token in CATEGORIES[category]:
            if token in name:
                return category
    else:
        return 'desconhecido'
