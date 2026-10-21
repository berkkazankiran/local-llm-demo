import json
from urllib.request import Request, urlopen


def modele_sor(soru):
    adres = "http://127.0.0.1:11434/api/chat"

    veri = {
        "model": "llama3.2:3b",
        "messages": [
            {"role": "user", "content": soru}
        ],
        "stream": False
    }

    govde = json.dumps(veri).encode("utf-8")

    istek = Request(
        adres,
        data=govde,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(istek, timeout=300) as yanit:
        sonuc = json.loads(yanit.read().decode("utf-8"))

    return sonuc["message"]["content"]


if __name__ == "__main__":
    soru = input("Sorunuz: ")
    cevap = modele_sor(soru)
    print("Modelin cevabı:", cevap)
