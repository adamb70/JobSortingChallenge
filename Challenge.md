## Solution

Similar to model [topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) problems.


Usual implementations of topological sorting build an outgoing adjacency list (`dependency => [task1, task2]`). In this challenge we are given an input in the opposite (incoming) form `task => dependency`. We also only need to deal with a single item in each mapping instead of a list. This makes it easier to work with a simple DFS instead of using one of the usual topological sorting algorithms.

## The Challenge

Imagine we have a list of jobs, each represented by a character. Because certain jobs must be
done before others, a job may have a dependency on another job. For example, `a` may depend
on `b`, meaning the final sequence of jobs should place `b` before `a`. If `a` has no dependency, the
position of `a` in the final sequence does not matter.

##### Given you’re passed an empty string (no jobs), the result should be an empty sequence.

##### Given the following job structure:
```
a =>
```
The result should be a sequence consisting of a single job `a`.
  
##### Given the following job structure:
```
a =>
b =>
c =>
```
The result should be a sequence containing all three jobs `abc` in no significant order.

##### Given the following job structure:
```
a =>
b => c
c =>
```
The result should be a sequence that positions `c` before `b`, containing all three jobs `abc`.

##### Given the following job structure:
```
a =>
b => c
c => f
d => a
e => b
f =>
```
The result should be a sequence that positions `f` before `c`, `c` before `b`, `b` before `e` and `a`
before `d` containing all six jobs `abcdef`.

##### Given the following job structure:
```
a =>
b =>
c => c
```
The result should be an `error` stating that jobs can’t depend on themselves.

##### Given the following job structure:
```
a =>
b => c
c => f
d => a
e =>
f => b
```
The result should be an `error` stating that jobs can’t have circular dependencies.

