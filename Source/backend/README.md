# MaxTED

[BackEnd] BackEnd 시스템

## Backend ([FastAPI])

### Project Path

```sh
cd C:/Python/venv/rndops/Source/rndops-be
```

### Package 설치

```sh
pip install -r requirements.txt
```

### Package 삭제

```sh
pip uninstall -r requirements.txt
```

### Package 저장

> Note: 패키지를 추가하면 `requirements.txt` 업데이트하고 커밋할 것!

```sh
pip freeze > requirements.txt
```

### 서버실행 및 종료

> Note: .vscode/settings.json 을 설정한 경우 단축키 사용
>
> > 실행: 단축키 F5 or F11
> > 종료: 단축키 Ctrl + F2 or Ctrl + C

```sh
uvicorn main:app --reload
```

[//]: # "These are reference links used in the body of this note and get stripped out when the markdown processor does its job."
[Vue3]: https://vuejs.org
[FastAPI]: https://fastapi.tiangolo.com/ko
