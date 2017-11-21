package com.yugandhar.learn.open.ml.tensorflow.java

import java.nio.{FloatBuffer, LongBuffer}

import org.tensorflow._
import org.tensorflow.framework.OpDefProtos

/**
  * @author Yugandhar
  */
object ComputationGraph {

  implicit def toShape(shape: Array[Long]): Shape = Shape.make(shape(0), shape.slice(1, shape.length): _*)

  class GraphBuilder(var graph: Graph) {
    def div(x: Output, y: Output): Output = binaryOp("Div", x, y)

    def mul(x: Output, y: Output): Output = binaryOp("Mul", x, y)

    def sub(x: Output, y: Output): Output = binaryOp("Sub", x, y)

    def add(x: Output, y: Output): Output = binaryOp("Add", x, y)

    def exp(x: Output): Output = unaryOp("Exp", x)

    def pow(x: Output, e: Output): Output = binaryOp("Pow", x, e)

    def concat(x: Output, y: Output, dims: Output): Output = {
      graph.opBuilder("Concat", "Concat").addInput(dims.asOutput()).addInputList(Array(x, y)).build.output(0)
    }

    def log(x: Output): Output = unaryOp("Log", x)

    def sigmoid(x: Output): Output = unaryOp("Sigmoid", x)

    def sum(x: Output, dims: Output): Output = binaryOpKeepDims("Sum", x, dims)

    def mean(x: Output, dims: Output): Output = binaryOpKeepDims("Mean", x, dims)

    def min(x: Output, dims: Output): Output = binaryOpKeepDims("Min", x, dims)

    def max(x: Output, dims: Output): Output = binaryOpKeepDims("Max", x, dims)

    def sqrt(x: Output, dims: Output): Output = unaryOp("Sqrt", x)

    def matmul(x: Output, y: Output): Output = binaryOp("MatMul", y, x)

    def tile(x: Output, dims: Output): Output = binaryOp("Tile", x, dims)

    def slice(x: Output, begin: Output, size: Output): Output = {
      graph.opBuilder("Slice", "Slice").addInput(x).addInput(begin).addInput(size).build.output(0)
    }

    def minimum(x: Output, y: Output): Output = binaryOp("Minimum", x, y)

    def maximum(x: Output, y: Output): Output = binaryOp("Maximum", x, y)

    def argMin(x: Output, y: Output): Output = binaryOp("ArgMin", x, y)

    def argMax(x: Output, y: Output): Output = binaryOp("ArgMax", x, y)

    def oneHot(x: Output, dims: Output, onValue: Output, offValue: Output): Output = {
      graph.opBuilder("OneHot", "OneHot").addInput(x).addInput(dims).addInput(onValue).addInput(offValue).build.output(0)
    }

    def resizeBilinear(images: Output, size: Output): Output = binaryOp("ResizeBilinear", images, size)

    def expandDims(input: Output, dim: Output): Output = binaryOp("ExpandDims", input, dim)

    def cast(value: Output, dtype: DataType): Output = graph.opBuilder("Cast", "Cast").addInput(value).setAttr("DstT", dtype).build.output(0)

    def decodeJpeg(contents: Output, channels: Long): Output = graph.opBuilder("DecodeJpeg", "DecodeJpeg").addInput(contents).setAttr("channels", channels).build.output(0)

    def constant(name: String, value: Any): Output = try {
      val t = Tensor.create(value)
      try
        graph.opBuilder("Const", name).setAttr("dtype", t.dataType).setAttr("value", t).build.output(0)
      finally if (t != null) t.close()
    }

    def placeholder(name: String, dataType: DataType, firstDim: Long, restDim: Long*): Output = {
      graph.opBuilder("Placeholder", name).setAttr("dtype", dataType)
        .setAttr("shape", Shape.make(firstDim, restDim: _*)).build().output(0)
    }

    def variable(name: String, dataType: DataType, firstDim: Long, restDim: Long*): Output = {
      graph.opBuilder("Variable", name).setAttr("dtype", dataType)
        .setAttr("shape", Shape.make(firstDim, restDim: _*)).build().output(0)
    }


    private def binaryOp(`type`: String, in1: Output, in2: Output) = {
      graph.opBuilder(`type`, `type`).addInput(in1).addInput(in2).build.output(0)
    }

    private def binaryOpKeepDims(op: String, in1: Output, in2: Output) = {
      graph.opBuilder(op, op).addInput(in1).addInput(in2).setAttr("keep_dims", true).build.output(0)
    }

    private def unaryOp(`type`: String, in1: Output) = graph.opBuilder(`type`, `type`).addInput(in1).build.output(0)
  }

  val graph = new Graph()
  val session = new Session(graph)
  implicit val b: GraphBuilder = new GraphBuilder(graph)


  def main(args: Array[String]): Unit = {
    val left: FloatBuffer = FloatBuffer.allocate(300)
    val right: FloatBuffer = FloatBuffer.allocate(300)
    val resBuff: FloatBuffer = FloatBuffer.allocate(300)
    val intBuff: LongBuffer = LongBuffer.allocate(300)
    for (i <- 1 to 300) {
      left.put(i)
      right.put(2 * i)
    }
    left.rewind()
    right.rewind()

    val cr: Tensor = Tensor.create(Array(5, 60L), left)
    val att: Tensor = Tensor.create(Array(300L), right)
    val CR = graph.opBuilder("Placeholder", "CR").setAttr("dtype", cr.dataType())
      .setAttr("shape", Shape.make(5, 60)).build().output(0)
    val ATT = graph.opBuilder("Placeholder", "ATT").setAttr("dtype", att.dataType())
      .setAttr("shape", Shape.make(5, 10, 6)).build().output(0)
    val DIMS = graph.opBuilder("Placeholder", "DIMS").setAttr("dtype", DataType.FLOAT)
      .setAttr("shape", Shape.make(1, 1)).build().output(0)
    val dims = Tensor.create(2.toFloat)
    val r2 = b.pow(CR, DIMS)

    val DIM = graph.opBuilder("Placeholder", "DIM").setAttr("dtype", DataType.INT32)
      .setAttr("shape", Shape.scalar()).build().output(0)
    val dim = Tensor.create(2)

    val DEPTH = graph.opBuilder("Placeholder", "DEPTH").setAttr("dtype", DataType.INT32)
      .setAttr("shape", Shape.scalar()).build().output(0)
    val OnValue = graph.opBuilder("Placeholder", "OnValue").setAttr("dtype", DataType.FLOAT)
      .setAttr("shape", Shape.scalar()).build().output(0)
    val OffValue = graph.opBuilder("Placeholder", "OffValue").setAttr("dtype", DataType.FLOAT)
      .setAttr("shape", Shape.scalar()).build().output(0)
    val BEGIN = graph.opBuilder("Placeholder", "BEGIN").setAttr("dtype", DataType.INT32)
      .setAttr("shape", Shape.make(1)).build().output(0)
    val SIZE = graph.opBuilder("Placeholder", "SIZE").setAttr("dtype", DataType.INT32)
      .setAttr("shape", Shape.make(1)).build().output(0)

    val begin3d = Tensor.create(Array(10, 10))
    val zIn3d = Tensor.create(Array(20, 5))
    val result = b.slice(CR, BEGIN, SIZE)
    val scalar6 = Tensor.create(6)
    val scalar0 = Tensor.create(0.toFloat)
    val scalar1 = Tensor.create(1.toFloat)
    println(s"begin3d: $begin3d, zIn3d: $zIn3d, cr: $cr")
    val res = session.runner().fetch(result).feed("CR", cr).feed(BEGIN, begin3d).feed(SIZE, zIn3d)
        .run().get(0)
    println(s"CR = $CR, ATT = $ATT, res = $res")
    res.writeTo(resBuff)
    println(s"""res -> ${resBuff.array().mkString(",")}""")
  }


}
