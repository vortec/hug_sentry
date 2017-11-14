import hug


@hug.get('/fail')
def fail(request, amount: hug.types.number):
    amount / 0


@hug.get('/routing_fail/{amount}')
def routing_fail(request, amount: hug.types.number):
    raise Exception("Oh no!")
