

本模块依赖于第三方类库confluent-kafka:

```
pip install confluent-kafka
```

*接口实现位于implement包,配置示例位于implement/config*

*使用者只需关注生产者类和消费者类*

# topic操作：

```python
class CommunicationInitial(CommunicationInitialInterface)
```

## 查询topic列表

```python
@staticmethod
def topicQuery(communicationCharactor)
```

```python
:param communicationCharactor: a instance of class "CommunicationConsumer" or "CommunicationProducer"

:return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
```

### 可能异常：

```python
TopicQueryFailed # 对kafka异常的简单封装
```

## 创建topic

```python
@staticmethod
def topicCreate(topic, confPath)
```

```python
:param topic: this param is the name of the topic that you want to create. type: str

:param confPath: broker configuration, "bootstrap.servers" must be set

:return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
```

### 可能异常：

```python
NoConfigFileException # 配置文件不存在
WrongConfigContextException #　配置文件内容有误
TopicCreateFailed # topic创建失败
```

## 删除topic

```python
@staticmethod
def topicDelete(topic, confPath):
```

```python
:param topic: this param is the name of the topic that you want to delete. type: str

:param confPath: broker configuration, "bootstrap.servers" must be set

:return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
```

### 可能异常:

```python
NoConfigFileException # 配置文件不存在
WrongConfigContextException #　配置文件内容有误
TopicCreateFailed # topic删除失败
```

# 生产者：

```python
class CommunicationProducer(CommunicationProducerInterface)
```

*调用者只需要关注__init__和__send__的用法*

## 初始化

```python
def __init__(self, confPath, topic=0)
```

```python
:param confPath: this param is the path of the producer config file that you want to use. type: str
            
:param topic: this param don't need to config
```

## 查询topic列表

```python
def list_topics(self, topic=None, timeout=0.5)
```

```python
:param topic: this param is the topic name that you want to inquire, type: str
            
:param timeout: this param is the inquire timeout, type: int
            
:return: Map of topics indexed by the topic name. Value is TopicMetadata object in confluent-kafka.
```

## 发送消息

```python
def send(self, topic, value, key=None)
```

```python
:param topic: this param is the topic name that you want to send message to, type: str
            
:param value: this param is the message context, type: bytes
            
:param key: this param isn't used currently
        
:return: "ok" if successfully sent
```

### 可能异常：

```python
WrongMessageValueType #　消息类型非ｂｙｔｅｓ
```

## 关闭

```python
def close(self)
```

### 关闭动作：

推送生产者队列中的全部消息

# 消费者：

```python
class CommunicationConsumer(CommunicationConsumerInterface)
```

*调用者只需要关注__init__和__receive__的用法*

## 初始化

```python
def __init__(self, confPath, consumerId, topic=0)
```

```python
:param confPath: this param is the path of the producer config file that you want to use. type: str
            
:param consumerId: this param should be unique in the system, UUID suggested. type: str
            
:param topic: this param is the topic this consumer need to subscribe
```

### 可能异常：

```python
TopicNotAvailableException #　topic不存在或其他原因订阅失败
```

## 订阅

```python
def subscribe(self, topic)
```

```python
:param topic: this param is the topic this consumer need to subscribe
        
:return: incoming param "topic" when subscribe successfully
```

### 可能异常：

```python
TopicNotAvailableException #　topic不存在或其他原因订阅失败
```

## 取消订阅

```python
def unsubscribe(self)
```

## 查询topic列表

```python
def list_topics(self, topic=None, timeout=0.5)
```

```python
:param topic: this param is the topic name that you want to inquire, type: str

:param timeout: this param is the inquire timeout, type: int

:return: Map of topics indexed by the topic name. Value is TopicMetadata object in confluent-kafka.
```

## 接收消息

```python
def receive(self)
```

```python
:return: unpacking message received in timeout. type: bytes or None(when there is no message in timeout)
```

## 关闭

```python
def close(self)
```

### 关闭动作：

取消订阅、关闭消费者