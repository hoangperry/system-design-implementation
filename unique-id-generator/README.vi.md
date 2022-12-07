# Implementation of Unique ID Generator in distributed systems

`this is a implementation of chapter 7 in the System Design Interview books`

## Yêu cầu hệ thống

- IDs phải là duy nhất
- IDs là các chữ số
- IDs tối đa 64-bit
- IDs có thể sắp xếp theo thời gian tạo
- Hệ thống phải đảm bảo tải 10,000 unique IDs trên 1 giây

## Kiến trúc tổng quát

1. Muli-master replication
  - Phương pháp này sử dụng tính năng tự động tăng ID của database. Thay vì tăng ID bằng 1 đơn vị, phương pháp này tăng bằng $k$ đơn vị, với $k$ là là số server sử dụng
  - Cách này giải quyết được việc mở rộng của hệ thống bởi vì IDs có thể mở rộng theo số lượng server.
  - Nhưng phương pháp này cũng có một số điểm yếu
    - Khở mở rộng khi áp dụng cho nhiều datacenter
    - IDs không tăng theo trình tự thời gian giữa các server, bởi vì việc tăng giữa các server là riêng lẽ không đồng bộ
    - Không thể tự động mở rộng hoặc thu hẹp khi cần thêm hoặc gỡ server.

2. UUID
  - UUID là một cách đơn giản khác để tạo ra IDs duy nhất. UUID là một dãy số 128-bit dùng để định danh các thông tin trên cùng một máy tính. UUID có xác suất rất thấp để gây ra tình trụng trùng lặp. `Nếu mỗi giây chúng ta sinh ra 1.000.000.000 (1 tỷ) IDs trong vòng xấp xỉ 100 năm thì khả năng tạo ra một ID trùng lặp trên cùng 1 server là 50$ - Wikipedia`
  - Với cách này, mỗi máy trong hệ thống sẽ chứa một bộ tạo ID, và các bộ tạo ID này hoạt động độc lập với nhau.
  - Ưu điểm:
     - Đơn giản, không cần đồng bộ giữa các server
     - Hệ thống dễ mở rộng bởi vì các server chỉ tạo IDs mà nó sử dụng.
  - Nhược điểm:
    - ID có độ lớn là 128-bit, nhưng yêu cầu hệ thống ở trên là 64-bit
    - ID không tăng dần theo thời gian
    - ID có thể chứa các ký tự không phải số

3. Ticket server
  - Các lập trình viên của Flicker đã phát triển một hệ thống phân phối khóa chính.
  - Ý tưởng là sử dụng một bộ tăng ID tự động tập trung chạy trên một server, server này gọi là Ticket Server
  - Ưu điẻm:
    - Các ký tự trong ID là số.
    - Dễ để hiện thực hóa.
    - Phương pháp này có áp dụng được cho các hệ thống kích thước nhỏ và vừa.
  - Nhược điểm:
    - Việc chỉ sử dụng một Ticket server duy nhất có nghĩa là khi server Ticket sập nó sẽ kéo theo nhưng phần còn lại trên hệ thống có liên quan sập theo. Thể giải quyết vấn đề này chúng ta có thể dụng nhiều Ticket server. Nhưng khi tối ưu bằng cách này chúng ta cũng phải đối đặt mới một vấn đề khác là đồng bộ giữa các server

4. Twitter snowflake:
  - Thay vì tạo trực tiếp ID, cách này chi ID ra thành nhiều phần như sau:
    - Bit đánh dấu: là bit đầu tiên trên dãy ID, mặc định sẽ là không. Việc tạo ra ID này là để dự phòng cho cách mục đích khác trong tương lai. Nó có thể biến đổi giữa bị đánh dấu hoặc không đánh.
    - Timestamp: 41-bits, Đây là thời gian dưới dạng milisecond theo mốc cố định.
    - Datacenter ID: 5-bits, với 5-bits chúng ta có thể có tối đa $2^5$ = 32 datacenter 
    - Machine ID: 5-bits, với 5-bits này mỗi datacenter có thể chứa tối đa $2^5$ = 32 server
    - Chuỗi tăng dần: 12-bits, Với mỗi ID được tạo ra trên máy chủ hoặc luồng xử lý, số thứ tự tăng bằng 1, và số này sẽ reset về 0 sau mỗi milisecond

## DEEPER

Chúng ta hãy nói sâu hơn về các tiếp cận của Twitter

- DatacenterID và MachineID: Được chọn bằng thời gian khởi dộng của các server, được cố định mỗi khi server khởi động. Bất kỳ thay đổi nào trên MachineID và ServerID cần được kiểm tra cẩn thận để tránh bị xung đột.
- Timestamp: Đây là phần quan trọng nhất của ID, đây là lý do ID có thể sắp xếp được theo thời gian
- Sequence Number: với độ lớn 12-bits, dãy này có thể tạo nên 4096 số. Có thể fill số bằng này bằng 0 nếu nhu không có hơn 1 ID được tạo trong 1 millisecond.
- Về lý thuyết, mỗi máy có thể tạo ra 4096 ID mỗi 1 milisecond, Chúng ta có thể mở rộng tối đa 32 * 32 = 1024 servers. Việc này đồng nghĩa với cách này chúng ta có thể tạo ra tối đa 1024 * 4096 * 1000 = 4.194.304.000 mỗi giây.

