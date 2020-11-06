##  3.迁移完成后，下线节点，恢复路由策略
节点分片迁移完成后，停掉 ES 下线节点的服务进程：

```bash
kill {elasticsearch}  # 进程号
```
恢复路由策略，刚才排除节点的策略废除掉
```bash
curl -XPUT http://hostname:9200/_cluster/settings?pretty -H 'Content-Type: application/json' -d '{
  "transient": {
    "cluster.routing.allocation.exclude._name": null
  }
}'
```

# 三、重启集群其他节点
<font color=#999AAA >**这一步很重要**，之前讲过动态修改配置项，和配置文件，以前的配置文件可能包含下线节点的信息，比如es-name、master-node 信息，此时修改配置后滚动重启，避免之后因遗忘带来错误。
<font>

滚动重启比较简单：

## 1. 停止数据写入，重启期间有分片在写入会有异常
## 2.关闭集群自动分片
```bash
# 关闭集群分片自动分配
# 因为只是重启而已，不需要自动传输
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
  }
}
```

## 3.重启节点
## 4. 重新开启集群shard allocation
```bash
#打开集群分片自动分配
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}
```

**重启集群是  2-4 三个步骤的循环，每下一个节点，都要等待集群状态变为green** 中间分片数据是不传输的，恢复非常快，几乎在重启的1分钟内，如果有传输，就是命令输入不对

# 总结
<font color=#999AAA >以上就是我生产环境下线集群的实战记录，按步骤操作，顺滑无BUG <font>
