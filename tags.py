import texts

# t.me/Bot?start=zakup_Vodiy_Bozor -> kanal zakupi, kanal nomi "Vodiy Bozor"
ZAKUP_PREFIX = "zakup_"


def lead_tags(source: str) -> list[str]:
    """Manbaga qarab CRM teglarini qaytaradi."""
    if source.lower().startswith(ZAKUP_PREFIX):
        channel = source[len(ZAKUP_PREFIX):].replace("_", " ").strip()
        tags = [tag.format(channel=channel) for tag in texts.TAGS_ZAKUP]
    else:
        tags = list(texts.TAGS_TG_ADS)
    return [tag for tag in tags if tag]
