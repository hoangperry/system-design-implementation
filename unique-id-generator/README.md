# Implementation of Unique ID Generator in distributed systems

`this is a implementation of chapter 7 in the System Design Interview books`

## Requirement of the design

- IDs must be unique.
- IDs are numerical values only.
- IDs fit into 64-bit.
- IDs are ordered by date.
- Ability to generate over 10,000 unique IDs per second

## High-level design

1. **Multi-master replication approach:**
   - This approach use the databases *auto_increment* feature. 
   Instead of increasing the next ID by **1**, we increase it by **k**, where k is the number of database servers in use. 
   - This solves some scalability issues because IDs can scale with the number of database servers. 
   - This strategy has some major drawbacks: 
      - Hard to scale with multiple data centers.
      - IDs do not go up with time across multiple servers.
      - It does not scale well when a server added or removed.

2. **Universally unique identifier (UUID):**
    - A UUID is another easy way to obtain unique IDs. UUID is a 128-bit number used to identify information in computer systems.
   UUID has a very low probability of getting collusion. 
   `After generating 1.000.000.000 UUIDs every second for approximately 100 years would the probability of creating a single duplicate reach 50% - Wikipedia`
    - In this Design each web server contains an ID generator, and a web server is responsible for generating IDS independently.
    - Pros:
      - Generating UUID is simple. No coordination between servers is needed so there will not be any synchronization issues.
      - The system easy to scale because each web server is responsible for generating IDs they comsume. ID generator can easily scale with web servers.
    - Cons:
      - IDs are 128-bits long, but our requirement is 64-bits.
      - IDs do not go up with time.
      - IDs could be non-numeric.

3. **Ticket server:**
    - Flicker developed ticket servers to generate distributed primary keys.
    - The idea is to use centralized auto_increment feature in a single database server (Ticket Server)
    - Pros:
      - Numeric IDs
      - It is easy implement, and it works for small to medium-scale applications
    - Cons
      - Single ticket server means if the ticket server goes down, all systems that depend on it will face issues. 
      To avoid a single point of failure, we can set up multiple ticket servers. However, this will introduce new challenges such as data synchronization

4. **Twitter snowflake approach:**
    - Instead of generating an ID directly, we divide an ID into different sections:
      - Sign bit: 1 bit. It will always be 0. This is reversed for future uses. It can potentially be used to distinguish between signed and unsigned numbers.
      - Timestamp: 41 bít. Milliseconds since the epoch or custom epoch.
      - Datacenter ID: 5 bits, which gives us $(2^5 = 32)$ datacenters
      - Machine ID: 5 bít, which give us $(2^5 = 32)$ machines per datacenter.
      - Sequence number: 12 bits. For every ID generated on that machine/process, the sequence number is increment by 1 The number is reset to 0 every millisecond

## Deep dive

We will getting deep dive with Twitter snowflake approach.

- Datacenter IDs and Machine IDs: those are chosen at the startup time, generally fixed once the system is up running. 
Any changes in datacenter IDs and machine IDs require careful review since an accidental change in those values can lead to ID conflicts.
In this implementation I will use IP and hostname of machine with a hashtable instead.
- Timestamp: The most important 41 bít make up the timestamp section. As timestamps grow with time, IDs are sortable by time
- Sequence number is 12 bits, which give us $(2^12 = 4096)$ combinations. This field is 0 unless more than one ID is a milisecond on the same server. In theory, a machine can support a maximum of 4096 new IDs per millisecond