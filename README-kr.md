# mp3 chart merge

[English](README.md)

이 스크립트는 mp3 파일이름에 있는 순위를 제거하면서 다른 디렉토리로 파일을 복사/이동하는 일을 합니다.

빌보드 차트와 같이 주기적으로 발표되는 순위에 있는 mp3 파일들의 최신 목록만 유지하면서 기존 mp3 파일들을 한군데로 모으기 위해 사용합니다.

예를 들어, 다음과 같은 명령을 사용하면 `src` 디렉토리에 있는 mp3파일들을 `dest` 디렉토리로 이동하게 됩니다.

```bash
$ python merge.py --src ./Billboard.2016.12.02 --dest ./Billboard.2016 --move
```

```
[SRC] Billboard.2016.12.02/
 - 001.Black Beatles - Rae Sremmurd (feat. Gucci Mane).mp3
 - 002.The Chainsmokers feat. Halsey - Closer.mp3

[DEST] Billboard.2016/
 - Black Beatles - Rae Sremmurd (feat. Gucci Mane).mp3
 - The Chainsmokers feat. Halsey - Closer.mp3
```

### 원본 파일이름 패턴

```
${순위} ${가수}-${제목}.mp3
${순위}. ${가수}-${제목}.mp3
```

각 토큰들 사이에 있는 공백 문자는 무시된다.

### 대상 파일이름 패턴

```
${가수} - ${제목}.mp3
```

### 파일이름 비교 규칙

* 영숫자, 한글을 제외한 모든 공백과 특수문자는 무시한다.
* 괄호`()` 안에 있는 문자들은 무시한다.
* 대소문자를 구분하지 않는다.

## 실행시 필요사항

* [파이썬 3.x](https://www.python.org/downloads/)

## 명령행 옵션

### `--src dir`

원본 mp3 디렉토리

`*`와 같은 와일드 카드를 사용해서 여러 디렉토리를 지정할 수 있다.

### `--dest dir`

mp3 파일을 이동/복사할 대상 디렉토리

### `--move`

선택사항.

지정할 경우 mp3 파일들을 `dest` 디렉토리로 이동한다. 지정하지 않으면 복사한다.

대상 디렉토리에 중복된 mp3 파일이 있을 경우, 이동하지 않고 건너뛴다.

### 예제

```bash
# "mp3/Billboard 2016.*" 디렉토리들 안에 있는 모든 mp3 파일들을 "mp3/Billboard 2016" 디렉토리로 이동한다.
$ python merge.py --src "mp3/Billboard 2016.*" --dest "mp3/Billboard 2016" --move
```
