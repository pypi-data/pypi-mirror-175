# Prioridades Clickup 

<br>

sacar las prioridades de una(varias) vista(s) de clickup ᕙ( • ᴗ • )ᕗ

<br>

## Prerequisitos

   [Python 3.9](https://www.python.org/downloads/release/python-390/) +


## Ejemplo de uso

pip install 

```
from clickup_priorities import priorities


priorities("Your_view_urls", {"Authorization": 'Your_authorization'})

```
## Output
```

{'date': '2022-11-03', 'urgent_count': 4, 'urgent_time': 8.0, 'high_count': 26, 'high_time': 6.5, 
'normal_count': 41, 'normal_time': 20.2, 'low_count': 28, 'low_time': 41.0}

```

<br>