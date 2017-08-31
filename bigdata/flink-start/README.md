# Flink learning
True streaming engine (process data as soon as it's received with little buffers)

### Modules
* concepts

## Concepts
#### Iterations (applicable only DataSet API)
1. full iteration
* every iteration partial solution will be overridden
* can be limited by iterations, or empty result in the step function

2. delta iteration
* every iteration the resultant **diff** will be added to **final solution set**
* use another workset as context
* can be limited by iterations, or not updating the solution set
* Remember step function won't be executed every time, it'll just make plan out of it and reuses it

#### Streaming (DataStream API)
1. windowing
2. keyBy
3. groupBy
4. reduceBy

## Optimisations
1. `withForwardFields`, `withForwardFiedlsFirst`, `withForwardFieldsSecond` will help flink to copy the column of data, without replication
2. similarly for `readFields*` which will be used for reading and evaluating