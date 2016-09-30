from multiprocessing import Manager, Pool,cpu_count

manager = Manager()
dicct = manager.dict({1:{1:16,2:16,3:16},2:{1:16,2:16,3:16},3:{1:16,2:16,3:16},4:{1:16,2:16,3:16}})

def compress(Trie):
    del Trie[1]
    return Trie

def process(key,dicct):
    dicct[key] = compress(dicct[key])

print dicct

pool = Pool(cpu_count())

# [pool.apply_async(process, (key,dicct)) for key in dicct.keys()]

[process(key,dicct) for key in dicct.keys()] # Seq way

pool.close()
pool.join()

print dicct
