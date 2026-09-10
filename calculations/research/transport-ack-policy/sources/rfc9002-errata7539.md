<!-- 从 rfc9002-errata7539.html 迁移的资料快照；原始 HTML SHA-256: 685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a。 -->

## [RFC 9002](https://www.rfc-editor.org/info/rfc9002) [inline-errata](https://www.rfc-editor.org/rfc/inline-errata/rfc9002.html), "QUIC Loss Detection and Congestion Control", May 2021

**Source of RFC:** quic (wit)

Errata-ID: 7539

Status:  
Verified

Type:  
Technical

Publication Formats:  
TXT PDF HTML

Reported By:  
Sergey Kandaurov

Date Reported:  
2023-06-07

Verified by:  
Zaheduzzaman Sarker

Date Verified:  
2023-06-13

Section 5. says:

``` bg-light
smoothed_rtt = 7/8 * smoothed_rtt + 1/8 * adjusted_rtt
rttvar_sample = abs(smoothed_rtt - adjusted_rtt)
rttvar = 3/4 * rttvar + 1/4 * rttvar_sample
```

It should say:

``` bg-light
rttvar_sample = abs(smoothed_rtt - adjusted_rtt)
rttvar = 3/4 * rttvar + 1/4 * rttvar_sample
smoothed_rtt = 7/8 * smoothed_rtt + 1/8 * adjusted_rtt
```

Notes:

``` bg-light
Per Appendix A.7 of this RFC and Section 2 of the referred RFC 6298,
rttvar should be computed before updating smoothed_rtt itself.
```

[Report New Erratum](/new/entry-instructions/) [Back to Search](/search/)
