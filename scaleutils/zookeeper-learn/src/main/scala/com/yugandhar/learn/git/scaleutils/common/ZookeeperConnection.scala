package com.yugandhar.learn.git.scaleutils.common

import java.util.concurrent.{ConcurrentLinkedQueue, CountDownLatch}
import java.util.function.Consumer

import org.apache.zookeeper.Watcher.Event.KeeperState
import org.apache.zookeeper.{WatchedEvent, ZooKeeper}


/**
  * Provides synchronous function to connect, wraps zookeeper client
  * It's thread safe always creates new connection
  *
  * @author Yugandhar
  */
class ZookeeperConnection extends AutoCloseable {

  val clients: ConcurrentLinkedQueue[ZooKeeper] = new ConcurrentLinkedQueue[ZooKeeper]()

  def connect(host: String = "localhost", port: Int = 2181): ZooKeeper = {
    val countDownLatch: CountDownLatch = new CountDownLatch(1)
    val client = new ZooKeeper(host, port, (event: WatchedEvent) => {
      if (event.getState == KeeperState.SyncConnected) {
        countDownLatch.countDown()
      }
    })
    countDownLatch.await()
    clients.add(client)
    client
  }

  def close(): Unit = {
    clients.forEach(new Consumer[ZooKeeper] {
      override def accept(t: ZooKeeper): Unit = t.close()
    })
  }

}
