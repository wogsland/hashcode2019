# read in file
count = -1
images = []
for line in open('a_example.txt', 'r'):
    print line
    if count > -1:
        line.split(' ')
        images.append(line)
    count = count + 1

# build slideshow
for image in images:
    print image

"""
For two subsequent slides Si and Si+1, the interest factor is the minimum (the
smallest number of the three) of:
- the number of common tags between Si and Si+1
- the number of tags in Si but not in Si+1
- the number of tags in Si+1 but not in Si
"""

# output file
