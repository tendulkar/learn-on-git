package com.yugandhar.learn.open.bigdata.flink.concepts.iterations

import java.lang

import org.apache.flink.api.common.functions.GroupReduceFunction
import org.apache.flink.api.java.aggregation.Aggregations.SUM
import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.api.scala.{DataSet, ExecutionEnvironment, _}
import org.apache.flink.examples.java.graph.util.PageRankData
import org.apache.flink.util.Collector

import scala.collection.JavaConverters._

/**
  * Example for full iteration
  * Applies page rank algo
  *
  * logic is
  * start partial solution = input
  * for i <- 1 to maxIter
  * <ul>
  * <li>res = compute step function </li>
  * <li>partial solution = input</li>
  * </ul>
  * result is partial solution
  *
  * @author Yugandhar
  */
object PageRank {

  @SerialVersionUID(53909890123L)
  case class Page(pageId: Long, rank: Double) extends Serializable

  @SerialVersionUID(834759800988L)
  case class Link(sourceId: Long, targetId: Long) extends Serializable

  case class AdjacencyList(sourceId: Long, neighbours: Array[Long])

  def getPages(env: ExecutionEnvironment, params: ParameterTool): (DataSet[Long], Long) = {
    if (params.has("pages") && params.has("numPages")) {
      val pages = env
        .readCsvFile[Tuple1[Long]](params.get("pages"), fieldDelimiter = " ", lineDelimiter = "\n")
        .map(_._1)
      (pages, params.getLong("numPages"))
    } else {
      (env.generateSequence(1L, 15L), PageRankData.getNumberOfPages)
    }
  }

  def getLinks(env: ExecutionEnvironment, params: ParameterTool): (DataSet[Link]) = {
    if (params.has("links")) {
      env.readCsvFile[Link](params.get("links"), fieldDelimiter = " ",
        lineDelimiter = "\n", includedFields = Array(0, 1))
    } else {
      val edges = PageRankData.EDGES.map {
        case Array(v1, v2) => Link(v1.asInstanceOf[Long], v2.asInstanceOf[Long])
      }
      env.fromCollection(edges)
    }
  }

  def toAdjacencyList(links: DataSet[Link]): DataSet[AdjacencyList] = {
    links.groupBy("sourceId").reduceGroup(new GroupReduceFunction[Link, AdjacencyList] {
      override def reduce(values: lang.Iterable[Link], out: Collector[AdjacencyList]): Unit = {
        var sourceId = -1L
        val targets = values.asScala.map { link =>
          sourceId = link.sourceId
          link.targetId
        }
        out.collect(AdjacencyList(sourceId, targets.toArray))
      }
    })
  }

  def main(args: Array[String]): Unit = {

    // get env, put command line args as global job params
    val params = ParameterTool.fromArgs(args)
    val env = ExecutionEnvironment.getExecutionEnvironment
    env.getConfig.setGlobalJobParameters(params)

    // fetch data --> numPages, pagesWithRanks, adjacencyList, maxIterations
    val (pages, numPages) = getPages(env, params)
    val links = getLinks(env, params)
    val adjacencyList = toAdjacencyList(links)
    val pagesWithRanks = pages.map(p => Page(p, 1.0 / numPages)).withForwardedFields("*->pageId")
    val maxIterations = if (params.has("maxIterations")) params.getInt("maxIterations") else 10

    adjacencyList.print()

    // run the page rank algorithm (plan for algo)
    val finalRanks = pagesWithRanks.iterateWithTermination(maxIterations) { currentRanks =>
      val newRanks = currentRanks.join(adjacencyList).where("pageId").equalTo("sourceId") {
        (page, adjacent, out: Collector[Page]) =>
          val len = adjacent.neighbours.length
          adjacent.neighbours.foreach { t => out.collect(Page(t, page.rank / len)) }
      }.groupBy("pageId").aggregate(SUM, "rank")
        .map(p => {
          Page(p.pageId, p.rank * 0.85 + (1 / numPages) * 0.15)
        }).withForwardedFields("pageId")

      val termination = currentRanks.join(newRanks).where("pageId").equalTo("pageId") {
        (current, next, out: Collector[Int]) =>
          if (math.abs(current.rank - next.rank) > 0.0001) out.collect(1)
      }
      (newRanks, termination)
    }

    finalRanks.print()
  }
}
