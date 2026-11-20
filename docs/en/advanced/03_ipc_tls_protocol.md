# IPC Transport, TLS, and the Wire Protocol

When an application sends a batch of drawing commands to the Engine, the bytes must cross the boundary between two processes. On the server side, they must be split into complete messages, bound to the correct session, and then processed. The event returns in the opposite direction. Both sides also need to handle connection failures, timing, error attribution, and situations where requests and events overlap. This chapter starts with finding the service and ends with an IME test scenario to explain why responses and events need to be stored separately.

![from Bootstrap to TLS, then from background reception to UI thread](/images/en/advanced_tls_ipc_queues.png)

## 1. Why use TCP, TLS, and separate discovery pipelines

IPC generally refers to inter-process communication. Named pipes can connect processes on the same machine using named objects. Shared memory allows two processes to access the same area, but write rights, buffer boundaries, synchronization, and failure recovery still need to be specified separately. TCP provides an ordered byte stream and cross-machine addressing. TLS handles encryption, integrity, and server identity on this stream. After choosing TCP and TLS, both local and remote can share the same frame division, session, request, and event protocols.

Named pipes are still suitable for small-scale local discovery. The Engine publishes the connection description after current initialization is completed through `\\.\pipe\EasyVROverlayUIEngine.Bootstrap`, and the pipeline configuration rejects remote clients. The SDK reads ports, service process numbers, access credentials, and public key fingerprints from the local pipe, then returns the address in sequence. There is no need to guess whether a configuration file belongs to the current service, nor to replicate the server port and certificate implementation in the application process. The pipe also delivers its description using a length header and JSON. Its role is to complete after obtaining connection materials; persistent online data goes through TCP/TLS.

After installation, the Engine and its configuration are located in `bin/easyvrui_engine.exe` and `bin/config.json` respectively. The configuration saves the service port and shared access credentials. The default port is 49537, and the service establishes both IPv4 and independent IPv6 listening. The SDK uses a loopback address for local discovery. `EASYVRUI_ENGINE` specifies the Engine executable file for local automatic startup. Explicit remote connections use `--easyvrui-host=值`, `--easyvrui-port=值`, `--easyvrui-access-credential=值`, and `--easyvrui-public-key-fingerprint=值`, using 49537 when ports are omitted.

When placing the application and engine on two computers, only the machine where the Engine is located needs SteamVR and the GPU responsible for rendering. The machine where the client is located handles controls and callbacks, and the network transmits submissions and events to the other machine. Remote calls' sensory experiences are affected by round-trip latency, frame size, and queue backlog. Changing tag attributes to new values is still a local operation on the client, only crossing machines during the submission stage. Measurements that require waiting for returns, startup status, or management operations are distinguished by their respective public interface semantics as synchronous returns or asynchronous completion.

## 2. TLS Identity and Self-Signed Key Startup Self-Inspection

When a connection is established, the network address seen by the SDK only indicates that it has accessed a certain service. To verify the identity of the other party, the client reads `SubjectPublicKeyInfo` from the TLS certificate of the other party, encodes the structure in DER, calculates SHA-256, and then compares the result with the fingerprint obtained from discovery or remote configuration. The public key fingerprint is a public identity identifier. A self-signed certificate is sufficient to carry this public key, and the client has access to a trusted fingerprint through local discovery or remote configuration. The specific fingerprint of the public key is different from the hash of the entire certificate and is not a token used in subsequent sessions.

The client driver `channel.cpp` uses Schannel handshake, disabling SSL2, SSL3, TLS1.0, and TLS1.1. TLS handshake and subsequent application layer authentication have their respective responsibilities. TLS provides a verified channel for messages. Application layer authentication proves that the requesting party can complete challenges based on shared credentials. Thus, even if the network connection is established, the client still needs to complete protocol authentication to have a working session. When reading logs, observe whether errors occur during TLS handshake, fingerprint verification, or subsequent authentication stages.

The Engine uses the current Windows user's personal certificate storage and CNG key storage in `tls_server.cpp`. The service first opens the existing private key by specific container name, verifies that `NCRYPT_ALGORITHM_PROPERTY` corresponds to the algorithm of `ECDSA_P256`, and requires the key length to be 256 bits. Filtering by certificate subject only finds candidate certificates; it still needs to verify the key provider association and the real signature match. Two keys with the same name, same algorithm, and same bit length may come from different generation processes.

The actual pairing check can be understood through the following causal relationship.

1. A 32-byte digest is generated from the system's random source as the local verification data for this process.
2. The `NCryptSignHash` is called with the currently opened private key to retain the signature.
3. The public key is imported from the candidate certificate and verified against this signature using `BCryptVerifySignature`.
4. Only when the algorithm, candidate certificate requirements, and signature match will this set of resources be reused. Otherwise, a new persistent ECDSA P-256 key and self-signed certificate are generated, and a publishable fingerprint is then checked and calculated.

This verification is not a round of authentication message sent to a remote client. It addresses whether the private key and certificate prepared locally are paired. If the pairing fails and a new key is generated, the public key fingerprint will also change. Clients detected by the local Bootstrap will read the current value. Clients configured with a fixed remote fingerprint need to reconnect using new trusted materials. The topic name alone cannot explain this change; authentication based on the public key is needed to distinguish between re-generation and network errors.

## 3. Restoring complete JSON from the continuous byte stream

### Why doesn't the main data transmission directly reuse the local pipeline?

If only one local process sends a message to another process, the pipeline can still function. The design choice depends on the deployment goal. When the program is moved to a second machine, target addressing, reliable transmission, server identity, and shared credential authentication are also required. If both the local and remote sides use different data protocols, message fragmentation, heartbeat, timeout, response matching, and fault diagnosis need to be maintained separately. Using the same data channel allows the application to first verify the code and messages locally, then hand over the capture or presentation to the Engine in another machine. Only a short discovery action is retained locally, taking advantage of the operating system's access boundaries to named pipelines, without needing to send credential configurations to all applications for storage.

Shared memory can reduce copying in certain large-scale data scenarios, but it requires handling shared layouts, producer-consumer synchronization, reclamation after process crashes, and cross-process references. If it directly shares rendering instructions, it must ensure that the other side cannot observe a half-published instruction. When spanning machines, this data still needs to be translated into some transport protocol. This project expresses shared semantics using windows and drawing nodes, then relies on caching and deferred submission to reduce transmission volume. Benefits should be evaluated based on actual window update frequency and submission counts. An application that frequently refreshes large images may consume more bandwidth than one dealing with text or menus; reusing connections does not automatically offset load differences. ZZZ-001 ZZZ-002 ZZZ-003

Local discovery should be viewed as a single startup cycle. The service publishes after preparing for actual listening and public key fingerprint, and the client verifies the version, non-zero port, and connection materials. If the description is generated before the new service starts or has been cached multiple times, the old port and new service may differ, and even the old public key may have changed due to re-generation. Troubleshooting can only record the discovery phase, port, or error key, without writing complete shared credentials to the log. Remote startup parameters are also sensitive configuration on the deployment side, and the fingerprints used for comparison can be independently verified. Identity protection and visible information required for debugging can be designed separately.

### Decoding progress is calculated with three short reads.

Assuming the length header of a frame is `05 00 00 00 00 00 00 00`, and the body is the valid JSON text `false`. The first read gets three bytes `05 00 00`; the head length is now 3, with 5 remaining. The second read gets the remaining 5 head bytes and two payload bytes `fa`; the parser completes the head and gets a length of 5, with 3 remaining. The third read gets `lse`, resulting in a complete value. If the third data also includes the head of the next frame, the extra data must be retained and continued with the new head. These three segments are just for demonstrating the reading boundaries. The message body of normal Engine operations requires objects and fields as agreed upon by the protocol, and boolean values alone cannot form valid requests.

From the perspective of the length prefix, it can also be explained why we read full frames before interpretation. If the first byte `05` is parsed as 5, there may be higher bits in the subsequent head fields, and the actual frame length will be completely different. If we break the frame at the first line break in the string, multi-line JSON will be truncated, and escaped line breaks in the JSON string will also make human logs differ from the leading length. A fixed head length plus a clear number of body bytes eliminates the need for the decoder to guess the content. String escapes, indentation, and column positions are all part of the internal format; only bytes are counted when reading frames.

During debugging, the frame header arrangement, complete UTF-8 encoding, JSON syntax, and protocol fields can be verified separately. Premature end of length often occurs in byte calculation or short reading. If JSON can parse the object but the operation fails, the field types and boundaries should be checked. Using hexadecimal for the header and UTF-8 for the body can often reveal situations where the "integer value is correct but the end order is reversed." Collaborative testing can also send multiple small bodies at once, dividing the input into fixed slices to confirm that framing, decoding, and buffer behavior are consistent with expectations.

TCP promises to deliver bytes in order, not preserving the read/write boundaries as application layer messages. The sender continuously writes one request and one heartbeat, and the receiver may read half of the header length or part of two messages plus the next one. TLS encapsulates input into records according to its own rules, but application messages can also cross record boundaries. A reliable parsing method is to write a fixed-size header length before each message, reading the header full first, then reading the message body according to the number of bytes obtained from the header.

The project frame header is a 8-byte little-endian unsigned integer. If the message body occupies 258 bytes, 258 equals hexadecimal `0x0102`, and the little-endian header should be `02 01 00 00 00 00 00 00`. Define `B[i]` as the `i`th byte, with the value read from `i=0` to `7` summing to `B[i]·256^i`. In this example, the first two items are 2 and 256. When 8 bytes are zero or not fully read, it should be handled according to protocol validity and reading status; the number of bytes read on the first attempt cannot be considered the full frame length.

The length is the number of encoded UTF-8 bytes. In compact UTF-8, `{"s":"中"}` occupies 11 bytes, three of them for the Han character. Each quotation mark, colon, and brace contributes one byte. Count any spaces or line breaks that the JSON serializer adds. Encode the payload before measuring it so the frame header uses the byte count rather than the Unicode character count. Across language boundaries, preserve `uint64` exactly. Its upper bound is `2^64-1`. If the JSON reader parses numbers as binary floating-point by default, choose an integer representation that can preserve the full range.

Binary fields such as drawing images are encoded using Base64 within JSON according to the protocol. It maps every 3 bytes to 4 ASCII characters, with a length of `4·ceil(n/3)`. When the end is insufficient, it is filled according to the encoding rules. The header statistics refer to the entire JSON byte string, not the original image size, nor the product of the image pixel width and height. Identifying these numbers can help locate issues with byte buffering, JSON fields, or rendering resources.

## 4. Four-step application authentication above TLS

### Challenge and session tokens should be tracked separately

Set up layer-application authentication to start only after TLS is completed. The random values currently used by both parties are only used to form this proof; subsequent drawing requests will not recalculate this pair of nonces for each packet. After successful authentication, the service issues a random token to the session and then checks the identity field of the request against the connection. These fields have different functions from `id`. The token identifies the same authenticated connection context, the request ID relates to a question-and-answer, and the nonce prevents previous authentication proofs from being directly used for another challenge. During debugging, by reading the error stage, it can be determined whether to check the public key, shared credentials, or session identity, without keeping these data in the same plaintext log.

When browsing the protocol, first record the sender and the next step, then examine the fields. Each handshake message is a complete frame. The four steps of layer-application authentication are: the client sends `client_hello`, the Engine sends `challenge`, the client sends `authenticate`, and the Engine sends `welcome`. The first item publishes the version, name, process number, and client nonce. Standard SDKs use the system's random source to generate 32-byte nonces, which are then converted into 64 hexadecimal characters. The service first verifies the message type and field type; the name must be non-empty. When the local connection process is verified, the declared PID must match the connection's ownership.

Below is the field structure of `client_hello`. For ease of reading, nonce uses fixed example values. The real client generates random values each time for new attempts.

```json
{
    "message_type": "client_hello",
    "version": 1,
    "client_nonce": "0000000000000000000000000000000000000000000000000000000000000000",
    "process_id": 4242,
    "name": "计数器"
}
```

`challenge` returns the version and newly generated `server_nonce`, and the client checks the version. `proof` is calculated by the client using HMAC-SHA256 on the specified text. The following `\n` indicates a single LF byte, with no additional trailing LF. Two nonce values are used from the hexadecimal text in the message, while the access credentials use original UTF-8 bytes. The calculation output is encoded as a lowercase hexadecimal string and sent as `authenticate.proof`.

```text
data = "easyvrui-ipc-auth-v1\n" + client_nonce + "\n" + server_nonce
proof = hex(HMAC-SHA256(key = UTF8(access_credential), data = UTF8(data)))
```

HMAC ensures that both parties holding the same credentials get the same result. Roughly speaking, it doesn’t concatenate the credentials into the message but uses a key to create an irreversible verification. The service recalculates the expected value based on its own credentials and compares them. If someone gets the proof from the previous challenge, the next service nonce will be different, and the byte string input to HMAC will also differ, making the old proof ineffective for this challenge. The anti-replay scope here is the application-layer authentication between different challenges. After successful authentication, the ownership of subsequent messages is continued to be verified by the connection and session token.

`welcome` returns the protocol version, `session_id`, random `session_token`, service PID, verifiable owner PID, and creation time semantics. The PID of the remote client can be displayed as declaration information, while local process management relies on system authentication. See [Chapter 04 for details on](./04_session_and_context.md). TCP pre-connection or assigned numbers do not indicate that authentication is complete. `ipc_connection::implementation` enters the verified state and normal request reading phase only after the handshake is completed.

### Recompute one round trip using publicly available fictional values.

Set the access credential to `tutorial-credential`, using the client’s nonce that was all zeros before, and the service challenge example uses 64 `1`. These three values are only for educational purposes. The real Engine uses this random challenge and configured credential.

```json
{
    "message_type": "challenge",
    "version": 1,
    "server_nonce": "1111111111111111111111111111111111111111111111111111111111111111"
}
```

Using the above LF-separated format and UTF-8 key bytes, the following result is obtained. If different results are calculated, check one by one the trailing LF, space, and nonce to see if they are correctly encoded into 32 bytes, and whether the output has the expected 64 characters.

```json
{
    "message_type": "authenticate",
    "proof": "edad0de1f314ff105b236e2098b1699182061f9db9badbae7af9216bbfa7885a"
}
```

The service returns the session description after verification. The following example sets the service PID to 7000, retaining the client’s declared 4242. `owner_created=0` indicates that this example does not have the verified local creation time. The sample token is only used for later request and response pairing; the real value is randomly generated by the Engine.

```json
{
    "message_type": "welcome",
    "version": 1,
    "session_id": 12,
    "session_token": "2222222222222222222222222222222222222222222222222222222222222222",
    "process_id": 7000,
    "owner_process_id": 4242,
    "owner_created": 0
}
```

## 5. Message types, numbers, and heartbeats

### Compare a request and response with identity information

TLS only protects the transmission. After reading the request object, the service still needs to match the session ID and token of the connection, checking operations and values. The following example uses session 12 and request number 17, closing the submitted window 7. The token follows the previous example. The real program uses the current connection token sent by `welcome`.

```json
{
    "message_type": "request",
    "session_id": 12,
    "session_token": "2222222222222222222222222222222222222222222222222222222222222222",
    "id": 17,
    "op": "surface_close",
    "window": 7
}
```

The response frame uses the same request number to associate the result. If the client receives frames from another session, it will notice inconsistencies during the session verification phase. In the same session, other responses or window events may also be received first. In such cases, check the session fields, request numbers, and reception order separately, answering “which connection does it belong to,” “which operation is it responding to,” and “when it was read.” If the user logs mix these three numbers into the same ID, it will be difficult to explain the concurrent submission results.

```json
{
    "message_type": "response",
    "session_id": 12,
    "session_token": "2222222222222222222222222222222222222222222222222222222222222222",
    "id": 17,
    "ok": true,
    "value": null
}
```

The asynchronous requests here also do not require the service to complete all operations in the order of sending. One operation may wait for component confirmation, while another only needs to verify the object. The frames actually sent by the service form an ordered byte stream. The client retains this actual sending order and matches with the callback by ID. Using the stream sequence number for blind response ID matching, or sorting service events by request ID, will result in the loss of another necessary piece of information.

`message_type` distinguishes between authentication messages, `request`, `response`, `event`, and `heartbeat`. The requested `op` specifies the action, and `id` associates a request with a response. The completed response has `ok` and corresponding result values or errors. Service-initiated input, tracking, or window state updates are `event`, distinguished by `event_type`. It has no reason to occupy the callback of a certain request; events can arrive at any main loop cycle.

The authenticated frames are verified against `session_id` and `session_token`. The server saves the suspension request numbers to prevent incomplete requests with the same ID from being mixed together. When an application sends two different operations simultaneously, the order of return is determined by the actual completion of each operation and the sending queue. It's impossible to guess which response will arrive first based on numerical order. Therefore, the client's asynchronous path uses the ID in `pending` for callback matching, while the network arrival order is expressed with a separate number.

The keep-alive intervals between the client and Engine are approximately 1 second, with a timeout threshold of about 10 seconds. Connection activity is determined based on the time when data is received. Heartbeats keep normal connections with little interaction visible, preventing them from becoming clickable or key-related events in the application control tree. This 10-second interval is a unit of measure for transmission activity. The deadline for a synchronization call, the deadline for each empty stage of input components, and the deadline for asynchronous finishing when closing each have different starting points. During troubleshooting, it's important to identify from logs which stage has already begun waiting.

## 6. Diagnosis methods for crossing IPC, C ABI, and Python

Owned errors can include `error_diagnostic`, specifying the source file, line, column, function, and triggering condition. C++ uses `source_location` to capture the calling location, with conditions passed down from macros and other entry points. Transmissions can also include language keys, parameter lists, and messages. By saving location information and display text as separate fields, the other end can display single-line diagnostics and determine which condition failed based on structure. When there's only a single human-readable string, it's difficult for the receiver to always correctly distinguish between the original location and parameters.

For example, when the Engine verifies a submission, it throws an exception with an error key. The error details in the corresponding request response carry the original diagnosis. `connection::implementation::throw_request_error()` reads `language_key`, `message`, `argument_list`, and `diagnostic` from the details, restoring them to `request_error`. Even if the caller later receives a failure in the button event, the exception diagnosis can still point to the actual verification condition of the Engine.

The native client's internal C ABI also needs to transmit failure information at the boundary. C++ exceptions cannot normally pass through the C interface called by each language, so the internal implementation records errors as serialized details readable by the same thread, which are obtained by entries like `engine_interface_get_last_error()`. The connection layer's `throw_native_error()` parses the details and continues with unified error conversion. The Python extension's exception translation passes the available diagnosis to the corresponding exception object. The program can read attributes such as `file`, `line`, `column`, `condition`, and language keys from the diagnosis. When only an unknown standard exception is received, the diagnosis can usually be traced to the capture boundary. The separation of source code lines and display text allows language switching without sacrificing troubleshooting accuracy.

## 7. How dual queues separate synchronous waiting from event dispatch

`reader` in `connection.cpp` runs in the background. After the underlying session completes frame reading and parsing, the reading thread identifies the message according to `message_type` under the protection of the connection state lock. When encountering `response` and the ID matches the current `synchronous_id`, it is placed in the unique `synchronous_response` slot. Other responses are added to `response_list`. `event` is added to `event_list`. The latter two share the increasing serial number `next_sequence`. The event callback itself is executed in the owner thread's pump, and the reader's responsibility is to receive, store, and notify.

`request()`: First, the owner thread is required to open a connection and obtain a new ID. Then, `synchronous_id` is registered before sending the message. After sending, the thread waits for its own slot on the condition variable, or waits for changes in the session generation, disconnections, failures, or timeouts. During this waiting period, the state lock is released, allowing the background to continue receiving packets. Once the corresponding result is detected, the slot is retrieved and cleared. Finally, the success or error value is interpreted. Synchronous waiting does not call `pump_message_list()`, so there’s no need to run any other response callbacks, local deliveries, or server events to obtain this response.

The key lies in the order of registration and sending. When sending first and then registering, the response has a chance to see the empty slot ID in the background thread, thus being treated as an asynchronous response. If the code registers first, even if the response is quickly returned, it can be assigned to the correct position. The wait predicate cannot be omitted either. Receiving an event may also lead to notification, but after waking from the synchronous request, it still decides whether to end based on its own slot and error status.

Session algebra protects the lifecycle of connections. Requests from waiters belong to a specific connection algebra. When a connection is closed, retired, or replaced, the algebra can be used to prevent the state of an old request from being transferred to a new connection. Failed sends, timeouts, and other exceptions will clean up the synchronization state. The current connection uses a single synchronization slot, which is constrained by the owner thread. Therefore, it doesn’t need to be designed as a general-purpose RPC table where multiple threads can block simultaneously.

## 8. How do two queues regain the same order on the same line?

### ZZZ001 ZZZ002 ZZZ003 Verify the rationality of the split using three counterexamples.

The first counterexample is to execute pending callbacks within a synchronous request. Suppose the application is closing an editing window, and the closing callback is waiting for a synchronization service result. The local code sets a flag indicating progress but has not yet completed cleanup. If another click is assigned automatically during the wait, the business may attempt to use the editor in an intermediate state again. Protecting all APIs with just a local boolean value is difficult to maintain and will also affect normal modal nesting. A single response slot makes ordinary synchronous waits become a narrow path. The network continues to move, and application callbacks are executed only at the agreed pump entry.

The second counterexample is to process all events before all responses in each round. There is an earlier response that updates the window state, and the subsequent event depends precisely on that state. Processing events in a fixed order creates the opposite reverse sequence. For example, the application waits for the service to return an available state submitted for the initial window, and subsequent events explain dependencies on the synchronized context. Fixed priorities cannot generally express protocol causality. Comparing the queue numbers at the heads of two queues retains the actual sequence in the same receive stream, without rereasoning which response each event depends on.

The third counterexample is to take the entire queue and then execute the callback. The outer layer moves messages A, B, and C from the shared queue to a local array and then executes A. A opens a new modal window and waits for results or events associated with B and C. The inner layer cannot see the work temporarily stored by the outer array, and the outer layer waits for the inner layer to return. The current implementation takes only one message at a time in the lock, and after releasing the lock, unexecuted messages can still be taken by the inner layer. For debugging, this also keeps clear which “is being processed” and “how many remain in the shared queue”.

The deadline number handles the scope of one round of consumption. Suppose each user callback performs some task at `post`. If the pump waits for the queue to be completely empty and continuously receives tasks, this round may never end, leading to starvation due to refreshing and timing. Grabbing the water level when entering the pump and leaving future work to a new pump can give other stages a chance to run. When explicitly entering the modal cycle, there is a new pump water level, which is a natural result of the business deciding to continue interaction. Two layers use the same queue and consume work based on the first arrival, with the outer layer continuing from the current head later.

### Determine which thread is waiting: the read thread, I/O session, or UI thread.

The application may immediately send a synchronous request from the window callback. After sending, the application thread sleeps on the condition variable. The underlying client is responsible for TLS byte reading and writing and heartbeat. The reader of `connection` reads the formed message from the underlying C ABI, fills the slot after matching the current synchronization ID, and wakes up. When the UI thread gets the result, many other tasks may already be waiting in the network queue. This period can simultaneously have “active background reception” and “interface callback pause”. When the user sees the interface stuck, it should not be first attributed to a TCP stop, but also the time from the synchronization send to the corresponding response should be measured. If the application must allow the user to continue interacting with the window, the asynchronous entry provided by this operation or phased organization of business should be used.

On the other hand, it is not guaranteed that the thread will receive a response quickly. The service may have rejected an incorrect request, the connection may have expired, serialization may have failed, or the successfully waited response may not have arrived yet. In this case, the exception priority will carry the available original diagnosis. Blind re-sending may make an operation that has already succeeded but not received a response execute again. Whether retrying is safe depends on whether the operation itself can be repeated, whether the old session is still valid, and whether the application knows that the service has changed state. `present`'s batch isolation and retry rules are described in Chapter 05 of [,](./05_rendering_pipeline.md). Do not apply them directly to all RPCs.

Asynchronous responses and events occupy separate queues but receive sequence numbers from the same counter. On entering `pump_message_list()`, the UI thread saves `cutoff = next_sequence`. It compares the queue heads, selects the smaller sequence number, and dispatches only work received before the cutoff. The pump removes each message under the lock and releases the lock before calling user code. A callback can then start a nested modal loop safely. That loop takes its own cutoff and consumes eligible work.

Manual calculation round. Asynchronous request 17 corresponds to the hidden input area. Before the response arrives, the last item `ime_submit` is received and assigned number 40 to be placed in the event queue. Subsequently, response 17 is assigned number 41 and placed in the response queue. If the cutoff value at the start of the pump is 42, the text event will be executed first, followed by the shutdown completion callback according to number 17. If request number 40 is being processed at the same time, and a regular event with number 42 is received, it will be left for the next pump or handled by a more internal pump that has legitimate access. The comparison is based on the order of receipt, regardless of the request number.

The `callback_list` generated by the local `post()` also uses the cutoff value to determine whether it belongs to this round. The code first merges and processes network asynchronous responses and events, and then handles local callbacks. Therefore, the network order here does not mean that all three types of work are combined into a single global queue. Synchronous request-specific responses also go into their own slots. This ensures that network messages from adjacent connections are processed properly, while avoiding the need to wait for a synchronous result before executing application callbacks.

According to the example above, if the pump always executes all responses first, followed by all events, the shutdown completion might occur before the last text segment. The SDK may miss the right moment to send the text to the old editor that is being shut down. On the Engine side, serial draining allows the successful path to send the old text first and then complete the shutdown. The client preserves this causal order by number. Only by solving half of each side can a cross-process input switch be truly closed. For the complete component timing, see Chapter 06](./06_input_routing_and_drain.md) of [.

## 9. Which path does waiting, emptying, and error recovery take?

`wait_until()` is used in the main loop to sleep when there's no activity. It will control its operation based on network queues, local callbacks, disconnection, stopping callback reception, or reaching a given cutoff time. It does not execute callbacks; consumption occurs at the next pump. `drain()` is an auxiliary process at the client's end, continuing to pump messages around pending asynchronous requests and callbacks, with its own limits and error delivery paths. The emptying commands between the Engine and input components focus on the old input path and component tasks, although their names are similar and their objects are different.

Imagine a key event triggering a copy operation, while the business synchronously reads service data within the callback. The reader may first receive window event C, followed by the response to that request. Regular synchronous requests should return directly after their responses arrive, with event C remaining in the event queue. When the outer callback returns to the main loop or the application explicitly enters a supported modal message loop, C will be dispatched. This arrangement allows the call stack to execute in the order written in code, providing a foundation for the multi-layer synchronous modal of Chapter 04](./04_session_and_context.md) of [.

During debugging, three moments can be recorded for the same event: "Background received," "Entered queue," and "UI executed." If the background receives the text first and the UI is still busy in the previous time-consuming callback, the delay comes from the application thread. If the network has already received the text and response, but the callback order is reversed, the selection conditions for the two queue heads need to be checked. If a synchronous request is waiting indefinitely, check whether its ID is registered and whether it has arrived, excluding service rejection, disconnection, and timeout. The three types of errors are diagnosed at different levels, and they can be linked back to a timeline using the same session, request ID, and number.