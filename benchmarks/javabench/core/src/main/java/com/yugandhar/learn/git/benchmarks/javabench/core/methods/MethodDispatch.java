package com.yugandhar.learn.git.benchmarks.javabench.core.methods;

import com.yugandhar.learn.git.benchmarks.javabench.core.methods.models.Data;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.Random;

/**
 * @author Yugandhar
 */
@State(Scope.Benchmark)
public class MethodDispatch {
    @Param("100")
    private int count;

    private Data[] datas;

    @Setup
    public void setup() {
        datas = new Data[count];
        Random r = new Random();
        for (int c = 0; c < count; c++) {
            byte[] contents = new byte[10];
            r.nextBytes(contents);
            datas[c] = new Data((byte) r.nextInt(2), contents);
        }
    }

    @Benchmark
    public void dynamicInterfaceRef(Blackhole blackhole) {
        Data[] l = datas;
        int c = count;
        for (int i = 0; i < c; ++i) {
            blackhole.consume(l[i].doDynamicInterfaceRef());
        }
    }

    @Benchmark
    public void dynamicAbstractRef(Blackhole blackhole) {
        Data[] l = datas;
        int c = count;
        for (int i = 0; i < c; ++i) {
            blackhole.consume(l[i].doDynamicAbstractRef());
        }
    }

    @Benchmark
    public void staticRef(Blackhole blackhole) {
        Data[] l = datas;
        int c = count;
        for (int i = 0; i < c; ++i) {
            blackhole.consume(l[i].doStaticRef());
        }
    }
}
