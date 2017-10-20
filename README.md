# pyFreeAssociation

python binder for [FreeAssociation](http://w3.usf.edu/FreeAssociation/)

## FreeAssociation
In FreeAssociation,
>Participants were asked to write the first word that came to mind that was meaningfully related or strongly associated to the presented word on the blank shown next to each item. For example, if given BOOK _________, they might write READ on the blank next to it. This procedure is called a discrete association task because each participant is asked to produce only a single associate to each word.

And in FreeAssociation, many index listed below are defined and calculated. The important thing is that we should consider about not only direct associative links but also INDIRECT ones. By INDIRECT, I mean 2 or more step links. For example, if A is linked to WORD and WORD is linked to ENGLISH, we could say that A is also in some meaning linked to ENGLISH.

|Index Name|Description|
|:--:|:--:|
|CUE|Normed Word|
|TARGET|Response to Normed Word|
|NORMED?|Is Response Normed?|
|#G|Group size|
|#P|Number of Participants Producing Response|
|FSG|Forward Cue-to-Target Strength|
|BSG|Backward Target-to-Cue Strength|
|MSG|Mediated Strength|
|OSG|Overlapping Associate Strength|
|#M|Number of Mediators|
|MMIA|Number of Non-Normed Potential Mediating Associates|
|#O|Number of Overlapping Associates|
|OMIA|Number of Non-Normed Overlapping Associates|
|QSS|Cue: Set Size|
|QFR|Cue: Frequency|
|QCON|Cue: Concreteness|
|QH|Cue is a Homograph?|
|QPS|Cue: Part of Speech|
|QMC|Cue: Mean Connectivity Among Its Associates|
|QPR|Cue: Probability of a Resonant Connection|
|QRSG|Cue: Resonant Strength¥
|QUC|Cue: Use Code|
|TSS|Target: Set Size|
|TFR|Target: Frequency|
|TCON|Target: Concreteness|
|TH|Target is a Homograph?|
|TPS|Target: Part of Speech|
|TMC|Target: Mean Connectivity Among Its Associates|
|TPR|Target: Probability of a Resonant Connection|
|TRSG|Target: Resonant Strength|
|TUC|Target: Use Code|

## How To Use
Just `import FreeAssocation` and declare of use like `fa = FreeAssociation()`. Then you can use many kind of method defined in FreeAssociation Object which you can find in FreeAssociation.py file.

## TODO
Now in FreeAssociation Object, a few methods are defined and not all informations are extracted from the source. The index such as QFR, QPR, etc. are not used. However the sqlite database contains as much data as the source, We can extract some data and use them for some purpose. And also I'm now begging the developer of Japanese Associative Concept Dictionary to give me the data. After I get the data I will bind them to this system so that you can find both English and Japanese associations.
