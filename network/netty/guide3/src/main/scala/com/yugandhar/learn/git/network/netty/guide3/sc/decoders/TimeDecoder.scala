package com.yugandhar.learn.git.network.netty.guide3.sc.decoders

import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{Channel, ChannelHandlerContext}
import org.jboss.netty.handler.codec.frame.FrameDecoder

/**
  * @author Yugandhar
  */
class TimeDecoder extends FrameDecoder {
  override def decode(ctx: ChannelHandlerContext, channel: Channel, buffer: ChannelBuffer): ChannelBuffer = {
    if (buffer.readableBytes() < java.lang.Long.BYTES) {
      null
    } else {
      buffer.readBytes(java.lang.Long.BYTES)
    }
  }
}
