# API for short texts

---
- A simple API for managing short texts, using [Django Rest Framework](https://www.django-rest-framework.org)<br>
- Developed for a recruitment assignment
- Hosted on Heroku -> [short-text-api.herokuapp.com](http://short-text-api.herokuapp.com)
- All sample requests are shown using [httpie](https://httpie.io)

### Open Endpoints

---
- [register](http://short-text-api.herokuapp.com/api-auth/register/) `POST /api-auth/register/`
```json
{
  "username": "[username]",
  "password": "[password (8 chars+, not too similar to the username]",
  "password2": "[repeat passsword]",
  "email": "[valid email adress]",
  "first_name": "[a string (optional)]",
  "last_name": "[a string (optional)]"
}
 ```
- [login](http://short-text-api.herokuapp.com/api-auth/login/) `POST /api-auth/login/` useful when connecting through the browser
```json
{
  "username": "[username]",
  "password": "[password]"
}
```
- [shorttexts](http://short-text-api.herokuapp.com/shorttexts/) `GET /shorttexts/` returns all the short texts in the database along with their viewcount and ids
  It is also possible to filter the texts with simple queries:
    -  `?viewcount=<int>`
    -  `?viewcount__gt=<int>`
    -  `?viewcount__lt=<int>`
    -  `?viewcount__gte=<int>`
    -  `?viewcount__lte=<int>`
    -  `?text=<string>`
    -  `?text__contains=<string>`
- [shorttexts info](http://short-text-api.herokuapp.com/shorttexts/) `GET /shorttexts/<text_id>/` view of a single short text<br>



###Endpoints requiring authentication


---
- [create shorttexts](http://short-text-api.herokuapp.com/shorttexts/) `POST /shorttexts/`
```json
{
  "text": "[a short non-empty message no longer, than 160 characters]"
}
```
```commandline
http POST http://short-text-api.herokuapp.com/shorttexts/ text="Hello, World" -a username:password
```
- [update shorttexts](http://short-text-api.herokuapp.com/shorttexts/) `PUT /shorttexts/<text_id>/` this also sets viewcount back to 0
```json
{
  "text": "[a short non-empty message no longer, than 160 characters]"
}
```
```commandline
http PUT http://short-text-api.herokuapp.com/shorttexts/ text="Hello, World" -a username:password
```
- [delete shorttexts](http://short-text-api.herokuapp.com/shorttexts/) `DELETE /shorttexts/<text_id>/`
```commandline
http DELETE http://short-text-api.herokuapp.com/shorttexts/<text_id>/ -a username:password
```

