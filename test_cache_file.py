from pyiceberg.catalog import load_catalog
from pyiceberg.cache import LRUCache, MRUCache, NoCache

import time

CACHES = {"LRU Cache": LRUCache(), "MRU Cache": MRUCache(), "no Cache": NoCache()}

glue_database_name = 'iceberg_tutorial_db'
glue_catalog_uri = 's3://pyiceberg-proj-bucket/nyc-taxi-iceberg'
catalog = load_catalog("glue", **{"type": "glue",
                                  "s3.region": "us-east-1",
                                  })

# reduce file plans to just one
FILTERS_ = ['True', 'passenger_count == 7', 'False']

for cache_type, cache in CACHES.items():
    for filt in FILTERS_:
        total_time = 0
        for i in range(10):
            start_time = time.perf_counter()
            final_table = catalog.load_table(
                'iceberg_tutorial_db.nyc_taxi_iceberg').scan(row_filter=filt).to_arrow(cache)
            end_time = time.perf_counter()

            total_time += end_time - start_time
        
        print(f"cached retrieval for {cache_type} (filter: {filt}) took {(total_time/10):.6f} seconds")
        print(f"cache size in bytes: {cache.get_cache_byte_size()} bytes")
        print("\n-----------------------------------------------------------\n")

        cache.empty()
