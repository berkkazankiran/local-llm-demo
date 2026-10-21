# Local LLM API Demo

Bu projede bilgisayarımda çalışan Llama 3.2 3B modeline Ollama API üzerinden basit bir soru gönderdim. Önce Quickstart örneğindeki cURL yapısıyla tek bir API çağrısı yaptım. Ardından aynı isteği Python'da yazdığım `modele_sor()` fonksiyonu ile gönderdim.

Tool calling kullanılmadı. Python fonksiyonunu program doğrudan çağırır; model herhangi bir Python fonksiyonunu seçmez veya çalıştırmaz. Python kodu 100 satırın altındadır.

## Gereksinimler

- Python 3.12 (çalışmanın yapıldığı sürüm)
- Ollama
- `llama3.2:3b` modeli
- cURL (Windows'ta `curl.exe`)

Ek Python paketi veya API anahtarı gerekmez. Kod Python standart kütüphanesini kullanır.

## Kurulum

1. [Ollama'yı](https://ollama.com/download/windows) kurup açın.
2. Terminalde modeli indirin:

```powershell
ollama pull llama3.2:3b
```

3. İndirilen modeli kontrol edin:

```powershell
ollama list
```

İstekler gönderilirken Ollama çalışıyor olmalıdır. API adresi `http://127.0.0.1:11434/api/chat` şeklindedir. `127.0.0.1`, kodun çalıştığı bilgisayarı ifade eder.

## cURL ile tek API çağrısı

Aşağıdaki komutu Windows CMD'de çalıştırın:

```bat
curl.exe http://127.0.0.1:11434/api/chat -H "Content-Type: application/json" -d "{\"model\":\"llama3.2:3b\",\"messages\":[{\"role\":\"user\",\"content\":\"What is the capital of Turkey? Answer in one sentence.\"}],\"stream\":false}"
```

Aynı komut `curl_test.cmd` dosyasında da bulunur. PowerShell'den çalıştırmak için:

```powershell
.\curl_test.cmd
```

Komut JSON verisi içeren bir HTTP POST isteği gönderir. `model` modeli, `messages` kullanıcı sorusunu, `stream` yanıtın gönderilme biçimini belirler. Dönen JSON içindeki `message.content` alanı modelin cevap metnidir.

## Python ile çalıştırma

Terminalde proje klasörüne geçip çalıştırın:

```powershell
python main.py
```

`Sorunuz:` yazısı geldiğinde soruyu girin:

```text
Sorunuz: What is the capital of Turkey? Answer in one sentence.
Modelin cevabı: The capital of Turkey is Ankara.
```

Bu, çalışmada alınan örnek yanıttır. Modelin cevap metni farklı çalıştırmalarda değişebilir.

## Python kodunun işleyişi

1. `json`, istek ve yanıt verilerini JSON ile Python sözlüğü arasında dönüştürür.
2. `Request` ve `urlopen`, HTTP isteğini oluşturmak ve göndermek için kullanılır.
3. `modele_sor(soru)`, kullanıcı sorusunu parametre olarak alır.
4. `veri`, model adını, kullanıcı mesajını ve `stream: False` ayarını içerir.
5. `json.dumps()` sözlüğü JSON metnine çevirir; `encode()` UTF-8 baytlarına dönüştürür.
6. `Request`, JSON gövdesi ve içerik türü başlığı ile POST isteğini hazırlar.
7. `urlopen`, isteği gönderir. `timeout=300`, soket işlemlerinin zaman aşımını saniye cinsinden ayarlar.
8. `read()` yanıtı okur, `decode()` metne çevirir, `json.loads()` sözlüğe dönüştürür.
9. `return`, yanıtın yalnızca `message.content` alanını döndürür.
10. Dosya doğrudan çalıştırıldığında `input()` soruyu alır, fonksiyon çağrılır ve `print()` cevabı gösterir.

Her çalıştırmada bir soru için tek API isteği yapılır. Önceki soruların geçmişi gönderilmez.

## Streaming karşılaştırması

| Ayar | Gözlenen davranış |
| --- | --- |
| `stream: true` | Yanıt üretilirken ayrı JSON parçaları gelir. Ara parçalarda `done: false`, son parçada `done: true` görülür. |
| `stream: false` | Tamamlanan yanıt tek JSON nesnesi olarak gelir ve `done: true` içerir. |

Streaming, bütün alternatif tahminleri veya kelime olasılıklarını göstermez. Üretilen çıktıyı parçalar halinde iletir; her parça tam bir kelime olmak zorunda değildir. Projede istenen ayar `false` olduğu için hem cURL hem Python örneğinde bu ayar kullanılmıştır. JSON'da `false`, Python'da `False` yazılır.

## Dosyalar

- `main.py`: Kendi fonksiyonum üzerinden yerel modele istek gönderir.
- `curl_test.cmd`: Tek cURL isteğini çalıştırır.
- `.gitignore`: Geçici Python dosyalarını ve sanal ortamları Git dışında tutar.
- `README.md`: Kurulum, çalıştırma ve kod açıklamalarını içerir.

## Sınırlar

Modelin yanıt vermesi, cevabının her zaman doğru olduğu anlamına gelmez. Program bağlantı veya model hatalarını ayrıca yakalamaz; bu durumda Python hata çıktısı gösterir.

## Başvurulan dokümantasyon

- [Ollama Quickstart](https://docs.ollama.com/quickstart)
- [Chat API](https://docs.ollama.com/api/chat)
- [Streaming](https://docs.ollama.com/capabilities/streaming)
