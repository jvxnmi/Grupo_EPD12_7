import sqlite3
import pandas as pd

# Ruta del archivo CSV
file_path = "EPD12_7_happyscore_income.csv"

# Cargamos el CSV en un DataFrame
df = pd.read_csv(file_path)

# Convertimos las columnas en numéricas porque están en formato string
def clean_numeric(column):
    return pd.to_numeric(df[column].astype(str).str.replace(".", "", regex=True), errors='coerce')

numeric_columns = ['avg_income', 'median_income', 'income_inequality', 'happyScore', 'GDP']
for col in numeric_columns:
    df[col] = clean_numeric(col)

# Conectamos a SQLite
conn = sqlite3.connect("BBDD.sqlite")
cursor = conn.cursor()

# Creamos la tabla "paises" pero también eliminamos la tabla que se haya podido crear previamente ya que se realizaron varias ejecuciones durante la resolución de este problema P3

cursor.execute("DROP TABLE IF EXISTS paises")

cursor.execute('''
    CREATE TABLE paises (
        country TEXT PRIMARY KEY,
        adjusted_satisfaction REAL,
        avg_satisfaction REAL,
        std_satisfaction REAL,
        avg_income REAL,
        median_income REAL,
        income_inequality REAL,
        region TEXT,
        happyScore REAL,
        GDP REAL
    )
''')
conn.commit()

# Insertar datos en la tabla "paises"
df.to_sql("paises", conn, if_exists="replace", index=False)

# Realizar una sentencia “SELECT” con una cláusula “WHERE” compleja que seleccione
# varias filas (entre 5 y 20) y muestre el resultado por pantalla. En este caso consultamos los países con happyScore ≥ 7 y que pertenezcan a "Western Europe"
cursor.execute("""
    SELECT * FROM paises
    WHERE happyScore >= 7 AND region = 'Western Europe'
    LIMIT 20;
""")
rows = cursor.fetchall()
print("Paises de Europa Occidental con happyScore >= 7:")
for row in rows:
    print(row)

# Realizar una sentencie “UPDATE” para actualizar el valor de un campo con una
# cláusula “WHERE” que seleccione varias filas (entre 5 y 20). Aumentaremos en 5 puntos el adjusted_satisfaction de los países con income_inequality superior a 40
cursor.execute("""
    UPDATE paises
    SET adjusted_satisfaction = adjusted_satisfaction + 5
    WHERE income_inequality > 40
""")
conn.commit()

# Obtener el nombre del país con mayor GDP
#Otra sentencia "SELECT" pero esta vez ordena los paises de manera descendente según su GDP y se queda solo con el primero
cursor.execute("""
    SELECT country FROM paises
    ORDER BY GDP DESC
    LIMIT 1;
""")
print("Pais con mayor GDP:", cursor.fetchone()[0])

# Realizar una sentencia “SELECT” que calcule realice el agrupamiento de datos por una
# columna y realice una operación de agregación (suma, media …) sobre otra columna en este caso media de happyScore por región
cursor.execute("""
    SELECT region, AVG(happyScore) FROM paises
    GROUP BY region;
""")
print("\nPromedio de happyScore por región:") #Sacamos por pantalla
for row in cursor.fetchall():
    print(row)

# Realizar una sentencia “DELETE” con una cláusula “WHERE” que seleccione varias
# filas (entre 5 y 20) para su eliminación. En este caso eliminamos varias filas con DELETE
cursor.execute("""
    DELETE FROM paises
    WHERE rowid IN (
        SELECT rowid
        FROM paises
        WHERE avg_satisfaction < 5
        LIMIT 10
    );
""")
conn.commit()  #utilizando rowid como subconsulta selecciona las primeras 10 filas que cumplen la condición avg_satisfaction < 5, y la consulta DELETE las elimina.

# Finalmente cerramos la conexión
conn.close()
