import pandas as pd
import os.path
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from numpy import array
from keras.models import load_model
import matplotlib.pyplot as plt

from keras.layers import Dense
from keras.layers import LSTM
from numpy import array
from keras.models import load_model
import math
from sklearn.metrics import mean_squared_error


	
def error_plotting(true,predicted):
	f, ax = plt.subplots(3,sharex=True)
	
	for i in range (2,5):
		ax[i-2].plot(true[i,:])
		ax[i-2].plot(predicted[i,:])
	ax[1].set_ylabel('Number of events')
	ax[2].set_xlabel('Time step')
	plt.show()
	
def data_lotting(data):
	f, ax = plt.subplots(10,sharex=True)
	for i in range (10):
		ax[i].plot(data[i,:])
	plt.show()	
	
def simple_lstm(train,test):
	
	
	y = train[1:,:]
	X=train[:-1,:]	
	
	testy = test[1:,:]
	testX=test[:-1,:]
	
	from sklearn import preprocessing
	from sklearn.preprocessing import StandardScaler
	scalerX = StandardScaler().fit(X)
	scalery= StandardScaler().fit(y)
	X = scalerX.transform(X)
	y= scalery.transform(y)
	scalertestX = StandardScaler().fit(testX)
	scalertesty= StandardScaler().fit(testy)
	testX = scalertestX.transform(testX)
	testy = scalertesty.transform(testy)
		
	X = X.reshape(  X.shape[0],1, X.shape[1])
	y = y.reshape(  y.shape[0],1, y.shape[1])
		
	testX = testX.reshape(  testX.shape[0],100, testX.shape[1])
	testy = testy.reshape(  testy.shape[0],100, testy.shape[1])
	
	seq = [[0.0, 0.1], [0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5]]
	seq = array(seq)
	#x = np.arange(0, 4, 0.1)
	#X, y = x, np.sin(3*x)#seq[:, 0], np.sin(5*seq[:, 0])
	#print(y)
	#X = X.reshape((len(X), 1, 1))
	
	from keras import optimizers	
	# define model
	model = Sequential()
	model.add(LSTM(X.shape[2],return_sequences=True, input_shape=(1,X.shape[2])))
	model.add(Dense(X.shape[2], activation='softmax'))
	sgd = optimizers.SGD(lr=0.001, decay=1e-3, momentum=0.9, nesterov=True)
	# compile model
	model.compile(loss='mean_squared_error', optimizer='adam')	
	model.fit(X, y, epochs=1*5*2000, shuffle=False, verbose=1)
	'''
	yhat = model.predict(X, verbose=0)
	yhat_ = scalery.inverse_transform(yhat)
	print(yhat)
	#plt.plot(yhat)
	#plt.show()
	'''
	# make predictions
	trainPredict = model.predict(X)
	testPredict = model.predict(testX)
	# invert predictions
	trainPredict = scalerX.inverse_transform(trainPredict)
	trainY = scalery.inverse_transform(y)
	testPredict = scalertestX.inverse_transform(testPredict)
	testY = scalertesty.inverse_transform(testy)
	# calculate root mean squared error
	print('$$$$$$$$$$$$$trainY shape:', trainY.shape)
	print('$$$$$$$$$$$$$trainPredict shape:', trainPredict.shape)
	trainY= trainY.reshape(  trainY.shape[0], trainY.shape[2])
	trainPredict = trainPredict.reshape(  trainPredict.shape[0], trainPredict.shape[2])
	trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
	print('Train Score: %.2f RMSE' % (trainScore))
	testY= testY.reshape(  testY.shape[0], testY.shape[2])
	testPredict = testPredict.reshape(testPredict.shape[0], testPredict.shape[2])
	testScore = math.sqrt(mean_squared_error(testY, testPredict))
	print('Test Score: %.2f RMSE' % (testScore))
	np.savetxt('test.csv',testY)
	np.savetxt('testPredict.csv',testPredict)
	error_plotting(testY, testPredict)
	
	

def vector_moving_average(a, n=3) :
	#print('a: ',a)
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def moving_average(A):
	n = 3
	B = np.zeros((A.shape[0],A.shape[1]-n+1))
	for i in range(A.shape[0]):
		B[i,:] = vector_moving_average(A[i,:])
	print(B)
	
	

####### Data preparing


np.random.seed(7)
Dir = '/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/10days166-100repos-watch/'
Fls = os.listdir(Dir)
Data = []
for _,f in enumerate(Fls):
	data = pd.read_csv(Dir + f)
	Data.append(data.ix[:,1].tolist())
Data = np.array(Data).T
Data = Data[0,:]
#Data = Data[~(Data==0).all(1)]
train_size = int(len(Data) * 0.80)
test_size = len(Data) - train_size
train, test = Data[0:train_size,:], Data[train_size:len(Data),:]	
simple_lstm(train,test)
#moving_average(Data)
#data_plotting(Data)





def outdated():
	'''
	#print('total time:', (time.time() - t1)/60)
	
	df = pd.read_csv('/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/10days100repo-fork/2015-02-1.csv')
	df=df.loc[df['2015-02-1']>0]
	#dfList = df[]
	files =[]
	for i in range(0,9):
		for j in range(0,4):
				files.append('10days100repo-fork/2015-0%d-%d.csv' %(i,j))
	#print(files)
	for i in files:
		if os.path.isfile(i):
			print('%s is' %i)
			df2=pd.read_csv(i)
			df = pd.merge(df,df,on='name_h')
	
	df.to_csv('merged_files.csv',index=False)
	print(Data.shape)
	f, ax = plt.subplots(10,sharex=True)
	for i in range(10):
		ax[i].plot(Data[:,i])
	plt.show()
	
		# return training data
	def get_train():
			seq = [[0.0, 0.1], [0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5]]
			seq = array(seq)
			X, y = seq[:, 0], seq[:, 1]
			X = X.reshape((len(X), 1, 1))
			return X, y
	 
	# define model
	model = Sequential()
	model.add(LSTM(200, input_shape=(1,1)))
	model.add(Dense(1, activation='linear'))
	# compile model
	model.compile(loss='mse', optimizer='adam')
	# fit model
	X,y = get_train()
	model.fit(X, y, epochs=300, shuffle=False, verbose=0)
	# save model to single file
	model.save('lstm_model.h5')
	 
	# snip...
	# later, perhaps run from another script
	 
	# load model from single file
	model = load_model('lstm_model.h5')
	# make predictions
	yhat = model.predict(X, verbose=0)
	print(yhat)
	plt.plot(y)
	plt.plot(yhat)
	plt.show()
	'''
	#t1 = time.time()
















