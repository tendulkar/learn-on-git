package com.yugandhar.learn.git.bigdata.akka.akkalearn.actors

import akka.actor.{Actor, ActorLogging, Props}

/**
  * Props carry info about
  * 1. class name (in this example it's Printer class, it can't be abstract class ever)
  * 2. mailbox
  * 3. path
  * 4. config
  * 5 ...
  *
  * ActorLogging trait allows to access logger with name "log"
  *
  * @author Yugandhar
  */
class Printer extends Actor with ActorLogging {

  import Printer._

  override def receive: Actor.Receive = {
    case Greeting(msg) => log.info(s"Received greeting with message: $msg")
    case _ => log.error("Received message can't be decoded!!")
  }
}

object Printer {
  def props: Props = Props[Printer]

  final case class Greeting(msg: String)

}
