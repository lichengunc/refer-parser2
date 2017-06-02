"""
This parser is to extract "real" relative position word, as well as absolute position word.
For clefParser and cocoParser, there are quite amount of inaccurate (r5, r6), e.g., (prep_in, shirt) for "The boy in white shirt."
On the one hand, this belongs to details of the referred object itself; On the other hand, this doesn't actually reflect position.
Here, we extract:
1) NN, JJ, VB, ...             as object's attribute words,
2) big, large, ...             as object's relative size words,
3) left, right, top, ...       as absolute position words,
4) <left> object, ...          as relative location and object pairs,

Approach: we rely on the parsed r1-r7 from clef/coco Parser, and categorize them into the above four types.
1) r1, r2, r7 and r8 into attribute words (without forbidden words)
2) check "prep_with" and "prep_in" of (r5, r6), put some of them into attribute words
3)

"""




