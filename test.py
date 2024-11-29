async def run_scrapy_spider(param_string):
    project_directory = 'sp_EFRSB_parse'
    command = ['scrapy', 'crawl', 'bargaining_new', '-a', f'my_param={param_string}']

    # Создаем асинхронный процесс
    process = await asyncio.create_subprocess_exec(
        *command, 
        cwd=project_directory, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    async for line in process.stdout:
        print(f"STDOUT: {line.decode().strip()}")
    if process.returncode == 0:
        try:
            output = json.loads(stdout.decode('utf-8'))
            return output
        except json.JSONDecodeError:
            return False
    else:
        print(f"Error: {stderr.decode('utf-8')}")
        return False

https://fedresurs.ru/biddings?searchString=%D0%97%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%B5%D1%80%D1%81&tradeType=all&price=null&tradePeriod=null&bankrupt=null&onlyAvailableToParticipate=false&regionNumber=all&limit=15