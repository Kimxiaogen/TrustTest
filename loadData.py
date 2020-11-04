def load(path):
    total = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            arr = line.split(',')
            total.append(arr)
    return total
