
from evaluer import evaluer, charger
from classifieur import CONSIGNE_EXEMPLES

evaluer(
    "qwen/qwen3.8-27b",
    charger(),
    consigne=CONSIGNE_EXEMPLES,
    etiquette="qwen/qwen3.8-27b + 4 exemples"
)
