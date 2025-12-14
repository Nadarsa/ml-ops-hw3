# MLOPS 3

## Production Deployment

Сервис автоматически деплоится на Render.com при каждом push в main 

Сервис доступен по адресу: **https://ml-ops-hw3.onrender.com**

Первый запрос после периода неактивности (15 минут) может занять 30-60 секунд (cold start) из-за ограничений бесплатного тарифа. Последующие запросы обрабатываются мгновенно.

## API
GET /health - состояние сервиса и версия модели  
```bash
curl https://ml-ops-hw3.onrender.com/health
```

POST /predict - предсказание модели  
```bash
curl -X POST https://ml-ops-hw3.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Screenshot
![Api call](/screenshots/api-call-screenshont.jpg)

## Стратегия
Blue-Green deployment позволяет иметь две идентичные production среды:
- **Blue** (v1.0.0) - текущая стабильная версия на порту 8080
- **Green** (v1.1.0) - новая версия для тестирования на порту 8081

Сначала запускаем обе версии параллельно, тестируем новую, и если все работает - переключаем трафик. Если что-то пошло не так - возвращаемся на старую версию.

## Шаги запуска

### Обучить модель
`python train.py`

### Локально

```bash
pip install -r requirements.txt
python train.py
uvicorn app.main:app --port 8080
```

Открыть http://localhost:8080/docs для документации.

### С Docker (Blue-Green)

```bash

# Запустить Blue версию (v1.0.0)
docker build -t ml-service:v1 .
docker-compose -f docker-compose.blue.yml up -d

# Запустить Green версию (v1.1.0)
docker-compose -f docker-compose.green.yml up -d

# Проверить обе версии
curl http://localhost:8080/health
curl http://localhost:8081/health
```

### Переключение между версиями

Протестировать Green

```bash
curl -X POST http://localhost:8081/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```
Если все работает - переключить Nginx на порт 8081
В nginx.conf изменить upstream ml_backend с 8080 на 8081
Затем: sudo nginx -s reload

Откат при проблемах
Вернуть Nginx обратно на 8080 и перезагрузить
