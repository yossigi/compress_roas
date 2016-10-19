def do_something(data):
    return data * 2

def consumer(inQ, outQ):
    while True:
        try:
            # get a new message
            val = inQ.get()

            # this is the 'TERM' signal
            if val is None:
                break;

            # unpack the message
            pos = val[0]  # its helpful to pass in/out the pos in the array
            data = val[1]

            # process the data
            ret = do_something(data)

            # send the response / results
            outQ.put( (pos, ret) )


        except Exception, e:
            print "error!", e
            break

def process_data(data_list, inQ, outQ):
    # send pos/data to workers
    for i,dat in enumerate(data_list):
        inQ.put( (i,dat) )

    # process results
    for i in range(len(data_list)):
        ret = outQ.get()
        pos = ret[0]
        dat = ret[1]
        data_list[pos] = dat
