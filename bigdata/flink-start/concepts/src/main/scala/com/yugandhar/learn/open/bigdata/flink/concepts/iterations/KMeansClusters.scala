package com.yugandhar.learn.open.bigdata.flink.concepts.iterations

import java.lang

import org.apache.flink.api.common.functions.{GroupReduceFunction, RichMapFunction}
import org.apache.flink.api.java.functions.FunctionAnnotation.ForwardedFields
import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.api.scala.{ExecutionEnvironment, _}
import org.apache.flink.examples.java.clustering.util.KMeansData
import org.apache.flink.configuration.Configuration
import org.apache.flink.util.Collector


import scala.collection.JavaConverters._

/**
  * Using full iterations
  *
  * @author Yugandhar
  */
object KMeansClusters {

  trait Coordinate extends Serializable {
    var x: Double
    var y: Double

    def add(c: Coordinate): this.type = {
      x += c.x
      y += c.y
      this
    }

    def div(z: Double): this.type = {
      x /= z
      y /= z
      this
    }

    def clear(): Unit = {
      x = 0d
      y = 0d
    }

    def distance(c: Coordinate): Double = {
      math.sqrt((x - c.x) * (x - c.x) + (y - c.y) * (y - c.y))
    }

    override def toString: String = s"$x $y"
  }

  @SerialVersionUID(83971112000L)
  case class Point(override var x: Double, override var y: Double) extends Coordinate

  @SerialVersionUID(876354897234095L)
  case class Centroid(var id: Int = 0, override var x: Double = 0d, override var y: Double = 0d) extends Coordinate {
    override def toString: String = s"$id => $x, $y"
  }

  def getPoints(env: ExecutionEnvironment, params: ParameterTool): DataSet[Point] = {
    if (params.has("points")) {
      env.readCsvFile[(Double, Double)](params.get("points"),
        fieldDelimiter = " ", lineDelimiter = "\n", includedFields = Array(0, 1))
        .map(x => Point(x._1, x._2))
    } else {
      env.fromCollection(KMeansData.POINTS.map {
        case Array(x, y) => Point(x.asInstanceOf[Double], y.asInstanceOf[Double])
      })
    }
  }

  def getCentroids(env: ExecutionEnvironment, params: ParameterTool): DataSet[Centroid] = {
    if (params.has("centroids")) {
      env.readCsvFile[(Int, Double, Double)](params.get("centroids"),
        fieldDelimiter = " ", lineDelimiter = "\n", includedFields = Array(0, 1, 2))
        .map(x => Centroid(x._1, x._2, x._3))
    } else {
      env.fromCollection(KMeansData.CENTROIDS.map {
        case Array(id, x, y) => Centroid(id.asInstanceOf[Int], x.asInstanceOf[Double], y.asInstanceOf[Double])
      })
    }
  }

  @ForwardedFields(Array("*->_2"))
  class SelectNearest extends RichMapFunction[Point, (Int, Point)] {
    var centroids: Traversable[Centroid] = _

    override def open(parameters: Configuration): Unit = {
      centroids = getRuntimeContext.getBroadcastVariable[Centroid]("centroids").asScala
    }

    override def map(p: Point): (Int, Point) = {
      var nearestId = -1
      var nearestDist = 0d
      centroids.foreach(centroid => {
        val dist = p.distance(centroid)
        if (nearestId == -1 || nearestDist > dist) {
          nearestDist = dist
          nearestId = centroid.id
        }
      })
      (nearestId, p)
    }
  }

  def main(args: Array[String]): Unit = {
    // setup env
    val env = ExecutionEnvironment.getExecutionEnvironment
    val params = ParameterTool.fromArgs(args)
    env.getConfig.setGlobalJobParameters(params)

    // get data
    val points = getPoints(env, params)
    val centroids = getCentroids(env, params)
    val maxIterations = params.getInt("maxIterations", 10)

    // plan for kmeans
    val finalCentroids = centroids.iterate(maxIterations) { currentCentroids =>
      // first, find nearest centroids
      val clustePts = points.map(new SelectNearest).withBroadcastSet(currentCentroids, "centroids")
      // recalculate cluster centroid
      val newCentroids = clustePts.map(x => (x._1, x._2, 1L))
        .groupBy(0).reduceGroup(new GroupReduceFunction[(Int, Point, Long), Centroid] {
        override def reduce(values: lang.Iterable[(Int, Point, Long)], out: Collector[Centroid]): Unit = {
          var cnt = 0d
          var id = -1
          val pt = Point(0, 0)
          values.asScala.foreach(x => {
            pt.add(x._2)
            cnt += 1d
            id = x._1
          })
          val centroid = pt.div(cnt)
          out.collect(Centroid(id, centroid.x, centroid.y))
        }
      })
      newCentroids
    }
    // calculate centroid of each cluster
    val result = points.map(new SelectNearest).withBroadcastSet(finalCentroids, "centroids")
    println("****************************Centroids************")
    finalCentroids.print()
    println("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    println("************************Points**********************")
    result.map(x => (x._1, 1L)).groupBy(0).reduce((p1, p2) => (p1._1, p1._2 + p2._2)).print()
    println("====================================================")
    // write to stdout
  }

}
