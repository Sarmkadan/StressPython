s='123456789'
print(s[1:2])
print(s[-1:-2])
print(s[3])
print(s[:-3])

all_tasks = [1, 2, 3, 4, 5, 6, 7]
batch_size = 3


batches = [all_tasks[i:i + batch_size] for i in range(0, len(all_tasks), batch_size)]
print(batches)