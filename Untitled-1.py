"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    password="ragops_dev",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

