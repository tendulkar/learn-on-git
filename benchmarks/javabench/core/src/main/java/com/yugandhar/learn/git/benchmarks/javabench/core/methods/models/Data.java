package com.yugandhar.learn.git.benchmarks.javabench.core.methods.models;

import com.yugandhar.learn.git.benchmarks.javabench.core.methods.services.AbstractCoder;
import com.yugandhar.learn.git.benchmarks.javabench.core.methods.services.Coder;
import com.yugandhar.learn.git.benchmarks.javabench.core.methods.services.Coder0;
import com.yugandhar.learn.git.benchmarks.javabench.core.methods.services.Coder1;
import org.openjdk.jmh.annotations.CompilerControl;

/**
 * @author Yugandhar
 */
public class Data {

    private static final Coder0 coder0 = new Coder0();
    private static final Coder1 coder1 = new Coder1();
    private final Coder coder;
    private final AbstractCoder abstractCoder;
    private final byte id;
    private final byte[] data;

    public Data(byte id, byte[] data) {
        this.id = id;
        this.data = data;
        this.coder = coder0;
        this.abstractCoder = coder0;
    }

    private Coder interfaceIdSwitch() {
        switch (id) {
            case 0:
                return coder0;
            case 1:
                return coder1;
            default:
                throw new IllegalArgumentException();
        }
    }

    @CompilerControl(CompilerControl.Mode.DONT_INLINE)
    public int doDynamicInterfaceRef() {
        return coder.work(data);
    }

    @CompilerControl(CompilerControl.Mode.DONT_INLINE)
    public int doDynamicAbstractRef() {
        return abstractCoder.abstractWork(data);
    }

    @CompilerControl(CompilerControl.Mode.DONT_INLINE)
    public int doStaticRef() {
        return Coder0.staticWork(data);
    }
}
