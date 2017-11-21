package com.yugandhar.learn.git.network.netty.guide3.sc.handlers

import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{ChannelHandlerContext, ExceptionEvent, MessageEvent, SimpleChannelHandler}

class ServerHandler extends SimpleChannelHandler {

  override def messageReceived(ctx: ChannelHandlerContext, e: MessageEvent): Unit = {
    val buffer: ChannelBuffer = e.getMessage.asInstanceOf[ChannelBuffer]
    val channel = e.getChannel
    channel.write(e.getMessage)
    println(s"Message received: ${new String(buffer.array())}")
  }

  override def exceptionCaught(ctx: ChannelHandlerContext, e: ExceptionEvent): Unit = {
    e.getCause.printStackTrace()
    e.getChannel.close()
  }
}