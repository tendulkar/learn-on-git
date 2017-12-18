package com.yugandhar.learn.git.benchmarks.javabench.core.methods.services;

/**
 * @author Yugandhar
 */
public class Coder0 extends AbstractCoder implements Coder {
    public static int staticWork(byte[] data) {
        return data.length;
    }

    @Override
    public int abstractWork(byte[] data) {
        return data.length;
    }

    @Override
    public int work(byte[] data) {
        return data.length;
    }
}
