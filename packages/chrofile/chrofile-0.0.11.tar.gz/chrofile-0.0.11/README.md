## 参考

### PyPIパッケージのリリースもバージョニングもGitHub単独で完結させる
https://zenn.dev/detsu/articles/5d74bf72e96a0f


### How can I infinite-scroll a web page using selenium webdriver in python
https://stackoverflow.com/questions/70906433/how-can-i-infinite-scroll-a-web-page-using-selenium-webdriver-in-python


## Chrofile
Get a list of user profiles for the chrome browser.

## installation
```
pip install chrofile
```

### usage
```
from time import sleep
import chrofile

def main():
  driver = None
  try:
    chrome = chrofile.start()
    sleep(30)
    ### some browser controls ###
  except Exception as e:
    print(e)
  finally:
    if chrome: chrome.quit()

main()

```


## Reference
```
https://mikebird28.hatenablog.jp/entry/2020/06/15/233447
```

## Upload PyPI
```
pip install pip install setuptools wheel twine
rm -rf build dist chrofile.egg-info

python setup.py sdist && python setup.py bdist_wheel && python -m twine upload --repository pypi dist/*
```