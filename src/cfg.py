from datetime import datetime

bot_data = {
    'prefix': "<",
    'token': "ODcxOTkyNjgzNDc5MDUyMzMw.GLUmo0.R8EHD4yTy4s8HGbU6skfnIg2ZgO-7yCrLU8uS0",
    'cogs': ["nitro"],
    'owner_id': 713476551978647623,
    'white_list_servers': [],
    'logs_channel': 1128775700481052752
}


async def write_log(log: str) -> None:
    now = datetime.now()

    try:
        file = open("logs.txt", "a+")
        file.write(f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}.{now.microsecond} {log}\n")
        file.close()
    except Exception as error:
        raise f"Произошла ошибка {error} при логировании"

    print(f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}.{now.microsecond} {log}")
