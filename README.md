# HTTP API自动化pytest HTTP API自动化测试框架
## info
- mongoDB
- pytest
- jenkins
- allure

## 功能模块
### 1.数据驱动
- data 输入参数, scm 返回校验模板, desc 测试数据描述
- 1.1代码中写入测试数据

@pytest.mark.parametrize('data,scm', [
        ({}, {'data': '{% str %}'}),
        ({'username': '{{ user }}', 'password': 'wrong'}, {'data': '{% str %}'}),
        ({'username': 'wrong', 'password': '{{ pwd }}'}, {'data': '{% str %}'})
    ])

- 1.2测试类名+方法名 映射为mongodb中一个集合， 存储数据为data 和scm字段
  适合嵌套结构多层的json字段
- 1.3测试类名+方法名 映射为excel中一个sheet， 存储数据每列对应json中一个key
  适合结构简单的请求数据

## 2.数据动态渲染
#### 支持数据动态替换，
#### 如‘{{ DevToken }}’，替换变量，变量池为Req中的cache
#### {% random.randint(1, 10) %}，替换为函数
#### 默认支持python库中 fake项目的函数，可在comm.tools中自定义函数
#### 例如测试数据中：

{ 'key': {
    'company': '{% fake.company() %}',
    'phone': '{% fake.phone_number() %}',
    'str': '{% fake.pystr(max_chars=10) %}'
   },
   'tu': [
       '{{ val }}', 
       {'newkey': '{{ val }}'}
   ]
}

#### 运行时会动态替换成

{ 'key': {
    'company': '凌颖信息传媒有限公司', 
    'phone': '13481047148', 
    'str': 'RBDjMHbZfm'
   },
  'tu': [
      456, 
      {'newkey': 456}
  ]
}


## 3.数据校验
#### 与数据一样，校验函数也是动态的，测试数据中配置数据校验模板，可以减少assert语句，代码更加简洁
#### 规则与数据替换大致一致 例如：

{
    "data" : "{% str %}",        #校验返回的data是个字符串对象
    "traceID" : "{{ traceID }}", #校验traceID相等
    "message" : "token错误",     #校验返回的message
    "code" : "00120112001",
    "success" : False            #校验布尔值等于false
}

## 4.多环境配置
#### 执行环境信息保存在config.ini文件中,运行的时候 --env=test 使用测试环境 --env=online执行线上环境

[env_test]
host: http://192.168.95.27:9527
username: testuser
password: 111111
[env_online]
host: http://www.example.com
username: testuser2
password: 111111

# 快速开始
- clone本项目
- Dependency  
   + python3 Docker
   + pip install -r requirements.txt
- 运行
   + docker run --name mongo -d -v /root/docker/mongo:/data/db -p 27017:27017 mongo
   + pytest
   + allure serve -p 8090

# 集成jenkins
todo


```python

```


```python

```


```python

```
