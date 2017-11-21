package com.yugandhar.learn.open.bigdata.flink.concepts.streaming

import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer010
import org.apache.flink.streaming.connectors.wikiedits.{WikipediaEditEvent, WikipediaEditsSource}
import org.apache.flink.streaming.util.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.scala._
import org.apache.flink.table.api.TableEnvironment

/**
  * Learn:
  * 1. windowing of streaming to make it bound
  * 2. aggregations using fold, reduce, more common aggregate
  *   init for each partition
  *   add for each element
  *   merge for each partition
  *   result for final aggregation
  * 3. common source and sink
  *
  * @author Yugandhar
  */
object WikipediaAnalysis {

  case class UserCount(var user: String, var count: Long)

  def main(args: Array[String]): Unit = {
    val see = StreamExecutionEnvironment.getExecutionEnvironment
    val wikiEditEvents = see.addSource(new WikipediaEditsSource())
    val editsByUser = wikiEditEvents.keyBy[String]((event: WikipediaEditEvent) => event.getUser)
    val editsByUserInWindow = editsByUser.timeWindow(Time.seconds(5)).
      aggregate[UserCount, UserCount](new AggregateFunction[WikipediaEditEvent, UserCount, UserCount] {

      override def add(value: WikipediaEditEvent, accumulator: UserCount): Unit = {
        accumulator.user = value.getUser
        accumulator.count += value.getByteDiff
      }

      override def createAccumulator() = UserCount("", 0L)

      override def getResult(accumulator: UserCount): UserCount = accumulator

      override def merge(a: UserCount, b: UserCount) = UserCount(a.user, a.count + b.count)
    })

    val tableEnv = TableEnvironment.getTableEnvironment(see)
    val table = tableEnv.fromDataStream(wikiEditEvents)
    table.join(table).printSchema()

    editsByUserInWindow.map(_.toString)
      .addSink(new FlinkKafkaProducer010[String]("localhost:9092", "wiki-result", new SimpleStringSchema()))
    see.execute()
  }
}
