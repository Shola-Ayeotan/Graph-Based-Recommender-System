import pandas as pd
import numpy as np
import duckdb
import time
import networkx as nx
import matplotlib.pyplot as plt

start = time.time()
con = duckdb.connect(database=':memory:', read_only=False)

# Product View Table
con.execute('''
CREATE TABLE product_view_tbl AS
SELECT 
user_id,
product_id, 
CAST(event_time[:-3] as DATETIME) as event_time, 
user_session
FROM '../Data/optimised_raw_data.parquet'
WHERE user_session in (SELECT 
user_session
FROM '../Data/optimised_raw_data.parquet'
WHERE event_type = 'view'
  AND user_session IS NOT NULL
  AND product_id IS NOT NULL
GROUP BY user_session
HAVING count(distinct product_id) > 1)
ORDER BY user_session, CAST(event_time[:-3] as DATETIME)
''').df()

# Edge List Query
con.execute("""CREATE TABLE product_views_graph AS select product_id, 
LEAD(product_id, 1, -1) OVER (PARTITION BY user_session ORDER BY event_time) as next_viewed_product_id,
user_session,
event_time
from product_view_tbl
""").df()

# Raw Unweighted Directed Graph with No PDP refresh cases
raw_unweighted_directed_graph = con.execute("""SELECT product_id AS pid_1,
       next_viewed_product_id AS pid_2
FROM product_views_graph
WHERE product_id!=next_viewed_product_id
  AND next_viewed_product_id<>-1
""").df()

raw_unweighted_directed_graph.to_parquet('../Data/ConstructedGraph/raw_unweighted_directed_product_views_graph.parquet',index=False)

# Directed Weighted Graph: Weight is Co-occurence count of two products
directed_weighted_graph = con.execute("""
SELECT product_id AS pid_1,
       next_viewed_product_id AS pid_2,
       COUNT(*) AS occurence_ct
FROM product_views_graph
WHERE next_viewed_product_id<>-1
  AND product_id IS NOT NULL
  AND product_id != next_viewed_product_id
GROUP BY 1,
         2
""").df()

directed_weighted_graph.to_parquet('../Data/ConstructedGraph/directed_weighted_product_views_graph.parquet',index=False)

# Undirected Weighted Graph: Weight is Co-occurence count of two products
undirected_weighted_graph = con.execute("""
SELECT CASE
           WHEN product_id > next_viewed_product_id THEN product_id
           ELSE next_viewed_product_id
       END AS pid_1,
       CASE
           WHEN product_id < next_viewed_product_id THEN product_id
           ELSE next_viewed_product_id
       END AS pid_2,
       COUNT(*) AS occurence_ct
FROM product_views_graph
WHERE next_viewed_product_id<>-1
  AND product_id IS NOT NULL
  AND product_id != next_viewed_product_id
GROUP BY 1,
         2
""").df()

undirected_weighted_graph.to_parquet('../Data/ConstructedGraph/undirected_weighted_product_views_graph.parquet',index=False)
