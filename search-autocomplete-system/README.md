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

$24.000 \text{ (QPS)} = \frac{1.000.000.000 \text{ (users)} \times 10.000 \text{ (queries/day)} \times 20\text{ (characters)}} {24 \text{ (hours)} \times 3600 \text{ (seconds)})}$

- Peak $QPS = QPS \times 2$
- Assume 20% of the daily queries are new.
- 0.4 GB of new data is added to storage daily

1.000.000.000 \text{ (users)} \times 10.000 \text{ (queries/day)} \times 20\text{ (bytes per query)} \times 20\% \cong 0.4 \text{ GB}
