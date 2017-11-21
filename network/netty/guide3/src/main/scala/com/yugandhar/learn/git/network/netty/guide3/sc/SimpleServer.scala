package com.yugandhar.learn.git.network.netty.guide3.sc

import java.net.InetSocketAddress
import java.util.concurrent.Executors

import com.yugandhar.learn.git.network.netty.guide3.sc.decoders.TimeEncoder
import com.yugandhar.learn.git.network.netty.guide3.sc.handlers.TimeServerHandler
import org.jboss.netty.bootstrap.ServerBootstrap
import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory
import org.jboss.netty.channel.{ChannelPipeline, ChannelPipelineFactory, Channels}

class MyChannelPipelineFactory extends ChannelPipelineFactory {
  override def getPipeline: ChannelPipeline = {
    Channels.pipeline(new TimeServerHandler(), new TimeEncoder())
  }
}

/**
  * @author Yugandhar
  */
object SimpleServer {

  def shutdownHook(serverBootstrap: ServerBootstrap): Runnable = new Runnable {
    override def run(): Unit = {
      println("Clean up server resources")
      val future = TimeServerHandler.allChannels.close()
      future.awaitUninterruptibly()
      serverBootstrap.releaseExternalResources()
    }
  }

  def main(args: Array[String]): Unit = {
    val serverSocketChannelFactory = new NioServerSocketChannelFactory(
      Executors.newCachedThreadPool(), Executors.newCachedThreadPool())
    val serverBootstrap = new ServerBootstrap(serverSocketChannelFactory)
    serverBootstrap.setPipelineFactory(new MyChannelPipelineFactory())
    serverBootstrap.setOption("child.tcpNoDelay", true)
    serverBootstrap.setOption("child.keepAlive", true)
    val channel = serverBootstrap.bind(new InetSocketAddress(9700))
    TimeServerHandler.allChannels.add(channel)
    println("Bind done!!")
    Runtime.getRuntime.addShutdownHook(new Thread(shutdownHook(serverBootstrap)))
  }
}
