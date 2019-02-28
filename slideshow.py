from random import shuffle, randint, sample

files = ['a_example', 'b_lovely_landscapes', 'c_memorable_moments', 'd_pet_pictures', 'e_shiny_selfies']
bests = [2, 39, 1463, 174853, 112853]


def read_images(filename):
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
    return images


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


def get_slide_tags(slide, images):
    tags = []
    if type(slide) is str:
        tags = get_vertical_tags(slide, images)
    else:
        tags = images[slide][3]
    return tags


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
        s1_tags = get_slide_tags(row1, images)
        row2 = slideshow[i + 1]
        s2_tags = get_slide_tags(row2, images)
        score = score + score_pair(s1_tags, s2_tags)
        # print 'score {}'.format(score)
    return score


def create_slideshow(images):
    " builds slideshow "

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
    # print 'horizontal + vertical pairs'
    # print slideshow
    # score = score_slideshow(slideshow, images)
    # print 'score {}'.format(score)

    return slideshow


def optimize_slideshow(slideshow, images):
    " takes a slideshow and optimizes pairs"

    # put slide in new slideshow & remove it
    index = randint(0, len(slideshow) - 1)
    new_slideshow = [slideshow[index]]
    slideshow.pop(index)

    # find the next best slide & remove from random subset of possibles
    for i in range(0, len(slideshow)):
        best_score = 0
        slide1 = new_slideshow[i]
        index_to_remove = 0

        # a more useful version of the slideshow array
        eslideshow = []
        for k, kslide in enumerate(slideshow):
            eslideshow.append([k, kslide])
        slide_subset = sample(eslideshow, min(10, len(slideshow) - 1))
        for j, slide2 in slide_subset:
            tags1 = get_slide_tags(slide1, images)
            tags2 = get_slide_tags(slide2, images)
            score = score_pair(tags1, tags2)
            if score > best_score:
                best_score = score
                index_to_remove = j
        # print 'length {}'.format(len(slideshow))
        # print 'index_to_remove {}'.format(index_to_remove)
        if len(slideshow) > 0:
            new_slideshow.append(slideshow[index_to_remove])
            slideshow.pop(index_to_remove)
    # print slideshow
    return new_slideshow


def create_output(filename):
    # read in file
    images = read_images(filename)

    # create slideshow
    slideshow = create_slideshow(images)
    # score = score_slideshow(slideshow, images)

    best = 0
    for i, name in enumerate(files):
        if name == filename:
            best = bests[i]
    print 'best so far for {}: {}'.format(filename, best)

    slideshow = optimize_slideshow(slideshow, images)
    # print slideshow
    score = score_slideshow(slideshow, images)
    print 'score {}'.format(score)
    if score > best:
        # output file
        f = open(filename + ".out", "w")
        f.write(str(len(slideshow)) + '\n')
        for slide in slideshow:
            f.write(str(slide) + '\n')

        best = score
        print 'new best: {}'.format(best)
    return score


total_score = 0
total_score = total_score + create_output('a_example')
# total_score = total_score + create_output('b_lovely_landscapes')
# total_score = total_score + create_output('c_memorable_moments')
total_score = total_score + create_output('d_pet_pictures')
# total_score = total_score + create_output('e_shiny_selfies')
print 'total_score: {}'.format(total_score)
