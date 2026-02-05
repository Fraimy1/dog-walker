TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "welcome": "Привет! Выберите язык:",
        "language_set": "Язык установлен. Теперь вы можете выгуливать собаку!",
        "walk_button": "🐕 Выгулять собаку",
        "didnt_poop": "💩 Не покакал",
        "long_walk": "🦮 Долгая прогулка",
        "send": "✅ Отправить",
        "walk_started": "Выберите параметры прогулки или нажмите «Отправить»:",
        "walk_logged": "🐕 {username} выгулял собаку в {time}",
        "additional": "Дополнительно: {params}",
        "param_didnt_poop": "не покакал",
        "param_long_walk": "долгая прогулка",
        "walk_sent": "Прогулка записана!",
        "no_active_walk": "Нет активной прогулки. Нажмите кнопку «Выгулять собаку».",
        "param_toggled": "Параметр обновлён.",
    },
    "en": {
        "welcome": "Hello! Choose your language:",
        "language_set": "Language set. Now you can walk the dog!",
        "walk_button": "🐕 Walk the dog",
        "didnt_poop": "💩 Didn't poop",
        "long_walk": "🦮 Long walk",
        "send": "✅ Send",
        "walk_started": "Select walk parameters or press «Send»:",
        "walk_logged": "🐕 {username} walked the dog at {time}",
        "additional": "Additional: {params}",
        "param_didnt_poop": "didn't poop",
        "param_long_walk": "long walk",
        "walk_sent": "Walk logged!",
        "no_active_walk": "No active walk. Press «Walk the dog» button.",
        "param_toggled": "Parameter updated.",
    },
}


def get_text(key: str, lang: str = "ru") -> str:
    """Get localized text by key."""
    return TEXTS.get(lang, TEXTS["ru"]).get(key, key)
