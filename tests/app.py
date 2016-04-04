import hug


@hug.get('/fail')
def fail(request, amount: hug.types.number):
    amount / 0
