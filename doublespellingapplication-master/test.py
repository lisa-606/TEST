from psychopy import visual, core, event  # import some libraries from PsychoPy
import matplotlib.pyplot as plt
import numpy as np
#create a window
mywin = visual.Window([1600,900], monitor="testMonitor", units="deg", fullscr=True, waitBlanking=False, color=(0, 0, 0), colorSpace='rgb255')
#image = plt.imread('test.png')
#print(np.max(image))
#f = plt.figure()
#plt.imshow(image)
#plt.axis('off')
#f.show()
#print(image.shape)
#create some stimuli
#grating1 = visual.GratingStim(win=mywin, size=3, pos=[-3,0], sf=3, color=(255, 255, 255), colorSpace='rgb255')
#message1 = visual.TextStim(mywin, pos=[-3,0],text='Test1', color=(0, 0, 0), colorSpace='rgb255',)
#grating2 = visual.GratingStim(win=mywin, size=3, pos=[3,0], sf=0, color=(255, 255, 255), colorSpace='rgb255')
#message2 = visual.TextStim(mywin, pos=[3,0],text='Test2', color=(0, 0, 0), colorSpace='rgb255',)
#fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=1)
#image = visual.ImageStim(mywin,image = image, pos = [0,0], size=[1600, 900], units = 'pix', flipVert=True)
#draw the stimuli and update the window
n = 0
while True:
    #grating1.setPhase(8/(1*60), '+')
    #grating1.draw()
    #message1.draw()
    #grating2.setPhase(10/(1*60), '+')
    #grating2.draw()
    #message2.draw()
    #image.draw()
    #stimList = [grating1, message1, grating2, message2]
    #screenshot = visual.BufferImageStim(mywin, stim=stimList)
    #screenshot.draw()
    tmp = 'E:/lqbz/postgraduate/Stimulation_Operation/StimulationSystem/stimulationInformationFolder/UAVControl/0/'+str(n)+'.png'
    n+=1
    image = visual.ImageStim(mywin,
                             image='E:/lqbz/postgraduate/Stimulation_Operation/StimulationSystem/StimulationUICreator/Resource/baseFrameworkFile.png',
                             pos=[0, 0], size=[1600, 900], units='pix', flipVert=False)

    # image.setImage(tmp)
    image.draw()
    mywin.flip()
    if len(event.getKeys())>0:
        break
    event.clearEvents()

#pause, so you get a chance to see it!
#core.wait(5.0)
mywin.close()
core.quit()