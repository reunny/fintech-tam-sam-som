import pandas as pd

# --- TAM / SAM / SOM Computation Functions ---

def compute_tam(df, ticket_size):
    """Compute total addressable market based on all entities."""
    return len(df) * ticket_size


def compute_sam(df, filters):
    """Apply filters like region or AUM to get the serviceable market."""
    d = df.copy()
    if 'region' in filters and filters['region']:
        d = d[d['region'].isin(filters['region'])]
    if 'aum_min' in filters:
        d = d[d['AUM'] >= filters['aum_min']]
    if 'aum_max' in filters:
        d = d[d['AUM'] <= filters['aum_max']]
    return d


def compute_som(sam_df, arr_per_person, team_size):
    """Estimate the reachable market based on internal capacity."""
    capacity = arr_per_person * team_size
    reachable = min(len(sam_df), int(capacity))
    return reachable
