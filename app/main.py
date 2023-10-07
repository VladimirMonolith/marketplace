from fastapi import FastAPI


app = FastAPI(title='marketplace')


# Optional[int] = None - делает поле необязательным, подставляя None. Если нужно сделать больше1, меньше 5, то Query
