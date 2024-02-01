# Information
Full Name: Mohammad Amin Karami

Student ID: 98105998

# How to Run the Code
The project is written in Python.
To execute the code, follow these steps:

1. Open your terminal/console.
2. Navigate to the project directory.
3. Run the following command to start the server:

```bash
make run-server
```

4. To remove the virtual environment when you're done, run the following command:

```bash
make clean
```

# Code Description
The implementation is located in the `src` directory.

To enable the code to respond in parallel, asyncio is used.

When the module is executed, the `start_proxy_server` function is called, which creates a server and passes client streams as input to the `handle_client` function.

### `handle_client` Function
In the `handle_client` function, based on the request sent to the server, a TCP connection is established between the proxy server and the corresponding host. Then, depending on the method specified in the request, one of the `forward_http` or `forward_https` functions is called, and finally, the connections related to the request are closed.

### `forward_http` Function
In this function, a request related to the target is first created based on the request. Then, this request is sent to the target, and the `perform_forwarding` function is called.

### `forward_https` Function
In this function, the response related to the establishment of a connection between the proxy server and the target is sent to the client. Finally, the `perform_forwarding` function is called.

### `perform_forwarding` Function
In this function, the main operation of the proxy server takes place. Data read from the target is sent to the client, and data coming from the client towards the proxy server is sent to the target. This transfer is done through the `_forward` function.