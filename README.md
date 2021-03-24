

# elk_study

学习使用docker搭建elk

---
[toc]

### 准备工作

#### 拉取docker镜像

> Elasticsearch:

```
docker pull elasticsearch:7.11.2
```

> Logstash:

```
docker pull logstash:7.11.2
```

> Kibana:

```
docker pull kibana:7.11.2
```

#### 创建network

```
docker network create elk-net
```

#### 创建volume
```
docker volume create es-data
```

#### 挂载配置文件

- logstash

    ```
    docker run -d --rm --name logstash logstash:7.11.2
    
    # 放在自己指定位置
    
    docker cp logstash:/usr/share/logstash/config ./logstash
    docker cp logstash:/usr/share/logstash/pipeline ./logstash
    ```
    - 删除容器(`--rm`参数`stop`即删除)
    ```
    docker stop logstash
    ```

    - 在`/logstash/pipeline`新增配置文件`python-logstash.conf`
        ```
        input {
                tcp {
                    port => 5959  
                    codec => json
                }
        }
        output {
                elasticsearch {
                    hosts => ["elasticsearch:9200"]
                    index => "python-message-%{+YYYY.MM.dd}"
                }
                stdout {
                    codec => rubydebug
                }
        }
        ```
      > 注意事项：**tcp**在`log.py`中 为`TCPLogstashHandler`；**5959**需要映射端口
      
      > input 是指从应用中产出的日志或者一些信息,具体看`log.py`
      > 
      > output 是指推送到elasticsearch中


### 启动

#### Elasticsearch
```
docker run -d --name es --network elk-net -p 9200:9200 -p 9300:9300 -v es-data:/usr/share/elasticsearch/data -e "discovery.type=single-node" elasticsearch:7.11.2
```
- 检验

[http://localhost:9200](http://localhost:9200)

#### Kibana

```
docker run -d --name kibana --network elk-net -p 5601:5601 kibana:7.11.2
```

- 检验

[http://localhost:5601](http://localhost:5601)

#### Logstash

```
docker run -d --name logstash --network elk-net -p 5044:5044 -p 5959:5959 -v <absolute path>/logstash/config:/usr/share/logstash/config -v <absolute path>/logstash/pipeline:/usr/share/logstash/pipeline logstash:7.11.2
```

<absolute path> 改成绝对路径 

### docker-compose

```
# 在docker-compose.yaml目录下
docker-compose up -d
```



### 另外

#### Windows下挂载volume问题

> `Docker_Desktop`>`docker设置`⚙ > `Resource`>`FILE SHARING` > `C:\path\to\exported\directory`>`+`

> 可以将整个盘如`D:`添加

#### 生成模拟数据

> 见 `es_insert.py`,es入门可见[ 阮一峰Elasticsearch 入门教程](http://www.ruanyifeng.com/blog/2017/08/elasticsearch.html)

#### Kibana启动后如何可视化ES数据

- 访问5601,无数据下`Ready to try Kibana?First,you need data`. 

> 可以选择模拟数据`Add Sample data`看看效果

![image-20210324173000056](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210324173000056.png)

- 插入数据后,之后`Create index pattern`创建索引范例来查看数据

![image-20210324173047818](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210324173047818.png)

- 在侧边栏`Analytics`>`Discover`中查看,以及一些`Dashboard`可视化面板

  ![image-20210324174216087](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210324174216087.png)

####  如何用Logstash收集数据

> 见`log.py`

