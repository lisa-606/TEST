from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.BasicSchemaStimulationFramesFactory import BasicSchemaStimulationFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.SchemaStimulationFrames import SchemaStimulationFrames
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimTargetRect import StimTargetRect
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Resource.fig2data import fig2data
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from psychopy import visual, core, event


class SchemaStimulationFramesFactory(BasicSchemaStimulationFramesFactory):

    def initial(self, stimulation_ui_parameters):
        BasicSchemaStimulationFramesFactory.initial(self, stimulation_ui_parameters)

    def get_frames(self, target_table):
        frames = SchemaStimulationFrames()
        stimulation_frequency_set = target_table['FREQUENCY']
        stimulation_phase_set = target_table['PHASE']
        stim_rect_max_color = self.stimulation_ui_parameters.white
        char_set = target_table['DISPLAYCHAR']
        #base_framework = mpimg.imread(self.stimulation_ui_parameters.base_framework_file)

        stim_target_rect_set = []

        i = 0
        target_site_point = [400, 190]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 1
        target_site_point = [400, 730]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 2
        target_site_point = [160, 460]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 3
        target_site_point = [640, 460]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 4
        target_site_point = [1360, 190]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 5
        target_site_point = [1360, 730]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 6
        target_site_point = [1120, 460]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 7
        target_site_point = [1600, 460]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 8
        target_site_point = [880, 190]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        i = 9
        target_site_point = [880, 730]
        current_stim_rect_size = [160, 160]
        stim_target_rect_set.append(StimTargetRect(target_site_point, current_stim_rect_size,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[i], stimulation_phase_set[i],
                                                   stim_rect_max_color))

        #target_char_set = target_table['DISPLAYCHAR']

        f0 = plt.figure(figsize=(19.20, 10.80), facecolor='k', dpi=100,)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        current_axis = plt.gca()
        for j in range(0, 10):
            brightness = 1
            rect = patches.Rectangle(
                (stim_target_rect_set[j].site_point[0] / 1920, stim_target_rect_set[j].site_point[1] / 1080),
                stim_target_rect_set[j].rect_size[0] / 1920, stim_target_rect_set[j].rect_size[1] / 1080,
                linewidth=1, facecolor= [brightness, brightness, brightness])
            v = plt.text(
                stim_target_rect_set[j].site_point[0] / 1920 + (stim_target_rect_set[j].rect_size[0] / 1920) / 2,
                stim_target_rect_set[j].site_point[1] / 1080 + (stim_target_rect_set[j].rect_size[1] / 1080) / 2,
                char_set[j],
                fontsize=30, horizontalalignment='center', verticalalignment='center')
            current_axis.add_patch(rect)
        plt.axis('off')
        initial_frame = fig2data(f0)
        plt.close(f0)

        frame_set = []

        for N in range(0,self.stimulation_ui_parameters.max_preload_frames):
            f = plt.figure(figsize=(19.20, 10.80), facecolor='k', dpi=100)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)

            plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
            current_axis = plt.gca()
            for j in range(0, 10):
                brightness = stim_target_rect_set[j].cal_brightness(N)
                rect = patches.Rectangle((stim_target_rect_set[j].site_point[0] / 1920, stim_target_rect_set[j].site_point[1] / 1080),
                                        stim_target_rect_set[j].rect_size[0] / 1920, stim_target_rect_set[j].rect_size[1] / 1080,
                                        linewidth=1, facecolor= [brightness, brightness, brightness])
                v = plt.text(stim_target_rect_set[j].site_point[0] / 1920 + (stim_target_rect_set[j].rect_size[0] / 1920) / 2,
                            stim_target_rect_set[j].site_point[1] / 1080 + (stim_target_rect_set[j].rect_size[1] / 1080) / 2, char_set[j],
                            fontsize=30, horizontalalignment='center', verticalalignment='center')
                current_axis.add_patch(rect)
            plt.axis('off')
            frame_set.append(fig2data(f))
            plt.close(f)

        frames.initial_frame = initial_frame
        frames.frame_set = frame_set
        frames.stim_target_rect_set = stim_target_rect_set
        return frames


if __name__ == '__main__':
    '''
    display_char = ['下降','上升','左转','右转','后退','前进','左飞','右飞','降落','起飞']
    frequency = np.linspace(8.0, 15.2, 10)
    phase = [0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi, 0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi, 0*math.pi, 0.5*math.pi]
    target_table = {'DISPLAYCHAR': display_char,
                    'FREQUENCY': frequency,
                    'PHASE': phase}
    t = SchemaStimulationFramesFactory()
    t.initial(StimulationUIParameters)
    frames = t.get_frames(target_table)
    images = []
    for frame in range(0, 120):
        plt.imsave('temp.png', frames.frame_set[frame])
        images.append(plt.imread('temp.png'))
        #print(type(images[0]))
    images = np.array(images)
    print(images.shape)
    np.save('images.npy',images)
    '''
    #images = np.load('images.npy')
    #images = images.tolist()
    mywin = visual.Window([1920, 1080], monitor="testMonitor", units="pix", fullscr=True, waitBlanking=True,
                          color=(0, 0, 0), colorSpace='rgb255')

    image_sti = []

    for j in range(0, 300):
        image_sti.append(visual.ImageStim(mywin, image='D:/postgraduate/Stimulation_Operation/StimulationSystem/stimulationInformationFolder/UAVControl/0/'+str(j)+'.png', pos=[0, 0], size=[1920, 1080], units='pix', flipVert=False))
    #np.array(images.pop(index=0))
    #print(np.max(frames.frame_set[0]))
    i = 0
    #images = []

    while True:
        #image = visual.ImageStim(mywin, image=images[i], pos=[0, 0], size=[1600, 900], units='pix', flipVert=True)
        image_sti[i].draw()
        print(mywin.flip())
        i += 1
        if i == 300:
            i = 0
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()
