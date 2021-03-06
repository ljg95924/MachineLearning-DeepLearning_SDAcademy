# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:12:53 2018

@author: SDEDU
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets('./mnist/data/',one_hot=True)

#신경망 모델 구성
x=tf.placeholder(tf.float32,[None, 28*28])
y=tf.placeholder(tf.float32,[None,10])

#dropout에 사용할 placeholder
#training시에는 일부만 사용
#test시에는 전체사용
keep_prob=tf.placeholder(tf.float32)


W1=tf.Variable(tf.random_normal([784,256], stddev=0.01))
L1=tf.nn.relu(tf.matmul(x,W1))
L1=tf.nn.dropout(L1,keep_prob)


W2=tf.Variable(tf.random_normal([256,256],stddev=0.01))
L2=tf.nn.relu(tf.matmul(L1,W2))
L2=tf.nn.dropout(L2,keep_prob)

W3=tf.Variable(tf.random_normal([256,10], stddev=0.01))
model=tf.matmul(L2,W3)

cost=tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=model,labels=y))
optimizer=tf.train.AdamOptimizer(0.001).minimize(cost)

init=tf.global_variables_initializer()
sess=tf.Session()
sess.run(init)

batch_size=100
total_batch=int(mnist.train.num_examples/batch_size)

for epoch in range(15):
    total_cost=0
    
    for i in range(total_batch):
        batch_xs,batch_ys=mnist.train.next_batch(batch_size)
        _,cost_val=sess.run([optimizer,cost],
                            feed_dict={x:batch_xs,y:batch_ys,
                                       keep_prob:1.0})
        total_cost +=cost_val
    print('Epoch: ', '%04d' %(epoch+1),
          'Avg. cost : ','{:.3f}'.format(total_cost/total_batch))
print('학습완료')

#테스트 데이터로 검증
is_correct=tf.equal(tf.argmax(model, 1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('accuracy:',sess.run(accuracy,
                           feed_dict={x:mnist.test.images,
                                      y:mnist.test.labels,
                                       keep_prob:1.0}))

