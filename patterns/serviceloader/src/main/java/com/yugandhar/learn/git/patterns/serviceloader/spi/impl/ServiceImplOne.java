package com.yugandhar.learn.git.patterns.serviceloader.spi.impl;

import com.yugandhar.learn.git.patterns.serviceloader.spi.IService;

/**
 * @author Yugandhar
 */
public class ServiceImplOne implements IService {
    public void show() {
        System.out.println("ServiceImplOne is used!");
    }
}
