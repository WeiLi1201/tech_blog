
<font color=#999AAA >提示：ES很健壮也很脆弱，不要蛮干

</font>

@[TOC](Elasticsearch 平滑下线节点实战)


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 场景

<font color=#999AAA >由于历史原因，ES节点中有几台配置很低，需要下线，换成新的与集群其他配置相同的ES节点。</font>

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

<font color=#999AAA >提示：ES平滑下线主要注意要做下线前检查，一是避免因下线节点脑裂，集群崩掉，二是下线时保证数据不丢失，集群健康状态始终为green

# 一、检查集群配置，修改ES配置项


<font color=#999AAA >做下线操作前，检查 master-eligible 节点的数量与 minimum_master_nodes 配置，确认下线节点不会影响集群可用性与稳定性。默认所有节点都是master-eligible节点，即有资格选为master的节点。</font>
```bash
discovery.zen.minimum_master_nodes: 3
node.master: true
```
<font color=#999AAA >如果本来5个节点，最后决定剩下3个节点，那么设置的值建议为 **minimum_master_nodes = (master_eligible_nodes / 2) + 1**  </font>

<font color=#999AAA >具体操作为：**先通过命令动态修改，并修改配置文件待下一次重启生效。**
```bash
# 设置 minimum_master_nodes 为 2
curl -XPUT 'http://hostname:9200/_cluster/settings' -H 'Content-Type: application/json' -d '{
  "persistent" : {
    "discovery.zen.minimum_master_nodes" : 2
  }
}'
```
</font>
