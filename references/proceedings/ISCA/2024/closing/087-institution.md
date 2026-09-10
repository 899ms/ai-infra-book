<!-- 从 087-institution.html 迁移的资料快照；原始 HTML SHA-256: 534828c1398034b8d1132ac6df310253f49af8980390f2ef1e185ec5b840a493。 -->

# GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms

Sandeepa Bhuyan

, Ziyu Ying

, [Mahmut T. Kandemir](https://pure.psu.edu/en/persons/mahmut-kandemir/)

, [Mahanth Gowda](https://pure.psu.edu/en/persons/mahanth-gowda/)

, [Chita R. Das](https://pure.psu.edu/en/persons/chitaranjan-das/)

- [Computer Science and Engineering](https://pure.psu.edu/en/organisations/computer-science-and-engineering/)
- [Institute for Computational and Data Sciences (ICDS)](https://pure.psu.edu/en/organisations/httpsicspsuedu/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[10   Link opens in a new tab](https://www.scopus.com/pages/publications/85201153642#tab=citedBy) Scopus citations

[](https://plu.mx/plum/a/?doi=10.1109/ISCA59077.2024.00097)

- [ Overview ](/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/)
- [ Fingerprint ](/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/fingerprints/)

## Abstract

Cloud gaming (also referred to as Game Streaming) is a rapidly emerging application that is changing the way people enjoy video games. However, if the user demands a high-resolution (e.g., 2 K or 4 K) stream, the game frames require high bandwidth and the stream often suffers from a significant number of frame drops due to network congestion degrading the Quality of Experience (QoE). Recently, the DNN-based Super Resolution (SR) technique has gained prominence as a practical alternative for streaming low-resolution frames and upscaling them at the client for enhanced video quality. However, performing such DNN-based tasks on resource-constrained and battery-operated mobile platforms is very expensive and also fails to meet the real-time requirement (60 frames per second (FPS)). Unlike traditional video streaming, where the frames can be downloaded and buffered, and then upscaled by their playback turn, Game Streaming is real-time and interactive, where the frames are generated on the fly and cannot tolerate high latency/lags for frame upscaling. Thus, state-of-the-art (SOTA) DNN-based SR cannot satisfy the mobile Game Streaming requirements. Towards this, we propose GameStreamSR, a framework for enabling real-time Super Resolution for Game Streaming applications on mobile platforms. We take visual perception nature into consideration and propose to only apply DNN-based SR to the regions with high visual importance and upscale the remaining regions using traditional solutions such as bilinear interpolation. Especially, we leverage the depth data from the game rendering pipeline to intelligently localize the important regions, called regions of importance (RoI), in the rendered game frames. Our evaluation of ten popular games on commodity mobile platforms shows that our proposal can enable realtime (60 FPS) neurally-augmented SR. Our design achieves a 13 × frame rate speedup (and \approx 4 × Motion-to-Photon latency improvement) for the reference frames and a 1.6 × frame rate speedup for the non-reference frames, which translates to, on average 2 × FPS performance improvement and 26-33% energy savings over the SOTA DNN-based SR execution, while achieving about 2dB PSNR gain and better perceptual quality than the current SOTA.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | Proceedings - International Symposium on Computer Architecture |
| ISSN (Print) | 1063-6897 |
| ISSN (Electronic) | 2575-713X |

### Conference

|  |  |
|----|----|
| Conference | 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 |
| Country/Territory | Argentina |
| City | Buenos Aires |
| Period | 6/29/24 → 7/3/24 |

## All Science Journal Classification (ASJC) codes

- Hardware and Architecture

## Access to Document

- [10.1109/ISCA59077.2024.00097](https://doi.org/10.1109/ISCA59077.2024.00097)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85201153642)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/85201153642#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms'. Together they form a unique fingerprint.

-  Super-resolution Keyphrases 100%
-  Mobile Platform Keyphrases 100%
-  DNN-based Keyphrases 100%
-  Augmented Games Keyphrases 100%
-  Game Streaming Keyphrases 100%
-  super resolution Computer Science 100%
-  Deep Neural Network Computer Science 83%
-  Frames per Second Keyphrases 60%

[ View full fingerprint ](/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Bhuyan, S., Ying, Z.[, Kandemir, M. T.](https://pure.psu.edu/en/persons/mahmut-kandemir/)[, Gowda, M.](https://pure.psu.edu/en/persons/mahanth-gowda/)[, & Das, C. R.](https://pure.psu.edu/en/persons/chitaranjan-das/) (2024). [GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms](https://pure.psu.edu/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/). In *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024* (pp. 1309-1322). (Proceedings - International Symposium on Computer Architecture). Institute of Electrical and Electronics Engineers Inc.. [https://doi.org/10.1109/ISCA59077.2024.00097](https://doi.org/10.1109/ISCA59077.2024.00097)

Bhuyan, Sandeepa ; Ying, Ziyu [ ; Kandemir, Mahmut T.](https://pure.psu.edu/en/persons/mahmut-kandemir/) et al. / [**GameStreamSR : Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms**](https://pure.psu.edu/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/). Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. pp. 1309-1322 (Proceedings - International Symposium on Computer Architecture).

@inproceedings{44b04fd0ab9e436789cf2a6dddf7f954,

title = "GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms",

abstract = "Cloud gaming (also referred to as Game Streaming) is a rapidly emerging application that is changing the way people enjoy video games. However, if the user demands a high-resolution (e.g., 2 K or 4 K) stream, the game frames require high bandwidth and the stream often suffers from a significant number of frame drops due to network congestion degrading the Quality of Experience (QoE). Recently, the DNN-based Super Resolution (SR) technique has gained prominence as a practical alternative for streaming low-resolution frames and upscaling them at the client for enhanced video quality. However, performing such DNN-based tasks on resource-constrained and battery-operated mobile platforms is very expensive and also fails to meet the real-time requirement (60 frames per second (FPS)). Unlike traditional video streaming, where the frames can be downloaded and buffered, and then upscaled by their playback turn, Game Streaming is real-time and interactive, where the frames are generated on the fly and cannot tolerate high latency/lags for frame upscaling. Thus, state-of-the-art (SOTA) DNN-based SR cannot satisfy the mobile Game Streaming requirements. Towards this, we propose GameStreamSR, a framework for enabling real-time Super Resolution for Game Streaming applications on mobile platforms. We take visual perception nature into consideration and propose to only apply DNN-based SR to the regions with high visual importance and upscale the remaining regions using traditional solutions such as bilinear interpolation. Especially, we leverage the depth data from the game rendering pipeline to intelligently localize the important regions, called regions of importance (RoI), in the rendered game frames. Our evaluation of ten popular games on commodity mobile platforms shows that our proposal can enable realtime (60 FPS) neurally-augmented SR. Our design achieves a 13 {\texttimes} frame rate speedup (and \textbackslash{}approx 4 {\texttimes} Motion-to-Photon latency improvement) for the reference frames and a 1.6 {\texttimes} frame rate speedup for the non-reference frames, which translates to, on average 2 {\texttimes} FPS performance improvement and 26-33\\ energy savings over the SOTA DNN-based SR execution, while achieving about 2dB PSNR gain and better perceptual quality than the current SOTA.",

author = "Sandeepa Bhuyan and Ziyu Ying and Kandemir, \\Mahmut T.\\ and Mahanth Gowda and Das, \\Chita R.\\",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 ; Conference date: 29-06-2024 Through 03-07-2024",

year = "2024",

doi = "10.1109/ISCA59077.2024.00097",

language = "English (US)",

series = "Proceedings - International Symposium on Computer Architecture",

publisher = "Institute of Electrical and Electronics Engineers Inc.",

pages = "1309--1322",

booktitle = "Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024",

address = "United States",

}

Bhuyan, S, Ying, Z[, Kandemir, MT](https://pure.psu.edu/en/persons/mahmut-kandemir/)[, Gowda, M](https://pure.psu.edu/en/persons/mahanth-gowda/)[ & Das, CR](https://pure.psu.edu/en/persons/chitaranjan-das/) 2024, [GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms](https://pure.psu.edu/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/). in *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024.* Proceedings - International Symposium on Computer Architecture, Institute of Electrical and Electronics Engineers Inc., pp. 1309-1322, 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024, Buenos Aires, Argentina, 6/29/24. [https://doi.org/10.1109/ISCA59077.2024.00097](https://doi.org/10.1109/ISCA59077.2024.00097)

[**GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms.**](https://pure.psu.edu/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/) / Bhuyan, Sandeepa; Ying, Ziyu[; Kandemir, Mahmut T.](https://pure.psu.edu/en/persons/mahmut-kandemir/) et al.  
Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. p. 1309-1322 (Proceedings - International Symposium on Computer Architecture).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - GameStreamSR

T2 - 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024

AU - Bhuyan, Sandeepa

AU - Ying, Ziyu

AU - Kandemir, Mahmut T.

AU - Gowda, Mahanth

AU - Das, Chita R.

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - Cloud gaming (also referred to as Game Streaming) is a rapidly emerging application that is changing the way people enjoy video games. However, if the user demands a high-resolution (e.g., 2 K or 4 K) stream, the game frames require high bandwidth and the stream often suffers from a significant number of frame drops due to network congestion degrading the Quality of Experience (QoE). Recently, the DNN-based Super Resolution (SR) technique has gained prominence as a practical alternative for streaming low-resolution frames and upscaling them at the client for enhanced video quality. However, performing such DNN-based tasks on resource-constrained and battery-operated mobile platforms is very expensive and also fails to meet the real-time requirement (60 frames per second (FPS)). Unlike traditional video streaming, where the frames can be downloaded and buffered, and then upscaled by their playback turn, Game Streaming is real-time and interactive, where the frames are generated on the fly and cannot tolerate high latency/lags for frame upscaling. Thus, state-of-the-art (SOTA) DNN-based SR cannot satisfy the mobile Game Streaming requirements. Towards this, we propose GameStreamSR, a framework for enabling real-time Super Resolution for Game Streaming applications on mobile platforms. We take visual perception nature into consideration and propose to only apply DNN-based SR to the regions with high visual importance and upscale the remaining regions using traditional solutions such as bilinear interpolation. Especially, we leverage the depth data from the game rendering pipeline to intelligently localize the important regions, called regions of importance (RoI), in the rendered game frames. Our evaluation of ten popular games on commodity mobile platforms shows that our proposal can enable realtime (60 FPS) neurally-augmented SR. Our design achieves a 13 × frame rate speedup (and \approx 4 × Motion-to-Photon latency improvement) for the reference frames and a 1.6 × frame rate speedup for the non-reference frames, which translates to, on average 2 × FPS performance improvement and 26-33% energy savings over the SOTA DNN-based SR execution, while achieving about 2dB PSNR gain and better perceptual quality than the current SOTA.

AB - Cloud gaming (also referred to as Game Streaming) is a rapidly emerging application that is changing the way people enjoy video games. However, if the user demands a high-resolution (e.g., 2 K or 4 K) stream, the game frames require high bandwidth and the stream often suffers from a significant number of frame drops due to network congestion degrading the Quality of Experience (QoE). Recently, the DNN-based Super Resolution (SR) technique has gained prominence as a practical alternative for streaming low-resolution frames and upscaling them at the client for enhanced video quality. However, performing such DNN-based tasks on resource-constrained and battery-operated mobile platforms is very expensive and also fails to meet the real-time requirement (60 frames per second (FPS)). Unlike traditional video streaming, where the frames can be downloaded and buffered, and then upscaled by their playback turn, Game Streaming is real-time and interactive, where the frames are generated on the fly and cannot tolerate high latency/lags for frame upscaling. Thus, state-of-the-art (SOTA) DNN-based SR cannot satisfy the mobile Game Streaming requirements. Towards this, we propose GameStreamSR, a framework for enabling real-time Super Resolution for Game Streaming applications on mobile platforms. We take visual perception nature into consideration and propose to only apply DNN-based SR to the regions with high visual importance and upscale the remaining regions using traditional solutions such as bilinear interpolation. Especially, we leverage the depth data from the game rendering pipeline to intelligently localize the important regions, called regions of importance (RoI), in the rendered game frames. Our evaluation of ten popular games on commodity mobile platforms shows that our proposal can enable realtime (60 FPS) neurally-augmented SR. Our design achieves a 13 × frame rate speedup (and \approx 4 × Motion-to-Photon latency improvement) for the reference frames and a 1.6 × frame rate speedup for the non-reference frames, which translates to, on average 2 × FPS performance improvement and 26-33% energy savings over the SOTA DNN-based SR execution, while achieving about 2dB PSNR gain and better perceptual quality than the current SOTA.

UR - https://www.scopus.com/pages/publications/85201153642

UR - https://www.scopus.com/pages/publications/85201153642#tab=citedBy

U2 - 10.1109/ISCA59077.2024.00097

DO - 10.1109/ISCA59077.2024.00097

M3 - Conference contribution

AN - SCOPUS:85201153642

T3 - Proceedings - International Symposium on Computer Architecture

SP - 1309

EP - 1322

BT - Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024

PB - Institute of Electrical and Electronics Engineers Inc.

Y2 - 29 June 2024 through 3 July 2024

ER -

Bhuyan S, Ying Z[, Kandemir MT](https://pure.psu.edu/en/persons/mahmut-kandemir/)[, Gowda M](https://pure.psu.edu/en/persons/mahanth-gowda/)[, Das CR](https://pure.psu.edu/en/persons/chitaranjan-das/). [GameStreamSR: Enabling Neural-Augmented Game Streaming on Commodity Mobile Platforms](https://pure.psu.edu/en/publications/gamestreamsr-enabling-neural-augmented-game-streaming-on-commodit/). In Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc. 2024. p. 1309-1322. (Proceedings - International Symposium on Computer Architecture). doi: 10.1109/ISCA59077.2024.00097
