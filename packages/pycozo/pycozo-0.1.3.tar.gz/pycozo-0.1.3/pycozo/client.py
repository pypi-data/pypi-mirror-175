class Client:
    def __init__(self, *, path=None, host=None, auth=None, dataframe=True):
        self.pandas = None
        if path is not None:
            from cozo_embedded import CozoDbPy
            self.embedded = CozoDbPy(path)
        elif host is not None:
            self.host = host
            self.auth = auth or ''
        else:
            raise Exception('you must specify either `path` for embedded mode, or `host` for client/server mode')

        if dataframe:
            try:
                import pandas
                self.pandas = pandas
            except ImportError as _:
                print('`pandas` feature was requested, but pandas is not installed')
                pass

    def url(self):
        return f'{self.host}/text-query'

    def headers(self):
        return {
            'x-cozo-auth': self.auth
        }

    def client_request(self, script, params=None):
        import requests

        r = requests.post(self.url(), headers=self.headers(), json={
            'script': script,
            'params': params or {}
        })
        if r.ok:
            res = r.json()
            return self.format_return(res)
        else:
            raise QueryException(r.text)

    def format_return(self, res):
        if self.pandas:
            return self.pandas.DataFrame(columns=res['headers'], data=res['rows']).style.applymap(
                colour_code_type)
        else:
            return res

    def embedded_request(self, script, params=None):
        import json
        import time
        import math

        params_str = json.dumps(params or {}, ensure_ascii=False)
        try:
            start_time = time.time()
            res = self.embedded.run_query(script, params_str)
            taken = math.floor((time.time() - start_time) * 1000)
            res = json.loads(res)
            res['time_taken'] = taken
            return self.format_return(res)
        except Exception as e:
            e_str = str(e)
            raise QueryException(e_str) from None

    def run(self, script, params=None):
        if self.embedded is None:
            return self.client_request(script, params)
        else:
            return self.embedded_request(script, params)


def colour_code_type(val):
    if isinstance(val, int) or isinstance(val, float):
        colour = '#307fc1'
    elif isinstance(val, str):
        colour = 'black'
    else:
        colour = '#bf5b3d'
    return f'color: {colour}'


class QueryException(Exception):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    def _repr_pretty_(self, p, cycle):
        p.text(self.text)
