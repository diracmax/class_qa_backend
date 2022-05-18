# class_qa_backend

## curlでapi叩く方法

```shell
 curl -X POST 'http://localhost:80/classes/1/questions' -H 'Content-Type: application/json;charset=utf-8' -d '{"content":"aiu"}' -H 'Authorization: Bearer XX
XX' | jq .
```

```shell
curl -X POST -H "Content-Type: application/json" -d '{"username":"太郎", "password":"gain"}' http://localhost:80/users
```

```shell
curl -X POST 'http://localhost:80/classes/1/questions' -H "Content-Type: application/json" -d '{"content":"aiu"}' -H 'Authorization: Bearer $2b$12$UMtdnZRtsE1mDFLfLgr7I.Mege/VlHpr1tAySaVNPfwAxB9bSfD9q'
```