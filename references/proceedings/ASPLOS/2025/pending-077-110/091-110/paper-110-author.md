<!-- 从 paper-110-author.html 迁移的资料快照；原始 HTML SHA-256: 7b330c5d21f91c958aee3ed93743d46e098df9bc42ce6d7fc3c3379dda5f7556。 -->

Toggle navigation

[Wei Yang](/)

- [Home](/#about)
- [Students](/#students)
- [Research](/#research)
- [Publications](/publication)
- [Teaching](/#teaching)
- [Service](/#service)
- [Contact](/#contact)

# TAOPT: Tool-Agnostic Optimization of Parallelized Automated Mobile UI Testing

Dezhi Ran, Zihe Song, Wenyu Wang, Wei Yang, Tao Xie

- [](https://twitter.com/intent/tweet?text=TAOPT%3a%20Tool-Agnostic%20Optimization%20of%20Parallelized%20Automated%20Mobile%20UI%20Testing&url=http%3a%2f%2fyoungwei.com%2fpublication%2ftaopt%2f)
- [](https://www.facebook.com/sharer.php?u=http%3a%2f%2fyoungwei.com%2fpublication%2ftaopt%2f)
- [](https://www.linkedin.com/shareArticle?mini=true&url=http%3a%2f%2fyoungwei.com%2fpublication%2ftaopt%2f&title=TAOPT%3a%20Tool-Agnostic%20Optimization%20of%20Parallelized%20Automated%20Mobile%20UI%20Testing)
- [](http://service.weibo.com/share/share.php?url=http%3a%2f%2fyoungwei.com%2fpublication%2ftaopt%2f&title=TAOPT%3a%20Tool-Agnostic%20Optimization%20of%20Parallelized%20Automated%20Mobile%20UI%20Testing)
- [](/cdn-cgi/l/email-protection#48773b3d2a222d2b3c751c0907181c6d7b296d7a781c27272465092f26273b3c212b6d7a7807383c21252132293c2127266d7a78272e6d7a7818293a2924242d2421322d2c6d7a78093d3c2725293c2d2c6d7a7805272a21242d6d7a781d016d7a781c2d3b3c21262f6e292538732a272c3175203c3c386d7b296d7a2e6d7a2e31273d262f3f2d21662b27256d7a2e383d2a24212b293c2127266d7a2e3c2927383c6d7a2e)

### Abstract

The emergence of modern testing clouds, equipped with a vast array of real testing devices and high-fidelity emulators, has significantly increased the need for parallel automated mobile testing to optimally utilize the resources of testing clouds. Parallel testing aligns perfectly with the characteristic of rapid iteration cycles for mobile app development, where testing time is limited. While numerous tools have been proposed for optimizing the testing effectiveness on a single testing device, it remains an open problem to optimize the parallelization of automated mobile UI testing in terms of resource and time utilization.  
To optimize the parallelization of automated mobile UI testing, in this paper, we propose TaOPT, a fully automated, tool-agnostic approach, which improves the parallelization effectiveness of any given testing tool without modifying the tool’s internal workflow. In particular, TaOPT conducts online analysis to infer loosely coupled UI subspaces in the App Under Test (AUT). TaOPT then manages access to these subspaces across various testing devices, guiding automated UI testing toward distinct subspaces on different devices without knowing the testing tool’s inner workings. We apply TaOPT on highly popular mobile apps with three state-of-the-art automated UI testing tools for Android. Evaluation results show that TaOPT helps the tools reach comparable code coverage using 60% less testing duration and 62% less machine time than the baseline on average. In addition, TaOPT consistently enhances automated UI testing tools to detect 1.2 to 2.1 times more unique crashes given the same testing resources.

Type

[Conference paper](https://youngwei.com/publication/#1)

Publication

In *the ACM International Conference on Architectural Support for Programming Languages and Operating Systems*.

Date

January, 2025

Links

[PDF](https://youngwei.com/content/project/)

© 2018 · Powered by the [Academic theme](https://sourcethemes.com/academic/) for [Hugo](https://gohugo.io). [ ](#)

×

#### Cite

``` modal-body
```

[ Copy](#) [ Download](#)
