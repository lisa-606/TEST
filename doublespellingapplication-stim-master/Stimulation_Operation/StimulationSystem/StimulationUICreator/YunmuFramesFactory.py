from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.BasicSchemaStimulationFramesFactory import BasicSchemaStimulationFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.SchemaStimulationFrames import SchemaStimulationFrames
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimTargetRect import StimTargetRect
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Resource.fig2data import fig2data
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
import numpy as np
import math
from psychopy import visual, core, event


class YunmuFramesFactory(BasicSchemaStimulationFramesFactory):

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
        j = 0

        for i in range(0, 4):
            y = 903
            x = 750 + 140*i
            target_site_point = [x, y]
            radius = 100
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

            y = 177
            x = 750 + 140*i
            target_site_point = [x, y]
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

        for i in range(0, 5):
            y = 782
            x = 680 + 140 * i
            target_site_point = [x, y]
            radius = 100
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

            y = 298
            x = 680 + 140 * i
            target_site_point = [x, y]
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

        for i in range(0, 6):
            y = 661
            x = 610 + 140 * i
            target_site_point = [x, y]
            radius = 100
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

            y = 419
            x = 610 + 140 * i
            target_site_point = [x, y]
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

        for i in range(0, 7):
            y = 540
            x = 540 + 140 * i
            target_site_point = [x, y]
            radius = 100
            stim_target_rect_set.append(StimTargetRect(target_site_point, radius,
                                                       self.stimulation_ui_parameters.monitor_refresh_rate,
                                                       stimulation_frequency_set[j], stimulation_phase_set[j],
                                                       stim_rect_max_color))
            j += 1

        stim_target_rect_set.append(StimTargetRect([680, 56], 100,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[j], stimulation_phase_set[j],
                                                   stim_rect_max_color))
        j += 1

        stim_target_rect_set.append(StimTargetRect([960, 56], 100,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[j], stimulation_phase_set[j],
                                                   stim_rect_max_color))
        j += 1

        stim_target_rect_set.append(StimTargetRect([1240, 56], 100,
                                                   self.stimulation_ui_parameters.monitor_refresh_rate,
                                                   stimulation_frequency_set[j], stimulation_phase_set[j],
                                                   stim_rect_max_color))


        #target_char_set = target_table['DISPLAYCHAR']

        path = 'C:\Windows\Fonts\simsun.ttc'
        font_prop = font_manager.FontProperties(fname=path)
        font_prop.set_size(25)

        f0 = plt.figure(figsize=(19.20, 10.80), facecolor='k', dpi=100,)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        current_axis = plt.gca()

        plt.text(340 / 1920,
                 270 / 1080,
                 '按→切换至告警模式\n按↓退出刺激端',
                 horizontalalignment='center', verticalalignment='center', color='lightgray', font_properties=font_prop)

        for j in range(0, 40):
            brightness = 0.5
            rect = patches.Ellipse(
                (stim_target_rect_set[j].site_point[0] / 1920, stim_target_rect_set[j].site_point[1] / 1080),
                width=stim_target_rect_set[j].rect_size/1920, height=stim_target_rect_set[j].rect_size/1080,
                linewidth=1, facecolor= [brightness, brightness, brightness])
            v = plt.text(
                stim_target_rect_set[j].site_point[0] / 1920,
                stim_target_rect_set[j].site_point[1] / 1080,
                char_set[j],
                fontsize=25, horizontalalignment='center', verticalalignment='center', color='lightgray')
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

            plt.text(340 / 1920,
                     270 / 1080,
                     '按→切换至告警模式\n按↓退出刺激端',
                     horizontalalignment='center', verticalalignment='center', color='lightgray',
                     font_properties=font_prop)

            for j in range(0, 40):
                brightness = stim_target_rect_set[j].cal_brightness(N)
                rect = patches.Ellipse(
                    (stim_target_rect_set[j].site_point[0]/1920, stim_target_rect_set[j].site_point[1]/1080),
                    width=stim_target_rect_set[j].rect_size/1920, height=stim_target_rect_set[j].rect_size/1080,
                    linewidth=1, facecolor=[brightness, brightness, brightness])
                current_axis.add_patch(rect)
                v = plt.text(stim_target_rect_set[j].site_point[0] / 1920,
                            stim_target_rect_set[j].site_point[1] / 1080, char_set[j],
                            fontsize=25, horizontalalignment='center', verticalalignment='center', color='lightgray')

            plt.axis('off')
            frame_set.append(fig2data(f))
            plt.close(f)

        frames.initial_frame = initial_frame
        frames.frame_set = frame_set
        frames.stim_target_rect_set = stim_target_rect_set
        return frames


if __name__ == '__main__':
    '''
    display_char = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                    'iu', 'ei', 'e', 'uan\ner', 'ue', 'un', 'u', 'i', 'uo\no', 'ie',
                    'a', 'ong\niong', 'ai', 'en', 'eng', 'ang', 'an', 'uai\ning', 'uang\niang',
                    'ou', 'ua\nia', 'ao', 'ui\nv', 'in', 'iao', 'ian', 'DEL',
                    ',', '.', 'Enter']
    frequency = np.linspace(8.0, 15.8, 40)
    phase = [0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
             0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi]
    target_table = {'DISPLAYCHAR': display_char,
                    'FREQUENCY': frequency,
                    'PHASE': phase}
    t = YunmuFramesFactory()
    t.initial(StimulationUIParameters)
    frames = t.get_frames(target_table)
    images = []
    for frame in range(0, 120):
        plt.imsave('D:/postgraduate/doublespelling/Stimulation_Operation/StimulationSystem/stimulationInformationFolder/DoubleSpelling/1/'+str(frame)+'.png', frames.frame_set[frame])
        images.append(plt.imread('D:/postgraduate/doublespelling/Stimulation_Operation/StimulationSystem/stimulationInformationFolder/DoubleSpelling/1/'+str(frame)+'.png'))
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

    for j in range(0, 120):
        image_sti.append(visual.ImageStim(mywin, image='D:/postgraduate/doublespelling/Stimulation_Operation/StimulationSystem/stimulationInformationFolder/DoubleSpelling/1/'+str(j)+'.png', pos=[0, 0], size=[1920, 1080], units='pix', flipVert=False))
    #np.array(images.pop(index=0))
    #print(np.max(frames.frame_set[0]))
    i = 0
    #images = []

    while True:
        #image = visual.ImageStim(mywin, image=images[i], pos=[0, 0], size=[1600, 900], units='pix', flipVert=True)
        image_sti[i].draw()
        print(mywin.flip())
        i += 1
        if i == 120:
            i = 0
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()

