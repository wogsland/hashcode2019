def score_pair(s1_tags, s2_tags):
    common_tags = 0
    not_in_s1_tags = 0
    not_in_s2_tags = 0
    for tag1 in s1_tags:
        found_in_2 = False
        for tag2 in s2_tags:
            if tag1 == tag2:
                common_tags = common_tags + 1
                found_in_2 = True
        if not found_in_2:
            not_in_s2_tags = not_in_s2_tags + 1
    not_in_s1_tags = len(s2_tags) - common_tags
    # print 'common_tags'
    # print common_tags
    # print 'not_in_s1_tags'
    # print not_in_s1_tags
    # print 'not_in_s2_tags'
    # print not_in_s2_tags
    score = min(common_tags, not_in_s1_tags, not_in_s2_tags)
    # print 'score {}'.format(score)
    return score


def get_vertical_tags(row, images):
    indexes = row.split(' ')
    tags1 = images[int(indexes[0])][3]
    tags2 = images[int(indexes[1])][3]
    nondupes = set(tags2) - set(tags1)
    return tags1 + list(nondupes)


def score_slideshow(slideshow, images):
    """
    For two subsequent slides Si and Si+1, the interest factor is the minimum (the
    smallest number of the three) of:
    - the number of common tags between Si and Si+1
    - the number of tags in Si but not in Si+1
    - the number of tags in Si+1 but not in Si
    """
    score = 0
    for i in range(0, len(slideshow) - 1):
        row1 = slideshow[i]
        s1_tags = []
        if type(row1) is str:
            s1_tags = get_vertical_tags(row1, images)
        else:
            s1_tags = images[row1][3]
        # print 's1_tags'
        # print s1_tags
        row2 = slideshow[i + 1]
        s2_tags = []
        if type(row2) is str:
            s2_tags = get_vertical_tags(row2, images)
        else:
            s2_tags = images[row2][3]
        # print 's2_tags'
        # print s2_tags
        score = score + score_pair(s1_tags, s2_tags)
        # print 'score {}'.format(score)
    return score


def create_output(filename):
    # read in file
    count = -1
    images = []
    for line in open(filename + '.txt', 'r'):
        # print line
        if count > -1:
            trunk = line.split('\n')
            pieces = trunk[0].split(' ')
            image = [count]
            image.append(pieces[0])
            image.append(pieces[1])
            image.append(pieces[2:])
            images.append(image)
        count = count + 1

    # build + score slideshows

    # only horizontal
    """
    slideshow = []
    for image in images:
        # print image
        if image[1] == 'H':
            slideshow.append(image[0])
    print 'horizontal only'
    # print slideshow
    print 'score {}'.format(score_slideshow(slideshow, images))
    """

    # horizontal + vertical pairs
    slideshow = []
    vertical_pair = ''
    for image in images:
        # print image
        if image[1] == 'H':
            slideshow.append(image[0])
        else:
            # print 'a vertical image'
            if '' == vertical_pair:
                vertical_pair = str(image[0])
            else:
                slideshow.append(vertical_pair + ' ' + str(image[0]))
                vertical_pair = ''
            # print 'vertical_pair: {}'.format(vertical_pair)
    print 'horizontal + vertical pairs'
    # print slideshow
    score = score_slideshow(slideshow, images)
    print 'score {}'.format(score)

    # output file
    f = open(filename + ".out", "w")
    f.write(str(len(slideshow)) + '\n')
    for slide in slideshow:
        f.write(str(slide) + '\n')

    return score


total_score = 0
total_score = total_score + create_output('a_example')
total_score = total_score + create_output('b_lovely_landscapes')
total_score = total_score + create_output('c_memorable_moments')
total_score = total_score + create_output('d_pet_pictures')
total_score = total_score + create_output('e_shiny_selfies')
print 'total_score: {}'.format(total_score)
