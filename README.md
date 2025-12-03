# alos-ani-mvp
# ALOS ANI MVP

**ALOS (Advanced Logistics Operating System)** – региональная логистическая OS.  
Этот репозиторий – минимальный прототип модуля **ANI (Automated Neural Inspector)** для таможенной классификации.

## Что делает этот MVP

- Нормализует "грязные" описания товаров на армянском / русском / смеси языков
  (например: `բլուտուզ խոսփաքեր`) в латиницу.
- Кодирует текст в эмбеддинги с помощью `sentence-transformers`.
- Ищет ближайшее описание в маленькой справочной базе и возвращает:
  - предполагаемый HS-код,
  - флаг риска (low / encryption / dual-use),
  - значение confidence.

Это **не production-код**, а демонстрация архитектуры.

## Установка

```bash
git clone https://github.com/USERNAME/alos-ani-mvp.git
cd alos-ani-mvp
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
