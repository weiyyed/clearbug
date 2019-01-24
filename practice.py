from functools import wraps
from decorator import decorator
# def hint(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print('{} is running'.format(func.__name__))
#         return func(*args, **kwargs)
#     return wrapper
@decorator
def hint(func, *args, **kwargs):
   print('{} is running'.format(func.__name__))
   return func(*args, **kwargs)

@hint
def hello():
    print("Hello!")
import time
from functools import wraps


# 装饰器增加缓存功能
def cache(instance):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
           # 构建key: key => func_name::args::kwargs
            joint_args = ','.join((str(x) for x in args))
            joint_kwargs = ','.join('{}={}'.format(k, v) for k, v in sorted(kwargs.items()))
            key = '{}::{}::{}'.format(func.__name__,joint_args, joint_kwargs)
           # 根据key获取结果。如果key已存在直接返回结果，不用重复计算。
            result = instance.get(key)
            if result is not None:
                return result
           # 如果结果不存在，重新计算，缓存。
            result = func(*args, **kwargs)
            instance.set(key, result)
            return result
        return inner_wrapper
    return wrapper


# 创建字典构造函数，用户缓存K/V键值对
class DictCache:
   def __init__(self):
       self.cache = dict()

   def get(self, key):
       return self.cache.get(key)

   def set(self, key, value):
       self.cache[key] = value

   def __str__(self):
       return str(self.cache)

   def __repr__(self):
       return repr(self.cache)


# 创建缓存对象
cache_instance = DictCache()

# Python语法糖调用装饰器
@cache(cache_instance)
def long_time_func(x):
   time.sleep(x)
   print(x)
   return x

# 调用装饰过函数

if __name__ == '__main__':
    # print(hello.__name__)
    # print(type(",".join(['1','2'])))
    long_time_func(3)