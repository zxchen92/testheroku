import numpy as np
import pandas as pd
import tensorflow as tf
import sklearn
from sklearn.preprocessing import MinMaxScaler


# Your code here

def get_recommendations(user_id):
    

    #cell[2]
    rating = pd.read_csv('FoodRatings2.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
    user = pd.read_csv('UserID.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
    food = pd.read_csv('Food.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
    food_rating = pd.merge(rating, food, on='foodid')
    cols = ['UserID', 'FoodID', 'Rating', 'Food']

    rating_count = (food_rating.
        groupby(by = ['food'])['rating'].
        count().
        reset_index().
        rename(columns = {'rating': 'RatingCount_Food'})
        [['food', 'RatingCount_Food']])
    

    threshold = 10
    rating_count = rating_count.query('RatingCount_Food >= @threshold')

    user_rating = pd.merge(rating_count, food_rating, left_on='food', right_on='food', how='left')
    
    user_count = (user_rating.
     groupby(by = ['userid'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'RatingCount_user'})
     [['userid', 'RatingCount_user']]
    )

    threshold = 9
    user_count = user_count.query('RatingCount_user >= @threshold')
    user_count

    combined = user_rating.merge(user_count, left_on = 'userid', right_on = 'userid', how = 'inner')
    
    scaler = MinMaxScaler()
    combined['rating'] = combined['rating'].values.astype(float)
    rating_scaled = pd.DataFrame(scaler.fit_transform(combined['rating'].values.reshape(-1,1)))
    combined['rating'] = rating_scaled
    combined['rating']

    combined = combined.drop_duplicates(['userid', 'food'])
    user_food_matrix = combined.pivot(index='userid', columns='food', values='rating')
    user_food_matrix.fillna(0, inplace=True)

    users = user_food_matrix.index.tolist()
    books = user_food_matrix.columns.tolist()

    user_food_matrix = user_food_matrix.values

    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

    num_input = combined['food'].nunique()
    num_hidden_1 = 10
    num_hidden_2 = 5

    X = tf.placeholder(tf.float64, [None, num_input])

    weights = {
        'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)),
        'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)),
        'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)),
        'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)),
        }

    biases = {
        'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
        'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        'decoder_b2': tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
        }
    
    def encoder(x):
        layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
        layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
        return layer_2

    def decoder(x):
        layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
        layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
        return layer_2
    
    encoder_op = encoder(X)
    decoder_op = decoder(encoder_op)

    y_pred = decoder_op

    y_true = X

    loss = tf.losses.mean_squared_error(y_true, y_pred)
    optimizer = tf.train.RMSPropOptimizer(0.03).minimize(loss)
    eval_x = tf.placeholder(tf.int32, )
    eval_y = tf.placeholder(tf.int32, )
    pre, pre_op = tf.metrics.precision(labels=eval_x, predictions=eval_y)

    init = tf.global_variables_initializer()
    local_init = tf.local_variables_initializer()
    pred_data = pd.DataFrame()

    with tf.Session() as session:
        epochs = 100
        batch_size = 35
        

        session.run(init)
        session.run(local_init)

        num_batches = int(user_food_matrix.shape[0] / batch_size)
        user_food_matrix = np.array_split(user_food_matrix, num_batches)
        
        for i in range(epochs):

            avg_cost = 0
            for batch in user_food_matrix:
                _, l = session.run([optimizer, loss], feed_dict={X: batch})
                avg_cost += l

            avg_cost /= num_batches

            print("epoch: {} Loss: {}".format(i + 1, avg_cost))
        
        user_food_matrix = np.concatenate(user_food_matrix, axis=0)

        preds = session.run(decoder_op, feed_dict={X: user_food_matrix})

        pred_data = pd.concat([pred_data, pd.DataFrame(preds)]) #pred_data.append(pd.DataFrame(preds))

        pred_data = pred_data.stack().reset_index(name='rating')
        pred_data.columns = ['userid', 'food', 'rating']
        pred_data['userid'] = pred_data['userid'].map(lambda value: users[value])
        pred_data['food'] = pred_data['food'].map(lambda value: books[value])

    keys = ['userid', 'food']
    index_1 = pred_data.set_index(keys).index
    index_2 = combined.set_index(keys).index

    top_ten_ranked = pred_data[~index_1.isin(index_2)]
    top_ten_ranked = top_ten_ranked.sort_values(['userid', 'rating'], ascending=[True, False])
    top_ten_ranked = top_ten_ranked.groupby('userid').head(10)

    recommendations = top_ten_ranked.loc[top_ten_ranked['userid'] == user_id]
    recommendations_food = recommendations['food'].values.tolist()

    print('ken: user id is' + str(user_id) +'end' +  str(recommendations_food), flush=True )



    
    # Return recommendations
    # ...
    return recommendations_food