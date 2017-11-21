package com.yugandhar.learn.open.ml.tensorflow.java

import com.yugandhar.learn.open.ml.tensorflow.java.ComputationGraph.GraphBuilder
import org.tensorflow.{DataType, Output}

/**
  * @author Yugandhar
  */
object implicits {


  implicit class OutputFun(output: Output) {

    def +(rhs: Output)(implicit builder: GraphBuilder): Output = builder.add(output, rhs)

    def -(rhs: Output)(implicit builder: GraphBuilder): Output = builder.sub(output, rhs)

    def *(rhs: Output)(implicit builder: GraphBuilder): Output = builder.mul(output, rhs)

    def /(rhs: Output)(implicit builder: GraphBuilder): Output = builder.div(output, rhs)

    def exp(implicit builder: GraphBuilder): Output = builder.exp(output)

    def cast(dtype: DataType)(implicit builder: GraphBuilder): Output = builder.cast(output, dtype)

    def *:(rhs: Output)(implicit builder: GraphBuilder): Output = builder.matmul(output, rhs)

  }

}
