<!-- 从 anthropic-prachub.html 迁移的资料快照；原始 HTML SHA-256: dbe757f450acf87f9544ec3900fd809db180c75c2e106aa790f35a39601e7967。 -->

1.  [Home](/)
2.  /
3.  [Interview Experiences](/interview-experiences)
4.  /
5.  [Anthropic](/companies/anthropic)

# Anthropic Software Engineer Interview Experience — Perfect OA, Rejected at the ML Inference System Design Phone Screen

![](https://www.google.com/s2/favicons?domain=anthropic.com&sz=128)

Anthropic·Software Engineer·Jul 2026

Technical ScreenOnline AssessmentRejectedmedium

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWhlYXJ0IiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIgOS41YTUuNSA1LjUgMCAwIDEgOS41OTEtMy42NzYuNTYuNTYgMCAwIDAgLjgxOCAwQTUuNDkgNS40OSAwIDAgMSAyMiA5LjVjMCAyLjI5LTEuNSA0LTMgNS41bC01LjQ5MiA1LjMxM2EyIDIgMCAwIDEtMyAuMDE5TDUgMTVjLTEuNS0xLjUtMy0zLjItMy01LjUiIC8+PC9zdmc+)0

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNoYXJlMiBsdWNpZGUtc2hhcmUtMiIgYXJpYS1oaWRkZW49InRydWUiPjxjaXJjbGUgY3g9IjE4IiBjeT0iNSIgcj0iMyI+PC9jaXJjbGU+PGNpcmNsZSBjeD0iNiIgY3k9IjEyIiByPSIzIj48L2NpcmNsZT48Y2lyY2xlIGN4PSIxOCIgY3k9IjE5IiByPSIzIj48L2NpcmNsZT48bGluZSB4MT0iOC41OSIgeDI9IjE1LjQyIiB5MT0iMTMuNTEiIHkyPSIxNy40OSI+PC9saW5lPjxsaW5lIHgxPSIxNS40MSIgeDI9IjguNTkiIHkxPSI2LjUxIiB5Mj0iMTAuNDkiPjwvbGluZT48L3N2Zz4=)Share

I bugged a former coworker for a referral, and then got rejected right at the phone screen. The round was a system design interview, a classic ML inference design question. I felt okay about it after the interview and don't know why I got rejected. There were a few points where I think I either matched what the interviewer wanted, or was way off. The interviewer gave basically no real-time feedback.

Caching might not have been necessary — I argued that caching didn't make much sense here since the hit ratio wouldn't be high either, and the interviewer at least seemed to agree on the surface.

The batching strategy really was the key focus.

He had me calculate the theoretical max throughput and then estimate the actual throughput. In my own work, real-time inference throughput ends up far below the max throughput that offline inference can hit, because you have to account for latency. The interviewer didn't seem to get my point here and instead asked why it would be so far off from the theoretical max. Maybe I just don't have enough experience — in the online systems I've worked on, you can get to about 70% of offline throughput, and p99 latency is generally not great.

For the GPU server load-balancing strategy, I mentioned random round robin, and the interviewer didn't seem too convinced.

I prepared for a long time, got a perfect 600/600 on the OA, and then got rejected at the phone screen. That stings a bit.

Published Aug 24, 2026

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMyIgaGVpZ2h0PSIxMyIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNwYXJrbGVzIHRleHQtZW1lcmFsZC01MDAiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMTEuMDE3IDIuODE0YTEgMSAwIDAgMSAxLjk2NiAwbDEuMDUxIDUuNTU4YTIgMiAwIDAgMCAxLjU5NCAxLjU5NGw1LjU1OCAxLjA1MWExIDEgMCAwIDEgMCAxLjk2NmwtNS41NTggMS4wNTFhMiAyIDAgMCAwLTEuNTk0IDEuNTk0bC0xLjA1MSA1LjU1OGExIDEgMCAwIDEtMS45NjYgMGwtMS4wNTEtNS41NThhMiAyIDAgMCAwLTEuNTk0LTEuNTk0bC01LjU1OC0xLjA1MWExIDEgMCAwIDEgMC0xLjk2Nmw1LjU1OC0xLjA1MWEyIDIgMCAwIDAgMS41OTQtMS41OTR6IiAvPjxwYXRoIGQ9Ik0yMCAydjQiIC8+PHBhdGggZD0iTTIyIDRoLTQiIC8+PGNpcmNsZSBjeD0iNCIgY3k9IjIwIiByPSIyIj48L2NpcmNsZT48L3N2Zz4=)Curated and edited by PracHub

## Practice the questions from this interview

[](/interview-questions/design-a-low-latency-gpu-inference-service)

Design a Low-Latency GPU Inference ServiceML System Design

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNSIgaGVpZ2h0PSIxNSIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb24tcmlnaHQgc2hyaW5rLTAgdGV4dC16aW5jLTQwMCBncm91cC1ob3Zlcjp0ZXh0LWVtZXJhbGQtNjAwIGRhcms6Z3JvdXAtaG92ZXI6dGV4dC1lbWVyYWxkLTQwMCB0cmFuc2l0aW9uLWNvbG9ycyIgYXJpYS1oaWRkZW49InRydWUiPjxwYXRoIGQ9Im05IDE4IDYtNi02LTYiIC8+PC9zdmc+)

## ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLW1lc3NhZ2Utc3F1YXJlIHRleHQtZW1lcmFsZC02MDAgZGFyazp0ZXh0LWVtZXJhbGQtNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIyIDE3YTIgMiAwIDAgMS0yIDJINi44MjhhMiAyIDAgMCAwLTEuNDE0LjU4NmwtMi4yMDIgMi4yMDJBLjcxLjcxIDAgMCAxIDIgMjEuMjg2VjVhMiAyIDAgMCAxIDItMmgxNmEyIDIgMCAwIDEgMiAyeiIgLz48L3N2Zz4=)Discussion

[Sign in](/login?redirect=/interview-experiences/anthropic-software-engineer-interview-experience-perfect-oa-rejected-at-the-ml-inference-system-design-phone-screen%23comments) to join the discussion. The author is notified of every comment.

Loading comments…
