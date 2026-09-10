<!-- 从 cheri-simt-institution.html 迁移的资料快照；原始 HTML SHA-256: 61cfe06df3b0664b725629c183b1cc968f120ebe34b701d316d72db2573ceffc。 -->

 

## CHERI-SIMT: Implementing Capability Memory Protection in GPUs

#####  Accepted version 

##### ![](data:image/svg+xml;base64,PHN2ZyBfbmdjb250ZW50LWRzcGFjZS1hbmd1bGFyLWMyNTA2NTg0NDgzIGFyaWEtaGlkZGVuPSJ0cnVlIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHN0eWxlPSJwb3NpdGlvbjogYWJzb2x1dGU7IHdpZHRoOiAwOyBoZWlnaHQ6IDA7IG92ZXJmbG93OiBoaWRkZW47Ij48ZGVmcyBfbmdjb250ZW50LWRzcGFjZS1hbmd1bGFyLWMyNTA2NTg0NDgzPjxzeW1ib2wgX25nY29udGVudC1kc3BhY2UtYW5ndWxhci1jMjUwNjU4NDQ4MyBpZD0iaWNvbi11c2VyLWNoZWNrIiB2aWV3Ym94PSIwIDAgMzIgMzIiPjxwYXRoIF9uZ2NvbnRlbnQtZHNwYWNlLWFuZ3VsYXItYzI1MDY1ODQ0ODMgZD0iTTMwIDE5bC05IDktMy0zLTIgMiA1IDUgMTEtMTF6IiAvPjxwYXRoIF9uZ2NvbnRlbnQtZHNwYWNlLWFuZ3VsYXItYzI1MDY1ODQ0ODMgZD0iTTE0IDI0aDEwdi0zLjU5OGMtMi4xMDEtMS4yMjUtNC44ODUtMi4wNjYtOC0yLjMyMXYtMS42NDljMi4yMDMtMS4yNDIgNC00LjMzNyA0LTcuNDMyIDAtNC45NzEgMC05LTYtOXMtNiA0LjAyOS02IDljMCAzLjA5NiAxLjc5NyA2LjE5MSA0IDcuNDMydjEuNjQ5Yy02Ljc4NCAwLjU1NS0xMiAzLjg4OC0xMiA3LjkxOGgxNHYtMnoiIC8+PC9zeW1ib2w+PC9kZWZzPjwvc3ZnPg==)![](data:image/svg+xml;base64,PHN2ZyBfbmdjb250ZW50LWRzcGFjZS1hbmd1bGFyLWMyNTA2NTg0NDgzIGNsYXNzPSJpY29uIGljb24tdXNlci1jaGVjayI+PHVzZSBfbmdjb250ZW50LWRzcGFjZS1hbmd1bGFyLWMyNTA2NTg0NDgzIHhsaW5rOmhyZWY9IiNpY29uLXVzZXItY2hlY2siIC8+PC9zdmc+) Peer-reviewed

## Repository URI

[https://www.repository.cam.ac.uk/handle/1810/390089](https://www.repository.cam.ac.uk/handle/1810/390089)

## Repository DOI

[https://doi.org/10.17863/CAM.121764](https://doi.org/10.17863/CAM.121764)

------------------------------------------------------------------------

Loading...

![Thumbnail Image](/)

## Files

[Primary Accepted version (1.18 MB)](/bitstreams/dd683099-0405-4d5b-b2c8-6d4b164480d8/download)

## Type

[Conference Object](/browse/type?startsWith=Conference%20Object)

Full item page

## Change log

## Authors

[Naylor, Matthew](/browse/author?startsWith=Naylor,%20Matthew)

[Joannou, Alexandre](/browse/author?startsWith=Joannou,%20Alexandre)

[Markettos, A Theodore](/browse/author?startsWith=Markettos,%20A%20Theodore)

[Metzger, Paul](/browse/author?startsWith=Metzger,%20Paul)

[Moore, Simon W](/browse/author?startsWith=Moore,%20Simon%20W)

Show 1 more

## Abstract

Governments are increasingly advising software manufacturers to employ memory-safe languages and technologies to combat adversarial attacks on modern computing infrastructure. This introduces pressures across the entire computing industry, including GPU vendors who provide implementations of unsafe C/C++-based languages, such as CUDA and OpenCL, for programming the devices they produce. One of the memory-safety technologies being recommended is Capability Hardware Enhanced RISC Instructions (CHERI). CHERI builds strong and efficient memory safety into underlying instruction-set architectures allowing continued, but memory-safe, use of C/C++-based languages on top. In this paper, we evaluate the feasibility of incorporating CHERI into GPU architectures by extending a prototype, open-source, synthesisable, SIMT core and CUDA-like programming environment with support for CHERI. We present techniques to considerably ameliorate the costs of CHERI in SIMT designs, reducing register-file storage overheads from 103% to 7%, logic-area overheads by 44% to a cost comparable to one additional multiplier per vector lane, and execution-time overheads to 1.6%. With the proposed techniques, CHERI offers a viable path to strong and efficient GPU memory safety, while avoiding the need to replace established programming practices.

## Description

## Keywords

[33 Built Environment and Design](/browse/srsc?startsWith=33%20Built%20Environment%20and%20Design)

## Journal Title

Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 1

## Conference Name

Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 1

## Journal ISSN

## Volume Title

## Publisher

Association for Computing Machinery (ACM)

## Publisher DOI

[https://doi.org/10.1145/3760250.3762234](https://doi.org/10.1145/3760250.3762234)

## Rights and licensing

[![Attribution 4.0 International (CC BY 4.0)](/assets/images/cc-licenses/by.png)](https://creativecommons.org/licenses/by/4.0/)

Except where otherwised noted, this item's license is described as [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

##### Sponsorship

EPSRC (EP/V000381/1)

Our work was supported by the UK EPSRC under the CAPcelerate Project (EP/V000381/1) and the Chrompartments Project (EP/X015963/1), both part of the Digital Security by Design (DSbD) Programme and the DSbDtech initiative.

#### Relationships

**Is supplemented by:**

[https://doi.org/10.17863/CAM.120202](https://doi.org/10.17863/CAM.120202)

[https://doi.org/10.17863/CAM.120202](https://doi.org/10.17863/CAM.120202)

## Collections

[University of Cambridge Research Outputs (Articles and Conferences)](/collections/8221b33d-a09b-486e-89c3-374f99afcbe2)

  
