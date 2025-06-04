# zk-snark-iot

Проект демонстрирует, как можно использовать zk-SNARK доказательства для верификации условий, полученных от IoT-устройства (например, пульс выше порогового значения) **без раскрытия самих данных**.  

## Структура проекта

```bash
zk-snark-iot/
├── backend/                # [планируется] Серверная логика взаимодействия с датчиком и контрактом
├── contract/
│   └── verifier.sol        # Контракт на Solidity для верификации доказательства
├── circom/
│   ├── pulse_check.circom  # Основная схема Circom
│   ├── input.json          # Пример входных данных (пульс, порог, алерт)
│   ├── generate_proof.sh   # Скрипт генерации всех артефактов
│   └── ...                 # Все промежуточные и финальные файлы схемы, zkey, wasm и пр.
├── docker/
│   └── Dockerfile          # Образ со snarkjs и зависимостями
├── docker-compose.yml      # Compose-файл для запуска среды
└── README.md
```

---

## Как развернуть и протестировать локально

> Проект можно запустить **полностью локально**, без подключения датчиков.

### 1. Клонировать и зайти в проект

```bash
git clone https://github.com/your-name/zk-snark-iot.git
cd zk-snark-iot
```

### 2. Собрать Docker-окружение

```bash
docker compose up --build
```

### 3. Зайти внутрь контейнера

```bash
docker exec -it zk-snark-iot-zk-1 bash
```

### 4. Проверить работу схемы

Внутри контейнера выполните:

```bash
cd /app/circom
node pulse_check_js/generate_witness.js pulse_check_js/pulse_check.wasm input.json witness.wtns
snarkjs groth16 prove pulse_check.zkey witness.wtns proof.json public.json
snarkjs groth16 verify verification_key.json public.json proof.json
```

Если всё работает корректно, вы увидите:

```
[INFO]  snarkJS: OK!
```

---

## Пример входных данных (`input.json`)

```json
{
  "pulse": "90",
  "threshold": "80",
  "alert": "1"
}
```

Схема проверяет, что:

```text
alert * (pulse - threshold) == (pulse - threshold)
```

Т.е. если `pulse > threshold`, то `alert == 1`. В противном случае схема не будет удовлетворена.

---

## Solidity-смарт-контракт

Файл `contract/verifier.sol` можно задеплоить в любую EVM-среду (например, в Hardhat, Remix или Polygon), чтобы проверять доказательства вне цепочки.

---

## Что дальше

- Подключить ESP32 + датчик (например, MAX30102) и отправлять значения `pulse` через POST-запрос.
- Реализовать `backend/` часть, которая:
  - Получает значения с датчика
  - Формирует `input.json`
  - Вызывает генерацию доказательства и верификацию через контракт

