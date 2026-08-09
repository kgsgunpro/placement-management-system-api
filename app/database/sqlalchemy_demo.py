from sqlalchemy import create_engine , text

engine = create_engine(
    "postgresql+psycopg://postgres:2005@localhost:5432/postgres" , echo=True 
)
conn = engine.connect()
res = conn.execute(text('select*from students'))
print(res.mappings())

for x in res.mappings() :
    y=x['name']
    
    z=x['id']
print(x,y,z)