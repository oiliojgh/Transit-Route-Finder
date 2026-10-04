# Transit Route Finder

A route-planning tool for public transit networks, built on GTFS data. The project uses **pandas** to load, clean, and model real transit schedules, and implements **Breadth-First Search (BFS)** and **Dijkstra's algorithm** from scratch to compute optimal routes between stops.

---

## Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Dataset: GTFS](#dataset-gtfs)
- [Project Architecture](#project-architecture)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Testing](#testing)
- [Known Challenges](#known-challenges)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Public transit agencies publish their schedules in a standardized format called the **General Transit Feed Specification (GTFS)**. This project turns that raw tabular data into a **graph model** of a transit network and uses classic graph algorithms to answer a practical question:

> *Given a starting stop and a destination, what is the best way to get there?*

"Best" is evaluated under two different criteria:

1. **Fewest stops**, found using BFS.
2. **Shortest travel time**, found using Dijkstra's algorithm.

The project sits at the intersection of **data engineering** (cleaning and structuring messy real-world data) and **algorithms** (graph traversal and shortest-path search), showing how the two disciplines work together in a single application.

## Objectives

- Apply pandas to ingest, clean, and transform a large real-world dataset.
- Model a transit network as a weighted graph using an adjacency list.
- Implement BFS and Dijkstra's algorithm without relying on graph libraries.
- Compare the outputs of both algorithms and analyze why they differ.
- Practice handling real-world data issues such as duplicate entities, missing values, and non-standard time formats.

## Key Features

- **GTFS ingestion:** reads standard GTFS files into pandas DataFrames.
- **Data cleaning pipeline:** normalizes station names, handles missing values, and parses GTFS time formats, including times past `24:00:00`.
- **Graph construction:** builds a directed, weighted graph from trip and stop-time data.
- **Dual routing modes:** fewest-stops routing (BFS) and fastest-route routing (Dijkstra).
- **Path reconstruction:** returns the full ordered list of stops along the chosen route, not just the total cost.
- **Edge-case handling:** covers identical start and end stops, unreachable destinations, and ambiguous station names.

## Technologies Used

| Component | Purpose |
|---|---|
| **Python 3.9+** | Core language |
| **pandas** | Data loading, cleaning, merging, and grouping |
| **collections.deque** | Queue structure for BFS |
| **heapq** | Min-heap priority queue for Dijkstra's algorithm |
| **networkx** *(optional)* | Used only to validate results against a reference implementation |
| **folium / matplotlib** *(optional)* | Route visualization |

## Dataset: GTFS

GTFS is distributed as a ZIP archive of CSV-formatted `.txt` files. This project relies on four of them:

| File | Contents |
|---|---|
| `stops.txt` | Stop ID, name, and geographic coordinates |
| `routes.txt` | Route and line metadata |
| `trips.txt` | Individual trips, each linked to a route |
| `stop_times.txt` | Ordered stops per trip with arrival and departure times |

`stop_times.txt` is the most important of the four, since it defines which stop follows which and how long each leg takes.

**Where to find data:** many transit agencies publish free GTFS feeds on their open data portals. The [Mobility Database](https://mobilitydatabase.org/) is a good starting point. For development, a small city or single-mode feed is recommended, since large metropolitan feeds can contain millions of rows in `stop_times.txt`.

> **Note:** Dataset files are not included in this repository. Download a feed of your choice and place it in the `data/` directory.

## Project Architecture

The project follows a four-stage pipeline:

```
GTFS Files  →  Cleaning (pandas)  →  Graph Construction  →  Routing (BFS / Dijkstra)
```

1. **Load and explore:** read the GTFS files, inspect shapes, data types, and missing values, and join `stop_times`, `trips`, and `routes` into a unified view.
2. **Clean:** standardize station names, parse times, remove stops that never appear in any trip, and resolve duplicate stop entries.
3. **Build the graph:** for each trip, order its stops by `stop_sequence` and connect consecutive stops with a directed edge weighted by travel time. The result is stored as an adjacency list mapping each stop to its `(neighbor, weight)` pairs.
4. **Route:** run BFS or Dijkstra's algorithm on the graph and reconstruct the path using parent pointers.

## Algorithms

### Breadth-First Search (BFS)

Finds the route with the **fewest stops**. It treats every edge as having equal cost and explores the graph level by level using a queue, so the first time it reaches the destination is guaranteed to be via the fewest hops.

- **Time complexity:** O(V + E)
- **Data structures:** queue (`deque`), visited set, parent dictionary

### Dijkstra's Algorithm

Finds the route with the **shortest total travel time**. It uses a priority queue to always expand the closest unvisited node, relying on non-negative edge weights.

- **Time complexity:** O((V + E) log V) with a binary heap
- **Data structures:** min-heap (`heapq`), distance dictionary, parent dictionary

### Why Both?

The two algorithms can return different routes for the same pair of stops. A route with few stops may include slow legs, while a longer route with many quick stops may be faster overall. Comparing the two highlights the difference between **unweighted** and **weighted** shortest-path problems.

## Project Structure

```
transit-route-finder/
├── data/                  # GTFS files (not tracked in version control)
├── notebooks/             # Exploration and analysis notebooks
├── src/
│   ├── loader.py          # GTFS loading and merging
│   ├── cleaning.py        # Cleaning and normalization
│   ├── graph.py           # Graph construction
│   ├── bfs.py             # Fewest-stops routing
│   └── dijkstra.py        # Shortest-time routing
├── tests/                 # Unit tests
├── requirements.txt
└── README.md
```

*The structure above is a suggested layout and can be adapted as the project evolves.*

## Getting Started

### Prerequisites

- Python 3.9 or higher
- A GTFS feed (ZIP archive) from a transit agency

### Installation

```bash
git clone https://github.com/<your-username>/transit-route-finder.git
cd transit-route-finder
pip install -r requirements.txt
```

### Data Setup

1. Download a GTFS feed.
2. Extract it into the `data/` directory.
3. Confirm that `stops.txt`, `routes.txt`, `trips.txt`, and `stop_times.txt` are present.

## Usage

The intended interface takes a start stop, a destination stop, and a routing mode:

```bash
python -m src.main --from "Central Station" --to "Airport" --mode fastest
python -m src.main --from "Central Station" --to "Airport" --mode fewest-stops
```

Each query is expected to return the ordered list of stops, the number of stops, and the total estimated travel time.

*Command-line options may change as the project develops.*

## Testing

Planned test coverage includes:

- Routes where BFS and Dijkstra agree, and routes where they differ.
- Identical start and end stops.
- Unreachable destinations.
- Stops with duplicate or ambiguous names.
- Times beyond `24:00:00`.
- Cross-validation of results against `networkx` on sample queries.

```bash
pytest tests/
```

## Known Challenges

- **Duplicate stop entities:** a single physical station is often represented by several stop IDs (for example, one per platform or direction). Deciding how to merge or link them has a direct effect on route quality.
- **Non-standard time values:** GTFS permits times such as `25:10:00` for trips that continue past midnight, which standard datetime parsers reject.
- **Static schedule assumption:** the baseline version treats travel times as fixed and does not model time-of-day variation or real-time delays.
- **Data scale:** large feeds require efficient grouping and memory-conscious processing.

## Roadmap

- [ ] Add transfer penalties for changing lines
- [ ] Add walking connections between nearby stops using coordinate distance
- [ ] Implement A* search with a straight-line distance heuristic and benchmark it against Dijkstra
- [ ] Support time-of-day-aware schedules
- [ ] Visualize routes on an interactive map
- [ ] Add a command-line or web interface

## Contributing

Contributions, suggestions, and bug reports are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes with clear messages.
4. Open a pull request describing what you changed and why.

## License

This project is licensed under the [MIT License](LICENSE). Transit data is subject to the terms of the agency that publishes it; please review the license of any GTFS feed you use.

## Acknowledgments

- Transit agencies that publish open GTFS data
- The [GTFS Reference](https://gtfs.org/documentation/schedule/reference/) maintained by the GTFS community
- The pandas and Python standard library documentation
