### ДЗ 4


##### Авторизация для сервиса генерации логотипов по промпту

* реализована авторизация через JWT токены, которые генерируются при входе юзера в систему

* refresh_token необходим для упрощенного получения нового access_token, обновление сессии реализовано в запросе /update/token

* генерация логотипов выполнена в годовом проекте, но модель занимает ~70 Gb места и только с видеокартой запускается, поэтому заменена на генерацию случайных изображений разного цвета
(согласовано с преподавателем)

* для авторизованных пользователей в ендпоинте /generate_image генерируется новое изображение, релизовано также кэширование изображений с совпадающими промптами

* сгенерированный логотип попадает в директорию generated и раздается статикой, по ссылки вида:
```
http://localhost/generated/b4b0bdf5-f9a1-4b01-ac54-f21435fd10ae.png
```

##### Документация

http://45.9.73.228/docs

или  

http://localhost/docs


### Запуск проекта 

Из корневой директории выполнить docker-compose up -d

**Удаление проекта**

1. docker-compose down
2. docker image prune --all

### Ссылка на репозиторий

https://github.com/efgraph/devops_hw_1

__ФИО:__ _Спиридонов Д В (специальность МОВС)_


