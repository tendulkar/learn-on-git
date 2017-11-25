package com.yugandhar.learn.git.bigdata.akka.akkalearn.actors

import akka.actor.{Actor, ActorRef, Props}

/**
  * ActorRef don't take any template param
  * However contains class name
  *
  * @author Yugandhar
  */
class Greeter(msg: String, printerActor: ActorRef) extends Actor {

  import Greeter._
  import Printer._

  var greetMsg: String = ""

  override def receive: Receive = {
    case WhoToGreet(who) => greetMsg = s"$msg, $who"
    case Greet => printerActor ! Greeting(greetMsg)
  }
}

object Greeter {
  def props(msg: String, printerActor: ActorRef): Props = Props[Greeter](new Greeter(msg, printerActor))

  final case class WhoToGreet(who: String)

  case object Greet

}
