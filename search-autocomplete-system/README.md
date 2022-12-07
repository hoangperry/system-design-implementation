# Implementation of Search Autocomplete System

## Requirement of the design

- The matching only supported at the beginning of a search query
- Return 5 suggestions determined by popularity, decided by the historical query frequency
- No support spell check or autocorrect
- Multi-language support
- Assume all search queries have lowercase alphabetic characters
- 10.000.000 DAU
- Fast response time, reveals that the system needs to return results within 100 milliseconds

## Estimation

- Assume 10.000.000 daily active users.
- An average person performs 10 searches per day.
- 20 bytes of data per query string. 
Assume we use ASCII character encoding. 1 character = 1 byte
Assume a query contains 4 words, and each word contains 5 characters on average, that is $(4x5=20)$ bytes per query
- For every character entered into the search box, a client seeds a request to the backend for autocomplete suggestions.
On everage, 20 requests are sent for each search query.
- ~24.000 query per second (QPS) 

$(24.000 \text{ (QPS)} = \frac{1.000.000.000 \text{ (users)} \times 10 \text{ (queries/day)} \times 20\text{ (characters)}} {24 \text{ (hours)} \times 3600 \text{ (seconds)})})$

- Peak $QPS = QPS \times 2$
- Assume 20% of the daily queries are new.
- 0.4 GB of new data is added to storage daily. 10.000.000 * 10 * 20 * 20% = 0.4GB

## Design

1. Data gathering service
    - Assume we have a frequency table that stores the query string and ít frequency.

2. Query service
    - Assume we have a frequency table has 2 field
      - Query: it stores the query string.
      - Frequency: it represents the number of times a query been searched.
    - To get top 5 frequency searched queries, execute the following SQL query:
      - `SELECT * FROM f_table WHERE query like 'prefix%' ORDER BY frequency DESC LIMIT 5`
    - This solution is acceptable when the data set is small. When it is large, accessing the database becomee
   a bottleneck

## Deep dive

1. Trie data structure
- Relational databases are used for storage in high-level design. 
However, fetching the top 5 search queries from a relational database is inefficient
- The data structure trie (prefix tree) is used to overcome the problem. 
- The main idea of trie consists of the following:
  - A trie is a tree-like data structure.
  - The root represents an empty string.
  - Each node stores a characters and has 26 children one for each possible character.

- To support sorting by frequency, frequency info needs to be included in nodes. 
- How does autocomplete work with trie:
  - $p$: length of a prefix
  - $n$: total number of nodes in trie
  - $c$: number of children of a given node

- Steps to get top $k$ most searched queries are listed below:
  1. Find the prefix. Time complexity $O(p)$
  2. Traverse the subtree from the prefix node to get all valid children. 
  A child is valid if it can from a valid query string. Time complexity $O(c)$
  3. Sort the children and get top k. Time complexity: $O(clogc)$
- The time complexity of this algorithm is the sum of time spent on each step: $O(p) + O(c) + O(clogc)$
- The above algorithm is straightforward. However, it is too slow because we need to traverse the entire trie to get top $k$
There are two optimizations:
  1. Limit the max length of a prefix
  2. Cache top search queries one by one



