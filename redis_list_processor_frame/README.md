# README

## 功能
提供基于redis list的简单消息队列框架
- 结构为：左进右出的队列
- 生产者`lpush`即可，配合`ltrim`可实现定长队列
- 任务结构为：`dict`的`json`
    - `retry`和`execute_timestamp`为保留字段，请勿使用。
- 本框架利用多线程实现并发，可再使用supervisor的`numprocs`实现多进程的水平拓展。
- 消费者循环地`brpop`，异常则重新sleep后再`lpush`。





