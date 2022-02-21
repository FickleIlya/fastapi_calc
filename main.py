from fastapi import FastAPI, Query
from typing import Optional
from starlette.responses import Response
from solution import solution
import re

app = FastAPI()

# create our list of expressions
res = []


@app.get('/calc')
async def calc(expression: str):

    pattern = r'[+-]?(\d*\.\d*|\d+)([+\-*/](\d*\.\d*|\d+))*$'

    if re.match(pattern, expression):
        status = 'success'

        num = solution(expression)

        # if num is float and equal {some number}.0
        # {some number}.0 -> {some number}
        if re.search(r'\.0$', str(num)):
            num = int(num)

        answer = {expression: str(round(num, 3))}
        res.append({'request': expression,
                    'response': str(round(num, 3)),
                    'status': status})

    else:
        status = 'fail'
        answer = {expression: ''}
        res.append({'request': expression,
                    'response': '',
                    'status': status})

    if len(res) > 30:
        del res[0]

    return answer


@app.get('/history')
async def history(status: Optional[str] = None, limit: int = Query(30, ge=1, le=30)):

    if limit in range(1, 31):

        if not status:
            lst = list(reversed(res))
            return lst[:limit]

        elif status in ['fail', 'success']:

            lst = list(reversed([expression for expression in res if expression['status'] == status]))

            return lst[:limit]

        # returns error if status wrong
        else:
            return Response("Internal server error", status_code=500)

