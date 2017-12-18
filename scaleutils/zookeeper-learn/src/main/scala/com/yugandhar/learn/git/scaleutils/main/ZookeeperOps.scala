package com.yugandhar.learn.git.scaleutils.main

import com.yugandhar.learn.git.scaleutils.common.ZookeeperConnection
import org.apache.zookeeper._
import org.apache.zookeeper.data.Stat

import scala.collection.JavaConverters._
import scala.util.Try

/**
  * @author Yugandhar
  */
object ZookeeperOps {

  val conn: ZookeeperConnection = new ZookeeperConnection()
  val client: ZooKeeper = conn.connect("localhost", 2181)

  def create(path: String, data: Array[Byte]): Unit = {
    client.create(path, data, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT)
  }

  def exists(path: String): Stat = {
    client.exists(path, true)
  }

  def delete(path: String): Unit = {
    client.delete(path, exists(path).getVersion)
  }

  def get(path: String): Array[Byte] = {
    client.getData(path, true, exists(path))
  }

  def getChildren(path: String): List[String] = {
    client.getChildren(path, true).asScala.toList
  }

  def main(args: Array[String]): Unit = {
    val path = "/MyNodePath"
    Try {
      create(path, Array[Byte](1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
      val stat = exists(path)
      println(s"Exists result version: ${stat.getVersion}")
      val children = getChildren(path)
      println(s"Get children result: $children")
      val data = get(path)
      println(s"Data is: ${data.toList}")
      delete(path)
      Try {
        val newData = get(path)
        println(s"After delete data is: ${newData.toList}")
      } recover {
        case ex: KeeperException.NoNodeException => println(s"As expected the data is cleaned up for path: $path")
      }
    } recover {
      case ex: Throwable => ex.printStackTrace()
    }
    conn.close()
  }
}
