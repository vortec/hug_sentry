class SentryExceptionHandler:
    exclude = type(None)

    def __init__(self, client):
        self.client = client

    def __call__(self, request, response, exception):
        data = {
            'request': {
                'url': request.url,
                'method': request.method,
                'query_string': request.query_string,
                'headers': list(request.headers.items()),
                'cookies': list(request.cookies.items()),
                'env': self.clean_environment(request.env)
            },
            'user': {
                # 'id': 'testuser',
                # 'username': 'fkochem',
                'ip_address': self.guess_user_ip_from_request(request)
                # 'email': 'test2@gmail.org'
            }
        }

        self.client.captureException(data=data)

        raise exception

    def clean_environment(self, env):
        """
        Only keep 'REMOTE_ADDR' and environment attributes which begin
        with 'SERVER_'.
        """
        cleaned_env = {}

        for key, value in env.items():
            if key.startswith('SERVER_') or key == 'REMOTE_ADDR':
                cleaned_env[key] = value

        return cleaned_env

    def guess_user_ip_from_request(self, request):
        """
        Return 'X-FORWARDED-FOR' from the request headers if set,
        otherwise return 'REMOTE_ADDR' from the environment. If both are
        not set, return '127.0.0.1'.
        """
        forwarded_for = request.headers.get('X-FORWARDED-FOR', None)
        if forwarded_for:
            return forwarded_for

        remote_addr = request.env.get('REMOTE_ADDR', None)
        if remote_addr:
            return remote_addr

        return '127.0.0.1'
