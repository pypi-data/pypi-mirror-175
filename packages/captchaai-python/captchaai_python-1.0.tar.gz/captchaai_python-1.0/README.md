CaptchaAI.IO package for Python
=
![PyPI - Wheel](https://img.shields.io/pypi/wheel/captchaai_python?style=plastic) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/captchaai_python?style=flat) ![GitHub last commit](https://img.shields.io/github/last-commit/alperensert/captchaai_python?style=flat) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/alperensert/captchaai_python?style=flat) ![PyPI - Downloads](https://img.shields.io/pypi/dm/captchaai_python?style=flat) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/alperensert/captchaai_python?style=flat) ![GitHub Repo stars](https://img.shields.io/github/stars/alperensert/captchaai_python?style=social) 

[CaptchaAI.IO](https://captchaai.io) package for Python3

Register now from [here](https://dashboard.captchaai.io/passport/register?inviteCode=kXa8cbNF-b2l).

If you have any problem with usage, [read the documentation](https://github.com/alperensert/captchaai_python/wiki) or [create an issue](https://github.com/alperensert/captchaai_python/issues/new)

### Installation
```
pip install captchaai_python
```

### Supported captcha types
- Image to Text
- Recaptcha V2
- Recaptcha V2 Enterprise
- Recaptcha V3
- FunCaptcha
- HCaptcha
- GeeTest
- AntiAkamaiBMP
- HCaptcha Classification
- DataDome Slider
- FunCaptcha Classification

Usage examples
-

#### ImageToText

```python
from captchaai_python import ImageToTextTask

captchaaiio = ImageToTextTask("API_KEY")
task_id = captchaaiio.create_task(image_path="img.png")
result = captchaaiio.join_task_result(task_id)
print(result.get("text"))
```

#### Recaptcha v2

```python
from captchaai_python import RecaptchaV2Task

captchaaiio = RecaptchaV2Task("API_KEY")
task_id = captchaaiio.create_task("website_url", "website_key")
result = captchaaiio.join_task_result(task_id)
print(result.get("gRecaptchaResponse"))
```

#### Recaptcha v2 enterprise

```python
from captchaai_python import RecaptchaV2EnterpriseTask

captchaaiio = RecaptchaV2EnterpriseTask("API_KEY")
task_id = captchaaiio.create_task("website_url", "website_key", {"s": "payload value"}, "api_domain")
result = captchaaiio.join_task_result(task_id)
print(result.get("gRecaptchaResponse"))
```

#### GeeTest

```python
from captchaai_python import GeeTestTask

captchaaiio = GeeTestTask("API_KEY")
task_id = captchaaiio.create_task("website_url", "gt", "challenge")
result= captchaaiio.join_task_result(task_id)
print(result.get("challenge"))
print(result.get("seccode"))
print(result.get("validate"))
```

For other examples and api documentation please visit [wiki](https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/overview)