package com.yugandhar.learn.open.bigdata.flink.concepts.iterations

import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.api.scala.{DataSet, ExecutionEnvironment}
import org.apache.flink.examples.java.graph.util.ConnectedComponentsData
import org.apache.flink.util.Collector
import org.apache.flink.api.scala._

import scala.collection.JavaConverters._

/**
  * Example for delta iteration
  * delta iteration logic
  * start solution set and working set
  * for i <- 1 to maxIter:
  * <ul>
  * <li> run iteration and get diff solution set, and working set </li>
  * <li> solution set += diff solution set </li>
  * </ul>
  * return solution set
  *
  * @author Yugandhar
  */
object ConnectedComponents {

  case class Vertex(id: Long, label: Long)

  case class Link(from: Long, to: Long)

  def getVertices(env: ExecutionEnvironment, params: ParameterTool): DataSet[Vertex] = {
    if (params.has("vertices")) {
      env.readCsvFile[Tuple1[Long]](params.get("vertices"),
        fieldDelimiter = " ", lineDelimiter = "\n", includedFields = Array(0))
        .map(x => Vertex(x._1, x._1)).withForwardedFields("_1->id;_1->label")
    } else {
      env.fromCollection(ConnectedComponentsData.VERTICES)
        .map(x => Vertex(x, x)).withForwardedFields("*->id;*->label")
    }
  }

  def getLinks(env: ExecutionEnvironment, params: ParameterTool): DataSet[Link] = {
    if (params.has("edges")) {
      env.readCsvFile[(Long, Long)](params.get("edges"),
        fieldDelimiter = " ", lineDelimiter = "\n", includedFields = Array(0, 1))
        .map(x => Link(x._1, x._2)).withForwardedFields("_1->id;_2->label")

    } else {
      env.fromCollection(ConnectedComponentsData.EDGES)
        .map(x => Link(x(0).asInstanceOf[Long], x(1).asInstanceOf[Long]))
    }
  }


  def main(args: Array[String]): Unit = {
    // setup env with params
    val env = ExecutionEnvironment.getExecutionEnvironment
    val params = ParameterTool.fromArgs(args)
    env.getConfig.setGlobalJobParameters(params)

    // get data
    val vertices = getVertices(env, params)
    val edges = getLinks(env, params)
    val maxIterations = params.getInt("maxIterations", 10)
    // make plan for connected comps
    val result: DataSet[Vertex] = vertices.iterateDelta(vertices, maxIterations, Array("id")) { (solset, workset) =>

      // every node in work set, broadcast label to neighbours
      val bcLabels = workset.join(edges).where("id").equalTo("from") { (vertex, link) =>
        Vertex(link.to, vertex.label)
      }.withForwardedFieldsFirst("label->label").withForwardedFieldsSecond("to->id")

      // for each vertx, get min among it's received
      val bestBcLabel = bcLabels.groupBy("id").min("label")

      // see if it's better (less) than existing labels, if it's add to future working set/solution set
      val updatedComps = bestBcLabel.join(solset).where("id").equalTo("id") {
        (newVertex, oldVertex, out: Collector[Vertex]) =>
          if (newVertex.label < oldVertex.label) {
            println(s"Adding vertx: $newVertex <- oldVertex: $oldVertex")
            out.collect(newVertex)
          }
      }.withForwardedFieldsFirst("*")
      println("ITERATION done")

      (updatedComps, updatedComps)
    }
    // write to stdout
    result.print()
  }
}
