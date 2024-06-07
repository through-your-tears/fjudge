from aiohttp.web import json_response

from main import isSolvedPy


async def python_judge(request):
    data = await request.post()
    student_program = data['program']
    checker = data['checker']


    result = isSolvedPy()
