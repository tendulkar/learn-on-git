package com.yugandhar.learn.git.bigdata.akka.akkalearn

import akka.actor.ActorSystem
import com.yugandhar.learn.git.bigdata.akka.akkalearn.actors.{Greeter, Printer}

/**
  * Learning:
  * 1. ActorRef is handle to the actor, like file descriptor
  * 2. Using TestProbe, from akka test toolkit we can intercept incoming messages and can add expectMsg methods
  *
  * @author Yugandhar
  */
object AkkaQuickStart {

  import com.yugandhar.learn.git.bigdata.akka.akkalearn.actors.Greeter._

  def main(args: Array[String]): Unit = {

    // create system
    val system = ActorSystem("ActorSystemName")

    // create 4 different actors
    // Given info about mailbox, config, path, class in props along with name
    val printer = system.actorOf(Printer.props, "printerActorName")
    val howdyGreeter = system.actorOf(Greeter.props("Howdy", printer), "howdyGreeter")
    val helloGreeter = system.actorOf(Greeter.props("Hello", printer), "helloGreeter")
    val goodDayGreeter = system.actorOf(Greeter.props("Good day", printer), "goodDayGreeter")

    // send messages
    howdyGreeter ! WhoToGreet("Akka")
    howdyGreeter ! Greet

    helloGreeter ! WhoToGreet("Lightbend")
    helloGreeter ! Greet

    goodDayGreeter ! WhoToGreet("Scala")
    goodDayGreeter ! Greet

    howdyGreeter ! WhoToGreet("Play")
    howdyGreeter ! Greet

    println(s"HowdyGreeter path: ${howdyGreeter.path}")

  }
}