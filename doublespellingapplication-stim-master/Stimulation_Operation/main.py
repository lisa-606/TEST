import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg


def fig2data(f):
    """
    fig = plt.figure()
    image = fig2data(fig)
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    import PIL.Image as Image
    # draw the renderer
    f.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = f.canvas.get_width_height()
    buf = np.frombuffer(f.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    image = Image.frombytes("RGBA", (w, h), buf.tobytes())
    image = np.asarray(image)
    return image

if __name__ == '__main__':

    target_site_point = []
    current_stim_rect_size = []
    charset = []

    target_site_point.append([400, 190])
    current_stim_rect_size.append([160, 160])
    charset.append('1')

    target_site_point.append([400, 730])
    current_stim_rect_size.append([160, 160])
    charset.append('2')

    target_site_point.append([160, 460])
    current_stim_rect_size.append([160, 160])
    charset.append('3')

    target_site_point.append([640, 460])
    current_stim_rect_size.append([160, 160])
    charset.append('4')

    target_site_point.append([1360, 190])
    current_stim_rect_size.append([160, 160])
    charset.append('5')

    target_site_point.append([1360, 730])
    current_stim_rect_size.append([160, 160])
    charset.append('6')

    target_site_point.append([1120, 460])
    current_stim_rect_size.append([160, 160])
    charset.append('7')

    target_site_point.append([1600, 460])
    current_stim_rect_size.append([160, 160])
    charset.append('8')

    target_site_point.append([880, 190])
    current_stim_rect_size.append([160, 160])
    charset.append('9')

    target_site_point.append([880, 730])
    current_stim_rect_size.append([160, 160])
    charset.append('10')

    f = plt.figure(figsize=(16,9), facecolor='k')#
    #v = plt.text(0, 0, 'hello', fontsize=30, horizontalalignment='center', verticalalignment='center')
    currentAxis = plt.gca()
    print(len(target_site_point))
    for j in range(0,10):
        rect = patches.Rectangle((target_site_point[j][0]/1920, target_site_point[j][1]/1080), current_stim_rect_size[j][0]/1920, current_stim_rect_size[j][1]/1080, linewidth=1, facecolor=[0.2,0.2,0.2])
        v = plt.text(target_site_point[j][0]/1920 + (current_stim_rect_size[j][0]/1920)/2, target_site_point[j][1]/1080 + (current_stim_rect_size[j][1]/1080)/2, charset[j], fontsize=30, horizontalalignment='center', verticalalignment='center')
        currentAxis.add_patch(rect)
    plt.axis('off')


    plt.savefig('test.png', facecolor='k')
    f.show()

    image = fig2data(f)
    print(image.shape)
    f2 = plt.figure()
    plt.imshow(image)
    #plt.axis('off')
    f2.show()
    '''
    t = mpimg.imread('test.png')
    print(t.shape)
    plt.imshow(t[:,:])
    plt.axis('off')
    plt.show()
    #plt.waitforbuttonpress(0)
    '''



