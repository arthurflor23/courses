import tensorflow as tf


class xLSTM(tf.keras.layers.Layer):
    """
    """

    def __init__(self,
                 units,
                 num_heads=4,
                 blockchain=['slstm'],
                 dropout=0.0,
                 **kwargs):
        """
        """

        super().__init__(**kwargs)

        if units % num_heads != 0:
            raise ValueError("units must be divisible by num_heads")

        self.units = units
        self.num_heads = num_heads
        self.head_size = units // num_heads
        self.blockchain = blockchain
        self.num_blocks = len(blockchain)
        self.dropout = dropout

    def get_config(self):
        """
        """

        config = super().get_config()

        config.update({
            'units': self.units,
            'num_heads': self.num_heads,
            'head_size': self.head_size,
            'blockchain': self.blockchain,
            'num_blocks': self.num_blocks,
            'dropout': self.dropout,
        })

        return config

    def build(self, input_shape):
        """
        """

        super().build(input_shape)

        self.input_shape = input_shape
        self.sequential_reshape = len(input_shape) > 3

        self.features = input_shape[-1]
        self.blocks = []

        for i in range(self.num_blocks):
            if self.blockchain[i] == 'slstm':
                self.blocks.append({
                    'up_left': tf.keras.layers.Dense(units=int(self.features * 4/3)),
                    'up_right': tf.keras.layers.Dense(units=int(self.features * 4/3)),
                    'down': tf.keras.layers.Dense(units=self.features),
                    'causal': tf.keras.layers.Conv1D(filters=1, kernel_size=4, padding='causal'),
                    'wz': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wi': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wf': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wo': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'rz': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'ri': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'rf': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'ro': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'ln': tf.keras.layers.LayerNormalization(),
                    'gn': tf.keras.layers.GroupNormalization(groups=self.num_heads),
                    'dp': tf.keras.layers.Dropout(rate=self.dropout),
                })

            else:
                self.blocks.append({
                    'up_left': tf.keras.layers.Dense(units=int(self.features * 2)),
                    'up_right': tf.keras.layers.Dense(units=self.units),
                    'down': tf.keras.layers.Dense(units=self.features),
                    'causal': tf.keras.layers.Conv1D(filters=1, kernel_size=4, padding='causal'),
                    'skip': tf.keras.layers.Dense(units=self.units),
                    'wq': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wk': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wv': [tf.keras.layers.Dense(units=self.head_size) for _ in range(self.num_heads)],
                    'wi': tf.keras.layers.Dense(units=self.units),
                    'wf': tf.keras.layers.Dense(units=self.units),
                    'wo': tf.keras.layers.Dense(units=self.units),
                    'ln': tf.keras.layers.LayerNormalization(),
                    'gn': tf.keras.layers.GroupNormalization(groups=self.num_heads),
                    'dp': tf.keras.layers.Dropout(rate=self.dropout),
                })

    @tf.function
    def call(self, inputs, training=False):
        """
        """

        if self.sequential_reshape:
            tf_shape = tf.unstack(tf.shape(inputs))
            inputs = tf.reshape(inputs, shape=[tf_shape[0], -1, tf_shape[-1]])

        shape = tf.unstack(tf.shape(inputs))
        batch_size, sequence_length = shape[0], shape[1]

        h = [tf.zeros((batch_size, self.units)) for _ in range(self.num_blocks)]
        c = [tf.zeros((batch_size, self.units)) for _ in range(self.num_blocks)]
        n = [tf.zeros((batch_size, self.units)) for _ in range(self.num_blocks)]
        m = [tf.zeros((batch_size, self.units)) for _ in range(self.num_blocks)]

        ta = tf.TensorArray(dtype=tf.float32, size=sequence_length)

        for t in tf.range(sequence_length):
            xt = inputs[:, t, :]

            for i in range(self.num_blocks):
                if self.blockchain[i] == 'slstm':
                    x_norm = self.blocks[i]['ln'](xt, training=training)

                    x_conv = self.blocks[i]['causal'](tf.expand_dims(x_norm, axis=-1))
                    x_conv = tf.nn.silu(tf.squeeze(x_conv, axis=-1))

                    wz = tf.split(xt, self.num_heads, axis=-1)
                    wz = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wz'], wz)], axis=-1)

                    rz = tf.split(h[i], self.num_heads, axis=-1)
                    rz = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['rz'], rz)], axis=-1)

                    z = tf.tanh(wz + rz)

                    wo = tf.split(xt, self.num_heads, axis=-1)
                    wo = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wo'], wo)], axis=-1)

                    ro = tf.split(h[i], self.num_heads, axis=-1)
                    ro = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['ro'], ro)], axis=-1)

                    o = tf.sigmoid(wo + ro)

                    wi = tf.split(x_conv, self.num_heads, axis=-1)
                    wi = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wi'], wi)], axis=-1)

                    ri = tf.split(h[i], self.num_heads, axis=-1)
                    ri = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['ri'], ri)], axis=-1)

                    i_tilde = wi + ri

                    wf = tf.split(x_conv, self.num_heads, axis=-1)
                    wf = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wf'], wf)], axis=-1)

                    rf = tf.split(h[i], self.num_heads, axis=-1)
                    rf = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['rf'], rf)], axis=-1)

                    f_tilde = wf + rf

                    m_t = tf.maximum(f_tilde + m[i], i_tilde)
                    j = tf.exp(i_tilde - m_t)
                    f = tf.exp(f_tilde + m[i] - m_t)

                    c_t = f * c[i] + j * z
                    n_t = f * n[i] + j
                    h_t = o * c_t / n_t

                    ru = self.blocks[i]['gn'](h_t, training=training)

                    ru_left = self.blocks[i]['up_left'](ru)
                    ru_right = self.blocks[i]['up_right'](ru)

                    ru = ru_left * tf.nn.gelu(ru_right)
                    ru = self.blocks[i]['down'](ru)

                    if training and self.dropout:
                        ru = self.blocks[i]['dp'](ru)

                    xt = xt + ru
                    h[i], c[i], n[i], m[i] = h_t, c_t, n_t, m_t

                else:
                    x_norm = self.blocks[i]['ln'](xt, training=training)

                    x_up_left = self.blocks[i]['up_left'](x_norm)
                    x_up_right = self.blocks[i]['up_right'](x_norm)

                    x_conv = self.blocks[i]['causal'](tf.expand_dims(x_up_left, axis=-1))
                    x_conv = tf.nn.silu(tf.squeeze(x_conv, axis=-1))

                    x_skip = self.blocks[i]['skip'](x_conv)

                    q = tf.split(x_conv, self.num_heads, axis=-1)
                    q = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wq'], q)], axis=-1)

                    k = tf.split(x_conv, self.num_heads, axis=-1)
                    k = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wk'], k)], axis=-1)
                    k = k / (self.head_size ** 0.5)

                    v = tf.split(x_up_left, self.num_heads, axis=-1)
                    v = tf.concat([f(chunk) for f, chunk in zip(self.blocks[i]['wv'], v)], axis=-1)

                    i_tilde = self.blocks[i]['wi'](x_conv)
                    f_tilde = self.blocks[i]['wf'](x_conv)
                    o = tf.nn.sigmoid(self.blocks[i]['wo'](x_up_left))

                    m_t = tf.math.maximum(f_tilde + m[i], i_tilde)
                    j = tf.exp(i_tilde - m_t)
                    f = tf.exp(f_tilde + m[i] - m_t)

                    c_t = f * c[i] + j * (v * k)
                    n_t = f * n[i] + j * k
                    h_t = o * (c_t * q) / tf.reduce_max(tf.abs(tf.matmul(tf.transpose(n_t), q)), axis=1)

                    ru = self.blocks[i]['gn'](h_t, training=training)

                    ru = (ru + x_skip) * tf.nn.silu(x_up_right)
                    ru = self.blocks[i]['down'](ru)

                    if training and self.dropout:
                        ru = self.blocks[i]['dp'](ru)

                    xt = xt + ru
                    h[i], c[i], n[i], m[i] = h_t, c_t, n_t, m_t

            ta = ta.write(t, xt)

        outputs = tf.transpose(ta.stack(), perm=[1, 0, 2])

        if self.sequential_reshape:
            outputs = tf.reshape(outputs, shape=tf_shape)

        outputs = tf.ensure_shape(outputs, shape=self.input_shape)

        return outputs
