import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time}")
        return result
    return wrapper

@timer
def my_function(x, y):
    return x + y

result = my_function(2, 3)
print(result)