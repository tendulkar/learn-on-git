package com.yugandhar.learn.git.network.netty.guide3.sc.handlers

import com.yugandhar.learn.git.network.netty.guide3.sc.models.UnixTime
import org.jboss.netty.channel._
import org.jboss.netty.channel.group.{ChannelGroup, DefaultChannelGroup}

import scala.collection.mutable.ListBuffer

/**
  * @author Yugandhar
  */
class TimeServerHandler extends SimpleChannelHandler {

  import TimeServerHandler._

  override def channelOpen(ctx: ChannelHandlerContext, e: ChannelStateEvent): Unit = {
    allChannels.add(e.getChannel)
  }

  override def channelConnected(ctx: ChannelHandlerContext, e: ChannelStateEvent): Unit = {
    println("Using Server handler")
    val ch = e.getChannel
    val future = ch.write(UnixTime(System.currentTimeMillis()))
    future.addListener(new ChannelFutureListener {
      override def operationComplete(fut: ChannelFuture): Unit = fut.getChannel.close()
    })
  }

  override def exceptionCaught(ctx: ChannelHandlerContext, e: ExceptionEvent): Unit = {
    e.getCause.printStackTrace()
    e.getChannel.close()
  }
}

object TimeServerHandler {
  final val allChannels: ChannelGroup = new DefaultChannelGroup("Default-test-netty")
}
