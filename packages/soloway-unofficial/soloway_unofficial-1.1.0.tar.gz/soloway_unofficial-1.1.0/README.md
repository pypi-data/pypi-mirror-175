# Soloway SDK (Unofficial)

Простейшая реализация SDK для https://dsp.soloway.ru/

### Реализованные методы
* ``/login``
* ``/whoami``
* ``/clients/{clientGuid}/placements``
* ``/placements_stat``
* ``/placements/{placementGuid}/stat``

## Установка
```bash    
    $ pip install soloway-unofficial
```

## Использование

```python
from soloway_unofficial import Client

client = Client("YOUR_LOGIN", "YOUR_PASSWORD")
```    

Получение статистики размещений по всем кампаниям.
```python
start_date = datetime.date(2022, 1,1)
stop_date = datetime.date(2022, 12,31)
data = client.get_placements_stat_all(start_date, stop_date)
```    

```python
start_date = datetime.date(2022, 1,1)
stop_date = datetime.date(2022, 12,31)
data = client.get_placements_stat(list["PLACEMENT_ID"],start_date, stop_date)
```    

Получение статистики по всем кампаниям по дням.
```python        
start_date = datetime.date(2022, 1,1)
stop_date = datetime.date(2022, 12,31)
data = client.get_placements_stat_by_day(start_date, stop_date)
```

Получение статистики по выбранной кампании по дням.
```python    
start_date = datetime.date(2022, 1,1)
stop_date = datetime.date(2022, 12,31)    
data = client.get_placement_stat_by_day("PLACEMENT_ID", start_date, stop_date)
```