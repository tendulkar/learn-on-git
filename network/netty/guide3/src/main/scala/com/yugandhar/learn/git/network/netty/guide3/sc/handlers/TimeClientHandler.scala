package com.yugandhar.learn.git.network.netty.guide3.sc.handlers

import java.util.Date

import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{ChannelHandlerContext, ExceptionEvent, MessageEvent, SimpleChannelHandler}

/**
  * @author Yugandhar
  */
class TimeClientHandler extends SimpleChannelHandler {

  override def messageReceived(ctx: ChannelHandlerContext, e: MessageEvent): Unit = {
    val buffer = e.getMessage.asInstanceOf[ChannelBuffer]
    val result = buffer.getLong(0)
    println(s"Current time: ${new Date(result)}")
    e.getChannel.close()
  }

  override def exceptionCaught(ctx: ChannelHandlerContext, e: ExceptionEvent): Unit = {
    e.getCause.printStackTrace()
    e.getChannel.close()
  }
}
