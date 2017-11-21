package com.yugandhar.learn.git.network.netty.guide3.sc

import java.net.InetSocketAddress
import java.util.concurrent.Executors

import com.yugandhar.learn.git.network.netty.guide3.sc.decoders.TimeDecoderReplaying
import com.yugandhar.learn.git.network.netty.guide3.sc.handlers.TimeClientHandler
import org.jboss.netty.bootstrap.ClientBootstrap
import org.jboss.netty.channel.socket.nio.NioClientSocketChannelFactory
import org.jboss.netty.channel.{ChannelPipeline, ChannelPipelineFactory, Channels}

class SimpleClientPipelineFactory extends ChannelPipelineFactory {
  override def getPipeline: ChannelPipeline = {
    Channels.pipeline(new TimeDecoderReplaying(), new TimeClientHandler())
  }
}

/**
  * @author Yugandhar
  */
object SimpleClient {

  def main(args: Array[String]): Unit = {
    val clientSocketChannelFactory = new NioClientSocketChannelFactory(
      Executors.newCachedThreadPool(), Executors.newCachedThreadPool())
    val clientBootstrap = new ClientBootstrap(clientSocketChannelFactory)
    clientBootstrap.setPipelineFactory(new SimpleClientPipelineFactory())
    clientBootstrap.setOption("tcpNoDelay", true)
    clientBootstrap.setOption("keepAlive", true)
    val future = clientBootstrap.connect(new InetSocketAddress("localhost", 9700))
    future.awaitUninterruptibly()
    if (!future.isSuccess) {
      future.getCause.printStackTrace()
    }
    future.getChannel.getCloseFuture.awaitUninterruptibly()
    clientBootstrap.releaseExternalResources()
  }
}
