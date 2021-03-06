'''使用logistic regression 对鸢尾花进行分类
基于scikit-learn库
Version = V1.0.0
'''
from sklearn import datasets
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

#画出算法的决策区域
def plot_decision_region(X,y,classifier,test_idx=None,resolution=0.01):
	markers = ('s','x','o','^','v')
	colors = ('red','blue','lightgreen','gray','cyan')
	cmap = ListedColormap(colors[:len(np.unique(y))])
	
	x1_min,x1_max = X[:,0].min() - 1,X[:,0].max() + 1
	x2_min,x2_max = X[:,1].min() - 1,X[:,1].max() + 1

	xx1,xx2 = np.meshgrid(np.arange(x1_min,x1_max,resolution),
						np.arange(x2_min,x2_max,resolution))
	z = classifier.predict(np.array([xx1.ravel(),xx2.ravel()]).T)
	z = z.reshape(xx1.shape)
	plt.contourf(xx1,xx2,z,alpha=0.4,cmap=cmap)

	for idx,c1 in enumerate(np.unique(y)):
		plt.scatter(x=X[y == c1,0],y=X[y == c1,1],
			alpha=0.8,c=cmap(idx),
			marker=markers[idx],label=c1)

	if test_idx:
		X_test,y_test = X[test_idx,:],y[test_idx]
		plt.scatter(X_test[:,0],X_test[:,1],
			c='gray',alpha=1.0,
			linewidth=1,marker='o',
			s=15,label='test set')
	plt.xlabel('sepal length')
	plt.ylabel('petal length')
	plt.legend(loc='upper left')
	plt.show()


#主任务
if __name__ == '__main__':
	#1.获取鸢尾花数据
	iris = datasets.load_iris()
	X = iris.data[:,[2,3]]
	y = iris.target

	#2.数据预处理（拆分数据集，标准化数据）
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
	sc = StandardScaler()
	sc.fit(X_train)
	X_train_std = sc.transform(X_train)
	X_test_std = sc.transform(X_test)


	X_combined_std = np.vstack((X_train_std,X_test_std))
	y_combined = np.hstack((y_train,y_test))

	lr = LogisticRegression(C=1000.0,random_state=0)
	lr.fit(X_train_std,y_train)
	plot_decision_region(X_combined_std,y_combined,classifier=lr,test_idx=range(105,150))

