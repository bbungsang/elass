# Deploy EC2

## requirements

**Python**
3.6.1

**pip**

```
>>> pip install -r requirements.txt
```

## Create .config_secret file

[.config_secret/settings_common.json]

```json
{
	"django": {
		"secret_key": "m9&l-fgj&...(프로젝트 생성시 발급받는 secret_key)"
	}
}
```

## 해당 파일을 settings 파일에서 open 하여 secret_key 값 적용하기

현재 디렉토리 구조

```
project(root directory)/
	.config_secret/
		settings_common.json
	django_app/
		config/
			settings/
				base.py
				debug.py
				deploy.py
```

[settings/base.py]

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

ROOT_DIR = os.path.join(BASE_DIR)

CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')

config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())

# Secret Key
SECRET_KEY = config_secret_common['django']['secret_key']
```
