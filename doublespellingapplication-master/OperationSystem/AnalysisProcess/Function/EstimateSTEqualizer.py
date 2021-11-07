import numpy as np
import scipy
from doubleSpellingApplication.CommonSystem.AssistFunction.arfit.arfit import arfit
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.horizontal_expanse_to_tense import horizontal_expanse_to_tense
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.tense_horizontal_expanse import tense_horizontal_expanse


def EstimateSTEqualizer(data, P):

   if P == None:
      P = [4, 6]
   elif(len(P)<2):
      P[1]=P[0]

   #去均值
   data = data - np.reshape(np.mean(data,1), [data.shape[0],1])

   STEqualizerTemp, STEDataD, V, armodel, C = equalizer_estimate(data,P)

   equalizerOrder = STEqualizerTemp.shape[2]
   STEDataD = np.mat(STEDataD,dtype=complex)
   STEqualizer = horizontal_expanse_to_tense(np.mat(np.diag((1/np.sqrt(np.array(STEDataD))).reshape(STEDataD.shape[0]))) * tense_horizontal_expanse(STEqualizerTemp), equalizerOrder)
   Pi = np.ceil((STEqualizer.shape[2])/2)
   return STEqualizer, Pi


def equalizer_estimate(x, P):

   L = x.shape[0]

   w, A, C, sbc, fpe, th = arfit(x.T, P[0],P[1],'fpe','zero')

   armodel = np.hstack((np.identity(L), -A))
   [D,V] = np.linalg.eigh(C)

   V = -V
   V[:,3] = -V[:,3]
   D=np.mat(D.reshape(len(D),1))
   equalizerTense = V.H * armodel

   temp = horizontal_expanse_to_tense(equalizerTense, equalizerTense.shape[1]/L)
   # equalizer = np.zeros((temp.shape[0], temp.shape[1], 1))
   # for i in range(0, temp.shape[0]):
   #    for j in range(0, temp.shape[1]):
   #       equalizer =

   equalizer = temp

   return equalizer, D, V, armodel, C
