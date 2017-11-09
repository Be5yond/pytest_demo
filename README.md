接口自动化测试框架
===========

##Info
MongoDB+pytest+Allure+jenkins

##可维护性

## 功能模块
+ 数据驱动
  - 测试类名+方法名 映射为mongodb中一个集合， 存储数据为data 和scm字段-
  - data 输入参数, scm 返回校验模板, desc 测试数据描述
  ![](files/mongo.png) 
  - 测试代码 发送data,使用scm模板校验返回
  ![](files/code.png) 
  - 结果报告
  ![](files/allure.png) 
      
+ 数据动态渲染
  - 支持数据动态替换，如‘{{ DevToken }}’，替换变量，{% int %}替换为函数。
     {'tu': ['{{ val }}', {'newkey': '{{ val }}'}],  
      'key': {'str': '{% fake.pystr(max_chars=10) %}',  
              'phone': '{% fake.phone_number() %}',  
              'company': '{% fake.company() %}'}   
     }  
  ------->  
     {'tu': [456, {'newkey': 456}],  
      'key': {'str': 'CxtMTqAhLY',  
              'phone': '13319170599',  
              'company': '精芯网络有限公司'}   
     }  
+ Schema 模板使用
  - 支持部分校验，只校验scm中有的key值
  - 规则支持函数 例如   
    {   
        "data" : "{% str %}",              #校验返回的data是个字符串对象    
        "traceID" : "{{ traceID }}",       #校验traceID相等    
        "message" : "token错误",            #校验返回的message   
        "code" : "00120112001",   
        "success" : false                  #校验布尔值等于false   
    }    
+ 执行环境配置
  -  执行环境信息保存在config.ini文件中,运行的时候 --env=test 使用测试环境  --env=online执行线上环境   
  [env_test]   
   host: http://192.168.95.27:9527   
   username: testuser   
   password: 111111   
  [env_online]  
   host: http://www.example.com   
   username: testuser2   
   password: 111111 
   

##快速开始
+ Dependency
  - python3.5 docker
+ 安装依赖包
  - pip install -r requirements.txt
+ docker 启动mongodb 
  - docker run --name mongo -d -v /root/docker/mongo:/data/db -p 27017:27017 mongo
+ 运行
  - pytest 
  - allure serve -p 8090


