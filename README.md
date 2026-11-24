# India import-shock cascade (Neo4j + NLP + input-output, no ML)

## Run in VS Code
1. Install Python 3.10+ and Neo4j (easiest: Docker)  
   `docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5`  (or free Neo4j Aura: set NEO4J_URI to its `neo4j+s://` address)
2. Open this folder in VS Code. Terminal: `python -m venv .venv`, activate it, then `pip install -r requirements.txt`
3. Copy `merged_master_trade_data2.csv` and `MoSPI_Industry_Input_Output_Matrices23.xlsx` into `./data`
4. Try without any database first: `python test_offline.py`, then `set OFFLINE=1` (Windows) / `export OFFLINE=1` (Mac/Linux) and `uvicorn server:app --reload`
5. With Neo4j: set `NEO4J_PASSWORD` if different, run `python load_neo4j.py --wipe` once (loads every month since 2011), then `uvicorn server:app --reload`
6. Open http://127.0.0.1:8000 : pick supplier, goods and how much stops. (Optional text mode: `python main.py "If Russia stops oil exports"`)

## Graph in Neo4j
`(Country {name,lat,lng}) -[:SUPPLIED_TO_INDIA {ym, usd}]-> (Commodity {hs,name,refill})` one relationship per month since 2011  
`(Commodity)-[:FEEDS {dep}]->(Industry)` and `(Industry)-[:SUPPLIES_INPUT {c}]->(Industry)`

## Files
config.py (assumptions, coordinates) · data_files.py · io_model.py (cascade + Neo4j queries) · service.py · server.py · static/index.html (screen) · offline_graph.py · load_neo4j.py · nlp_parser.py + main.py (optional text mode) · test_offline.py

## Know the limits
- Import-dependence per good and SPREAD_STRENGTH (0.6) are assumptions in config.py. Calibrate with the backtest.
- "Refill by other suppliers" is a plain historical average (event study), not a prediction.
- The screen loads COBE from the internet (`cobe@latest`). If a newer COBE changes its API, the page falls back to older versions, and says so under the globe.
- Neo4j loading and queries are untested by the author (no database in the build sandbox). Fix small Cypher issues if your Neo4j version differs.
