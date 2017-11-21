package com.yugandhar.learn.git.network.netty.guide3.sc.decoders

import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{Channel, ChannelHandlerContext}
import org.jboss.netty.handler.codec.replay.{ReplayingDecoder, VoidEnum}

/**
  * @author Yugandhar
  */
class TimeDecoderReplaying extends ReplayingDecoder[VoidEnum] {
  override def decode(ctx: ChannelHandlerContext,
                      channel: Channel,
                      buffer: ChannelBuffer,
                      state: VoidEnum): ChannelBuffer = {
    buffer.readBytes(8)
  }
}
