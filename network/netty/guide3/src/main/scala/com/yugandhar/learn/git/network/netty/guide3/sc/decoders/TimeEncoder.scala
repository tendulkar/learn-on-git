package com.yugandhar.learn.git.network.netty.guide3.sc.decoders

import com.yugandhar.learn.git.network.netty.guide3.sc.models.UnixTime
import org.jboss.netty.buffer.ChannelBuffers._
import org.jboss.netty.channel.Channels._
import org.jboss.netty.channel.{ChannelHandlerContext, Channels, MessageEvent, SimpleChannelHandler}
/**
  * @author Yugandhar
  */
class TimeEncoder extends SimpleChannelHandler {

  override def writeRequested(ctx: ChannelHandlerContext, e: MessageEvent): Unit = {
    println("Using time encoder")
    val time = e.getMessage.asInstanceOf[UnixTime]
    val buf = buffer(java.lang.Long.BYTES)
    buf.writeLong(time.millis)
    write(ctx, e.getFuture, buf)
  }
}
