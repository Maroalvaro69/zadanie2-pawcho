# zadanie2-pawcho
Automatyczne budowanie i publikacja obrazu Dockera – PAwChO Zadanie 2

## 🎯 Cel projektu

Celem projektu jest zautomatyzowanie procesu budowania obrazu Dockera na podstawie aplikacji z Zadania 1 oraz przesłanie go do **publicznego rejestru obrazów GHCR** (GitHub Container Registry) z wykorzystaniem GitHub Actions. Proces ten dodatkowo:

- wspiera wiele architektur (`linux/amd64`, `linux/arm64`),
- korzysta z cache przechowywanego w **publicznym repozytorium DockerHub**,
- wykonuje **skan bezpieczeństwa CVE** przy użyciu narzędzia Trivy.

---

## ⚙️ Technologie

- **Docker**
- **DockerHub** (cache)
- **GHCR (GitHub Container Registry)**
- **GitHub Actions**
- **Trivy** – skaner bezpieczeństwa

---

## 🔄 Proces CI/CD w GitHub Actions

Workflow `build-and-push.yml` realizuje automatyczne:

1. **Sprawdzenie kodu z repozytorium**
2. **Logowanie do GHCR (GitHub Container Registry)**
3. **Logowanie do DockerHub w celu pobrania i zapisu cache**
4. **Budowa obrazu z cache dla `linux/amd64` i `linux/arm64`**
5. **Skanowanie obrazu Trivy (CVE)**
6. **Push do GHCR tylko przy braku luk HIGH/CRITICAL**

---

## 📦 Tagowanie obrazów

Obraz jest tagowany jako:

ghcr.io/maroalvaro69/pawcho-app:latest

Użycie `latest` pozwala na proste wdrażanie najnowszej wersji. W przyszłości można łatwo rozszerzyć to o np. `:v1.0.0` lub `:${{ github.sha }}`.

## 🧠 Cache – konfiguracja i uzasadnienie

Cache warstw budowania obrazu wykorzystuje backend `registry` i tryb `max`. Pozwala to na:

- skrócenie czasu budowy,
- reużycie warstw między commitami.

**Cache jest przechowywany w:**
docker.io/marekgornicki/cache-pawcho:cache


Repozytorium to zostało ustawione jako **publiczne**. Tryb `mode=max` zapewnia optymalne wykorzystanie cache'u, co zwiększa wydajność i zmniejsza koszty.

Źródło: [Docker Buildx cache](https://docs.docker.com/build/cache/backends/registry/)

---

## 🔒 Trivy – skan bezpieczeństwa

Workflow wykorzystuje **Trivy** do skanowania obrazu pod kątem luk bezpieczeństwa. Obraz zostanie wypchnięty tylko wtedy, gdy nie zawiera żadnych luk o poziomie:

- `HIGH`
- `CRITICAL`

Składnia kroku:

- name: Scan pushed image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/maroalvaro69/pawcho-app:latest
    format: table
    exit-code: 1
    ignore-unfixed: true
    severity: HIGH,CRITICAL
Użycie Trivy jest szybkie, proste i nie wymaga osobnych konfiguracji (jak np. Docker Scout), co czyni go optymalnym wyborem.

🔐 Sekrety GitHub Actions
W repozytorium ustawiono trzy zmienne środowiskowe w sekcji Settings → Secrets and variables → Actions → Repository secrets:

Nazwa	                Opis
GHCR_TOKEN	            Token PAT z GitHub do publikacji obrazu do GHCR
DOCKERHUB_USERNAME	    Login DockerHub
DOCKERHUB_TOKEN	        Token dostępu DockerHub z uprawnieniami Write & Read

📂 Struktura projektu

├── .github/
│   └── workflows/
│       └── build-and-push.yml
├── Dockerfile
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── README.md
