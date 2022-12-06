# A Implementation for URL Shortener

## Requirement

- Assume URL https://github.com/hoangperry/2d-chatbot is the original URL. Your service creates an alias with shorter length:
https://hoang.tech/abcxyz. If you click the alias, it redirects you to the original URL.
- Traffic volume: 100.000.000 URLs generated per day, mean 1160 write ops/s. 
- Assume read ops is 10 times with write ops, read ops is 11600 ops/s
- The URL as short as possible, assume average is 100
- URL can be a combination of numbers and characters
- URL cannot be deleted or updated

## Design

1. **Endpoints:**
   - URL shortening: to create new short URL, client sends a POST request, 
   which contains one parameter: the original URL:
     - POST: `api/v1/data/shortern` 
     - Request: `{long_url: long_url_string}`
     - Return: `short_url`

    - URL redirecting, to redirect a short URL to the corresponding original URL, client sends a GET request:
      - GET `api/ai/short_url`
      - RETURN `HTTP redirection`

2. **URL Redirecting:**
   - **301 Redirect:**  URL is permanently moved to the long URL. The browser caches the response, 
   and subsequent requests for the same URL will be sent to the URL shortening service first. 
   Then they are redirected to the original URL server.

   - **301 Redirect:** URL is temporarily moved to the long URL. 
   Meaning that subsequent requests for the same URL will be sent to the URL shortening service first.
   Then they are redirected to the long URL server.

    - Each method has its pros and cons. If the priority is to reduce the server load, 
   using **301** makes sense as only the first request of the same URL is sent to URL shortening servers.
   However, if analytics is important, 302 is a better choice as it can track click rate and source of the click more easily
    
    - The most intuitive way to implement URL redirecting is to use hash tables. Assuming the hash table store <short_url, origin_url> pairs

3. **URL Shortening:**

    - Let us assume the short URL looks like this: `https://hoang.tech/{hash_value}`. 
   To support use case, we must find a hash function fx that maps a long URL to the `hash_value`. 
    - The hash function must satisfy the following requirements:
      - Each long URL must the hashed to one `hash_value`
      - Each `hash_value` can be mapped back the long URL


## Deep dive

1. **Data model:**
    - In the design, everything is stored in a hash table. 
   This is a good starting point, but this approach is not feasible for real-world systems as memory resource are limited and expensive.
    - A better option is to store <long_url, short_url> mapping in a relational database. The simplified version of the table contains 3 columns: `id, short_url, long_url`

2. **Hash function:**
    - **Hash value length:** the hash value consists [0-9, a-z, A-Z], mean 62 possible characters. To figure out the length of hash_value,
   find the smallest `n` such as 62^n >= 365 billion. The system must be support up to 365 billion URLs based on the back of the envelope estimation.
    - n=7, 62^n = ~3.5 trillion is more than enough to hold 365 billion URLs, so the length of hash_value is 7

3. **collision resolution:**
   - We should implement a hash function that hashes a URRL to a 7-char string.
   - The first approach is to collect the first 7 characters of a hash value; 
   however this method can lead to hash collisions. To resolve hash collisions, we can recursively append a new predefined string util no more collision
   is discovered. however it is expensive to query the database to check if a short URL exists for every request
   - A technique called bloom filters can improve performance. A bloom filter is a space-efficient probabilistic technique to test if an element is a member of a set
   

### TEST MATH

When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$ and they are 
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$
